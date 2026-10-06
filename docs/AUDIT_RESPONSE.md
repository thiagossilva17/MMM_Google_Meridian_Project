# Resposta à auditoria independente

Revisão de 06/10/2026, baseada no relatório publicado no commit `ac9960a3a86e7af07a507121043c6914fcbc4195`, que avaliou `c301905`. O relatório e seus artefatos em `outputs/audit/` foram preservados. Esta resposta não altera a nota independente nem atribui nova nota.

## Tratamento dos pontos da seção 13

CSV sem prefixo refere-se a `outputs/tables/`. Os resultados são calculados na execução, não preenchidos manualmente.

| Prioridade / ponto | Alteração e evidência | Situação |
|---|---|---|
| P1 — quatro REVIEW de variabilidade/extremos | `official_outlier_cases`, `official_outlier_selected_cases`, `official_outlier_reconciliation`: valores brutos/escalados, limites e comparação de todas as chaves GEO–variável–semana. `official_review_resolution` contém risco, decisão e limite residual. | Revisão descritiva encerrada; severidade REVIEW preservada |
| P1 — extremos sem contextualização | `outlier_group_review`, `outlier_case_review`, `outlier_case_windows`, `outlier_coincidence`: IQR bruto/per capita/dentro do geo, posição local, até três maiores casos por variável e janela ±2 semanas. Promo contínuo com massa em zero, não binário. | Implementado; dados simulados preservados com justificativa |
| P1 — Channel2 esparso | `activity_support_by_geo`, `activity_intensity_summary`, `national_zero_media_weeks`: atividade por geo, sequências, cobertura mínima em 13 semanas, contraste Channel3 e decomposição atividade/intensidade. | Implementado |
| P1 — prontidão genérica | `channel_integrated_review`, `control_relationship_review`, `readiness_actions` e `docs/channel_review.md`; cada ação traz risco, responsável, evidência e critério. | EDA documentada; decisões causais reservadas à próxima fase |
| P2 — ordem per capita | Reindexação após divisão; teste com índice não ordenado e comparação de eixos no gate. | Corrigido |
| P2 — SVGs vazios | Gravação atômica, tamanho mínimo, XML/conteúdo gráfico; regeneração completa e `artifact_validation.json`. | Gate obrigatório antes da publicação |
| P2 — custom versus oficial | Correlação/VIF reconciliados na mesma escala; igualdade das localizações de IQR; `custom_official_scale_comparison` quantifica diferenças; CPMU tem casos e desvio relativo. | Implementado; definições distintas explicitadas |
| P2 — tempo/controles | `temporal_interpretation`, `control_detailed_profile`: tendência STL, forças descritivas, ACF 1/13/52, datas e mudanças de cada controle; revisão no capítulo 05. | Implementado com limite de três ciclos |
| P2 — mix/população | `channel_geo_interpretation`, `mix_deviations_pp.svg`: amplitude/desvio em p.p., população versus volume/intensidade, R² bruto/per capita e resíduo por canal. | Corrigido e aprofundado |
| P2 — pares substantivos | `substantive_pair_comparison`, `predictor_kpi_comparison`; Channel2 × Channel3 entre níveis; excluir redundância contábil da síntese. | Implementado |
| P2 — bootstrap/ref | HEAD conferido contra REPO_REF resolvido; URL/SHA de `direct_url.json` do Meridian verificados. Divergência interrompe sem apagar trabalho existente. | Implementado |
| P2 — outputs antigos | Manifesto com status/timestamps, commit, alterações locais, hash do raw/código, versões/origem do pacote e hashes de saídas. | Implementado; conclusões rejeitam incompatibilidade |
| P2 — head(12) | Tabelas até 50 linhas completas; tabelas grandes identificadas como amostra, com sínteses selecionadas e CSV integral. | Corrigido |
| P2 — problemas visuais | Todos os ticks categóricos, nomes completos, datas anuais, CPMU sem ampliar ruído e legenda externa; heatmaps repetitivos em apêndice. | Implementado e inspecionado por amostra |
| P3 — rótulos/coordenadas | Dicionário distingue coordenadas GEO/tempo de medidas e pares mídia/gasto. CV não interpretável de índices centrados explicitado nos CSVs. | Corrigido |

## Decisões e limites

A revisão não transforma REVIEW em INFO. Preservar extremos neste exemplo simulado é uma decisão descritiva: domínio válido, localização e comparação de escalas não certificam plausibilidade comercial nem ausência de influência no futuro ajuste. Casos de CPMU têm magnitude relativa microscópica, compatível com precisão de exportação, sem provar sua causa. Nenhum threshold foi alterado.

A identidade atividade/intensidade descreve a variância **within** de mídia não negativa; não decompõe o resíduo two-way nem estima efeito. O suporte de Channel2 deve orientar o desenho de janelas de treino/holdout, sem excluir mecanicamente o canal.

A agregação nacional oficial de controles/Promo soma valores por padrão; a própria usa média ponderada por população. Por isso diferenças entre escalas são esperadas. Na mesma escala oficial, correlação/VIF devem concordar em 10⁻⁵ e as localizações IQR devem coincidir exatamente; divergência interrompe a execução.

## Escopo e pendência externa

A extensão opcional atividade/intensidade foi incluída por responder diretamente à dúvida sobre Channel2. Sensibilidade por subperíodos/exclusão temporária de geos e estabilidade temporal de correlações continuam opções futuras, não requisitos faltantes desta EDA. Não foram acrescentados posterior, clustering, mapas fictícios ou seleção causal por correlação.

**Colab real continua pendente externa.** A execução local das células não demonstra funcionamento do serviço/frontend. `COLAB_VALIDATION.md` documenta o procedimento e o critério de encerramento. Resultados efetivos de validação desta cópia estão em `docs/validation.md` e `outputs/logs/`; a revisão foi reconstruída após restauração do ambiente, e testes anteriores não foram presumidos válidos para ela.
