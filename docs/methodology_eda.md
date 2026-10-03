# Metodologia exploratória

## Objetivo e unidade observacional

A unidade é uma combinação GEO × semana. Os geos são mercados fictícios, e os dados são simulados pelo projeto Google Meridian. A investigação pergunta se o painel contém variação adicional à série nacional; não mede eficácia de canais. Não é apropriado apresentar os resultados como estudo de uma marca real.

## Proveniência e contrato

O CSV e o código upstream são identificados por commit em `data/metadata/source.json`. A verificação SHA-256 ocorre antes de cada leitura. A cópia raw não é transformada. Removemos exclusivamente o índice exportado, depois de validar a sequência, e convertemos a data na cópia processada. O contrato exige pares únicos geo–tempo, grade semanal completa, população positiva e estável, valores finitos, schema conhecido e não negatividade das grandezas cujo domínio a requer.

O descobrimento dos canais usa os pares de colunas efetivamente presentes; seus papéis são confirmados pelo notebook oficial. Colunas desconhecidas ou ausentes provocam erro para evitar classificações sem suporte. Reach/frequency não existem nesta base. A implementação não finge suportar datasets arbitrários.

## Agregação e unidades

Conversões, impressões e gasto são somados entre geos. População usa um valor por geo na comparação territorial, não soma de semanas. Controles sintéticos e Promo são médias ponderadas por população para exploração nacional. A receita derivada é `sum(conversions × revenue_per_conversion)`, e seu fator nacional é a receita dividida pelo total de conversões. Nunca somamos razões. A moeda não foi especificada pela base; não se assume BRL, USD ou EUR.

CPMU = gasto / impressões. Divisão por zero produz NaN, acompanhado de contadores de inconsistência. Total de gasto / total de impressões é diferente da média não ponderada dos CPMUs. CV = desvio padrão/média; média zero torna o CV indefinido. CV de controles centrados/negativos não é interpretado como intensidade; usamos amplitude, desvio e número de valores distintos.

## Entre mercados, dentro dos mercados e efeitos temporais

Para X_gt, m é a média global, m_g a média do geo e m_t a média da semana. Com painel balanceado e momentos ddof=0:

`V_total = mean((X_gt − m)²)`

`V_between = mean((m_g − m)²)`

`V_within = mean((X_gt − m_g)²)`

`V_total = V_between + V_within`

`R²_geo = V_between / V_total`

`R²_time = mean((m_t − m)²) / V_total`

`residual_gt = X_gt − m_g − m_t + m`

`R²_geo + R²_time + mean(residual_gt²)/V_total = 1`

Essas são regressões descritivas em dummies com intercepto. A decomposição two-way só é aplicada ao painel completo; double demeaning simples não deve ser transplantado para painéis desbalanceados. Variáveis constantes têm razões indefinidas. A variância within inclui choques nacionais, por isso não basta como prova de informação geo-temporal adicional.

Repetimos a análise em valores por 1.000 habitantes. Um painel X_gt = população_g × intensidade_t pode gerar resíduo em decomposição aditiva bruta mesmo sem execução territorial distinta. Comparar escala bruta e por habitante é essencial. Nem a decomposição nem a normalização garantem identificação causal.

## Concentração e mix

`mix_gm = gasto_gm / sum_m(gasto_gm)` responde como o orçamento do geo é dividido.

`allocation_gm = gasto_gm / sum_g(gasto_gm)` responde onde o canal investe.

HHI = soma dos quadrados dos shares geográficos. Seu intervalo é [1/G, 1]; 1/HHI é um número equivalente de geos uniformes. Não se aplicam limiares de concentração de mercado usados em defesa da concorrência. Não representa tamanho amostral efetivo.

## Tempo, extremos e atividade

A média móvel retrospectiva de 13 semanas é visual. STL com período 52 aproxima anualidade em dados semanais; três anos oferecem base limitada, e anos civis não têm exatamente 52 semanas. A decomposição não demonstra mecanismo causal nem mudança estrutural. Diferenças semanais e ACF são descritivas. Não se faz teste de estacionariedade como requisito mecânico para MMM.

Atividade é I(impressões > 0); cada sequência contínua de atividade/zero é exportada por geo e canal. IQR com fator 1,5 e z modificado por MAD com corte 3,5 são triagem explícita. MAD zero é indefinido. Sinalizações não alteram os dados. População, campanhas e controles binários contextualizam extremos.

## Dependência e redundância

Calculamos Pearson e Spearman nacional, no painel bruto, após remoção da média do geo e após remoção das médias de geo e tempo. Spearman aplicado aos resíduos não é automaticamente uma correlação parcial de postos. Não usamos p-valores ingênuos em linhas dependentes. Tendência, sazonalidade, endogeneidade, composição e falácia ecológica limitam a interpretação.

VIF_j = 1/(1−R²_j), com intercepto na regressão auxiliar e colunas padronizadas. Constantes são indefinidas; dependência linear exata gera infinito. Os preditores incluem mídia paga e orgânica, controles e Promo; não incluem o KPI. Gasto e impressões não entram juntos, para não duplicar sinais de custo unitário. Não existe remoção automática por VIF. A transformação futura por adstock/saturação pode modificar a colinearidade.

Lags 0–8 alinham mídia anterior com KPI atual no agregado nacional e informam N após o deslocamento. Não selecionam adstock nem demonstram efeito defasado.

## Comparação com a EDA oficial

Meridian 2.1.0 no commit fixado usa `DataFrameInputDataBuilder` e `meridian.model.eda.meridian_eda.MeridianEDA`. O construtor gera amostras da prior automaticamente; o projeto não chama amostragem posterior. O relatório oficial completo inclui diagnósticos de prior com defaults provisórios, sem interpretá-los como estimativas causais.

R² oficial é ajustado e calculado em variáveis transformadas. A reconciliação independente utiliza as mesmas escalas e soma de quadrados: `R²_ajustado = 1 − (1−R²)(N−1)/(N−K)`, com K igual ao número de grupos para regressão em dummies. A tolerância 1e-5 é numérica, não um threshold de aceitação de dados. Defaults e limiares do Meridian não foram alterados.

O guardrail dados/parâmetros utiliza `G×T / (G−1 + knots + controles + tratamentos)`. Não conta todos os efeitos locais como independentes e não mede amostra efetiva. A adequação final dependerá de incerteza posterior, diagnóstico de convergência e holdout.

## Fontes primárias verificadas

- [Código e dados oficiais no commit usado](https://github.com/google/meridian/tree/02111531f8661373aa7b6ba31c316c67d72d1dd2)
- [Demo oficial: schema e InputDataBuilder](https://github.com/google/meridian/blob/02111531f8661373aa7b6ba31c316c67d72d1dd2/demo/Meridian_Getting_Started.ipynb)
- [Guia oficial de EDA](https://developers.google.com/meridian/docs/pre-modeling/perform-eda)
- [Implementação MeridianEDA](https://github.com/google/meridian/blob/02111531f8661373aa7b6ba31c316c67d72d1dd2/meridian/model/eda/meridian_eda.py)
- [Motor oficial: fórmulas e transformações](https://github.com/google/meridian/blob/02111531f8661373aa7b6ba31c316c67d72d1dd2/meridian/model/eda/eda_engine.py)
