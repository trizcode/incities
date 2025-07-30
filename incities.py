import streamlit as st
from streamlit_option_menu import option_menu
from utils import *
from PCA import *
import pandas as pd
from sqlalchemy import create_engine
import warnings
warnings.filterwarnings('ignore')

DB_NAME = 'emdat_db'
DB_USER = 'postgres'
DB_PASSWORD = 'admin'
DB_HOST = 'localhost'
DB_PORT = '5432'

engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

st.set_page_config(page_title="InCITIES", page_icon=":cityscape:", layout="wide")

# Create Menu side bar
with st.sidebar:
    menu = option_menu(
    menu_title="Menu",
    options=["Indicators Charts", "Cities Ranking", "Check List"],
    icons=["bar-chart", "buildings", "list-check"],
    menu_icon="cast"
    )

if menu == "Indicators Charts":
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
                chart_list = ["Line Chart", "Map", "Bar Chart"]
                chart = st.selectbox("Choose type of chart:", chart_list)
            if chart == "Line Chart":
                echarts_option('line_chart_inclusion', 'dataset_code', dataset_code)
            elif chart == "Map":
                plotly_chart('map_inclusion', 'dataset_code', dataset_code)
            else:
                echarts_option('bar_chart_inclusion', 'dataset_code', dataset_code)
            
            with st.expander("About KPI"):
                st.caption(add_informative_texts(dataset_code))
                
        elif sub_domain == "Economic":
            
            st.title("🤝 Economic Inclusion")
            st.text("")
            col1, col2, col3 = st.columns(3)
            with col1:
                kpi = st.selectbox("Select KPI:", list(economic_inclusion_kpis.keys()))
                dataset_code = economic_inclusion_kpis[kpi]
            with col2:
                chart_list = ["Line Chart", "Map", "Bar Chart"]
                chart = st.selectbox("Choose type of chart:", chart_list)
            if chart == "Line Chart":
                echarts_option('line_chart_inclusion', 'dataset_code', dataset_code)
            elif chart == "Map":
                plotly_chart('map_inclusion', 'dataset_code', dataset_code)
            else:
                echarts_option('bar_chart_inclusion', 'dataset_code', dataset_code)
                
            with st.expander("About KPI"):
                st.caption(add_informative_texts(dataset_code))
                
        else:
            st.title("🤝 Gender Inclusion")
            st.text("")
            col1, col2, col3 = st.columns(3)
            with col1:
                kpi = st.selectbox("Select KPI:", list(gender_inclusion_kpis.keys()))
                dataset_code = gender_inclusion_kpis[kpi]
            with col2:
                chart_list = ["Line Chart", "Map", "Bar Chart"]
                chart = st.selectbox("Choose type of chart:", chart_list)
            if chart == "Line Chart":
                echarts_option('line_chart_inclusion', 'dataset_code', dataset_code)
            elif chart == "Map":
                plotly_chart('map_inclusion', 'dataset_code', dataset_code)
            else:
                echarts_option('bar_chart_inclusion', 'dataset_code', dataset_code)
                
            with st.expander("About KPI"):
                st.caption(add_informative_texts(dataset_code))


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
                            
                with st.expander("About KPI"):
                    st.caption(add_informative_texts(kpi))   
            
            if topic == "Energy":
                col1, col2, col3 = st.columns(3)
                #with col1:
                #    kpi_name = st.selectbox("Select KPI:", list(energy_kpis.keys()))
                #    dataset_code = energy_kpis[kpi_name]
                with col1:
                    chart_list = ["Line Chart", "Bar Chart"]
                    chart = st.selectbox("Choose type of chart:", chart_list)
                if chart == "Line Chart":
                    echarts_option_kpi('line_chart_energy', 'sdg_07_40', 'nrg_bal', 'REN')
                if chart == "Bar Chart":
                    echarts_option_kpi('bar_chart_energy', 'sdg_07_40', 'nrg_bal', 'REN')   
                with st.expander("About KPI"):
                    st.caption(add_informative_texts('REN'))   
            
            if topic == "Biodiversity":
                    echarts_option('bar_chart_TPA_prot_area', 'dataset_code', 'env_bio4')
                    with st.expander("About KPI"):
                        st.caption(add_informative_texts('env_bio4'))   

            if topic == "Environmental quality":
                col1, col2, col3 = st.columns(3)
                with col1:
                    chart_list = ["Line Chart", "Bar Chart", "Donut Chart"]
                    chart = st.selectbox("Choose type of chart:", chart_list)
                if chart == "Line Chart":
                    echarts_option('line_chart_waste_recycled', 'dataset_code', 'env_wastrt')
                elif chart == "Bar Chart":
                    echarts_option('bar_chart_waste_recycled', 'dataset_code', 'env_wastrt')
                else:
                    echarts_option('donut_chart_waste_recycled', 'dataset_code', 'env_wastrt')
                with st.expander("About KPI"):
                    st.caption(add_informative_texts('env_wastrt'))
                
        if sub_domain == "Economic":
            
            st.title("🌍📈 Economic Sustainability")
            col1, col2, col3 = st.columns(3)
            with col1:
                    kpi_name = st.selectbox("Select KPI:", list(economic_sustainability_kpis.keys()))
                    dataset_code = economic_sustainability_kpis[kpi_name]
            with col2:
                chart_list = ["Line Chart", "Bar Chart"]
                chart = st.selectbox("Choose type of chart:", chart_list)
            if chart == "Line Chart":
                echarts_option('line_chart_economic_sustainability', 'dataset_code', dataset_code)
            else:
                echarts_option('bar_chart_economic_sustainability', 'dataset_code', dataset_code)
                
        if sub_domain == "Social":
            
            st.title("🤝🌍 Social Sustainability")
        
            col1, col2, col3 = st.columns(3)
            with col1:
                kpi_name = st.selectbox("Select KPI:", list(social_sustainability_kpis.keys()))
                dataset_code = social_sustainability_kpis[kpi_name]
            with col2:
                chart_list = ["Line Chart", "Bar Chart"]
                chart = st.selectbox("Choose type of chart:", chart_list)
            if chart == "Line Chart":
                echarts_option('line_chart_social_sustainability', 'dataset_code', dataset_code)
            else:
                echarts_option('bar_chart_social_sustainability', 'dataset_code', dataset_code)

    # Add visualizations for Resilience dashboard   
    if domain == "Resilience":

        if sub_domain == "Social":
            
            st.title("🏙️🤝 Social Resilience")
            topic = st.sidebar.selectbox("Select topic:", social_resilience_topics)
            
            if topic == "Educational equality":
                col1, col2, col3 = st.columns(3)
                with col1:
                    kpi = st.selectbox("Select KPI:", list(edu_equality_kpis.keys()))
                    dataset_code = edu_equality_kpis[kpi]
                with col2:
                    chart_list = ["Line Chart", "Bar Chart"]
                    chart = st.selectbox("Type of chart:", chart_list)
                
                if chart == "Line Chart":
                    echarts_option('line_chart_educational_equality', 'dataset_code', dataset_code)
                else:
                    echarts_option('bar_chart_educational_equality', 'dataset_code', dataset_code)
                
            
            elif topic == "Demography":
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
            else:
                echarts_option_without_kpi('donut_chart_transportation_access')
            
        if sub_domain == "Economic":
            st.title("🏙️📈 Economic Resilience")
            col1, col2, col3 = st.columns(3)
            with col1:
                kpi = st.selectbox("Select KPI:", list(economic_resilience_kpis.keys()))
                dataset_code = economic_resilience_kpis[kpi] 
            with col2:
                chart_list = ["Line Chart", "Bar Chart"]
                chart = st.selectbox("Choose type of chart:", chart_list)
            if chart == "Line Chart":
                echarts_option('line_chart_economic_resilience', 'dataset_code', dataset_code)
            else:
                echarts_option('bar_chart_economic_resilience', 'dataset_code', dataset_code)
            
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
            
            hazard_resilience()
            
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
        
        
if menu == "Check List":
    
    col1, col2 = st.columns(2)
    with col1:
        st.header("Indicators Check List")
    with col2:
        ind_list = ["All indicators used", "Indicators that need improvement"]
        user_choice = st.selectbox("", ind_list)
    
    query = 'SELECT * FROM kpi_list'
    df = pd.read_sql(query, engine)
    
    st.sidebar.header("Choose your filter")
    domain_list = df["Domain"].unique()
    domain = st.sidebar.selectbox("Select domain:", domain_list)
    
    df = df[df["Domain"] == domain]
    
    if user_choice == "Indicators that need improvement":
        df.dropna(subset=['Notes'], inplace=True)
    
    df.fillna("-", inplace=True)
    df = df[["Indicator", "Database", "Spatial Level", "Notes"]]
    
    st.text("")
    
    st.table(df)

    
if menu == "Cities Ranking":

    query = 'SELECT * FROM pca'
    df = pd.read_sql(query, engine)
    
    st.sidebar.header("Choose your filter")
    
    domain_name = ["Inclusion", "Sustainability", "Resilience"]
    domain = st.sidebar.selectbox("Select domain:", domain_name)
    
    if domain == "Inclusion":
        ind_list = [
        'tessi190', 
        'tepsr_sp200',  
        'edat_lfse_22', 
        'ilc_lvhl21n', 
        'ilc_li41',
        'tepsr_lm220'
        ]
        ind_name = {
            "tessi190": "gini_coef",
            "tepsr_sp200": "disab_empl_gap",
            "edat_lfse_22": "you_peo_neet",
            "ilc_lvhl21n": "house_low_work_int",
            "ilc_li41": "risk_pvt_rate",
            "tepsr_lm220": "gen_empl_gap", 
        }
    elif domain == "Sustainability":
        ind_list = [
            'tgs00007',
            'cei_gsr011',
            'env_wastrt',
            'sdg_07_40',
            'hlth_cd_yro',
            'hlth_cd_yinfr',
            'urb_clivcon',
            'urb_ceduc',
            'tgs00038'
        ]
        ind_name = {
            "tgs00007": "empl_rate",
            "cei_gsr011": "ghg_emiss",
            "env_wastrt": "waste_recy",
            "sdg_07_40": "renew_energy",
            "hlth_cd_yro": "nr_deaths",
            "hlth_cd_yinfr": "inf_mort", 
            "urb_clivcon": "murd_viol_death", 
            "urb_ceduc": "stu_high_edu", 
            "tgs00038": "hr_scie_tech"
        }
    else:
        ind_list = [
            'tgs00109',
            'tgs00006',
            'edat_lfse_04',
            'pop_prod_age',
            'pop_aged_65',
            'demo_r_d3dens',
            'tin00129'
        ]
        ind_name = {
            "tgs00109": "tert_edu_attain",
            "tgs00006": "reg_gross_dom_p",
            "edat_lfse_04": "pop_0_2_edu_lev",
            "demo_r_d3dens": "pop_density",
            "tin00129": "consul_or_vote"
        }
    
    df = df[df['dataset_code'].isin(ind_list)]
    df['dataset_code'] = df['dataset_code'].replace(ind_name)

    df = df.pivot_table(index=['geo', 'time'], columns='dataset_code', values='values')
    df = replace_NaN_values(df)
    df = normalize_data(df)
    
    corr_matrix = df.corr().round(3)
          
    with st.expander("Correlation Matrix"):
        corr_matrix_plot(corr_matrix)
        st.table(corr_matrix)
        
    with st.expander("Kaiser-Meyer-Olkin (KMO) Measure"):
        KMO_measure(corr_matrix)
    
    if domain == "Sustainability":
        with st.expander("Principal Component Eigenvalues"):
            pca_result_df = principal_component_analysis(df)
            st.table(pca_result_df)
            get_loadings_table(df)
        
        get_final_ranking(df, pca_result_df)
        
        col1, col2, col3 = st.columns(3) 
        with col1:
            city_name = ["Helsinki", "Paris", "Cologne", "Lisbon", "Zilina"]
            city = st.selectbox("Select city:", city_name)
        
        radar_plot(df, city)
        radar_plot_all_cities(df)
        
    else:        
        col1, col2, col3 = st.columns(3) 
        with col1:
            city_name = ["Helsinki", "Paris", "Cologne", "Lisbon", "Zilina"]
            city = st.selectbox("Select city:", city_name)
 
        radar_plot(df, city)
        radar_plot_all_cities(df)