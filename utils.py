import requests
import streamlit as st
from streamlit_echarts import st_echarts

# Domain list
domains_list = ["Inclusion", "Sustainability", "Resilience"]

#Sub domain list
inclusion_list = ["Social"]
sustainability_list = ["Air Quality", "Clean City"]
resilience_list = ["Social", "Economic", "Infrastructure"]

# KPIs
# --> Inclusion
social_inclusion_kpis = {
  "Gini coefficient": "tessi190",
  "Disability employment gap": "tepsr_sp200",
  "People at risk of poverty": "tepsr_lm410",
  "Gender employment gap": "tepsr_lm220"
}
# --> Sustainability
air_quality_kpis = {
  "Greenhouse gases emissions": "cei_gsr011",
  "Average CO2 emissions": "sdg_12_30",
  'Annual average concentration of NO2': "EN2026V",
  'Annual average concentration of PM10': "EN2027V",
  'Accumulated ozone concentration': "EN2025V"
}


# Functions to display echarts visualizations

# --> General chart functions
def echarts_option(echarts_function, kpi):
    response = requests.get(f'http://localhost:8000/data_charts/{echarts_function}/?dataset_code={kpi}')
    chart_option = response.json()
    st_echarts(options=chart_option, height="400px", width="700px")


def echarts_option_city(echarts_function, kpi, city):
    response = requests.get(f'http://localhost:8000/data_charts/{echarts_function}/?dataset_code={kpi}&city={city}')
    chart_option = response.json()
    st_echarts(options=chart_option, height="500px")


# --> Specific chart functions
def echarts_option_dash2_q11(echarts_function, kpi): 
    year_filter_list = [5, 10, 15]
    year_filter = st.selectbox('Filter by years to display:', year_filter_list)
    
    if kpi in ["cei_gsr011", "sdg_12_30"]:
        response = requests.get(f'http://localhost:8000/data_charts/{echarts_function}/?dataset_code={kpi}&year_filter={year_filter}')
    if kpi in ["EN2026V", "EN2027V", "EN2025V"]:
        response = requests.get(f'http://localhost:8000/data_charts/{echarts_function}/?dataset_code=urb_cenv&indic_ur={kpi}&year_filter={year_filter}')

    chart_option = response.json()
    st_echarts(options=chart_option, height="400px", width="700px")


def echarts_option_dash2_q12(echarts_function, kpi):
    if kpi in ["cei_gsr011", "sdg_12_30"]:
        get_years = requests.get(f"http://localhost:8000/data_charts/get_available_years/?dataset_code={kpi}")
        years_list = get_years.json()
    if kpi in ["EN2026V", "EN2027V", "EN2025V"]:
        get_years = requests.get(f"http://localhost:8000/data_charts/get_available_years/?dataset_code=urb_cenv&indic_ur={kpi}")
        years_list = get_years.json()
    
    default_year1 = 2010
    default_year2 = 2022
    
    if default_year1 in years_list:
        default_index1 = years_list.index(default_year1)
    else:
        default_index1 = len(years_list) - 11
    if default_year2 in years_list:
        default_index2 = years_list.index(default_year2)
    else:
        default_index2 = len(years_list) - 1
    
    col1, col2 = st.columns(2)
    with col1:
        year1 = st.selectbox('Select year 1:', years_list, index=default_index1)
    with col2:
        year2 = st.selectbox('Select year 2:', years_list, index=default_index2)
    
    if kpi in ["cei_gsr011", "sdg_12_30"]:  
        response = requests.get(f'http://localhost:8000/data_charts/{echarts_function}/?dataset_code={kpi}&year1={year1}&year2={year2}')
    if kpi in ["EN2026V", "EN2027V", "EN2025V"]:
        response = requests.get(f'http://localhost:8000/data_charts/{echarts_function}/?dataset_code=urb_cenv&indic_ur={kpi}&year1={year1}&year2={year2}')

    chart_option = response.json()
    st_echarts(options=chart_option, height="400px", width="700px")