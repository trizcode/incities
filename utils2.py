import pandas as pd
import requests
import streamlit as st
from streamlit_echarts import st_echarts
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.io as pio


# Define domains
domain_list = ["Inclusion", "Sustainability", "Resilience"]

# Define sub-domains
sub_domain_inclusion = ["Social", "Economic", "Gender"]

sub_domain_sustainability = ["Environmental", "Social", "Economic"]

sub_domain_resilience = ["Social", "Economic", "Infrastructure", "Institutional", "Hazard"]

# Define sub-domain KPIs
economic_inclusion_kpis = {
    "Gini coefficient": "tessi190", 
    "Poverty Rate": "ilc_li41",
    "Persons employed in productive age": "tgs00007"
}

social_inclusion_kpis = {
    "Youth Unemployment": "edat_lfse_22", 
    "Slum Household": "ilc_lvhl21n", 
    "Disability employment gap": "tepsr_sp200", 
    "Voter turnout": ""
}

gender_inclusion_kpis = {
    "Gender employment gap": "tepsr_lm220", 
    "Equitable School Enrolment": "educ_uoe_enra11"
}

sustainability_kpis = [""]

resilience_kpis = [""]

# Functions to display data visualizations
def echarts_option(echarts_function, kpi):
    
    response = requests.get(f'http://localhost:8000/data_charts/{echarts_function}/?dataset_code={kpi}')
    chart_option = response.json()
    st_echarts(options=chart_option, height="500px")
    
def plotly_chart(plotly_chart, kpi):
    
    response = requests.get(f'http://localhost:8000/data_charts/{plotly_chart}/?dataset_code={kpi}')
    fig_json = response.json()
    fig = pio.from_json(fig_json)
    st.plotly_chart(fig)