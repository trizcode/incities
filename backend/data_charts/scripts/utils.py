from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.views import get_api_data
import pandas as pd
import json


def json_to_dataframe(dataset_code, geo):
    
    api_data = get_api_data(dataset_code)
    json_data = json.loads(api_data)
    df = pd.DataFrame(json_data)
    if geo == "nat":
        geo = 'geo'
        geo_list = ["DE", "FI", "SK", "PT", "FR"]
        geo_name = {
            "DE": "Germany",
            "FI": "Finland",
            "SK": "Slovakia",
            "PT": "Portugal",
            "FR": "France"
        }
    if geo == "nuts2":
        geo = 'geo'
        geo_list = ["DEA2", "FI1B", "SK03", "PT17", "FR10"]
        geo_name = {
            "DEA2": "Köln",
            "FI1B": "Helsinki-Uusimaa",
            "SK03": "Stredné Slovensko",
            "PT17": "Área M. de Lisboa",
            "FR10": "Ile de France"
        }
    if geo == "nuts2_1":
        geo = 'geo'
        geo_list = ["DEA23", "FR101", "PT170", "SK031", "FI1B1"]
    if geo == "nuts3":
        geo = 'cities'
        geo_list = ["DE004C", "FI001C", "SK006C", "PT001C", "FR001C"]
    
    df = df[df[geo].isin(geo_list)]
    df[geo] = df[geo].replace(geo_name)
    return df


@api_view(["GET"])
def get_available_years(request):
    dataset_code = request.GET.get("dataset_code")
    df = json_to_dataframe(dataset_code)
    
    df = df[(df['values'].notnull())]
    df['time'] = df['time'].astype(int)
    available_years = sorted(df['time'].unique(), reverse=True)
    
    return Response(available_years)