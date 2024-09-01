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
        topic = st.sidebar.selectbox("Select sub-domain:", resilience_topics)

# Add visualizations for Inclusion dashboard
if domain == "Inclusion":
    
    st.title("🤝 Inclusion")
    st.text("")
    
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
        
        st.title("🌍 Environmental Sustainability")
        st.subheader("Air Quality")
        st.text("")
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
        
        st.title("🌍 Environmental Sustainability")
        st.subheader("Energy")
        st.text("")
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
        
        st.title("🌍 Environmental Sustainability")
        st.subheader("Biodiversity")
        st.text("")
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
            
    if topic == "Waste Management":
        
        st.title("🌍 Environmental Sustainability")
        st.subheader("Waste Management")
        st.text("")
        col1, col2, col3 = st.columns(3)
        with col1:
            geo_name = st.selectbox('Filter by country:', list(nat_dict.keys()))
            geo = nat_dict[geo_name]
            
        echarts_option_kpi('line_chart_waste', 'env_wastrt', 'geo', geo)
        echarts_option_kpi('donut_chart_waste', 'env_wastrt', 'geo', geo)
        
        col1, col2 = st.columns(2)
        with col1:
            echarts_option('line_chart_waste_recycled', 'dataset_code', 'env_wastrt')
        with col2:
            echarts_option('bar_chart_waste_recycled', 'dataset_code', 'env_wastrt')
            
    if topic == "Employment":
        
        st.title("🌍📈 Economic Sustainability")
        st.subheader("Employment")
        st.text("")
        
        col1, col2 = st.columns(2)
        with col1:
            echarts_option('line_chart_employment', 'dataset_code', 'tgs00007')
        with col2:
            geo_name = st.selectbox('Filter by nuts2 regions:', list(nuts2_dict.keys()))
            geo = nuts2_dict[geo_name]
            echarts_option_kpi('donut_chart_employment', 'tgs00007', 'geo', geo)
            
    if topic == "Infrastructure":
        
        st.title("🌍📈 Economic Sustainability")
        st.subheader("Infrastructure")
        st.text("")
        col1, col2 = st.columns(2)
        with col1:
            echarts_option('line_chart_infrastructure', 'dataset_code', 'tgs00047')
        with col2:
            echarts_option('bar_chart_infrastructure', 'dataset_code', 'tgs00047')
            
    if topic == "Innovation":
        
        st.title("🌍📈 Economic Sustainability")
        st.subheader("Innovation")
        st.text("")
        col1, col2 = st.columns(2)
        with col1:
            echarts_option('line_chart_innovation', 'dataset_code', 'rd_p_persreg')
        with col2:
            echarts_option('grouped_bar_chart_innovation', 'dataset_code', 'rd_p_persreg')
            
    if topic == "Health":
        
        st.title("🤝🌍 Social Sustainability")
        st.subheader("Health")
        st.text("")
        col1, col2 = st.columns(2)
        kpi = st.selectbox("Select KPI:", list(health_kpis.keys()))
        dataset_code = health_kpis[kpi]
        
        
    if topic == "Safety":
        
        st.title("🤝🌍 Social Sustainability")
        st.subheader("Safety")
        st.text("")
        col1, col2 = st.columns(2)
        with col1:
            echarts_option('line_chart_safety', 'dataset_code', 'urb_clivcon')
        with col2:
            echarts_option('bar_chart_safety', 'dataset_code', 'urb_clivcon')
        
    if topic == "Education":
        
        st.title("🤝🌍 Social Sustainability")
        st.subheader("Education")
        st.text("")
        col1, col2 = st.columns(2)
        with col1:
            echarts_option('line_chart_education', 'dataset_code', 'urb_ceduc')
        with col2:
            echarts_option('bar_chart_education', 'dataset_code', 'urb_ceduc')
        
# Add visualizations for Resilience dashboard   
if domain == "Resilience":

    if topic == "Social":
        
        st.title("🏙️🤝 Social Resilience")
        st.text("")
        
        kpi = st.selectbox("Select KPI:", list(social_resilience_kpis.keys()))
        dataset_code = social_resilience_kpis[kpi]
        
        echarts_option('line_chart_social_resilience', 'dataset_code', dataset_code)
        
        st.subheader("Education equality")
        st.text("")
        
        plotly_chart_without_kpi('bar_chart_educational_equality_by_sex')
        
        st.subheader("Demography")
        st.text("")
        
        col1, col2 = st.columns(2)
        with col1:
            echarts_option_without_kpi('donut_chart_demo_pop_productive_age')
        with col2:
            echarts_option_without_kpi('donut_chart_demo_pop_aged_65')
            
        echarts_option_without_kpi('bar_chart_demo_pop_density')
        
        st.subheader("Transportation access")
        st.text("")
        
        col1, col2 = st.columns(2)
        with col1:
            echarts_option_without_kpi('donut_chart_transportation_access')
        with col2:
            echarts_option_without_kpi('grouped_bar_chart_transportation_access')
        
    if topic == "Economic":
        st.title("🏙️📈 Economic Resilience")
        st.text("")
        
    if topic == "Infrastructure":
        st.title("🏗️💪 Infrastructure Resilience")
        st.text("")
        
    if topic == "Hazard":
        st.title("🚨🛡️ Hazard Resilience")
        st.text("")
        
    if topic == "Institutional":
        st.title("🏛️🔄 Institutional Resilience")
        st.text("")
        
        
    