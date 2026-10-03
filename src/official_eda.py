"""Camada independente de auditoria: API Google Meridian 2.1.0 verificada no commit fixado."""
import dataclasses
import importlib.metadata
import json
import warnings
import numpy as np
import pandas as pd
from .config import *
from .data import channels
from .reporting import table, result

def official_eda(panel):
    from meridian.data import data_frame_input_data_builder
    from meridian.model import model, spec
    from meridian.model.eda import meridian_eda
    if importlib.metadata.version('google-meridian')!='2.1.0':
        raise RuntimeError('Instale o commit fixado em requirements.txt para reproduzir a API validada.')
    paid=channels(panel)
    frame=panel.copy();frame[TIME]=frame[TIME].dt.strftime('%Y-%m-%d')
    builder=data_frame_input_data_builder.DataFrameInputDataBuilder(
        kpi_type='non_revenue',default_kpi_column=KPI,default_revenue_per_kpi_column=REVENUE_PER_KPI)
    builder=(builder.with_kpi(frame).with_revenue_per_kpi(frame).with_population(frame)
             .with_controls(frame,control_cols=CONTROLS)
             .with_media(frame,media_cols=[c+'_impression' for c in paid],media_spend_cols=[c+'_spend' for c in paid],media_channels=paid)
             .with_organic_media(frame,organic_media_cols=ORGANIC,organic_media_channels=['Organic_channel0'])
             .with_non_media_treatments(frame,non_media_treatment_cols=NON_MEDIA))
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter('always')
        # Defaults de ModelSpec: cenário provisório para EDA, não escolha final de MMM.
        mmm=model.Meridian(input_data=builder.build(),model_spec=spec.ModelSpec())
        # O construtor oficial faz amostragem PRIOR. Nenhuma amostragem posterior.
        eda=meridian_eda.MeridianEDA(mmm,seed=SEED)
        eda.generate_and_save_report(filename='meridian_eda_report.html',filepath=str(ROOT/'outputs/reports'))
        engine=eda.eda_engine
        methods=['check_geo_cost_per_media_unit','check_national_cost_per_media_unit',
                 'check_geo_std','check_national_std','check_overall_kpi_invariability',
                 'check_population_corr_raw_media','check_population_corr_scaled_treatment_control',
                 'check_geo_pairwise_corr','check_national_pairwise_corr','check_geo_vif','check_national_vif',
                 'check_variable_geo_time_collinearity','check_data_param_ratio']
        findings=[];outcomes={}
        for method in methods:
            outcome=getattr(engine,method)();outcomes[method]=outcome
            for finding in outcome.findings:
                findings.append(dict(check=method,severity=finding.severity.name,cause=finding.finding_cause.name,explanation=finding.explanation))
            for i,artifact in enumerate(outcome.analysis_artifacts):
                for field in dataclasses.fields(artifact):
                    value=getattr(artifact,field.name)
                    if hasattr(value,'to_dataframe'):
                        if not value.dims:
                            exported=pd.DataFrame([{k:v.item() for k,v in value.data_vars.items()}]) if hasattr(value,'data_vars') else pd.DataFrame({field.name:[value.item()]})
                        elif hasattr(value,'data_vars'):
                            exported=value.to_dataframe()
                        else:
                            exported=value.to_dataframe(name=field.name)
                        table(exported,f'official_{method}_{i}_{field.name}')
        checks=table(pd.DataFrame(findings),'meridian_eda_checks',False)
        ratio=outcomes['check_data_param_ratio'].analysis_artifacts[0]
        adequacy=table(pd.DataFrame([{key:getattr(ratio,key) for key in ['n_geos','n_times','n_knots','n_controls','n_treatments','n_data_points','n_parameters','ratio']}]),'meridian_data_adequacy',False)
        # Reconciliação numérica: mesmas escalas oficiais, algoritmo independente
        # de soma de quadrados, sem reutilizar o OLS de R² da biblioteca.
        from meridian.model.eda.eda_engine import stack_variables
        from .statistics import variance_decomposition
        scaled=stack_variables(engine.treatment_control_scaled_ds).to_dataframe(name='value').reset_index()
        scaled_panel=scaled.pivot(index=[GEO,TIME],columns='var',values='value').reset_index()
        variables=[c for c in scaled_panel if c not in [GEO,TIME]]
        custom_scaled=variance_decomposition(scaled_panel,variables)
        n=len(scaled_panel);g=scaled_panel[GEO].nunique();t=scaled_panel[TIME].nunique()
        custom_scaled['custom_adjusted_r2_geo']=1-(1-custom_scaled.r2_geo)*(n-1)/(n-g)
        custom_scaled['custom_adjusted_r2_time']=1-(1-custom_scaled.r2_time)*(n-1)/(n-t)
        official_r2=outcomes['check_variable_geo_time_collinearity'].analysis_artifacts[0].rsquared_ds.to_dataframe().rename_axis('variable')
        reconciliation=custom_scaled.join(official_r2)
        for axis in ['geo','time']:
            reconciliation['absolute_difference_'+axis]=(reconciliation['custom_adjusted_r2_'+axis]-reconciliation['rsquared_'+axis]).abs()
        table(reconciliation,'official_r2_reconciliation')
        agreement=bool(np.allclose(reconciliation.custom_adjusted_r2_geo,reconciliation.rsquared_geo,atol=1e-5,equal_nan=True)
                       and np.allclose(reconciliation.custom_adjusted_r2_time,reconciliation.rsquared_time,atol=1e-5,equal_nan=True))
    warning_table=pd.DataFrame([{'category':w.category.__name__,'message':str(w.message)} for w in captured],columns=['category','message'])
    table(warning_table.drop_duplicates(),'meridian_warnings',False)
    assert 'posterior' not in mmm.inference_data.groups(), 'Esta fase não pode conter posterior.'
    (ROOT/'data/metadata/meridian_run.json').write_text(json.dumps({'version':importlib.metadata.version('google-meridian'),
        'source_commit':UPSTREAM_COMMIT,'prior_sampling':'automatic constructor, default draws, fixed seed',
        'posterior_sampled':False,'model_spec':'defaults; provisional EDA only','knots':ratio.n_knots,
        'max_lag':mmm.model_spec.max_lag,'inference_groups':mmm.inference_data.groups()},indent=2))
    comparison=[]
    labels={
        'cost_per_media_unit':('CPMU = spend/media; NaN em zero','cost_per_media_unit.csv','Mesmas unidades; verificar artefatos por geo e nível nacional.'),
        'std':('Variância bruta, zeros, IQR e MAD','channel_summary.csv','Escalas distintas: Meridian transforma as variáveis; limites oficiais mantidos.'),
        'population':('Spearman de população × total de mídia','population_media_correlation.csv','Total e média temporal são proporcionais em painel balanceado; checagem escalada responde outra pergunta.'),
        'pairwise':('Pearson/Spearman nacional, overall e within','correlation_summary.csv','Meridian usa transformação própria; within da EDA não é seu agregado nacional.'),
        'vif':('VIF com intercepto em preditores brutos/within','vif_summary.csv','Diagnósticos oficiais usam escalas/população; diferenças não são automaticamente erro.'),
        'geo_time':('R² não ajustado em valores brutos e per capita','geo_time_r2.csv','Meridian usa R² ajustado sobre variáveis transformadas; comparar definições antes dos números.'),
        'data_param':('G×T observações; parâmetros não são todos independentes','data_audit.csv','Guardrail provisório; razão não prova adequação nem identificação.')}
    for key,(custom,evidence,interpretation) in labels.items():
        selection=checks[checks.check.str.contains(key)]
        comparison.append(dict(issue=key,custom_eda=custom,custom_evidence=evidence,
                               meridian_eda=str(selection.severity.value_counts().to_dict()),
                               agreement='comparação de definições; não igualdade numérica presumida',interpretation=interpretation))
    comp=table(pd.DataFrame(comparison),'custom_vs_meridian',False)
    comp.loc[comp.issue=='geo_time','agreement']=f'R² ajustado reconciliado na mesma escala: {agreement}; tolerância numérica 1e-5'
    cpmu_summary=pd.read_csv(ROOT/'outputs/tables/cost_per_media_unit.csv') if (ROOT/'outputs/tables/cost_per_media_unit.csv').exists() else None
    if cpmu_summary is not None:
        comp.loc[comp.issue=='cost_per_media_unit','agreement']=f'REVIEW por extremos, mas CV máximo de CPMU={cpmu_summary.cv.max():.3e}; inspecionar precisão numérica'
    table(comp,'custom_vs_meridian',False)
    cpmu_note=(f'Os alertas de CPMU precisam de contexto: o CV máximo do custo unitário é {cpmu_summary.cv.max():.3e}. '
               'A variação relativa minúscula é compatível com arredondamento na geração/exportação, e não evidencia dispersão econômica de custos. '
               'Não alteramos o dado ou o threshold IQR oficial para eliminar o alerta.') if cpmu_summary is not None else 'Consultar cost_per_media_unit.csv após executar o capítulo 00 para contextualizar os alertas de CPMU.'
    text=f'''O relatório HTML oficial foi executado com Meridian {importlib.metadata.version('google-meridian')}, sem amostragem posterior. Os checks exportaram {len(checks)} achados: {checks.severity.value_counts().to_dict()}. As advertências de execução estão em meridian_warnings.csv; não foram silenciadas nem resolvidas por alteração de thresholds.

A API atual usa DataFrameInputDataBuilder. MeridianEDA gera amostras da prior no construtor para completar diagnósticos da especificação. Isso não ajusta o modelo aos dados e não produz estimativas posteriores. A especificação default é provisória: {ratio.n_knots} knots e {mmm.model_spec.max_lag} lags. Não escolhemos hiperparâmetros finais com esta EDA.

A razão oficial é {ratio.n_data_points}/({ratio.n_geos}−1+{ratio.n_knots}+{ratio.n_controls}+{ratio.n_treatments}) = {ratio.ratio:.2f}. Essa contagem é um guardrail que não conta todos os efeitos geo como parâmetros independentes. Não é prova de tamanho amostral efetivo ou de suficiência.

{cpmu_note}

Uma diferença metodológica importante: os R² oficiais são ajustados e usam dados transformados; a EDA própria mostra R² brutos e por habitante não ajustados. Recalculando por soma de quadrados na mesma escala oficial, a concordância dentro de 1e-5 foi **{agreement}**. A tabela official_r2_reconciliation contém as diferenças por variável. VIF e correlações também dependem da população e agregação. Artefatos numéricos foram exportados para investigar essas diferenças.'''
    return result('06_meridian_official_eda',text,{'official_checks':checks,'data_adequacy':adequacy,'comparison':comp},[], 'Consolidar os achados, implicações e limites de prontidão.')
