"""Células originais em IPython/processo novo; não valida kernel/frontend."""
import sys,subprocess,json,time,os
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1];LOGS=ROOT/'outputs/logs/cell_execution'
if '--worker' in sys.argv:
    import nbformat
    from IPython.core.interactiveshell import InteractiveShell
    from IPython.utils.capture import capture_output
    path=ROOT/'notebooks'/sys.argv[-1];nb=nbformat.read(path,as_version=4);os.chdir(ROOT);shell=InteractiveShell.instance();count=0
    for i,cell in enumerate(nb.cells):
        if cell.cell_type!='code':continue
        count+=1;print('CELL',i,flush=True);cell.outputs=[];cell.execution_count=count
        with capture_output() as cap:result=shell.run_cell(cell.source,store_history=False)
        for name,value in [('stdout',cap.stdout),('stderr',cap.stderr)]:
            if value:cell.outputs.append(nbformat.v4.new_output('stream',name=name,text=value))
        for output in cap.outputs:
            data=dict(output.data)
            if 'image/png' in data:data.pop('image/png');data['text/plain']='[Figura gerada; veja outputs/figures ou execute a célula.]'
            cell.outputs.append(nbformat.v4.new_output('display_data',data=data,metadata=output.metadata))
        print(cap.stdout);print(cap.stderr,file=sys.stderr)
        if not result.success:raise RuntimeError(f'{path.name}: célula {i}: {result.error_before_exec or result.error_in_exec}')
    nbformat.write(nb,path);print('ALL CELLS PASSED',flush=True)
else:
    LOGS.mkdir(parents=True,exist_ok=True);results=[]
    for name in sys.argv[1:] or [p.name for p in sorted((ROOT/'notebooks').glob('*.ipynb'))]:
        start=time.monotonic();print('EXECUTING',name,flush=True)
        with (LOGS/(name+'.log')).open('w') as log:p=subprocess.run([sys.executable,__file__,'--worker',name],stdout=log,stderr=subprocess.STDOUT)
        row=dict(notebook=name,status='passed' if p.returncode==0 else 'failed',returncode=p.returncode,seconds=round(time.monotonic()-start,2),method='IPython original cells; fresh process; no sockets',finished_utc=datetime.now(timezone.utc).isoformat());results.append(row);print(row,flush=True)
        (ROOT/'outputs/logs/notebook_validation.json').write_text(json.dumps(results,indent=2))
        if p.returncode:sys.exit(p.returncode)
