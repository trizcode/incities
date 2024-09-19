import streamlit as st
from streamlit_option_menu import option_menu
from utils import *
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
        sub_domain = st.sidebar.selectbox("Select sub-domain:", sub_domain_inclusion)
    elif domain == "Sustainability":
        sub_domain = st.sidebar.selectbox("Select sub-domain:", sub_domain_sustainability)
    else:
        sub_domain = st.sidebar.selectbox("Select sub-domain:", sub_domain_resilience)

# Add visualizations for Inclusion dashboard
if domain == "Inclusion":
    
    if sub_domain == "Social":
        
        st.title("🤝 Social Inclusion")
        st.text("")
        col1, col2, col3 = st.columns(3)
        with col1:
            kpi = st.selectbox("Select KPI:", list(social_inclusion_kpis.keys()))
            dataset_code = social_inclusion_kpis[kpi]
        with col2:
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
            
    elif sub_domain == "Economic":
        
        st.title("🤝 Economic Inclusion")
        st.text("")
        col1, col2, col3 = st.columns(3)
        with col1:
            kpi = st.selectbox("Select KPI:", list(economic_inclusion_kpis.keys()))
            dataset_code = economic_inclusion_kpis[kpi]
        with col2:
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
            
    else:
        st.title("🤝 Gender Inclusion")
        st.text("")
        col1, col2, col3 = st.columns(3)
        with col1:
            kpi = st.selectbox("Select KPI:", list(gender_inclusion_kpis.keys()))
            dataset_code = gender_inclusion_kpis[kpi]
        with col2:
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
      
    if sub_domain == "Environmental":
        
        st.title("🌍 Environmental Sustainability")
        topic = st.sidebar.selectbox("Select topic:", environment_sustainability_topics)
        
        if topic == "Air Quality":
            col1, col2, col3 = st.columns(3)
            with col1:
                kpi_name = st.selectbox("Select KPI:", list(air_quality_kpis.keys()))
                kpi = air_quality_kpis[kpi_name]
            if kpi == "cei_gsr011":
                with col2:
                    chart_list = ["Line Chart", "Bar Chart"]
                    chart = st.selectbox("Choose type of chart:", chart_list)
                if chart == "Line Chart":
                    echarts_option('line_chart_GHG', 'dataset_code', kpi)
                else:
                    echarts_option('bar_chart_GHG', 'dataset_code', kpi)
            else:
                echarts_option('bar_chart_air_quality', 'kpi', kpi)  
                figures = plotly_chart_cards('card_air_quality', 'kpi', kpi)
                cols = st.columns(len(figures))
                for i, fig in enumerate(figures):
                    with cols[i]:
                        st.plotly_chart(fig, use_container_width=True)    
        
        if topic == "Energy":
            col1, col2, col3 = st.columns(3)
            with col1:
                kpi_name = st.selectbox("Select KPI:", list(energy_kpis.keys()))
                dataset_code = energy_kpis[kpi_name]
            with col2:
                chart_list = ["Line Chart", "Bar Chart"]
                chart = st.selectbox("Choose type of chart:", chart_list)
            if chart == "Line Chart":
                echarts_option_kpi('line_chart_energy', 'sdg_07_40', 'nrg_bal', dataset_code)
            if chart == "Bar Chart":
                echarts_option_kpi('bar_chart_energy', 'sdg_07_40', 'nrg_bal', dataset_code)
        
        if topic == "Biodiversity":
                echarts_option('bar_chart_TPA_prot_area', 'dataset_code', 'env_bio4')

        if topic == "Environmental quality":
            col1, col2, col3 = st.columns(3)
            with col1:
                chart_list = ["Line Chart", "Bar Chart"]
                chart = st.selectbox("Choose type of chart:", chart_list)
            if chart == "Line Chart":
                echarts_option('line_chart_waste_recycled', 'dataset_code', 'env_wastrt')
            else:
                echarts_option('bar_chart_waste_recycled', 'dataset_code', 'env_wastrt')
            
    if sub_domain == "Economic":
        
        st.title("🌍📈 Economic Sustainability")
        col1, col2, col3 = st.columns(3)
        with col1:
            chart_list = ["Line Chart", "Bar Chart"]
            chart = st.selectbox("Choose type of chart:", chart_list)
        if chart == "Line Chart":
            echarts_option_without_kpi('line_chart_employment')
        else:
            plotly_chart_without_kpi('bar_chart_employment')
            
    if sub_domain == "Social":
        
        st.title("🤝🌍 Social Sustainability")
        topic = st.sidebar.selectbox("Select topic:", social_sustainability_topics)
               
        if topic == "Safety":
            col1, col2, col3 = st.columns(3)
            with col1:
                chart_list = ["Line Chart", "Bar Chart"]
                chart = st.selectbox("Choose type of chart:", chart_list)
            if chart == "Line Chart":
                echarts_option_without_kpi('line_chart_safety')
            else:
                echarts_option_without_kpi('bar_chart_safety')

        if topic == "Education":
            col1, col2, col3 = st.columns(3)
            with col1:
                chart_list = ["Line Chart", "Bar Chart"]
                chart = st.selectbox("Choose type of chart:", chart_list)
            if chart == "Line Chart":
                echarts_option_without_kpi('line_chart_education')
            else:
                echarts_option_without_kpi('bar_chart_education')

# Add visualizations for Resilience dashboard   
if domain == "Resilience":

    if sub_domain == "Social":
        
        st.title("🏙️🤝 Social Resilience")
        topic = st.sidebar.selectbox("Select topic:", social_resilience_topics)
        
        if topic == "Educational equality":
            plotly_chart_without_kpi('bar_chart_educational_equality_by_sex')
        
        if topic == "Demography":
            col1, col2, col3 = st.columns(3)
            with col1:
                kpi = st.selectbox("Select KPI:", list(demography_kpis.keys()))
                dataset_code = demography_kpis[kpi] 
            if dataset_code == "demo_r_pjangrp3":  
                echarts_option_without_kpi('donut_chart_demo_pop_productive_age')
            if dataset_code == "demo_r_pjangrp3_aged":
                echarts_option_without_kpi('donut_chart_demo_pop_aged_65')
            if dataset_code == "demo_r_d3dens":
                echarts_option_without_kpi('bar_chart_demo_pop_density')
        
    if sub_domain == "Economic":
        st.title("🏙️📈 Economic Resilience")
        col1, col2, col3 = st.columns(3)
        with col1:
            chart_list = ["Line Chart", "Bar Chart"]
            chart = st.selectbox("Choose type of chart:", chart_list)
        if chart == "Line Chart":
            echarts_option('line_chart_economic_resilience', 'dataset_code', 'tgs00006')
        else:
            echarts_option('bar_chart_economic_resilience', 'dataset_code', 'tgs00006')
         
    if sub_domain == "Infrastructure":
        st.title("🏗️💪 Infrastructure Resilience")
        col1, col2, col3 = st.columns(3)
        with col1:
            chart_list = ["Line Chart", "Bar Chart"]
            chart = st.selectbox("Choose type of chart:", chart_list)
        if chart == "Line Chart":
            echarts_option_without_kpi('line_chart_infrastructure_resilience')
        else:
            echarts_option_without_kpi('bar_chart_infrastructure_resilience')
        
    if sub_domain == "Hazard":
        st.title("🚨🛡️ Hazard Resilience")
        st.text("")
        
    if sub_domain == "Institutional":
        st.title("🏛️🔄 Institutional Resilience")
        col1, col2, col3 = st.columns(3)
        with col1:
            chart_list = ["Line Chart", "Bar Chart"]
            chart = st.selectbox("Choose type of chart:", chart_list)
        if chart == "Line Chart":
            echarts_option_without_kpi('line_chart_institutional_resilience')
        else:
            echarts_option_without_kpi('bar_chart_institutional_resilience')
        
        
    