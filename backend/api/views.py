from eurostatapiclient import EurostatAPIClient
from rest_framework.decorators import api_view
from rest_framework.response import Response


# View to get data from Eurostat API
@api_view(["GET"])
def fetch_eurostat_data(request):
    
    dataset_code = request.GET.get("dataset_code")   
    data = get_eurostat_api_data(dataset_code)
    return Response(data)

def get_eurostat_api_data(dataset_code):
    
    VERSION = '1.0'
    FORMAT = 'json'
    LANGUAGE = 'en'
    
    client = EurostatAPIClient(VERSION, FORMAT, LANGUAGE)
    
    dataset = client.get_dataset(dataset_code)
    df = dataset.to_dataframe()
    df["indicator_label"] = dataset.label
    data_json = df.to_json(orient='records')
    
    return data_json


# View to get data from OpenWeather API
@api_view(["GET"])
def fetch_openweather_data(request):
    
    return Response("Hello")

def get_openweather_api_data():
    print("")
