from api.views import get_api_data
import json
import pandas as pd


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