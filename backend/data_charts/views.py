from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd


@api_view(["GET"])
def dash1_inclusion_q11(request):
    kpi = request.GET.get("kpi")
    data = fetch_data_from_api(kpi)
    chart_options = d1_line_chart(data, kpi)
    return Response(chart_options)


def fetch_data_from_api(kpi):
    # Fetch data from API and return a pandas dataframe
    api_url = f"http://127.0.0.1:8000/api/fetch_data?indicators={kpi}"
    df = pd.read_json(api_url)
    return df


def d1_line_chart(df, kpi):
    
    print(df)
    
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
        
    chart_data = {
        "title": {"text": kpi},
        "tooltip": {"trigger": 'axis'},
        "legend": {"data": geo_list, 'bottom': '1%'},
        "grid": {'top': '10%', 'right': '1%', 'bottom': '8%', 'left': '1%', 'containLabel': 'true'},
        "xAxis": {"type": 'category', "data": year_list},
        "yAxis": {"type": 'value'},
        "series": result
    }
  
    return chart_data
