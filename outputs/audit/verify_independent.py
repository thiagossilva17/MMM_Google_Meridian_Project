"""Auditoria independente do commit c301905; não importa funções do projeto.
Uso: python outputs/audit/verify_independent.py [raiz_do_projeto]
"""
from pathlib import Path
import sys, json, hashlib
import numpy as np
import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor
root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[2]
out=Path(__file__).resolve().parent
p=pd.read_csv(root/'data/raw/geo_all_channels.csv').drop(columns='Unnamed: 0').sort_values(['geo','time']).reset_index(drop=True)
t=root/'outputs/tables'
results=[]
def check(name, actual, expected, atol=1e-9, rtol=1e-7):
 a=np.asarray(actual,dtype=float);e=np.asarray(expected,dtype=float)
 ok=bool(np.allclose(a,e,atol=atol,rtol=rtol,equal_nan=True))
 delta=np.abs(a-e);finite=delta[np.isfinite(delta)]
 results.append(dict(check=name,passed=ok,max_absolute_difference=float(finite.max()) if finite.size else None))
def read(n,index=None): return pd.read_csv(t/(n+'.csv'),index_col=index)
meta=json.loads((root/'data/metadata/source.json').read_text())
results.append(dict(check='raw_sha256',passed=hashlib.sha256((root/'data/raw/geo_all_channels.csv').read_bytes()).hexdigest()==meta['sha256']))
check('balanced_panel',[len(p),p.duplicated(['geo','time']).sum(),p.isna().sum().sum()],[40*156,0,0])
spendcols=[c for c in p if c.endswith('_spend')]
spend=p.groupby('geo')[spendcols].sum();spend.columns=spend.columns.str.removesuffix('_spend')
mix=read('media_mix','geo').sort_index();alloc=read('geo_allocation','geo').sort_index()
check('mix_values',mix,spend.div(spend.sum(axis=1),axis=0));check('mix_sum',mix.sum(axis=1),1)
check('allocation_values',alloc,spend.div(spend.sum(axis=0),axis=1));check('allocation_sum',alloc.sum(),1)
check('spend_share',read('spend_share','channel').spend_share,spend.sum()/spend.to_numpy().sum())
geo=read('geo_kpi_summary','geo').sort_index();pop=p.groupby('geo').population.first()
check('population_count_once',geo.population,pop)
check('kpi_per_capita',geo.kpi_per_1000_per_week,p.groupby('geo').conversions.mean()/pop*1000)
vd=read('within_between_variance','variable')
# OLS explícito com intercepto; não reutiliza fórmula de decomposição do autor.
y=p[vd.index].to_numpy();sst=((y-y.mean(axis=0))**2).sum(axis=0)
g=pd.get_dummies(p.geo,drop_first=True,dtype=float).to_numpy();time=pd.get_dummies(p.time,drop_first=True,dtype=float).to_numpy()
for label,d in [('geo',g),('time',time),('geo_time',np.column_stack([g,time]))]:
 x=np.column_stack([np.ones(len(p)),d]);fit=x@np.linalg.lstsq(x,y,rcond=None)[0]
 r2=1-((y-fit)**2).sum(axis=0)/sst
 check('r2_'+label+'_ols',vd['r2_'+label],r2)
check('variance_identity',vd.total_variance,vd.between_geo+vd.within_geo)
check('two_way_partition',vd.r2_geo+vd.r2_time+vd.residual_geo_time_share,1)
columns=list(vd.index);within=p[columns]-p.groupby('geo')[columns].transform('mean');tw=within-p.groupby('time')[columns].transform('mean')+p[columns].mean()
for level,d in [('overall',p[columns]),('within',within),('two_way',tw)]:
 for method in ['pearson','spearman']:
  check('correlation_'+level+'_'+method,read('correlation_'+level+'_'+method,0),d.corr(method=method))
 v=read('vif_summary');v=v[v.level==level];x=d[list(v.variable)];x=(x-x.mean())/x.std(ddof=0);design=np.column_stack([np.ones(len(x)),x])
 check('vif_'+level+'_statsmodels',v.vif,[variance_inflation_factor(design,i+1) for i in range(x.shape[1])])
# Per-capita usado para a pergunta central.
pc=read('per_capita_panel').sort_values(['geo','time']).reset_index(drop=True)
check('per_capita_all',pc.drop(columns=['geo','time']),p[pc.columns[2:]].div(p.population,axis=0)*1000)
# Séries nacionais: razões de somas e média ponderada explícita.
nat=read('national_timeseries','time');expected=p.groupby('time').conversions.sum();check('national_kpi',nat.conversions,expected)
check('national_population',nat.population,pop.sum())
check('national_revenue',nat.revenue_derived,(p.conversions*p.revenue_per_conversion).groupby(p.time).sum())
for c in ['competitor_sales_control','sentiment_score_control','Promo']:
 check('national_weighted_'+c,nat[c],(p[c]*p.population).groupby(p.time).sum()/pop.sum())
for c in spend.columns:
 check('national_cpmu_'+c,read('national_cpmu','time')[c],nat[c+'_spend']/nat[c+'_impression'].replace(0,np.nan))
check('official_reconciliation',read('official_r2_reconciliation').filter(regex='absolute_difference'),0,atol=1e-5)
# Evidência de profundidade: extremos, sparsity e heterogeneidade do mix.
metrics={}
for c in spend.columns:
 active=p[c+'_impression']>0
 rates=active.groupby(p.geo).mean()
 metrics[c]={'zero_share':float((~active).mean()),'geo_active_min':float(rates.min()),'geo_active_max':float(rates.max()),'national_zero_dates':list(nat.index[nat[c+'_impression']==0]),'mix_min':float(mix[c].min()),'mix_max':float(mix[c].max()),'mix_sd':float(mix[c].std(ddof=0))}
(out/'independent_checks.json').write_text(json.dumps(results,indent=2))
(out/'channel_evidence.json').write_text(json.dumps(metrics,indent=2))
print(json.dumps({'checks':len(results),'passed':sum(r['passed'] for r in results),'failed':[r for r in results if not r['passed']]},indent=2))
