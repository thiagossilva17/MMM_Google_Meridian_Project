"""Capítulos centrais: heterogeneidade GEO e execução territorial de mídia."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .config import *
from .data import channels, analytical_columns
from .statistics import variance_decomposition, safe_divide
from .reporting import table, result
from . import plots

def geo_analysis(panel):
    grouped=panel.groupby(GEO)
    geo=grouped[KPI].agg(['sum','mean','std','min','max']).rename(columns={'sum':'kpi_total'})
    geo[POP]=grouped[POP].first()
    geo['kpi_share']=geo.kpi_total/geo.kpi_total.sum()
    geo['population_share']=geo[POP]/geo[POP].sum()
    geo['kpi_per_1000_per_week']=geo['mean']/geo[POP]*1000
    geo=geo.sort_values('kpi_total',ascending=False)
    table(geo,'geo_kpi_summary');table(geo[[POP,'population_share']],'population_summary')
    decomposition=variance_decomposition(panel,analytical_columns(panel))
    table(decomposition,'within_between_variance');table(decomposition[['r2_geo','r2_time','r2_geo_time','residual_geo_time_share']],'geo_time_r2')
    per_capita=panel.copy()
    pc_cols=[KPI]+[c+'_impression' for c in channels(panel)]+[c+'_spend' for c in channels(panel)]+ORGANIC
    per_capita[pc_cols]=panel[pc_cols].div(panel[POP],axis=0)*1000
    pc_decomp=table(variance_decomposition(per_capita,pc_cols),'geo_time_r2_per_capita')
    table(per_capita[[GEO,TIME]+pc_cols],'per_capita_panel',False)
    pop_corr=pd.DataFrame([{'method':method,'correlation':geo[POP].corr(geo.kpi_total,method=method)} for method in ['pearson','spearman']])
    table(pop_corr,'population_kpi_correlation',False)
    concentration=pd.DataFrame({'rank':np.arange(1,len(geo)+1),'geo':geo.index,'cumulative_kpi_share':geo.kpi_share.cumsum().values})
    table(concentration,'kpi_concentration',False)
    figures=[plots.bars(geo.kpi_total,'geo','kpi_by_geo','KPI acumulado por geo — volume não é performance','Conversões sintéticas / período completo'),
             plots.bars(geo[POP].sort_values(ascending=False),'geo','population_by_geo','População simulada por geo','População'),
             plots.bars(geo.kpi_per_1000_per_week.sort_values(ascending=False),'geo','kpi_per_capita','KPI médio semanal por 1.000 habitantes','Conversões / 1.000 habitantes / semana'),
             plots.scatter(geo[POP],geo.kpi_total,'geo','population_kpi','População × KPI acumulado','População simulada','Conversões sintéticas acumuladas')]
    figures.append(plots.lines(concentration.set_index('rank')[['cumulative_kpi_share']],'geo','kpi_concentration','Concentração cumulativa do KPI (geos ordenados)','Fração acumulada'))
    pivot=panel.pivot(index=TIME,columns=GEO,values=KPI).reindex(columns=geo.index)
    figures.append(plots.heatmap(pivot.corr(),'geo','geo_correlation','Sincronização do KPI entre geos (Pearson)','RdBu_r',-1,1))
    table(pivot.corr(),'geo_kpi_correlation')
    # Seleção determinística: extremos de volume, centro do ranking e extremos de volatilidade.
    cv=grouped[KPI].std(ddof=0)/grouped[KPI].mean().replace(0,np.nan)
    selected=list(dict.fromkeys(list(geo.index[:2])+list(geo.index[-2:])+list(geo.index[len(geo)//2-1:len(geo)//2+1])+[cv.idxmin(),cv.idxmax()]))
    table(pd.DataFrame({'geo':selected,'criterion':'união: top2/bottom2/centro de volume e min/max CV'}),'geo_plot_selection',False)
    fig,axes=plt.subplots(4,2,figsize=(13,10),sharex=True)
    for ax,g in zip(axes.flat,selected):
        ax.plot(pivot.index,pivot[g]);ax.set(title=g,ylabel='Conversões')
    for ax in list(axes.flat)[len(selected):]:ax.set_visible(False)
    fig.suptitle('KPI por geo; escalas Y próprias revelam a dinâmica')
    figures.append(plots.save(fig,'geo','kpi_small_multiples'))
    fig,ax=plt.subplots(figsize=(12,5))
    decomposition[['between_share','within_share']].plot.bar(stacked=True,ax=ax)
    ax.set(title='Decomposição between/within — ddof=0',ylabel='Fração da variância total')
    figures.append(plots.save(fig,'geo','variance_decomposition'))
    fig,ax=plt.subplots(figsize=(12,6))
    plotted=decomposition.loc[[c for c in decomposition.index if not c.endswith('_spend')]]
    for i,(var,row) in enumerate(plotted.iterrows()):
        label=var.removesuffix('_impression').replace('_control','')
        ax.scatter(row.r2_geo,row.r2_time,s=65,marker=['o','s','^','D','v'][i%5],
                   label=f'{label} ({row.r2_geo:.3f}; {row.r2_time:.3f})')
    ax.legend(title='Variável (R² geo; R² time)',loc='upper left',bbox_to_anchor=(1.01,1),fontsize=8)
    ax.set(xlabel='R² explicado por efeitos de geo',ylabel='R² explicado por efeitos de semana',
           title='GEO × TIME: origem da variação bruta',xlim=(-.02,.8),ylim=(-.02,.42))
    ax.text(0,-.2,'Gasto: coordenadas quase idênticas às impressões; valores completos em geo_time_r2.csv.',transform=ax.transAxes,fontsize=8)
    figures.append(plots.save(fig,'geo','geo_time_r2'))
    for col in [KPI]+CONTROLS:
        matrix=panel.pivot(index=GEO,columns=TIME,values=col).reindex(geo.index)
        figures.append(plots.heatmap(matrix,'geo',col+'_geo_time',f'{col}: GEO × semana'))
    matrix=per_capita.pivot(index=GEO,columns=TIME,values=KPI).reindex(geo.index)
    figures.append(plots.heatmap(matrix,'geo','kpi_pc_geo_time','Conversões semanais / 1.000 habitantes'))
    text=f'''O maior geo responde por {geo.kpi_share.max():.1%} do KPI acumulado; os cinco maiores por {geo.kpi_share.head(5).sum():.1%}. A correlação populacional com KPI total é {pop_corr.loc[pop_corr.method=='spearman','correlation'].iloc[0]:.3f} (Spearman). A escala populacional precisa ser considerada antes de interpretar rankings.

O KPI tem {decomposition.loc[KPI,'between_share']:.1%} da variância between-geo e {decomposition.loc[KPI,'within_share']:.1%} within-geo. A identidade usa momentos populacionais (ddof=0), com peso igual por observação. R²_geo equivale à parcela between; R²_time quantifica semanas comuns. No painel balanceado, a parcela residual two-way do KPI é {decomposition.loc[KPI,'residual_geo_time_share']:.1%}; por habitante é {pc_decomp.loc[KPI,'residual_geo_time_share']:.1%}.

Within não significa automaticamente sinal geográfico novo: inclui choques temporais nacionais. Por isso apresentamos também o resíduo após remover simultaneamente geo e tempo. Essa decomposição é descritiva e depende da escala. Os small multiples usam geos escolhidos por critérios registrados; os cálculos e heatmaps incluem todos os geos. Geo0…Geo39 são rótulos sintéticos, sem fronteiras para um mapa geográfico real.'''
    return result('03_eda_geo',text,{'geo_summary':geo,'decomposition':decomposition,'per_capita_decomposition':pc_decomp},figures,'Mix, alocação territorial, concentração e variação de cada canal dentro dos geos.')

def media_geo(panel):
    paid=channels(panel)
    population=panel.groupby(GEO)[POP].first()
    order=panel.groupby(GEO)[KPI].sum().sort_values(ascending=False).index
    spend=panel.groupby(GEO)[[c+'_spend' for c in paid]].sum().reindex(order)
    spend.columns=paid;spend.columns.name='channel'
    mix=spend.div(spend.sum(axis=1).replace(0,np.nan),axis=0)
    allocation=spend.div(spend.sum(axis=0).replace(0,np.nan),axis=1)
    table(spend,'geo_media_summary');table(mix,'media_mix');table(allocation,'geo_allocation')
    figures=[plots.heatmap(spend,'media_geo','spend_geo_channel','Gasto total por GEO × canal (moeda não especificada)'),
             plots.heatmap(mix,'media_geo','media_mix','Mix: parcela do gasto de cada geo',vmin=0,vmax=1),
             plots.heatmap(allocation,'media_geo','geo_allocation','Alocação: parcela de cada canal destinada ao geo',vmin=0,vmax=allocation.max().max()),
             plots.heatmap(spend.div(population,axis=0)*1000,'media_geo','spend_per_capita','Gasto acumulado / 1.000 habitantes')]
    fig,ax=plt.subplots(figsize=(13,5));mix.plot.bar(stacked=True,ax=ax,width=.85)
    ax.set(title='Composição do orçamento por geo',ylabel='Fração do gasto do geo')
    figures.append(plots.save(fig,'media_geo','mix_stacked'))
    cv_rows=[];correlations=[];concentration=[];cost_rows=[]
    for channel in paid:
        media_col=channel+'_impression';spend_col=channel+'_spend'
        med=panel.groupby(GEO)[media_col].agg(['sum','mean','std'])
        med['std']=panel.groupby(GEO)[media_col].std(ddof=0)
        cv=safe_divide(med['std'],med['mean'])
        for geo,value in cv.items():cv_rows.append(dict(channel=channel,geo=geo,cv=value))
        for method in ['pearson','spearman']:
            correlations.append(dict(channel=channel,method=method,population_media_correlation=population.corr(med['sum'],method=method)))
        shares=allocation[channel].sort_values(ascending=False)
        concentration.append(dict(channel=channel,hhi=(shares**2).sum(),effective_geos=1/(shares**2).sum(),top1=shares.iloc[0],top5=shares.head(5).sum()))
        figures.append(plots.scatter(population,med['sum'].reindex(population.index),'media_geo',channel+'_population',channel+': população × mídia','População','Impressões acumuladas'))
        for col,label in [(media_col,'impressões'),(spend_col,'gasto')]:
            matrix=panel.pivot(index=GEO,columns=TIME,values=col).reindex(order)
            figures.append(plots.heatmap(matrix,'media_geo',col+'_geo_time',f'{channel}: {label} por GEO × semana'))
            figures.append(plots.heatmap(matrix.div(population,axis=0)*1000,'media_geo',col+'_pc_geo_time',f'{channel}: {label} / 1.000 habitantes por semana'))
        cost=panel.assign(cpmu=safe_divide(panel[spend_col],panel[media_col]))
        for geo,group in cost.groupby(GEO):
            cost_rows.append(dict(channel=channel,geo=geo,mean=group.cpmu.mean(),min=group.cpmu.min(),max=group.cpmu.max(),std=group.cpmu.std(ddof=0)))
    cvs=table(pd.DataFrame(cv_rows),'within_geo_cv',False)
    table(pd.DataFrame(correlations),'population_media_correlation',False)
    concentration=table(pd.DataFrame(concentration),'channel_geo_concentration',False)
    table(pd.DataFrame(cost_rows),'geo_cpmu',False)
    figures.append(plots.heatmap(cvs.pivot(index='geo',columns='channel',values='cv').reindex(order),'media_geo','within_geo_cv','CV de mídia ao longo do tempo dentro de cada geo'))
    fig,ax=plt.subplots(figsize=(9,4));cvs.boxplot(column='cv',by='channel',ax=ax);fig.suptitle('');ax.set(title='Distribuição dos CVs within por canal',ylabel='Desvio padrão / média')
    figures.append(plots.save(fig,'media_geo','within_cv_distribution'))
    spread=(mix.max()-mix.min()).sort_values(ascending=False)
    text=f'''O mix divide cada linha GEO × canal pelo orçamento total do geo; a alocação divide cada coluna pelo orçamento do canal. Essas perguntas são diferentes. A maior amplitude de share do mix é {spread.iloc[0]:.1%}, em {spread.index[0]}.

HHI é a soma dos quadrados das participações geográficas de um canal: varia de 1/G (uniforme) a 1 (um único geo). Observamos {concentration.hhi.min():.3f} a {concentration.hhi.max():.3f}, sem aplicar limiares de concorrência econômica. O inverso traduz concentração em número equivalente de geos uniformes, não em tamanho amostral efetivo.

Os CVs within variam de {cvs.cv.min():.3f} a {cvs.cv.max():.3f}. Médias zero produzem CV indefinido. Heatmaps usam a mesma ordenação de geos por KPI total e escalas de cor próprias por variável; não comparar cores entre painéis sem ler as escalas. As versões por habitante ajudam a investigar diferenças que persistem além do tamanho dos mercados.'''
    return result('04_eda_media_geo',text,{'media_mix':mix,'geo_allocation':allocation,'concentration':concentration,'within_cv':cvs},figures,'Correlações entre canais e controles, VIF e conflitos com geo/tempo.')
