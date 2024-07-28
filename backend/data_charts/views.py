from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd


@api_view(["GET"])
def dash1_inclusion_q11(request):
    kpi = request.GET.get("kpi")
    chart_options = d1_line_chart(kpi)
    return Response(chart_options)


def params_to_query_string(params):
    return '&'.join([f'{key}={",".join(value)}' for key, value in params.items()])


def d1_line_chart(kpi):
    
    nat_params = {
    'geo': ['FR', 'FI', 'PT', 'DE', 'SK']
    }
    query_params = params_to_query_string(nat_params)
    api_url = f"http://localhost:8000/charts/dash1_inclusion_q11/?kpi={kpi}&{query_params}"
    df = pd.read_json(api_url)
    
    geo_name = {"DE": "Germany", "FI": "Finland", "SK": "Slovakia", "PT": "Portugal", "FR": "France"}
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
