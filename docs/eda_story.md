# Da auditoria à prontidão para MMM

### Resultado observado e conclusão parcial

Recebemos 6,240 registros, 40 geos e 156 semanas, de 2021-01-25 a 2024-01-15. A grade é semanal, completa e sem duplicatas, nulos ou violações de domínio verificadas. População é constante dentro de cada geo.

O CSV original tem uma coluna de índice exportado, validada como 0…N−1 e removida apenas da cópia processada. Conversões são valores contínuos simulados; controles podem ser negativos na escala fornecida. Há 5 canais pagos, uma mídia orgânica e Promo. Não há reach/frequency; nenhuma variável desse tipo foi inventada.

CPMU = gasto/impressões. 7496 razões são indefinidas por ausência de impressões e permanecem NaN. Conferir os contadores de inconsistências na auditoria. Isso distingue zero atividade de custo zero.

**Decisão de estrutura:** chave, grade, domínios e população validados. CPMU indefinido em zero atividade permanece NaN. Coordenadas e pares mídia/gasto estão explícitos no dicionário.

### O que ainda NÃO podemos concluir

As relações são descritivas. Não estimamos ROI, contribuição incremental ou efeitos causais.
Os dados são simulados: padrões não descrevem um mercado real e não validam, por si, a identificação de um MMM.

### CHECKPOINT

- **O que descobrimos?** **Decisão de estrutura:** chave, grade, domínios e população validados. CPMU indefinido em zero atividade permanece NaN. Coordenadas e pares mídia/gasto estão explícitos no dicionário.
- **Quais problemas apareceram?** Integridade estrutural não certifica plausibilidade dos extremos; investigar nos capítulos 01 e 06.
- **O que falta investigar?** Distribuições, concentração de investimento, zeros e extremos.
- **Podemos avançar?** Podemos prosseguir com a investigação exploratória após revisar estes achados; isso não aprova automaticamente a modelagem.


### Resultado observado e conclusão parcial

O KPI nacional tem média semanal de 422,632,783 conversões sintéticas e CV de 6.9%. O agregado nacional soma conversões entre geos; não soma taxas.

O maior share de gasto é de Channel3 (40.0%). Share mede alocação, não retorno. A atividade varia de 35.7% a 97.3% das células GEO × semana. Exportamos todas as sequências de atividade e zeros, sem classificar com limiares arbitrários.

Foram sinalizados 6039 pares observação/variável por IQR (1,5×) ou MAD (|z modificado|>3,5). São regras de triagem, não critérios de remoção. Séries esparsas e geos grandes podem ser sinalizados legitimamente. Quando MAD é zero o escore fica indefinido. Nenhum extremo foi removido.

**Channel2 versus Channel3:** atividade por geo entre 28.2% e 44.2%; maior sequência de zeros 27 semanas. Channel3 tem sequência ativa máxima de 127 semanas. Zeros nacionais de Channel2: 2021-04-26, 2022-07-25, 2023-05-15, 2023-06-19.

**Atividade e intensidade:** Var(X)=p Var(X|X>0)+p(1−p)E(X|X>0)². A alternância zero/positivo corresponde a 50.5% da variância within em Channel2, contra 10.5% em Channel3. CV mediano de Channel2: 1.88 geral e 0.81 entre valores positivos. Essa identidade não decompõe o resíduo two-way nem estima eficácia.

**Extremos:** 6039 pares triados; até três casos por variável com comparação bruto/per capita/dentro do geo e janelas de ±2 semanas. Promo é contínuo com massa em zero, não binário. Os grupos e as justificativas estão nas tabelas; dados simulados são preservados, sem validação comercial presumida.

### O que ainda NÃO podemos concluir

As relações são descritivas. Não estimamos ROI, contribuição incremental ou efeitos causais.
Os dados são simulados: padrões não descrevem um mercado real e não validam, por si, a identificação de um MMM.

### CHECKPOINT

- **O que descobrimos?** **Channel2 versus Channel3:** atividade por geo entre 28.2% e 44.2%; maior sequência de zeros 27 semanas. Channel3 tem sequência ativa máxima de 127 semanas. Zeros nacionais de Channel2: 2021-04-26, 2022-07-25, 2023-05-15, 2023-06-19.
- **Quais problemas apareceram?** Sparsity limita suporte em janelas específicas; não inventar calendário de campanhas.
- **O que falta investigar?** Dinâmica temporal dos sinais e seus controles.
- **Podemos avançar?** Podemos prosseguir com a investigação exploratória após revisar estes achados; isso não aprova automaticamente a modelagem.


### Resultado observado e conclusão parcial

O máximo nacional ocorre em 2023-05-15 (491,287,369) e o mínimo em 2022-09-19 (340,283,293). A média móvel de 13 semanas suaviza a série sem antecipar valores futuros; é apenas visual.

A decomposição STL usa período 52 como aproximação anual para dados semanais. Há apenas 3.0 ciclos: tendência, sazonalidade e mudanças de nível não são evidência confirmatória de mecanismos de negócio. Nenhum teste formal de quebra foi feito. As maiores mudanças e a ACF foram exportadas.

Todos os canais têm gráficos separados de impressões, gasto, CPMU e comparação padronizada com KPI. Controles e Promo são agregados por média ponderada por população porque somar índices sintéticos não tem interpretação. A mídia orgânica é somada. Existem 0 variáveis constantes entre os controles/tratamentos apresentados. Valores próximos de constantes devem ser avaliados na sua escala, sem corte universal.

**Trajetória:** tendência STL de 413,074,059 a 429,184,890 (+3.90%). Maior mudança semanal em 2023-03-06: -101,396,624. ACF nos lags 1/13/52: 0.008/0.090/0.032. Forças descritivas sazonal/tendência: 0.503/0.034, calculadas por 1−Var(resíduo)/Var(componente+resíduo), truncadas em zero; não são parcelas aditivas ou testes.

competitor_sales_control: amplitude [-4.826,3.925], desvio 1.210, 6240 valores distintos; maior mudança nacional ponderada em 2022-05-16 (-2.382). Não é quase constante na escala observada; CV não é interpretável.

sentiment_score_control: amplitude [-4.230,4.320], desvio 1.175, 6239 valores distintos; maior mudança nacional ponderada em 2021-12-13 (+2.357). Não é quase constante na escala observada; CV não é interpretável.

Promo: amplitude [0.000,4.801], desvio 0.694, 3319 valores distintos; maior mudança nacional ponderada em 2023-08-21 (-1.133). Não é quase constante na escala observada; CV não é interpretável.

### O que ainda NÃO podemos concluir

As relações são descritivas. Não estimamos ROI, contribuição incremental ou efeitos causais.
Os dados são simulados: padrões não descrevem um mercado real e não validam, por si, a identificação de um MMM.

### CHECKPOINT

- **O que descobrimos?** **Trajetória:** tendência STL de 413,074,059 a 429,184,890 (+3.90%). Maior mudança semanal em 2023-03-06: -101,396,624. ACF nos lags 1/13/52: 0.008/0.090/0.032. Forças descritivas sazonal/tendência: 0.503/0.034, calculadas por 1−Var(resíduo)/Var(componente+resíduo), truncadas em zero; não são parcelas aditivas ou testes.
- **Quais problemas apareceram?** Somente três ciclos; STL/ACF não confirmam sazonalidade de negócio nem quebras causais.
- **O que falta investigar?** Heterogeneidade entre geos e decomposição within/between.
- **Podemos avançar?** Podemos prosseguir com a investigação exploratória após revisar estes achados; isso não aprova automaticamente a modelagem.


### Resultado observado e conclusão parcial

O maior geo responde por 5.0% do KPI acumulado; os cinco maiores por 22.9%. A correlação populacional com KPI total é 0.978 (Spearman). A escala populacional precisa ser considerada antes de interpretar rankings.

O KPI tem 67.9% da variância between-geo e 32.1% within-geo. A identidade usa momentos populacionais (ddof=0), com peso igual por observação. R²_geo equivale à parcela between; R²_time quantifica semanas comuns. No painel balanceado, a parcela residual two-way do KPI é 30.7%; por habitante é 86.1%.

Within não significa automaticamente sinal geográfico novo: inclui choques temporais nacionais. Por isso apresentamos também o resíduo após remover simultaneamente geo e tempo. Essa decomposição é descritiva e depende da escala. Os small multiples usam geos escolhidos por critérios registrados; os cálculos e heatmaps incluem todos os geos. Geo0…Geo39 são rótulos sintéticos, sem fronteiras para um mapa geográfico real.

**Sincronização:** 780 pares, mediana 0.0280, mínimo -0.2151 (Geo32 × Geo24), máximo 0.2804 (Geo14 × Geo22). Baixa sincronização linear não demonstra independência. Small multiples cobrem extremos de volume/CV e usam escalas Y próprias.

### O que ainda NÃO podemos concluir

As relações são descritivas. Não estimamos ROI, contribuição incremental ou efeitos causais.
Os dados são simulados: padrões não descrevem um mercado real e não validam, por si, a identificação de um MMM.

### CHECKPOINT

- **O que descobrimos?** **Sincronização:** 780 pares, mediana 0.0280, mínimo -0.2151 (Geo32 × Geo24), máximo 0.2804 (Geo14 × Geo22). Baixa sincronização linear não demonstra independência. Small multiples cobrem extremos de volume/CV e usam escalas Y próprias.
- **Quais problemas apareceram?** Geos fictícios não permitem inventar contextos territoriais.
- **O que falta investigar?** Mix, alocação territorial, concentração e variação de cada canal dentro dos geos.
- **Podemos avançar?** Podemos prosseguir com a investigação exploratória após revisar estes achados; isso não aprova automaticamente a modelagem.


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


### Resultado observado e conclusão parcial

Exportamos Pearson e Spearman em quatro níveis: nacional, painel bruto, within-geo e residual two-way. Within remove a média de cada geo; two-way remove também a média semanal comum. Spearman de resíduos mede a ordenação dos resíduos e não é uma correlação parcial de postos.

O maior VIF within entre preditores é 2.11. A regressão auxiliar inclui intercepto e colunas padronizadas. Spend e impressões são diagnosticados em matrizes separadas; colocá-los juntos no VIF duplicaria sinais de custo praticamente fixo. Constantes são indefinidas e dependência linear perfeita gera infinito.

A maior associação absoluta within entre preditores distintos é Channel4_impression × competitor_sales_control (0.550); o ranking exclui pares gasto–impressões do mesmo canal. Lags 0–8 são exploratórios, sem selecionar adstock. Não calculamos p-valores que presumiriam independência das 6,240 linhas: existe dependência temporal e geográfica.

Diferenças entre correlações nacionais e within podem resultar de composição populacional, tendência, sazonalidade e mídia alocada em antecipação à demanda. Correlação mídia–KPI não constitui efeito de mídia.

**Channel2 × Channel3:** nacional 0.7003, within 0.5035, two-way 0.4511. Parte do movimento conjunto acompanha composição/tempo comum, mas há associação residual. O ranking exclui gasto–impressões do mesmo canal.

competitor_sales_control: R² tempo 0.332; VIF within 1.83; maior associação two-way com Channel4_impression (+0.478). Justificar papel pré-tratamento/confundidor no DAG; associação não autoriza inclusão causal.

sentiment_score_control: R² tempo 0.274; VIF within 1.88; maior associação two-way com Organic_channel0_impression (+0.437). Justificar papel pré-tratamento/confundidor no DAG; associação não autoriza inclusão causal.

Promo: R² tempo 0.198; VIF within 1.28; maior associação two-way com Channel0_impression (+0.297). Justificar papel pré-tratamento/confundidor no DAG; associação não autoriza inclusão causal.

### O que ainda NÃO podemos concluir

As relações são descritivas. Não estimamos ROI, contribuição incremental ou efeitos causais.
Os dados são simulados: padrões não descrevem um mercado real e não validam, por si, a identificação de um MMM.

### CHECKPOINT

- **O que descobrimos?** **Channel2 × Channel3:** nacional 0.7003, within 0.5035, two-way 0.4511. Parte do movimento conjunto acompanha composição/tempo comum, mas há associação residual. O ranking exclui gasto–impressões do mesmo canal.
- **Quais problemas apareceram?** VIF moderado não resolve confundimento nem colinearidade após adstock/saturação.
- **O que falta investigar?** Checagens independentes da ferramenta oficial e comparação de definições.
- **Podemos avançar?** Podemos prosseguir com a investigação exploratória após revisar estes achados; isso não aprova automaticamente a modelagem.


### Resultado observado e conclusão parcial

O relatório HTML oficial foi executado com Meridian 2.1.0, sem amostragem posterior. Os checks exportaram 16 achados: {'INFO': 10, 'REVIEW': 6}. As advertências de execução estão em meridian_warnings.csv; não foram silenciadas nem resolvidas por alteração de thresholds.

A API atual usa DataFrameInputDataBuilder. MeridianEDA gera amostras da prior no construtor para completar diagnósticos da especificação. Isso não ajusta o modelo aos dados e não produz estimativas posteriores. A especificação default é provisória: 156 knots e 8 lags. Não escolhemos hiperparâmetros finais com esta EDA.

A razão oficial é 6240/(40−1+156+2+7) = 30.59. Essa contagem é um guardrail que não conta todos os efeitos geo como parâmetros independentes. Não é prova de tamanho amostral efetivo ou de suficiência.

Os alertas de CPMU precisam de contexto: o CV máximo do custo unitário é 3.475e-08. A variação relativa minúscula é compatível com arredondamento na geração/exportação, e não evidencia dispersão econômica de custos. Não alteramos o dado ou o threshold IQR oficial para eliminar o alerta.

Uma diferença metodológica importante: os R² oficiais são ajustados e usam dados transformados; a EDA própria mostra R² brutos e por habitante não ajustados. Recalculando por soma de quadrados na mesma escala oficial, a concordância dentro de 1e-5 foi **True**. A tabela official_r2_reconciliation contém as diferenças por variável. VIF e correlações também dependem da população e agregação. Artefatos numéricos foram exportados para investigar essas diferenças.

**Revisão localizada:** 6 REVIEW têm localizações, magnitude, decisão e limite residual documentados. A severidade oficial permanece REVIEW. Correlação/VIF são reconciliados na mesma escala; IQR compara todas as chaves geo–variável–semana. CPMU tem casos nos arquivos official_cpmu_cases_geo/national. Controles/Promo nacionais oficiais usam soma por default; a EDA própria pondera por população, explicando diferenças entre escalas.

### O que ainda NÃO podemos concluir

As relações são descritivas. Não estimamos ROI, contribuição incremental ou efeitos causais.
Os dados são simulados: padrões não descrevem um mercado real e não validam, por si, a identificação de um MMM.

### CHECKPOINT

- **O que descobrimos?** **Revisão localizada:** 6 REVIEW têm localizações, magnitude, decisão e limite residual documentados. A severidade oficial permanece REVIEW. Correlação/VIF são reconciliados na mesma escala; IQR compara todas as chaves geo–variável–semana. CPMU tem casos nos arquivos official_cpmu_cases_geo/national. Controles/Promo nacionais oficiais usam soma por default; a EDA própria pondera por população, explicando diferenças entre escalas.
- **Quais problemas apareceram?** Guardrails oficiais extremos não são certificados de qualidade. Preservação no exemplo não certifica plausibilidade econômica.
- **O que falta investigar?** Consolidar os achados, implicações e limites de prontidão.
- **Podemos avançar?** Podemos prosseguir com a investigação exploratória após revisar estes achados; isso não aprova automaticamente a modelagem.


1. **Estrutura.** O painel tem 40 geos × 156 semanas = 6240 observações, completude de 100.0% e 0 células ausentes. A chave geo–tempo foi validada.

2. **Tempo.** Todos os 5 canais pagos variam; a parcela within-geo da variância fica entre 61.0% e 94.7%. Channel2 é o canal com mais zeros: 64.3% das células, com 5.5% do gasto. A tabela de atividade e os gráficos distinguem semanas sem mídia de mudanças de intensidade. Movimentos de nível e sazonalidade são exploratórios.

3. **Geografia.** As médias por geo explicam de 5.3% a 39.0% da variância bruta da mídia paga. Rankings de volume dependem de população; mix e medidas por habitante oferecem lentes complementares.

4. **GEO × TEMPO.** Após retirar médias de geo e de semana, permanece de 42.9% a 77.9% da variância bruta de mídia paga; por habitante, de 64.8% a 79.3%. Esse componente é perdido ao observar apenas o agregado nacional. O painel contém variação potencialmente informativa, mas o resíduo pode conter ruído, endogeneidade e confundimento. Comparar com a decomposição per capita é essencial: diferenças multiplicativas de tamanho também podem gerar resíduos aditivos.

5. **Identificabilidade.** R², correlações, VIF e os alertas oficiais devem orientar hipóteses de especificação. Nenhuma dessas métricas prova identificação causal ou que um modelo geo terá melhor previsão que o nacional. Essa comparação exige futura modelagem com validação temporal comum, priors justificados e diagnósticos posteriores.

**Prontidão:** a integridade permite continuar o estudo metodológico, com a revisão dos seis alertas documentada e critérios por canal/controle em readiness_actions. As limitações da simulação permanecem. Não há recomendação de alocação de orçamento nesta EDA.

## Revisão após auditoria

**Prontidão revisada:** casos e alertas possuem decisão descritiva. Avançar ao desenho da especificação, mantendo os dados. DAG, controles, priors e validação temporal pertencem à próxima fase. Colab real continua pendente externa.

**Channel0:** zeros 12.1%; CV positivo 0.59; sequência zero 4; amplitude mix 3.30 p.p.; R² GEO bruto/per capita 0.248/0.006; resíduo per capita 0.783; VIF within 1.36; maior associação two-way sentiment_score_control (0.365). Risco: escala populacional e movimentos conjuntos não equivalem a efeito. Ação: verificar hipótese causal e colinearidade após transformações.

**Channel1:** zeros 27.9%; CV positivo 0.67; sequência zero 7; amplitude mix 3.74 p.p.; R² GEO bruto/per capita 0.144/0.004; resíduo per capita 0.765; VIF within 1.19; maior associação two-way sentiment_score_control (0.307). Risco: escala populacional e movimentos conjuntos não equivalem a efeito. Ação: verificar hipótese causal e colinearidade após transformações.

**Channel2:** zeros 64.3%; CV positivo 0.81; sequência zero 27; amplitude mix 2.42 p.p.; R² GEO bruto/per capita 0.053/0.004; resíduo per capita 0.793; VIF within 1.62; maior associação two-way Channel3_impression (0.451). Risco: suporte intermitente; janelas sem exposição. Ação: documentar suporte por janela de treino/holdout e incerteza do canal.

**Channel3:** zeros 2.7%; CV positivo 0.48; sequência zero 2; amplitude mix 3.36 p.p.; R² GEO bruto/per capita 0.390/0.005; resíduo per capita 0.648; VIF within 2.11; maior associação two-way Channel2_impression (0.451). Risco: escala populacional e movimentos conjuntos não equivalem a efeito. Ação: verificar hipótese causal e colinearidade após transformações.

**Channel4:** zeros 13.1%; CV positivo 0.60; sequência zero 4; amplitude mix 3.37 p.p.; R² GEO bruto/per capita 0.237/0.004; resíduo per capita 0.706; VIF within 1.65; maior associação two-way competitor_sales_control (0.478). Risco: escala populacional e movimentos conjuntos não equivalem a efeito. Ação: verificar hipótese causal e colinearidade após transformações.