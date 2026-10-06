from .provenance import tracked, record
"""Exportação, resultados calculados e checkpoints didáticos."""
import json
import logging
from pathlib import Path
import pandas as pd
from .config import ROOT

def table(frame, name: str, index: bool=True):
    if isinstance(frame,pd.Series): frame=frame.to_frame()
    path=ROOT/'outputs/tables'/f'{name}.csv'
    frame=frame.copy()
    if 'cv' in frame.columns:
        names=frame['variable'] if 'variable' in frame else pd.Series(frame.index,index=frame.index)
        mask=names.isin(['competitor_sales_control','sentiment_score_control','Promo'])
        frame['cv_interpretation']='razão descritiva; verificar domínio'
        frame.loc[mask,'cv']=float('nan');frame.loc[mask,'cv_interpretation']='não interpretável: índice centrado/tratamento zero-inflado'
    frame.to_csv(path,index=index)
    record(path)
    logging.info('Tabela: %s (%s linhas)',path,len(frame))
    return frame

def result(chapter: str, text: str, tables: dict, figures: list, next_step: str):
    from .investigation import enrich
    extra=enrich(chapter)
    text+='\n\n'+extra['text'];tables.update(extra['tables']);figures.extend(extra['figures'])
    if chapter.startswith('07'):
        for name in ['findings.md','eda_story.md']:
            path=ROOT/'docs'/name;path.write_text(path.read_text()+'\n\n## Revisão após auditoria\n\n'+extra['text']);record(path)
    narrative=f'''### Resultado observado e conclusão parcial

{text}

### O que ainda NÃO podemos concluir

As relações são descritivas. Não estimamos ROI, contribuição incremental ou efeitos causais.
Os dados são simulados: padrões não descrevem um mercado real e não validam, por si, a identificação de um MMM.

### CHECKPOINT

- **O que descobrimos?** {extra['text'].split(chr(10)+chr(10))[0]}
- **Quais problemas apareceram?** {extra['limitation']}
- **O que falta investigar?** {next_step}
- **Podemos avançar?** Podemos prosseguir com a investigação exploratória após revisar estes achados; isso não aprova automaticamente a modelagem.
'''
    (ROOT/'outputs/reports'/f'{chapter}.md').write_text(narrative,encoding='utf-8')
    record(ROOT/'outputs/reports'/f'{chapter}.md')
    return dict(chapter=chapter,narrative=narrative,tables=tables,figures=figures)

def show(report,part="all"):
    from IPython.display import display, Markdown, Image
    if part in ['all','summary']:display(Markdown(report['narrative']))
    if part=='summary':return
    for name,frame in report['tables'].items():
        display(Markdown(f'**{name}** — {len(frame)} linhas; CSV completo em `outputs/tables/`.'))
        if len(frame)<=50:
            with pd.option_context('display.max_rows',60,'display.max_columns',None):display(frame)
        else:
            display(Markdown('Amostra das primeiras 12 linhas; sínteses selecionadas abaixo e CSV integral disponível.'));display(frame.head(12))
    for path in report['figures']:
        if report['chapter'].startswith('04') and '_geo_time' in path.stem and (path.stem.startswith(('Channel0','Channel1','Channel4')) or '_spend' in path.stem):
            display(Markdown(f"Apêndice: [{path.stem}](https://github.com/thiagossilva17/MMM_Google_Meridian_Project/blob/main/{path.with_suffix('.svg').relative_to(ROOT)})"));continue
        from .investigation import figure_comment
        display(Markdown(figure_comment(path)))
        display(Image(filename=str(path),width=950))

@tracked('07')
def conclusions(panel):
    """Consolida somente evidências existentes; exige capítulos 00–06 completos."""
    from .provenance import require_stages
    require_stages()
    folder=ROOT/'outputs/tables'
    def read(name): return pd.read_csv(folder/f'{name}.csv')
    audit=read('data_audit').set_index('metric').value
    variance=read('within_between_variance').set_index('variable')
    pc=read('geo_time_r2_per_capita').set_index('variable')
    channel=read('channel_summary').set_index('channel')
    official=read('meridian_eda_checks')
    vif=read('vif_summary')
    readiness=[]
    def row(dim,question,evidence,finding,implication):
        readiness.append(dict(Dimension=dim,Question=question,Evidence=evidence,Finding=finding,Modeling_implication=implication))
    row('integridade','Painel completo?', 'data_audit',f"{audit['rows']} linhas, {audit['geos']} geos, {audit['periods']} semanas; completude {audit['panel_completeness']}",'Contrato validado; preservar raw e schema.')
    row('missing','Há valores ausentes?', 'missing_summary',f"{audit['missing_cells']} células ausentes",'Não imputar dados completos.')
    out=read('outliers')
    row('outliers','Há extremos descritivos?', 'outliers',f'{len(out)} pares observação/variável sinalizados por IQR ou MAD','Revisão por caso e grupo em outlier_case_review; manter dados simulados sem evidência de corrupção.')
    for role,cols in [('KPI variation',['conversions']),('media variation',[c for c in variance.index if c.endswith('_impression')]),('spend variation',[c for c in variance.index if c.endswith('_spend')]),('control collinearity',[c for c in variance.index if c.endswith('_control')])]:
        selected=variance.loc[cols]
        row(role,'Existe variação?', 'within_between_variance',f"{(selected.total_variance>0).sum()}/{len(cols)} variáveis com variância positiva; resíduo two-way entre {selected.residual_geo_time_share.min():.2%} e {selected.residual_geo_time_share.max():.2%}",'Variação é necessária, não suficiente para identificar efeitos.')
    for dim,metric in [('temporal variation','r2_time'),('geo variation','r2_geo'),('within variation','within_share'),('between variation','between_share'),('geo-time variation','residual_geo_time_share'),('R² geo','r2_geo'),('R² time','r2_time')]:
        media=variance.loc[channel.index+'_impression']
        row(dim,'Quanto varia a mídia paga?', 'geo_time_r2',f'{metric}: {media[metric].min():.2%} a {media[metric].max():.2%}','Avaliar também escala por população e colinearidade conjunta.')
    row('population scaling','A geografia é apenas tamanho?', 'geo_time_r2_per_capita',f"Resíduo two-way por habitante: {pc.residual_geo_time_share.min():.2%} a {pc.residual_geo_time_share.max():.2%}",'O ajuste por população muda a leitura; não substituir inputs brutos do Meridian.')
    mix=read('media_mix').set_index('geo')
    row('media mix heterogeneity','O mix difere?', 'media_mix',f'Amplitude máxima do share de um canal entre geos: {100*(mix.max()-mix.min()).max():.2f} p.p.','Mix acumulado relativamente semelhante pode coexistir com execução semanal diferente.')
    row('channel collinearity','Os sinais são redundantes?', 'vif_summary',f'VIF máximo overall={vif.loc[vif.level=="overall","vif"].max():.2f}; within={vif.loc[vif.level=="within","vif"].max():.2f}','Não remover canais mecanicamente; diagnóstico não incorpora adstock/saturação.')
    ratio=read('meridian_data_adequacy')
    row('data adequacy','Guardrails oficiais?', 'meridian_eda_checks',f"{len(official)} achados: {official.severity.value_counts().to_dict()}; razão dados/parâmetros={ratio['ratio'].iloc[0]:.2f}",'Checagens dependem da especificação provisória; revisar antes do ajuste.')
    ready=table(pd.DataFrame(readiness),'readiness_report',False)
    paid=variance.loc[channel.index+'_impression']
    paid_pc=pc.loc[channel.index+'_impression']
    sparse=channel.zero_share.idxmax()
    text=f'''1. **Estrutura.** O painel tem {audit['geos']} geos × {audit['periods']} semanas = {audit['rows']} observações, completude de {float(audit['panel_completeness']):.1%} e {audit['missing_cells']} células ausentes. A chave geo–tempo foi validada.

2. **Tempo.** Todos os {len(channel)} canais pagos variam; a parcela within-geo da variância fica entre {paid.within_share.min():.1%} e {paid.within_share.max():.1%}. {sparse} é o canal com mais zeros: {channel.loc[sparse,'zero_share']:.1%} das células, com {channel.loc[sparse,'spend_share']:.1%} do gasto. A tabela de atividade e os gráficos distinguem semanas sem mídia de mudanças de intensidade. Movimentos de nível e sazonalidade são exploratórios.

3. **Geografia.** As médias por geo explicam de {paid.r2_geo.min():.1%} a {paid.r2_geo.max():.1%} da variância bruta da mídia paga. Rankings de volume dependem de população; mix e medidas por habitante oferecem lentes complementares.

4. **GEO × TEMPO.** Após retirar médias de geo e de semana, permanece de {paid.residual_geo_time_share.min():.1%} a {paid.residual_geo_time_share.max():.1%} da variância bruta de mídia paga; por habitante, de {paid_pc.residual_geo_time_share.min():.1%} a {paid_pc.residual_geo_time_share.max():.1%}. Esse componente é perdido ao observar apenas o agregado nacional. O painel contém variação potencialmente informativa, mas o resíduo pode conter ruído, endogeneidade e confundimento. Comparar com a decomposição per capita é essencial: diferenças multiplicativas de tamanho também podem gerar resíduos aditivos.

5. **Identificabilidade.** R², correlações, VIF e os alertas oficiais devem orientar hipóteses de especificação. Nenhuma dessas métricas prova identificação causal ou que um modelo geo terá melhor previsão que o nacional. Essa comparação exige futura modelagem com validação temporal comum, priors justificados e diagnósticos posteriores.

**Prontidão:** a integridade permite continuar o estudo metodológico, com a revisão dos seis alertas documentada e critérios por canal/controle em readiness_actions. As limitações da simulação permanecem. Não há recomendação de alocação de orçamento nesta EDA.'''
    (ROOT/'docs/findings.md').write_text('# Achados da EDA\n\n'+text+'\n\n'+ready.to_markdown(index=False),encoding='utf-8')
    chapters=sorted((ROOT/'outputs/reports').glob('0[0-6]_*.md'))
    (ROOT/'docs/eda_story.md').write_text('# Da auditoria à prontidão para MMM\n\n'+'\n\n'.join(p.read_text() for p in chapters)+'\n\n'+text,encoding='utf-8')
    import matplotlib.pyplot as plt
    from .plots import save
    fig,axes=plt.subplots(1,2,figsize=(12,5))
    paid[['between_share','r2_time','residual_geo_time_share']].rename(columns={'between_share':'GEO','r2_time':'Semana','residual_geo_time_share':'Resíduo GEO × tempo'},index=lambda x:x.replace('_impression','')).plot.bar(stacked=True,ax=axes[0],rot=0)
    axes[0].legend(loc='upper center',bbox_to_anchor=(.5,1.25),ncol=3,fontsize=8);axes[0].set_xlabel('Canal')
    axes[0].set_title('Mídia paga: decomposição da variância');axes[0].set_ylabel('Fração da variância total')
    official.severity.value_counts().plot.bar(ax=axes[1],color='#245b78')
    axes[1].set_title('Achados oficiais por severidade');axes[1].set_ylabel('Número de achados')
    path=save(fig,'relationships','readiness_dashboard')
    return result('07_eda_conclusions',text,{'readiness_report':ready},[path],'Desenho causal, especificação, priors, holdout temporal e posterior em fase futura.')
