import requests
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
            "PT170": "Área M. de Lisboa",
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

    option = line_chart(kpi, "", geo_list, year_list, result)
    return Response(option)


@api_view(["GET"])
def dash3_chart_2(request):
    year = request.GET.get("year")
    return d3_bar_chart_population_by_age_group(year)


def d3_bar_chart_population_by_age_group(year):
    
    df = json_to_dataframe("demo_r_pjangrp3")
    
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
    
    child = ['Y_LT5', 'Y5-9']
    young = ['Y15-19','Y20-24','Y25-29','Y30-34','Y35-39']
    middle_age = ['Y40-44','Y45-49','Y50-54','Y55-59']
    old = ['Y60-64','Y65-69','Y70-74', 'Y75-79','Y80-84','Y85-89','Y_GE85','Y_GE90']
    age_group = {}
    for age in child:
        age_group[age] = 'Children'
    for age in young:
        age_group[age] = 'Young adults'
    for age in middle_age:
        age_group[age] = 'Middle-aged adults'
    for age in old:
        age_group[age] = 'Old adults'
    df['age'] = df['age'].map(age_group)
    
    df = df.groupby(['geo', 'age'])['values'].sum().reset_index()

    dimensions = ['geo'] + ['Children'] + ['Young adults'] + ['Middle-aged adults'] + ['Old adults']
    pivot_df = df.pivot(index='geo', columns='age', values='values').reset_index()
    source = pivot_df.to_dict(orient='records')
    
    option = {
		"title": {"text": "Population by age group: " + year},
		"legend": {'bottom': '1%'},
		"grid": {'top': '10%', 'right': '1%', 'bottom': '8%', 'left': '1%', 'containLabel': 'true'},
		"tooltip": {},
		"dataset": {
			"dimensions": dimensions,
			"source": source
		},
		"xAxis": { "type": 'category' },
		"yAxis": {},
		'series': [
			{
                'type': 'bar',
                'itemStyle': {
                        'color': '#BD93F9'
                }
			},
			{
                'type': 'bar',
                'itemStyle': {
                        'color': '#50FA7B'
                }
			},
			{
                'type': 'bar',
                'itemStyle': {
                        'color': '#FF79C6'
                }
			},
			{
                'type': 'bar',
                'itemStyle': {
                        'color': '#44475A'
                }
			}
		]
	}
    return Response(option)


# ----------------------- Economic & Infrastructure sResilience -----------------------

@api_view(["GET"])
def dash3_chart_3(request):
    dataset_code = request.GET.get("dataset_code")
    df = json_to_dataframe(dataset_code)
    return d3_line_chart(dataset_code, df)


def d3_line_chart(kpi, df):
        
    if kpi in ["hlth_rs_physreg", "tgs00006", "tgs00064"]:
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
        elif kpi == "tgs00006":
            df = df[(df['values'].notnull())]
            df = df[['values', 'geo', 'time']]
            kpi = "Regional gross domestic product"
        else:
            df = df[(df['values'].notnull())]
            df = df[['values', 'geo', 'time']]
            kpi = "Available beds in hospitals by NUTS 2 regions"

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
    
    option = line_chart(kpi, "", geo_list, year_list, result)
    return Response(option)


@api_view(["GET"])
def dash3_chart_4(request):
    dataset_code_1 = "hlth_rs_physreg" # Physicians number 
    dataset_code_2 = "tgs00064" # Hospital beds number
    year = request.GET.get("year")
    return d3_bar_chart(dataset_code_1, dataset_code_2, year)


def d3_bar_chart(dataset_code_1, dataset_code_2, year):
    
    geo_nuts2 = ["DEA2", "FR10", "PT17", "SK03", "FI1B"]
    
    df_1 = json_to_dataframe(dataset_code_1)
    df_1 = df_1[(df_1['values'].notnull()) & (df_1['time'] == year) & (df_1['unit'] == 'P_HTHAB')]
    df_1 = df_1[['values', 'geo', 'indicator_label']]
    df_1 = df_1[df_1['geo'].isin(geo_nuts2)]
    
    df_2 = json_to_dataframe(dataset_code_2)
    df_2 = df_2[(df_2['values'].notnull()) & (df_2['time'] == year)]
    df_2 = df_2[['values', 'geo', 'indicator_label']]
    df_2 = df_2[df_2['geo'].isin(geo_nuts2)]
    
    df = pd.merge(df_1, df_2, on='geo', suffixes=('_df1', '_df2'))
    df = pd.melt(
        df,
        id_vars=['geo'],
        value_vars=['values_df1', 'values_df2'],
        var_name='indicator_label',
        value_name='values'
    )
    df['ind_label'] = df['indicator_label'].replace({
        'values_df1': 'Number of physicians',
        'values_df2': 'Available beds'
    })
    df = df.drop(columns=['indicator_label'])
    
    geo_name = {
        "DEA2": "Köln",
        "FI1B": "Helsinki-Uusimaa",
        "SK03": "Stredné Slovensko",
        "PT17": "Área M. de Lisboa",
        "FR10": "Ile de France"
    }    
    df['geo'] = df['geo'].replace(geo_name)
    
    dimensions = ['geo'] + ['Number of physicians'] + ['Available beds']
    pivot_df = df.pivot(index='geo', columns='ind_label', values='values').reset_index()
    source = pivot_df.to_dict(orient='records')
    
    option = bar_chart("Number of physicians vs Available hospital beds: " + year, "(per 100 000 inhabitants)", dimensions, source)
    return Response(option)