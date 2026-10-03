"""Configuração auditável; caminhos relativos à raiz do projeto."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = 20261003
UPSTREAM_COMMIT = '02111531f8661373aa7b6ba31c316c67d72d1dd2'
SOURCE_PATH = 'meridian/data/simulated_data/csv/geo_all_channels.csv'
DATA_URL = f'https://raw.githubusercontent.com/google/meridian/{UPSTREAM_COMMIT}/{SOURCE_PATH}'
RAW = ROOT / 'data/raw/geo_all_channels.csv'
# Papéis confirmados no notebook oficial, não inferidos apenas de correlações.
KPI = 'conversions'
GEO, TIME, POP = 'geo', 'time', 'population'
CONTROLS = ['competitor_sales_control', 'sentiment_score_control']
ORGANIC = ['Organic_channel0_impression']
NON_MEDIA = ['Promo']
REVENUE_PER_KPI = 'revenue_per_conversion'

def directories() -> None:
    for folder in ['data/raw', 'data/processed', 'data/metadata', 'outputs/tables',
                   'outputs/reports', 'outputs/logs', 'docs']:
        (ROOT / folder).mkdir(parents=True, exist_ok=True)
    for chapter in ['data_audit', 'general', 'temporal', 'geo', 'media_geo', 'relationships']:
        (ROOT / 'outputs/figures' / chapter).mkdir(parents=True, exist_ok=True)
