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
