from api.views import *
import pandas as pd
import json


def json_to_dataframe(dataset_code, geo):
    
    api_data = get_eurostat_api_data(dataset_code)
    json_data = json.loads(api_data)
    df = pd.DataFrame(json_data)
        
    if geo == "nat":
        geo = 'geo'
        geo_list = ["DE", "FI", "SK", "PT", "FR"]
    if geo == "nuts2":
        geo = 'geo'
        geo_list = ["DEA2", "FI1B", "SK03", "PT17", "FR10"]
    if geo == "nuts3":
        geo = 'cities'
        geo_list = ["DE004C", "FI001C", "SK006C", "PT001C", "FR001C"]
    if geo == "nuts3_1":
        geo = 'geo'
        geo_list = ["FI1B1", "PT170", "FR101", "DEA23", "SK031"]
    
    df = df[df[geo].isin(geo_list)]
    
    df = df[(df['values'].notnull())]
    df['time'] = df['time'].astype(int)
    
    df = df[df['time'] >= 2014]
    
    return df

