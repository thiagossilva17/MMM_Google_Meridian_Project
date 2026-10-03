### Resultado observado e conclusão parcial

Exportamos Pearson e Spearman em quatro níveis: nacional, painel bruto, within-geo e residual two-way. Within remove a média de cada geo; two-way remove também a média semanal comum. Spearman de resíduos mede a ordenação dos resíduos e não é uma correlação parcial de postos.

O maior VIF within entre preditores é 2.11. A regressão auxiliar inclui intercepto e colunas padronizadas. Spend e impressões são diagnosticados em matrizes separadas; colocá-los juntos no VIF duplicaria sinais de custo praticamente fixo. Constantes são indefinidas e dependência linear perfeita gera infinito.

A maior associação absoluta within entre todas as variáveis comparadas é Channel1_impression × Channel1_spend (1.000); isso pode ser uma relação contábil entre gasto e mídia. Lags 0–8 são exploratórios, sem selecionar adstock. Não calculamos p-valores que presumiriam independência das 6,240 linhas: existe dependência temporal e geográfica.

Diferenças entre correlações nacionais e within podem resultar de composição populacional, tendência, sazonalidade e mídia alocada em antecipação à demanda. Correlação mídia–KPI não constitui efeito de mídia.

### O que ainda NÃO podemos concluir

As relações são descritivas. Não estimamos ROI, contribuição incremental ou efeitos causais.
Os dados são simulados: padrões não descrevem um mercado real e não validam, por si, a identificação de um MMM.

### CHECKPOINT

- **O que descobrimos?** As evidências numéricas acima e as tabelas exportadas respondem à pergunta deste capítulo.
- **Quais problemas apareceram?** Os limites e alertas estão descritos nos resultados; nenhuma observação foi excluída ou imputada.
- **O que falta investigar?** Checagens independentes da ferramenta oficial e comparação de definições.
- **Podemos avançar?** Podemos prosseguir com a investigação exploratória após revisar estes achados; isso não aprova automaticamente a modelagem.
