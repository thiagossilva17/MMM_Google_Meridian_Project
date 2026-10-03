# Cobertura da especificação

| Bloco da especificação | Implementação | Evidência |
|---|---|---|
| 1–9: escopo, fonte, reprodução, Colab, organização e narrativa | config/data, bootstrap de todos os notebooks, metodologia | source.json, execution.json, capítulos 00–07 |
| 10–17: aquisição, schema, dimensões, chave, missing, domínio, CPMU, testes | data.py, validation.py, data_audit | data_dictionary, data_audit, missing*, duplicate_summary, cost_per_media_unit; testes |
| 18–23: macro, canais, share, sparsity, extremos | eda.general | national_descriptive, channel_summary, spend_share, channel_activity, activity_runs, outliers |
| 24–28: tendência, mídia, KPI e controles no tempo | eda.temporal | national_timeseries, national_cpmu, kpi_stl_52, kpi_level_changes, kpi_acf, control_temporal_summary |
| 29–37: tamanho, população, intensidade, sincronização, within/between e R² | geo_analysis.geo_analysis, statistics.variance_decomposition | geo_kpi_summary, population_summary, geo_plot_selection, geo_kpi_correlation, within_between_variance, geo_time_r2, geo_time_r2_per_capita |
| 38–46: mix, alocação, população, heatmaps, CV e concentração | geo_analysis.media_geo | geo_media_summary, media_mix, geo_allocation, population_media_correlation, within_geo_cv, channel_geo_concentration, geo_cpmu |
| 47–53: correlações, controles, VIF e lags | eda.relationships | correlation_summary, matrizes por nível/método, vif_summary, exploratory_lags |
| 54–59: EDA oficial, HTML, checks, adequação, confronto | official_eda.py | meridian_eda_report.html, meridian_eda_checks, meridian_data_adequacy, custom_vs_meridian, official_r2_reconciliation, official_* |
| 60–68: síntese, readiness, cinco perguntas e limites | reporting.conclusions | readiness_report, findings.md, eda_story.md |
| 69–77: figuras, tabelas, documentação, README, master e qualidade | plots.py, scripts/build_notebooks.py | SVG/PNG, 9 notebooks, metodologia, dicionário, decisões |
| 78–89: problemas preservados, logs, checkpoints, execução e auditoria | módulos, scripts/execute_notebooks.py e testes | meridian_warnings, logs, validation.md |
| 90: entrega | README e mensagem final | Links para master, achados e commit |

## 23 famílias de figuras obrigatórias

1. `data_audit/panel_completeness.svg`
2. `general/national_kpi.svg`
3. `general/kpi_distribution.svg`
4. `general/spend_share.svg`
5. `temporal/Channel*_timeseries.svg`
6. `general/channel_activity.svg` (fração zero = 1 − atividade; contagens em CSV)
7. `geo/kpi_by_geo.svg`
8. `geo/population_by_geo.svg`
9. `geo/population_kpi.svg`
10. `geo/kpi_per_capita.svg`
11. `geo/kpi_small_multiples.svg`
12. `geo/geo_correlation.svg`
13. `geo/variance_decomposition.svg`
14. `geo/geo_time_r2.svg`
15. `media_geo/spend_geo_channel.svg`
16. `media_geo/media_mix.svg`
17. `media_geo/geo_allocation.svg`
18. `media_geo/Channel*_impression_geo_time.svg`
19. `media_geo/Channel*_population.svg`
20. `relationships/correlation_overall.svg` (mídias e demais variáveis; matrizes exclusivas por mídia/gasto em CSV)
21. `relationships/correlation_within.svg`
22. `relationships/vif.svg`
23. `relationships/readiness_dashboard.svg`

Além dessas famílias, há painéis por habitante, controles, gasto, lags, CV e concentração. Não há mapas cartográficos: os geos são fictícios sem geometria documentada.
