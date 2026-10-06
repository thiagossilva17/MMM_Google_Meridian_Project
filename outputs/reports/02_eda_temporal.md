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
