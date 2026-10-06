"""Auditoria antes de calcular estatísticas: nunca imputar ou corrigir silenciosamente."""
import numpy as np
import pandas as pd
from .config import *
from .data import roles, channels

def audit(panel: pd.DataFrame) -> pd.DataFrame:
    roles(panel)
    dates=pd.DatetimeIndex(sorted(panel[TIME].unique()))
    complete=pd.MultiIndex.from_product([sorted(panel[GEO].unique()), dates],names=[GEO,TIME])
    present=pd.MultiIndex.from_frame(panel[[GEO,TIME]])
    nonnegative=[KPI,POP,REVENUE_PER_KPI]+[c for c,r in roles(panel).items() if r in ['media','spend','organic_media']]
    gaps=dates.to_series().diff().dropna().dt.days
    checks={
        'rows':len(panel),'geos':panel[GEO].nunique(),'periods':panel[TIME].nunique(),
        'expected_rows':len(complete),'unique_geo_time':len(present.unique()),
        'panel_completeness':len(present.unique())/len(complete),
        'duplicate_keys':int(panel.duplicated([GEO,TIME]).sum()),
        'missing_geo_time':len(complete.difference(present)),
        'missing_cells':int(panel.isna().sum().sum()),
        'nonfinite_numeric':int((~np.isfinite(panel.select_dtypes('number'))).sum().sum()),
        'negative_domain_values':int((panel[nonnegative]<0).sum().sum()),
        'nonpositive_population':int((panel[POP]<=0).sum()),
        'population_varying_geos':int((panel.groupby(GEO)[POP].nunique()>1).sum()),
        'regular_weekly_grid':bool(len(gaps)>0 and gaps.eq(7).all()),
        'first_date':str(dates.min().date()),'last_date':str(dates.max().date()),
        'paid_channels':len(channels(panel)),'controls':len(CONTROLS),
        'reach_frequency_present':False,
    }
    for channel in channels(panel):
        media,spend=panel[channel+'_impression'],panel[channel+'_spend']
        checks[channel+'_media_positive_spend_zero']=int(((media>0)&(spend==0)).sum())
        checks[channel+'_media_zero_spend_positive']=int(((media==0)&(spend>0)).sum())
    return pd.DataFrame({'metric':checks.keys(),'value':checks.values()})

def require_valid_panel(panel: pd.DataFrame) -> None:
    checks=audit(panel).set_index('metric').value
    fatal=['duplicate_keys','missing_geo_time','missing_cells','nonfinite_numeric',
           'negative_domain_values','nonpositive_population','population_varying_geos']
    failures=[k for k in fatal if checks[k]!=0]
    if not checks['regular_weekly_grid']: failures.append('regular_weekly_grid')
    if failures: raise ValueError(f'Contrato falhou; consultar auditoria, sem imputação: {failures}')

def dictionary(panel: pd.DataFrame) -> pd.DataFrame:
    rows=[]
    for col,role in roles(panel).items():
        x=panel[col]; num=pd.api.types.is_numeric_dtype(x)
        unit={'kpi':'conversões sintéticas (contínuas)', 'population':'população simulada',
              'media':'impressões', 'organic_media':'impressões orgânicas',
              'spend':'unidade monetária não especificada', 'control':'escala sintética; unidade não especificada',
              'revenue_per_kpi':'moeda não especificada/conversão','non_media_treatment':'tratamento contínuo com massa em zero'}.get(role,role)
        rows.append(dict(variable=col,role=role,dtype=str(x.dtype),dimension={'geo':'coordenada geo','time':'coordenada time','population':'geo'}.get(role,'geo × time'),paired_variable=col.replace('_impression','_spend') if role=='media' else col.replace('_spend','_impression') if role=='spend' else '',
                         unit=unit,missing=x.isna().sum(),zeros=x.eq(0).sum() if num else np.nan,
                         min=x.min(),max=x.max(),mean=x.mean() if num else np.nan,std=x.std(ddof=0) if num else np.nan))
    return pd.DataFrame(rows)
