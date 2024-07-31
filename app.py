import streamlit as st

from utils import *

st.set_page_config(layout="wide")

domains_list = ["Inclusion", "Sustainability", "Resilience"]

inclusion_kpis = {
  "Gini coefficient": "tessi190",
  "Disability employment gap": "tepsr_sp200",
  "People at risk of poverty": "tepsr_lm410",
  "Gender employment gap": "tepsr_lm220"
}

sustainability_list = ["Air Quality", "Clean City", "Biodiversity"]

air_quality_kpis = {
  "Greenhouse gases emissions": "cei_gsr011",
  "Average CO2 emissions": "sdg_12_30",
  'Annual average concentration of NO2': "EN2026V",
  'Annual average concentration of PM10': "EN2027V",
  'Accumulated ozone concentration': "EN2025V"
}

# ---------------------------- App ----------------------------

st.title("InCITIES  Analytics Dashboard")
col1, col2 = st.columns(2)
with col1:
  domain = st.selectbox("Select domain", domains_list)
with col2:
  if domain == "Inclusion":
    kpi_name = st.selectbox("Select KPI", list(inclusion_kpis.keys()))
    dataset_code = inclusion_kpis[kpi_name]

if domain == "Sustainability":
  col1, col2 = st.columns(2)
  with col1:
    sub_domain = st.selectbox("Select sub-domain", sustainability_list)
  if sub_domain == "Air Quality":
    with col2:
      kpi_name = st.selectbox("Select KPI", list(air_quality_kpis.keys()))
      dataset_code = air_quality_kpis[kpi_name]
    
    
col1, col2 = st.columns(2)
if domain == "Inclusion":
  with col1:
    chart_1 = echarts_option('dash1_inclusion_q11', dataset_code)

  with col2:  
    chart_2 = echarts_option('dash1_inclusion_q12', dataset_code)

if domain == "Sustainability":
  
  if sub_domain == "Air Quality":
    
    with col1:
      chart_1 = echarts_option_dash2_q11('dash2_q11', dataset_code)
      
    #with col2:
      #chart_2 = echarts_option('dash2_q12', dataset_code)