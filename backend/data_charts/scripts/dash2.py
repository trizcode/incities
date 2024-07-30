from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import *
from .charts import *


# ----------------------- Air Quality -----------------------

@api_view(["GET"])
def dash2_q11(request):
    dataset_code = request.GET.get("dataset_code")
    df = json_to_dataframe(dataset_code)
    return d2_line_chart_air_quality(dataset_code, df)


def d2_line_chart_air_quality(kpi, df):
    
    if kpi in ["cei_gsr011", "sdg_12_30"]:
        geo_nat = ["DE", "FI", "SK", "PT", "FR"]
        df = df[df['geo'].isin(geo_nat)]
        geo = 'geo'
        df = df[["values", geo, "time"]]
        df = df[(df['values'].notnull())]
        geo_name = {
            "DE": "Germany",
            "FI": "Finland",
            "SK": "Slovakia",
            "PT": "Portugal",
            "FR": "France"
        }
        if kpi == "cei_gsr011":
            kpi = "Greenhouse gases emissions from production activities"
        else:
            kpi = "Average CO2 emissions per km from new passenger cars"
    else:
        geo_nuts3 = ["DE004C", "FI001C", "SK006C", "PT001C", "FR001C"]
        df = df[df['geo'].isin(geo_nuts3)]
        geo = 'cities'
        df = df[["values", geo, "time"]]
        df = df[(df['values'].notnull()) & (df['indic_ur'] == kpi)]
        geo_name = {
            "DE004C": "Köln",
            "FI001C": "Helsinki",
            "SK006C": "Zilina",
            "PT001C": "Lisbon",
            "FR001C": "Paris"
        }
        if kpi == 'EN2026V':
            kpi = 'Annual average concentration of NO2 (µg/m³)'
        elif kpi == 'EN2027V':
            kpi = 'Annual average concentration of PM10 (µg/m³)'
        elif kpi == 'EN2025V':
            kpi = 'Accumulated ozone concentration in excess 70 µg/m³'
        else:
            return None
    
    df["values"] = df["values"].round(2)
    df[geo] = df[geo].replace(geo_name)
    
    common_years = df.groupby(geo)['time'].apply(set).reset_index()
    common_years = set.intersection(*common_years['time'])
    df = df[df['time'].isin(common_years)]
    
    df_grouped = df.groupby(geo).agg(list).reset_index()
    
    result = []
    colors = ['#6272A4', '#8BE9FD', '#FFB86C', '#FF79C6', '#BD93F9']
    
    for index, row in df_grouped.iterrows():
        data_dict = {
            'name': row[geo],
            'type': 'line',
            'data': row['values'],
            'itemStyle': {
            'color': colors[index % len(colors)]
        }
        }
        result.append(data_dict) 
               
    geo_list = df[geo].unique().tolist()    
    year_list = df['time'].unique().tolist()
    
    option = line_chart(kpi, geo_list, year_list, result)
    return Response(option)


@api_view(["GET"])
def dash2_q12(request):
    dataset_code = request.GET.get("dataset_code")
    year1 = request.GET.get("year1")
    year2 = request.GET.get("year2")
    df = json_to_dataframe(dataset_code)
    return d2_bar_chart_air_quality(dataset_code, df, year1, year2)


def d2_bar_chart_air_quality(kpi, df, year1, year2):

    if kpi in ["cei_gsr011", "sdg_12_30"]:
        geo_nat = ["DE", "FI", "SK", "PT", "FR"]
        df = df[df['geo'].isin(geo_nat)]
        geo = 'geo'
        df = df[["values", geo, "time"]]
        df = df[(df['values'].notnull()) & (df['time'].isin([year1, year2]))]
        geo_name = {
            "DE": "Germany",
            "FI": "Finland",
            "SK": "Slovakia",
            "PT": "Portugal",
            "FR": "France"
        }
        if kpi == "cei_gsr011":
            kpi = "Greenhouse gases emissions from production activities"
        else:
            kpi = "Average CO2 emissions per km from new passenger cars"
    else:
        geo_nuts3 = ["DE004C", "FI001C", "SK006C", "PT001C", "FR001C"]
        df = df[df['geo'].isin(geo_nuts3)]
        geo = 'cities'
        df = df[["values", geo, "time"]]
        df = df[(df['values'].notnull()) & (df['indic_ur'] == kpi)]
        geo_name = {
            "DE004C": "Köln",
            "FI001C": "Helsinki",
            "SK006C": "Zilina",
            "PT001C": "Lisbon",
            "FR001C": "Paris"
        }
        if kpi == 'EN2026V':
            kpi = 'Annual average concentration of NO2 (µg/m³)'
        elif kpi == 'EN2027V':
            kpi = 'Annual average concentration of PM10 (µg/m³)'
        elif kpi == 'EN2025V':
            kpi = 'Accumulated ozone concentration in excess 70 µg/m³'
        else:
            return None
    
    df["values"] = df["values"].round(2)
    
    df[geo] = df[geo].replace(geo_name)
    
    common_years = df.groupby(geo)['time'].apply(set).reset_index()
    common_years = set.intersection(*common_years['time'])
    df = df[df['time'].isin(common_years)]

    df_pivot = df.pivot(index=geo, columns='time', values='values').reset_index()
    df_pivot.columns.name = None
    
    dimensions = ['city'] + [str(year) for year in df_pivot.columns[1:]]
    source = df_pivot.rename(columns={geo: 'city'}).to_dict(orient='records')
    
    option = bar_chart(kpi, dimensions, source)   
    return Response(option)


# ----------------------- Clean City -----------------------

@api_view(["GET"])
def dash2_q21(request):
    dataset_code = "urb_percep"
    city = request.GET.get("city")
    df = json_to_dataframe(dataset_code)
    return d2_pie_chart_clean_city(df, city)


def d2_pie_chart_clean_city(df, city):
    
    geo_nuts3 = ["DE004C", "FI001C", "SK006C", "PT001C", "FR001C"]
    df = df[df['geo'].isin(geo_nuts3)]
    
    df = df[["values", 'indic_ur', 'cities', "time"]]
    df = df[(df['values'].notnull()) 
        & (df['time'].isin(['PS2072V', 'PS2073V', 'PS2074V', 'PS2075V', 'PS2076V'])) 
        & (df['cities'] == city)]
    
    indic_ur_name = {
        "PS2072V": "strongly agree",
        "PS2073V": "somewhat agree",
        "PS2074V": "somewhat disagree",
        "PS2075V": "strongly disagree",
        "PS2076V": "don't know / no answer"
    }
    df['indic_ur'] = df['indic_ur'].replace(indic_ur_name)
    
    if city == "DE004C":
        city = "Köln"
    elif city == "FI001C":
        city = "Helsinki"
    elif city == "SK006C":
        city = "Zilina"
    elif city == "PT001C":
        city = "Lisbon"
    else:
        city = "Paris"
        
    df = df.groupby('indic_ur')['values'].sum().reset_index()
    total = df['values'].sum()
    df['normalized_values'] = df['values'] / total * 100
    df['normalized_values'] = df['normalized_values'].round(2)
    
    colors = ['#6272A4', '#8BE9FD', '#FFB86C', '#FF79C6', '#BD93F9']
    result = [
        {'value': row['normalized_values'], 'name': row['indic_ur']}
        for _, row in df.iterrows()
    ]
    kpi = "This city is a clean city"
    
    option = donut_chart(kpi, city, result, colors)
    return Response(option)