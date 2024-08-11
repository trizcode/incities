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
    kpi_name = st.selectbox("Select KPI:", list(inclusion_kpis.keys()))
    dataset_code = inclusion_kpis[kpi_name]
  
  col1, col2 = st.columns(2)
  with col1:
    echarts_option('dash1_line_chart', dataset_code)
  with col2:
    echarts_option('dash1_bar_chart_ranking', dataset_code)
  
  with col1:
    scatter_plot_gini_vs_poverty()
  with col2:
    col1, col2 = st.columns(2)
    with col2:
      lev_limit_list = {'Severe': 'SEV', 'Some': 'SOME'}
      lev_limit_name = st.selectbox("Select activity limitation level:", list(lev_limit_list.keys()))
      lev_limit = lev_limit_list[lev_limit_name]
    echarts_option_kpi('disability_employment_gap_by_sex', 'tepsr_sp200', 'lev_limit', lev_limit)


if selected == "Sustainability":
  
  col1, col2, col3 = st.columns(3)
  with col1:
    topic = st.selectbox("Select topic:", dash2_topics)
  with col2:
    if topic == "Air Quality":
      kpi_name = st.selectbox("Select kpi:", list(dash2_air_quality_kpis.keys()))
      dataset_code = dash2_air_quality_kpis[kpi_name]
    if topic == "Energy":
      kpi_name = st.selectbox("Select kpi:", list(dash2_energy_kpis.keys()))
      dataset_code = dash2_energy_kpis[kpi_name]
  
  col1, col2 = st.columns(2)
  if topic == "Air Quality":
    with col1:
      echarts_option('dash2_q11', dataset_code)
    with col2:
      echarts_option('dash2_q12', dataset_code)
    
  if topic == "Energy":
    with col1:
      echarts_option_kpi('dash2_q22', 'sdg_07_40', 'nrg_bal', dataset_code)
    with col2:
      echarts_option_kpi('dash2_bar_chart_energy_ranking', 'sdg_07_40', 'nrg_bal', dataset_code)
    with col1:
      col1, col2 = st.columns(2)
      with col1:
        geo_name = st.selectbox('Filter by country:', list(geo_dict.keys()))
        geo = geo_dict[geo_name]
      
      echarts_option_kpi('d2_donut_chart_energy', 'sdg_07_40', 'geo', geo)
      
  if topic == "Biodiversity":
    
    with col1:
      echarts_option('d2_bar_chart_TPA_prot_area', 'env_bio4')
    with col2:
      echarts_option('d2_bar_chart_MPA_prot_area', 'env_bio4')
    with col1:
      echarts_option('dash2_q41', 'env_bio4')
    with col2:
      geo_name = st.selectbox('Filter by country:', list(geo_dict.keys()))
      geo = geo_dict[geo_name]
      echarts_option_kpi('d2_donut_chart_prot_area', 'env_bio4', 'geo', geo)
      
  if topic == "Waste Management":
    with col1:
      geo_name = st.selectbox('Filter by country:', list(geo_dict.keys()))
      geo = geo_dict[geo_name]
      echarts_option_kpi('dash2_line_chart_wst_oper', 'env_wastrt', 'geo', geo)  
    with col2:
      echarts_option('dash2_bar_chart_wst_ranking', 'env_wastrt')
    with col1:
      echarts_option_kpi('dash2_q51', 'env_wastrt', 'geo', geo)
    with col2:
      echarts_option_kpi('dash2_q52', 'env_wastrt', 'geo', geo)
      
  if topic == "Employment":
    with col1:
      echarts_option('dash2_q61', 'tgs00007')
    with col2:
      echarts_option('dash2_bar_chart_employment_ranking', 'tgs00007')
    with col1:
      geo_name = st.selectbox('Filter by nuts2 regions:', list(nuts2_dict.keys()))
      geo = nuts2_dict[geo_name]
      echarts_option_kpi('dash2_donut_chart_employment_by_sex', 'tgs00007', 'geo', geo)
      
      
if selected == "Resilience":
  col1, col2 = st.columns(2)
  with col1:
    echarts_option('dash3_chart_1_1_ranking', 'demo_r_pjangrp3')
  with col2:
    echarts_option('dash3_chart_1_2_ranking', 'demo_r_pjangrp3')
  with col1:
    echarts_option('dash3_chart_1', 'tgs00109')
  with col2:
    echarts_option('dash3_chart_2', 'demo_r_pjangrp3')
  with col1:
    kpi_name = st.selectbox("Select kpi:", list(dash3_kpis.keys()))
    dataset_code = dash3_kpis[kpi_name]
    echarts_option('dash3_chart_3', dataset_code)
  with col2:
    echarts_option_w_kpi('dash3_chart_4')