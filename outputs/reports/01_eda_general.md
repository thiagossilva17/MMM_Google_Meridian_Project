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
