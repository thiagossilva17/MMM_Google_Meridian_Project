"""Reconciliação independente e revisão localizada, sem alterar thresholds."""
import dataclasses
import numpy as np
import pandas as pd
from .config import ROOT,KPI,POP,CONTROLS,NON_MEDIA
from .statistics import vif_table
from .reporting import table

def long_frame(array):
    f=array.to_dataframe(name='value').reset_index()
    if 'var' not in f:
        c=next((c for c in f if 'channel' in c),None)
        f=f.rename(columns={c:'var'}) if c else f.assign(var=KPI)
    if 'geo' not in f:f['geo']='NATIONAL'
    f['time']=f.time.astype(str).str[:10]
    return f
def source_variable(var):return var+'_impression' if var.startswith(('Channel','Organic_channel')) else KPI if 'kpi' in var else var

def compare_and_review(engine,outcomes,panel):
    from meridian.model.eda.eda_engine import stack_variables
    datasets={'geo':stack_variables(engine.treatment_control_scaled_ds),'national':stack_variables(engine.national_treatment_control_scaled_ds)}
    corr_rows=[];vif_rows=[]
    for level,array in datasets.items():
        f=long_frame(array);x=f.pivot(index=['geo','time'],columns='var',values='value');corr=x.corr()
        expected=outcomes[f'check_{level}_pairwise_corr'].analysis_artifacts[0].corr_matrix
        expected_vif=outcomes[f'check_{level}_vif'].analysis_artifacts[0].vif_da.to_series();custom_vif=vif_table(x,level).set_index('variable')
        for col in x:
            a=custom_vif.loc[col,'vif'];b=expected_vif.loc[col]
            vif_rows.append(dict(level=level,variable=col,custom_same_scale=a,official=b,absolute_difference=abs(a-b)))
        for i,left in enumerate(x):
            for right in x.columns[i+1:]:
                official=float(expected.sel(var1=left,var2=right));corr_rows.append(dict(level=level,left=left,right=right,custom_same_scale=corr.loc[left,right],official=official,absolute_difference=abs(corr.loc[left,right]-official)))
    correlations=table(pd.DataFrame(corr_rows),'official_correlation_reconciliation',False);vifs=table(pd.DataFrame(vif_rows),'official_vif_reconciliation',False)
    if correlations.absolute_difference.max()>1e-5 or vifs.absolute_difference.max()>1e-5:raise ValueError('Reconciliação de correlação/VIF falhou')
    raw=pd.read_csv(ROOT/'outputs/tables/correlation_summary.csv');comparison=[]
    for r in correlations.itertuples():
        left,right=source_variable(r.left),source_variable(r.right);level='overall' if r.level=='geo' else 'national'
        match=raw[(raw.level==level)&(raw.method=='pearson')&(((raw.left==left)&(raw.right==right))|((raw.left==right)&(raw.right==left)))]
        if len(match):comparison.append(dict(level=level,left=left,right=right,custom_raw=match.correlation.iloc[0],official_scaled=r.official,delta=r.official-match.correlation.iloc[0],reason='Geo: transformação populacional. Nacional: controles/Promo oficiais somados, custom ponderados por população.'))
    table(pd.DataFrame(comparison),'custom_official_scale_comparison',False)
    arrays={('geo',0):engine.kpi_scaled_da,('geo',1):datasets['geo'],('national',0):engine.national_kpi_scaled_da,('national',1):datasets['national']}
    cases=[];reconciliations=[];reviews=[];original=panel.copy();original['time']=original.time.dt.strftime('%Y-%m-%d')
    def review(check,artifact,finding,risk,decision,evidence):
        reviews.append(dict(review_id=f'REVIEW-{len(reviews)+1}',check=check,artifact=artifact,finding=finding,risk=risk,decision=decision,closure_criterion='localizações verificadas, magnitude quantificada, decisão justificada; sem remoção automática',status='encerrado para EDA simulada; REVIEW oficial preservado',evidence=evidence,residual_limitation='Não certifica plausibilidade comercial; influência/predição posterior serão avaliadas na modelagem.'))
    for (level,index),array in arrays.items():
        method=f'check_{level}_std';artifact=outcomes[method].analysis_artifacts[index];f=long_frame(array);keys=set();local=[]
        for (geo,var),g in f.groupby(['geo','var']):
            q1,q3=g.value.quantile([.25,.75]);lower=q1-1.5*(q3-q1);upper=q3+1.5*(q3-q1)
            for r in g[(g.value<lower)|(g.value>upper)].itertuples():
                keys.add((str(geo),str(var),r.time));col=source_variable(str(var));selection=original[original.time==r.time]
                if geo=='NATIONAL':value=selection[col].sum();pop=selection[POP].sum()
                else:
                    row=selection[selection.geo==geo].iloc[0];value=row[col];pop=row[POP]
                reason='Promo contínuo e zero-inflado; IQR não diagnostica erro' if col=='Promo' else 'Índice sintético com valores negativos admissíveis' if col in CONTROLS else 'Domínio válido; magnitude confrontada na escala oficial e dentro do nível/geo'
                local.append(dict(check=method,artifact=index,geo=geo,variable=var,time=r.time,raw_value=value,scaled_value=r.value,lower_bound=lower,upper_bound=upper,population=pop,raw_per_1000=value/pop*1000 if col not in CONTROLS+NON_MEDIA else np.nan,reason=reason,decision='manter no exemplo simulado; sem evidência de corrupção',limitation='plausibilidade comercial não demonstrada'))
        cases.extend(local);official=artifact.outlier_df.reset_index()
        if 'var' not in official:official['var']=KPI
        if 'geo' not in official:official['geo']='NATIONAL'
        expected=set(zip(official.geo.astype(str),official['var'].astype(str),official.time.astype(str).str[:10]));difference=len(keys.symmetric_difference(expected))
        reconciliations.append(dict(check=method,artifact=index,custom_cases=len(keys),official_cases=len(expected),symmetric_difference=difference))
        if difference:raise ValueError(f'Localizações IQR divergem: {method}/{index}')
        if local:
            worst=max(local,key=lambda r:abs(r['scaled_value']));counts=pd.Series([r['variable'] for r in local]).value_counts().to_dict()
            review(method,index,f'{len(local)} extremos; grupos={counts}; máximo |escalado|={abs(worst["scaled_value"]):.4f} em {worst["geo"]}/{worst["variable"]}/{worst["time"]}','confundir cauda sintética, escala e intermitência com erro','preservar: limites e localizações reconciliados, domínio válido; não há evidência/contexto comercial para corrigir','official_outlier_cases.csv; official_outlier_reconciliation.csv')
    for level in ['geo','national']:
        method=f'check_{level}_cost_per_media_unit';a=outcomes[method].analysis_artifacts[0];out=a.outlier_df.reset_index();table(out,f'official_cpmu_cases_{level}',False);f=long_frame(a.cost_per_media_unit_da)
        relative=[]
        for _,g in f.groupby(['geo','var']):
            x=g.value.dropna();relative.extend((x/x.mean()-1).abs().tolist())
        if len(out):review(method,0,f'{len(out)} casos CPMU; máximo desvio relativo na respectiva série={max(relative):.3e}; inconsistências spend/media={len(a.cost_media_unit_inconsistency_df)}','IQR amplifica dispersão microscópica','preservar custo e limiar: magnitude compatível com precisão de exportação, sem provar sua causa',f'official_cpmu_cases_{level}.csv')
    frame=table(pd.DataFrame(cases),'official_outlier_cases',False)
    table(frame.sort_values('scaled_value',key=lambda x:x.abs(),ascending=False).groupby(['check','variable'],sort=False).head(2),'official_outlier_selected_cases',False)
    table(pd.DataFrame(reconciliations),'official_outlier_reconciliation',False);table(pd.DataFrame(reviews),'official_review_resolution',False)
    thresholds=[]
    for field in dataclasses.fields(engine.spec):
        value=getattr(engine.spec,field.name)
        if dataclasses.is_dataclass(value):
            for item in dataclasses.fields(value):
                v=getattr(value,item.name)
                if isinstance(v,(float,int)):thresholds.append(dict(check_group=field.name,parameter=item.name,value=v,modified=False,scope='guardrail oficial, não certificado universal de qualidade'))
    table(pd.DataFrame(thresholds),'official_thresholds',False)
