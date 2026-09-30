# # TCC — Análise exploratória dos dados sintéticos Google Meridian
# Etapa 1: compreender, auditar e preparar dados geo-temporais. Não estima efeitos causais.
# 
# Base principal: `geo_all_channels.csv`. Comparações: `geo_media.csv` e `geo_media_rf.csv`.
# São cenários sintéticos diferentes: não juntar registros nem comparar KPIs como se fossem a mesma empresa.
# O notebook é independente do pacote Meridian e roda em CPU no Colab com pandas, numpy e matplotlib.
# Fonte fixada por commit; o primeiro carregamento usa os arquivos locais quando disponíveis ou baixa os CSVs oficiais.
# 
# Pergunta do TCC: como um MMM Bayesiano hierárquico permite estimar efeitos de mídia e apoiar alocação em dados geo-temporais? A EDA estabelece a adequação dos dados e as limitações de identificação antes da inferência.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import hashlib, json, platform, urllib.request
from IPython.display import display
plt.rcParams.update({'figure.figsize': (11, 4), 'axes.grid': True, 'grid.alpha': .2})
pd.set_option('display.max_columns', 30)
ROOT = Path.cwd() if (Path.cwd() / 'data').exists() else (Path.cwd().parent if (Path.cwd().parent / 'data').exists() else Path.cwd() / 'meridian_eda')
DATA = ROOT / 'data'; OUT = ROOT / 'reports' / 'eda'
DATA.mkdir(parents=True, exist_ok=True); OUT.mkdir(parents=True, exist_ok=True)
UPSTREAM_COMMIT = '58ea51bb6225717fce55949ae02708308ce0e090'
BASE_URL = f'https://raw.githubusercontent.com/google/meridian/{UPSTREAM_COMMIT}/meridian/data/simulated_data/csv/'
datasets = {}; provenance = {}
for name in ['geo_all_channels', 'geo_media', 'geo_media_rf']:
    path = DATA / f'{name}.csv'
    if not path.exists():
        with urllib.request.urlopen(BASE_URL + path.name, timeout=60) as response:
            path.write_bytes(response.read())
    raw = path.read_bytes()
    datasets[name] = pd.read_csv(path).drop(columns=['Unnamed: 0'], errors='ignore')
    datasets[name]['time'] = pd.to_datetime(datasets[name]['time'], format='%Y-%m-%d', errors='raise')
    provenance[name] = {'url': BASE_URL + path.name, 'sha256': hashlib.sha256(raw).hexdigest()}
versions = {'python': platform.python_version(), 'pandas': pd.__version__, 'numpy': np.__version__, 'upstream_commit': UPSTREAM_COMMIT, 'sources': provenance}
(OUT / 'provenance.json').write_text(json.dumps(versions, indent=2))
df = datasets['geo_all_channels'].sort_values(['geo', 'time']).reset_index(drop=True)
paid = [c for c in df if c.startswith('Channel') and c.endswith('_impression')]
spend = [c.replace('_impression', '_spend') for c in paid]
controls = [c for c in df if c.endswith('_control')]
organic = ['Organic_channel0_impression']
print('Versões:', versions['python'], versions['pandas'], versions['numpy'])
def table(frame, filename):
    frame.to_csv(OUT / (filename + '.csv'), index=True)
    display(frame)
def show(name):
    plt.tight_layout(); plt.savefig(OUT / (name + '.png'), dpi=160, bbox_inches='tight'); plt.show(); plt.close()


# ## 1. Inventário e dicionário
# Cada linha representa uma região em uma semana. As 6.240 linhas do painel principal não são 6.240 observações independentes: regiões compartilham condições de mercado e semanas têm dependência temporal.
# 
# `conversions` é o KPI, não receita. Receita sintética por linha = conversions × revenue_per_conversion; some esses produtos, em vez de multiplicar totais por uma média simples.
# As unidades monetárias não estão identificadas no CSV; não atribuímos reais, euros ou dólares.
# Os nomes Channel0–Channel4 não identificam TV, Search ou Social. Os controles são escores sintéticos; valores negativos não são vendas negativas. `Promo` é intensidade contínua, não uma flag binária.

inventory = pd.DataFrame([{'base': name, 'linhas': len(d), 'colunas_uteis': len(d.columns), 'regioes': d.geo.nunique(), 'semanas': d.time.nunique(), 'inicio': d.time.min(), 'fim': d.time.max(), 'nulos': int(d.isna().sum().sum()), 'duplicatas_geo_time': int(d.duplicated(['geo', 'time']).sum())} for name, d in datasets.items()]).set_index('base')
table(inventory, 'inventario')
def role(c):
    if c in ['geo','time']: return 'coordenada'
    if c == 'conversions': return 'KPI não monetário'
    if c == 'revenue_per_conversion': return 'valor monetário por unidade do KPI'
    if c == 'population': return 'escala regional; constante no tempo'
    if c in controls: return 'controle sintético; mecanismo causal não documentado no CSV'
    if c == 'Promo': return 'tratamento não mídia; intensidade contínua'
    if c.startswith('Organic'): return 'exposição orgânica; sem gasto informado'
    return 'gasto pago' if c.endswith('_spend') else 'exposição paga'
table(pd.DataFrame([{'coluna':c, 'papel':role(c), 'tipo':str(df[c].dtype), 'valores_distintos':df[c].nunique()} for c in df]).set_index('coluna'), 'dicionario')


# ## 2. Auditoria de qualidade e suporte
# Verificamos chaves, painel completo, cadência semanal, valores finitos, domínios, população constante e alinhamento entre exposição e gasto. Zeros de mídia podem representar pausas; não os imputamos. Extremos pela regra IQR são alertas descritivos, não exclusões automáticas. Removemos apenas a coluna de índice exportado `Unnamed: 0`.

audit = []
for name, d in datasets.items():
    grid = pd.MultiIndex.from_product([d.geo.unique(), sorted(d.time.unique())], names=['geo', 'time'])
    observed = pd.MultiIndex.from_frame(d[['geo','time']])
    gaps = d.sort_values(['geo','time']).groupby('geo').time.diff().dropna().dt.days
    numeric = d.select_dtypes('number')
    domain = [c for c in numeric if not c.endswith('_control')]
    audit.append({'base':name, 'faltam_geo_semanas':len(grid.difference(observed)), 'cadencia_7_dias':bool(gaps.eq(7).all()), 'nao_finitos':int((~np.isfinite(numeric)).sum().sum()), 'negativos_fora_controles':int(numeric[domain].lt(0).sum().sum()), 'populacao_positiva':bool(d.population.gt(0).all()), 'max_populacoes_por_geo':int(d.groupby('geo').population.nunique().max())})
table(pd.DataFrame(audit).set_index('base'), 'auditoria')
assert not df.duplicated(['geo','time']).any()
assert len(df) == df.geo.nunique()*df.time.nunique()
assert np.isfinite(df.select_dtypes('number')).all().all()
assert df.population.gt(0).all()
num = df.select_dtypes('number')
q1, q3 = num.quantile(.25), num.quantile(.75); iqr=q3-q1
quality = pd.DataFrame({'nulos':num.isna().sum(), 'zeros_pct':num.eq(0).mean()*100, 'negativos':num.lt(0).sum(), 'extremos_IQR':((num.lt(q1-1.5*iqr)) | (num.gt(q3+1.5*iqr))).sum(), 'constante':num.nunique().le(1)})
table(quality, 'qualidade_colunas')
table(num.describe(percentiles=[.01,.05,.25,.5,.75,.95,.99]).T, 'estatisticas')
print('Conversões fracionárias (%):', 100*df.conversions.mod(1).ne(0).mean())
print('Conversões/população: intervalo', (df.conversions/df.population).min(), (df.conversions/df.population).max())
print('Isso não é probabilidade individual de conversão nem contagem de clientes únicos.')


# ## 3. Investimento, exposição e custo
# CPM = 1.000 × soma(gasto)/soma(impressões). É um custo observado, não ROI.
# A razão receita total/gasto total descreve o conjunto de receitas, inclusive baseline, promoções e mídia orgânica; não mede retorno incremental de publicidade.
# Uma relação praticamente determinística entre gasto e impressões indica preços artificiais constantes. Não inclua ambos como regressoras independentes para o mesmo canal.

df['receita_sintetica'] = df.conversions*df.revenue_per_conversion
df['gasto_total'] = df[spend].sum(axis=1)
rows=[]
for imp, cost in zip(paid, spend):
    active=df[imp].gt(0); cpm=1000*df.loc[active,cost]/df.loc[active,imp]
    rows.append({'canal':imp.replace('_impression',''), 'gasto':df[cost].sum(), 'impressions':df[imp].sum(), 'participacao_gasto_pct':100*df[cost].sum()/df.gasto_total.sum(), 'zero_exposicao_pct':100*(~active).mean(), 'zero_inconsistente':int((df[imp].eq(0)!=df[cost].eq(0)).sum()), 'CPM_ponderado':1000*df[cost].sum()/df[imp].sum(), 'CV_CPM_ativo':cpm.std()/cpm.mean(), 'corr_gasto_exposicao':df[imp].corr(df[cost])})
channels=pd.DataFrame(rows).set_index('canal'); table(channels,'canais')
print('Receita sintética total:',df.receita_sintetica.sum())
print('Gasto total:',df.gasto_total.sum())
channels.gasto.sort_values().plot.barh(title='Investimento total por canal — unidade monetária sintética'); show('gasto_canais')


# ## 4. Tempo: tendência, variabilidade, calendário e dependência
# Agregamos apenas grandezas aditivas (KPI, receita, gasto, impressões). A população é repetida semanalmente: para população nacional, some uma observação por região.
# Índices base 100 permitem comparar movimentos sem confundir escalas. Perfis mensais são descritivos; três anos não confirmam sazonalidade estável. ACF e correlações defasadas não identificam adstock.

weekly = df.groupby('time')[['conversions','receita_sintetica','gasto_total']+paid+organic].sum()
table(weekly.describe().T,'resumo_semanal')
weekly[['conversions','gasto_total']].div(weekly[['conversions','gasto_total']].iloc[0]).mul(100).plot(title='KPI e gasto — índice da primeira semana = 100'); show('series_indices')
weekly[paid].plot(title='Exposição semanal paga agregada'); show('exposicao_semanal')
monthly=weekly.assign(mes=weekly.index.month).groupby('mes')[['conversions','gasto_total']].mean()
monthly.div(monthly.mean()).plot.bar(title='Perfil mensal médio relativo à média; descritivo'); show('perfil_mensal')
acf=pd.DataFrame({c:[weekly[c].autocorr(lag=l) for l in range(1,14)] for c in ['conversions','gasto_total']}, index=range(1,14))
table(acf,'autocorrelacao_semanal'); acf.plot.bar(title='Autocorrelação — lags de 1 a 13 semanas'); show('acf')
weekly[['conversions','gasto_total']].pct_change().dropna().plot(title='Variação semanal relativa; extremos preservados'); show('variacoes_semanais')


# ## 5. Heterogeneidade regional e informação dentro de cada região
# Uma região grande pode ter mais anúncios e mais conversões simplesmente por tamanho. Comparamos valores brutos e por habitante e medimos variabilidade temporal por região. Normalização aqui é diagnóstico; o Meridian possui transformações próprias e não deve receber dados pré-normalizados sem uma decisão explícita.

geo = df.groupby('geo').agg(populacao=('population','first'), conversoes=('conversions','sum'), receita=('receita_sintetica','sum'), gasto=('gasto_total','sum'))
geo['conversoes_por_habitante_semana']=geo.conversoes/geo.populacao/df.time.nunique()
geo['gasto_por_habitante_semana']=geo.gasto/geo.populacao/df.time.nunique()
geo['participacao_gasto_pct']=100*geo.gasto/geo.gasto.sum()
table(geo.sort_values('gasto',ascending=False),'regioes')
fig,axes=plt.subplots(1,2,figsize=(12,4))
axes[0].scatter(geo.populacao,geo.conversoes); axes[0].set(xlabel='População',ylabel='KPI total',title='Tamanho regional e KPI')
axes[1].scatter(geo.gasto_por_habitante_semana,geo.conversoes_por_habitante_semana); axes[1].set(xlabel='Gasto/habitante/semana',ylabel='KPI/habitante/semana',title='Associação entre regiões')
show('heterogeneidade')
within_cv=df.groupby('geo')[paid+['conversions']].std()/df.groupby('geo')[paid+['conversions']].mean()
table(within_cv,'cv_temporal_por_geo')
heat=df.assign(kpi_pc=df.conversions/df.population).pivot(index='geo',columns='time',values='kpi_pc')
plt.figure(figsize=(12,7)); plt.imshow(heat,aspect='auto',cmap='viridis'); plt.yticks(range(len(heat)),heat.index,fontsize=7); plt.xlabel('Semana ordenada'); plt.colorbar(label='KPI/habitante'); plt.title('Painel geo-temporal normalizado'); show('painel_geo')


# ## 6. Correlações, confundimento e redundância
# Comparamos Pearson, Spearman, associação nacional e associações dentro de regiões. A transformação com efeitos de região e semana subtraídos é apenas um diagnóstico de covariação residual em painel balanceado; não estima causalidade.
# VIF sinaliza dependência linear entre entradas; valores elevados podem dificultar separar canais. Não removemos variáveis causais automaticamente por VIF.
# Defasagens sempre são feitas dentro de cada região para não conectar o fim de uma série ao início de outra.

features=paid+organic+controls+['Promo']
cols=features+['conversions']
raw=df[cols].corr(); rank=df[cols].corr(method='spearman')
percap=df[cols].copy()
for c in paid+organic+['conversions']: percap[c]=percap[c]/df.population
within=percap-percap.groupby(df.geo).transform('mean')
twoway=within-percap.groupby(df.time).transform('mean')+percap.mean()
table(pd.DataFrame({'Pearson_bruto':raw.conversions, 'Spearman_bruto':rank.conversions, 'Pearson_per_capita':percap.corr().conversions, 'dentro_geo_per_capita':within.corr().conversions, 'efeitos_geo_semana_removidos':twoway.corr().conversions}), 'correlacoes_kpi')
table(weekly[paid+['conversions']].corr(),'correlacao_nacional')
plt.figure(figsize=(10,8)); plt.imshow(raw,vmin=-1,vmax=1,cmap='coolwarm'); plt.xticks(range(len(cols)),cols,rotation=90,fontsize=7); plt.yticks(range(len(cols)),cols,fontsize=7); plt.colorbar(label='Pearson'); show('correlacao_bruta')
def vif_frame(X):
    X=(X-X.mean())/X.std(ddof=0)
    results=[]
    for c in X:
        y=X[c].to_numpy(); others=X.drop(columns=c).to_numpy()
        fit=np.column_stack([np.ones(len(y)),others]); beta=np.linalg.lstsq(fit,y,rcond=None)[0]
        r2=1-np.sum((y-fit@beta)**2)/np.sum((y-y.mean())**2)
        results.append({'variavel':c,'VIF':1/max(1-r2,1e-12)})
    return pd.DataFrame(results).set_index('variavel')
table(vif_frame(percap[features]),'vif_per_capita')
lagrows=[]
for c in paid:
    for lag in range(9):
        shifted=percap[c].groupby(df.geo).shift(lag)
        lagrows.append({'canal':c,'lag_semanas':lag,'corr_descritiva':shifted.corr(percap.conversions),'pares':int(shifted.notna().sum())})
lags=pd.DataFrame(lagrows); table(lags,'correlacoes_defasadas')
lags.pivot(index='lag_semanas',columns='canal',values='corr_descritiva').plot(title='Exposição anterior × KPI atual — diagnóstico não causal'); show('lags')


# ## 7. Suporte de dose, mídia orgânica e promoções
# Agrupamos exposição em quantis para inspecionar suporte. Curvatura em um gráfico observacional não demonstra saturação: pode refletir região, calendário, promoções ou endogeneidade. As curvas Hill serão estimadas na etapa Bayesiana.
# Mídia orgânica tem exposição mas nenhum gasto próprio no arquivo; não se calcula ROI orgânico com denominador zero.
# Comparar semanas com e sem promoções não é um experimento aleatorizado.

support=[]
fig,axes=plt.subplots(1,len(paid),figsize=(18,4))
for ax,c in zip(axes,paid):
    tmp=pd.DataFrame({'x':df[c]/df.population,'y':df.conversions/df.population})
    tmp['bin']=pd.qcut(tmp.x,10,duplicates='drop')
    b=tmp.groupby('bin',observed=True).agg(exposicao_pc=('x','mean'),kpi_pc=('y','mean'),n=('y','size')).reset_index(drop=True)
    b['canal']=c; support.append(b); ax.plot(b.exposicao_pc,b.kpi_pc,'o-'); ax.set(title=c.replace('_impression',''),xlabel='Impressões/habitante',ylabel='KPI/habitante')
show('dose_observacional'); table(pd.concat(support,ignore_index=True),'suporte_quantils')
promo=df.assign(promo_ativa=df.Promo.gt(0),kpi_pc=df.conversions/df.population).groupby('promo_ativa').agg(n=('conversions','size'),kpi_pc_medio=('kpi_pc','mean'),intensidade_media=('Promo','mean'))
table(promo,'promo_descritivo')
print('Promo varia de',df.Promo.min(),'a',df.Promo.max(),'; fração positiva:',df.Promo.gt(0).mean())
print('Mídia orgânica: zeros (%):',100*df[organic[0]].eq(0).mean())


# ## 8. Cenário separado de alcance e frequência
# `geo_media_rf.csv` não é uma extensão linha a linha da base principal. Channel3 possui alcance e frequência. Verificamos impressões ≈ alcance × frequência e alcance ≤ população.
# Alcance pode ser somado entre regiões disjuntas na mesma semana; não some semanas como se obtivesse pessoas únicas. Frequência nacional requer ponderação pelo alcance, nunca média simples das frequências.
# Na futura carga do Meridian, Channel3 deve entrar pelo grupo reach/frequency/rf_spend; não duplicar o canal também em media/media_spend.

rf=datasets['geo_media_rf']
reconstructed=rf.Channel3_reach*rf.Channel3_frequency
active=rf.Channel3_impression.gt(0)
rfchecks=pd.Series({'max_erro_absoluto_impressao':(reconstructed-rf.Channel3_impression).abs().max(),'max_erro_relativo_ativo':((reconstructed[active]-rf.loc[active,'Channel3_impression']).abs()/rf.loc[active,'Channel3_impression']).max(),'alcance_maior_populacao':int(rf.Channel3_reach.gt(rf.population).sum()),'freq_negativa':int(rf.Channel3_frequency.lt(0).sum()),'zeros_rf_inconsistentes':int((rf.Channel3_reach.eq(0)!=rf.Channel3_frequency.eq(0)).sum())})
table(rfchecks.to_frame('valor'),'auditoria_rf')
rfsummary=rf.groupby('time').agg(alcance=('Channel3_reach','sum'),impressoes=('Channel3_impression','sum'))
rfsummary['frequencia_ponderada']=rfsummary.impressoes/rfsummary.alcance.replace(0,np.nan)
table(rfsummary.describe().T,'resumo_rf')
rf.loc[active,'Channel3_frequency'].plot.hist(bins=30,title='Frequência de Channel3 em semanas ativas'); show('frequencia_rf')


# ## 9. Preparação de avaliação e próximos passos
# Separamos as últimas 26 semanas como proposta de holdout temporal comum a todas as regiões. Não utilizamos embaralhamento aleatório. Na modelagem, tuning, priors orientadas por dados e transformações aprendidas devem usar apenas treino. Valores anteriores de mídia podem ser necessários como histórico para carryover; o CSV começa junto com o KPI, sem pré-histórico de exposição.
# A comparação abaixo descreve mudança de suporte. Não é desempenho preditivo, pois nenhum modelo foi ajustado.
# 
# O CSV não contém nomes reais de canais, preço de produto, GQV, experimento de incrementalidade, mecanismo causal completo ou parâmetros verdadeiros do gerador. Assim, não permite identificar um caso de Paid Search nem validar recuperação de ROI verdadeiro só com esses arquivos.
# 
# Próximas etapas: DAG e premissas; ingestão no Meridian; baseline e priors alternativas; prior predictive checks; MCMC e diagnósticos R-hat/ESS/divergências; posterior predictive checks e holdout; contribuição/ROI com incerteza; curvas de resposta e mROI; otimização com limites e sensibilidade. Bom ajuste preditivo não prova identificação causal.

times=np.sort(df.time.unique()); split=pd.Timestamp(times[-26])
df['holdout']=df.time.ge(split)
comparison=df.groupby('holdout')[['conversions','gasto_total']+paid+controls+['Promo']].agg(['mean','std','min','max'])
table(comparison,'treino_holdout_descritivo')
print('Holdout a partir de',split.date(),'; treino:',(~df.holdout).sum(),'; teste:',df.holdout.sum())
# CSV limpo preserva unidades originais e não inclui variáveis derivadas para o loader.
original_cols=datasets['geo_all_channels'].columns
clean=df[original_cols].copy(); clean['time']=clean.time.dt.strftime('%Y-%m-%d')
clean.to_csv(OUT/'geo_all_channels_clean.csv',index=False)
# Máscara por coordenadas explicitamente ordenadas, para futura construção do ModelSpec.
mask=df.pivot(index='geo',columns='time',values='holdout').sort_index().sort_index(axis=1)
mask.to_csv(OUT/'holdout_geo_time.csv')
print('Tabelas e figuras disponíveis em:',OUT)


# ## 10. Ajustes conceituais recomendados para o texto do TCC
# 1. Priors hierárquicas e mais regiões não garantem identificação causal; esta depende das premissas e dos confundidores medidos.
# 2. O parâmetro de meia-saturação da Hill marca H(x)=0,5; não é, em geral, o ponto de inflexão (e curvas em C podem não ter inflexão interior).
# 3. A recursão de adstock do referencial é uma representação didática. Compare-a com a transformação efetiva e a janela finita/normalização do Meridian antes de atribuir equivalência.
# 4. Esclareça ROI como receita incremental/gasto na convenção do Meridian; isso não é lucro líquido nem a fórmula financeira (retorno-custo)/custo.
# 5. O caráter sintético sustenta demonstração metodológica. Validação de recuperação de parâmetros exige verdade conhecida e gerador documentado, além de múltiplas simulações.
# 
# Fontes: [repositório oficial](https://github.com/google/meridian), [guia de carga completa](https://developers.google.com/meridian/docs/user-guide/load-geo-data-with-organic-and-non-media), [guia de alcance/frequência](https://developers.google.com/meridian/docs/user-guide/load-geo-data-with-rf). Consultadas em 30/09/2026. Esquema e estatísticas conferidos diretamente nos CSVs do commit fixado.