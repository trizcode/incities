import requests
import streamlit as st
from streamlit_echarts import st_echarts

st.title("InCITIES  Analytics Dashboard")

inclusion_kpis = {
    "Gini coefficient": "tessi190",
    "Disability employment gap": "tepsr_sp200",
    "People at risk of poverty": "tepsr_lm410",
    "Gender employment gap by NUTS 2 regions": "tepsr_lm220",
}

kpi_name = st.selectbox("Select KPI", list(inclusion_kpis.keys()))
dataset_code = inclusion_kpis[kpi_name]

dash1_inclusion_q11 = requests.get(f'http://localhost:8000/data_charts/dash1_inclusion_q11/?dataset_code={dataset_code}')
if dash1_inclusion_q11.status_code == 200:
    chart_options = dash1_inclusion_q11.json()
    st_echarts(options=chart_options)
else:
    st.error("Failed to load data. Please try again.")

dash1_inclusion_q12 = requests.get(f'http://localhost:8000/data_charts/dash1_inclusion_q12/?dataset_code={dataset_code}')
if dash1_inclusion_q12.status_code == 200:
    chart_options = dash1_inclusion_q12.json()
    st_echarts(options=chart_options)
else:
    st.error("Failed to load data. Please try again.")