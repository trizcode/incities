from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.views import get_api_data
import pandas as pd
import json

@api_view(["GET"])
def dash1_inclusion_q11(request):
    dataset_code = request.GET.get("dataset_code")
    api_data = get_api_data(dataset_code)
    json_data = json.loads(api_data)
    df = pd.DataFrame(json_data)
    return Response(d1_line_chart(dataset_code, df))

def d1_line_chart(kpi, df):
    
    if kpi in ["tessi190", "tepsr_sp200", "tepsr_lm410"]:
        geo_nat = ["DE", "FI", "SK", "PT", "FR"]
        df = df[df['geo'].isin(geo_nat)]
        geo_name = {
            "DE": "Germany", 
            "FI": "Finland", 
            "SK": "Slovakia", 
            "PT": "Portugal", 
            "FR": "France"
        }
        if kpi == "tessi190":
            df = df[["values", "geo", "time"]]
            df = df[(df['values'].notnull())]
            kpi = "Gini coefficient of equivalized disposable income (%) "
        elif kpi == "tepsr_sp200":
            df = df[(df['values'].notnull()) & (df['lev_limit'] == 'SEV') & (df['sex'] == 'T')]
            df = df[["values", "geo", "time"]]
            kpi = "Disability employment gap by severe limitation"
        else:
            df = df[(df['values'].notnull()) & (df['sex'] == 'T')]
            df = df[["values", "geo", "time"]]
            kpi = "People at risk of poverty or social exclusion"
    else:
        geo_nuts2 = ["DEA2", "FI1B", "SK03", "PT17", "FR10"]
        df = df[df['geo'].isin(geo_nuts2)]
        geo_name = {
            "DEA2": "Köln",
            "FI1B": "Helsinki-Uusimaa",
            "SK03": "Stredné Slovensko",
            "PT17": "Área Metropolitana de Lisboa",
            "FR10": "Ile de France"
        }
        df = df[["values", "geo", "time"]]
        df = df[(df['values'].notnull())]
        kpi = "Gender employment gap by NUTS 2 regions"

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
        
    option = {
        "title": {"text": kpi},
        "tooltip": {"trigger": 'axis'},
        "legend": {"data": geo_list, 'bottom': '1%'},
        "grid": {'top': '10%', 'right': '1%', 'bottom': '8%', 'left': '1%', 'containLabel': 'true'},
        "xAxis": {"type": 'category', "data": year_list},
        "yAxis": {"type": 'value'},
        "series": result
    }

    return option


@api_view(["GET"])
def dash1_inclusion_q12(request):
    dataset_code = request.GET.get("dataset_code")
    api_data = get_api_data(dataset_code)
    json_data = json.loads(api_data)
    df = pd.DataFrame(json_data)
    return Response(d1_heatmap(dataset_code, df))

def d1_heatmap(kpi, df):
    
    if kpi in ["tessi190", "tepsr_sp200", "tepsr_lm410"]:
        geo_nat = ["DE", "FI", "SK", "PT", "FR"]
        df = df[df['geo'].isin(geo_nat)]
        geo_name = {
            "DE": "Germany",
            "FI": "Finland",
            "SK": "Slovakia",
            "PT": "Portugal",
            "FR": "France"
        }
        if kpi == "tessi190":
                df = df[["values", "geo", "time"]]
                df = df[(df['values'].notnull())]
                kpi = "Gini coefficient of equivalized disposable income (%) "
        elif kpi == "tepsr_sp200":
                df = df[(df['values'].notnull()) & (df['lev_limit'] == 'SEV') & (df['sex'] == 'T')]
                df = df[["values", "geo", "time"]]
                kpi = "Disability employment gap by severe limitation"
        else:
                df = df[(df['values'].notnull()) & (df['sex'] == 'T')]
                df = df[["values", "geo", "time"]]
                kpi = "People at risk of poverty or social exclusion"
    else:
        geo_nuts2 = ["DEA2", "FI1B", "SK03", "PT17", "FR10"]
        df = df[df['geo'].isin(geo_nuts2)]
        geo_name = {
            "DEA2": "Köln",
            "FI1B": "Helsinki-Uusimaa",
            "SK03": "Stredné Slovensko",
            "PT17": "Área M. de Lisboa",
            "FR10": "Ile de France"
        }
        df = df[["values", "geo", "time"]]
        df = df[(df['values'].notnull())]
        kpi = "Gender employment gap by NUTS 2 regions"
        
    df['geo'] = df['geo'].replace(geo_name)

    year_list = df['time'].unique().tolist()
    geo_list = df['geo'].unique().tolist()
        
    data = [[row['time'], row['geo'], row['values']] for index, row in df.iterrows()]

    min_value = df['values'].min()
    max_value = df['values'].max()

    option = {
    'title': {'text': kpi},
    "tooltip": {
        "position": 'top'
    },
    "grid": {
        "height": '65%',
        "top": '12%',
        'left': '11%',
        'right': '2%'
    },
    "xAxis": {
        "type": 'category',
        "data": year_list,
        "splitArea": {
        "show": "true"
        }
    },
    "yAxis": {
        "type": 'category',
        "data": geo_list,
        "splitArea": {
        "show": "true"
        }
    },
    "visualMap": {
        "min": min_value,
        "max": max_value,
        "calculable": "true",
        "orient": 'horizontal',
        "left": 'center',
        "bottom": '4%'
    },
    "series": [{
        'name': 'Risk',
        'type': 'heatmap',
        'data': data,
    }]
    }

    return option