### Resultado observado e conclusão parcial

1. **Estrutura.** O painel tem 40 geos × 156 semanas = 6240 observações, completude de 100.0% e 0 células ausentes. A chave geo–tempo foi validada.

2. **Tempo.** Todos os 5 canais pagos variam; a parcela within-geo da variância fica entre 61.0% e 94.7%. Channel2 é o canal com mais zeros: 64.3% das células, com 5.5% do gasto. A tabela de atividade e os gráficos distinguem semanas sem mídia de mudanças de intensidade. Movimentos de nível e sazonalidade são exploratórios.

3. **Geografia.** As médias por geo explicam de 5.3% a 39.0% da variância bruta da mídia paga. Rankings de volume dependem de população; mix e medidas por habitante oferecem lentes complementares.

4. **GEO × TEMPO.** Após retirar médias de geo e de semana, permanece de 42.9% a 77.9% da variância bruta de mídia paga; por habitante, de 64.8% a 79.3%. Esse componente é perdido ao observar apenas o agregado nacional. O painel contém variação potencialmente informativa, mas o resíduo pode conter ruído, endogeneidade e confundimento. Comparar com a decomposição per capita é essencial: diferenças multiplicativas de tamanho também podem gerar resíduos aditivos.

5. **Identificabilidade.** R², correlações, VIF e os alertas oficiais devem orientar hipóteses de especificação. Nenhuma dessas métricas prova identificação causal ou que um modelo geo terá melhor previsão que o nacional. Essa comparação exige futura modelagem com validação temporal comum, priors justificados e diagnósticos posteriores.

**Prontidão:** a integridade permite continuar o estudo metodológico, com a revisão dos seis alertas documentada e critérios por canal/controle em readiness_actions. As limitações da simulação permanecem. Não há recomendação de alocação de orçamento nesta EDA.

**Prontidão revisada:** casos e alertas possuem decisão descritiva. Avançar ao desenho da especificação, mantendo os dados. DAG, controles, priors e validação temporal pertencem à próxima fase. Colab real continua pendente externa.

**Channel0:** zeros 12.1%; CV positivo 0.59; sequência zero 4; amplitude mix 3.30 p.p.; R² GEO bruto/per capita 0.248/0.006; resíduo per capita 0.783; VIF within 1.36; maior associação two-way sentiment_score_control (0.365). Risco: escala populacional e movimentos conjuntos não equivalem a efeito. Ação: verificar hipótese causal e colinearidade após transformações.

**Channel1:** zeros 27.9%; CV positivo 0.67; sequência zero 7; amplitude mix 3.74 p.p.; R² GEO bruto/per capita 0.144/0.004; resíduo per capita 0.765; VIF within 1.19; maior associação two-way sentiment_score_control (0.307). Risco: escala populacional e movimentos conjuntos não equivalem a efeito. Ação: verificar hipótese causal e colinearidade após transformações.

**Channel2:** zeros 64.3%; CV positivo 0.81; sequência zero 27; amplitude mix 2.42 p.p.; R² GEO bruto/per capita 0.053/0.004; resíduo per capita 0.793; VIF within 1.62; maior associação two-way Channel3_impression (0.451). Risco: suporte intermitente; janelas sem exposição. Ação: documentar suporte por janela de treino/holdout e incerteza do canal.

**Channel3:** zeros 2.7%; CV positivo 0.48; sequência zero 2; amplitude mix 3.36 p.p.; R² GEO bruto/per capita 0.390/0.005; resíduo per capita 0.648; VIF within 2.11; maior associação two-way Channel2_impression (0.451). Risco: escala populacional e movimentos conjuntos não equivalem a efeito. Ação: verificar hipótese causal e colinearidade após transformações.

**Channel4:** zeros 13.1%; CV positivo 0.60; sequência zero 4; amplitude mix 3.37 p.p.; R² GEO bruto/per capita 0.237/0.004; resíduo per capita 0.706; VIF within 1.65; maior associação two-way competitor_sales_control (0.478). Risco: escala populacional e movimentos conjuntos não equivalem a efeito. Ação: verificar hipótese causal e colinearidade após transformações.

### O que ainda NÃO podemos concluir

As relações são descritivas. Não estimamos ROI, contribuição incremental ou efeitos causais.
Os dados são simulados: padrões não descrevem um mercado real e não validam, por si, a identificação de um MMM.

### CHECKPOINT

- **O que descobrimos?** **Prontidão revisada:** casos e alertas possuem decisão descritiva. Avançar ao desenho da especificação, mantendo os dados. DAG, controles, priors e validação temporal pertencem à próxima fase. Colab real continua pendente externa.
- **Quais problemas apareceram?** Colab real não comprovado; EDA não demonstra identificação causal ou superioridade preditiva.
- **O que falta investigar?** Desenho causal, especificação, priors, holdout temporal e posterior em fase futura.
- **Podemos avançar?** Podemos prosseguir com a investigação exploratória após revisar estes achados; isso não aprova automaticamente a modelagem.
