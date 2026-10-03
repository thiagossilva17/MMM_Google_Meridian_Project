# Validação da entrega

- Ambiente isolado: Python 3.12.14, CPU; versões exatas em `data/metadata/validated_environment.txt`.
- 11 testes automatizados passaram. Incluem contrato da base, rejeição de duplicatas/lacunas/negativos/população inválida/data irregular/schema incompleto, identidade de variâncias, colinearidade perfeita no VIF e agregação de receita.
- Todos os oito notebooks modulares e o master foram executados com `nbclient`, cada um em kernel novo, sem permitir erros de célula. Tempos e número de células estão no JSON abaixo.
- O master executa a sequência completa e gera os resultados novamente, sem depender de estados de outros notebooks.
- SHA-256 do raw validado em toda leitura; nenhuma imputação, exclusão de extremos ou remoção de canais.
- Meridian 2.1.0 executado; relatório HTML completo e artefatos exportados. O objeto de inferência contém apenas `prior`, nunca `posterior`.
- R² ajustados reconciliados por método independente na mesma escala oficial, diferenças inferiores a 10⁻¹⁵ nesta execução.
- 78 figuras SVG e 88 tabelas CSV geradas. Figuras centrais R² GEO×TIME e dashboard foram inspecionadas visualmente; rótulos sobrepostos no scatter foram substituídos por legenda externa com coordenadas.
- Imagens PNG são produzidas e exibidas ao executar. Foram externalizadas dos outputs embutidos dos notebooks para evitar duplicação; SVGs estão versionados.
- Não houve execução interativa no serviço Google Colab. O bootstrap e o fluxo foram executados localmente no runtime equivalente; o clone/download público e instalação foram verificados separadamente. Se uma sessão Colab tiver versões antigas já importadas, pode ser necessário reiniciá-la após instalar.

## Problemas corrigidos durante a execução

1. Exportação de artefatos xarray escalares exigia tabela de uma linha, em vez de índice inexistente.
2. A dimensão de variável do motor oficial chama-se `var`; a reconciliação foi corrigida para esse schema verificado.
3. A execução Jupyter precisou de portas locais entre kernel e executor; não representa acesso a dados externos.
4. `git push` via terminal não tinha credenciais; publicação realizada pelo conector GitHub autenticado.

## Evidências por notebook

- `00_data_audit.ipynb`: passed; 2 células de código; 2.08 segundos.
- `01_eda_general.ipynb`: passed; 2 células de código; 3.2 segundos.
- `02_eda_temporal.ipynb`: passed; 2 células de código; 7.68 segundos.
- `03_eda_geo.ipynb`: passed; 2 células de código; 7.83 segundos.
- `04_eda_media_geo.ipynb`: passed; 2 células de código; 18.67 segundos.
- `05_eda_relationships.ipynb`: passed; 2 células de código; 3.18 segundos.
- `06_meridian_official_eda.ipynb`: passed; 3 células de código; 25.49 segundos.
- `07_eda_conclusions.ipynb`: passed; 3 células de código; 1.46 segundos.
- `EDA_COMPLETE_COLAB.ipynb`: passed; 11 células de código; 60.88 segundos.
