# TCC — Marketing Mix Modeling com Google Meridian

EDA completa, com foco em **GEO × TEMPO × MÍDIA**, construída para preparar um estudo de MMM hierárquico. Esta fase descreve os dados, investiga sua qualidade e variação e compara os resultados com a ferramenta oficial. **Não estima posterior, ROI ou contribuição incremental.**

[Abrir o notebook completo no Google Colab](https://colab.research.google.com/github/thiagossilva17/MMM_Google_Meridian_Project/blob/main/notebooks/EDA_COMPLETE_COLAB.ipynb)

## Comece aqui

Para compreender cada análise e interpretar os resultados, consulte o [Guia didático completo da EDA](docs/EDA_DIDACTIC_GUIDE.md).

1. Abra o master no link acima e use um runtime novo de CPU com Python 3.12+.
2. Execute a primeira célula para obter o repositório e instalar as dependências. Não são necessárias credenciais privadas.
3. Execute as células em ordem. Leia a pergunta e o método antes de observar os resultados de cada capítulo.
4. Consulte `docs/findings.md` e `outputs/tables/readiness_report.csv` para a síntese.
5. Ao final, a célula de exportação cria `EDA_RESULTS.zip`. Descomente o download se quiser guardar os resultados do Colab.

Se você copiar as células para um notebook vazio, copie também a célula inicial de bootstrap. O código reutilizável é obtido de `src/` pelo clone. A execução não depende de arquivos desta máquina. Se já havia outras versões científicas importadas na sessão Colab, reinicie-a após instalar as dependências.

## Dados e resultados principais

Fonte: `geo_all_channels.csv`, exemplo **simulado** do Google Meridian, congelado no commit `02111531f8661373aa7b6ba31c316c67d72d1dd2`. SHA-256, URL, licença e versões estão em `data/metadata/`.

- 40 geos fictícios, 156 semanas, 6.240 linhas; 25/01/2021 a 15/01/2024.
- Painel completo e regular, sem nulos ou duplicatas na chave geo–tempo.
- Cinco canais pagos, uma mídia orgânica, dois controles e Promo. Não há reach/frequency.
- Channel2 tem 64,3% das células sem mídia; Channel3 concentra 40,0% do gasto. Isso não mede retorno.
- Após retirar efeitos aditivos de geo e semana, resta 42,9%–77,9% da variância bruta das mídias pagas; por habitante, 64,8%–79,3%.
- Os 13 checks de dados oficiais exportados produziram 10 achados INFO e 6 REVIEW. O HTML completo inclui também diagnósticos de prior.
- R² ajustados foram reconciliados numericamente na mesma escala oficial, com diferença máxima inferior a 10⁻¹⁵.

Há variação geo-temporal potencialmente informativa, mas isso **não prova identificação causal nem superioridade do MMM geo-level**. Channel0–4 não são nomes de plataformas reais, e os dados não descrevem uma empresa real. Consulte as ressalvas e evidências completas em [docs/findings.md](docs/findings.md).

## Organização

| Pasta / arquivo | Conteúdo |
|---|---|
| `data/raw/` | CSV original imutável |
| `data/processed/` | Painel ordenado com data validada; sem índice de exportação |
| `data/metadata/` | Fonte, hash, licença, versões e especificação provisória oficial |
| `src/` | Funções de aquisição, contratos, estatística, EDA, gráficos e relatórios |
| `notebooks/` | Oito capítulos e master Colab, com resultados textuais executados |
| `outputs/figures/` | Figuras vetoriais SVG; PNGs também são gerados ao executar |
| `outputs/tables/` | Tabelas CSV completas, incluindo artefatos oficiais |
| `outputs/reports/` | Relatórios de capítulos e HTML oficial do Meridian |
| `outputs/logs/` | Evidências de execução e validação |
| `docs/` | Metodologia, dicionário, decisões, narrativa, achados e cobertura |
| `tests/` | Contratos de dados e verificações de propriedades estatísticas |
| `scripts/` | CLI de execução e geração/validação dos notebooks |

## Ordem dos notebooks

| Ordem | Notebook | Pergunta |
|---|---|---|
| 00 | [Auditoria](notebooks/00_data_audit.ipynb) | O que recebemos e a estrutura é válida? |
| 01 | [Geral](notebooks/01_eda_general.ipynb) | Qual é a escala, distribuição e atividade? |
| 02 | [Temporal](notebooks/02_eda_temporal.ipynb) | Como os sinais mudam ao longo do tempo? |
| 03 | [GEO](notebooks/03_eda_geo.ipynb) | Diferenças territoriais vão além da população? |
| 04 | [Mídia × GEO](notebooks/04_eda_media_geo.ipynb) | Como o orçamento e a mídia são distribuídos? |
| 05 | [Relações](notebooks/05_eda_relationships.ipynb) | Quais sinais são sincronizados ou redundantes? |
| 06 | [EDA oficial](notebooks/06_meridian_official_eda.ipynb) | A ferramenta oficial encontra os mesmos padrões? |
| 07 | [Conclusões](notebooks/07_eda_conclusions.ipynb) | O que permite avançar e o que continua incerto? |
| Completo | [Master Colab](notebooks/EDA_COMPLETE_COLAB.ipynb) | Sequência completa do início ao fim |

Os modulares verificam etapas anteriores por manifesto de conteúdo/ambiente e recalculam resultados ausentes, alterados ou desatualizados. O 07 exige 00–06 completos e compatíveis. Para garantir atualização de todas as análises, execute o master. Imagens binárias foram retiradas dos outputs embutidos após a validação para evitar duplicação; estão em `outputs/figures/` e reaparecem ao executar as células.

## Executar localmente

```bash
git clone https://github.com/thiagossilva17/MMM_Google_Meridian_Project.git
cd MMM_Google_Meridian_Project
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/run_eda.py
python -m pytest -q
python scripts/validate_artifacts.py
```

No Windows, a ativação é `.venv\Scripts\activate`. A CLI executa os mesmos módulos dos notebooks. Para validar as células em kernels novos:

```bash
python scripts/execute_notebooks.py
```

Não é preciso GPU para esta EDA. A instalação oficial inclui dependências grandes como TensorFlow/JAX. `requirements.txt` fixa o commit validado do Meridian; `data/metadata/validated_environment.txt` registra as versões transitivas efetivamente testadas. Para reprodução histórica exata, use também o SHA do commit deste projeto, em vez de acompanhar `main`.

## EDA oficial e limites

A versão verificada é Meridian 2.1.0. `MeridianEDA` gera **amostras da prior** no construtor; o projeto registra essa operação e verifica que não existe grupo posterior. Nenhum threshold oficial é alterado. `ModelSpec()` é provisório, com 156 knots e max_lag 8 nesta base, não uma recomendação final de modelo.

O HTML em `outputs/reports/meridian_eda_report.html` deve ser baixado e aberto em navegador; o GitHub mostra o código HTML. Alguns gráficos usam bibliotecas JavaScript carregadas pela internet. O Markdown e os CSVs podem ser lidos diretamente no GitHub.

Os alertas de CPMU exigem contexto: os custos são praticamente constantes (CV da ordem de 10⁻⁸); pequenos desvios podem ser compatíveis com arredondamento. Os alertas são mantidos e documentados, sem "corrigir" os dados para passar nos checks.

## Revisão da auditoria

Veja [a resposta ponto a ponto](docs/AUDIT_RESPONSE.md), [a síntese por canal](docs/channel_review.md) e `outputs/tables/readiness_actions.csv`. Os REVIEW foram investigados sem alterar severidade ou dados. A comprovação no serviço Colab continua [pendente explicitamente](docs/COLAB_VALIDATION.md).

Quando o ambiente impedir sockets do Jupyter, `python scripts/execute_cells.py` executa células originais em processos IPython novos e salva outputs reais. Isso não valida a comunicação kernel/frontend. O mecanismo efetivo consta em `notebook_validation.json`.

## Validação e próxima etapa

As evidências estão em `outputs/logs/notebook_validation.json` e `docs/validation.md`. O runtime de validação é Python 3.12 em CPU. Execução local do master não equivale a afirmar que houve uma sessão interativa no serviço Google Colab.

Próxima fase: formular hipóteses causais e controles, definir priors e holdout temporal, justificar especificação e então estimar o MMM e seus diagnósticos. A EDA não recomenda eliminar canais, alterar orçamento ou selecionar adstock pela maior correlação.
