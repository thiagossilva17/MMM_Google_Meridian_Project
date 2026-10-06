"""Gera notebooks didáticos e o master a partir da mesma sequência verificável."""
from pathlib import Path
import nbformat as nbf

ROOT=Path(__file__).resolve().parents[1]
BOOTSTRAP='''# Execute esta célula primeiro. Em Colab novo, usa somente CPU.
import os, sys, subprocess, importlib.util, importlib.metadata
from pathlib import Path

REPO_URL = "https://github.com/thiagossilva17/MMM_Google_Meridian_Project.git"
REPO_REF = "main"  # Para repetir uma execução publicada, substitua pelo SHA do commit.
IN_COLAB = importlib.util.find_spec("google.colab") is not None if importlib.util.find_spec("google") else False
cwd = Path.cwd()
candidates = [cwd, *cwd.parents]
PROJECT_ROOT = next((p for p in candidates if (p / "src/config.py").exists()), None)
if PROJECT_ROOT is None:
    PROJECT_ROOT = cwd / "MMM_Google_Meridian_Project"
    if not PROJECT_ROOT.exists():
        subprocess.run(["git", "clone", REPO_URL, str(PROJECT_ROOT)], check=True)
        subprocess.run(["git", "-C", str(PROJECT_ROOT), "checkout", REPO_REF], check=True)
    elif not (PROJECT_ROOT / "src/config.py").exists():
        raise RuntimeError("Diretório de destino existe, mas não contém o projeto esperado.")

required = ["meridian", "pandas", "numpy", "scipy", "matplotlib", "statsmodels", "tabulate"]
missing = any(importlib.util.find_spec(package) is None for package in required)
try:
    wrong_meridian = importlib.metadata.version("google-meridian") != "2.1.0"
except importlib.metadata.PackageNotFoundError:
    wrong_meridian = True
if missing or wrong_meridian:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r",
                    str(PROJECT_ROOT / "requirements-colab.txt")], check=True)

os.chdir(PROJECT_ROOT)
sys.path.insert(0, str(PROJECT_ROOT))
os.environ.setdefault("MPLCONFIGDIR", str(PROJECT_ROOT / "outputs/.mplcache"))
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
from src.config import SEED, ROOT
from src.data import load_panel
from src.reporting import show
from src.provenance import verify_checkout, verify_meridian_origin
print("Código:",verify_checkout(PROJECT_ROOT, REPO_REF))
print("Meridian:",verify_meridian_origin())
import numpy as np
np.random.seed(SEED)
geo_time_panel = load_panel()
print(f"Colab: {IN_COLAB}; projeto: {ROOT}; painel: {geo_time_panel.shape}")
'''

CHAPTERS=[
('00_data_audit','O que recebemos e podemos confiar na estrutura?', 'src.eda','data_audit',
 'Antes de procurar associações, é necessário verificar se cada linha representa um geo em uma semana, sem duplicação, lacunas ou valores impossíveis.',
 'Verificar SHA-256, schema documentado no exemplo oficial, índice exportado, chave GEO × tempo, grade de 7 dias, nulos, domínios, população e pares gasto/impressões. Calcular CPMU com denominador zero indefinido.',
 'Painel completo permite as decomposições balanceadas posteriores. Controles negativos não são automaticamente inválidos: são índices sintéticos. Conversões não inteiras não devem ser arredondadas. Problemas de contrato interrompem a execução após salvar a auditoria.'),
('01_eda_general','Qual é a escala do KPI, do gasto e da atividade de mídia?','src.eda','general',
 'Participações, assimetria, zeros e extremos ajudam a entender o desenho dos dados antes de comparar mercados.',
 'Somar contagens e gastos por semana; calcular percentis, IQR, CV, fichas por canal, participação no gasto, sequências de atividade e de zeros. Sinalizar IQR 1,5× e |z modificado MAD| > 3,5, preservando observações.',
 'Share de gasto mede alocação. Um canal com poucos zeros não é necessariamente eficiente. IQR/MAD são triagem: escala populacional, intermitência e unidades podem explicar extremos.'),
('02_eda_temporal','Como o mercado e seus controles evoluem no tempo?','src.eda','temporal',
 'Choques comuns, tendência e sazonalidade podem criar associações que se parecem com resposta à mídia.',
 'Séries nacionais e média móvel de 13 semanas, STL anual aproximado de 52 semanas, ACF, diferenças e picos. Para cada canal: mídia, gasto, CPMU e z-score versus KPI. Controles/Promo usam média ponderada por população; orgânico usa soma.',
 'Três ciclos anuais oferecem evidência limitada de sazonalidade. O z-score serve para comparar forma, não unidades ou tamanho de efeito. Mudanças de nível são descritivas, sem teste confirmatório de quebra.'),
('03_eda_geo','As diferenças entre geos vão além do tamanho populacional?','src.geo_analysis','geo_analysis',
 'Um painel pode ter muitas linhas e ainda ser formado por cópias escaladas da série nacional. Precisamos separar tamanho, diferenças persistentes e diferenças de dinâmica.',
 'Rankings e concentração do KPI, população, KPI semanal por 1.000 habitantes, sincronização, small multiples selecionados por critério. Decompor variância total = between + within; calcular R²_geo, R²_time e resíduo two-way em escala bruta e per capita.',
 'R²_geo alto indica diferenças persistentes. R²_time alto indica movimento comum. Within inclui movimento nacional, logo não equivale à informação adicional geo-temporal. No painel balanceado: R²_geo + R²_time + fração residual = 1. Essa identidade não demonstra causalidade.'),
('04_eda_media_geo','Como e onde os canais recebem investimento?','src.geo_analysis','media_geo',
 'O valor do painel para MMM depende também de execução territorial e temporal diferenciada, e não somente do número de geos.',
 'Matrizes de gasto, mix dentro de cada geo e alocação de cada canal; intensidade por habitante; Spearman/Pearson com população; HHI; CV within; heatmaps GEO × semana para gasto e impressões, brutos e per capita.',
 'Mix tem denominador por geo; alocação tem denominador por canal. HHI mede concentração, não performance. Diferenças de cor entre figuras não são comparáveis sem observar escalas. Geos seguem ordem fixa pelo KPI total.'),
('05_eda_relationships','Quais sinais se movem juntos ou podem ser redundantes?','src.eda','relationships',
 'Mídia pode responder à demanda e compartilhar tendência, sazonalidade ou alocação com outros canais. Isso limita interpretações ingênuas.',
 'Pearson/Spearman nacional, overall, within e two-way; matrizes separadas de gasto e mídia; VIF com intercepto em preditores, sem duplicar spend e impressões; lags de 0 a 8 semanas, com contagem das observações alinhadas.',
 'Não usar VIF como regra automática de remoção. Correlações entre gasto e impressões podem ser contábeis. Lags não estimam adstock. Não calcular significância supondo independência de linhas geo-temporais.'),
('06_meridian_official_eda','A auditoria oficial encontra os mesmos padrões?','src.official_eda','official_eda',
 'Uma implementação independente pode revelar diferenças de definição, escalonamento e critérios de alerta.',
 'Construir InputData com DataFrameInputDataBuilder; instanciar Meridian com defaults provisórios e MeridianEDA; gerar HTML, checks, warnings e artefatos numéricos. Recalcular R² ajustado na escala oficial por soma de quadrados e comparar com tolerância 1e-5.',
 'A API 2.1.0 gera amostras PRIOR automaticamente; não há posterior ou MCMC. Os defaults não são especificação final. INFO não significa ausência de problema; REVIEW e FAIL precisam ser lidos. R² oficial é ajustado e usa variáveis transformadas.'),
('07_eda_conclusions','Há evidência para justificar investigar um MMM geo-level?','src.reporting','conclusions',
 'Precisamos responder às perguntas do TCC com resultados, limites e implicações, evitando transformar descrição em causalidade.',
 'Consolidar integridade, missing, extremos, variabilidade, população, mix, within/between, R², colinearidade e adequação oficial; produzir relatório de prontidão e narrativa final.',
 'Informação geo-temporal residual pode justificar a investigação hierárquica, mas não garante causalidade, generalização ou superioridade preditiva. A próxima fase requer especificação, priors, holdout e diagnósticos posteriores.')]

def chapter_cells(chapter):
    name,title,module,function,motivation,method,interpretation=chapter
    narrative=f'''## {name[:2]} — {title}

### Pergunta
{title}

### Motivação
{motivation}

### Método
{method}

### Interpretação antes de olhar os resultados
{interpretation}

**Dependências:** painel validado e funções em `{module.replace('.', '/')}.py`. O código reutilizável está comentado e pode ser aberto para inspecionar as fórmulas. Todos os resultados são calculados na execução, não preenchidos manualmente.
'''
    cells=[nbf.v4.new_markdown_cell(narrative),nbf.v4.new_code_cell(f'from {module} import {function}\nreport_{name[:2]} = {function}(geo_time_panel)\nshow(report_{name[:2]},part="summary")')]
    cells.extend([nbf.v4.new_markdown_cell('### Evidências e leitura das figuras\nTabelas pequenas são exibidas integralmente. As sínteses selecionam os casos relevantes; os CSVs mantêm os dados completos.'),nbf.v4.new_code_cell(f'show(report_{name[:2]},part="evidence")')])
    if name.startswith('06'):
        cells.append(nbf.v4.new_code_cell('from IPython.display import display, FileLink\ndisplay(FileLink("outputs/reports/meridian_eda_report.html"))\n# Baixe o HTML e abra no navegador para explorar os gráficos oficiais.'))
    return cells

def notebook(cells):
    nb=nbf.v4.new_notebook(cells=cells)
    nb.metadata.kernelspec={'display_name':'Python 3','language':'python','name':'python3'}
    nb.metadata.language_info={'name':'python','version':'3.12'}
    return nb

intro='''# TCC · EDA de Marketing Mix Modeling com Google Meridian

**Dados simulados oficiais, foco GEO × TEMPO.** Não há estimação posterior, ROI ou recomendação de orçamento.

Execute de cima para baixo em runtime novo Python 3.12+ (CPU). A primeira execução instala dependências; isso pode levar alguns minutos. Se o Colab já tinha versões diferentes de NumPy/TensorFlow carregadas, reinicie a sessão após instalar e execute novamente.

O bootstrap clona o repositório público quando necessário, preserva instalações compatíveis e salva tudo na pasta do projeto. A fonte de dados e a API estão fixadas por commit/checksum. Para uma cópia histórica exata do projeto, configure `REPO_REF` com o commit da entrega. Os dados não possuem nomes de canais reais ou localização geográfica real.
'''

if __name__=='__main__':
    for chapter in CHAPTERS:
        cells=[nbf.v4.new_markdown_cell(intro),nbf.v4.new_code_cell(BOOTSTRAP)]
        stage=int(chapter[0][:2])
        if stage:
            cells.append(nbf.v4.new_markdown_cell('O manifesto verifica código, raw, ambiente, conclusão das etapas e hashes dos outputs; resultados incompatíveis são recalculados.'))
            dependencies=f"""from src.provenance import require_stages
try:
    require_stages(range({stage}))
except RuntimeError as stale:
    print('Recalculando etapas anteriores:',stale)
    from src.eda import data_audit,general,temporal,relationships
    from src.geo_analysis import geo_analysis,media_geo
    from src.official_eda import official_eda
    for analysis in [data_audit,general,temporal,geo_analysis,media_geo,relationships,official_eda][:{stage}]:
        analysis(geo_time_panel)
"""
            cells.append(nbf.v4.new_code_cell(dependencies))
        cells+=chapter_cells(chapter)
        nbf.write(notebook(cells),ROOT/'notebooks'/f'{chapter[0]}.ipynb')
    master=[nbf.v4.new_markdown_cell(intro),nbf.v4.new_code_cell(BOOTSTRAP)]
    for chapter in CHAPTERS:master+=chapter_cells(chapter)
    master.append(nbf.v4.new_markdown_cell('## Levar os resultados do Colab\nA célula abaixo prepara um ZIP com tabelas, relatórios, figuras e metadados. No Colab, o download exige somente descomentar as duas linhas indicadas.'))
    master.append(nbf.v4.new_code_cell('''import zipfile
archive_path = ROOT / 'EDA_RESULTS.zip'
with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as archive:
    for folder in ['outputs', 'docs', 'data/metadata']:
        for path in (ROOT / folder).rglob('*'):
            if path.is_file() and '.mplcache' not in str(path):
                archive.write(path, path.relative_to(ROOT))
print(archive_path)
# from google.colab import files
# files.download(str(archive_path))
'''))
    nbf.write(notebook(master),ROOT/'notebooks/EDA_COMPLETE_COLAB.ipynb')
