"""Proveniência de execução e invalidação por conteúdo, não por existência."""
import functools, hashlib, importlib.metadata, json, subprocess
from datetime import datetime, timezone
from pathlib import Path
from .config import ROOT, RAW, UPSTREAM_COMMIT
MANIFEST=ROOT/'outputs/logs/run_manifest.json'
_active=None
_written=set()
def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write_json(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_suffix('.tmp');temp.write_text(json.dumps(value,ensure_ascii=False,indent=2,default=str));temp.replace(path)
def git_head(root=ROOT):return subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()
def verify_checkout(root,ref):
    candidates=[f'refs/remotes/origin/{ref}',ref] if ref=='main' else [ref]
    resolved=None
    for candidate in candidates:
        r=subprocess.run(['git','-C',str(root),'rev-parse','--verify',candidate+'^{commit}'],capture_output=True,text=True)
        if r.returncode==0:resolved=r.stdout.strip();break
    if resolved is None or git_head(root)!=resolved:raise RuntimeError(f'HEAD incompatível com REPO_REF={ref}; faça fetch/checkout explicitamente. Nada foi sobrescrito.')
    return {'requested_ref':ref,'resolved_commit':resolved,'dirty':bool(subprocess.check_output(['git','-C',str(root),'status','--porcelain','--','src','scripts','requirements.txt'],text=True))}
def verify_meridian_origin():
    origin=json.loads(importlib.metadata.distribution('google-meridian').read_text('direct_url.json') or '{}')
    if origin.get('vcs_info',{}).get('commit_id')!=UPSTREAM_COMMIT or origin.get('url','').rstrip('/')!='https://github.com/google/meridian.git':
        raise RuntimeError('Origem/commit Meridian incompatível; reinstale requirements.txt. Versão 2.1.0 sozinha é insuficiente.')
    return origin
def fingerprint():
    files=sorted((ROOT/'src').glob('*.py'))+[ROOT/'scripts/build_notebooks.py',ROOT/'requirements.txt',ROOT/'requirements-colab.txt']
    source=hashlib.sha256(''.join(str(p.relative_to(ROOT))+digest(p) for p in files).encode()).hexdigest()
    versions={p:importlib.metadata.version(p) for p in ['google-meridian','numpy','pandas','scipy','statsmodels','matplotlib','jax','tensorflow']}
    return {'raw_sha256':digest(RAW),'source_sha256':source,'versions':versions,'meridian_origin':verify_meridian_origin()}
def record(path):
    if _active is not None:_written.add(str(Path(path).resolve().relative_to(ROOT)))
def require_stages(stages=range(7)):
    if not MANIFEST.exists():raise RuntimeError('Manifesto ausente: execute etapas anteriores ou master.')
    manifest=json.loads(MANIFEST.read_text());current=fingerprint()
    for stage in stages:
        info=manifest.get('stages',{}).get(f'{stage:02}',{})
        if info.get('status')!='complete' or info.get('fingerprint')!=current:raise RuntimeError(f'Etapa {stage:02} ausente/desatualizada; reexecute.')
        for name,checksum in info['files'].items():
            if not (ROOT/name).exists() or digest(ROOT/name)!=checksum:raise RuntimeError(f'Output alterado/ausente: {name}')
    return manifest
def tracked(stage):
    def decorate(function):
        @functools.wraps(function)
        def wrapped(*args,**kwargs):
            global _active,_written
            if _active is not None:raise RuntimeError('Etapas aninhadas não suportadas')
            _active=stage;_written=set()
            manifest=json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {'stages':{}}
            info={'status':'running','started_utc':datetime.now(timezone.utc).isoformat(),'git_commit_at_execution':git_head(),'source_dirty':bool(subprocess.check_output(['git','-C',str(ROOT),'status','--porcelain','--','src','scripts'],text=True)),'fingerprint':fingerprint()}
            manifest['stages'][stage]=info;write_json(MANIFEST,manifest)
            try:
                result=function(*args,**kwargs)
                if fingerprint()!=info['fingerprint']:raise RuntimeError('Fonte/ambiente mudou durante a etapa; reexecute.')
                info.update(status='complete',finished_utc=datetime.now(timezone.utc).isoformat(),files={p:digest(ROOT/p) for p in sorted(_written)})
                return result
            except Exception as exc:
                info.update(status='failed',error=str(exc));raise
            finally:
                manifest['stages'][stage]=info;write_json(MANIFEST,manifest);_active=None;_written=set()
        return wrapped
    return decorate
