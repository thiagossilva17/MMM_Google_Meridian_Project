"""Execução CLI completa; a mesma sequência está no master notebook."""
import sys
import logging
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.data import load_panel
from src.eda import data_audit, general, temporal, relationships
from src.geo_analysis import geo_analysis, media_geo
from src.official_eda import official_eda
from src.reporting import conclusions

if __name__=='__main__':
    panel=load_panel()
    for function in [data_audit,general,temporal,geo_analysis,media_geo,relationships,official_eda,conclusions]:
        print(f'INÍCIO {function.__name__}',flush=True)
        try:
            report=function(panel)
        except Exception:
            logging.exception('Falha no capítulo %s',function.__name__)
            raise
        print(report['narrative'],flush=True)
