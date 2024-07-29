from rest_framework.decorators import api_view
from rest_framework.response import Response
from eurostatapiclient import EurostatAPIClient

@api_view(["GET"])
def fetch_data(request):
    
    dataset_code = request.GET.get("dataset_code")   
    data = get_api_data(dataset_code)
    return Response(data)

def get_api_data(dataset_code):
    
    VERSION = '1.0'
    FORMAT = 'json'
    LANGUAGE = 'en'
    
    client = EurostatAPIClient(VERSION, FORMAT, LANGUAGE)
    
    try:
        dataset = client.get_dataset(dataset_code)
        df = dataset.to_dataframe()
        df["indicator_label"] = dataset.label
        data_json = df.to_json(orient='records')
        return data_json
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
