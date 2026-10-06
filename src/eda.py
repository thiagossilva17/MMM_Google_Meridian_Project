from .provenance import tracked, record
"""Capítulos 00–02 e 05: integridade, escala, tempo e relações."""
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .config import *
from .data import channels, analytical_columns, national
from .validation import audit, dictionary, require_valid_panel
from .statistics import describe, outliers, vif_table, safe_divide
from .reporting import table, result
from . import plots

@tracked('00')
def data_audit(panel):
    audit_table=table(audit(panel),'data_audit',False)
    dictionary_table=table(dictionary(panel),'data_dictionary',False)
    (ROOT/'docs/data_dictionary.md').write_text('# Dicionário dos dados\n\nDados simulados. Reach/frequency não estão presentes. Channel0–4 não identificam plataformas reais.\n\n'+dictionary_table.to_markdown(index=False),encoding='utf-8')
    missing=table(panel.isna().sum().rename('missing'),'missing_summary')
    table(panel.isna().groupby(panel[GEO]).sum(),'missing_by_geo')
    table(panel.isna().groupby(panel[TIME]).sum(),'missing_by_time')
    table(panel[[c+'_impression' for c in channels(panel)]].isna().sum().rename('missing'),'missing_by_channel')
    duplicates=table(panel[panel.duplicated([GEO,TIME],keep=False)],'duplicate_summary',False)
    presence=panel.assign(present=1).pivot_table(index=GEO,columns=TIME,values='present',aggfunc='sum')
    presence=presence.reindex(columns=pd.date_range(panel[TIME].min(),panel[TIME].max(),freq='7D')).fillna(0)
    figures=[plots.heatmap(presence,'data_audit','panel_completeness','Presença de observações GEO × semana',vmin=0,vmax=1)]
    figures.append(plots.bars(missing['missing'],'data_audit','missing_values','Valores ausentes por variável','Células ausentes'))
    # Persistir auditoria antes de interromper diante de contrato inválido.
    require_valid_panel(panel)
    cpmu=[]
    for channel in channels(panel):
        cost=safe_divide(panel[channel+'_spend'],panel[channel+'_impression'])
        cpmu.append(dict(channel=channel,undefined=int(cost.isna().sum()),**describe(cost)))
    costs=table(pd.DataFrame(cpmu),'cost_per_media_unit',False)
    text=f'''Recebemos {len(panel):,} registros, {panel[GEO].nunique()} geos e {panel[TIME].nunique()} semanas, de {panel[TIME].min().date()} a {panel[TIME].max().date()}. A grade é semanal, completa e sem duplicatas, nulos ou violações de domínio verificadas. População é constante dentro de cada geo.

O CSV original tem uma coluna de índice exportado, validada como 0…N−1 e removida apenas da cópia processada. Conversões são valores contínuos simulados; controles podem ser negativos na escala fornecida. Há {len(channels(panel))} canais pagos, uma mídia orgânica e Promo. Não há reach/frequency; nenhuma variável desse tipo foi inventada.

CPMU = gasto/impressões. {int(costs.undefined.sum())} razões são indefinidas por ausência de impressões e permanecem NaN. Conferir os contadores de inconsistências na auditoria. Isso distingue zero atividade de custo zero.'''
    return result('00_data_audit',text,{'data_audit':audit_table,'dictionary':dictionary_table,'CPMU':costs},figures,'Distribuições, concentração de investimento, zeros e extremos.')

@tracked('01')
def general(panel):
    require_valid_panel(panel)
    nat=national(panel)
    desc=table(pd.DataFrame({c:describe(nat[c]) for c in analytical_columns(panel)}).T,'national_descriptive')
    total_spend=panel[[c+'_spend' for c in channels(panel)]].sum().sum()
    summaries=[];activities=[];runs=[]
    for channel in channels(panel):
        media=panel[channel+'_impression'];spend=panel[channel+'_spend']
        active=media>0
        summaries.append(dict(channel=channel,total_media_units=media.sum(),total_spend=spend.sum(),spend_share=spend.sum()/total_spend,
                              active_periods=panel.loc[active,TIME].nunique(),active_geos=panel.loc[active,GEO].nunique(),
                              cpmu=spend.sum()/media.sum() if media.sum()>0 else np.nan,**describe(media)))
        for geo,group in panel.groupby(GEO,sort=True):
            indicator=group[channel+'_impression']>0
            ids=indicator.ne(indicator.shift()).cumsum()
            for _,segment in group.assign(active=indicator,run=ids).groupby('run'):
                runs.append(dict(channel=channel,geo=geo,active=bool(segment.active.iloc[0]),start=segment[TIME].min(),end=segment[TIME].max(),weeks=len(segment)))
        activities.append(dict(channel=channel,active_cells=int(active.sum()),zero_cells=int((~active).sum()),active_share=active.mean(),
                               active_periods=panel.loc[active,TIME].nunique(),active_geos=panel.loc[active,GEO].nunique()))
    summary=table(pd.DataFrame(summaries).set_index('channel'),'channel_summary')
    activity=table(pd.DataFrame(activities).set_index('channel'),'channel_activity')
    run_table=table(pd.DataFrame(runs),'activity_runs',False)
    table(run_table.groupby(['channel','active']).weeks.agg(['count','mean','max']),'activity_streaks')
    extremes=table(outliers(panel,analytical_columns(panel)),'outliers',False)
    table(summary[['total_spend','spend_share']],'spend_share')
    figs=[plots.lines(nat[[KPI]],'general','national_kpi','Conversões nacionais por semana','Conversões sintéticas'),
          plots.bars(summary.spend_share.sort_values(ascending=False),'general','spend_share','Participação no investimento total','Fração do gasto'),
          plots.bars(activity.active_share,'general','channel_activity','Atividade dos canais no painel','Fração de células com mídia > 0')]
    fig,axes=plt.subplots(1,2,figsize=(10,4))
    axes[0].hist(nat[KPI],bins=20,color='#245b78');axes[0].set(xlabel='Conversões nacionais/semana',ylabel='Semanas',title='Distribuição nacional do KPI')
    axes[1].boxplot(nat[KPI]);axes[1].set(ylabel='Conversões nacionais/semana',title='Boxplot do KPI')
    figs.append(plots.save(fig,'general','kpi_distribution'))
    text=f'''O KPI nacional tem média semanal de {nat[KPI].mean():,.0f} conversões sintéticas e CV de {desc.loc[KPI,'cv']:.1%}. O agregado nacional soma conversões entre geos; não soma taxas.

O maior share de gasto é de {summary.spend_share.idxmax()} ({summary.spend_share.max():.1%}). Share mede alocação, não retorno. A atividade varia de {activity.active_share.min():.1%} a {activity.active_share.max():.1%} das células GEO × semana. Exportamos todas as sequências de atividade e zeros, sem classificar com limiares arbitrários.

Foram sinalizados {len(extremes)} pares observação/variável por IQR (1,5×) ou MAD (|z modificado|>3,5). São regras de triagem, não critérios de remoção. Séries esparsas e geos grandes podem ser sinalizados legitimamente. Quando MAD é zero o escore fica indefinido. Nenhum extremo foi removido.'''
    return result('01_eda_general',text,{'national_descriptive':desc,'channel_summary':summary,'activity':activity},figs,'Dinâmica temporal dos sinais e seus controles.')

@tracked('02')
def temporal(panel):
    from statsmodels.tsa.seasonal import STL
    from statsmodels.tsa.stattools import acf
    nat=national(panel);table(nat,'national_timeseries')
    figs=[]
    smooth=nat[[KPI]].assign(media_movel_13_semanas=nat[KPI].rolling(13,min_periods=13).mean())
    figs.append(plots.lines(smooth,'temporal','kpi_trend','KPI e média móvel retrospectiva (13 semanas)','Conversões sintéticas'))
    stl=STL(nat[KPI],period=52,robust=True).fit()
    stl_frame=pd.DataFrame({'observado':nat[KPI],'tendencia':stl.trend,'sazonal':stl.seasonal,'residuo':stl.resid},index=nat.index)
    table(stl_frame,'kpi_stl_52')
    fig=stl.plot();fig.set_size_inches(11,8);figs.append(plots.save(fig,'temporal','kpi_stl_52'))
    changes=nat[[KPI]].assign(difference=nat[KPI].diff(),pct_change=nat[KPI].pct_change())
    table(changes.reindex(changes.difference.abs().sort_values(ascending=False).index),'kpi_level_changes')
    table(pd.DataFrame({'lag':np.arange(53),'acf':acf(nat[KPI],nlags=52)}),'kpi_acf',False)
    cost_rows=[]
    for channel in channels(panel):
        media=nat[channel+'_impression'];spend=nat[channel+'_spend'];cost=safe_divide(spend,media)
        fig,axes=plt.subplots(3,1,figsize=(11,7),sharex=True)
        for ax,series,label in zip(axes,[media,spend,cost],['Impressões','Gasto (moeda não especificada)','Gasto / impressão']):
            ax.plot(series.index,series);ax.set_ylabel(label)
        axes[2].set_ylim(0,cost.max()*1.08);axes[2].ticklabel_format(axis='y',style='plain',useOffset=False)
        axes[2].text(.01,.78,f'CV relativo={cost.std(ddof=0)/cost.mean():.2e}; variação microscópica',transform=axes[2].transAxes,fontsize=8)
        axes[0].set_title(f'{channel}: volumes, gasto e CPMU nacionais');axes[-1].set_xlabel('Semana')
        figs.append(plots.save(fig,'temporal',channel+'_timeseries'))
        z=nat[[KPI,channel+'_impression']].apply(lambda x:(x-x.mean())/x.std(ddof=0))
        figs.append(plots.lines(z,'temporal',channel+'_kpi_z',f'{channel} × KPI: co-movimento descritivo','Desvios padrão da própria série'))
        cost_rows.append(cost.rename(channel))
    table(pd.concat(cost_rows,axis=1),'national_cpmu')
    control_stats=[]
    for col in CONTROLS+NON_MEDIA+ORGANIC:
        figs.append(plots.lines(nat[[col]],'temporal',col+'_time',f'{col}: trajetória nacional', 'Impressões' if col in ORGANIC else 'Média ponderada por população'))
        fig,ax=plt.subplots(figsize=(7,4));ax.hist(panel[col],bins=25);ax.set(title=f'{col}: distribuição GEO × semana',xlabel='Valor na escala fornecida',ylabel='Observações')
        figs.append(plots.save(fig,'temporal',col+'_distribution'))
        control_stats.append(dict(variable=col,unique=panel[col].nunique(),range=panel[col].max()-panel[col].min(),**describe(panel[col])))
    control_stats=table(pd.DataFrame(control_stats),'control_temporal_summary',False)
    peak=nat[KPI].idxmax(); low=nat[KPI].idxmin()
    text=f'''O máximo nacional ocorre em {peak.date()} ({nat.loc[peak,KPI]:,.0f}) e o mínimo em {low.date()} ({nat.loc[low,KPI]:,.0f}). A média móvel de 13 semanas suaviza a série sem antecipar valores futuros; é apenas visual.

A decomposição STL usa período 52 como aproximação anual para dados semanais. Há apenas {len(nat)/52:.1f} ciclos: tendência, sazonalidade e mudanças de nível não são evidência confirmatória de mecanismos de negócio. Nenhum teste formal de quebra foi feito. As maiores mudanças e a ACF foram exportadas.

Todos os canais têm gráficos separados de impressões, gasto, CPMU e comparação padronizada com KPI. Controles e Promo são agregados por média ponderada por população porque somar índices sintéticos não tem interpretação. A mídia orgânica é somada. Existem {int((control_stats['std']==0).sum())} variáveis constantes entre os controles/tratamentos apresentados. Valores próximos de constantes devem ser avaliados na sua escala, sem corte universal.'''
    return result('02_eda_temporal',text,{'control_temporal_summary':control_stats,'national_timeseries':nat},figs,'Heterogeneidade entre geos e decomposição within/between.')

@tracked('05')
def relationships(panel):
    columns=analytical_columns(panel)
    nat=national(panel)[columns]
    within=panel[columns]-panel.groupby(GEO)[columns].transform('mean')
    two_way=within-panel.groupby(TIME)[columns].transform('mean')+panel[columns].mean()
    levels={'national':nat,'overall':panel[columns],'within':within,'two_way':two_way}
    figs=[];pairs=[]
    for level,data in levels.items():
        for method in ['pearson','spearman']:
            corr=data.corr(method=method);table(corr,f'correlation_{level}_{method}')
            if method=='pearson':
                figs.append(plots.heatmap(corr,'relationships',f'correlation_{level}',f'Correlação {method} — {level}',cmap='RdBu_r',vmin=-1,vmax=1))
            for suffix in ['_impression','_spend']:
                selected=[c+suffix for c in channels(panel)]
                table(corr.loc[selected,selected],f'{suffix[1:]}_correlation_{level}_{method}')
            for i,left in enumerate(columns):
                for right in columns[i+1:]: pairs.append(dict(level=level,method=method,left=left,right=right,correlation=corr.loc[left,right]))
    summary=table(pd.DataFrame(pairs),'correlation_summary',False)
    # Não incluir spend junto com impressions: custo quase fixo duplica o sinal por construção.
    predictors=[c+'_impression' for c in channels(panel)]+ORGANIC+CONTROLS+NON_MEDIA
    vif=pd.concat([vif_table(data[predictors],level) for level,data in levels.items()],ignore_index=True)
    table(vif,'vif_summary',False)
    figures=vif.pivot(index='variable',columns='level',values='vif')
    figs.append(plots.heatmap(np.log10(figures.replace([np.inf,-np.inf],np.nan)),'relationships','vif','log10(VIF): colunas comparáveis; sem exclusão automática'))
    lag_rows=[]
    for channel in channels(panel):
        for lag in range(9):
            aligned=pd.concat([nat[channel+'_impression'].shift(lag),nat[KPI]],axis=1).dropna()
            lag_rows.append(dict(channel=channel,lag_weeks=lag,n=len(aligned),correlation=aligned.iloc[:,0].corr(aligned.iloc[:,1])))
    lags=table(pd.DataFrame(lag_rows),'exploratory_lags',False)
    figs.append(plots.lines(lags.pivot(index='lag_weeks',columns='channel',values='correlation'),'relationships','lags','Correlação mídia(t−k) × KPI(t); descritiva','Pearson'))
    strongest=summary[(summary.level=='within')&(summary.method=='pearson')&(summary.left.isin(predictors))&(summary.right.isin(predictors))].copy()
    strongest=strongest.loc[strongest.correlation.abs().sort_values(ascending=False).index]
    text=f'''Exportamos Pearson e Spearman em quatro níveis: nacional, painel bruto, within-geo e residual two-way. Within remove a média de cada geo; two-way remove também a média semanal comum. Spearman de resíduos mede a ordenação dos resíduos e não é uma correlação parcial de postos.

O maior VIF within entre preditores é {vif.loc[vif.level=='within','vif'].max():.2f}. A regressão auxiliar inclui intercepto e colunas padronizadas. Spend e impressões são diagnosticados em matrizes separadas; colocá-los juntos no VIF duplicaria sinais de custo praticamente fixo. Constantes são indefinidas e dependência linear perfeita gera infinito.

A maior associação absoluta within entre preditores distintos é {strongest.iloc[0]['left']} × {strongest.iloc[0]['right']} ({strongest.iloc[0].correlation:.3f}); o ranking exclui pares gasto–impressões do mesmo canal. Lags 0–8 são exploratórios, sem selecionar adstock. Não calculamos p-valores que presumiriam independência das {len(panel):,} linhas: existe dependência temporal e geográfica.

Diferenças entre correlações nacionais e within podem resultar de composição populacional, tendência, sazonalidade e mídia alocada em antecipação à demanda. Correlação mídia–KPI não constitui efeito de mídia.'''
    return result('05_eda_relationships',text,{'vif':vif,'correlations':strongest.head(15),'lags':lags},figs,'Checagens independentes da ferramenta oficial e comparação de definições.')
