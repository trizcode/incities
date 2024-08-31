from datetime import datetime
from eurostatapiclient import EurostatAPIClient
import pandas as pd
import requests
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
    
    return Response(get_openweather_api_data())

def get_openweather_api_data():
    
    cities_lat_lon_dict = {
        "Lisboa": ("38.7369","-9.1427"),
        "Helsinki": ("60.192059","24.945831"),
        "Paris": ("48.864716","2.349014"),
        "Zilina": ("49.22315", "18.73941"),
        "Koln": ("50.935173","6.953101")
    }
    
    api_key = "05c1afa5a2f15e69b222f5cc7f1af802"
    data = []
    
    for city, (lat, lon) in cities_lat_lon_dict.items():
        weather_api_url = requests.get(f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}")
        weather_data_json = weather_api_url.json()

        for item in weather_data_json.get('list', []):
            dt = datetime.utcfromtimestamp(item['dt']).strftime('%Y-%m-%d %H:%M:%S')
            main_data = item['main']
            components = item['components']

            data.append({
                "cities": city,
                "date": dt,
                "aqi": main_data.get('aqi'),
                "co": components.get('co'),
                "no": components.get('no'),
                "no2": components.get('no2'),
                "o3": components.get('o3'),
                "so2": components.get('so2'),
                "pm2_5": components.get('pm2_5'),
                "pm10": components.get('pm10'),
                "nh3": components.get('nh3')
            })

    df = pd.DataFrame(data)
    df = df[['cities', 'aqi', 'no2', 'pm10', 'pm2_5', 'date']]
    df = pd.melt(df, id_vars=["cities", "date"], var_name="indicator_name", value_name="values")

    return df