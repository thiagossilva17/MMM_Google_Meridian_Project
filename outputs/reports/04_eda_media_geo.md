### Resultado observado e conclusão parcial

O mix divide cada linha GEO × canal pelo orçamento total do geo; a alocação divide cada coluna pelo orçamento do canal. Essas perguntas são diferentes. A maior amplitude de share do mix é 3.74 pontos percentuais, em Channel1.

HHI é a soma dos quadrados das participações geográficas de um canal: varia de 1/G (uniforme) a 1 (um único geo). Observamos 0.030 a 0.031, sem aplicar limiares de concorrência econômica. O inverso traduz concentração em número equivalente de geos uniformes, não em tamanho amostral efetivo.

Os CVs within variam de 0.442 a 2.153. Médias zero produzem CV indefinido. Heatmaps usam a mesma ordenação de geos por KPI total e escalas de cor próprias por variável; não comparar cores entre painéis sem ler as escalas. As versões por habitante ajudam a investigar diferenças que persistem além do tamanho dos mercados.

**Mix relativamente semelhante:** dispersões são expressas em pontos percentuais; o gráfico de desvios do nacional expõe pequenas diferenças sem sugerir forte heterogeneidade acumulada.

Channel0: mix 16.70%–20.00%, amplitude 3.30 p.p., desvio 0.74 p.p.; Spearman população×volume 0.993, população×intensidade 0.286; R² GEO bruto/per capita 0.248/0.006; resíduo per capita 0.783.

Channel1: mix 12.36%–16.10%, amplitude 3.74 p.p., desvio 0.82 p.p.; Spearman população×volume 0.987, população×intensidade 0.047; R² GEO bruto/per capita 0.144/0.004; resíduo per capita 0.765.

Channel2: mix 4.04%–6.46%, amplitude 2.42 p.p., desvio 0.57 p.p.; Spearman população×volume 0.966, população×intensidade 0.206; R² GEO bruto/per capita 0.053/0.004; resíduo per capita 0.793.

Channel3: mix 38.00%–41.36%, amplitude 3.36 p.p., desvio 0.91 p.p.; Spearman população×volume 0.994, população×intensidade 0.142; R² GEO bruto/per capita 0.390/0.005; resíduo per capita 0.648.

Channel4: mix 20.56%–23.92%, amplitude 3.37 p.p., desvio 0.79 p.p.; Spearman população×volume 0.993, população×intensidade 0.232; R² GEO bruto/per capita 0.237/0.004; resíduo per capita 0.706.

### O que ainda NÃO podemos concluir

As relações são descritivas. Não estimamos ROI, contribuição incremental ou efeitos causais.
Os dados são simulados: padrões não descrevem um mercado real e não validam, por si, a identificação de um MMM.

### CHECKPOINT

- **O que descobrimos?** **Mix relativamente semelhante:** dispersões são expressas em pontos percentuais; o gráfico de desvios do nacional expõe pequenas diferenças sem sugerir forte heterogeneidade acumulada.
- **Quais problemas apareceram?** Resíduo pode conter alternância de atividade e ruído, não apenas sinal causal.
- **O que falta investigar?** Correlações entre canais e controles, VIF e conflitos com geo/tempo.
- **Podemos avançar?** Podemos prosseguir com a investigação exploratória após revisar estes achados; isso não aprova automaticamente a modelagem.
