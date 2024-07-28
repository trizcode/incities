from rest_framework.decorators import api_view
from rest_framework.response import Response
from eurostatapiclient import EurostatAPIClient

@api_view(["GET"])
def fetch_data(request):
    indicators_list = request.GET.getlist("indicators")
    params = request.GET.dict()
    data = get_api_data(indicators_list, params)
    return Response(data)

def get_api_data(indicators_list, params):
    VERSION = '1.0'
    FORMAT = 'json'
    LANGUAGE = 'en'
    
    client = EurostatAPIClient(VERSION, FORMAT, LANGUAGE)
    dataframes = {}
    
    for ind_code in indicators_list:
        dataset = client.get_dataset(ind_code, params=params)
        df = dataset.to_dataframe()
        #df["indicator_label"] = dataset.label
        #df["dataset_code"] = ind_code
        dataframes[ind_code] = df
        print(dataframes)
    
    return dataframes
