import requests
import streamlit as st
from streamlit_echarts import st_echarts


def echarts_option(echarts_function, dataset_code):
    response = requests.get(f'http://localhost:8000/data_charts/{echarts_function}/?dataset_code={dataset_code}')
    if response.status_code == 200:
        chart_option = response.json()
        st_echarts(options=chart_option, height="400px", width="700px")
    else:
        st.error("Failed to load data. Please try again.")


domains_list = ["Inclusion", "Sustainability", "Resilience"]
inclusion_kpis = {
    "Gini coefficient": "tessi190",
    "Disability employment gap": "tepsr_sp200",
    "People at risk of poverty": "tepsr_lm410",
    "Gender employment gap": "tepsr_lm220",
}
    
st.title("InCITIES  Analytics Dashboard")
col1, col2 = st.columns(2)
with col1:
  domain = st.selectbox("Select domain", domains_list)
with col2:
  if domain == "Inclusion":
    kpi_name = st.selectbox("Select KPI", list(inclusion_kpis.keys()))
    dataset_code = inclusion_kpis[kpi_name]
  
col1, col2 = st.columns(2)
if domain == "Inclusion":
  with col1:
    chart_1 = echarts_option('dash1_inclusion_q11', dataset_code)

  with col2:  
    chart_2 = echarts_option('dash1_inclusion_q12', dataset_code)