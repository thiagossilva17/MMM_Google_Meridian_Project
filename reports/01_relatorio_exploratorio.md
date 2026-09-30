# TCC — Análise exploratória do Google Meridian

Análise realizada em 30/09/2026 a partir dos quatro documentos do TCC e dos CSVs oficiais no commit `58ea51bb6225717fce55949ae02708308ce0e090`. O notebook foi executado localmente, preservando resultados, tabelas e gráficos. Não houve ajuste de MMM nesta etapa.

## Objetivo e escolha da base

O objetivo do TCC é demonstrar e avaliar criticamente um MMM Bayesiano hierárquico, incluindo sensibilidade às priors, contribuição incremental e alocação. A base principal é `geo_all_channels.csv`, do exemplo completo do Meridian: ela acrescenta mídia orgânica e promoções, permitindo uma análise mais abrangente que o exemplo somente com mídia paga.

| Arquivo | Regiões | Semanas | Linhas | Conteúdo |
|---|---:|---:|---:|---|
| geo_all_channels.csv | 40 | 156 | 6.240 | 5 canais pagos, 1 orgânico, 2 controles e promoção |
| geo_media.csv | 20 | 156 | 3.120 | 4 canais pagos e 2 controles |
| geo_media_rf.csv | 20 | 156 | 3.120 | 4 canais pagos; Channel3 também tem alcance/frequência |

Todos cobrem 25/01/2021–15/01/2024, em semanas de sete dias. São simulações diferentes: os KPIs, populações e exposições diferem; os arquivos não devem ser unidos pelas chaves compartilhadas como se pertencessem ao mesmo cenário.

## O que uma linha contém

Uma linha é uma região em uma semana. Na base completa há 20 colunas brutas; `Unnamed: 0` é o índice exportado e pode ser removido, restando 19 variáveis úteis.

| Variável | Interpretação | Uso futuro |
|---|---|---|
| geo e time | Região sintética e semana | Coordenadas do painel |
| conversions | KPI sintético não monetário | Variável resposta |
| revenue_per_conversion | Valor sintético por unidade do KPI | Receita incremental e ROI |
| population | Escala regional, constante no período | Escalonamento e comparação regional |
| Channel0–4_impression | Exposição paga por canal | Adstock e saturação na modelagem |
| Channel0–4_spend | Gasto pago por canal | ROI e orçamento; não duplicar a exposição como regressora |
| Organic_channel0_impression | Exposição orgânica, sem gasto informado | Efeito da mídia orgânica |
| competitor_sales_control | Escore sintético de concorrência | Controle, sujeito à justificativa causal |
| sentiment_score_control | Escore sintético de sentimento | Controle, sujeito à justificativa causal |
| Promo | Intensidade contínua de promoção | Tratamento não mídia |

Os controles admitem valores negativos e não representam literalmente vendas negativas. Promo varia continuamente e é zero em 2.922 registros (46,83%); não converter automaticamente em flag binária. Os canais não possuem nomes de plataformas: não há evidência de que Channel0 represente Search, por exemplo. A documentação mostra GQV em exemplos, mas o CSV fixado não contém essa variável.

A receita observada sintética deve ser calculada por linha: `conversions * revenue_per_conversion`. Seu total é aproximadamente 1,319 bilhão de unidades monetárias sintéticas; o gasto total é 219,492 milhões. Não há identificação de moeda no CSV. A razão desses totais não é ROI incremental: inclui o resultado de baseline e de outros fatores.

## Auditoria e limites de realismo

Os três painéis são completos, sem nulos, chaves duplicadas, intervalos irregulares ou valores não finitos. Não há valores negativos fora dos controles. População é positiva e constante dentro de cada região. Os zeros de exposição e gasto coincidem em todos os canais pagos da base principal.

Cerca de 25,08% das conversões da base completa são fracionárias. O KPI semanal por habitante varia de 2,42 a 44,13. Portanto, esses números não devem ser tratados como contagem de pessoas únicas ou taxa de conversão individual. São valores de uma simulação destinada a demonstrar a estrutura do modelo. A boa qualidade formal da tabela não equivale a realismo de negócio.

Não há pré-histórico de exposição anterior ao primeiro KPI no CSV. A influência da inicialização do carryover precisará ser considerada na modelagem. Extremos IQR foram contabilizados, mas preservados: uma campanha intensa ou uma região grande não deve ser descartada apenas por uma regra estatística.

## Mix de investimento e custo

| Canal | Gasto total (milhões de unidades sintéticas) | Participação | Semanas-regionais com exposição zero | CPM ponderado |
|---|---:|---:|---:|---:|
| Channel0 | 40,502 | 18,45% | 12,10% | 7,33 |
| Channel1 | 31,320 | 14,27% | 27,92% | 9,64 |
| Channel2 | 12,079 | 5,50% | 64,26% | 7,43 |
| Channel3 | 87,860 | 40,03% | 2,71% | 7,79 |
| Channel4 | 47,731 | 21,75% | 13,14% | 7,79 |

Channel3 recebe mais investimento; isso não demonstra que possua maior eficiência. Channel2 tem muitas pausas, importante para avaliar suporte e o contraste entre exposições baixas e altas. Os zeros não constituem, por si só, um experimento: a decisão de desligar um canal pode estar relacionada à demanda.

Em cada canal, gasto e impressões são praticamente proporcionais: correlação ≈ 1 e coeficiente de variação do CPM ativo ≈ 3×10⁻⁸. É uma simplificação da simulação. O CPM mede custo por mil impressões, não resultado de marketing. O estudo não poderá investigar mudanças reais de preço de leilão a partir desses arquivos.

## O principal achado: correlação muda com a escala regional

| Canal | Correlação bruta exposição × KPI | Correlação por habitante | Dentro de região, por habitante |
|---|---:|---:|---:|
| Channel0 | 0,414 | 0,024 | 0,023 |
| Channel1 | 0,293 | −0,027 | −0,025 |
| Channel2 | 0,148 | −0,090 | −0,093 |
| Channel3 | 0,469 | −0,103 | −0,103 |
| Channel4 | 0,348 | −0,119 | −0,125 |

A associação positiva bruta enfraquece ou muda de sinal quando comparamos exposição e KPI por habitante. Isso é compatível com uma influência importante do tamanho regional nas correlações brutas. Não demonstra efeito negativo da publicidade, nem prova que tamanho seja o único confundidor.

Didaticamente: uma região maior pode ter mais impressões e conversões apenas porque tem mais população. O modelo precisa separar escala, diferenças persistentes entre regiões, variações temporais, controles e tratamentos. A EDA não consegue substituir essa decomposição causal.

O notebook acrescenta Pearson, Spearman, correlações nacionais, remoção descritiva de efeitos de região/semana e correlações defasadas de 0 a 8 semanas, sempre com shift dentro de região. As correlações defasadas não estimam retenção do adstock.

Os VIFs das exposições por habitante, orgânico, controles e Promo variam de 1,23 a 2,60. Nessa especificação exploratória não aparece dependência linear extrema entre essas entradas. Isso não garante que parâmetros de adstock/Hill e contribuições sejam identificáveis. Não incluímos gastos e impressões juntos nesse cálculo, porque são redundantes dentro de canal.

## Tempo, geografia e suporte de resposta

Foram produzidos gráficos de séries semanais, índice base 100, mudanças semanais, perfil mensal, autocorrelação, painel geo-temporal e comparação entre regiões por habitante. O perfil mensal é exploratório: três anos não demonstram sazonalidade estável. Os CSVs de resultados permitem examinar cada região e cada semana.

Os gráficos de dose em quantis não mostram uma curva causal de saturação. Alguns canais apresentam associação observacional decrescente por habitante. Isso exige investigação e modelagem, e não a interpretação de que aumentar anúncios reduz vendas. A identificação de saturação requer lidar com adstock, controles, calendário, heterogeneidade e suporte de exposição, além de analisar a posterior.

A comparação de semanas com Promo positiva e zero também é descritiva. Se promoções são escolhidas em semanas de baixa demanda, a diferença de médias pode ser enganosa. Mídia orgânica pode ser modelada, mas o arquivo não fornece custo que permita calcular seu ROI diretamente.

## Alcance e frequência no cenário separado

Em `geo_media_rf.csv`, Channel3 satisfaz `impressões ≈ alcance × frequência`: o erro relativo máximo nas linhas ativas é aproximadamente 1,02×10⁻⁷, compatível com arredondamento numérico. Não há alcance maior que população, frequência negativa ou inconsistência entre zeros de alcance e frequência.

Esse cenário permite estudar frequência como exposição repetida entre pessoas alcançadas. Na carga do Meridian, Channel3 deve ser incluído pelo grupo reach/frequency/rf_spend, sem duplicá-lo como canal por impressões. Não somar alcance de várias semanas como se fosse alcance único total; frequência agregada deve ser ponderada pelo alcance.

## Quais perguntas do TCC podem ser respondidas

| Grupo de perguntas | EDA atual | Etapa necessária |
|---|---|---|
| Estrutura geo-temporal, qualidade, custos e distribuição de mídia | Responde descritivamente | Auditoria documentada |
| Diferenças entre regiões e padrões temporais | Mostra heterogeneidade e associações | MMM para efeitos e partial pooling |
| Correlação versus causalidade | Mostra por que correlação bruta pode enganar | DAG e hipóteses de identificação |
| Contribuição incremental, ROI e incerteza | Não estima | Posterior de MMM e contrafactuais |
| Adstock e saturação | Examina suporte e defasagens | Estimar transformações e parâmetros |
| Priors, posterior e shrinkage | Define desenho de estudo | Rodadas Bayesiana e sensibilidade |
| Convergência MCMC | Não se aplica ainda | R-hat, ESS, divergências e mistura |
| Melhor orçamento, mROI e frequência ótima | Não recomenda | Curvas posteriores e otimização restrita |
| Validade preditiva | Propõe holdout | Ajuste e posterior predictive checks |
| Recuperação da verdade e generalização real | CSV isolado não permite | Gerador e verdade conhecida; dados reais externos |

A proposta de holdout reserva as últimas 26 semanas, a partir de 24/07/2023: 5.200 observações de treino e 1.040 de teste. O recorte é comum a todas as regiões; não embaralha semanas. Transformações aprendidas e decisões orientadas pelos dados devem usar treino; mantenha histórico de mídia para calcular carryover no teste. O arquivo de máscara é ordenado por geo e time para evitar desalinhamento.

## Revisões conceituais dos documentos

A introdução delimita corretamente o uso de dados sintéticos. Recomenda-se trocar afirmações absolutas, como “padrão-ouro” e garantias de maior estabilidade, por vantagens condicionais às hipóteses e ao desenho de avaliação. Modelos lineares não pressupõem necessariamente independência entre regressores; a dificuldade com canais correlacionados é separação de efeitos e identificação, não uma proibição geral de correlação.

Na função Hill, o parâmetro de meia-saturação produz H(x)=0,5; não é, em geral, o ponto de inflexão. A recursão didática do adstock não deve ser apresentada como transformação exata do Meridian sem conferir janela, pesos, normalização e ordem de Hill/adstock. Use símbolos distintos para retenção e inclinação de Hill para evitar ambiguidade.

Mais geos ampliam a informação potencial, mas não tornam todas as linhas independentes e não resolvem confundimento automaticamente. Bayes quantifica incerteza condicional ao modelo; posterior estreita não elimina erro de especificação. Bom desempenho de holdout não prova causalidade.

Na modelagem futura, especifique ROI na convenção de receita incremental/gasto, distinta de lucro líquido. Não identifique Paid Search sem metadados. A lista de referências foi lida para compreender o desenho; não constitui verificação bibliográfica independente dos trabalhos citados.

## Reprodutibilidade e continuidade

O notebook inclui saídas executadas, 12 gráficos e tabelas CSV. Fixamos URLs por commit e SHA-256 dos três CSVs; a remoção do índice exportado está documentada. Os arquivos de dados brutos são baixados pelo próprio notebook e não são necessários no repositório.

Para rodar no Colab, abra o notebook e use “Executar tudo”. A EDA não exige GPU nem instalação do Meridian. Para rodar localmente, instale requirements.txt e execute `python src/eda_meridian.py` na raiz do projeto. Os outputs vão para reports/eda. Esta etapa foi executada em ambiente Python local; a execução no Colab ainda será feita pelo usuário.

Fontes primárias:
- https://github.com/google/meridian/tree/58ea51bb6225717fce55949ae02708308ce0e090/meridian/data/simulated_data/csv
- https://developers.google.com/meridian/docs/user-guide/load-geo-data-with-organic-and-non-media
- https://developers.google.com/meridian/docs/user-guide/load-geo-data-with-rf
- https://developers.google.com/meridian/docs/user-guide/load-geo-data-without-rf
