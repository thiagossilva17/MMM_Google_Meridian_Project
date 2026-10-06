"""Regressões de problemas concretos identificados na auditoria."""
import numpy as np
import pandas as pd
import pytest
from src.geo_analysis import per_capita_matrix
from src import provenance
from scripts.validate_artifacts import validate_svg

def test_per_capita_preserves_order():
    x=pd.DataFrame({'week':[60.,20.,90.]},index=['Geo2','Geo0','Geo1']);pop=pd.Series({'Geo0':10.,'Geo1':30.,'Geo2':20.})
    actual=per_capita_matrix(x,pop,x.index)
    assert actual.index.tolist()==x.index.tolist()
    np.testing.assert_allclose(actual.week,[3000.,2000.,3000.])
@pytest.mark.parametrize('content',['','<svg>','<svg viewBox="0 0 10 10"></svg>'])
def test_rejects_invalid_svg(tmp_path,content):
    p=tmp_path/'bad.svg';p.write_text(content)
    with pytest.raises(ValueError):validate_svg(p)
def test_manifest_detects_changed_output(tmp_path,monkeypatch):
    monkeypatch.setattr(provenance,'ROOT',tmp_path);monkeypatch.setattr(provenance,'MANIFEST',tmp_path/'manifest.json');monkeypatch.setattr(provenance,'fingerprint',lambda:{'source':'verified'})
    p=tmp_path/'evidence.csv';p.write_text('value\n1\n')
    provenance.write_json(provenance.MANIFEST,{'stages':{'00':{'status':'complete','fingerprint':{'source':'verified'},'files':{'evidence.csv':provenance.digest(p)}}}})
    provenance.require_stages([0]);p.write_text('value\n2\n')
    with pytest.raises(RuntimeError,match='alterado'):provenance.require_stages([0])
def test_manifest_rejects_stale_or_incomplete_stage(tmp_path,monkeypatch):
    monkeypatch.setattr(provenance,'MANIFEST',tmp_path/'manifest.json');monkeypatch.setattr(provenance,'fingerprint',lambda:{'source':'current'})
    for status,source in [('complete','old'),('failed','current'),('running','current')]:
        provenance.write_json(provenance.MANIFEST,{'stages':{'00':{'status':status,'fingerprint':{'source':source},'files':{}}}})
        with pytest.raises(RuntimeError):provenance.require_stages([0])
def test_activity_identity():
    x=np.array([0.,0.,2.,4.,9.]);positive=x[x>0];p=len(positive)/len(x)
    assert np.isclose(np.var(x),p*np.var(positive)+p*(1-p)*np.mean(positive)**2)
def test_ref_mismatch_preserves_checkout(tmp_path):
    import subprocess
    subprocess.run(['git','init','-q',str(tmp_path)],check=True)
    with pytest.raises(RuntimeError,match='REPO_REF'):provenance.verify_checkout(tmp_path,'missing-ref')
