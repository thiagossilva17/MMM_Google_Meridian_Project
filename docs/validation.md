# Validação da revisão após auditoria

Data: 06/10/2026. Base: `ac9960a3a86e7af07a507121043c6914fcbc4195`.

- Ambiente isolado Python 3.12, CPU, instalação pelo requirements; versões completas em `data/metadata/validated_environment.txt`. Origem/commit Meridian verificados.
- **19 testes passaram**, incluindo regressões da ordem per capita, SVG inválido, ref incompatível e manifesto desatualizado.
- **Nove notebooks passaram** executando as células originais em ordem em processos IPython novos. O master recalculou todas as etapas; outputs armazenados não foram usados como prova de execução.
- nbclient foi tentado, mas o ambiente bloqueou sockets antes de iniciar o kernel. `nbclient_attempt.txt` preserva o erro. O executor alternativo valida código/outputs, não comunicação kernel/frontend.
- **79 SVGs válidos**, **21 verificações de ordem** e **129 CSVs**. O gate exige manifesto das oito etapas completo e compatível.
- Inspeção visual amostral: dois SVGs antes vazios, CPMU Channel2, mix em p.p., small multiples e dashboard. Não se afirma inspeção individual de todas as figuras nem navegação interativa do HTML.
- Maior diferença absoluta na reconciliação de correlação: 4.88e-15; VIF: 1.33e-15. Quatro conjuntos IQR coincidem em todas as localizações; tolerância numérica 10⁻⁵.
- Os seis REVIEW permanecem no relatório oficial, com decisões descritivas separadas. Apenas prior, sem posterior. Raw e auditoria independente preservados.
- **Colab real permanece não comprovado**, com procedimento em `COLAB_VALIDATION.md`.

## Execução das células

| Notebook | Resultado | Tempo (s) | Mecanismo |
|---|---|---:|---|
| 00_data_audit.ipynb | passed | 2.7 | IPython, processo novo |
| 01_eda_general.ipynb | passed | 4.16 | IPython, processo novo |
| 02_eda_temporal.ipynb | passed | 8.41 | IPython, processo novo |
| 03_eda_geo.ipynb | passed | 7.75 | IPython, processo novo |
| 04_eda_media_geo.ipynb | passed | 20.0 | IPython, processo novo |
| 05_eda_relationships.ipynb | passed | 3.05 | IPython, processo novo |
| 06_meridian_official_eda.ipynb | passed | 28.74 | IPython, processo novo |
| 07_eda_conclusions.ipynb | passed | 1.4 | IPython, processo novo |
| EDA_COMPLETE_COLAB.ipynb | passed | 67.46 | IPython, processo novo |

`outputs/logs/notebook_validation.json` registra mecanismo, resultado e timestamp; logs por notebook em `outputs/logs/cell_execution/`. Os notebooks preservam saídas textuais reais; imagens são externalizadas. O manifesto vincula etapas a conteúdo de código, raw, ambiente e outputs. O commit registrado é a base da revisão, com alterações locais explicitamente indicadas; o hash do código identifica o conteúdo executado antes da publicação.

O ambiente foi restaurado antes desta rodada. As alterações foram reconstruídas e validadas novamente; resultados da tentativa anterior não foram presumidos válidos. O gate de publicação verifica tamanho/hash/XML dos SVGs, seguido da comparação da árvore Git remota com a árvore local preparada.
