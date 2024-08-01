from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.views import get_api_data
import pandas as pd
import json


def json_to_dataframe(dataset_code):
    api_data = get_api_data(dataset_code)
    json_data = json.loads(api_data)
    df = pd.DataFrame(json_data)
    return df


def kpi_name(kpi):
    
    data_kpis = {
        "Gini coefficient of equivalized disposable income (%)": "tessi190",
        "Disability employment gap by severe limitation": "tepsr_sp200",
        "People at risk of poverty or social exclusion": "tepsr_lm410",
        "Gender employment gap by NUTS 2 regions": "tepsr_lm220"
    }
    kpi_name = {code: name for name, code in data_kpis.items()}
    return kpi_name.get(kpi)


@api_view(["GET"])
def get_available_years(request):
    dataset_code = request.GET.get("dataset_code")
    df = json_to_dataframe(dataset_code)
    available_years = sorted(df['time'].unique())
    return Response(available_years)
