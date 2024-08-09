from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import *
from .charts import *


@api_view(["GET"])
def dash1_line_chart(request):
    dataset_code = request.GET.get("dataset_code")
    
    if dataset_code in ["tessi190", "tepsr_sp200", "tespm010"]:
        df = json_to_dataframe(dataset_code, 'nat')
    if dataset_code == "tepsr_lm220":
        df = json_to_dataframe(dataset_code, 'nuts2')

    return d1_line_chart_by_kpi(df, dataset_code)


def d1_line_chart_by_kpi(df, kpi):
    
    if kpi in ["tessi190", "tepsr_sp200", "tespm010"]:
        if kpi == "tessi190":
            df = df[["values", "geo", "time"]]
            df = df[(df['values'].notnull())]
            kpi = "Gini coefficient of equivalized disposable income"
        elif kpi == "tepsr_sp200":
            df = df[(df['values'].notnull()) & (df['lev_limit'] == 'SM_SEV') & (df['sex'] == 'T')]
            df = df[["values", "geo", "time"]]
            kpi = "Disability employment gap"
        else:
            df = df[["values", "geo", "time"]]
            df = df[(df['values'].notnull())]
            kpi = "At risk of poverty rate"
    
    if kpi == "tepsr_lm220":         
        df = df[["values", "geo", "time"]]
        df = df[(df['values'].notnull())]
        kpi = "Gender employment gap by NUTS 2 regions"

    common_years = df.groupby('geo')['time'].apply(set).reset_index()
    common_years = set.intersection(*common_years['time'])
    df = df[df['time'].isin(common_years)]
    
    df_grouped = df.groupby('geo').agg(list).reset_index()
    
    result = []
    colors = ['#6272A4', '#8BE9FD', '#FFB86C', '#FF79C6', '#BD93F9']
    
    for index, row in df_grouped.iterrows():
        data_dict = {
            'name': row['geo'],
            'type': 'line',
            'data': row['values'],
            'itemStyle': {'color': colors[index % len(colors)]}
        }
        result.append(data_dict)
                
    geo_list = df['geo'].unique().tolist()    
    year_list = df['time'].unique().tolist()
    
    option = line_chart(kpi, "", geo_list, year_list, result)
    
    return Response(option)


@api_view(["GET"])
def dash1_bar_chart_ranking(request):
    dataset_code = request.GET.get("dataset_code")
    
    if dataset_code in ["tessi190", "tepsr_sp200", "tespm010"]:
        df = json_to_dataframe(dataset_code, 'nat')
    if dataset_code =="tepsr_lm220":
        df = json_to_dataframe(dataset_code, 'nuts2')
        
    return d1_bar_chart_ranking_cities_by_kpi(df, dataset_code)


def d1_bar_chart_ranking_cities_by_kpi(df, kpi):
    
    if kpi in ["tessi190", "tepsr_sp200", "tespm010"]:
        if kpi == "tessi190":
            df = df[(df['values'].notnull()) & (df['time'] == '2023')]
            df = df[["values", "geo"]]
            kpi = "Gini coefficient of equivalized disposable income"
        elif kpi == "tepsr_sp200":
            df = df[(df['values'].notnull()) & (df['lev_limit'] == 'SM_SEV') & (df['sex'] == 'T') & (df['time'] == '2023')]
            df = df[["values", "geo"]]
            kpi = "Disability employment gap"
        else:
            df = df[(df['values'].notnull()) & (df['time'] == '2023')]
            df = df[["values", "geo"]]
            kpi = "At risk of poverty rate"
    
    if kpi == "tepsr_lm220":
        df = df[(df['values'].notnull()) & (df['time'] == '2023')]
        df = df[["values", "geo"]]
        kpi = "Gender employment gap"
        
    df = df.sort_values(by='values')

    geo_list = df['geo'].unique().tolist()
    values_list = df['values'].tolist()
    
    option = basic_bar_chart(kpi, "Year: 2023", geo_list, values_list)
    
    return Response(option)


@api_view(["GET"])
def dash1_gini_coef_vs_poverty_risk(request):
    
    gini_df = json_to_dataframe('tessi190', 'nat')
    poverty_df = json_to_dataframe('tespm010', 'nat')
    
    gini_df = gini_df[(gini_df['values'].notnull())]
    gini_df = gini_df[["values", "geo", "time"]]
    
    poverty_df = poverty_df[(poverty_df['values'].notnull()) & (poverty_df['time'] >= '2014')]
    poverty_df = poverty_df[["values", "geo", "time"]]
    
    df = pd.merge(gini_df, poverty_df, on=['geo', 'time'], suffixes=('_gini', '_poverty'))
    
    return Response(df)


@api_view(["GET"])
def disability_employment_gap_by_sex(request):
    
    lev_limit = request.GET.get("lev_limit")
    
    df = json_to_dataframe('tepsr_sp200', 'nat')
    
    df = df[(df['values'].notnull()) & (df["sex"] != "T") & (df["lev_limit"] == lev_limit) & (df["time"] == '2023')]
    df = df[["values", "geo", "sex"]]

    df['sex'] = df['sex'].replace({'M': 'Male', 'F': 'Female'})
    
    dimensions = ['geo'] + ['Male'] + ['Female']
    pivot_df = df.pivot(index='geo', columns='sex', values='values').reset_index()
    source = pivot_df.to_dict(orient='records')
    
    option = bar_chart("Disability employment gap by sex", "Year: 2023", dimensions, source)
    return Response(option)
    
    