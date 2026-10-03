### Resultado observado e conclusão parcial

1. **Estrutura.** O painel tem 40 geos × 156 semanas = 6240 observações, completude de 100.0% e 0 células ausentes. A chave geo–tempo foi validada.

2. **Tempo.** Todos os 5 canais pagos variam; a parcela within-geo da variância fica entre 61.0% e 94.7%. Channel2 é o canal com mais zeros: 64.3% das células, com 5.5% do gasto. A tabela de atividade e os gráficos distinguem semanas sem mídia de mudanças de intensidade. Movimentos de nível e sazonalidade são exploratórios.

3. **Geografia.** As médias por geo explicam de 5.3% a 39.0% da variância bruta da mídia paga. Rankings de volume dependem de população; mix e medidas por habitante oferecem lentes complementares.

4. **GEO × TEMPO.** Após retirar médias de geo e de semana, permanece de 42.9% a 77.9% da variância bruta de mídia paga; por habitante, de 64.8% a 79.3%. Esse componente é perdido ao observar apenas o agregado nacional. O painel contém variação potencialmente informativa, mas o resíduo pode conter ruído, endogeneidade e confundimento. Comparar com a decomposição per capita é essencial: diferenças multiplicativas de tamanho também podem gerar resíduos aditivos.

5. **Identificabilidade.** R², correlações, VIF e os alertas oficiais devem orientar hipóteses de especificação. Nenhuma dessas métricas prova identificação causal ou que um modelo geo terá melhor previsão que o nacional. Essa comparação exige futura modelagem com validação temporal comum, priors justificados e diagnósticos posteriores.

**Prontidão:** a integridade permite continuar o estudo metodológico, condicionando a próxima fase à revisão dos alertas oficiais e das limitações dos dados simulados. Não há recomendação de alocação de orçamento nesta EDA.

### O que ainda NÃO podemos concluir

As relações são descritivas. Não estimamos ROI, contribuição incremental ou efeitos causais.
Os dados são simulados: padrões não descrevem um mercado real e não validam, por si, a identificação de um MMM.

### CHECKPOINT

- **O que descobrimos?** As evidências numéricas acima e as tabelas exportadas respondem à pergunta deste capítulo.
- **Quais problemas apareceram?** Os limites e alertas estão descritos nos resultados; nenhuma observação foi excluída ou imputada.
- **O que falta investigar?** Desenho causal, especificação, priors, holdout temporal e posterior em fase futura.
- **Podemos avançar?** Podemos prosseguir com a investigação exploratória após revisar estes achados; isso não aprova automaticamente a modelagem.
