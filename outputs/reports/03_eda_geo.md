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
