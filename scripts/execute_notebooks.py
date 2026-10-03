"""Valida cada notebook em kernel novo; não permite erros de célula."""
import json
import os
import sys
import time
from pathlib import Path
import nbformat
from nbclient import NotebookClient
from jupyter_client.kernelspec import KernelSpecManager

ROOT=Path(__file__).resolve().parents[1]

if __name__=='__main__':
    kernel_dir=ROOT/'outputs/logs/kernel'
    kernel_dir.mkdir(parents=True,exist_ok=True)
    (kernel_dir/'kernel.json').write_text(json.dumps({'argv':[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'],
        'display_name':'TCC validation','language':'python'}))
    # Não depende do kernel Python global. Instalado somente na pasta de execução.
    kernel_prefix=ROOT/'outputs/logs/jupyter'
    KernelSpecManager().install_kernel_spec(str(kernel_dir),kernel_name='tcc-validation',prefix=str(kernel_prefix))
    os.environ['JUPYTER_PATH']=str(kernel_prefix/'share/jupyter')
    validation_path=ROOT/'outputs/logs/notebook_validation.json'
    results=json.loads(validation_path.read_text()) if validation_path.exists() else []
    paths=[ROOT/'notebooks'/name for name in sys.argv[1:]] if len(sys.argv)>1 else sorted((ROOT/'notebooks').glob('*.ipynb'))
    for path in paths:
        print('EXECUTING',path.name,flush=True)
        nb=nbformat.read(path,as_version=4)
        start=time.monotonic()
        NotebookClient(nb,timeout=900,kernel_name='tcc-validation',resources={'metadata':{'path':str(ROOT)}},allow_errors=False).execute()
        # Preserve textos/tabelas; gráficos completos estão em SVG/PNG e são exibidos ao rodar.
        # Remover somente binários embutidos evita duplicar dezenas de MB nos 9 notebooks.
        images_removed=0
        for cell in nb.cells:
            for output in cell.get('outputs',[]):
                if 'data' in output and 'image/png' in output.data:
                    output.data.pop('image/png');images_removed+=1
                    output.data['text/plain']='[Figura gerada; veja outputs/figures ou execute esta célula para exibir.]'
        nbformat.write(nb,path)
        results=[r for r in results if r['notebook']!=path.name]
        results.append({'notebook':path.name,'status':'passed','seconds':round(time.monotonic()-start,2),
                        'code_cells':sum(c.cell_type=='code' for c in nb.cells),'figures_externalized':images_removed})
        (ROOT/'outputs/logs/notebook_validation.json').write_text(json.dumps(results,indent=2))
        print('PASSED',results[-1],flush=True)
