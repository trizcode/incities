from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import *
from .charts import *


# ----------------------- Social Resilience -----------------------

@api_view(["GET"])
def dash3_chart_1(request):
    dataset_code = request.GET.get("dataset_code")
    df = json_to_dataframe(dataset_code)
    indicator = request.GET.get("ind")
    return d3_line_chart_social_resilience(dataset_code, indicator, df)


def d3_line_chart_social_resilience(kpi, indicator, df):
		
    if kpi == "demo_r_pjangrp3": 
        geo_name = {
            "DEA23": "Köln, Kreisfreie Stadt",
            "FR101": "Paris",
            "PT170": "Área Metropolitana de Lisboa",
            "SK031": "Žilinský kraj",
            "FI1B1": "Helsinki-Uusimaa"
            }
        geo_nuts2 = ["DEA23", "FR101", "PT170", "SK031", "FI1B1"]
        df = df[df['geo'].isin(geo_nuts2)]
        
        if indicator == "Total":
            df = df[(df['values'].notnull()) & (df['sex']== 'T') & (df['age']== 'TOTAL')]
            df = df[["values", 'geo', "time"]]
            kpi = "Total Population on 1 January"
        else:
            df = df[(df['values'].notnull()) & (df['sex'] == 'T') & (df['age'].isin(['Y65-69', 'Y70-74', 'Y75-79','Y80-84', 'Y85-89', 'Y_GE85','Y_GE90']))]
            df = df[["values", 'geo', "time"]]
            df = df.groupby(['geo', 'time'])['values'].sum().reset_index()
            df = df.sort_values('time')
            kpi = "Proportion of population aged 65 and over"
            
    if kpi in ["tgs00109", "tgs00108"]:
            
        geo_name = {
            "DEA2": "Köln",
            "FI1B": "Helsinki-Uusimaa",
            "SK03": "Stredné Slovensko",
            "PT17": "Área M. de Lisboa",
            "FR10": "Ile de France"
        }
        geo_nuts2 = ["DEA2", "FI1B", "SK03", "FR10", "PT17"]
        df = df[df['geo'].isin(geo_nuts2)]
        
        if kpi == "tgs00109":
            df = df[(df['values'].notnull()) & (df['sex']== 'T')]
            df = df[["values", 'geo', "time"]]
            kpi = "Tertiary educational attainment of population in age group 24-64 years (%)"
        else:
            df = df[(df['values'].notnull())]
            df = df[["values", 'geo', "time"]]
            kpi = "People living in households with very low work intensity (%)"

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
                'itemStyle': {
                'color': colors[index % len(colors)]
        }
        }
        result.append(data_dict)
                            
    geo_list = df['geo'].unique().tolist()    
    year_list = df['time'].unique().tolist()

    option = line_chart(kpi, geo_list, year_list, result)
    return Response(option)


@api_view(["GET"])
def dash3_chart_2(request):
    dataset_code = "demo_r_pjangrp3"
    df = json_to_dataframe(dataset_code)
    year = request.GET.get("year")
    return d3_bar_chart_population_by_age_group(year, df)


def d3_bar_chart_population_by_age_group(year, df):
    
    geo_nuts2 = ["DEA23", "FR101", "PT170", "SK031", "FI1B1"]
    df = df[df['geo'].isin(geo_nuts2)]
    df = df[(df['values'].notnull()) & (df['time'] == year) & (df['age'].isin(['TOTAL', 'UNK']) == False) & (df['sex'] == 'T')]
    df = df[['values', 'geo', 'age']]

    geo_name = {
        "DEA23": "Köln",
        "FR101": "Paris",
        "PT170": "Área M. de Lisboa",
        "SK031": "Žilinský kraj",
        "FI1B1": "Helsinki-Uusimaa"
    }
    df['geo'] = df['geo'].replace(geo_name)

    df['age'] = df['age'].replace(
    {'Y_LT5': 'Children',
        'Y5-9': 'Children', 
        'Y10-14': 'Children',
        'Y15-19': 'Young adults',
        'Y20-24': 'Young adults',
        'Y25-29': 'Young adults',
        'Y30-34': 'Young adults',
        'Y35-39': 'Young adults',
        'Y40-44': 'Middle-aged Adults',
        'Y45-49': 'Middle-aged Adults',
        'Y50-54': 'Middle-aged Adults',
        'Y55-59': 'Middle-aged Adults',
        'Y60-64': 'Old Adults',
        'Y65-69': 'Old Adults',
        'Y70-74': 'Old Adults',
        'Y75-79': 'Old Adults',
        'Y80-84': 'Old Adults',
        'Y85-89': 'Old Adults',
        'Y_GE85': 'Old Adults',
        'Y_GE90': 'Old Adults'
    })

    df = df.groupby(['geo', 'age'])['values'].sum().reset_index()

    dimensions = ['geo'] + ['Children'] + ['Young adults'] + ['Middle-aged Adults'] + ['Old Adults']
    pivot_df = df.pivot(index='geo', columns='age', values='values').reset_index()
    source = pivot_df.to_dict(orient='records')
    
    option = bar_chart("Population by Age Group in " + year, dimensions, source)
    return Response(option)


# ----------------------- Economic Resilience -----------------------

@api_view(["GET"])
def dash3_chart_3(request):
    dataset_code = request.GET.get("dataset_code")
    df = json_to_dataframe(dataset_code)
    return d3_line_chart_economic_resilience(dataset_code, df)


def d3_line_chart_economic_resilience(kpi, df):
        
    if kpi in ["hlth_rs_physreg", "tgs00006"]:
        geo_nuts2 = ["DEA2", "FR10", "PT17", "SK03", "FI1B"]
        df = df[df['geo'].isin(geo_nuts2)]
        geo_name = {
            "DEA2": "Köln",
            "FI1B": "Helsinki-Uusimaa",
            "SK03": "Stredné Slovensko",
            "PT17": "Área M. de Lisboa",
            "FR10": "Ile de France"
        }
        if kpi == "hlth_rs_physreg":
            df = df[(df['values'].notnull()) & (df['unit'] == 'NR')]
            df = df[['values', 'geo', 'time']]
            kpi = "Number of Physicians"
        else:
            df = df[(df['values'].notnull())]
            df = df[['values', 'geo', 'time']]
            kpi = "Regional gross domestic product"

    last_ten_years = sorted(df['time'].unique())[-10:]
    df = df[df['time'].isin(last_ten_years)]

    df['geo'] = df['geo'].replace(geo_name)

    #common_years = df.groupby('geo')['time'].apply(set).reset_index()
    #common_years = set.intersection(*common_years['time'])
    #df = df[df['time'].isin(common_years)]

    df_grouped = df.groupby('geo').agg(list).reset_index()

    result = []
    colors = ['#6272A4', '#8BE9FD', '#FFB86C', '#FF79C6', '#BD93F9']

    for index, row in df_grouped.iterrows():
        data_dict = {
            'name': row['geo'],
            'type': 'line',
            'data': row['values'],
            'itemStyle': {
            'color': colors[index % len(colors)]
            }
        }
        result.append(data_dict)
                            
    geo_list = df['geo'].unique().tolist()    
    year_list = df['time'].unique().tolist()
    
    option = line_chart(kpi, geo_list, year_list, result)
    return Response(option)


# ----------------------- Infrastructure Resilience -----------------------

@api_view(["GET"])
def dash3_chart_4(request):
    dataset_code = "tgs00064"
    df = json_to_dataframe(dataset_code)
    return d3_line_chart_available_hospital_beds(df)

def d3_line_chart_available_hospital_beds(df):
    
    geo_nuts2 = ["DEA2", "FR10", "PT17", "SK03", "FI1B"]
    df = df[df['geo'].isin(geo_nuts2)]
    
    df = df[(df['values'].notnull())]
    df = df[['values', 'geo', 'time']]

    geo_name = {
        "DEA2": "Köln",
        "FI1B": "Helsinki-Uusimaa",
        "SK03": "Stredné Slovensko",
        "PT17": "Área M. de Lisboa",
        "FR10": "Ile de France"
    }    
    df['geo'] = df['geo'].replace(geo_name)

    df_grouped = df.groupby('geo').agg(list).reset_index()

    result = []
    colors = ['#6272A4', '#8BE9FD', '#FFB86C', '#FF79C6', '#BD93F9']

    for index, row in df_grouped.iterrows():
        data_dict = {
            'name': row['geo'],
            'type': 'line',
            'data': row['values'],
            'itemStyle': {
            'color': colors[index % len(colors)]
            }
        }
        result.append(data_dict)
                            
    geo_list = df['geo'].unique().tolist()    
    year_list = df['time'].unique().tolist()
    
    option = line_chart("Available beds in hospitals by NUTS 2 regions", geo_list, year_list, result)
    return Response(option)