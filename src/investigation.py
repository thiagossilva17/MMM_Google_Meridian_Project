"""Investigações localizadas motivadas pela auditoria, sem remoção de dados."""
from pathlib import Path
import numpy as np
import pandas as pd
from .config import ROOT,GEO,TIME,KPI,POP,CONTROLS,NON_MEDIA,ORGANIC
from .data import channels,analytical_columns,national

def read(name,**kw):return pd.read_csv(ROOT/'outputs/tables'/f'{name}.csv',**kw)
def export(frame,name,index=False):
    from .reporting import table
    return table(frame,name,index)
def iqr_flags(x):
    q1,q3=x.quantile([.25,.75]);d=q3-q1
    return (x<q1-1.5*d)|(x>q3+1.5*d)
def outlier_investigation(p):
    original=read('outliers');groups=[];cases=[];windows=[]
    for col in analytical_columns(p):
        x=p[col];raw=iqr_flags(x);additive=col not in CONTROLS+NON_MEDIA
        scaled=x/p[POP]*1000 if additive else x;normalized=iqr_flags(scaled)
        within=p.groupby(GEO)[col].transform(iqr_flags).astype(bool)
        flagged=original[original.variable==col]
        reason=(f'Promo contínuo: {x.nunique()} valores distintos, {x.eq(0).mean():.1%} zeros; não binário.' if col=='Promo' else
                'Índice sintético centrado; valores negativos admissíveis, sem unidade comercial validada.' if col in CONTROLS else
                f'IQR bruto: {raw.sum()}; per capita: {normalized.sum()}; interseção: {(raw&normalized).sum()}. Escala e cauda devem ser distinguidas.')
        groups.append(dict(variable=col,custom_iqr_or_mad=len(flagged),raw_iqr=raw.sum(),per_capita_iqr=normalized.sum() if additive else np.nan,within_geo_iqr=within.sum(),overlap_raw_normalized=(raw&normalized).sum(),investigation=reason,decision='manter no estudo simulado; domínio válido, sem evidência de corrupção'))
        eligible=pd.MultiIndex.from_frame(p[[GEO,TIME]]).isin(pd.MultiIndex.from_frame(flagged.assign(time=pd.to_datetime(flagged.time))[[GEO,TIME]]))
        selected=(x-x.median()).abs().where(eligible).dropna().nlargest(3).index
        for i in selected:
            r=p.loc[i];g=p[p.geo==r.geo]
            cases.append(dict(variable=col,geo=r.geo,time=r.time,value=x[i],population=r[POP],per_1000=scaled[i] if additive else np.nan,raw_iqr=bool(raw[i]),normalized_iqr=bool(normalized[i]),within_geo_iqr=bool(within[i]),geo_percentile=g[col].rank(pct=True).loc[i],context=reason,decision='preservar: localizado e comparado por escala/geo; sem evidência de erro',limitation='plausibilidade comercial não demonstrada; influência pertence à modelagem'))
            for _,near in g[(g.time-r.time).abs()<=pd.Timedelta(weeks=2)].iterrows():windows.append(dict(variable=col,case_geo=r.geo,case_time=r.time,time=near.time,value=near[col],is_case=near.time==r.time))
    export(pd.DataFrame(windows),'outlier_case_windows')
    coincident=original.groupby([GEO,TIME]).variable.agg(count='size',variables=lambda x:', '.join(sorted(x))).reset_index().sort_values('count',ascending=False)
    export(coincident,'outlier_coincidence')
    return export(pd.DataFrame(groups),'outlier_group_review'),export(pd.DataFrame(cases),'outlier_case_review')
def activity_investigation(p):
    runs=read('activity_runs');rows=[];zeros=[];summaries=[]
    for c in channels(p):
        for geo,g in p.groupby(GEO):
            x=g.sort_values(TIME)[c+'_impression'];positive=x[x>0];prob=x.gt(0).mean();r=runs[(runs.channel==c)&(runs.geo==geo)]
            intensity=prob*positive.var(ddof=0) if len(positive) else 0.;switch=prob*(1-prob)*positive.mean()**2 if len(positive) else 0.
            rows.append(dict(channel=c,geo=geo,active_share=prob,positive_n=len(positive),positive_cv=positive.std(ddof=0)/positive.mean(),unconditional_cv=x.std(ddof=0)/x.mean(),max_zero_streak=r.loc[~r.active,'weeks'].max(),max_active_streak=r.loc[r.active,'weeks'].max(),minimum_active_in_13_weeks=x.gt(0).rolling(13).sum().min(),within_variance=x.var(ddof=0),activity_variance=switch,intensity_variance=intensity))
        total=p.groupby(TIME)[c+'_impression'].sum()
        zeros.extend(dict(channel=c,time=t) for t in total[total.eq(0)].index)
    support=export(pd.DataFrame(rows).fillna({'max_zero_streak':0,'max_active_streak':0}),'activity_support_by_geo')
    for c,g in support.groupby('channel'):
        if not np.allclose(g.within_variance,g.activity_variance+g.intensity_variance):raise ValueError('Identidade atividade/intensidade falhou')
        summaries.append(dict(channel=c,active_share_min=g.active_share.min(),active_share_max=g.active_share.max(),median_positive_cv=g.positive_cv.median(),median_unconditional_cv=g.unconditional_cv.median(),max_zero_streak=g.max_zero_streak.max(),max_active_streak=g.max_active_streak.max(),minimum_active_in_13_weeks=g.minimum_active_in_13_weeks.min(),within_variance_activity_share=g.activity_variance.sum()/g.within_variance.sum(),within_variance_intensity_share=g.intensity_variance.sum()/g.within_variance.sum()))
    return support,export(pd.DataFrame(summaries),'activity_intensity_summary'),export(pd.DataFrame(zeros,columns=['channel','time']),'national_zero_media_weeks')
def temporal_investigation(p):
    stl=read('kpi_stl_52');acf=read('kpi_acf').set_index('lag').acf;change=read('kpi_level_changes').iloc[0];v=stl.residuo.var(ddof=0)
    summary=export(pd.DataFrame([dict(first_trend=stl.tendencia.iloc[0],last_trend=stl.tendencia.iloc[-1],trend_change_percent=100*(stl.tendencia.iloc[-1]/stl.tendencia.iloc[0]-1),seasonal_strength=max(0,1-v/(stl.residuo+stl.sazonal).var(ddof=0)),trend_strength=max(0,1-v/(stl.residuo+stl.tendencia).var(ddof=0)),acf_lag1=acf.loc[1],acf_lag13=acf.loc[13],acf_lag52=acf.loc[52],largest_weekly_change_date=change.time,largest_weekly_change=change.difference)]),'temporal_interpretation')
    rows=[]
    for col in CONTROLS+NON_MEDIA:
        x=p[col];d=national(p)[col].diff();date=d.abs().idxmax()
        rows.append(dict(variable=col,min=x.min(),max=x.max(),std=x.std(ddof=0),distinct=x.nunique(),zero_share=x.eq(0).mean(),std_over_range=x.std(ddof=0)/(x.max()-x.min()),largest_national_change_date=date,largest_national_change=d.loc[date],cv_interpretation='não usar em índice centrado/zero-inflado'))
    return summary,export(pd.DataFrame(rows),'control_detailed_profile')
def media_investigation(p):
    from . import plots
    mix=read('media_mix',index_col=0);national_share=read('channel_summary').set_index('channel').spend_share
    raw=read('geo_time_r2').set_index('variable');pc=read('geo_time_r2_per_capita').set_index('variable');pop=p.groupby(GEO)[POP].first();rows=[]
    for c in channels(p):
        col=c+'_impression';m=p.groupby(GEO)[col].sum()
        rows.append(dict(channel=c,mix_min_percent=100*mix[c].min(),mix_max_percent=100*mix[c].max(),mix_range_pp=100*(mix[c].max()-mix[c].min()),mix_std_pp=100*mix[c].std(ddof=0),population_corr_raw=pop.corr(m,method='spearman'),population_corr_per_capita=pop.corr(m/pop,method='spearman'),r2_geo_raw=raw.loc[col,'r2_geo'],r2_geo_per_capita=pc.loc[col,'r2_geo'],residual_raw=raw.loc[col,'residual_geo_time_share'],residual_per_capita=pc.loc[col,'residual_geo_time_share']))
    delta=100*(mix-national_share);limit=delta.abs().max().max()
    return export(pd.DataFrame(rows),'channel_geo_interpretation'),[plots.heatmap(delta,'media_geo','mix_deviations_pp','Mix do GEO menos mix nacional — pontos percentuais','RdBu_r',-limit,limit)]
def relationship_investigation(p):
    corr=read('correlation_summary');predictors=[c+'_impression' for c in channels(p)]+ORGANIC+CONTROLS+NON_MEDIA
    selected=corr[corr.left.isin(predictors)&corr.right.isin(predictors)]
    wide=selected.pivot(index=['left','right','method'],columns='level',values='correlation').reset_index().sort_values('within',key=lambda x:x.abs(),ascending=False)
    wide['national_minus_within']=wide.national-wide.within;export(wide,'substantive_pair_comparison')
    export(corr[(corr.left==KPI)&corr.right.isin(predictors)],'predictor_kpi_comparison')
    v=read('vif_summary');r=read('geo_time_r2').set_index('variable');rows=[]
    for col in CONTROLS+NON_MEDIA:
        peers=wide[(wide.method=='pearson')&((wide.left==col)|(wide.right==col))];best=peers.loc[peers.two_way.abs().idxmax()]
        rows.append(dict(variable=col,r2_geo=r.loc[col,'r2_geo'],r2_time=r.loc[col,'r2_time'],vif_within=v[(v.variable==col)&(v.level=='within')].vif.iloc[0],strongest_two_way_peer=best.right if best.left==col else best.left,strongest_two_way_correlation=best.two_way,implication='Justificar papel pré-tratamento/confundidor no DAG; associação não autoriza inclusão causal.'))
    return wide,export(pd.DataFrame(rows),'control_relationship_review')
def integrated_review():
    base=read('channel_summary').set_index('channel');support=read('activity_intensity_summary').set_index('channel');geo=read('channel_geo_interpretation').set_index('channel');vif=read('vif_summary');corr=read('substantive_pair_comparison');rows=[];gates=[]
    for c,r in base.iterrows():
        col=c+'_impression';peers=corr[(corr.method=='pearson')&((corr.left==col)|(corr.right==col))];best=peers.loc[peers.two_way.abs().idxmax()]
        rows.append(dict(channel=c,zero_share=r.zero_share,spend_share=r.spend_share,**support.loc[c].to_dict(),**geo.loc[c].to_dict(),vif_within=vif[(vif.variable==col)&(vif.level=='within')].vif.iloc[0],strongest_two_way_peer=best.right if best.left==col else best.left,strongest_two_way_correlation=best.two_way,risk='suporte intermitente; janelas sem exposição' if c=='Channel2' else 'escala populacional e movimentos conjuntos não equivalem a efeito',action='documentar suporte por janela de treino/holdout e incerteza do canal' if c=='Channel2' else 'verificar hipótese causal e colinearidade após transformações',eda_decision='manter na especificação candidata, sem exclusão mecânica'))
    integrated=export(pd.DataFrame(rows),'channel_integrated_review')
    for r in integrated.itertuples():gates.append(dict(subject=r.channel,finding=f'zeros {r.zero_share:.1%}; resíduo per capita {r.residual_per_capita:.1%}; VIF within {r.vif_within:.2f}',risk=r.risk,action=r.action,closure_criterion='ficha completa e hipóteses justificadas antes do ajuste',status='EDA documentada; especificação futura',owner='autor do TCC',evidence='channel_integrated_review.csv'))
    for r in read('control_relationship_review').itertuples():gates.append(dict(subject=r.variable,finding=f'R² time {r.r2_time:.3f}; VIF within {r.vif_within:.2f}',risk='controle pós-tratamento/proxy de demanda',action=r.implication,closure_criterion='DAG e temporalidade justificados',status='pendente da especificação',owner='autor do TCC',evidence='control_relationship_review.csv'))
    for r in read('official_review_resolution').itertuples():gates.append(dict(subject=r.review_id,finding=r.finding,risk=r.risk,action=r.decision,closure_criterion=r.closure_criterion,status=r.status,owner='autor do TCC',evidence=r.evidence))
    gates.append(dict(subject='Colab real',finding='não executado no serviço',risk='diferenças de runtime/frontend',action='Run all em sessão nova e registrar versões/log',closure_criterion='master com todos os capítulos e gates concluídos no serviço',status='pendente externa',owner='autor do TCC',evidence='docs/COLAB_VALIDATION.md'))
    return integrated,export(pd.DataFrame(gates),'readiness_actions')
def enrich(chapter):
    p=pd.read_csv(ROOT/'data/processed/geo_time_panel.csv',parse_dates=[TIME]);stage=chapter[:2];tables={};figures=[]
    if stage=='00':
        text='**Decisão de estrutura:** chave, grade, domínios e população validados. CPMU indefinido em zero atividade permanece NaN. Coordenadas e pares mídia/gasto estão explícitos no dicionário.';limitation='Integridade estrutural não certifica plausibilidade dos extremos; investigar nos capítulos 01 e 06.'
    elif stage=='01':
        groups,cases=outlier_investigation(p);support,activity,zeros=activity_investigation(p);a=activity.set_index('channel');c2=a.loc['Channel2'];c3=a.loc['Channel3']
        tables={'Revisão por grupo':groups,'Casos selecionados':cases,'Atividade versus intensidade':activity,'Semanas nacionais sem mídia':zeros,'Channel2: menor suporte por GEO':support[support.channel=='Channel2'].nsmallest(5,'active_share')}
        text=f"**Channel2 versus Channel3:** atividade por geo entre {c2.active_share_min:.1%} e {c2.active_share_max:.1%}; maior sequência de zeros {c2.max_zero_streak:.0f} semanas. Channel3 tem sequência ativa máxima de {c3.max_active_streak:.0f} semanas. Zeros nacionais de Channel2: {', '.join(zeros[zeros.channel=='Channel2'].time.astype(str).str[:10])}.\n\n**Atividade e intensidade:** Var(X)=p Var(X|X>0)+p(1−p)E(X|X>0)². A alternância zero/positivo corresponde a {c2.within_variance_activity_share:.1%} da variância within em Channel2, contra {c3.within_variance_activity_share:.1%} em Channel3. CV mediano de Channel2: {c2.median_unconditional_cv:.2f} geral e {c2.median_positive_cv:.2f} entre valores positivos. Essa identidade não decompõe o resíduo two-way nem estima eficácia.\n\n**Extremos:** {groups.custom_iqr_or_mad.sum()} pares triados; até três casos por variável com comparação bruto/per capita/dentro do geo e janelas de ±2 semanas. Promo é contínuo com massa em zero, não binário. Os grupos e as justificativas estão nas tabelas; dados simulados são preservados, sem validação comercial presumida."
        limitation='Sparsity limita suporte em janelas específicas; não inventar calendário de campanhas.'
    elif stage=='02':
        t,controls=temporal_investigation(p);r=t.iloc[0];tables={'Leitura temporal':t,'Controles individualizados':controls}
        text=f'**Trajetória:** tendência STL de {r.first_trend:,.0f} a {r.last_trend:,.0f} ({r.trend_change_percent:+.2f}%). Maior mudança semanal em {r.largest_weekly_change_date}: {r.largest_weekly_change:+,.0f}. ACF nos lags 1/13/52: {r.acf_lag1:.3f}/{r.acf_lag13:.3f}/{r.acf_lag52:.3f}. Forças descritivas sazonal/tendência: {r.seasonal_strength:.3f}/{r.trend_strength:.3f}, calculadas por 1−Var(resíduo)/Var(componente+resíduo), truncadas em zero; não são parcelas aditivas ou testes.'
        for _,r in controls.iterrows():text+=f"\n\n{r.variable}: amplitude [{r['min']:.3f},{r['max']:.3f}], desvio {r['std']:.3f}, {r.distinct} valores distintos; maior mudança nacional ponderada em {str(r.largest_national_change_date)[:10]} ({r.largest_national_change:+.3f}). Não é quase constante na escala observada; CV não é interpretável."
        limitation='Somente três ciclos; STL/ACF não confirmam sazonalidade de negócio nem quebras causais.'
    elif stage=='03':
        corr=read('geo_kpi_correlation',index_col=0);pairs=pd.DataFrame([dict(geo_a=g,geo_b=h,correlation=corr.loc[g,h]) for i,g in enumerate(corr.index) for h in corr.columns[i+1:]]).sort_values('correlation');export(pairs,'geo_synchronization_pairs')
        summary=export(pd.DataFrame([dict(n_pairs=len(pairs),minimum=pairs.correlation.min(),median=pairs.correlation.median(),maximum=pairs.correlation.max(),q25=pairs.correlation.quantile(.25),q75=pairs.correlation.quantile(.75))]),'geo_synchronization_summary');tables={'Sincronização':summary,'Pares extremos':pd.concat([pairs.head(3),pairs.tail(3)])}
        text=f'**Sincronização:** {len(pairs)} pares, mediana {pairs.correlation.median():.4f}, mínimo {pairs.correlation.min():.4f} ({pairs.iloc[0].geo_a} × {pairs.iloc[0].geo_b}), máximo {pairs.correlation.max():.4f} ({pairs.iloc[-1].geo_a} × {pairs.iloc[-1].geo_b}). Baixa sincronização linear não demonstra independência. Small multiples cobrem extremos de volume/CV e usam escalas Y próprias.';limitation='Geos fictícios não permitem inventar contextos territoriais.'
    elif stage=='04':
        summary,figures=media_investigation(p);tables={'Mix, população e resíduo por canal':summary};text='**Mix relativamente semelhante:** dispersões são expressas em pontos percentuais; o gráfico de desvios do nacional expõe pequenas diferenças sem sugerir forte heterogeneidade acumulada.'
        for r in summary.itertuples():text+=f'\n\n{r.channel}: mix {r.mix_min_percent:.2f}%–{r.mix_max_percent:.2f}%, amplitude {r.mix_range_pp:.2f} p.p., desvio {r.mix_std_pp:.2f} p.p.; Spearman população×volume {r.population_corr_raw:.3f}, população×intensidade {r.population_corr_per_capita:.3f}; R² GEO bruto/per capita {r.r2_geo_raw:.3f}/{r.r2_geo_per_capita:.3f}; resíduo per capita {r.residual_per_capita:.3f}.'
        limitation='Resíduo pode conter alternância de atividade e ruído, não apenas sinal causal.'
    elif stage=='05':
        pairs,controls=relationship_investigation(p);tables={'Pares substantivos':pairs[pairs.method=='pearson'].head(10),'Controles e cuidados':controls};r=pairs[(pairs.left=='Channel2_impression')&(pairs.right=='Channel3_impression')&(pairs.method=='pearson')].iloc[0]
        text=f'**Channel2 × Channel3:** nacional {r.national:.4f}, within {r.within:.4f}, two-way {r.two_way:.4f}. Parte do movimento conjunto acompanha composição/tempo comum, mas há associação residual. O ranking exclui gasto–impressões do mesmo canal.'
        for r in controls.itertuples():text+=f'\n\n{r.variable}: R² tempo {r.r2_time:.3f}; VIF within {r.vif_within:.2f}; maior associação two-way com {r.strongest_two_way_peer} ({r.strongest_two_way_correlation:+.3f}). {r.implication}'
        limitation='VIF moderado não resolve confundimento nem colinearidade após adstock/saturação.'
    elif stage=='06':
        reviews=read('official_review_resolution');tables={n:read(n) for n in ['official_review_resolution','official_outlier_selected_cases','official_outlier_reconciliation','official_correlation_reconciliation','official_vif_reconciliation','official_thresholds']}
        text=f'**Revisão localizada:** {len(reviews)} REVIEW têm localizações, magnitude, decisão e limite residual documentados. A severidade oficial permanece REVIEW. Correlação/VIF são reconciliados na mesma escala; IQR compara todas as chaves geo–variável–semana. CPMU tem casos nos arquivos official_cpmu_cases_geo/national. Controles/Promo nacionais oficiais usam soma por default; a EDA própria pondera por população, explicando diferenças entre escalas.';limitation='Guardrails oficiais extremos não são certificados de qualidade. Preservação no exemplo não certifica plausibilidade econômica.'
    else:
        integrated,gates=integrated_review();tables={'Fichas integradas':integrated,'Ações verificáveis':gates};text='**Prontidão revisada:** casos e alertas possuem decisão descritiva. Avançar ao desenho da especificação, mantendo os dados. DAG, controles, priors e validação temporal pertencem à próxima fase. Colab real continua pendente externa.'
        for r in integrated.itertuples():text+=f'\n\n**{r.channel}:** zeros {r.zero_share:.1%}; CV positivo {r.median_positive_cv:.2f}; sequência zero {r.max_zero_streak:.0f}; amplitude mix {r.mix_range_pp:.2f} p.p.; R² GEO bruto/per capita {r.r2_geo_raw:.3f}/{r.r2_geo_per_capita:.3f}; resíduo per capita {r.residual_per_capita:.3f}; VIF within {r.vif_within:.2f}; maior associação two-way {r.strongest_two_way_peer} ({r.strongest_two_way_correlation:.3f}). Risco: {r.risk}. Ação: {r.action}.'
        from .provenance import record
        path=ROOT/'docs/channel_review.md';path.write_text('# Síntese por canal e critérios de avanço\n\n'+text+'\n\n'+gates.to_markdown(index=False));record(path)
        limitation='Colab real não comprovado; EDA não demonstra identificação causal ou superioridade preditiva.'
    return dict(text=text,limitation=limitation,tables=tables,figures=figures)
def figure_comment(path):
    name=Path(path).stem
    if name.startswith('Channel'):
        c=name.split('_')[0];r=read('channel_summary').set_index('channel').loc[c]
        return f'**{c}:** {r.zero_share:.1%} das células sem mídia; {r.spend_share:.1%} do gasto. Confronte com a ficha de suporte. CPMU microscópico não representa variação econômica; cores de painéis distintos exigem leitura da escala.'
    notes={'mix_deviations_pp':'Diferenças em pontos percentuais; mix acumulado semelhante pode coexistir com execução semanal diferente.','geo_correlation':'A distribuição dos 780 pares contextualiza a matriz; baixa correlação não prova independência.','kpi_small_multiples':'Comparar dinâmica com atenção às escalas Y próprias; datas anuais permitem leitura sem sobreposição.','kpi_stl_52':'Apenas três ciclos; confrontar ACF, forças descritivas e datas na síntese.','readiness_dashboard':'Partes de variância são descritivas; contagem INFO/REVIEW não substitui decisões por alerta.'}
    return '**Como ler — '+name.replace('_',' ')+':** '+notes.get(name,'Compare com os resultados numéricos e a interpretação do capítulo. Unidade e denominador delimitam a leitura; associação não demonstra eficácia.')
