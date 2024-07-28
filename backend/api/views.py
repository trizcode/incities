from rest_framework.decorators import api_view
from rest_framework.response import Response
from eurostatapiclient import EurostatAPIClient


@api_view(["GET"])
def fetch_data(request):
    
    dataset_code = request.GET.getlist("dataset_code")
    params = request.GET.dict()
    data = get_api_data(dataset_code, params)
    
    return Response(data)


def get_api_data(dataset_code, params):
    
    VERSION = '1.0'
    FORMAT = 'json'
    LANGUAGE = 'en'
    
    client = EurostatAPIClient(VERSION, FORMAT, LANGUAGE)
    
    try:
        
        dataset = client.get_dataset(dataset_code, params=params)
        df = dataset.to_dataframe()
        #df["indicator_label"] = dataset.label
        #df["dataset_code"] = ind_code
        return df
    
    except Exception as e:
        
        print(f"Error fetching data: {e}")
        return None
