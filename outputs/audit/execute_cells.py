"""Executor de auditoria sem sockets; um processo novo por notebook.
Executa células originais em ordem com IPython; não simula o frontend Colab.
Uso: python execute_cells.py RAIZ [notebook.ipynb ...]
"""
import sys,subprocess,json,time,os
from pathlib import Path
root=Path(sys.argv[1]).resolve(); out=Path(__file__).resolve().parent
if '--worker' in sys.argv:
 from IPython.core.interactiveshell import InteractiveShell
 from IPython.utils.capture import capture_output
 p=root/'notebooks'/sys.argv[-1];n=json.loads(p.read_text());os.chdir(root)
 shell=InteractiveShell.instance()
 for i,c in enumerate(n['cells']):
  if c['cell_type']!='code':continue
  print('CELL',i,flush=True)
  with capture_output() as cap: result=shell.run_cell(''.join(c['source']),store_history=False)
  print(cap.stdout);print(cap.stderr,file=sys.stderr)
  if not result.success: raise RuntimeError(f'{p.name}: célula {i} falhou: {result.error_before_exec or result.error_in_exec}')
 print('ALL CELLS PASSED',flush=True)
else:
 names=sys.argv[2:] or [p.name for p in sorted((root/'notebooks').glob('*.ipynb'))]
 results=[]
 for name in names:
  start=time.monotonic();print('EXECUTING',name,flush=True)
  with (out/(name+'.log')).open('w') as log:
   p=subprocess.run([sys.executable,__file__,str(root),'--worker',name],stdout=log,stderr=subprocess.STDOUT)
  record={'notebook':name,'returncode':p.returncode,'seconds':round(time.monotonic()-start,2),'method':'IPython cells; fresh subprocess; no sockets'}
  results.append(record);print(record,flush=True)
  (out/'cell_execution.json').write_text(json.dumps(results,indent=2))
  if p.returncode:sys.exit(p.returncode)
