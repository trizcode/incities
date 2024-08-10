import pandas as pd
import requests
import streamlit as st
from streamlit_echarts import st_echarts
import matplotlib.pyplot as plt
import seaborn as sns

dash2_topics = ["Air Quality", "Energy", "Biodiversity", "Waste Management", "Employment"]
resilience_list = ["Social", "Economic & Infrastructure"]

# KPIs
# --> Inclusion
inclusion_kpis = {
  "Gini coefficient": "tessi190",
  "Disability employment gap": "tepsr_sp200",
  "Risk of poverty rate": "tespm010",
  "Gender employment gap": "tepsr_lm220"
}
# --> Sustainability
dash2_air_quality_kpis = {
  "Greenhouse gases emissions": "cei_gsr011",
  "Average CO2 emissions": "sdg_12_30"
}
dash2_energy_kpis = {
    "Renewable energy sources": "REN",
    "Renewable energy sources in transport": "REN_TRA",
    "Renewable energy sources in electricity": "REN_ELC",
    "Renewable energy sources in heating and cooling": "REN_HEAT_CL",
}
# --> Resilience
dash3_social_kpis = {
    "Total Population on 1 January": "Total",
    "Proportion of population aged over 65": "Aged",
    "Tertiary educational attainment": "tgs00109",
    "Low work intensity households": "tgs00108"
}

# National dictionary
geo_dict = {
    "Finland": "FI",
    "Portugal": "PT",
    "Slovakia": "SK", 
    "France": "FR", 
    "Germany": "DE"
}
# Nuts2_2 dictionary
nuts2_dict = {
    "Köln": "DEA2",
    "Helsinki-U.": "FI1B",
    "S. Slovensko": "SK03",
    "A. M. Lisboa": "PT17",
    "Ile de France": "FR10"
}
# Nuts3 dictionary
cities_dict = {
    "Helsinki": "FI001C", 
    "Lisbon": "PT001C", 
    "Paris": "FR001C",
    "Köln": "DE004C",
    "Zilina": "SK006C"
}

# Functions to display echarts visualizations

# --> General chart functions
def echarts_option(echarts_function, kpi):
    
    response = requests.get(f'http://localhost:8000/data_charts/{echarts_function}/?dataset_code={kpi}')
    chart_option = response.json()
    st_echarts(options=chart_option, height="400px")


def echarts_option_kpi(echarts_function, dataset_code, col_kpi, kpi):
    response = requests.get(f"http://localhost:8000/data_charts/{echarts_function}/?dataset_code={dataset_code}&{col_kpi}={kpi}")
    chart_option = response.json()
    st_echarts(options=chart_option, height="400px")


# --> Specific chart functions

def scatter_plot_gini_vs_poverty():
    response = requests.get(f'http://localhost:8000/data_charts/dash1_gini_coef_vs_poverty_risk/')
    df = pd.DataFrame(response.json())
    sns.set_theme(style="white")
    plt.figure(figsize=(10, 6))
    
    sns.scatterplot(
        x="values_gini",
        y="values_poverty",
        hue="geo",
        sizes=(40, 400),
        alpha=0.5,
        palette="muted",
        data=df
    )
    
    plt.xlabel('Gini Coefficient (%)')
    plt.ylabel('Risk of Poverty Rate (%)')
    plt.title('Scatter Plot of Gini Coefficient vs. Risk of Poverty Rate')
    
    st.pyplot(plt)







def echarts_option_dash3_chart_1(kpi):
    
    if kpi in ["tgs00109", "tgs00108"]:
        response = requests.get(f"http://localhost:8000/data_charts/dash3_chart_1/?dataset_code={kpi}")
        chart_option = response.json()
    if kpi in ["Total", "Aged"]:
        response = requests.get(f"http://localhost:8000/data_charts/dash3_chart_1/?dataset_code=demo_r_pjangrp3&ind={kpi}")
        chart_option = response.json()
        
    st_echarts(options=chart_option, height="500px")
    

def echarts_option_dash3_chart2():
    
    get_years = requests.get(f"http://localhost:8000/data_charts/get_available_years/?dataset_code=demo_r_pjangrp3&geo=nuts2_1")
    years_list = get_years.json()
    
    year = st.selectbox('Filter by year:', years_list)
    
    response = requests.get(f"http://localhost:8000/data_charts/dash3_chart_2/?dataset_code=demo_r_pjangrp3&year={year}")
    chart_option = response.json()
    st_echarts(options=chart_option, height="500px")