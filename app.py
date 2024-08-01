import streamlit as st
from utils import *

st.set_page_config(layout="wide")

st.title("InCITIES  Analytics Dashboard")

col1, col2, col3 = st.columns(3)
with col1:
  domain = st.selectbox("Select domain", domains_list)
with col2:
  if domain == "Inclusion":
    sub_domain = st.selectbox("Select sub-domain", inclusion_list)
  elif domain == "Sustainability":
    sub_domain = st.selectbox("Select sub-domain", sustainability_list)
  else:
    sub_domain = st.selectbox("Select sub-domain", resilience_list)
with col3:
  if domain == "Inclusion":
    if sub_domain == "Social":
      kpi_name = st.selectbox("Select KPI", list(social_inclusion_kpis.keys()))
      dataset_code = social_inclusion_kpis[kpi_name]
      
  if domain == "Sustainability":
    if sub_domain == "Air Quality":
      kpi_name = st.selectbox("Select KPI", list(air_quality_kpis.keys()))
      dataset_code = air_quality_kpis[kpi_name]
    if sub_domain == "Clean City":
      dataset_code = "urb_percep"


col1, col2 = st.columns(2)
if domain == "Inclusion":
  
  if sub_domain == "Social":
    with col1:
      chart_1 = echarts_option('dash1_inclusion_q11', dataset_code)

    with col2:  
      chart_2 = echarts_option('dash1_inclusion_q12', dataset_code)

if domain == "Sustainability":
  
  if sub_domain == "Air Quality":
    with col1:
      chart_1 = echarts_option_dash2_q11('dash2_q11', dataset_code)
    with col2:
      chart_2 = echarts_option_dash2_q12('dash2_q12', dataset_code)
  
  if sub_domain == "Clean City":
    cities_list = ["FI001C", "PT001C", "FR001C"]    
    city = st.selectbox('Filter by city:', cities_list)
    chart_1 = echarts_option_city('dash2_q21', dataset_code, city)