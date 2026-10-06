# Achados da EDA

1. **Estrutura.** O painel tem 40 geos × 156 semanas = 6240 observações, completude de 100.0% e 0 células ausentes. A chave geo–tempo foi validada.

2. **Tempo.** Todos os 5 canais pagos variam; a parcela within-geo da variância fica entre 61.0% e 94.7%. Channel2 é o canal com mais zeros: 64.3% das células, com 5.5% do gasto. A tabela de atividade e os gráficos distinguem semanas sem mídia de mudanças de intensidade. Movimentos de nível e sazonalidade são exploratórios.

3. **Geografia.** As médias por geo explicam de 5.3% a 39.0% da variância bruta da mídia paga. Rankings de volume dependem de população; mix e medidas por habitante oferecem lentes complementares.

4. **GEO × TEMPO.** Após retirar médias de geo e de semana, permanece de 42.9% a 77.9% da variância bruta de mídia paga; por habitante, de 64.8% a 79.3%. Esse componente é perdido ao observar apenas o agregado nacional. O painel contém variação potencialmente informativa, mas o resíduo pode conter ruído, endogeneidade e confundimento. Comparar com a decomposição per capita é essencial: diferenças multiplicativas de tamanho também podem gerar resíduos aditivos.

5. **Identificabilidade.** R², correlações, VIF e os alertas oficiais devem orientar hipóteses de especificação. Nenhuma dessas métricas prova identificação causal ou que um modelo geo terá melhor previsão que o nacional. Essa comparação exige futura modelagem com validação temporal comum, priors justificados e diagnósticos posteriores.

**Prontidão:** a integridade permite continuar o estudo metodológico, com a revisão dos seis alertas documentada e critérios por canal/controle em readiness_actions. As limitações da simulação permanecem. Não há recomendação de alocação de orçamento nesta EDA.

| Dimension               | Question                      | Evidence                | Finding                                                                     | Modeling_implication                                                                                |
|:------------------------|:------------------------------|:------------------------|:----------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------|
| integridade             | Painel completo?              | data_audit              | 6240 linhas, 40 geos, 156 semanas; completude 1.0                           | Contrato validado; preservar raw e schema.                                                          |
| missing                 | Há valores ausentes?          | missing_summary         | 0 células ausentes                                                          | Não imputar dados completos.                                                                        |
| outliers                | Há extremos descritivos?      | outliers                | 6039 pares observação/variável sinalizados por IQR ou MAD                   | Revisão por caso e grupo em outlier_case_review; manter dados simulados sem evidência de corrupção. |
| KPI variation           | Existe variação?              | within_between_variance | 1/1 variáveis com variância positiva; resíduo two-way entre 30.68% e 30.68% | Variação é necessária, não suficiente para identificar efeitos.                                     |
| media variation         | Existe variação?              | within_between_variance | 6/6 variáveis com variância positiva; resíduo two-way entre 42.90% e 77.94% | Variação é necessária, não suficiente para identificar efeitos.                                     |
| spend variation         | Existe variação?              | within_between_variance | 5/5 variáveis com variância positiva; resíduo two-way entre 42.90% e 77.94% | Variação é necessária, não suficiente para identificar efeitos.                                     |
| control collinearity    | Existe variação?              | within_between_variance | 2/2 variáveis com variância positiva; resíduo two-way entre 66.24% e 72.19% | Variação é necessária, não suficiente para identificar efeitos.                                     |
| temporal variation      | Quanto varia a mídia paga?    | geo_time_r2             | r2_time: 13.63% a 19.07%                                                    | Avaliar também escala por população e colinearidade conjunta.                                       |
| geo variation           | Quanto varia a mídia paga?    | geo_time_r2             | r2_geo: 5.35% a 38.99%                                                      | Avaliar também escala por população e colinearidade conjunta.                                       |
| within variation        | Quanto varia a mídia paga?    | geo_time_r2             | within_share: 61.01% a 94.65%                                               | Avaliar também escala por população e colinearidade conjunta.                                       |
| between variation       | Quanto varia a mídia paga?    | geo_time_r2             | between_share: 5.35% a 38.99%                                               | Avaliar também escala por população e colinearidade conjunta.                                       |
| geo-time variation      | Quanto varia a mídia paga?    | geo_time_r2             | residual_geo_time_share: 42.90% a 77.94%                                    | Avaliar também escala por população e colinearidade conjunta.                                       |
| R² geo                  | Quanto varia a mídia paga?    | geo_time_r2             | r2_geo: 5.35% a 38.99%                                                      | Avaliar também escala por população e colinearidade conjunta.                                       |
| R² time                 | Quanto varia a mídia paga?    | geo_time_r2             | r2_time: 13.63% a 19.07%                                                    | Avaliar também escala por população e colinearidade conjunta.                                       |
| population scaling      | A geografia é apenas tamanho? | geo_time_r2_per_capita  | Resíduo two-way por habitante: 64.85% a 86.11%                              | O ajuste por população muda a leitura; não substituir inputs brutos do Meridian.                    |
| media mix heterogeneity | O mix difere?                 | media_mix               | Amplitude máxima do share de um canal entre geos: 3.74 p.p.                 | Mix acumulado relativamente semelhante pode coexistir com execução semanal diferente.               |
| channel collinearity    | Os sinais são redundantes?    | vif_summary             | VIF máximo overall=2.48; within=2.11                                        | Não remover canais mecanicamente; diagnóstico não incorpora adstock/saturação.                      |
| data adequacy           | Guardrails oficiais?          | meridian_eda_checks     | 16 achados: {'INFO': 10, 'REVIEW': 6}; razão dados/parâmetros=30.59         | Checagens dependem da especificação provisória; revisar antes do ajuste.                            |

## Revisão após auditoria

**Prontidão revisada:** casos e alertas possuem decisão descritiva. Avançar ao desenho da especificação, mantendo os dados. DAG, controles, priors e validação temporal pertencem à próxima fase. Colab real continua pendente externa.

**Channel0:** zeros 12.1%; CV positivo 0.59; sequência zero 4; amplitude mix 3.30 p.p.; R² GEO bruto/per capita 0.248/0.006; resíduo per capita 0.783; VIF within 1.36; maior associação two-way sentiment_score_control (0.365). Risco: escala populacional e movimentos conjuntos não equivalem a efeito. Ação: verificar hipótese causal e colinearidade após transformações.

**Channel1:** zeros 27.9%; CV positivo 0.67; sequência zero 7; amplitude mix 3.74 p.p.; R² GEO bruto/per capita 0.144/0.004; resíduo per capita 0.765; VIF within 1.19; maior associação two-way sentiment_score_control (0.307). Risco: escala populacional e movimentos conjuntos não equivalem a efeito. Ação: verificar hipótese causal e colinearidade após transformações.

**Channel2:** zeros 64.3%; CV positivo 0.81; sequência zero 27; amplitude mix 2.42 p.p.; R² GEO bruto/per capita 0.053/0.004; resíduo per capita 0.793; VIF within 1.62; maior associação two-way Channel3_impression (0.451). Risco: suporte intermitente; janelas sem exposição. Ação: documentar suporte por janela de treino/holdout e incerteza do canal.

**Channel3:** zeros 2.7%; CV positivo 0.48; sequência zero 2; amplitude mix 3.36 p.p.; R² GEO bruto/per capita 0.390/0.005; resíduo per capita 0.648; VIF within 2.11; maior associação two-way Channel2_impression (0.451). Risco: escala populacional e movimentos conjuntos não equivalem a efeito. Ação: verificar hipótese causal e colinearidade após transformações.

**Channel4:** zeros 13.1%; CV positivo 0.60; sequência zero 4; amplitude mix 3.37 p.p.; R² GEO bruto/per capita 0.237/0.004; resíduo per capita 0.706; VIF within 1.65; maior associação two-way competitor_sales_control (0.478). Risco: escala populacional e movimentos conjuntos não equivalem a efeito. Ação: verificar hipótese causal e colinearidade após transformações.