"""Aquisição, contrato de schema e agregação com semântica explícita."""
import hashlib
import importlib.metadata
import json
import logging
import platform
import re
from datetime import datetime, timezone
from urllib.request import urlopen

import numpy as np
import pandas as pd
from .config import *

def channels(frame: pd.DataFrame) -> list[str]:
    """Descobre os pares reais de impressão/gasto; rejeita pares incompletos."""
    found = sorted(c.removesuffix('_impression') for c in frame
                   if re.fullmatch(r'Channel\d+_impression', c))
    if not found or any(f'{c}_spend' not in frame for c in found):
        raise ValueError('Schema de mídia paga inesperado; revisar mapeamento oficial.')
    if set(c.removesuffix('_spend') for c in frame if c.endswith('_spend')) != set(found):
        raise ValueError('Gasto sem correspondente de mídia.')
    return found

def roles(frame: pd.DataFrame) -> dict[str, str]:
    mapped = {GEO:'geo', TIME:'time', KPI:'kpi', POP:'population',
              REVENUE_PER_KPI:'revenue_per_kpi', 'Unnamed: 0':'export_index'}
    for group, names in [('control',CONTROLS), ('organic_media',ORGANIC), ('non_media_treatment',NON_MEDIA)]:
        mapped.update(dict.fromkeys(names, group))
    for channel in channels(frame):
        mapped[channel+'_impression'] = 'media'
        mapped[channel+'_spend'] = 'spend'
    unknown = set(frame) - set(mapped)
    missing = set(mapped) - {'Unnamed: 0'} - set(frame)
    if unknown or missing:
        raise ValueError(f'Schema mudou: desconhecidas={unknown}; ausentes={missing}')
    return {c:mapped[c] for c in frame}

def load_panel() -> pd.DataFrame:
    """Mantém raw imutável e verifica o checksum de referência antes da análise."""
    directories()
    logging.basicConfig(filename=ROOT/'outputs/logs/execution.log', level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s', force=True)
    if not RAW.exists():
        with urlopen(DATA_URL, timeout=60) as response:
            payload = response.read()
        reference = json.loads((ROOT/'data/metadata/source.json').read_text())
        if hashlib.sha256(payload).hexdigest() != reference['sha256']:
            raise ValueError('Download diverge do checksum documentado.')
        RAW.write_bytes(payload)
    checksum = hashlib.sha256(RAW.read_bytes()).hexdigest()
    reference = json.loads((ROOT/'data/metadata/source.json').read_text())
    if checksum != reference['sha256']:
        raise ValueError('Arquivo raw alterado; restaurar a versão documentada.')
    panel = pd.read_csv(RAW)
    roles(panel)
    if 'Unnamed: 0' in panel:
        if not np.array_equal(panel['Unnamed: 0'].to_numpy(), np.arange(len(panel))):
            raise ValueError('Índice exportado inesperado; não remover automaticamente.')
        panel = panel.drop(columns='Unnamed: 0')
    panel[TIME] = pd.to_datetime(panel[TIME], errors='raise')
    panel = panel.sort_values([GEO,TIME]).reset_index(drop=True)
    panel.to_csv(ROOT/'data/processed/geo_time_panel.csv', index=False)
    versions = {'python':platform.python_version()}
    for package in ['google-meridian','numpy','pandas','scipy','matplotlib','statsmodels',
                    'jax','tensorflow','nbformat','nbclient']:
        try: versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError: versions[package] = 'not installed'
    execution = {'accessed_utc':datetime.now(timezone.utc).isoformat(), 'versions':versions,
                 'sha256':checksum, 'rows':len(panel), 'geos':panel[GEO].nunique(),
                 'periods':panel[TIME].nunique(), 'seed':SEED}
    (ROOT/'data/metadata/execution.json').write_text(json.dumps(execution,indent=2))
    logging.info('Dataset carregado e checksum validado: %s',execution)
    return panel

def analytical_columns(panel: pd.DataFrame) -> list[str]:
    return [KPI] + [c+'_impression' for c in channels(panel)] + [c+'_spend' for c in channels(panel)] + ORGANIC + CONTROLS + NON_MEDIA

def national(panel: pd.DataFrame) -> pd.DataFrame:
    """Soma contagens/gastos; controles e promoção usam média ponderada por população.

    A unidade original dos controles sintéticos é desconhecida. A média ponderada
    é uma lente descritiva explícita, não uma soma de vendas de concorrentes.
    """
    additive = [KPI] + [c+'_impression' for c in channels(panel)] + [c+'_spend' for c in channels(panel)] + ORGANIC
    result = panel.groupby(TIME)[additive].sum(min_count=1)
    population = panel.groupby(TIME)[POP].sum(min_count=1)
    for col in CONTROLS + NON_MEDIA:
        result[col] = (panel[col]*panel[POP]).groupby(panel[TIME]).sum(min_count=1)/population
    result['revenue_derived'] = (panel[KPI]*panel[REVENUE_PER_KPI]).groupby(panel[TIME]).sum(min_count=1)
    result[REVENUE_PER_KPI] = result['revenue_derived']/result[KPI].replace(0,np.nan)
    result[POP] = population
    return result
