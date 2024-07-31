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


def echarts_option_dash2_q11(echarts_function, dataset_code):   
    if dataset_code in ["cei_gsr011", "sdg_12_30"]:
        response = requests.get(f'http://localhost:8000/data_charts/{echarts_function}/?dataset_code={dataset_code}')
    
    if dataset_code in ["EN2026V", "EN2027V", "EN2025V"]:
        response = requests.get(f'http://localhost:8000/data_charts/{echarts_function}/?dataset_code=urb_cenv&indic_ur={dataset_code}')

    if response.status_code == 200:
        chart_option = response.json()
        st_echarts(options=chart_option, height="400px", width="700px")
    else:
        st.error("Failed to load data. Please try again.")


def echarts_option_dash2_q12(echarts_function, dataset_code, indic_ur, year1, year2):
    if dataset_code in ["cei_gsr011", "sdg_12_30"]:  
        response = requests.get(f'http://localhost:8000/data_charts/{echarts_function}/?dataset_code={dataset_code}&year1={year1}&year2={year2}')
    
    if dataset_code in ["EN2026V", "EN2027V", "EN2025V"]:
        response = requests.get(f'http://localhost:8000/data_charts/{echarts_function}/?dataset_code=urb_cenv&indic_ur={dataset_code}&year1={year1}&year2={year2}')

    if response.status_code == 200:
        chart_option = response.json()
        st_echarts(options=chart_option, height="400px", width="700px")
    else:
        st.error("Failed to load data. Please try again.")