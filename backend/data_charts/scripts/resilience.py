from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import *
from .charts import *


# ----------------------- Social Resilience -----------------------

@api_view(["GET"])
def line_chart_tertiary_educ_attain(request):
    
    df = json_to_dataframe("tgs00109", "nuts2")
     
    df = df[(df['sex']== 'T')]
    df = df[["values", 'geo', "time"]]
    kpi = "Tertiary educational attainment by Nuts 2 regions"
    subtitle = "Population in age group 24-64 years"

    geo_name = {
            "DEA2": "Köln",
            "FI1B": "Helsinki-U.",
            "SK03": "S. Slovensko",
            "PT17": "A. M. de Lisboa",
            "FR10": "Ile de France"
        }
    df['geo'] = df['geo'].replace(geo_name)

    common_years = df.groupby('geo')['time'].apply(set).reset_index()
    common_years = set.intersection(*common_years['time'])
    df = df[df['time'].isin(common_years)]

    df_grouped = df.groupby('geo').agg(list).reset_index()

    series = []
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
        series.append(data_dict)
                            
    geo_list = df['geo'].unique().tolist()    
    year_list = df['time'].unique().tolist()

    option = line_chart(kpi, subtitle, geo_list, year_list, series)
    return Response(option)


@api_view(["GET"])
def bar_chart_total_pop_ranking(request):
    df = json_to_dataframe("demo_r_pjangrp3", "nuts2")

    df = df[(df['sex']== 'T') & (df['age']== 'TOTAL') & (df['time'] == 2023)]
    df = df[['values', 'geo']]
    kpi = "Total Population by Nuts 2 regions"

    geo_name = {
        "DEA2": "Köln",
        "FI1B": "Helsinki-U.",
        "SK03": "S. Slovensko",
        "PT17": "A. M. de Lisboa",
        "FR10": "Ile de France"
    }
    df['geo'] = df['geo'].replace(geo_name)
    
    df = df.sort_values(by='values')

    geo_list = df['geo'].unique().tolist()
    values_list = df['values'].tolist()
    
    option = basic_bar_chart(kpi, "Year: 2023", geo_list, values_list)
    return Response(option)


@api_view(["GET"])
def bar_chart_pop_aged_ranking(request):
    df = json_to_dataframe("demo_r_pjangrp3", "nuts2")

    df = df[(df['sex'] == 'T') 
        & (df['age'].isin(['Y65-69','Y70-74', 'Y75-79','Y80-84','Y85-89','Y_GE85','Y_GE90']) 
        & (df["time"] == 2023))]
    df = df[["values", 'geo']]
    kpi = "Population aged 65 and over"

    geo_name = {
        "DEA2": "Köln",
        "FI1B": "Helsinki-U.",
        "SK03": "S. Slovensko",
        "PT17": "A. M. de Lisboa",
        "FR10": "Ile de France"
    }
    df['geo'] = df['geo'].replace(geo_name)

    df = df.sort_values(by='values')

    geo_list = df['geo'].unique().tolist()
    values_list = df['values'].tolist()
    
    option = basic_bar_chart(kpi, "Year: 2023", geo_list, values_list)
    return Response(option)


@api_view(["GET"])
def grouped_bar_chart_pop_by_age_group(request):
    
    df = json_to_dataframe("demo_r_pjangrp3", "nuts2")
    
    df = df[(df['time'] == 2023) & (df['age'].isin(['TOTAL', 'UNK']) == False) & (df['sex'] == 'T')]
    df = df[['values', 'geo', 'age']]

    geo_name = {
        "DEA2": "Köln",
        "FI1B": "Helsinki-U.",
        "SK03": "S. Slovensko",
        "PT17": "A. M. de Lisboa",
        "FR10": "Ile de France"
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
		"title": {"text": "Population by age group: 2023"},
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
def line_chart_by_resilience_kpis(request):
    dataset_code = request.GET.get("dataset_code")
    df = json_to_dataframe(dataset_code, "nuts2")
    return d3_line_chart_by_resilience_kpis(df, dataset_code)


def d3_line_chart_by_resilience_kpis(df, kpi):
        
    if kpi in ["hlth_rs_physreg", "tgs00006", "tgs00064"]:
        if kpi == "hlth_rs_physreg":
            df = df[(df['unit'] == 'NR')]
            df = df[['values', 'geo', 'time']]
            kpi = "Number of Physicians"
        elif kpi == "tgs00006":
            df = df[['values', 'geo', 'time']]
            kpi = "Regional gross domestic product"
        else:
            df = df[['values', 'geo', 'time']]
            kpi = "Available beds in hospitals by NUTS 2 regions"

    geo_name = {
        "DEA2": "Köln",
        "FI1B": "Helsinki-U.",
        "SK03": "S. Slovensko",
        "PT17": "A. M. de Lisboa",
        "FR10": "Ile de France"
    }
    df['geo'] = df['geo'].replace(geo_name)

    common_years = df.groupby('geo')['time'].apply(set).reset_index()
    common_years = set.intersection(*common_years['time'])
    df = df[df['time'].isin(common_years)]

    df_grouped = df.groupby('geo').agg(list).reset_index()

    series = []
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
        series.append(data_dict)
                            
    geo_list = df['geo'].unique().tolist()    
    year_list = df['time'].unique().tolist()
    
    option = line_chart(kpi, "", geo_list, year_list, series)
    return Response(option)


@api_view(["GET"])
def grouped_bar_chart_physi_vs_hosp_beds(request):

    df_1 = json_to_dataframe('hlth_rs_physreg', 'nuts2')
    df_1 = df_1[(df_1['time'] == 2022) & (df_1['unit'] == 'P_HTHAB')]
    df_1 = df_1[['values', 'geo', 'indicator_label']]
    
    df_2 = json_to_dataframe('tgs00064', 'nuts2')
    df_2 = df_2[(df_2['time'] == 2022)]
    df_2 = df_2[['values', 'geo', 'indicator_label']]
    
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
        "FI1B": "Helsinki-U.",
        "SK03": "S. Slovensko",
        "PT17": "A. M. de Lisboa",
        "FR10": "Ile de France"
    }    
    df['geo'] = df['geo'].replace(geo_name)
    
    dimensions = ['geo'] + ['Number of physicians'] + ['Available beds']
    pivot_df = df.pivot(index='geo', columns='ind_label', values='values').reset_index()
    source = pivot_df.to_dict(orient='records')
    
    option = bar_chart("Number of physicians vs Available hospital beds: 2022", "(per 100 000 inhabitants)", dimensions, source)
    return Response(option)