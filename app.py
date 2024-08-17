import streamlit as st
from utils import *
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")

selected = option_menu(
  menu_title="InCITIES Dashboard",
  options=["Ranking", "Cities", "Inclusion", "Sustainability", "Resilience"],
  icons=["bar-chart", "buildings", "people", "globe-europe-africa", "hammer"],
  menu_icon="cast",
  orientation="horizontal",
)

if selected == "Inclusion":
  col1, col2, col3 = st.columns(3)
  with col1:
    kpi_name = st.selectbox("Select indicator:", list(inclusion_kpis.keys()))
    dataset_code = inclusion_kpis[kpi_name]
  
  col1, col2 = st.columns(2)
  
  with col1:
    echarts_option('line_chart_inclusion_kpis', dataset_code)
  with col2:
    echarts_option('bar_chart_inclusion_kpis_ranking', dataset_code)

  if dataset_code == "tespm010":
    with col1:
      echarts_option('line_chart_inclusion_kpis', 'ilc_li41')
    with col2:
      echarts_option('bar_chart_inclusion_kpis_ranking', 'ilc_li41')
  
  with col1:
    st.header("")
    scatter_plot_gini_vs_poverty()
  with col2:
    col1, col2 = st.columns(2)
    with col2:
      lev_limit_list = {'Severe': 'SEV', 'Some': 'SOME'}
      lev_limit_name = st.selectbox("Select activity limitation level:", list(lev_limit_list.keys()))
      lev_limit = lev_limit_list[lev_limit_name]
    echarts_option_kpi('grouped_bar_chart_disability_employ_gap_by_sex', 'tepsr_sp200', 'lev_limit', lev_limit)


if selected == "Sustainability":
  
  col1, col2, col3 = st.columns(3)
  with col1:
    topic = st.selectbox("Select topic:", sustainability_topics)
  
  col1, col2 = st.columns(2)
  if topic == "Air Quality":
    with col1:
      echarts_option('line_chart_air_quality', 'cei_gsr011')
    with col2:
      echarts_option('bar_chart_air_quality_ranking', 'cei_gsr011')
    with col1:
      echarts_option('line_chart_air_quality', 'sdg_12_30')
    with col2:
      echarts_option('bar_chart_air_quality_ranking', 'sdg_12_30')
   

  if topic == "Energy":
    with col1:
      echarts_option_kpi('line_chart_energy', 'sdg_07_40', 'nrg_bal', 'REN')
    with col2:
      echarts_option_kpi('bar_chart_energy_ranking', 'sdg_07_40', 'nrg_bal', 'REN')
    
    col1, col2 = st.columns(2)
    with col1:
      kpi_name = st.selectbox("Select type of renewable energy source:", list(energy_kpis.keys()))
      dataset_code = energy_kpis[kpi_name]
    
    with col1:
      echarts_option_kpi('line_chart_energy', 'sdg_07_40', 'nrg_bal', dataset_code)
    with col2:
      st.header("")
      echarts_option_kpi('bar_chart_energy_ranking', 'sdg_07_40', 'nrg_bal', dataset_code)
    with col1:
      col1, col2 = st.columns(2)
      with col1:
        geo_name = st.selectbox('Filter by country:', list(nat_dict.keys()))
        geo = nat_dict[geo_name]
      
      echarts_option_kpi('donut_chart_energy', 'sdg_07_40', 'geo', geo)
      
  if topic == "Biodiversity":
    
    with col1:
      echarts_option('bar_chart_TPA_prot_area', 'env_bio4')
    with col2:
      echarts_option('bar_chart_MPA_prot_area', 'env_bio4')
    with col1:
      echarts_option('grouped_bar_chart_prot_area', 'env_bio4')
    with col2:
      geo_name = st.selectbox('Filter by country:', list(nat_dict.keys()))
      geo = nat_dict[geo_name]
      echarts_option_kpi('donut_chart_prot_area', 'env_bio4', 'geo', geo)
      
  if topic == "Waste Management":
    with col1:
      geo_name = st.selectbox('Filter by country:', list(nat_dict.keys()))
      geo = nat_dict[geo_name]
      echarts_option_kpi('line_chart_wst_oper', 'env_wastrt', 'geo', geo)  
    with col2:
      echarts_option('bar_chart_wst_oper_ranking', 'env_wastrt')
    with col1:
      echarts_option_kpi('horizontal_bar_chart_waste_treat', 'env_wastrt', 'geo', geo)
    with col2:
      echarts_option_kpi('pie_chart_waste_dim', 'env_wastrt', 'geo', geo)
      
  if topic == "Employment":
    with col1:
      echarts_option('line_chart_employment_rate', 'tgs00007')
    with col2:
      echarts_option('bar_chart_employment_ranking', 'tgs00007')
    with col1:
      geo_name = st.selectbox('Filter by nuts2 regions:', list(nuts2_dict.keys()))
      geo = nuts2_dict[geo_name]
      echarts_option_kpi('donut_chart_employment_by_sex', 'tgs00007', 'geo', geo)
      
      
if selected == "Resilience":
  col1, col2 = st.columns(2)
  with col1:
    echarts_option('bar_chart_total_pop_ranking', 'demo_r_pjangrp3')
  with col2:
    echarts_option('bar_chart_pop_aged_ranking', 'demo_r_pjangrp3')
  with col1:
    echarts_option('line_chart_tertiary_educ_attain', 'tgs00109')
  with col2:
    echarts_option('grouped_bar_chart_pop_by_age_group', 'demo_r_pjangrp3')
  with col1:
    kpi_name = st.selectbox("Select indicator:", list(resilience_kpis.keys()))
    dataset_code = resilience_kpis[kpi_name]
    echarts_option('line_chart_by_resilience_kpis', dataset_code)
  with col2:
    st.header("")
    echarts_option_w_kpi('grouped_bar_chart_physi_vs_hosp_beds')