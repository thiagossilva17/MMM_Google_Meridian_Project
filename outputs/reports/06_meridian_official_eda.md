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
