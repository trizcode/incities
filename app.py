import requests
import streamlit as st
from streamlit_echarts import st_echarts

st.title("InCITIES  Analytics Dashboard")

col1, col2 = st.columns(2)

with col1:
    kpi_options = {
        "Gini coefficient": "tessi190",
        "Disability employment gap": "tepsr_sp200",
        "People at risk of poverty": "tepsr_lm410",
    }

    kpi = st.selectbox("Select KPI", list(kpi_options.keys()))
    kpi_code = kpi_options[kpi]

with col2:

    api_url = f"http://localhost:8000/data_charts/dash1_inclusion_q11/?kpi={kpi_code}"
    response = requests.get(api_url)
    if response.status_code == 200:
        chart_data = response.json()
        st_echarts(options=chart_data, height="500px")
    else:
        st.write("Failed to fetch data from the API")
