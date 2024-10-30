import requests
import streamlit as st
import plotly.io as pio
from streamlit_echarts import st_echarts
import pandas as pd
import plotly.express as px


# Define domains
domain_list = ["Inclusion", "Sustainability", "Resilience"]

# Define sub-domains
sub_domain_inclusion = ["Social", "Economic", "Gender"]

sub_domain_sustainability = ["Environmental", "Social", "Economic"]

sub_domain_resilience = ["Social", "Economic", "Infrastructure", "Institutional", "Hazard"]

# Define sub-domain kpis
social_inclusion_kpis = { 
    "Disability employment gap": "tepsr_sp200",
    "Youth Unemployment": "edat_lfse_22",
    "Slum Household": "ilc_lvhl21n"
}

economic_inclusion_kpis = {
    "Gini coefficient": "tessi190",
    "Poverty Rate": "ilc_li41"
}

gender_inclusion_kpis = {
    "Gender employment gap": "tepsr_lm220",
    "Equitable Bachelor's Enrolment": "educ_uoe_enra11"
}

environment_sustainability_topics = ["Air Quality", "Energy", "Biodiversity", "Environmental quality"]

economic_sustainability_topics = ["Employment", "Infrastructure", "Innovation"]

social_resilience_topics = ["Educational equality", "Demography", "Transportation access"]

economic_resilience_topics = ["Health access", "Market access"]

air_quality_kpis = {
    "Greenhouse gas (GHG) emissions": "cei_gsr011",
    "Concentration of NO2 (µg/m³)": "no2", 
    "Concentration of PM10 (µg/m³)": "pm10",
}

energy_kpis = {
    "Renewable energy sources": "REN",
    "Renewable energy sources in transport": "REN_TRA",
    "Renewable energy sources in electricity": "REN_ELC",
    "Renewable energy sources in heating and cooling": "REN_HEAT_CL",
}

economic_sustainability_kpis = {
    "Persons employed in productive age": "tgs00007",
    "Household level of internet access": "tgs00047",
    "HR in science and technology": "tgs00038"
}

social_sustainability_kpis = {
    "Share of murders and violent deaths": "urb_clivcon",
    "Share of students in higher education": "urb_ceduc",
    "Share of total deaths": "hlth_cd_yro",
    "Infant mortality": "hlth_cd_yinfr"
}

edu_equality_kpis = {
    "Tertiary educational attainment": "tgs00109",
    "Population with 0-2 educational levels": "edat_lfse_04"
}

demography_kpis = {
    "Population in productive age": "demo_r_pjangrp3",
    "Population aged 65 years and older": "demo_r_pjangrp3_aged",
    "Population density": "demo_r_d3dens"
}

economic_resilience_kpis = {
    "Regional gross domestic product": "tgs00006",
    "Number of Physicians": "hlth_rs_physreg"
}

# Define regions
nat_dict = {
    "Finland": "FI",
    "Portugal": "PT",
    "Slovakia": "SK", 
    "France": "FR", 
    "Germany": "DE"
}

nuts2_dict = {
    "Köln": "DEA2",
    "Helsinki-U.": "FI1B",
    "S. Slovensko": "SK03",
    "A. M. Lisboa": "PT17",
    "Ile de France": "FR10"
}


# Functions to display data visualizations
def echarts_option(echarts_function, key_name, kpi):
    
    response = requests.get(f'http://localhost:8000/data_charts/{echarts_function}/?{key_name}={kpi}')
    chart_option = response.json()
    st_echarts(options=chart_option, height="500px")


def echarts_option_without_kpi(echarts_function):
    
    response = requests.get(f'http://localhost:8000/data_charts/{echarts_function}/')
    chart_option = response.json()
    st_echarts(options=chart_option, height="500px")
    

def echarts_option_kpi(echarts_function, dataset_code, col_kpi, kpi):
    response = requests.get(f"http://localhost:8000/data_charts/{echarts_function}/?dataset_code={dataset_code}&{col_kpi}={kpi}")
    chart_option = response.json()
    st_echarts(options=chart_option, height="500px")


def plotly_chart(plotly_chart, key_name, kpi):
    
    response = requests.get(f'http://localhost:8000/data_charts/{plotly_chart}/?{key_name}={kpi}')
    fig_json = response.json()
    fig = pio.from_json(fig_json)
    st.plotly_chart(fig)


def plotly_chart_without_kpi(plotly_chart):
    
    response = requests.get(f'http://localhost:8000/data_charts/{plotly_chart}/')
    fig_json = response.json()
    fig = pio.from_json(fig_json)
    st.plotly_chart(fig)
    
    
def plotly_chart_cards(plotly_chart, key_name, kpi):

    response = requests.get(f'http://localhost:8000/data_charts/{plotly_chart}/?{key_name}={kpi}')
    figures_json = response.json()
    figures = [pio.from_json(fig_json) for fig_json in figures_json]
    return figures


# Add charts for hazard resilience
def hazard_resilience():
    
    df = pd.read_excel('Emdat_database.xlsx', header=0, sheet_name='EM-DAT Data')

    col1, col2, col3 = st.columns(3)
    with col1:
        kpi_list = ["Frequency of disaster", "Variety of natural disasters"]
        kpi = st.selectbox('Select KPI:', kpi_list)
        
    if kpi == "Frequency of disaster":
        
        df = df.groupby(['Start Year', 'Country']).size().reset_index(name='Frequency of Disasters')
        df = df.groupby('Country')['Frequency of Disasters'].mean().reset_index()
        df.columns = ['geo', 'values']
        df = df.sort_values(by='values').round(2)
        
        geo_list = df['geo'].unique().tolist()
        values_list = df['values'].tolist()
        
        color_mapping = {
            "Germany": "#6272A4",
            "Finland": "#8BE9FD",
            "Slovakia": "#FFB86C",
            "Portugal": "#FF79C6",
            "France": "#BD93F9"
        }
        colors = [color_mapping.get(region) for region in geo_list]
        
        series_data = [{"value": y, "itemStyle": {"color": c}} for y, c in zip(values_list, colors)]

        option = {
            "title": {"text": "Frequency of disasters", "subtext": "Average per year"},
            "grid": {'top': '15%', 'right': '5%', 'bottom': '5%', 'left': '5%', 'containLabel': 'true'},
            "tooltip": {},
            "xAxis": {
                "type": 'category',
                "data": geo_list,
            },
            "yAxis": {
                "type": 'value'
            },
            "series": [
                {
                    "data": series_data,
                    "type": 'bar'
                }
            ]
        }
        
        st_echarts(options=option, height="500px")
        
    else:
        with col2:
            df = df[df['Disaster Group'] == 'Natural']
            disaster_type_list = df['Disaster Type'].unique().tolist()
            disaster_type = st.selectbox('Select disaster type:', disaster_type_list)
        
        df = df[df['Disaster Type'] == disaster_type]
        
        color_mapping = {
            "Germany": "#6272A4",
            "Finland": "#8BE9FD",
            "Slovakia": "#FFB86C",
            "Portugal": "#FF79C6",
            "France": "#BD93F9"
        } 
        with col3:
            view_mode = st.radio("Select chart view:", options=["Stacked", "Split by Country"], index=0)

        if view_mode == "Stacked":
            fig = px.bar(
                df,
                x="Start Year",
                y="Total Deaths",
                color="Country",
                title="Total Deaths by Year and Country",
                labels={"Start Year": "Year", "Total Deaths": "Total Deaths"},
                hover_data=["Disaster Type", "Disaster Group"],
                color_discrete_map=color_mapping
            )
            fig.update_layout(
                height=500
            )
            
        else:
            fig = px.bar(
                df,
                x="Start Year",
                y="Total Deaths",
                color="Country",
                title="Total Deaths by Year and Country (Split by Country)",
                labels={"Start Year": "Year", "Total Deaths": "Total Deaths"},
                hover_data=["Disaster Type", "Disaster Group"],
                facet_col="Country",
                facet_col_wrap=2,
                color_discrete_map=color_mapping
            )
        
            fig.update_layout(
                height=800
            )
        
        fig.update_layout(
            xaxis=dict(
                rangeslider=dict(visible=True),
                type="linear"
            ),
            xaxis_title="Year",
            yaxis_title="Total Deaths",
        )
        
        st.plotly_chart(fig)
        
        
def add_informative_texts(dataset_code):
    
    if dataset_code == "tepsr_sp200":
        text = "The disability employment gap is defined as the difference between the employment rates of people with no and those with some or severe limitation in their daily activities, aged 20-64. The employment rate is calculated by dividing the number of persons aged 20 to 64 in employment by the total population of the same age group."
    elif dataset_code == "edat_lfse_22":
        text = "The indicator on young people neither in employment nor in education and training (NEET) corresponds to the percentage of the population of a given age group and sex who is not employed and not involved in further education or training. The numerator of the indicator refers to persons who meet the following two conditions: (a) they are not employed (i.e. unemployed or inactive according to the International Labour Organisation definition) and (b) they have not received any education or training (i.e. neither formal nor non-formal) in the four weeks preceding the survey."
    elif dataset_code == "ilc_lvhl21n":
        text = "The indicator persons living in households with very low work intensity is defined as the number of persons living in a household where the members of working age worked a working time equal or less than 20% of their total work-time potential during the previous year."
    else:
        text = "No text available yet."
    return text