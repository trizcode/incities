import streamlit as st
import requests
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
    

def params_to_query_string(params):
    return '&'.join([f'{key}={",".join(value)}' for key, value in params.items()])

with col2:
    nat_params = {
    'geo': ['FR', 'FI', 'PT', 'DE', 'SK']
    }
    query_params = params_to_query_string(nat_params)
    print(query_params)
    api_url = f"http://localhost:8000/charts/dash1_inclusion_q11/?kpi={kpi_code}&{query_params}"
    
    response = requests.get(api_url)

    if response.status_code == 200:
        chart_data = response.json()
        st_echarts(options=chart_data, height="500px")
    else:
        st.write("Failed to fetch data from the API")
