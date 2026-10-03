# ESPECIFICAÇÃO DE EXECUÇÃO — EDA COMPLETA DO TCC DE MARKETING MIX MODELING COM GOOGLE MERIDIAN

## 1. PAPEL E CONTEXTO

Atue simultaneamente como:

- Cientista de Dados Sênior;
- Estatístico aplicado a Marketing Science;
- especialista em Marketing Mix Modeling;
- engenheiro de dados/Python;
- pesquisador acadêmico;
- desenvolvedor responsável pela organização do repositório GitHub;
- redator técnico capaz de explicar análises estatísticas de maneira didática.

O projeto é um Trabalho de Conclusão de Curso sobre **Marketing Mix Modeling utilizando Google Meridian**, com ênfase especial no diferencial de utilizar dados em nível geográfico (`geo-level`) em vez de trabalhar apenas com séries nacionais agregadas.

O autor possui formação quantitativa, mas está realizando seu primeiro projeto prático completo de MMM com Meridian. Portanto, o código NÃO deve ser apenas funcional. Ele deve formar uma narrativa estatística completa e didática.

Esta primeira grande fase do projeto é exclusivamente:

> **Compreensão dos dados + auditoria + análise exploratória + investigação profunda da dimensão geográfica e geo-temporal.**

NÃO realizar ainda:

- estimação posterior do MMM;
- MCMC/NUTS;
- inferência de ROI;
- mROI;
- contribuição incremental;
- curvas de resposta;
- otimização de orçamento;
- comparação de efeitos causais de canais.

Essas etapas virão posteriormente.

Nesta fase queremos determinar se os dados possuem estrutura, qualidade e variação suficientes para justificar e sustentar um modelo MMM hierárquico geo-level.

---

# 2. PRINCÍPIO CIENTÍFICO CENTRAL

Toda a EDA deve ser construída para responder quatro perguntas principais:

1. Os dados estão estruturalmente corretos e completos?
2. Existe variação temporal suficiente?
3. Existe variação geográfica suficiente?
4. Existe variação simultânea `GEO × TEMPO × MÍDIA` suficiente para justificar a utilização da estrutura geo-level do Meridian?

A quarta pergunta deve receber atenção especial.

O projeto não deve assumir que a simples existência de uma coluna `geo` torna os dados geograficamente informativos.

É necessário demonstrar empiricamente:

- variação entre geos;
- variação dentro de cada geo ao longo do tempo;
- diferenças no mix de mídia;
- diferenças na alocação territorial dos canais;
- diferenças temporais de execução;
- relação entre escala populacional e mídia/KPI;
- existência ou ausência de colinearidade com efeitos fixos de geo;
- existência ou ausência de colinearidade com efeitos temporais.

A EDA deverá preparar a resposta para:

> **A base contém informação geo-temporal adicional útil para identificação estatística do MMM, além da informação temporal que estaria disponível em um modelo nacional?**

Não force uma resposta positiva. A conclusão deve ser determinada pelos dados.

---

# 3. FONTES E DOCUMENTAÇÃO

Antes de escrever o código:

1. consulte a documentação oficial atual do Google Meridian;
2. consulte o repositório oficial atual do Google Meridian;
3. identifique a base de exemplo geo-level oficial disponibilizada pelo Google;
4. identifique o schema real dessa base;
5. identifique a versão atual da API Meridian utilizada;
6. verifique a API atual do pacote de EDA do Meridian;
7. verifique especialmente a implementação atual de `MeridianEDA`;
8. registre as versões utilizadas.

NÃO:

- invente nomes de colunas;
- invente canais;
- suponha dimensões sem verificar;
- utilize APIs antigas apenas porque aparecem em notebooks antigos;
- copie código depreciado sem validar na documentação atual.

Sempre prefira a documentação oficial e o código oficial do Google Meridian.

Se houver divergência entre exemplos antigos e API atual, utilize a API atual e documente a diferença.

---

# 4. REGRA DE REPRODUTIBILIDADE

Todo resultado deve poder ser reproduzido.

Registrar:

- versão do Python;
- versão do Meridian;
- pandas;
- numpy;
- scipy;
- matplotlib;
- plotly, se utilizado;
- statsmodels, se utilizado;
- demais bibliotecas relevantes;
- fonte exata dos dados;
- data de acesso;
- commit/hash do repositório oficial quando possível;
- dimensões da base;
- checksum do arquivo bruto quando possível.

Utilizar seeds fixas quando alguma operação aleatória for necessária.

Não modificar dados da pasta `raw`.

Qualquer transformação deve gerar um novo artefato em `processed`.

---

# 5. COMPATIBILIDADE COM GOOGLE COLAB

Todo o projeto será desenvolvido e versionado no GitHub, mas posteriormente executado no Google Colab.

Portanto:

## Requisito obrigatório

Todo notebook deverá ser executável em Google Colab do início ao fim.

Criar células iniciais capazes de:

1. identificar se o ambiente é Colab;
2. instalar dependências necessárias;
3. importar bibliotecas;
4. configurar paths;
5. obter os dados;
6. criar diretórios de outputs caso não existam.

Não depender de:

- caminhos absolutos da máquina local;
- configurações pessoais;
- credenciais privadas;
- ambientes Conda locais;
- arquivos fora do repositório.

Use `pathlib.Path`.

O código deverá funcionar tanto:

```text
GitHub repository → execução local
```

quanto:

```text
GitHub → Google Colab
```

Criar também:

```text
requirements.txt
```

e, caso faça sentido:

```text
requirements-colab.txt
```

Não fixe versões arbitrariamente. Fixe ou delimite versões apenas quando necessário para compatibilidade e registre a justificativa.

---

# 6. ESTRUTURA DO REPOSITÓRIO

Organizar o projeto desta forma:

```text
tcc-meridian/
│
├── README.md
│
├── requirements.txt
├── requirements-colab.txt
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── metadata/
│
├── notebooks/
│   ├── 00_data_audit.ipynb
│   ├── 01_eda_general.ipynb
│   ├── 02_eda_temporal.ipynb
│   ├── 03_eda_geo.ipynb
│   ├── 04_eda_media_geo.ipynb
│   ├── 05_eda_relationships.ipynb
│   ├── 06_meridian_official_eda.ipynb
│   └── 07_eda_conclusions.ipynb
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data.py
│   ├── validation.py
│   ├── eda.py
│   ├── geo_analysis.py
│   ├── statistics.py
│   ├── plots.py
│   └── reporting.py
│
├── outputs/
│   ├── figures/
│   │   ├── data_audit/
│   │   ├── general/
│   │   ├── temporal/
│   │   ├── geo/
│   │   ├── media_geo/
│   │   └── relationships/
│   │
│   ├── tables/
│   ├── reports/
│   └── logs/
│
├── docs/
│   ├── data_dictionary.md
│   ├── methodology_eda.md
│   ├── decisions.md
│   ├── eda_story.md
│   └── findings.md
│
└── tests/
    └── test_data_contract.py
```

Se o repositório já possuir uma estrutura parcialmente semelhante, preserve o que for útil e adapte sem destruir trabalho existente.

---

# 7. PRINCÍPIO DE ORGANIZAÇÃO DO CÓDIGO

Os notebooks devem priorizar:

- leitura;
- narrativa;
- interpretação;
- gráficos;
- resultados.

Funções reutilizáveis devem ficar em `src/`.

Evitar notebooks contendo centenas de linhas repetidas.

Exemplo:

```python
from src.geo_analysis import variance_decomposition
from src.plots import plot_geo_time_heatmap
```

é preferível a repetir toda a implementação em múltiplos notebooks.

Entretanto, os notebooks devem continuar suficientemente transparentes para que um estudante consiga entender o que está acontecendo.

Evite abstrações desnecessariamente complexas.

---

# 8. STORYTELLING OBRIGATÓRIO

Cada notebook deve funcionar como um capítulo sequencial de uma investigação.

Antes de cada conjunto importante de códigos, incluir uma célula Markdown explicando:

### Pergunta

O que queremos descobrir?

### Motivação

Por que isso importa para MMM?

### Método

O que será calculado?

### Interpretação

Como devemos interpretar possíveis resultados?

Depois da execução, incluir uma seção:

### Resultado observado

Apresentar os números realmente encontrados.

Depois:

### Conclusão parcial

Explicar o que aquele resultado sugere.

Depois:

### O que ainda NÃO podemos concluir

Evitar extrapolações indevidas.

Exemplo:

Não escrever:

> TV aumentou o KPI.

quando a análise realizada foi apenas correlação.

Escrever:

> TV e KPI apresentam associação temporal positiva neste conjunto de dados. A EDA não permite interpretar essa relação como efeito causal.

Sempre separar:

```text
descrição
≠
associação
≠
predição
≠
causalidade
```

---

# 9. CONCLUSÕES DINÂMICAS NOS NOTEBOOKS

Sempre que possível, gerar textos interpretativos utilizando os próprios resultados calculados.

Exemplo:

```python
from IPython.display import display, Markdown

display(Markdown(f"""
### Resultado observado

A base contém **{n_geos} geos**, **{n_periods} períodos** e
**{n_rows:,} observações geo-temporais**.

A completude do painel é de **{panel_completeness:.2%}**.
"""))
```

Não preencher conclusões com valores inventados.

---

# 10. NOTEBOOK 00 — DATA AUDIT

Objetivo:

> compreender exatamente o dataset antes de qualquer análise estatística.

---

## 10.1 Aquisição dos dados

Localizar a base oficial geo-level do Meridian.

Implementar download reproduzível.

Armazenar cópia original em:

```text
data/raw/
```

Registrar em:

```text
data/metadata/
```

informações sobre:

- origem;
- nome;
- versão;
- URL de origem, se aplicável;
- data de aquisição;
- hash/checksum;
- dimensões originais.

Se a base já estiver presente no repositório, verificar sua origem antes de baixar outra versão.

---

# 11. DESCOBRIR O SCHEMA REAL

Identificar automaticamente:

- variável temporal;
- geo;
- KPI;
- population;
- media;
- spend;
- reach;
- frequency;
- controles;
- organic media, se presente;
- non-media treatments, se presentes;
- revenue_per_kpi, se presente;
- demais campos.

Não assumir nomes.

Construir um **data dictionary**.

Gerar:

```text
docs/data_dictionary.md
```

e:

```text
outputs/tables/data_dictionary.csv
```

Com colunas como:

| variable | role | dtype | dimension | missing | zeros | min | max | mean | std |
|---|---|---|---|---|---|---|---|---|---|

---

# 12. DIMENSÕES DO DATASET

Calcular:

- número de registros;
- número de geos;
- número de períodos;
- frequência temporal;
- primeira data;
- última data;
- número de canais;
- número de controles;
- observações esperadas;
- observações existentes.

Para painel completo:

\[
N_{esperado}=G\times T
\]

Comparar com:

\[
N_{observado}
\]

Gerar tabela de auditoria.

---

# 13. CHAVE GEO × TIME

Verificar unicidade de:

```text
geo + time
```

Investigar:

- duplicidades;
- observações ausentes;
- períodos ausentes;
- geos incompletos;
- irregularidade temporal.

Criar matriz visual de completude:

```text
GEO × TIME
```

em que células indiquem presença/ausência.

Salvar figura.

---

# 14. MISSING VALUES

Calcular missing por:

- variável;
- geo;
- tempo;
- canal.

Criar tabela e visualização.

NÃO imputar automaticamente.

Se existirem missing values:

1. identificar padrão;
2. documentar;
3. avaliar se representam ausência real ou problema de dados;
4. criar proposta de tratamento;
5. só alterar a base quando houver justificativa clara;
6. preservar raw;
7. salvar base tratada em `processed`.

---

# 15. VALIDAÇÕES DE DOMÍNIO

Investigar:

- mídia negativa;
- spend negativo;
- population <= 0;
- KPI incompatível com o domínio;
- reach negativo;
- frequency negativa;
- valores infinitos;
- tipos inválidos.

Verificar inconsistências como:

```text
media > 0 e spend = 0
media = 0 e spend > 0
```

quando aplicável.

Não corrigir silenciosamente.

---

# 16. COST PER MEDIA UNIT

Quando aplicável, calcular:

\[
CPMU_{g,t,m}
=
\frac{Spend_{g,t,m}}{Media_{g,t,m}}
\]

com tratamento seguro para denominadores zero.

Investigar:

- distribuição;
- outliers;
- inconsistências;
- variação por geo;
- variação por tempo;
- variação por canal.

Produzir tabela resumo por canal.

---

# 17. TESTES AUTOMÁTICOS

Criar testes básicos em:

```text
tests/test_data_contract.py
```

para verificar pelo menos:

- chave geo-time;
- não negatividade onde aplicável;
- regularidade temporal;
- population válida;
- presença das variáveis obrigatórias;
- dimensões coerentes.

Esses testes não substituem EDA.

Servem como guardrails.

---

# 18. NOTEBOOK 01 — EDA GENERAL

Objetivo:

> compreender a estrutura macro do mercado antes de explorar diferenças territoriais.

---

# 19. KPI NACIONAL

Agregar corretamente o KPI dos geos para nível nacional quando sua natureza permitir soma.

Calcular:

- média;
- mediana;
- desvio padrão;
- variância;
- mínimo;
- máximo;
- P1;
- P5;
- P25;
- P50;
- P75;
- P95;
- P99;
- IQR;
- coeficiente de variação.

\[
CV=\frac{\sigma}{\mu}
\]

Criar:

- série temporal;
- histograma;
- boxplot;
- tabela descritiva.

Explicar o que cada visualização revela.

---

# 20. MÍDIAS

Para cada canal produzir uma ficha automática contendo:

- total media units;
- total spend;
- share de spend;
- média;
- mediana;
- desvio padrão;
- CV;
- mínimo;
- máximo;
- percentis;
- quantidade de zeros;
- percentual de zeros;
- períodos ativos;
- geos ativos;
- CPMU quando aplicável.

---

# 21. SHARE DE SPEND

Calcular:

\[
SpendShare_m =
\frac{\sum_{g,t} Spend_{g,t,m}}
{\sum_{g,t,m} Spend_{g,t,m}}
\]

Produzir:

- tabela;
- gráfico ordenado.

Explicar que spend share NÃO representa ROI ou eficiência.

---

# 22. SPARSITY E ATIVIDADE

Para cada mídia:

\[
Active_{g,t,m}=I(Media_{g,t,m}>0)
\]

Calcular:

- percentual de células ativas;
- percentual de células zeradas;
- quantidade de períodos com atividade;
- quantidade de geos com atividade;
- streaks de zeros;
- períodos contínuos de campanha.

Classificar apenas descritivamente padrões como:

- quase always-on;
- intermitente;
- muito esparso.

Não definir thresholds arbitrários sem documentá-los.

---

# 23. OUTLIERS

Utilizar abordagens descritivas robustas:

- IQR;
- MAD;
- percentis;
- inspeção temporal.

Não excluir outliers automaticamente.

Para cada potencial outlier:

> detectar → contextualizar → documentar → decidir.

Gerar tabela com observações extremas.

---

# 24. NOTEBOOK 02 — EDA TEMPORAL

Pergunta central:

> Como KPI, mídia, spend e controles evoluem ao longo do tempo?

---

# 25. KPI TEMPORAL

Analisar:

- tendência;
- mudanças de nível;
- picos;
- quedas;
- possíveis padrões sazonais;
- volatilidade.

Criar:

- linha temporal nacional;
- médias móveis exclusivamente como ferramenta visual, se útil;
- decomposição exploratória caso metodologicamente apropriado.

Não utilizar decomposição temporal como evidência causal.

---

# 26. CADA CANAL AO LONGO DO TEMPO

Para cada canal criar gráficos de:

- media units;
- spend;
- CPMU.

Evitar colocar todos os canais sobrepostos em um gráfico ilegível.

Usar small multiples quando conveniente.

---

# 27. MÍDIA VERSUS KPI

Para comparação visual, considerar padronização:

\[
Z(X)=\frac{X-\mu_X}{\sigma_X}
\]

Comparar temporalmente:

```text
Z(KPI)
vs
Z(Media)
```

para cada canal.

Explicar claramente:

> co-movimento visual não implica causalidade.

---

# 28. CONTROLES AO LONGO DO TEMPO

Para cada controle:

- série temporal;
- distribuição;
- variação;
- valores atípicos;
- mudanças estruturais.

Identificar controles quase constantes.

---

# 29. NOTEBOOK 03 — EDA GEO

Este notebook deve ser uma das principais contribuições do trabalho.

Pergunta:

> O mercado apresenta heterogeneidade geográfica relevante?

---

# 30. TAMANHO DOS GEOS

Para cada geo calcular:

\[
KPI_g=\sum_t KPI_{g,t}
\]

e:

\[
KPIShare_g=
\frac{KPI_g}
{\sum_g KPI_g}
\]

Produzir:

- ranking;
- distribuição;
- concentração;
- top geos;
- long tail.

Não transformar ranking de volume em ranking de performance.

---

# 31. POPULATION

Investigar:

\[
Population_g
\]

e:

\[
PopulationShare_g
=
\frac{Population_g}
{\sum_g Population_g}
\]

Gerar:

- distribuição populacional;
- ranking;
- scatter `Population × KPI`;
- Spearman;
- Pearson quando apropriado.

---

# 32. VOLUME ABSOLUTO VERSUS INTENSIDADE

Criar medidas exploratórias normalizadas por population.

Por exemplo:

\[
KPIpc_{g,t}
=
\frac{KPI_{g,t}}
{Population_g}
\]

escalando para:

```text
por 1.000
por 10.000
ou por 100.000 habitantes
```

conforme a escala fizer sentido.

Não substituir o KPI original.

Utilizar apenas como lente exploratória.

Explicar:

```text
volume alto
≠
intensidade alta
```

---

# 33. SMALL MULTIPLES DO KPI

Criar série temporal por geo usando small multiples.

Se houver muitos geos:

- selecionar amostra representativa para visualização;
- incluir maiores;
- menores;
- medianos;
- geos com padrões extremos;
- manter cálculo completo para todos.

Não escolher geos arbitrariamente sem explicar o critério.

---

# 34. CORRELAÇÃO ENTRE GEOS

Construir:

\[
Corr(KPI_g,KPI_{g'})
\]

ao longo do tempo.

Produzir heatmap.

Investigar:

- geos fortemente sincronizados;
- geos com dinâmica distinta;
- grupos aparentes.

Não fazer clustering inferencial sem necessidade.

---

# 35. VARIAÇÃO BETWEEN E WITHIN

Esta análise é OBRIGATÓRIA.

Para qualquer variável geo-temporal \(X_{g,t}\):

## Média por geo

\[
\bar X_g =
\frac{1}{T}
\sum_t X_{g,t}
\]

## Componente between

Diferenças entre:

\[
\bar X_g
\]

## Componente within

\[
X_{g,t}-\bar X_g
\]

Quantificar:

- variância total;
- variância between;
- variância within.

Aplicar a:

- KPI;
- mídias;
- spend;
- controles importantes.

Criar tabela:

| variable | total_variance | between_geo | within_geo | between_share | within_share |

Explicar didaticamente o significado.

---

# 36. POR QUE BETWEEN/WITHIN IMPORTA PARA MMM

Documentar:

Se uma mídia muda entre geos, mas permanece quase fixa dentro de cada geo:

```text
muita informação cross-sectional
pouca informação temporal within-geo
```

Se muda no tempo mas todos os geos recebem praticamente o mesmo padrão:

```text
muita informação temporal
pouca informação cross-sectional
```

Se varia em ambas:

```text
variação GEO
+
variação TIME
=
estrutura geo-temporal mais rica
```

Não declarar automaticamente que isso garante identificação causal.

---

# 37. R² GEO E R² TIME

Análise OBRIGATÓRIA.

Para cada mídia e controle estimar descritivamente:

\[
X_{g,t}
\sim
Geo_g
\]

e obter:

\[
R^2_{geo}
\]

Depois:

\[
X_{g,t}
\sim
Time_t
\]

obtendo:

\[
R^2_{time}
\]

Interpretar:

### R²_geo próximo de 1

Grande parcela da variabilidade é explicada por diferenças persistentes entre geos.

Isso implica pouca variação residual dentro dos geos.

### R²_time próximo de 1

Grande parcela da variabilidade é explicada por efeitos temporais compartilhados.

Isso implica pouca diferenciação geográfica naquele sinal.

Criar scatter:

```text
x = R²_geo
y = R²_time
```

Um ponto por variável.

Identificar cada canal.

Este deverá ser considerado um dos gráficos centrais do TCC.

Salvar versão de alta resolução.

---

# 38. NOTEBOOK 04 — MEDIA × GEO

Pergunta:

> Como a estratégia de mídia se distribui territorialmente?

---

# 39. SPEND POR GEO × CANAL

Calcular:

\[
Spend_{g,m}
=
\sum_t Spend_{g,t,m}
\]

Criar matriz:

```text
GEO × CHANNEL
```

e heatmap.

Criar tanto:

- valores absolutos;
- valores normalizados.

---

# 40. MIX DE MÍDIA DENTRO DE CADA GEO

Calcular:

\[
MediaMix_{g,m}
=
\frac{Spend_{g,m}}
{\sum_m Spend_{g,m}}
\]

Pergunta:

> Como cada geo distribui seu orçamento entre canais?

Produzir:

- heatmap;
- tabela;
- stacked bars quando legível.

---

# 41. DISTRIBUIÇÃO GEOGRÁFICA DE CADA CANAL

Calcular:

\[
GeoAllocation_{g,m}
=
\frac{Spend_{g,m}}
{\sum_g Spend_{g,m}}
\]

Pergunta:

> Como o investimento total de cada canal está distribuído entre geos?

Não confundir essa métrica com `MediaMix`.

Documentar a diferença explicitamente.

---

# 42. MEDIA PER CAPITA

Criar versões exploratórias:

\[
MediaPC_{g,t,m}
=
\frac{Media_{g,t,m}}{Population_g}
\]

e, quando útil:

\[
SpendPC_{g,t,m}
=
\frac{Spend_{g,t,m}}{Population_g}
\]

Comparar:

```text
mídia absoluta
vs
mídia ajustada por população
```

---

# 43. POPULATION × MEDIA

Para cada canal avaliar:

\[
Corr(Population_g, Media_g)
\]

Preferencialmente incluindo Spearman.

Criar scatterplots.

Objetivo:

> identificar quanto da variação geográfica bruta da mídia simplesmente acompanha diferenças de tamanho populacional.

---

# 44. GEO × TIME HEATMAPS

Esta análise é OBRIGATÓRIA.

Para cada canal produzir heatmap:

```text
linhas = geos
colunas = tempo
cor = intensidade de mídia
```

Ordenar geos de maneira consistente.

Gerar também versões para:

- spend;
- KPI;
- KPI per capita;
- controles relevantes.

Esses gráficos devem mostrar diretamente onde e quando existe variação.

---

# 45. COEFICIENTE DE VARIAÇÃO POR GEO

Para cada canal calcular, dentro de cada geo:

\[
CV_{g,m}
=
\frac{\sigma(Media_{g,t,m})}
{\mu(Media_{g,t,m})}
\]

com tratamento de médias zero.

Produzir distribuição dos CVs.

Objetivo:

> identificar em quais geos determinada mídia realmente muda ao longo do tempo.

---

# 46. CONCENTRAÇÃO GEOGRÁFICA

Avaliar concentração de mídia por geo utilizando medidas descritivas apropriadas.

Pode considerar:

- participação dos maiores geos;
- HHI, se metodologicamente justificado;
- concentração cumulativa.

Explicar a métrica antes de utilizar.

---

# 47. NOTEBOOK 05 — RELATIONSHIPS

Pergunta:

> Existem relações entre mídias, controles, KPI, geo e tempo que possam dificultar interpretação ou identificação estatística?

---

# 48. CORRELAÇÃO EM TRÊS NÍVEIS

Calcular relações separadamente.

## A. Nacional

Após agregação apropriada:

\[
Corr(X_t,Z_t)
\]

## B. Overall geo-time

\[
Corr(X_{g,t},Z_{g,t})
\]

## C. Within-geo

Remover médias específicas dos geos ou calcular relações dentro dos geos.

Comparar resultados.

Explicar por que correlações agregadas e within podem diferir.

---

# 49. MEDIA × MEDIA

Gerar matrizes de:

- Pearson;
- Spearman.

Separar:

- media units;
- spend.

Sinalizar canais altamente sincronizados.

Não remover canais automaticamente.

---

# 50. MEDIA × KPI

Calcular como análise descritiva.

Escrever explicitamente:

> Correlação mídia-KPI não constitui efeito de mídia.

Discutir possíveis confundidores como:

- sazonalidade;
- tendência;
- alocação de mídia antecipando demanda;
- diferenças geográficas;
- fatores de negócio.

---

# 51. CONTROLS

Para cada controle investigar relações com:

- KPI;
- cada mídia;
- spend;
- geo;
- tempo.

Aplicar também:

\[
R²_{geo}
\]

e:

\[
R²_{time}
\]

aos controles.

Identificar controles quase perfeitamente geográficos ou temporais.

---

# 52. VIF

Calcular VIF de forma tecnicamente adequada.

Investigar:

- overall geo-time;
- dentro dos geos quando possível e estatisticamente válido.

Explicar:

\[
VIF_j=
\frac{1}{1-R_j^2}
\]

Não utilizar automaticamente regra como:

```text
VIF > X → remover variável
```

Tratar VIF como diagnóstico.

Documentar thresholds apenas quando provenientes de fonte metodológica apropriada ou do próprio Meridian.

---

# 53. LAGS EXPLORATÓRIOS

Como investigação descritiva, pode ser útil analisar:

\[
Corr(Media_{t-k},KPI_t)
\]

para pequenos lags.

Entretanto:

- não utilizar isso para estimar adstock;
- não escolher parâmetros finais do Meridian apenas pela maior correlação;
- não interpretar como causalidade.

Se realizado, explicar claramente essas limitações.

---

# 54. NOTEBOOK 06 — MERIDIAN OFFICIAL EDA

Depois de concluir a EDA própria, utilizar o pacote oficial de EDA do Meridian como camada independente de validação.

Verificar primeiro a API atual.

Na versão atual, espera-se algo conceitualmente semelhante a:

```python
from meridian.model.eda import meridian_eda

mmm_eda = meridian_eda.MeridianEDA(mmm)
```

Mas NÃO copie cegamente esse código se a API oficial tiver mudado.

---

# 55. NÃO ESTIMAR O POSTERIOR

Instanciar apenas os objetos necessários para executar a EDA oficial.

Não rodar posterior sampling.

O objetivo é:

```text
nossa EDA independente
        ↓
comparação
        ↓
Meridian Official EDA
```

---

# 56. RELATÓRIO HTML OFICIAL

Gerar o relatório completo da ferramenta oficial.

Salvar em:

```text
outputs/reports/meridian_eda_report.html
```

Se possível, também gerar versão acessível diretamente no notebook.

---

# 57. CHECKS OFICIAIS

Extrair e documentar os resultados relacionados a:

1. spend e media units;
2. variabilidade individual;
3. outliers e sparsity;
4. population scaling;
5. relações entre variáveis;
6. correlação;
7. VIF;
8. colinearidade com geo;
9. colinearidade com tempo;
10. data adequacy/data-to-parameter ratio, quando disponível.

Não alterar thresholds default sem necessidade.

Caso algum threshold seja modificado:

- informar default;
- informar novo valor;
- justificar;
- registrar em `docs/decisions.md`.

---

# 58. DATA-TO-PARAMETER RATIO

Quando disponível e aplicável, calcular e explicar o guardrail utilizado pelo Meridian.

Conceitualmente:

\[
n_{data}=G\times T
\]

Comparar com quantidade aproximada de parâmetros.

Não apresentar a razão como prova definitiva de suficiência dos dados.

Explicar que modelos hierárquicos compartilham informação entre geos e que adequação final também será avaliada posteriormente por posterior uncertainty e diagnósticos do modelo.

---

# 59. COMPARAÇÃO ENTRE EDA PRÓPRIA E EDA OFICIAL

Criar tabela:

| issue | custom_eda | meridian_eda | agreement | interpretation |

Investigar divergências.

A ferramenta oficial deve funcionar como **auditor**, não como substituto da análise.

---

# 60. NOTEBOOK 07 — EDA CONCLUSIONS

Este notebook deve sintetizar toda a fase.

Não adicionar dezenas de novas análises.

Responder sequencialmente às perguntas de pesquisa exploratórias.

---

# 61. READINESS REPORT

Criar tabela consolidada:

| Dimension | Question | Evidence | Finding | Modeling implication |
|---|---|---|---|---|

Incluir pelo menos:

```text
integridade
missing
outliers
KPI variation
media variation
spend variation
temporal variation
geo variation
within variation
between variation
geo-time variation
population scaling
media mix heterogeneity
channel collinearity
control collinearity
R² geo
R² time
data adequacy
```

---

# 62. PERGUNTA 1 — ESTRUTURA

Responder:

> Os dados possuem estrutura apropriada e qualidade suficiente para avançar para modelagem?

Fundamentar com números.

---

# 63. PERGUNTA 2 — TEMPO

Responder:

> Como KPI, mídia, spend e controles variam ao longo do período?

Destacar:

- tendências;
- campanhas;
- sparsity;
- mudanças estruturais.

---

# 64. PERGUNTA 3 — GEO

Responder:

> KPI, mídia e investimento diferem entre mercados?

Usar evidências de:

- distribuição;
- population;
- KPI per capita;
- media per capita;
- spend;
- media mix.

---

# 65. PERGUNTA 4 — GEO × TIME

Esta deve receber a conclusão mais aprofundada:

> A base apresenta variação simultânea entre geos e ao longo do tempo capaz de oferecer informação adicional para um MMM geo-level?

Utilizar:

- between/within decomposition;
- CV within geo;
- GEO × TIME heatmaps;
- R²_geo;
- R²_time;
- diferenças de media mix;
- diferenças de alocação geográfica;
- sparsity;
- population scaling.

Não utilizar linguagem absoluta.

---

# 66. PERGUNTA 5 — IDENTIFICABILIDADE

Responder descritivamente:

> Existem canais ou controles cuja variação parece fortemente associada a efeitos exclusivamente geográficos, exclusivamente temporais ou a outros canais?

Isso deverá preparar decisões futuras de especificação.

---

# 67. CONCLUSÃO PERMITIDA

Exemplo de estrutura, APENAS se sustentada pelos resultados:

> Os dados apresentam variação temporal e geográfica relevante, com diferenças observáveis na distribuição territorial das mídias e no mix de investimento entre mercados. A decomposição between/within e a análise de colinearidade com efeitos de geo e tempo indicam que parte dos canais contém variação geo-temporal adicional potencialmente informativa para a estimação hierárquica no Meridian.

---

# 68. CONCLUSÕES NÃO PERMITIDAS NESTA FASE

Não afirmar:

```text
Canal A gera mais vendas.
Canal B é mais eficiente.
Canal C tem maior ROI.
O efeito causal de TV é X.
Devemos aumentar investimento em Search.
O melhor canal é Y.
```

Ainda não estimamos o MMM.

---

# 69. FIGURAS OBRIGATÓRIAS

Ao final da fase, devem existir pelo menos:

1. painel de completude GEO × TIME;
2. série temporal nacional do KPI;
3. distribuição do KPI;
4. share de spend por canal;
5. séries temporais de cada canal;
6. atividade/zeros por canal;
7. KPI por geo;
8. population por geo;
9. Population × KPI;
10. KPI per capita por geo;
11. small multiples do KPI;
12. correlação entre geos;
13. decomposição between/within;
14. R²_geo × R²_time;
15. heatmap GEO × CHANNEL de spend;
16. heatmap de media mix;
17. heatmap de geo allocation;
18. heatmaps GEO × TIME por mídia;
19. Population × Media por canal;
20. matriz de correlação de mídias;
21. matriz de correlação within-geo;
22. VIF;
23. summary/readiness dashboard.

Salvar em:

```text
outputs/figures/
```

com:

- nomes descritivos;
- resolução adequada para TCC;
- títulos;
- subtítulos quando úteis;
- labels claros;
- unidades;
- fonte dos dados quando apropriado.

Não usar estética excessivamente decorativa.

Priorizar visual acadêmico limpo.

---

# 70. TABELAS OBRIGATÓRIAS

Exportar CSV e, quando útil, Markdown:

```text
data_dictionary
data_audit
missing_summary
duplicate_summary
channel_summary
channel_activity
spend_share
geo_kpi_summary
population_summary
geo_media_summary
within_between_variance
geo_time_r2
correlation_summary
vif_summary
meridian_eda_checks
readiness_report
```

Salvar em:

```text
outputs/tables/
```

---

# 71. DOCUMENTAÇÃO ACADÊMICA

Criar:

```text
docs/methodology_eda.md
```

explicando:

- objetivo;
- métodos;
- equações;
- métricas;
- limitações.

Criar:

```text
docs/eda_story.md
```

como narrativa sequencial dos resultados.

Criar:

```text
docs/findings.md
```

com os principais achados factuais.

Criar:

```text
docs/decisions.md
```

registrando decisões como:

```text
Problema identificado
Evidência
Alternativas
Decisão
Justificativa
Impacto esperado
```

---

# 72. README

Atualizar `README.md`.

Adicionar:

## Projeto

Contexto acadêmico.

## Objetivo

MMM com Meridian e dados geo-level.

## Fase atual

EDA.

## Dados

Origem oficial.

## Estrutura do repositório

Explicação das pastas.

## Como executar

Local.

## Como executar no Colab

Passo a passo.

## Ordem dos notebooks

```text
00 → 01 → 02 → 03 → 04 → 05 → 06 → 07
```

---

# 73. MASTER COLAB

Além dos notebooks modulares, gerar:

```text
notebooks/EDA_COMPLETE_COLAB.ipynb
```

Esse notebook deverá reunir a sequência analítica completa de forma linear.

Objetivo:

> permitir que o pesquisador copie o notebook para Google Colab e execute toda a EDA do início ao fim.

Ele deve reutilizar funções de `src`.

No início, incluir opção para clonar o repositório GitHub quando executado no Colab.

Entretanto, não hardcode um repositório inexistente.

Deixe uma variável claramente identificada:

```python
REPO_URL = "SUBSTITUIR_PELO_REPOSITORIO"
```

caso ainda não seja possível detectar automaticamente o repositório real.

---

# 74. INDEPENDÊNCIA DAS CÉLULAS

O notebook deve seguir ordem lógica.

Evitar estados ocultos.

Cada seção deve informar dependências anteriores.

Todas as variáveis principais devem ter nomes claros.

Evitar:

```python
a
b
df2
teste3
temp_final2
```

Preferir:

```python
geo_time_panel
channel_summary
within_geo_variance
geo_time_r2
```

---

# 75. QUALIDADE DO PYTHON

Aplicar:

- funções pequenas;
- docstrings;
- type hints onde agregarem clareza;
- tratamento de erros;
- validação;
- nomes semânticos;
- comentários apenas quando úteis;
- DRY sem exagerar abstração.

Evitar:

- classes desnecessárias;
- padrões de software excessivamente complexos;
- código duplicado;
- células gigantes.

---

# 76. PERFORMANCE

A base é de exemplo, portanto priorizar clareza.

Ainda assim:

- preferir operações vetorizadas;
- evitar loops desnecessários;
- reutilizar agregações;
- evitar recalcular arquivos repetidamente.

---

# 77. PLOTS

Preferir:

- matplotlib;
- plotly quando interatividade realmente ajudar.

Não utilizar bibliotecas apenas por estética.

Criar funções reutilizáveis.

Sempre considerar:

- legibilidade;
- número de geos;
- número de canais;
- escala;
- outliers.

Quando houver muitos geos, não criar gráficos ilegíveis.

---

# 78. NÃO ESCONDER RESULTADOS PROBLEMÁTICOS

Se encontrar:

- pouca variação;
- canais altamente correlacionados;
- geos sem mídia;
- painel incompleto;
- outliers;
- sparsity;
- relação quase perfeita com tempo;
- relação quase perfeita com geo;
- inconsistência spend/media;

NÃO tente "consertar" apenas para permitir modelagem.

Documente.

O TCC deve refletir limitações reais.

---

# 79. NÃO OTIMIZAR PREMATURAMENTE

Não testar diversas transformações apenas para obter números mais "bonitos".

Não eliminar canais automaticamente.

Não remover geos automaticamente.

Não ajustar thresholds apenas para eliminar warnings.

Toda alteração deve possuir justificativa estatística ou de domínio.

---

# 80. LOG DE EXECUÇÃO

Criar mecanismo simples de logging.

Registrar:

- início;
- dataset carregado;
- dimensões;
- validações;
- arquivos criados;
- warnings relevantes;
- erros.

Salvar logs em:

```text
outputs/logs/
```

---

# 81. CHECKPOINTS

Após cada notebook, imprimir uma seção:

```text
CHECKPOINT
```

com:

```text
O que descobrimos?
Quais problemas apareceram?
O que ainda precisamos investigar?
Podemos avançar?
```

---

# 82. STORYTELLING GERAL

A narrativa completa deve seguir:

```text
1. O que recebemos?
        ↓
2. Os dados são confiáveis?
        ↓
3. Como o mercado evolui no tempo?
        ↓
4. Como os mercados diferem geograficamente?
        ↓
5. Como a mídia é distribuída entre os mercados?
        ↓
6. Existe variação dentro dos geos?
        ↓
7. Existe variação entre geos?
        ↓
8. Quanto da mídia é explicada apenas por GEO?
        ↓
9. Quanto é explicado apenas por TIME?
        ↓
10. Canais se movimentam juntos?
        ↓
11. Population explica parte das diferenças?
        ↓
12. O pacote oficial Meridian identifica os mesmos problemas?
        ↓
13. Os dados parecem apropriados para avançar ao MMM?
```

---

# 83. FILOSOFIA DE INTERPRETAÇÃO

Para toda análise seguir:

\[
Pergunta
\rightarrow
Método
\rightarrow
Resultado
\rightarrow
Interpretação
\rightarrow
Limitação
\rightarrow
Implicação
\]

Nunca apenas:

```text
código → gráfico
```

---

# 84. OBJETIVO ACADÊMICO DA FASE

O resultado final da EDA deve permitir que o texto do TCC explique, com evidências, por que utilizar dados geo-level é estatisticamente diferente de trabalhar apenas com uma série nacional.

O trabalho deve mostrar empiricamente quando possível:

\[
Informação\ nacional
=
variação\ temporal
\]

enquanto um painel geo-level potencialmente oferece:

\[
Informação
=
variação\ temporal
+
variação\ geográfica
+
variação\ dentro\ dos\ geos
+
variação\ entre\ geos.
\]

Mas tratar isso como hipótese a ser investigada nos dados, não como conclusão pré-definida.

---

# 85. CRITÉRIO FINAL DE SUCESSO

Considere esta fase concluída apenas quando:

- dados estiverem auditados;
- schema estiver documentado;
- painel geo-temporal estiver validado;
- KPI estiver caracterizado;
- mídias estiverem caracterizadas;
- spend estiver caracterizado;
- controles estiverem caracterizados;
- population estiver analisada;
- variação temporal estiver documentada;
- variação geográfica estiver documentada;
- variação within/between estiver quantificada;
- mix de mídia por geo estiver analisado;
- alocação dos canais por geo estiver analisada;
- GEO × TIME heatmaps estiverem produzidos;
- R²_geo e R²_time estiverem calculados;
- correlações estiverem analisadas;
- VIF estiver analisado;
- pacote oficial Meridian EDA estiver executado;
- resultados oficiais e próprios estiverem comparados;
- readiness report estiver produzido;
- conclusões e limitações estiverem documentadas;
- notebooks funcionarem do início ao fim;
- master notebook funcionar no Google Colab;
- outputs estiverem salvos e organizados;
- README estiver atualizado.

---

# 86. FORMA DE EXECUÇÃO DO TRABALHO

Não entregue apenas uma proposta.

EXECUTE o projeto.

Faça:

```text
inspeção
→ implementação
→ execução dos notebooks
→ correção dos erros
→ validação dos outputs
→ documentação
→ organização final do repositório
```

Sempre que o ambiente permitir executar Python, execute o código para validar.

Não considere um notebook pronto apenas porque o código "parece correto".

---

# 87. TRATAMENTO DE ERROS

Se uma etapa falhar:

1. investigar a causa;
2. consultar documentação oficial;
3. corrigir;
4. executar novamente;
5. documentar mudanças relevantes.

Não remover análises porque apresentaram erro sem antes investigar.

---

# 88. NÃO INVENTAR RESULTADOS

Regra absoluta:

> Nenhum resultado, número, correlação, conclusão ou característica do dataset pode ser inventado.

Se determinada análise não puder ser executada:

```text
marcar como não executada
+
explicar motivo
+
explicar como deveria ser executada posteriormente.
```

---

# 89. VERIFICAÇÃO FINAL

Antes de encerrar:

Executar uma auditoria do próprio projeto.

Verificar:

```text
[ ] todos notebooks existem
[ ] todos executam em sequência
[ ] imports funcionam
[ ] paths funcionam
[ ] dados raw não foram modificados
[ ] outputs foram gerados
[ ] figuras possuem labels
[ ] tabelas foram exportadas
[ ] não existem conclusões inventadas
[ ] não existe linguagem causal indevida
[ ] Meridian EDA foi validado contra documentação atual
[ ] documentação foi criada
[ ] README está atualizado
[ ] master Colab está executável
```

---

# 90. RESUMO FINAL A SER PRODUZIDO PELO CODEX

Ao finalizar a implementação, produzir uma mensagem resumindo:

## Arquivos criados

Listar.

## Arquivos modificados

Listar.

## Dados utilizados

Descrever.

## Análises executadas

Resumir.

## Principais achados

Somente achados efetivamente observados.

## Problemas encontrados

Listar.

## Decisões tomadas

Listar.

## Limitações

Listar.

## Validação

Informar o que foi efetivamente executado/testado.

## Próxima etapa recomendada

A próxima fase deverá ser:

```text
Especificação do primeiro modelo baseline no Google Meridian
```

mas NÃO implementar essa fase agora.

---

# 91. PRINCÍPIO FINAL

Este projeto não deve ser tratado como:

```text
carregar dados
→ gerar gráficos
→ rodar Meridian
```

Ele deve ser tratado como uma investigação estatística:

```text
DADOS
   ↓
AUDITORIA
   ↓
COMPREENSÃO
   ↓
TEMPO
   ↓
GEO
   ↓
POPULATION
   ↓
MÍDIA
   ↓
GEO × MÍDIA
   ↓
GEO × TEMPO
   ↓
WITHIN × BETWEEN
   ↓
R² GEO × R² TIME
   ↓
CORRELAÇÃO / COLINEARIDADE
   ↓
VALIDAÇÃO COM MERIDIAN EDA
   ↓
READINESS REPORT
   ↓
DECISÃO FUNDAMENTADA SOBRE AVANÇAR PARA O MMM
```

O objetivo não é apenas produzir código correto.

O objetivo é produzir uma **EDA reproduzível, estatisticamente defensável, visualmente clara e academicamente utilizável como parte do TCC**, de modo que um leitor que conheça estatística, mas ainda seja iniciante em Marketing Science e MMM, consiga acompanhar toda a investigação do começo ao fim e compreender:

> o que foi analisado, por que foi analisado, como foi analisado, o que os dados mostraram, o que isso significa para o futuro MMM e o que ainda não pode ser concluído.