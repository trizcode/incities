from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import *
from .charts import *


# ----------------------- Air Quality -----------------------

@api_view(["GET"])
def dash2_q11(request):
    
    dataset_code = request.GET.get("dataset_code")
    df = json_to_dataframe(dataset_code, 'nat')
    return d2_line_chart_air_quality(df, dataset_code)


def d2_line_chart_air_quality(df, kpi):
    
    if kpi in ["cei_gsr011", "sdg_12_30"]:
        df = df[["values", "geo", "time"]]
        df = df[(df["time"] >= 2010)]
        if kpi == "cei_gsr011":
            kpi = "Greenhouse gases emissions from production activities"
        else:
            kpi = "Average CO2 emissions per km from new passenger cars"
            
    geo_name = {
        "DE": "Germany",
        "FI": "Finland",
        "SK": "Slovakia",
        "PT": "Portugal",
        "FR": "France"
    }
    df['geo'] = df['geo'].replace(geo_name)
            
    df["values"] = df["values"].round(2)
    
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
            'itemStyle': {
            'color': colors[index % len(colors)]
        }
        }
        result.append(data_dict) 
               
    geo_list = df['geo'].unique().tolist()    
    year_list = df['time'].unique().tolist()
    
    option = line_chart(kpi, "", geo_list, year_list, result)
    return Response(option)


@api_view(["GET"])
def dash2_q12(request):
    dataset_code = request.GET.get("dataset_code")
    if dataset_code in ["cei_gsr011", "sdg_12_30"]:
        df = json_to_dataframe(dataset_code, 'nat')
    return d2_bar_chart_air_quality(df, dataset_code)


def d2_bar_chart_air_quality(df, kpi):

    if kpi in ["cei_gsr011", "sdg_12_30"]:
        
        df = df[(df['time'] == 2022)]
        df = df[["values", "geo"]]
        
        if kpi == "cei_gsr011":
            kpi = "Greenhouse gases emissions from production activities"
        else:
            kpi = "Average CO2 emissions per km from new passenger cars"
    
    geo_name = {
        "DE": "Germany",
        "FI": "Finland",
        "SK": "Slovakia",
        "PT": "Portugal",
        "FR": "France"
    }
    df['geo'] = df['geo'].replace(geo_name)
    
    df["values"] = df["values"].round(2)
    df = df.sort_values(by='values')

    geo_list = df['geo'].unique().tolist()
    values_list = df['values'].tolist()
    
    option = basic_bar_chart(kpi, "Year: 2022", geo_list, values_list)
    return Response(option)


# ----------------------- Energy -----------------------

@api_view(["GET"])
def dash2_q22(request):
    dataset_code = "sdg_07_40"
    df = json_to_dataframe(dataset_code, 'nat')
    nrg_bal = request.GET.get("nrg_bal")
    return d2_line_chart_energy(df, nrg_bal)


def d2_line_chart_energy(df, kpi):
    
    df = df[(df['nrg_bal'] == f'{kpi}')]
    df = df[["values", "geo", "time"]]
    
    geo_name = {
        "DE": "Germany",
        "FI": "Finland",
        "SK": "Slovakia",
        "PT": "Portugal",
        "FR": "France"
    }
    df['geo'] = df['geo'].replace(geo_name)
    
    geo_list = df['geo'].unique().tolist()
    year_list = df['time'].unique().tolist()
    
    result = []
    colors = ['#282A36', '#6272A4', '#FF79C6', '#50FA7B', '#BD93F9']
    
    for index, (name, group) in enumerate(df.groupby('geo')):
        data_dict = {
            'name': name,
            'type': 'line',
            'data': group['values'].tolist(),
            'itemStyle': {
            'color': colors[index % len(colors)]
        }
        }
        result.append(data_dict)
        
    if kpi == 'REN':
        kpi = 'Renewable energy sources'
    elif kpi == 'REN_TRA':
        kpi = 'Renewable energy sources in transport'
    elif kpi == 'REN_ELC':
        kpi = 'Renewable energy sources in electricity'
    else:
        kpi = 'Renewable energy sources in heating and cooling'
        
    option = line_chart("Share of renewable energy in gross final energy consumption", kpi, geo_list, year_list, result)
    return Response(option)


@api_view(["GET"])
def dash2_bar_chart_energy_ranking(request):
    dataset_code = "sdg_07_40"
    df = json_to_dataframe(dataset_code, 'nat')
    kpi = request.GET.get("nrg_bal")

    df = df[(df['nrg_bal'] == kpi) & (df['time'] == 2022)]
    df = df[["values", "geo"]]
    
    geo_name = {
        "DE": "Germany",
        "FI": "Finland",
        "SK": "Slovakia",
        "PT": "Portugal",
        "FR": "France"
    }
    df['geo'] = df['geo'].replace(geo_name)

    df = df.sort_values(by='values')

    geo_list = df['geo'].unique().tolist()
    values_list = df['values'].tolist()
    
    if kpi == 'REN':
        kpi = 'Renewable energy sources'
    elif kpi == 'REN_TRA':
        kpi = 'Renewable energy sources in transport'
    elif kpi == 'REN_ELC':
        kpi = 'Renewable energy sources in electricity'
    else:
        kpi = 'Renewable energy sources in heating and cooling'
    
    option = basic_bar_chart(kpi, "Year: 2022", geo_list, values_list, color="#50FA7B")
    return Response(option)


@api_view(["GET"])
def d2_donut_chart_energy(request):

    df = json_to_dataframe("sdg_07_40", 'nat')
    geo = request.GET.get("geo")
    
    df = df[(df['nrg_bal'] != 'REN') & (df['geo'] == geo) & (df['time'] == 2022)]
    df = df[["values", 'nrg_bal', "geo"]]

    nrg_bal_name = {
            "REN_TRA": "Transport",
            "REN_ELC": "Electricity",
            "REN_HEAT_CL": "Heating and cooling"
        }
    df['nrg_bal'] = df['nrg_bal'].replace(nrg_bal_name)
    
    if geo == "DE":
        geo = "Germany"
    elif geo == "FI":
        geo = "Finland"
    elif geo == "FR":
        geo = "France"
    elif geo == "PT":
        geo = "Portugal"
    else:
        geo = "Slovakia"
    
    df = df.groupby('nrg_bal')['values'].sum().reset_index()
    total = df['values'].sum()
    df['normalized_values'] = df['values'] / total * 100
    df['normalized_values'] = df['normalized_values'].round(2)
    
    colors = ['#50FA7B', '#44475A', '#FF79C6']

    result = [
        {'value': row['normalized_values'], 'name': row['nrg_bal']}
        for _, row in df.iterrows()
    ]
    
    option = donut_chart("Renewable energy by Sector in " + geo, 'Year: 2022', result, colors)
    return Response(option)


# ----------------------- Biodiversity -----------------------

@api_view(["GET"])
def d2_bar_chart_TPA_prot_area(request):
    dataset_code = "env_bio4"
    df = json_to_dataframe(dataset_code, 'nat')
    
    df = df[(df['areaprot'] == 'TPA') & (df['unit'] == 'KM2') & (df["time"] == 2021)]
    df = df[["values", 'geo']]
    
    geo_name = {
            "DE": "Germany",
            "FI": "Finland",
            "FR": "France",
            "PT": "Portugal",
            "SK": "Slovakia"
    }  
    df['geo'] = df['geo'].replace(geo_name)
    
    df = df.sort_values(by='values')
    
    geo_list = df['geo'].unique().tolist()   
    values_list = df['values'].unique().tolist()
        
    option = basic_bar_chart("Terrestrial protected area (Km)", "Year: 2021", geo_list, values_list)
    return Response(option)


@api_view(["GET"])
def d2_bar_chart_MPA_prot_area(request):
    dataset_code = "env_bio4"
    df = json_to_dataframe(dataset_code, 'nat')
    
    df = df[(df['areaprot'] == 'MPA') & (df['unit'] == 'KM2') & (df["time"] == 2021)]
    df = df[["values", 'geo']]
    
    geo_name = {
            "DE": "Germany",
            "FI": "Finland",
            "FR": "France",
            "PT": "Portugal",
            "SK": "Slovakia"
    }  
    df['geo'] = df['geo'].replace(geo_name)
    
    df = df.sort_values(by='values')
    
    geo_list = df['geo'].unique().tolist()   
    values_list = df['values'].unique().tolist()
        
    option = basic_bar_chart("Marine protected area (Km)", "Year: 2021", geo_list, values_list, color='#FF79C6')
    return Response(option)


@api_view(["GET"])
def dash2_q41(request):
    dataset_code = "env_bio4"
    df = json_to_dataframe(dataset_code, 'nat')
    
    df = df[(df['unit'] == 'KM2') & (df['time'] == 2021)]
    df = df[["values", 'geo', 'areaprot', "time"]]
    
    df["values"] = df["values"].astype('int')
    
    geo_name = {
            "DE": "Germany",
            "FI": "Finland",
            "SK": "Slovakia",
            "PT": "Portugal",
            "FR": "France"
        }
    df['geo'] = df['geo'].replace(geo_name)
    
    new_row = pd.DataFrame({'values': [0], 'geo': ['Slovakia'], 'areaprot': ['MPA'], 'time': [2021]})
    df = pd.concat([df, new_row]).reset_index(drop=True)
    
    df['areaprot'] = df['areaprot'].replace({'TPA': 'Terrestrial area (Km)', 'MPA': 'Marine area (Km)'})
    
    dimensions = ['geo'] + ['Terrestrial area (Km)'] + ['Marine area (Km)']
    pivot_df = df.pivot(index='geo', columns='areaprot', values='values').reset_index()
    source = pivot_df.to_dict(orient='records')
    
    option = bar_chart("Protected Areas", "Year: 2021", dimensions, source)
    return Response(option)


@api_view(["GET"])
def d2_donut_chart_prot_area(request):
    
    dataset_code = "env_bio4"
    df = json_to_dataframe(dataset_code, 'nat')
    geo = request.GET.get("geo")
    
    df = df[(df['unit'] == 'PC') & (df['time'] == 2021) & (df['geo'] == geo) ]
    df = df[["values", 'areaprot']]

    areaprot_name = {
            "TPA": "Terrestrial",
            "MPA": "Marine"
        }
    df['areaprot'] = df['areaprot'].replace(areaprot_name)
    
    if geo == "DE":
        geo = "Germany"
    elif geo == "FI":
        geo = "Finland"
    elif geo == "FR":
        geo = "France"
    elif geo == "PT":
        geo = "Portugal"
    else:
        geo = "Slovakia"
    
    df = df.groupby('areaprot')['values'].sum().reset_index()
    total = df['values'].sum()
    df['normalized_values'] = df['values'] / total * 100
    df['normalized_values'] = df['normalized_values'].round(2)
    
    colors = ['#FF79C6', '#BD93F9']

    result = [
        {'value': row['normalized_values'], 'name': row['areaprot']}
        for _, row in df.iterrows()
    ]
    
    option = donut_chart("Protected Area (%) in " + geo, 'Year: 2021', result, colors)
    return Response(option)


# ----------------------- Waste Management -----------------------

@api_view(["GET"])
def dash2_line_chart_wst_oper(request):
    dataset_code = "env_wastrt"
    df = json_to_dataframe(dataset_code, 'nat')
    geo = request.GET.get("geo")
    
    df = df[(df['waste'] == 'TOTAL')
            & (df['hazard'] == 'HAZ_NHAZ')
            & (df['unit'] == 'T')
            & (df['wst_oper'].isin(["DSP_L", "DSP_I", "RCV_E", "RCV_R_B"]))
            & (df['geo'] == geo)]
    df = df[["values", 'wst_oper', "time"]]

    wst_oper_name = {
        "DSP_L": "Landfill",
        "DSP_I": "Incineration",
        "RCV_E": "Energy recovery",
        "RCV_R_B": "Recycling"
    }
    df['wst_oper'] = df['wst_oper'].replace(wst_oper_name)
    
    wst_oper_list = df['wst_oper'].unique().tolist()   
    year_list = df['time'].unique().tolist()
    
    result = []
    colors = ['#282A36', '#6272A4', '#FF79C6', '#50FA7B', '#6272A4']
    
    for index, (name, group) in enumerate(df.groupby('wst_oper')):
        data_dict = {
            'name': name,
            'type': 'line',
            'data': group['values'].tolist(),
            'itemStyle': {
            'color': colors[index % len(colors)]
        }
        }
        result.append(data_dict)
    
    if geo == "DE":
        geo = "Germany"
    elif geo == "FI":
        geo = "Finland"
    elif geo == "FR":
        geo = "France"
    elif geo == "PT":
        geo = "Portugal"
    else:
        geo = "Slovakia"
        
    option = line_chart("Disposal and Recovery operations in " + geo, "", wst_oper_list, year_list, result)
    return Response(option)


@api_view(["GET"])
def dash2_bar_chart_wst_ranking(request):
    dataset_code = "env_wastrt"
    df = json_to_dataframe(dataset_code, 'nat')

    df = df[(df['wst_oper'] == 'TRT') 
            & (df['time'] == 2020) 
            & (df['waste'] == 'TOTAL')
            & (df['hazard'] == 'HAZ_NHAZ')
            & (df['unit'] == 'T')]
    df = df[["values", "geo"]]
    
    geo_name = {
        "DE": "Germany",
        "FI": "Finland",
        "SK": "Slovakia",
        "PT": "Portugal",
        "FR": "France"
    }
    df['geo'] = df['geo'].replace(geo_name)

    df = df.sort_values(by='values')

    geo_list = df['geo'].unique().tolist()
    values_list = df['values'].tolist()

    option = basic_bar_chart("Total Waste", "Year: 2020", geo_list, values_list)
    return Response(option)


@api_view(["GET"])
def dash2_q51(request):
    dataset_code = "env_wastrt"
    df = json_to_dataframe(dataset_code, 'nat')
    geo = request.GET.get("geo")
    return d2_bar_chart_waste_management(df, geo)


def d2_bar_chart_waste_management(df, geo):
    
    df = df[(df['waste'] == 'TOTAL') 
            & (df['hazard'] == 'HAZ_NHAZ') 
            & (df['unit'] == 'T') 
            & (df['wst_oper'].isin(["DSP_L", "DSP_I", "RCV_E", "RCV_R_B"]))
            & (df['geo'] == geo)
            & (df['time'] == 2020)
            ]
    df = df[["wst_oper", 'values']]
    
    wst_oper_name = {
            "DSP_L": "Landfill",
            "DSP_I": "Incineration",
            "RCV_E": "Energy recovery",
            "RCV_R_B": "Recycling"
        }
    df['wst_oper'] = df['wst_oper'].replace(wst_oper_name)
    
    df["values"] = df["values"].astype('int')
    
    wst_oper_list = df["wst_oper"].unique().tolist()
    data = df["values"].unique().tolist()
    
    if geo == "DE":
        geo = "Germany"
    elif geo == "FI":
        geo = "Finland"
    elif geo == "FR":
        geo = "France"
    elif geo == "PT":
        geo = "Portugal"
    else:
        geo = "Slovakia"
        
    option = horizontal_bar_chart("Treatment of waste by waste management operations in " + geo, "Year: 2020", wst_oper_list, data)
    return Response(option)


@api_view(["GET"])
def dash2_q52(request):
    dataset_code = "env_wastrt"
    df = json_to_dataframe(dataset_code, 'nat')
    geo = request.GET.get("geo")
    return d2_pie_chart_waste_dim(df, geo)


def d2_pie_chart_waste_dim(df, geo):
    
    df = df[(df['waste'] == 'TOTAL')
            & (df['hazard'] == 'HAZ_NHAZ')
            & (df['unit'] == 'T')
            & (df['wst_oper'] != 'TRT')
            & (df['geo'] == geo)
            & (df['time'] == 2020)
            ]
    df = df[["wst_oper", 'values']]
    
    df["values"] = df["values"].astype('int')
    
    wst_oper_domain = {
            "DSP_L_OTH": "Disposal",
            "DSP_L": "Disposal",
            "DSP_I": "Disposal",
            "DSP_OTH": "Disposal",
            "RCV_E": "Recovery",
            "RCV_R_B": "Recovery",
            "RCV_R": "Recovery",
            "RCV_B": "Recovery"
        }
    df['wst_oper'] = df['wst_oper'].replace(wst_oper_domain)

    sum_disposal = df[df['wst_oper'] == 'Disposal']['values'].sum()
    sum_recovery = df[df['wst_oper'] == 'Recovery']['values'].sum()
    df_sum = pd.DataFrame({
        'wst_oper': ['Disposal', 'Recovery'],
        'values': [sum_disposal, sum_recovery]
    })
    
    columns = df_sum[['wst_oper', 'values']]
    data = [{"value": row['values'], "name": row['wst_oper']} for _, row in columns.iterrows()]

    if geo == "DE":
        geo = "Germany"
    elif geo == "FI":
        geo = "Finland"
    elif geo == "FR":
        geo = "France"
    elif geo == "PT":
        geo = "Portugal"
    else:
        geo = "Slovakia"
        
    colors = ['#282A36', '#FFB86C']
    
    option = donut_chart('Treatment of waste operation domain in ' + geo, "Year: 2020", data, colors)
    return Response(option)


# ----------------------- Employment -----------------------

@api_view(["GET"])
def dash2_q61(request):
    dataset_code = "tgs00007"
    df = json_to_dataframe(dataset_code, 'nuts2')
    return d2_line_chart_employment_rate(df)


def d2_line_chart_employment_rate(df):
    
    df = df[(df['sex'] == 'T')]
    df = df[['values', 'geo', 'time']]
    
    geo_name = {
        "DEA2": "Köln",
        "FI1B": "Helsinki-U.",
        "SK03": "S. Slovensko",
        "PT17": "A. M. Lisboa",
        "FR10": "Ile de France"
    }
    df['geo'] = df['geo'].replace(geo_name)
    
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
            'itemStyle': {
            'color': colors[index % len(colors)]
        }
        }
        result.append(data_dict)
                
    geo_list = df['geo'].unique().tolist()    
    year_list = df['time'].unique().tolist()
    
    option = line_chart("Employment rate of population in productive age", "", geo_list, year_list, result)
    return Response(option)


@api_view(["GET"])
def dash2_bar_chart_employment_ranking(request):
    dataset_code = "tgs00007"
    df = json_to_dataframe(dataset_code, 'nuts2')
        
    df = df[(df['time'] == 2023)]
    df = df[["values", "geo"]]
    
    geo_name = {
        "DEA2": "Köln",
        "FI1B": "Helsinki-U.",
        "SK03": "S. Slovensko",
        "PT17": "A. M. Lisboa",
        "FR10": "Ile de France"
    }
    df['geo'] = df['geo'].replace(geo_name)
    
    df["values"] = df["values"].round(2)
    df = df.sort_values(by='values')

    geo_list = df['geo'].unique().tolist()
    values_list = df['values'].tolist()
    
    option = basic_bar_chart("Employment rate by NUTS 2 regions", "Year: 2023", geo_list, values_list)
    return Response(option)


@api_view(["GET"])
def dash2_donut_chart_employment_by_sex(request):
    
    dataset_code = "tgs00007"
    df = json_to_dataframe(dataset_code, 'nuts2')
    geo = request.GET.get("geo")
    
    df = df[(df['sex'] != 'T') & (df['time'] == 2023) & (df['geo'] == geo)]
    df = df[['values', 'sex', "geo"]]

    df['sex'] = df['sex'].replace({'M': 'Male', 'F': 'Female'})
    
    if geo == "DEA2":
        geo = "Köln"
    elif geo == "FI1B":
        geo = "Helsinki-U."
    elif geo == "FR10":
        geo = "Ile de France"
    elif geo == "PT17":
        geo = "A. M. Lisboa"
    else:
        geo = "S. Slovensko"
    
    df = df.groupby('sex')['values'].sum().reset_index()
    total = df['values'].sum()
    df['normalized_values'] = df['values'] / total * 100
    df['normalized_values'] = df['normalized_values'].round(2)
    
    colors = ['#FF79C6', '#BD93F9']

    result = [
        {'value': row['normalized_values'], 'name': row['sex']}
        for _, row in df.iterrows()
    ]
    
    option = donut_chart("Employment rate by sex in " + geo, "Year: 2023", result, colors)
    return Response(option)