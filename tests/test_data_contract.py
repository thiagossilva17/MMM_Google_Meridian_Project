"""Contratos e identidades estatísticas com casos de falha e painel sintético conhecido."""
import numpy as np
import pandas as pd
import pytest
from src.data import load_panel, roles, national, channels
from src.validation import require_valid_panel
from src.statistics import variance_decomposition, vif_table

@pytest.fixture(scope='module')
def panel(): return load_panel()

def test_data_contract(panel):
    require_valid_panel(panel)
    assert len(panel)==6240
    assert panel.geo.nunique()==40 and panel.time.nunique()==156

@pytest.mark.parametrize('issue',['duplicate','missing','negative','population','irregular','missing_column'])
def test_rejects_invalid_input(panel,issue):
    changed=panel.copy()
    if issue=='duplicate':changed=pd.concat([changed,changed.iloc[:1]])
    elif issue=='missing':changed=changed.iloc[1:]
    elif issue=='negative':changed.loc[0,'Channel0_spend']=-1
    elif issue=='population':changed.loc[0,'population']=0
    elif issue=='irregular':changed.loc[0,'time']+=pd.Timedelta(days=1)
    elif issue=='missing_column':changed=changed.drop(columns='conversions')
    with pytest.raises((ValueError,KeyError)):require_valid_panel(changed)

def test_variance_identity_and_known_components():
    grid=pd.MultiIndex.from_product([range(3),range(4)],names=['geo','time']).to_frame(index=False)
    grid['only_geo']=grid.geo*2.
    grid['only_time']=grid.time*3.
    grid['additive']=grid.only_geo+grid.only_time
    result=variance_decomposition(grid,['only_geo','only_time','additive'])
    np.testing.assert_allclose(result.total_variance,result.between_geo+result.within_geo)
    assert result.loc['only_geo','r2_geo']==1
    assert result.loc['only_time','r2_time']==1
    assert abs(result.loc['additive','residual_geo_time_share'])<1e-12

def test_vif_perfect_collinearity_and_constant():
    x=pd.DataFrame({'a':range(20),'b':np.arange(20)*2,'constant':1})
    result=vif_table(x,'fixture').set_index('variable')
    assert np.isinf(result.loc['a','vif']) and np.isinf(result.loc['b','vif'])
    assert pd.isna(result.loc['constant','vif'])

def test_national_revenue_is_sum_of_products(panel):
    nat=national(panel)
    expected=(panel.conversions*panel.revenue_per_conversion).groupby(panel.time).sum()
    np.testing.assert_allclose(nat.revenue_derived,expected)
    assert set(roles(panel).values())>={'media','spend','control','organic_media','non_media_treatment'}

def test_panel_decomposition_nonnegative_and_sums(panel):
    result=variance_decomposition(panel,[c+'_impression' for c in channels(panel)])
    np.testing.assert_allclose(result.r2_geo+result.r2_time+result.residual_geo_time_share,1,atol=1e-10)
    assert (result.residual_geo_time_share>=0).all()
