"""Gate de publicação: SVGs íntegros, eixos comparáveis e manifesto válido."""
import sys,json,xml.etree.ElementTree as ET
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.config import ROOT
from src.provenance import require_stages,digest,write_json

def validate_svg(path):
    path=Path(path)
    if path.stat().st_size<500:raise ValueError(f'SVG vazio/truncado: {path}')
    root=ET.parse(path).getroot()
    if not root.tag.endswith('svg') or not root.get('viewBox') or not any(n.tag.endswith(('path','image','rect')) for n in root.iter()):raise ValueError(f'SVG inválido: {path}')
    return dict(path=str(path.relative_to(ROOT)),bytes=path.stat().st_size,sha256=digest(path))
def main():
    import pandas as pd
    require_stages(range(8));figures=[validate_svg(p) for p in sorted((ROOT/'outputs/figures').rglob('*.svg'))]
    expected=pd.read_csv(ROOT/'outputs/tables/geo_kpi_summary.csv').geo.tolist();axes=json.loads((ROOT/'outputs/logs/heatmap_axes.json').read_text());checked=[]
    for name,value in axes.items():
        if name.startswith('media_geo/') and ('geo_time' in name or name.endswith('spend_per_capita')):
            if value['index']!=expected:raise ValueError(f'Ordem incorreta: {name}')
            checked.append(name)
    write_json(ROOT/'outputs/logs/artifact_validation.json',dict(status='passed',svg_count=len(figures),svg=figures,comparable_heatmaps=checked))
    print(dict(status='passed',svg_count=len(figures),order_checks=len(checked)))
if __name__=='__main__':main()
