# Registro de decisões

| Problema / evidência | Alternativas | Decisão e justificativa | Impacto |
|---|---|---|---|
| Repositório continha apenas README vazio; sobrescrita autorizada | Adaptar estrutura antiga ou reconstruir | Construir estrutura da especificação, preservando histórico Git | Entrega rastreável em novo commit |
| Exemplo oficial contém dados simulados | Narrar como mercado real ou estudo metodológico | Identificar simulação em todos os capítulos | Não generalizar conclusões para empresas/canais reais |
| API upstream pode mudar | Instalar main móvel ou fixar commit | Fixar código e CSV no commit 0211153… | Reproduzir schema e checks; versões transitivas registradas |
| CSV inclui Unnamed: 0 | Excluir automaticamente ou verificar | Validar sequência 0…N−1 e remover só da cópia processada | Raw permanece intacto |
| População difere por geo | Usar volume bruto apenas ou comparar intensidades | Exibir bruto e por 1.000 habitantes | Separar escala de execução territorial |
| Within contém efeitos temporais nacionais | Usar só between/within ou incluir two-way | Adicionar R² conjunto e resíduo geo–tempo | Evitar exagerar a informação adicional do painel |
| Controles sintéticos têm escala sem unidade de negócio garantida | Somar ou ponderar | Média ponderada por população para descrição nacional | Não interpretar como totais reais de vendas de concorrentes |
| Zero impressões torna CPMU indefinido | Preencher zero ou manter NaN | Manter NaN e contar inconsistências | Ausência de atividade não vira custo zero |
| Outliers podem refletir escala e sparsity | Remover ou preservar | Preservar; registrar IQR/MAD e geos/datas | Nenhuma limpeza para obter resultados mais favoráveis |
| API atual gera prior no construtor de MeridianEDA | Omitir HTML completo ou aceitar diagnóstico de prior | Executar recurso oficial, documentando seed e defaults | Nenhum posterior, ROI estimado ou MCMC |
| Modelo precisa de spec para EDA oficial | Escolher hiperparâmetros prematuramente ou usar defaults | Defaults provisórios, sem alterar thresholds oficiais | Knots/lag/priors serão revistos na modelagem |
| R² oficiais são ajustados e transformados | Comparar diretamente ou reconciliar | Recalcular na mesma escala com ajuste de graus de liberdade | Comparação numérica com tolerância 1e-5 |
| Gasto e impressões podem ser quase proporcionais | VIF com ambos ou representar exposição uma vez | VIF usa impressões, orgânico, controles e Promo; gasto tem matrizes próprias | Evita redundância contábil por construção |
| Artefatos xarray escalares não têm índice | Ignorar ou converter explicitamente | Exportar escalares como tabela de uma linha | Preserva resultados oficiais sem perder checks |
| Colab é transitório | Depender de arquivos locais ou bootstrap | Clone público, instalação inicial, raw versionado e ZIP de resultados | Execução em runtime novo sem credenciais privadas |

Nenhuma observação, canal ou geo foi excluído por desempenho estatístico. Nenhum threshold oficial foi modificado. Critérios IQR/MAD, STL 52, média móvel 13 e lags 0–8 são escolhas exploratórias explícitas, não parâmetros finais do MMM.
