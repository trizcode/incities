import streamlit as st
from streamlit_option_menu import option_menu
from utils2 import *
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="InCITIES Dashboard", page_icon=":cityscape:", layout="wide")

#st.title(":cityscape: InCITIES Dashboard")
#st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

# Create Menu side bar
with st.sidebar:
    menu = option_menu(
    menu_title="Menu",
    options=["Data Visualizations", "Cities Ranking", "Indicators Check List"],
    icons=["bar-chart", "buildings", "list-check"],
    menu_icon="cast"
    )

if menu == "Data Visualizations":
    st.sidebar.header("Choose your filter")
    # Create filter by Domain
    domain = st.sidebar.selectbox("Select domain:", domain_list)

    # Create side bar filters
    if domain == "Inclusion": 
        kpi = st.sidebar.selectbox("Select KPI:", list(inclusion_kpis.keys()))
        dataset_code = inclusion_kpis[kpi]
    elif domain == "Sustainability":
        topic = st.sidebar.selectbox("Select topic:", sustainability_topics)
    else:
        kpi = st.sidebar.selectbox("Select KPI:", resilience_kpis)

# Add visualizations for Inclusion dashboard
if domain == "Inclusion":
    col1, col2, col3 = st.columns(3)
    with col1:
        chart_list = ["Line Chart", "Map", "Bar Chart", "Donut Chart"]
        chart = st.selectbox("Choose type of chart:", chart_list)
    if chart == "Line Chart":
        echarts_option('line_chart_inclusion', 'dataset_code', dataset_code)
    elif chart == "Map":
        plotly_chart('map_inclusion', 'dataset_code', dataset_code)
    elif chart == "Bar Chart":
        echarts_option('bar_chart_inclusion', 'dataset_code', dataset_code)
    else:
        echarts_option('donut_chart_inclusion', 'dataset_code', dataset_code)

# Add visualizations for Sustainability dashboard   
if domain == "Sustainability":
    
    if topic == "Air Quality":
        echarts_option_without_kpi('grouped_bar_chart_air_quality')
        
        col1, col2, col3 = st.columns(3)
        with col1:
            kpi_name = st.selectbox("Select KPI:", list(air_quality_kpis.keys()))
            kpi = air_quality_kpis[kpi_name]
        
        st.text("")
        figures = plotly_chart_cards('card_air_quality', 'kpi', kpi)
        cols = st.columns(len(figures))
        for i, fig in enumerate(figures):
            with cols[i]:
                st.plotly_chart(fig, use_container_width=True)      

        echarts_option('bar_chart_air_quality', 'kpi', kpi)
        
        echarts_option_without_kpi('line_chart_air_quality')
    
    if topic == "Energy":
        
        col1, col2 = st.columns(2)
        with col1:
            echarts_option_kpi('line_chart_energy', 'sdg_07_40', 'nrg_bal', 'REN')
        with col2:
            echarts_option_kpi('bar_chart_energy', 'sdg_07_40', 'nrg_bal', 'REN')
        
        col1, col2 = st.columns(2)
        with col1:
            kpi_name = st.selectbox("Select type of renewable energy source:", list(energy_kpis.keys()))
            dataset_code = energy_kpis[kpi_name]
            
        with col1:
            echarts_option_kpi('line_chart_energy', 'sdg_07_40', 'nrg_bal', dataset_code)
        with col2:
            st.header("")
            echarts_option_kpi('bar_chart_energy', 'sdg_07_40', 'nrg_bal', dataset_code)
            
        col1, col2, col3 = st.columns(3)
        with col1:
            geo_name = st.selectbox('Filter by country:', list(nat_dict.keys()))
            geo = nat_dict[geo_name]
      
        echarts_option_kpi('donut_chart_energy', 'sdg_07_40', 'geo', geo)
        
    if topic == "Biodiversity":
        
        col1, col2 = st.columns(2)
        with col1:
            echarts_option('bar_chart_TPA_prot_area', 'dataset_code', 'env_bio4')
        with col2:
            echarts_option('bar_chart_MPA_prot_area', 'dataset_code', 'env_bio4')
        with col1:
            echarts_option('grouped_bar_chart_prot_area', 'dataset_code', 'env_bio4')
        with col2:
            geo_name = st.selectbox('Filter by country:', list(nat_dict.keys()))
            geo = nat_dict[geo_name]
            echarts_option_kpi('donut_chart_prot_area', 'env_bio4', 'geo', geo)