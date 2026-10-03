"""Estatísticas descritivas sem testes de significância para observações dependentes."""
import numpy as np
import pandas as pd

def safe_divide(numerator, denominator):
    return numerator / denominator.replace(0, np.nan)

def describe(series: pd.Series) -> dict:
    x = series.dropna()
    q = x.quantile([.01,.05,.25,.5,.75,.95,.99])
    mean, std = x.mean(), x.std(ddof=0)
    return dict(n=len(x),mean=mean,median=x.median(),std=std,variance=x.var(ddof=0),
                min=x.min(),max=x.max(),**{f'p{int(p*100):02}':v for p,v in q.items()},
                iqr=q.loc[.75]-q.loc[.25],cv=std/mean if mean != 0 else np.nan,
                zeros=int(x.eq(0).sum()),zero_share=x.eq(0).mean())

def variance_decomposition(panel: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Decomposição ponderada por observação (ddof=0); identidade total=between+within.

    R² two-way via double demeaning só é utilizado com painel completo/balanceado.
    O resíduo é interação/desvio geo-temporal, não efeito causal identificável.
    """
    if panel.duplicated(['geo','time']).any() or len(panel) != panel.geo.nunique()*panel.time.nunique():
        raise ValueError('Decomposição two-way exige painel balanceado sem duplicatas.')
    records=[]
    for col in columns:
        x=panel[col].astype(float)
        if not np.isfinite(x).all(): raise ValueError(f'{col}: valores não finitos.')
        grand=x.mean()
        g=x.groupby(panel.geo).transform('mean')
        t=x.groupby(panel.time).transform('mean')
        total=np.mean((x-grand)**2)
        between=np.mean((g-grand)**2)
        within=np.mean((x-g)**2)
        time=np.mean((t-grand)**2)
        residual=np.mean((x-g-t+grand)**2)
        ratio=lambda value: value/total if total>0 else np.nan
        records.append(dict(variable=col,total_variance=total,between_geo=between,
                            within_geo=within,between_share=ratio(between),within_share=ratio(within),
                            r2_geo=ratio(between),r2_time=ratio(time),
                            r2_geo_time=ratio(between+time),residual_geo_time_share=ratio(residual)))
    return pd.DataFrame(records).set_index('variable')

def vif_table(frame: pd.DataFrame, level: str) -> pd.DataFrame:
    """VIF com intercepto, colunas padronizadas, constantes explicitamente indefinidas."""
    x=frame.dropna().astype(float)
    if len(x)<len(x.columns)+2: raise ValueError('Amostra insuficiente para VIF.')
    varying=x.std(ddof=0)>1e-12
    z=(x.loc[:,varying]-x.loc[:,varying].mean())/x.loc[:,varying].std(ddof=0)
    rows=[]
    for col in x:
        if not varying[col]:
            rows.append(dict(variable=col,level=level,vif=np.nan,status='constant')); continue
        y=z[col].to_numpy()
        others=z.drop(columns=col).to_numpy()
        design=np.column_stack([np.ones(len(y)),others])
        fitted=design@np.linalg.lstsq(design,y,rcond=None)[0]
        residual_ratio=np.sum((y-fitted)**2)/np.sum(y*y)
        rows.append(dict(variable=col,level=level,vif=1/residual_ratio if residual_ratio>1e-12 else np.inf,
                         status='singular' if residual_ratio<=1e-12 else 'finite'))
    return pd.DataFrame(rows)

def outliers(panel: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    records=[]
    for col in columns:
        x=panel[col]
        q1,q3=x.quantile([.25,.75]); iqr=q3-q1
        median=x.median(); mad=(x-median).abs().median()
        score=.67448975*(x-median)/mad if mad>0 else pd.Series(np.nan,index=x.index)
        flags=(x<q1-1.5*iqr)|(x>q3+1.5*iqr)
        for i in panel.index[flags | (score.abs()>3.5)]:
            records.append(dict(geo=panel.loc[i,'geo'],time=panel.loc[i,'time'],variable=col,
                                value=x.loc[i],iqr_flag=bool(flags.loc[i]),modified_z=score.loc[i],
                                decision='preservar; investigar contexto e escala populacional'))
    return pd.DataFrame(records,columns=['geo','time','variable','value','iqr_flag','modified_z','decision'])
