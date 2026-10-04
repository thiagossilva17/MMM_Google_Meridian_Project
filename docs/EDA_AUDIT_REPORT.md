# Auditoria independente da EDA — MMM Google Meridian

Data: 04/10/2026. Repositório: `thiagossilva17/MMM_Google_Meridian_Project`.
Objeto auditado: branch `main`, commit **c301905af45877ec30fed37c63cfd102e2093ced**.
Este relatório avalia esse estado anterior à inclusão dos artefatos de auditoria.

## 1. Executive Summary

**Nota final: 8,2 / 10 — 82,0 / 100.**  
**Prontidão para MMM: PRONTO COM CORREÇÕES IMPORTANTES.**  
**Confiança da auditoria: Alta para cálculos e execução local; Média para completude interpretativa/visual; Colab real não comprovado.**

A EDA é muito boa como infraestrutura científica e demonstra variação geo-temporal adicional potencialmente útil. A decomposição between/within, os R² GEO/TIME, a normalização populacional e o VIF foram conferidos independentemente. Não identifiquei erro matemático material nesses cálculos, fabricação de resultados ou atribuição sistemática de causalidade a correlações. O projeto é substancialmente mais completo que um conjunto de rankings e gráficos por região.

A execução em ambiente virtual novo passou nos 11 testes. As células dos oito notebooks e do master passaram em processos IPython novos, sem usar outputs armazenados como evidência de execução. Os 88 CSVs regenerados coincidiram com os versionados dentro de tolerância numérica. A EDA oficial também executou: Meridian 2.1.0, 13 checks, 16 achados, sendo 10 INFO e 6 REVIEW; somente o grupo `prior` foi produzido. A tentativa via nbclient falhou antes de executar células devido à restrição de sockets do ambiente, não por erro da análise.

Os principais descontos são de **profundidade e entrega**: triagem de outliers sem investigação localizada suficiente; Channel2 esparso sem estudo narrativo das sequências e heterogeneidade; comparação customizada/oficial completa para R², mas superficial em outros diagnósticos; conclusões e checkpoints excessivamente genéricos. Há também um erro visual reproduzido: a divisão por população reordena os geos nos heatmaps per capita, contrariando a afirmação de ordenação fixa. Dois SVGs publicados estão vazios, embora o código os regenere.

O projeto permite iniciar o planejamento da especificação. Para apresentar a EDA como fase concluída e usar seus achados na decisão do primeiro ajuste, é necessário encerrar os alertas relevantes e aprofundar a síntese por canal. Não é necessário reconstruir a EDA nem acrescentar métodos sofisticados sem uma pergunta concreta.

## 2. O que foi auditado

Foram inventariados **221 arquivos versionados**: README, dependências, 9 notebooks, 10 módulos de `src`, 3 scripts, testes, dados bruto/processado, metadados, documentação, 88 tabelas e 78 figuras SVG, além dos relatórios e logs. O inventário completo está em `outputs/audit/inventory.json`. A especificação original `docs/execution_specification.md` foi lida e usada como requisito primário; o roteiro de auditoria anexado orientou avaliação, rubricagem e estrutura deste relatório.

| Local | Conteúdo auditado |
|---|---|
| Raiz | README, requirements, requirements-colab, pytest.ini |
| data/raw, processed, metadata | CSV original, transformação, hash, origem, licença e versões |
| notebooks/00…07 e EDA_COMPLETE_COLAB | Markdown, código, outputs anteriores e reexecução das células |
| src/ | config, data, validation, statistics, eda, geo_analysis, official_eda, plots, reporting, init |
| scripts/ | Geração de notebooks, execução nbclient e CLI |
| docs/ | Especificação original, metodologia, achados, narrativa, decisões, cobertura e validação |
| outputs/ | figures → 6 capítulos; tables → 88 CSVs; reports → capítulos e HTML; logs |
| tests/ | Contrato, casos inválidos, identidades, VIF e receita |

Ambiente da auditoria: Python **3.12.14**, CPU, venv novo, instalação pelo `requirements.txt` sem alterar dependências do projeto. Versões efetivas em `outputs/audit/environment.txt`: Meridian 2.1.0, NumPy 2.3.5, pandas 2.3.3, SciPy 1.18.1, statsmodels 0.14.6, matplotlib 3.10.9, JAX 0.11.2 e TensorFlow 2.21.0.

Escopo visual: dez figuras centrais foram abertas e inspecionadas visualmente; todos os 78 SVGs foram verificados estruturalmente e regenerados. Não afirmo inspeção visual individual de todos os 78 gráficos nem navegação interativa do HTML oficial. O HTML foi regenerado e seus artefatos numéricos foram comparados.

## 3. Validação de execução

| Component | Executed? | Result | Problems |
|---|---:|---|---|
| Instalação em venv novo | Sim | Concluída pelo requirements original | Dependências grandes; versões transitivas não congeladas no requirements |
| Download oficial independente | Sim | 966.498 bytes; SHA-256 idêntico | Nenhum |
| pytest | Sim | 11/11 passaram | Testes não validam publicação de SVG nem ordem dos eixos |
| 00_data_audit | Sim | Células passaram; 2,35 s | Nenhum erro de execução |
| 01_eda_general | Sim | Células passaram; 2,57 s | Nenhum erro de execução |
| 02_eda_temporal | Sim | Células passaram; 7,64 s | Nenhum erro de execução |
| 03_eda_geo | Sim | Células passaram; 7,83 s | SVG vazio no commit, regenerado na cópia |
| 04_eda_media_geo | Sim | Células passaram; 18,65 s | Ordem visual per capita inconsistente; SVG vazio no commit |
| 05_eda_relationships | Sim | Células passaram; 2,63 s | Nenhum erro de execução |
| 06_meridian_official_eda | Sim | Células passaram; 25,79 s | Warnings registrados; sem posterior |
| 07_eda_conclusions | Sim | Células passaram; 0,99 s | Consome CSVs por existência, sem manifesto de validade |
| EDA_COMPLETE_COLAB local | Sim | 11 células de código; 61,54 s | Não equivale a sessão no serviço Colab |
| CLI scripts/run_eda.py | Sim | Execução completa registrada | Mesmos módulos, sem correção do código |
| Executor scripts/execute_notebooks.py | Tentado | Kernel não iniciou | Operation not permitted em resolução/socket ZMQ; limitação ambiental |
| Google Colab real | Não | Não comprovado | Requer futura sessão nova no serviço |
| Sanity checks independentes | Sim | 36/36 passaram | Não equivalem a prova de correção de qualquer entrada futura |
| Comparação de outputs | Sim | 88/88 CSVs equivalentes; 78 SVGs regenerados válidos | 2/78 SVGs originais vazios |

Foi usada uma cópia temporária separada, removendo outputs anteriores e limpando outputs das células antes da sequência 00→07. O master executou em novo processo e refez a sequência inteira; rodou após os capítulos, portanto seus arquivos de entrada/saída não constituíam uma segunda cópia de filesystem vazia. O código foi lido para conferir que ele chama todos os capítulos, sem pular etapas por existência de arquivos. A CLI também foi testada.

`execute_cells.py` usa IPython para avaliar as células originais, em ordem, em subprocesso novo por notebook, sem alterar a lógica analítica. Essa alternativa valida código e produção de outputs, mas não a comunicação kernel/frontend do Jupyter. Logs completos e tempos estão em `outputs/audit/`. O problema de sockets não recebeu penalização como defeito do projeto.

## 4. Matriz completa de requisitos

A matriz abaixo contém **84 requisitos avaliáveis**, cobrindo os blocos relevantes da especificação original e as ampliações do roteiro de auditoria. `Quality` é profundidade: 0 ausente/não validado, 1 superficial, 2 adequado, 3 profundo. A nota global é calculada separadamente pela rubrica da seção 18, não pela média desses valores. `COMPLETO` exige implementação e validação; `PARCIAL` pode significar cálculo correto, mas interpretação incompleta. Em Colab/nbclient, “não executado” significa não concluído neste mecanismo/serviço, apesar da alternativa local bem-sucedida.

Referências `.csv` sem pasta apontam a `outputs/tables/`; evidências de auditoria `.json` e logs apontam a `outputs/audit/`. A coluna `source_requirement` do CSV vincula cada linha aos blocos originais. As 23 famílias de figuras e 16 famílias de tabelas solicitadas têm correspondentes funcionais; duas figuras individuais estão vazias no commit e recebem ressalva própria.

| ID   | Requirement                                         | Status                         | Evidence                                                              |   Quality | Problem                                                                       | Recommendation                                                         |
|:-----|:----------------------------------------------------|:-------------------------------|:----------------------------------------------------------------------|----------:|:------------------------------------------------------------------------------|:-----------------------------------------------------------------------|
| A01  | Proveniência oficial, commit e hash                 | COMPLETO                       | data/metadata/source.json; source_download.json                       |         3 | —                                                                             | Manter raw e fonte fixados                                             |
| A02  | Schema real e pares media/spend                     | COMPLETO                       | src/data.py:channels,roles; data_dictionary.csv                       |         3 | —                                                                             | Manter rejeição de schema desconhecido                                 |
| A03  | Dimensões e frequência                              | COMPLETO                       | data_audit.csv; independent_checks.json                               |         3 | —                                                                             | Manter 40×156=6240 e grade semanal                                     |
| A04  | Unicidade e completude GEO×TIME                     | COMPLETO                       | src/validation.py:audit; tests/test_data_contract.py                  |         3 | —                                                                             | Manter contrato e visual de presença                                   |
| A05  | Missing por variável/geo/tempo/canal                | COMPLETO                       | missing_summary.csv; missing_by_geo/time/channel.csv                  |         2 | —                                                                             | Manter ausência de imputação                                           |
| A06  | Domínio, finitos e população                        | COMPLETO                       | src/validation.py:require_valid_panel; pytest.txt                     |         3 | —                                                                             | Manter falha explícita                                                 |
| A07  | Inconsistências media positiva/spend zero e inverso | COMPLETO                       | data_audit.csv; src/validation.py:audit                               |         2 | —                                                                             | Manter contadores por canal                                            |
| A08  | Dicionário: papel, tipo, unidade e dimensão         | PARCIAL                        | docs/data_dictionary.md; src/validation.py:dictionary                 |         2 | geo e time recebem dimensão genérica geo×time                                 | Distinguir coordenadas de variáveis e explicitar os pares              |
| A09  | Reach/frequency                                     | NÃO APLICÁVEL                  | CSV raw e roles validados                                             |         0 | Ausentes no dataset                                                           | Não inventar variáveis                                                 |
| A10  | Orgânico e Promo                                    | COMPLETO                       | config.py; temporal; official_eda.py                                  |         2 | —                                                                             | Manter como papéis próprios                                            |
| A11  | Raw preservado e processed separado                 | COMPLETO                       | src/data.py:load_panel; source_download.json                          |         3 | —                                                                             | Manter validação do índice exportado                                   |
| A12  | CPMU: zeros, agregação e estatísticas               | COMPLETO                       | cost_per_media_unit.csv; national_cpmu.csv; geo_cpmu.csv              |         3 | —                                                                             | Manter razões de somas no nacional e NaN em 0/0                        |
| A13  | CPMU: extremos e interpretação                      | PARCIAL                        | custom_vs_meridian.csv; Channel2_timeseries.svg                       |         2 | Alertas contextualizados; gráfico amplia ruído de 10⁻⁹                        | Anotar escala relativa e contextualizar casos oficiais                 |
| B01  | KPI nacional: estatísticas, distribuição, série     | COMPLETO                       | national_descriptive.csv; general/kpi_distribution.svg                |         2 | —                                                                             | Manter soma de conversões sintéticas                                   |
| B02  | Ficha de mídia por canal                            | COMPLETO                       | channel_summary.csv; channel_activity.csv                             |         2 | —                                                                             | Manter totais, percentis, CV e CPMU                                    |
| B03  | Share de spend e denominador                        | COMPLETO                       | spend_share.csv; independent_checks.json                              |         3 | —                                                                             | Manter distinção de retorno                                            |
| B04  | Atividade e sequências de zeros                     | PARCIAL                        | activity_runs.csv; activity_streaks.csv; 01_eda_general               |         1 | Cálculo existe, sequências e exceções pouco interpretadas                     | Explicar Channel2 e contrastar Channel3                                |
| B05  | Outliers: IQR/MAD e preservação                     | COMPLETO                       | src/statistics.py:outliers; outliers.csv                              |         2 | —                                                                             | Preservar dados e indefinição quando MAD=0                             |
| B06  | Outliers: contextualizar e decidir por caso         | PARCIAL                        | outliers.csv:6039 registros e uma única decisão textual               |         1 | Triagem não se converte em investigação localizada                            | Investigar maiores casos e grupos após ajuste populacional             |
| B07  | KPI: tendência, picos, volatilidade, sazonalidade   | PARCIAL                        | kpi_stl_52.csv; kpi_acf.csv; kpi_level_changes.csv; relatório 02      |         2 | STL/ACF exportados sem leitura dos resultados principais                      | Narrar padrões, datas e limites dos três ciclos                        |
| B08  | Séries individuais media/spend/CPMU                 | COMPLETO                       | temporal/Channel0–4_timeseries.svg                                    |         2 | —                                                                             | Manter gráficos separados com unidades                                 |
| B09  | Z-score KPI×mídia                                   | COMPLETO                       | src/eda.py:temporal; Channel*_kpi_z.svg                               |         2 | —                                                                             | Manter uso descritivo                                                  |
| B10  | Controles: séries, distribuição, quase constância   | PARCIAL                        | control_temporal_summary.csv; relatórios 02 e 05                      |         2 | Quase constância e mudanças não recebem discussão por controle                | Discutir amplitude, desvio, R² e associações individuais               |
| B11  | Lags exploratórios                                  | COMPLETO                       | exploratory_lags.csv; src/eda.py:relationships                        |         2 | —                                                                             | Manter como opcional, sem escolha de adstock                           |
| C01  | KPI por geo, ranking, shares, concentração          | COMPLETO                       | geo_kpi_summary.csv; kpi_concentration.csv                            |         2 | —                                                                             | Manter distinção entre volume e performance                            |
| C02  | Population por geo e estabilidade temporal          | COMPLETO                       | population_summary.csv; data_audit.csv                                |         3 | —                                                                             | Manter um denominador por geo                                          |
| C03  | Population×KPI Pearson/Spearman                     | COMPLETO                       | population_kpi_correlation.csv; geo/population_kpi.svg                |         2 | —                                                                             | Manter ambas as lentes                                                 |
| C04  | KPI, mídia e spend per capita                       | COMPLETO                       | per_capita_panel.csv; independent_checks.json                         |         3 | —                                                                             | Manter como exploração sem substituir inputs brutos                    |
| C05  | Small multiples representativos                     | PARCIAL                        | geo_plot_selection.csv; kpi_small_multiples.svg                       |         2 | Seleção boa, datas se sobrepõem e painéis pouco interpretados                 | Ajustar ticks e comentar geos extremos                                 |
| C06  | Correlação entre geos e sincronização               | PARCIAL                        | geo_kpi_correlation.csv; geo/geo_correlation.svg                      |         1 | Matriz calculada sem síntese de pares/distribuição                            | Resumir mediana, extremos e ausência de forte sincronização            |
| D01  | Decomposição KPI/media/spend/controles              | COMPLETO                       | within_between_variance.csv; OLS independente                         |         3 | —                                                                             | Manter ddof=0, pesos e validação de painel                             |
| D02  | R² GEO com intercepto                               | COMPLETO                       | src/statistics.py:variance_decomposition; independent_checks.json     |         3 | —                                                                             | Manter definição descritiva                                            |
| D03  | R² TIME com intercepto                              | COMPLETO                       | geo_time_r2.csv; OLS independente                                     |         3 | —                                                                             | Manter distinção de efeitos comuns                                     |
| D04  | Resíduo two-way bruto e per capita                  | COMPLETO                       | geo_time_r2_per_capita.csv; metodologia                               |         3 | —                                                                             | Preservar avanço além de within simples                                |
| D05  | Scatter R² GEO×TIME                                 | COMPLETO                       | geo/geo_time_r2.svg                                                   |         2 | —                                                                             | Manter legenda; limites de eixo adaptáveis são opcionais               |
| D06  | Spend GEO×canal                                     | COMPLETO                       | geo_media_summary.csv; spend_geo_channel.svg                          |         2 | —                                                                             | Manter unidades explícitas                                             |
| D07  | Media mix e soma por geo                            | COMPLETO                       | media_mix.csv; independent_checks.json                                |         3 | —                                                                             | Manter denominador por linha                                           |
| D08  | Geo allocation e soma por canal                     | COMPLETO                       | geo_allocation.csv; independent_checks.json                           |         3 | —                                                                             | Manter denominador por coluna                                          |
| D09  | Magnitude e interpretação da heterogeneidade do mix | PARCIAL                        | media_mix.csv; relato 04                                              |         1 | Somente amplitude máxima, escrita em % em vez de p.p.                         | Quantificar dispersão e explicar semelhança entre geos                 |
| D10  | Population×media por canal                          | COMPLETO                       | population_media_correlation.csv; Channel*_population.svg             |         2 | —                                                                             | Manter Pearson e Spearman                                              |
| D11  | Comparar população com intensidades e gasto         | PARCIAL                        | per_capita_panel.csv; media_geo                                       |         2 | Versões per capita existem, mas interpretação cruzada é limitada              | Comparar relação bruta com normalizada; spend quase proporcional       |
| D12  | Heatmaps media/spend/KPI/controles                  | PARCIAL                        | 78 SVGs; inventory.json                                               |         2 | Dois SVGs versionados têm zero bytes                                          | Regenerar e validar publicação; código regenera corretamente           |
| D13  | Mesma ordenação entre heatmaps brutos/per capita    | EXECUTADO COM ERRO             | src/geo_analysis.py:107; heatmap_order.json                           |         1 | Pandas reordena linhas após div; contradiz narrativa                          | Aplicar reindex(order) após divisão e conferir eixos                   |
| D14  | CV within por geo/canal                             | COMPLETO                       | within_geo_cv.csv; within_cv_distribution.svg                         |         2 | —                                                                             | Manter proteção para média zero                                        |
| D15  | Interpretar CV e sparsity conjuntamente             | PARCIAL                        | within_geo_cv.csv; activity_streaks.csv                               |         1 | CV alto de Channel2 não é decomposto entre zeros e intensidade ativa          | Comparar CV condicional à atividade e regimes de zeros                 |
| D16  | HHI/top geos/concentração                           | COMPLETO                       | channel_geo_concentration.csv; media_geo narrativa                    |         2 | —                                                                             | Manter HHI em escala 0–1 e não como N efetivo                          |
| D17  | Síntese por canal e informação além do nacional     | PARCIAL                        | findings.md; readiness_report.csv                                     |         2 | Resposta correta mas baseada sobretudo em intervalos min–max                  | Integrar todos os diagnósticos em fichas por canal                     |
| E01  | Pearson/Spearman nacional/overall/within            | COMPLETO                       | correlation_*; independent_checks.json                                |         3 | —                                                                             | Manter alinhamento e centragem                                         |
| E02  | Matrizes de mídia e gasto separadas                 | COMPLETO                       | impression_correlation_*; spend_correlation_*                         |         2 | —                                                                             | Manter tabelas; simplificar figuras globais                            |
| E03  | Interpretação comparada de pares e controles        | PARCIAL                        | relatório 05; correlations strongest.head(15)                         |         1 | Maior associação destaca par contábil e não os canais distintos               | Excluir pares do mesmo canal apenas do ranking interpretativo          |
| E04  | VIF com intercepto, constantes e colinearidade      | COMPLETO                       | vif_summary.csv; tests; verificação statsmodels                       |         3 | —                                                                             | Manter conjunto sem KPI nem duplicação spend/media                     |
| E05  | Correlação não causal, confundimento e dependência  | COMPLETO                       | methodology_eda.md; relatórios 05/07                                  |         3 | —                                                                             | Manter ressalvas e ausência de p-valores ingênuos                      |
| E06  | Identificabilidade e implicações específicas        | PARCIAL                        | readiness_report.csv; findings.md                                     |         2 | Alerta geral; falta lista de canais/controles e próximos cuidados             | Mapear diagnósticos a decisões futuras sem exclusão mecânica           |
| F01  | Versão, API e construção InputData                  | COMPLETO                       | official_eda.py; ambiente; upstream consultado                        |         3 | —                                                                             | Manter commit 0211153 e roles confirmados                              |
| F02  | Sem posterior; prior explícita                      | COMPLETO                       | meridian_run.json; assert no código; API oficial                      |         3 | —                                                                             | Manter distinção prior/posterior                                       |
| F03  | HTML oficial e checks executados                    | COMPLETO                       | meridian_eda_report.html; logs de células; 13 checks                  |         3 | —                                                                             | Manter relatório e exportações                                         |
| F04  | Defaults e thresholds documentados                  | PARCIAL                        | docs/decisions.md; upstream eda_spec.py                               |         2 | Defaults preservados, valores dos limiares pouco explícitos no projeto        | Registrar 0,999; VIF 1000; std 1e-4 com escopo e versão                |
| F05  | Reconciliação R² ajustado na mesma escala           | COMPLETO                       | official_r2_reconciliation.csv                                        |         3 | —                                                                             | Preservar excelente comparação numérica                                |
| F06  | Confronto de correlações/VIF/outliers               | PARCIAL                        | custom_vs_meridian.csv                                                |         1 | Seis linhas ficam em comparação de definições, sem confronto de casos/valores | Comparar sinais relevantes, localizações e diferenças de transformação |
| F07  | Data-to-parameter guardrail                         | COMPLETO                       | meridian_data_adequacy.csv; metodologia                               |         3 | —                                                                             | Manter 6240/204 e limitação de interpretação                           |
| F08  | Revisão substantiva dos seis REVIEW                 | PARCIAL                        | meridian_eda_checks.csv; outliers.csv                                 |         1 | CPMU contextualizado, quatro alertas de variabilidade não encerrados por caso | Documentar variável/geo/semana, magnitude e decisão                    |
| G01  | Agregações e receita derivada                       | COMPLETO                       | src/data.py:national; independent_checks.json                         |         3 | —                                                                             | Manter soma de produtos e médias ponderadas documentadas               |
| G02  | Normalizações e domínios de métricas                | COMPLETO                       | 36 verificações independentes                                         |         3 | —                                                                             | Manter checks de somas, R² e correlações                               |
| G03  | CV de índices centrados/negativos                   | PARCIAL                        | national_descriptive.csv; methodology_eda.md                          |         2 | CV exportado para controles com média próxima de zero; texto adverte          | Marcar como não interpretável nas próprias tabelas                     |
| G04  | Linguagem de amplitude de shares                    | PARCIAL                        | src/geo_analysis.py:119; reporting.py:74                              |         2 | Amplitude em fração formatada como percentual                                 | Escrever diferença em pontos percentuais                               |
| H01  | Instalação limpa das dependências                   | COMPLETO                       | install.log; environment.txt                                          |         3 | —                                                                             | Manter commit e registrar ambiente efetivo                             |
| H02  | Testes positivos e negativos                        | COMPLETO                       | pytest.txt:11 passed; testes lidos                                    |         3 | —                                                                             | Acrescentar checks de publicação e ordem visual na futura correção     |
| H03  | Oito notebooks e master em processos novos          | COMPLETO                       | cell_execution.json; execute_cells.py                                 |         3 | —                                                                             | Preservar execução célula a célula; limitação de Jupyter declarada     |
| H04  | Executor nbclient neste ambiente                    | IMPLEMENTADO MAS NÃO EXECUTADO | nbclient_attempt.log                                                  |         0 | Kernel bloqueado antes da primeira célula por sockets                         | Revalidar nbclient em ambiente com IPC/rede local permitida            |
| H05  | Sessão real Google Colab                            | IMPLEMENTADO MAS NÃO EXECUTADO | bootstrap inspecionado; master local executado                        |         0 | Serviço Colab não foi usado                                                   | Executar Run all em sessão nova e guardar evidência                    |
| H06  | Bootstrap fixa ref e origem de Meridian             | PARCIAL                        | notebooks célula 1; build_notebooks.py                                |         2 | Checkout só no clone novo e verificação apenas de versão 2.1.0                | Validar HEAD e direct_url.json, inclusive diretório existente          |
| H07  | Outputs regeneráveis e íntegros                     | PARCIAL                        | artifact_comparison.json; inventory.json                              |         2 | Dois SVGs vazios no commit original                                           | Validar tamanho/XML antes de publicar                                  |
| H08  | Atualidade dos inputs de conclusões                 | PARCIAL                        | 07 célula 3; src/reporting.py:conclusions                             |         2 | Checa existência de CSV, não vínculo com fonte/código                         | Guardar manifesto e hash dos resultados consumidos                     |
| H09  | Logging e warnings                                  | PARCIAL                        | execution.log; meridian_warnings.csv; src/data.py:logging.basicConfig |         2 | Logs sem manifesto do conjunto; warnings de compatibilidade persistem         | Preservar avisos e registrar início/fim/commit por execução            |
| I01  | Pergunta/motivação/método por capítulo              | COMPLETO                       | Markdown dos nove notebooks                                           |         2 | —                                                                             | Manter introduções e ressalvas didáticas                               |
| I02  | Narrativa por análise e figura                      | PARCIAL                        | src/reporting.py:show; notebooks 00–05                                |         1 | Uma célula apresenta todas as figuras sem comentários individuais             | Intercalar resultado/interpretação/limite em blocos menores            |
| I03  | Resultados dinâmicos consistentes                   | COMPLETO                       | f-strings; relatórios regenerados; comparação de artefatos            |         2 | —                                                                             | Manter números calculados; corrigir frase de ordem visual              |
| I04  | Checkpoint substantivo                              | PARCIAL                        | src/reporting.py:result                                               |         1 | Perguntas respondidas com frases genéricas repetidas                          | Escrever descoberta, pendência e decisão específica por capítulo       |
| I05  | Readiness e cinco perguntas                         | PARCIAL                        | readiness_report.csv; findings.md                                     |         2 | Cobertura boa, alertas e responsáveis não viram critérios de avanço           | Adicionar condições verificáveis para liberar modelagem                |
| I06  | Documentação acadêmica e README                     | COMPLETO                       | docs/methodology_eda.md; decisions.md; README                         |         2 | —                                                                             | Preservar equações, fontes e limites; refinar achados                  |
| J01  | Modularidade e organização                          | COMPLETO                       | src,notebooks,scripts,tests,docs                                      |         2 | —                                                                             | Manter separação; sem necessidade de arquitetura adicional             |
| J02  | Truncamento de tabelas no notebook                  | PARCIAL                        | src/reporting.py:40 head(12)                                          |         1 | Omite controles na decomposição e parte dos checks/readiness                  | Mostrar integralmente tabelas pequenas críticas ou resumo selecionado  |
| J03  | Escalas, labels e redundância visual                | PARCIAL                        | plots.py:29–30; inspeção visual de 10 figuras                         |         2 | Nomes/ticks omitidos, legenda sobre barras e datas sobrepostas                | Formatação categórica distinta de datas; legenda externa               |
| J04  | Escopo sem modelagem prematura                      | COMPLETO                       | src completo; meridian_run.json                                       |         3 | —                                                                             | Manter ausência de posterior/ROI/otimização                            |

## 5. Avaliação por notebook

As notas abaixo são avaliações diagnósticas dos capítulos, não pesos adicionais na nota global.

| Notebook | Objetivo esperado e execução observada | Correto e bem feito | Superficial/ausente | Erro e qualidade visual | Interpretação | Nota |
|---|---|---|---|---|---|---:|
| 00 | Auditar estrutura; verifica hash/schema/painel/domínio e CPMU | Contrato forte, missing multidimensional, sem imputação | Dicionário de coordenadas pode ser mais preciso; extremos CPMU ficam para o 06 | Nenhum erro numérico encontrado; completude e missing disponíveis | Boa para início do estudo | 9,0 |
| 01 | Caracterizar KPI/canais; gera descrições, shares, atividade e outliers | Estatísticas e denominadores corretos; preserva observações | Streaks pouco narrados; contextualização de outliers não concluída | Nenhum erro de execução; artefatos existentes não substituem investigação | Explica regras, mas poucos casos concretos | 7,7 |
| 02 | Investigar tempo; séries por canal, STL, ACF, mudanças e controles | Agregação e z-score corretos; STL com ressalva de três ciclos | ACF e STL não recebem leitura factual detalhada; controles pouco discutidos | CPMU com offset microscópico sugere visualmente oscilação maior que a econômica | Picos identificados; tendências/variação dos controles requerem síntese | 7,5 |
| 03 | Heterogeneidade; população, per capita, correlações, decomposições | Melhor núcleo metodológico; two-way e escala per capita | Correlação entre geos sem narrativa de pares/distribuição | Um SVG vazio; datas sobrepostas nos small multiples | Boa explicação de within versus informação adicional | 8,7 |
| 04 | Distribuição territorial; spend, mix, allocation, CV e heatmaps | Fórmulas e HHI corretos, cobertura ampla | Pouca interpretação por canal; intensidade ativa versus zeros não separada | Ordenação per capita muda; um SVG vazio; escala 0–1 do mix esconde diferenças pequenas | Correta em conceitos, insuficiente para profundidade máxima | 7,9 |
| 05 | Relações e identificabilidade; quatro níveis, dois coeficientes e VIF | Cálculos e VIF confirmados; evita duplicar gasto e impressão no VIF | Texto destaca maior par contábil; pouco confronto substantivo entre níveis | Heatmaps cortam nomes e omitem alguns ticks categóricos | Cautela causal excelente; falta dizer quais pares realmente importam | 8,0 |
| 06 | Validação oficial; HTML, checks e reconciliação | API executa, prior explícita, R² reconciliado | Outros confrontos majoritariamente conceituais; REVIEW não encerrados | HTML gerado; sem inspeção interativa de todos os gráficos oficiais | Boa distinção entre escalas; insuficiente revisão de casos | 8,3 |
| 07 | Responder perguntas e decidir prontidão | Síntese dinâmica, limites causais e tabela ampla | Pendências não viram critérios de liberação; head(12) omite parte da tabela | Dashboard útil, mas legenda sobre barras e labels técnicos | Resposta central correta, ainda genérica por canal | 8,0 |
| Master | Executar investigação linear completa | Reutiliza módulos e gera ZIP; passou inteiro | Herda lacunas narrativas e bootstrap de versão/ref | Colab real não testado | Boa estrutura geral; blocos longos de gráficos sem comentários | 8,2 |

## 6. Auditoria estatística

**Agregações.** Conversões, impressões e spend são aditivos nesta base simulada. A receita derivada é soma de produtos, e não produto de somas/médias. Os controles e Promo usam média populacional ponderada como lente declarada, sem presumir unidade econômica conhecida. Verificação independente passou. A escolha descritiva nacional não deve ser automaticamente transplantada para especificação causal.

**Population.** O denominador territorial é `groupby(geo).first()` depois de verificar constância temporal. Não houve soma indevida das 156 réplicas por geo. A população nacional por semana é a soma de 40 geos. Não foi encontrada dupla contagem nos resultados conferidos.

**Per capita.** A escala é por 1.000 habitantes. KPI semanal por geo usa média semanal/população×1.000; gasto acumulado per capita está rotulado como acumulado. As matrizes numéricas são corretas. A operação de alinhamento do pandas muda a ordem de linhas de alguns gráficos — problema de comparabilidade visual, não de denominador ou valor.

**Between/within.** Para cada variável, a implementação calcula momentos com `ddof=0`, peso igual por observação e painel balanceado, com `Vtotal = Vbetween + Vwithin`. As 15 variáveis incluem KPI, cinco mídias, cinco gastos, orgânico, dois controles e Promo. A função rejeita duplicatas, falta de balanceamento e valores não finitos. OLS independente com dummies confirmou os resultados.

**R² GEO e R² TIME.** Correspondem a projeções com intercepto em indicadores de geo ou semana. No painel completo, os subespaços centrados são ortogonais, permitindo a soma de componentes. `R²geo + R²time + resíduo = 1` passou; o resíduo não é automaticamente efeito, informação causal ou interação estimável. R² de variável constante é indefinido, corretamente tratado com NaN.

**Correlações.** Alinhamento temporal e remoção das médias de geo estão corretos. O two-way remove também a média semanal comum. Spearman dos resíduos não é vendido como correlação parcial de postos. Não há p-valores que finjam independência das 6.240 linhas. A ausência de síntese dos pares mais informativos é lacuna interpretativa, não erro da fórmula.

**VIF.** O conjunto contém cinco mídias pagas, orgânico, dois controles e Promo; não contém KPI ou gasto duplicando exposição. Há intercepto e padronização. O cálculo independente de statsmodels coincidiu para overall, within e two-way. Máximos: overall 2,4843; within 2,1117; two-way 1,7994; nacional 3,8573. Não há sinal de redundância linear extrema nesse conjunto bruto, mas adstock/saturação e priors futuros mudam a questão.

**Sparsity.** `media > 0` é definição adequada de atividade. Sequências de zeros/atividade são calculadas por geo e tempo ordenado. Falta converter as sequências em uma avaliação localizada, especialmente Channel2. Um CV alto porque há muitos zeros não significa maior riqueza de intensidade quando a mídia está ativa.

**Outliers.** IQR e MAD são triagens legítimas e não removeram dados. O arquivo contém **6.039 pares observação–variável**, não 6.039 linhas distintas nem 6.039 erros. Há **2.128 sinalizações de Promo**; isso exige contextualizar a natureza do tratamento em vez de chamar toda ocorrência rara de anomalia. A coluna `decision` contém apenas uma frase repetida. “Preservar” é prudente, mas ainda não documenta investigação substantiva.

**Normalizações, geo allocation e media mix.** Fórmulas e somas foram confirmadas independentemente. A maior amplitude de mix é 0,03739 no Channel1, isto é, **3,74 pontos percentuais**, não uma variação relativa de 3,74%. A apresentação em `%` é imprecisa. HHI está na escala 0–1, sem limiares indevidos de concorrência econômica; `1/HHI` não é tratado como tamanho amostral efetivo.

**Inconsistências matemáticas materiais encontradas:** nenhuma nos cálculos centrais examinados. Imprecisões reais: unidade da diferença de shares; CV exportado para índices de média próxima de zero, embora a metodologia advirta contra interpretação; diferença entre ordem visual declarada e executada. A auditoria não declara correção universal para outros datasets.

## 7. Auditoria GEO × TIME × MEDIA

**Resposta: SIM, mas com ressalvas.** Existe evidência forte de variação descritiva no painel que não é recuperada apenas pela série nacional. A força dessa evidência não deve ser confundida com identificabilidade causal, ganho preditivo ou vantagem comprovada de um modelo hierárquico.

| Mídia | R² GEO bruto | R² TIME bruto | Resíduo two-way bruto | Resíduo two-way per capita | Células sem mídia | Mediana CV within |
|---|---:|---:|---:|---:|---:|---:|
| Channel0 | 24,84% | 13,63% | 61,53% | 78,28% | 12,10% | 0,736 |
| Channel1 | 14,41% | 16,79% | 68,80% | 76,52% | 27,92% | 1,013 |
| Channel2 | 5,35% | 16,71% | 77,94% | 79,28% | 64,26% | 1,881 |
| Channel3 | 38,99% | 18,11% | 42,90% | 64,85% | 2,71% | 0,521 |
| Channel4 | 23,72% | 19,07% | 57,20% | 70,58% | 13,14% | 0,759 |

Fonte: `geo_time_r2.csv`, `geo_time_r2_per_capita.csv`, `channel_activity.csv`, `within_geo_cv.csv`. Os valores foram conferidos com raw e OLS independente; essa tabela integra evidências existentes que o projeto deveria comentar canal a canal.

### Tamanho persistente não é a principal diferença após normalização

As correlações Spearman entre população e mídia acumulada variam de **0,9664 a 0,9936**. Depois de normalizar a mídia por população, R² GEO cai para aproximadamente **0,42%–0,59%**, enquanto o resíduo two-way permanece em **64,85%–79,28%**. Portanto, parte substancial das diferenças persistentes de volume acompanha o tamanho dos mercados. A informação adicional mais visível está na execução geo-temporal, não em afirmar que os mercados têm níveis per capita persistentemente muito diferentes.

O projeto faz corretamente a decomposição per capita e alerta que diferenças multiplicativas de tamanho podem produzir resíduo aditivo bruto. Deve preservar esse cuidado. A interpretação final, porém, deveria explicitar a queda do componente GEO, em vez de destacar somente a permanência de um grande resíduo.

### Mix difere pouco em termos absolutos

Os shares por geo variam de 16,70% a 20,00% em Channel0; 12,36% a 16,10% em Channel1; 4,04% a 6,46% em Channel2; 38,00% a 41,36% em Channel3; e 20,56% a 23,92% em Channel4. As diferenças existem, mas não sustentam, sozinhas, uma narrativa de estratégias territoriais radicalmente distintas. No heatmap 0–1, essas diferenças ficam visualmente comprimidas.

Uma síntese melhor diria: os mix acumulados são relativamente semelhantes, a alocação em volume acompanha população, e ainda assim persistem diferenças relevantes no padrão geo-temporal. Isso responde à pergunta científica com mais precisão que “há heterogeneidade” sem qualificação. Não se penaliza a base por apresentar mix parecido; penaliza-se a pouca discussão dessa evidência.

### Channel2 exige uma investigação própria

Channel2 possui **4.010 zeros em 6.240 células**, mas atividade em todos os 40 geos e em 152 de 156 semanas. A proporção ativa por geo varia de **28,21% a 44,23%**. Existem quatro semanas inteiramente sem mídia nacional: **26/04/2021, 25/07/2022, 15/05/2023 e 19/06/2023**. A maior sequência sem atividade em um geo chega a **27 semanas**. Channel3 oferece contraste: 97,29% de células ativas e sequência ativa de até 127 semanas.

Esses números estão disponíveis ou são diretamente deriváveis das tabelas existentes, mas não foram integrados ao storytelling do projeto. A pergunta a aprofundar é quanto do resíduo de Channel2 provém de alternância zero/positivo e quanto de intensidade condicional positiva; também quais geos e janelas têm suporte observacional suficiente. Nada disso autoriza remover o canal ou concluir efeito causal.

### KPI e sincronização geográfica

O KPI bruto tem **67,89% between** e **30,68% de resíduo two-way**. Por habitante, o resíduo chega a **86,11%**. Entre os 780 pares distintos de geos, a correlação temporal de KPI tem mínimo **−0,2151**, mediana **0,0280** e máximo **0,2804**. A matriz sugere baixa sincronização linear, mas o projeto quase não verbaliza esse achado. Isso não prova independência nem justifica inventar clusters.

### Relação com os outros canais e com o futuro MMM

Channel2×Channel3 tem correlação de impressões **0,7003 no nacional**, **0,5036 within** e **0,4511 two-way**. Comparar esses valores é mais útil que destacar gasto×impressões do mesmo canal próximo de 1. O VIF moderado nos sinais examinados ajuda a descartar redundância linear extrema, mas não encerra identificação após transformações nem resolve endogeneidade.

### O que foi demonstrado e o que continua aberto

Foi demonstrado que o painel não se resume a diferenças fixas de tamanho somadas a uma trajetória temporal comum, inclusive após normalização populacional. Os resíduos têm média zero ao agregar sobre geos em cada semana na decomposição, de modo que essa estrutura interna é perdida no agregado. Não se demonstrou que esses resíduos sejam sinal causal recuperável ou que o MMM geo superará o nacional. Essa última pergunta exige uma comparação futura de modelos, com validação temporal comparável e análise de incerteza.

Profundidade global deste bloco: **nível 2 forte**, com componentes de nível 3 nas decomposições. Para atingir nível 3 como investigação completa, faltam os contrastes por canal, a contextualização dos regimes esparsos e a integração explícita de mix, população e relações. Os cálculos adicionais apresentados nesta auditoria servem como evidência das lacunas; não foram incorporados à EDA original.

## 8. Cinco perguntas exploratórias

| Research Question | Status | Evidence | Strength of Evidence | Remaining Gap |
|---|---|---|---|---|
| Estrutura apropriada e qualidade suficiente? | RESPONDIDA quanto à estrutura; ressalva de outliers | 40×156; hash; contrato; 11 testes; sem missing/duplicatas | Alta | Encerrar avaliação de extremos antes de aceitar toda a adequação substantiva |
| KPI/mídia/spend/controles variam no tempo? | PARCIALMENTE RESPONDIDA | Séries, estatísticas, STL, ACF, atividade, R² TIME | Alta para existência; média para caracterização | Narrar mudanças, sazonalidade e controles, sem impor testes formais desnecessários |
| KPI/mídia/investimento diferem entre mercados? | RESPONDIDA descritivamente | Rankings, per capita, população, concentração, mix | Alta | Explicitar quais diferenças somem após normalizar e quão pequeno é o mix |
| Há informação GEO×TIME×MEDIA além do nacional? | RESPONDIDA com ressalvas | Two-way bruto/per capita, CV, atividade, heatmaps, mix/allocation | Alta para variação descritiva; não causal | Aprofundar Channel2 e integrar evidências por canal |
| Há potenciais dificuldades de identificabilidade? | PARCIALMENTE RESPONDIDA | R², VIF, quatro níveis de correlação, checks oficiais | Média/alta para diagnóstico linear | Comparar pares substantivos e transformar pendências em decisões verificáveis |

## 9. Meridian Official EDA

Funcionou na reexecução. O commit oficial fixado **02111531f8661373aa7b6ba31c316c67d72d1dd2** também era o `main` retornado pelo GitHub oficial na consulta desta auditoria, com commit datado de 02/10/2026. Portanto, não foi encontrada divergência entre a versão declarada e o upstream consultado. O código usa `DataFrameInputDataBuilder`, `Meridian`, `ModelSpec()` e `MeridianEDA`, sem chamada de posterior.

O construtor oficial amostra a prior se ela não existe; o default consultado é **500 draws**. A execução usa seed explícita. `meridian_run.json` registra apenas `prior`, 156 knots e max_lag 8. O HTML contém diagnóstico de prior, que não deve ser lido como posterior estimado. A especificação default é provisória.

Os 13 métodos de checagem geraram 16 achados: dois REVIEW de CPMU e quatro REVIEW de extremos/variabilidade em KPI e tratamentos/controles, além de dez INFO. Os artefatos numéricos foram exportados. A razão de adequação é **6240/(39+156+2+7) = 30,5882**, um guardrail, não número efetivo de parâmetros independentes nem prova de identificação.

A reconciliação do R² é particularmente forte: utiliza a escala oficial, ajuste de graus de liberdade e uma fórmula independente do OLS da biblioteca. Em outras famílias, `custom_vs_meridian.csv` registra contagens de severidade e diferenças conceituais, mas não identifica os casos em concordância/divergência. Essa parte é **PARCIAL**.

CPMU tem CV máximo de cerca de **3,475×10⁻⁸**; a hipótese de arredondamento é plausível e corretamente qualificada, não comprovada como causa. Os quatro REVIEW de variabilidade ainda precisam de análise individual dos casos ou grupos. INFO não significa “sem problema”: os defaults do código oficial consultado incluem correlação 0,999, VIF 1000 e limiar de desvio 1e-4 em seus respectivos checks. São guardrails extremos e não critérios universais de boa qualidade. Não houve alteração desses defaults pelo projeto.

Warnings incluem seed global sem efeito no backend JAX e depreciação de `shape(None)`. A API recebe seed explicitamente no sampling; não há evidência, nesta auditoria, de erro numérico por esses avisos. Convém acompanhar compatibilidade futura.

Fontes primárias consultadas:

- [Guia oficial de EDA](https://developers.google.com/meridian/docs/pre-modeling/perform-eda)
- [MeridianEDA no commit utilizado](https://github.com/google/meridian/blob/02111531f8661373aa7b6ba31c316c67d72d1dd2/meridian/model/eda/meridian_eda.py)
- [Configuração dos checks](https://github.com/google/meridian/blob/02111531f8661373aa7b6ba31c316c67d72d1dd2/meridian/model/eda/eda_spec.py)
- [Constantes oficiais](https://github.com/google/meridian/blob/02111531f8661373aa7b6ba31c316c67d72d1dd2/meridian/model/eda/constants.py)
- [Notebook oficial de schema](https://github.com/google/meridian/blob/02111531f8661373aa7b6ba31c316c67d72d1dd2/demo/Meridian_Getting_Started.ipynb)

A documentação atual foi usada para confirmar o fluxo; detalhes de implementação/defaults foram conferidos no código instalado do commit fixado. Não foram presumidos comportamentos de versões não consultadas.

## 10. Reproducibilidade

A aquisição foi verificada por download independente e hash. O raw tem 6.240 linhas e 20 colunas, incluindo o índice exportado; o painel remove apenas esse índice após validá-lo e ordena geo/time. A instalação em venv novo e a reprodução de 88 CSVs reforçam a confiabilidade. Valores de textos dinâmicos também se mantiveram na reexecução; a inconsistência de ordem visual é uma afirmação estática incorreta, não fabricação numérica.

Dois SVGs originais têm zero bytes: `outputs/figures/geo/sentiment_score_control_geo_time.svg` e `outputs/figures/media_geo/Channel3_impression_pc_geo_time.svg`. A cópia de auditoria os regenerou como XML válido. Isso diferencia defeito da publicação e capacidade do código de produzir a figura. A auditoria não substituiu os originais.

O bootstrap define `REPO_REF`, mas só faz checkout quando cria o clone. Se o diretório já existir ou for encontrado entre os pais do cwd, a referência solicitada não é assegurada. A verificação de Meridian usa a string `2.1.0`, que não distingue commits diferentes com a mesma versão. Esses caminhos não comprometem a execução limpa realizada, mas enfraquecem a promessa de reprodução histórica exata. Recomenda-se conferir o SHA e a origem registrada no `direct_url.json`.

O capítulo 07 usa existência de CSVs como sinal de disponibilidade. Não verifica se as tabelas pertencem à mesma versão de código/dados. O master evita esse risco ao regenerar a sequência. Recomenda-se manifesto de execução sem introduzir arquitetura desnecessária.

Dependências transitivas não estão integralmente fixadas no requirements, mas existe registro do ambiente validado; isso é uma limitação de reprodução histórica, não motivo para invalidar uma instalação que passou. Colab real continua **não comprovado**. Há bootstrap plausível, clone e instalação testados separadamente e master local executado; a interface Colab deve receber uma validação própria.

## 11. Storytelling e utilidade acadêmica

Um leitor estatístico iniciante em MMM consegue compreender a sequência e os limites gerais. As introduções explicam pergunta, motivação, método e interpretação; as equações em `methodology_eda.md` são úteis. A separação entre descrição e causalidade está consistentemente preservada.

Ainda assim, o leitor precisa interpretar sozinho muitos gráficos. Nos capítulos 00–05, uma célula principal chama uma função que produz várias análises; `show()` exibe a narrativa geral, depois tabelas e todos os gráficos. Não há interpretação individual suficiente depois dos painéis. A narrativa temporal cita máximo/mínimo e limitações de STL, mas não descreve concretamente o padrão da decomposição ou da ACF. A narrativa de relações destaca o par mais correlacionado, frequentemente gasto/impressões do mesmo canal.

`frame.head(12)` tem efeito didático concreto: a decomposição tem 15 variáveis e os controles/Promo ficam além das primeiras 12; checks e readiness também são truncados. Os CSVs completos existem, portanto não são análises ausentes, mas não aparecem integralmente no fluxo do notebook. Checkpoints como “as evidências numéricas acima respondem” repetem estrutura sem indicar a descoberta específica.

Para o TCC, preservar a estrutura e substituir blocos genéricos por comentários factuais curtos junto às figuras centrais. Não é necessário narrar toda linha de Python. É necessário explicar o achado, sua limitação e a implicação para a futura modelagem.

## 12. O que foi feito muito bem

| Strength | Evidence | Why it matters | Recommendation |
|---|---|---|---|
| Fonte imutável e hash | source.json; load_panel; download independente | Reproduz dados sem alteração silenciosa | Manter |
| Contratos com casos inválidos | 11 testes e require_valid_panel | Detecta erros antes das estatísticas | Manter e adicionar validação de artefatos na correção futura |
| Two-way além de within | statistics.py; metodologia; OLS independente | Evita confundir choques nacionais com informação GEO adicional | Preservar integralmente |
| Comparação bruta/per capita | geo_time_r2_per_capita | Separa escala populacional de dinâmica | Manter e aprofundar interpretação |
| Mix versus allocation | media_mix e geo_allocation; somas verificadas | Responde duas perguntas diferentes sem trocar denominadores | Manter |
| VIF bem especificado | statsmodels independente e testes | Evita duplicação contábil e exclusão mecânica | Manter |
| Cautela científica | Todos os capítulos, metodologia, findings | Não apresenta correlação/volume/share como ROI | Manter |
| EDA oficial realmente executada | HTML, checks, logs, prior-only | API confirmada empiricamente | Manter |
| Reconciliação R² oficial | official_r2_reconciliation | Investiga diferenças de escala/graus de liberdade | Manter como exemplo metodológico |
| Modularidade simples | src, scripts, notebooks | Facilita manutenção e execução em Colab | Refinar funções longas somente onde ajudar a narrativa |

## 13. Problemas encontrados

Não foi identificado P0 nos cálculos/execução desta base. As prioridades abaixo se referem a corrigir a EDA antes de tratá-la como concluída; não são ordens de remover dados ou ajustar posterior.

| Priority | Problem | Evidence | Impact | Required Fix |
|---|---|---|---|---|
| P1 | Quatro REVIEW de variabilidade e extremos sem fechamento substantivo | meridian_eda_checks; outliers; custom_vs_meridian | Adequação dos dados fica condicionada a alertas não investigados | Localizar casos, comparar escalas, registrar magnitude/contexto e decisão; src/official_eda.py e docs/decisions |
| P1 | Outliers recebem decisão genérica única | src/statistics.py:63; 6.039 pares, 2.128 de Promo | Triagem pode confundir tratamento raro, escala e erro | Investigar grupos e casos mais relevantes; documentar preservação sem inventar contexto de negócio |
| P1 | Channel2: sparsity profunda não examinada | activity_runs/streaks; within_geo_cv; quatro semanas nacionais zero | Grande resíduo/CV pode ser lido como riqueza de informação sem avaliar suporte | Cruzar atividade, streaks, geo e intensidade positiva; src/eda.py e geo_analysis.py |
| P1 | Readiness não explicita condições verificáveis de avanço | reporting.conclusions; readiness_report | Próxima fase herda pendências genéricas | Registrar achado→risco→ação→critério de encerramento por canal/controle |
| P2 | Geos reordenados após divisão per capita | geo_analysis.py:88,107; heatmap_order.json | Comparação linha a linha contradiz o texto | Reindexar após a divisão; conferir todos os painéis comparáveis |
| P2 | Dois SVGs publicados vazios | inventory e artifact_comparison | Figuras indisponíveis para leitura/exportação | Regenerar em etapa de correção e validar tamanho/XML antes de publicar |
| P2 | Comparação custom/oficial incompleta fora de R² | custom_vs_meridian | Não demonstra concordância de casos em outros checks | Tabela de casos/valores e justificativas para divergências de escala |
| P2 | Interpretação temporal e controles pouco específica | relatórios 02/05; ACF/STL/controle exportados | Cálculo não vira resposta analítica completa | Discutir padrões concretos, valores, datas e limites |
| P2 | Mix descrito só pela amplitude máxima e unidade imprecisa | media_geo:119 | Diferenças pequenas podem parecer heterogeneidade forte | Usar p.p., dispersão e comparação com tamanho populacional |
| P2 | Correlações sem foco nos pares substantivos | eda.relationships; strongest.head(15) | Redundância contábil ocupa o centro da narrativa | Separar pares do mesmo canal dos canais distintos e comparar níveis |
| P2 | Bootstrap não impõe SHA em diretório existente | notebook célula 1; build_notebooks | REPO_REF pode não representar código executado | Verificar HEAD e commit do pacote; falhar ou orientar ajuste explicitamente |
| P2 | Conclusões aceitam outputs antigos por existência | notebook 07 célula 3 | Mistura de versões pode passar despercebida | Manifesto com hash do raw, commit, ambiente e conclusão das etapas |
| P2 | head(12) oculta partes críticas no fluxo | reporting.py:40 | Leitor deixa de ver controles, alertas e readiness completos | Exibir pequenas tabelas críticas completas ou resumo intencional |
| P2 | Problemas visuais recorrentes | plots.py:29–30; amostra visual | Identificação de variáveis e comparação prejudicadas | Todos os ticks categóricos, nomes claros, datas menos densas e legenda externa |
| P3 | Labels técnicos e metadados de coordenadas | plots; dictionary | Menor acessibilidade acadêmica | Traduzir rótulos e distinguir dimensões de coordenadas |

## 14. Análises que precisam de maior profundidade

| Tema | Estado atual | Por que superficial | Investigar | Pergunta beneficiada |
|---|---|---|---|---|
| Outliers | Detectados e preservados | Não há contextualização individual/grupos | Casos extremos brutos versus escalados, Promo raro, coincidência temporal e decisões | Qualidade para avançar |
| Sparsity Channel2 | Contagens, runs e CV prontos | Narrativa quase só percentual de zeros | Quatro semanas nacionais, geos de menor atividade, longest streaks e intensidade positiva | Informação GEO×TIME útil |
| Population scaling | Correlações e decomposição prontas | Resultado per capita pouco comparado com bruto | Mostrar queda de R² GEO e permanência residual por canal | Tamanho versus execução territorial |
| Mix e allocation | Fórmulas corretas | Apenas máximo da amplitude | Intervalos/dispersão por canal, diferenças em p.p. e semelhanças de mix | Heterogeneidade entre mercados |
| Temporal | STL, ACF e mudanças prontos | Texto não interpreta a maioria dos outputs | Trajetória, volatilidade, datas e sinais sazonais com limite de três anos | Variação temporal relevante |
| Relações/controles | Matrizes extensas | Ranking dominado por pares contábeis | Channel2×3 e controles, nacional→within→two-way | Redundância/identificação |
| GEO sincronização | Matriz 40×40 pronta | Sem síntese factual | Distribuição de correlações e geos/pares extremos | Diferenças de dinâmica |

## 15. Análises adicionais recomendadas

**Necessárias antes do primeiro ajuste ou para encerrar requisitos incompletos:** análise localizada dos REVIEW; aprofundamento de Channel2 motivado pelos 64,26% de zeros; ficha integrada por canal; critérios verificáveis de readiness; correção da ordem visual e da integridade dos arquivos publicados. A maior parte reutiliza tabelas já existentes. Validar uma sessão Colab é necessário antes de afirmar compatibilidade comprovada no serviço.

**Interessantes, mas opcionais:** sensibilidade descritiva retirando temporariamente maiores geos e comparando períodos; decomposição da variação de mídia em atividade versus intensidade positiva; análise da estabilidade temporal das correlações; exploração de concentração do resíduo em poucos geos. A extensão de atividade/intensidade é particularmente útil em Channel2, mas não exige inserir modelo complexo nem altera a base principal. Nenhuma nota foi reduzida por ausência de clustering, testes formais de quebra, testes de estacionariedade, mapas de geos fictícios, posterior, ROI, adstock estimado ou otimização de orçamento.

## 16. Análises ou gráficos redundantes

Os heatmaps de spend e impressões do mesmo canal são quase cópias devido ao CPMU praticamente constante. Devem continuar disponíveis para auditoria, mas o texto principal do TCC pode mostrar um par demonstrativo e deslocar os demais ao apêndice. As correlações globais repetem pares gasto–impressões próximos de 1; priorizar matrizes de preditores e comparações de nível.

Os 20 heatmaps brutos/per capita de mídia paga e gasto têm utilidade de inspeção, mas não devem ser exibidos em sequência sem perguntas e comentários. Selecionar Channel2 e Channel3 como contraste no corpo principal é defensável, mantendo todos os dados. O gráfico de completude totalmente preenchido e o gráfico de missing todo zero comprovam integridade; uma apresentação resumida pode ser suficiente no TCC.

Figuras a preservar: scatter R² GEO×TIME com legenda; decomposição de variância; séries individuais de canal; heatmaps per capita após corrigir ordenação; dashboard após mover legenda. Figuras a refinar: small multiples com datas sobrepostas; matrizes com nomes cortados/ticks omitidos; CPMU com offset de 10⁻⁹ sem explicação na própria figura; heatmap de mix em escala ampla, que deve vir acompanhado de tabela de dispersão ou gráfico de desvios em p.p.

## 17. Readiness para modelagem

**PRONTO COM CORREÇÕES IMPORTANTES.** A estrutura e os cálculos não bloqueiam planejar um baseline. Há variação suficiente para justificar investigar o modelo, sem garantia de recuperação causal. A decisão de ajustar deve incorporar o que ainda não está encerrado:

1. Identificar e justificar os REVIEW de variabilidade e os principais grupos de extremos.
2. Documentar o suporte temporal/geográfico de Channel2 e os cuidados decorrentes.
3. Elaborar síntese por canal/controle que conecte R², população, sparsity, correlações e VIF às hipóteses de especificação.
4. Corrigir integridade de figuras e comparabilidade visual antes de usar os gráficos como evidência no TCC.

DAG/hipóteses causais, seleção fundamentada de controles, priors, knots, max_lag e holdout pertencem à próxima fase. Não são resultados ausentes da EDA nem foram implementados nesta auditoria. Não há exigência de remover canais, geos ou outliers para avançar.

## 18. Scorecard

`Score` está em escala 0–10; `Weighted Score = Weight × Score/10`. A pontuação ponderada foi atribuída primeiro, por dimensão; casas decimais do Score são apenas sua conversão. Avaliação qualitativa com evidências não representa medição objetiva sem julgamento.

| Dimension                 |   Weight |   Score |   Weighted Score | Rationale                                                                                           |
|:--------------------------|---------:|--------:|-----------------:|:----------------------------------------------------------------------------------------------------|
| Data audit                |       10 |    9.00 |             9.00 | Contrato, fonte e aritmética fortes; dicionário e fechamento CPMU incompletos.                      |
| EDA geral/temporal        |       10 |    7.50 |             7.50 | Execução ampla; outliers, streaks, STL/ACF e controles pouco interpretados.                         |
| GEO                       |       15 |    8.00 |            12.00 | População e per capita corretos; sincronização e extremos pouco explorados.                         |
| GEO × TIME × MEDIA        |       20 |    8.25 |            16.50 | Decomposição robusta; falta síntese por canal, ordem visual inconsistente e mix pouco discutido.    |
| Relationships             |       10 |    8.00 |             8.00 | Fórmulas corretas; narrativa prioriza associação contábil e não compara pares substantivos.         |
| Meridian EDA              |        7 |    7.86 |             5.50 | Execução e R² excelentes; contraste de outros checks e fechamento de alertas parciais.              |
| Estatística/interpretação |       10 |    9.00 |             9.00 | Nenhum erro material nos cálculos centrais verificados; imprecisões de unidade e apresentação.      |
| Reprodutibilidade         |        7 |    8.57 |             6.00 | Instalação e processos novos passaram; Colab não comprovado, dois SVGs vazios e bootstrap frágil.   |
| Storytelling              |        6 |    6.67 |             4.00 | Perguntas e limites claros; faltam comentários por figura e checkpoints concretos.                  |
| Engenharia                |        5 |    9.00 |             4.50 | Estrutura enxuta e testes úteis; head(12), cache por existência e labels genéricos limitam entrega. |

**Total = 82,0 / 100. Nota = 8,2 / 10.** Os pesos somam 100. Não foi aplicado cap: os cálculos centrais passaram, o GEO foi investigado e os notebooks executaram por mecanismo alternativo. A restrição ambiental do nbclient não foi classificada como falha do projeto.

## 19. Justificativa detalhada da nota

A nota reconhece a ampla cobertura e, principalmente, a correção verificada. A decomposição two-way, a comparação per capita e a reconciliação oficial merecem crédito alto por enfrentarem riscos conceituais reais. A execução limpa e a equivalência dos CSVs distinguem esta entrega de código apenas escrito. Isso sustenta a faixa “muito boa”.

Os 18 pontos não concedidos refletem lacunas concretas: Data audit 1,0 (dicionário e fechamento dos diagnósticos); geral/temporal 2,5 (interpretação dos extremos, streaks e tempo); GEO 3,0 (pouca investigação da sincronização/extremos); GEO×TIME×MEDIA 3,5 (síntese por canal e comparação visual); relações 2,0 (pares substantivos); oficial 1,5 (confronto e revisão dos alertas); estatística/interpretação 1,0 (unidades e limitações nas tabelas); reprodução 1,0 (artefatos/ref/cache e fronteira Colab); storytelling 2,0 (figuras/checkpoints); engenharia 0,5 (apresentação e verificações de entrega). Não são descontos por ter dados esparsos, outliers ou mix semelhante.

O que impede 10/10 é a distância entre **gerar diagnósticos corretos** e **encerrar uma investigação profunda e legível**. Muitos outputs respondem potencialmente às perguntas, mas ainda não foram interpretados em detalhe. Os exemplos numéricos da seção 7 mostram como aprofundar sem aumentar excessivamente a complexidade.

## 20. Plano de melhoria

1. **Encerrar alertas e extremos.** Produzir tabela de casos/grupos com localização, escala, magnitude, decisão e justificativa. Critério de conclusão: nenhum REVIEW relevante fica apenas com “investigar”.
2. **Aprofundar Channel2.** Registrar atividade por geo, semanas nacionais zero e sequências longas; comparar com Channel3. Critério: explicar o que os zeros significam para a informação disponível, sem inventar calendário de campanhas reais.
3. **Escrever a síntese por canal/controle.** Integrar bruto/per capita, R², residual, CV, mix, correlação e VIF. Critério: cada implicação tem tabela/figura e ressalva específica.
4. **Corrigir ordem e publicação visual.** Reindexar depois de `.div`, regenerar os dois SVGs e validar todos os arquivos. Critério: ordem declarada coincide com eixos e não há SVG vazio/inválido.
5. **Melhorar a leitura dos notebooks.** Dividir os blocos analíticos e comentar as figuras centrais; mostrar tabelas críticas sem corte arbitrário. Critério: leitor entende o achado sem abrir código/CSV para todas as conclusões.
6. **Consolidar reprodução.** Manifesto de outputs, verificação de SHA/ref/pacote e uma execução real no Colab. Critério: versão executada demonstrável e Run all documentado.
7. **Reavaliar prontidão e então especificar o baseline.** Usar os achados para formular escolhas futuras; não selecionar causalidade/adstock pela correlação exploratória.

## 21. Veredito final

**SIM, APÓS CORREÇÕES.** A EDA é suficientemente sólida em estrutura, execução e estatística para sustentar uma boa transição acadêmica à especificação do baseline, desde que os alertas e lacunas interpretativas destacados sejam resolvidos. A evidência de variação adicional no painel é real e reproduzível; não é prova de identificação causal ou superioridade de um MMM geo-level.

Preservar dados, contratos, decomposições, normalizações, VIF, limites causais e reconciliação oficial. Corrigir a ordem dos heatmaps e os arquivos vazios. Aprofundar os resultados que já existem, com prioridade para extremos, Channel2, população/mix e relações entre canais. A auditoria adiciona somente este diagnóstico e suas evidências; não refatora nem corrige a EDA original.
