# MMM Google Meridian — TCC

Projeto reprodutível de análise e avaliação de Marketing Mix Modeling Bayesiano com dados sintéticos oficiais do Google Meridian.

## Etapa 1 concluída: análise exploratória

[Abrir no Google Colab](https://colab.research.google.com/github/thiagossilva17/MMM_Google_Meridian_Project/blob/main/notebooks/01_eda_meridian.ipynb)

- [Notebook executado e comentado](notebooks/01_eda_meridian.ipynb)
- [Relatório didático e interpretação dos resultados](reports/01_relatorio_exploratorio.md)
- [Script Python equivalente](src/eda_meridian.py)
- [Tabelas e proveniência](reports/eda)

A base principal é geo_all_channels.csv (40 geos × 156 semanas), com comparação dos cenários geo_media e geo_media_rf. O notebook baixa os CSVs oficiais de um commit fixado; não exige instalação do Meridian nem GPU.

## Execução

No Colab, abra o link acima e execute todas as células. Saídas são salvas em reports/eda no diretório criado pelo notebook. Para preservá-las após a sessão do Colab, baixe os arquivos gerados.

Localmente, na raiz do repositório:

```bash
python -m pip install -r requirements.txt
python src/eda_meridian.py
```

## Escopo e próximos passos

A EDA audita o painel, descreve investimentos, custos, tempo, geografia, correlações, promoções, orgânico e alcance/frequência. Não produz ROI causal nem recomenda orçamento. Próximas etapas: DAG, ingestão no Meridian, priors e sensibilidade, MCMC, holdout, contribuição com incerteza, curvas de resposta e otimização.

Dados sintéticos não fornecem evidência de retorno para uma empresa real. Os documentos originais do TCC não foram publicados neste repositório; o código e o relatório incorporam seu objetivo metodológico.

Fonte: [Google Meridian](https://github.com/google/meridian), commit `58ea51bb6225717fce55949ae02708308ce0e090`. Ver reports/eda/provenance.json para URLs, checksums e versões da execução.
