from rest_framework.decorators import api_view
from rest_framework.response import Response
from data_charts.scripts.utils import *
from data_charts.scripts.charts import *
import plotly.express as px
import plotly.io as pio
import requests


# Create line chart view
@api_view(["GET"])
def line_chart_inclusion(request):
    
    kpi = request.GET.get("dataset_code")
    if kpi in ["tessi190", "tepsr_sp200"]:
        df = json_to_dataframe(kpi, 'nat')
    if kpi in ["ilc_li41", "tepsr_lm220", "educ_uoe_enra11", "ilc_lvhl21n", "edat_lfse_22"]:
        df = json_to_dataframe(kpi, 'nuts2')
    
    if kpi in ["tessi190", "tepsr_sp200"]:
        geo_name = {
            "DE": "Germany",
            "FI": "Finland",
            "SK": "Slovakia",
            "PT": "Portugal",
            "FR": "France"
        }        
        if kpi == "tessi190":
            kpi = "Gini coefficient (%)"
        else:
            df = df[(df['lev_limit'] == 'SM_SEV') & (df['sex'] == 'T')]
            kpi = "Disability employment gap (%)"
    
    if kpi in ["ilc_li41", "tepsr_lm220", "educ_uoe_enra11", "ilc_lvhl21n", "edat_lfse_22"]:
        geo_name = {
            "DEA2": "Köln",
            "FI1B": "Helsinki-U.",
            "SK03": "S. Slovensko",
            "PT17": "A. M. Lisboa",
            "FR10": "Ile France"
        }
        if kpi == "ilc_li41":
            kpi = "People at risk of poverty rate (%)"
        elif kpi == "tepsr_lm220":
            kpi = "Gender employment gap (%)"
        elif kpi == "educ_uoe_enra11":
            df = df[(df['sex'] == 'T') & (df['isced11'] == 'ED6')]
            kpi = "Equitable Bachelor's Enrolment"
        elif kpi == "ilc_lvhl21n":
            kpi = "Persons living in households with very low work intensity (%)"
        else:
            df = df[(df['sex'] == 'T') & (df['age'] == 'Y18-29')]
            kpi = "Youth Unemployment (%)"
        
    df = df[["values", "geo", "time"]]
    df['geo'] = df['geo'].replace(geo_name)

    common_years = df.groupby('geo')['time'].apply(set).reset_index()
    common_years = set.intersection(*common_years['time'])
    df = df[df['time'].isin(common_years)]
    
    df_grouped = df.groupby('geo').agg(list).reset_index()
    
    result = []
    colors = ['#6272A4', '#8BE9FD', '#FFB86C', '#FF79C6', '#BD93F9']
    
    for index, row in df_grouped.iterrows():
        data_dict = {
            'name': row['geo'],
            'type': 'line',
            'data': row['values'],
            'itemStyle': {'color': colors[index % len(colors)]}
        }
        result.append(data_dict)
                
    geo_list = df['geo'].unique().tolist()    
    year_list = df['time'].unique().tolist()
    
    option = line_chart(kpi, "", geo_list, year_list, result)
    
    return Response(option)


# Create map view
@api_view(["GET"])
def map_inclusion(request):
    
    dataset_code = request.GET.get("dataset_code")
    if dataset_code in ["tessi190", "tepsr_sp200"]:
        df = json_to_dataframe(dataset_code, 'nat')
    if dataset_code in ["ilc_li41", "tepsr_lm220", "educ_uoe_enra11", "ilc_lvhl21n", "edat_lfse_22"]:
        df = json_to_dataframe(dataset_code, 'nuts2')
    
    fig = d1_map_inclusion(df, dataset_code)
    fig_json = pio.to_json(fig)
    
    return Response(fig_json)


def d1_map_inclusion(df, kpi):
    
    if kpi in ["tessi190", "tepsr_sp200"]:
        geo_name = {
            'PT': 'Portugal',
            'DE': 'Germany',
            'FR': 'France',
            'FI': 'Finland',
            'SK': 'Slovakia'
        }
        df['geo_name'] = df['geo'].replace(geo_name)
        
        geo_code = {
            'PT': 'PRT',
            'DE': 'DEU',
            'FR': 'FRA',
            'FI': 'FIN',
            'SK': 'SVK'
        }
        
        if kpi == "tessi190":
            kpi = "Gini coefficient (%)"
        else:
            df = df[(df['lev_limit'] == 'SM_SEV') & (df['sex'] == 'T')]
            kpi = "Disability employment gap (%)"
    
    if kpi in ["ilc_li41", "tepsr_lm220", "educ_uoe_enra11", "ilc_lvhl21n", "edat_lfse_22"]:
        geo_name = {
            'PT17': 'Área Metropolitana de Lisboa',
            'DEA2': 'Köln',
            'FR10': 'Ile de France',
            'FI1B': 'Helsinki-Uusimaa',
            'SK03': 'Stredné Slovensko'
        }
        df['geo_name'] = df['geo'].replace(geo_name)
        geo_code = {
            'PT17': 'PRT',
            'DEA2': 'DEU',
            'FR10': 'FRA',
            'FI1B': 'FIN',
            'SK03': 'SVK'
        }
        if kpi == "ilc_li41":
            kpi = "People at risk of poverty rate (%)"
        elif kpi == "tepsr_lm220":
            kpi = "Gender employment gap (%)"
        elif kpi == "educ_uoe_enra11":
            df = df[(df['sex'] == 'T') & (df['isced11'] == 'ED6')]
            kpi = "Equitable Bachelor's Enrolment"
        elif kpi == "ilc_lvhl21n":
            kpi = "Persons living in households with very low work intensity (%)"
        else:
            df = df[(df['sex'] == 'T') & (df['age'] == 'Y18-29')]
            kpi = "Youth Unemployment (%)"
        
    df = df[['geo', 'time', 'geo_name', 'values']]
    
    df['geo'] = df['geo'].replace(geo_code)
    
    df = df.sort_values(by='time')
        
    geojson_url = 'https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/world-countries.json'
    response = requests.get(geojson_url)
    geojson = response.json()
    
    fig = px.choropleth_mapbox(
        df, 
        geojson=geojson, 
        locations='geo', 
        color='values',
        color_continuous_scale="YlGnBu",
        mapbox_style="open-street-map",
        zoom=2.2, 
        center = {"lat": 54.5260, "lon": 15.2551},
        opacity=0.5,
        hover_name="geo_name",
        labels={'values': kpi, 'geo': 'country_code', 'time': 'year'},
        animation_frame="time",
    )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    return fig


# Create bar chart view
@api_view(["GET"])
def bar_chart_inclusion(request):
    
    kpi = request.GET.get("dataset_code")
    if kpi in ["tessi190", "tepsr_sp200"]:
        df = json_to_dataframe(kpi, 'nat')
    if kpi in ["ilc_li41", "tepsr_lm220", "educ_uoe_enra11", "ilc_lvhl21n", "edat_lfse_22"]:
        df = json_to_dataframe(kpi, 'nuts2')

    if kpi in ["tessi190", "tepsr_sp200"]:
        geo_name = {
            "DE": "Germany",
            "FI": "Finland",
            "SK": "Slovakia",
            "PT": "Portugal",
            "FR": "France"
        }        
        if kpi == "tessi190":
            kpi = "Gini coefficient (%)"
        else:
            df = df[(df['lev_limit'] == 'SM_SEV') & (df['sex'] == 'T')]
            kpi = "Disability employment gap (%)"
    
    if kpi in ["ilc_li41", "tepsr_lm220", "educ_uoe_enra11", "ilc_lvhl21n", "edat_lfse_22"]:
        geo_name = {
            "DEA2": "Köln",
            "FI1B": "Helsinki-U.",
            "SK03": "S. Slovensko",
            "PT17": "A. M. Lisboa",
            "FR10": "Ile France"
        }
        if kpi == "ilc_li41":
            kpi = "People at risk of poverty rate (%)"
        elif kpi == "tepsr_lm220":
            kpi = "Gender employment gap (%)"
        elif kpi == "educ_uoe_enra11":
            df = df[(df['sex'] == 'T') & (df['isced11'] == 'ED6')]
            kpi = "Equitable Bachelor's Enrolment"
        elif kpi == "ilc_lvhl21n":
            kpi = "Persons living in households with very low work intensity (%)"
        else:
            df = df[(df['sex'] == 'T') & (df['age'] == 'Y18-29')]
            kpi = "Youth Unemployment (%)"
    
    max_year = df['time'].max()
    df = df[df['time'] == max_year]
    
    df = df[["values", "geo"]]
    
    df['geo'] = df['geo'].replace(geo_name)
    
    df = df.sort_values(by='values')

    geo_list = df['geo'].unique().tolist()
    values_list = df['values'].tolist()
    
    option = basic_bar_chart(kpi, "Year: " + str(max_year), geo_list, values_list)
    
    return Response(option)


# Create donut chart view
@api_view(['GET'])
def donut_chart_inclusion(request):
    
    kpi = request.GET.get("dataset_code")
    if kpi in ["tessi190", "tepsr_sp200"]:
        df = json_to_dataframe(kpi, 'nat')
    if kpi in ["ilc_li41", "tepsr_lm220", "educ_uoe_enra11", "ilc_lvhl21n", "edat_lfse_22"]:
        df = json_to_dataframe(kpi, 'nuts2')
    
    if kpi in ["tessi190", "tepsr_sp200"]:
        geo_name = {
            "DE": "Germany",
            "FI": "Finland",
            "SK": "Slovakia",
            "PT": "Portugal",
            "FR": "France"
        }      
        if kpi == "tessi190":
            kpi = "Gini coefficient (%)"
        else:
            df = df[(df['lev_limit'] == 'SM_SEV') & (df['sex'] == 'T')]
            kpi = "Disability employment gap (%)"
    
    if kpi in ["ilc_li41", "tepsr_lm220", "educ_uoe_enra11", "ilc_lvhl21n", "edat_lfse_22"]:
        geo_name = {
            "DEA2": "Köln",
            "FI1B": "Helsinki-U.",
            "SK03": "S. Slovensko",
            "PT17": "A. M. Lisboa",
            "FR10": "Ile France"
        }
        if kpi == "ilc_li41":
            kpi = "People at risk of poverty rate (%)"
        elif kpi == "tepsr_lm220":
            kpi = "Gender employment gap (%)"
        elif kpi == "educ_uoe_enra11":
            df = df[(df['sex'] == 'T') & (df['isced11'] == 'ED6')]
            kpi = "Equitable Bachelor's Enrolment"
        elif kpi == "ilc_lvhl21n":
            kpi = "Persons living in households with very low work intensity (%)"
        else:
            df = df[(df['sex'] == 'T') & (df['age'] == 'Y18-29')]
            kpi = "Youth Unemployment (%)"
    
    max_year = df['time'].max()
    df = df[df['time'] == max_year]
    
    df = df[["values", "geo"]]
    
    df['geo'] = df['geo'].replace(geo_name)

    total = df['values'].sum()
    df['normalized_values'] = df['values'] / total * 100
    df['normalized_values'] = df['normalized_values'].round(2)
    
    colors = ['#50FA7B', '#44475A', '#FF79C6', '#FFB86C', '#282A36']

    data = [
        {'value': row['normalized_values'], 'name': row['geo']}
        for _, row in df.iterrows()
    ]
    
    option = donut_chart(kpi, 'Year: ' + str(max_year), data, colors)
    
    return Response(option)