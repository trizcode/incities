from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import *
from .charts import *


# ----------------------- Air Quality -----------------------

@api_view(["GET"])
def dash2_q11(request):
    dataset_code = request.GET.get("dataset_code")
    df = json_to_dataframe(dataset_code)
    return d2_line_chart_air_quality(dataset_code, df)


def d2_line_chart_air_quality(kpi, df):
    
    if kpi in ["cei_gsr011", "sdg_12_30"]:
        geo_nat = ["DE", "FI", "SK", "PT", "FR"]
        df = df[df['geo'].isin(geo_nat)]
        geo = 'geo'
        df = df[["values", geo, "time"]]
        df = df[(df['values'].notnull())]
        geo_name = {
            "DE": "Germany",
            "FI": "Finland",
            "SK": "Slovakia",
            "PT": "Portugal",
            "FR": "France"
        }
        if kpi == "cei_gsr011":
            kpi = "Greenhouse gases emissions from production activities"
        else:
            kpi = "Average CO2 emissions per km from new passenger cars"
    else:
        geo = 'cities'
        geo_nuts3 = ["DE004C", "FI001C", "SK006C", "PT001C", "FR001C"]
        df = df[df[geo].isin(geo_nuts3)]
        df = df[["values", geo, "time"]]
        df = df[(df['values'].notnull()) & (df['indic_ur'] == kpi)]
        geo_name = {
            "DE004C": "Köln",
            "FI001C": "Helsinki",
            "SK006C": "Zilina",
            "PT001C": "Lisbon",
            "FR001C": "Paris"
        }
        if kpi == 'EN2026V':
            kpi = 'Annual average concentration of NO2 (µg/m³)'
        elif kpi == 'EN2027V':
            kpi = 'Annual average concentration of PM10 (µg/m³)'
        elif kpi == 'EN2025V':
            kpi = 'Accumulated ozone concentration in excess 70 µg/m³'
        else:
            return None
    
    df["values"] = df["values"].round(2)
    df[geo] = df[geo].replace(geo_name)
    
    common_years = df.groupby(geo)['time'].apply(set).reset_index()
    common_years = set.intersection(*common_years['time'])
    df = df[df['time'].isin(common_years)]
    
    df_grouped = df.groupby(geo).agg(list).reset_index()
    
    result = []
    colors = ['#6272A4', '#8BE9FD', '#FFB86C', '#FF79C6', '#BD93F9']
    
    for index, row in df_grouped.iterrows():
        data_dict = {
            'name': row[geo],
            'type': 'line',
            'data': row['values'],
            'itemStyle': {
            'color': colors[index % len(colors)]
        }
        }
        result.append(data_dict) 
               
    geo_list = df[geo].unique().tolist()    
    year_list = df['time'].unique().tolist()
    
    option = line_chart(kpi, geo_list, year_list, result)
    return Response(option)


@api_view(["GET"])
def dash2_q12(request):
    dataset_code = request.GET.get("dataset_code")
    year1 = request.GET.get("year1")
    year2 = request.GET.get("year2")
    df = json_to_dataframe(dataset_code)
    return d2_bar_chart_air_quality(dataset_code, df, year1, year2)


def d2_bar_chart_air_quality(kpi, df, year1, year2):

    if kpi in ["cei_gsr011", "sdg_12_30"]:
        geo_nat = ["DE", "FI", "SK", "PT", "FR"]
        df = df[df['geo'].isin(geo_nat)]
        geo = 'geo'
        df = df[["values", geo, "time"]]
        df = df[(df['values'].notnull()) & (df['time'].isin([year1, year2]))]
        geo_name = {
            "DE": "Germany",
            "FI": "Finland",
            "SK": "Slovakia",
            "PT": "Portugal",
            "FR": "France"
        }
        if kpi == "cei_gsr011":
            kpi = "Greenhouse gases emissions from production activities"
        else:
            kpi = "Average CO2 emissions per km from new passenger cars"
    else:
        geo = 'cities'
        geo_nuts3 = ["DE004C", "FI001C", "SK006C", "PT001C", "FR001C"]
        df = df[df[geo].isin(geo_nuts3)]
        df = df[["values", geo, "time"]]
        df = df[(df['values'].notnull()) & (df['indic_ur'] == kpi)]
        geo_name = {
            "DE004C": "Köln",
            "FI001C": "Helsinki",
            "SK006C": "Zilina",
            "PT001C": "Lisbon",
            "FR001C": "Paris"
        }
        if kpi == 'EN2026V':
            kpi = 'Annual average concentration of NO2 (µg/m³)'
        elif kpi == 'EN2027V':
            kpi = 'Annual average concentration of PM10 (µg/m³)'
        elif kpi == 'EN2025V':
            kpi = 'Accumulated ozone concentration in excess 70 µg/m³'
        else:
            return None
    
    df["values"] = df["values"].round(2)
    
    df[geo] = df[geo].replace(geo_name)
    
    common_years = df.groupby(geo)['time'].apply(set).reset_index()
    common_years = set.intersection(*common_years['time'])
    df = df[df['time'].isin(common_years)]

    df_pivot = df.pivot(index=geo, columns='time', values='values').reset_index()
    df_pivot.columns.name = None
    
    dimensions = ['city'] + [str(year) for year in df_pivot.columns[1:]]
    source = df_pivot.rename(columns={geo: 'city'}).to_dict(orient='records')
    
    option = bar_chart(kpi, dimensions, source)   
    return Response(option)


# ----------------------- Clean City -----------------------

@api_view(["GET"])
def dash2_q21(request):
    dataset_code = "urb_percep"
    city = request.GET.get("city")
    df = json_to_dataframe(dataset_code)
    return d2_donut_chart_clean_city(df, city)


def d2_donut_chart_clean_city(df, city):
    
    geo_nuts3 = ["DE004C", "FI001C", "SK006C", "PT001C", "FR001C"]
    df = df[df['cities'].isin(geo_nuts3)]
    
    df = df[["values", 'indic_ur', 'cities', "time"]]
    df = df[(df['values'].notnull()) 
        & (df['indic_ur'].isin(['PS2072V', 'PS2073V', 'PS2074V', 'PS2075V', 'PS2076V'])) 
        & (df['cities'] == city)]
    
    indic_ur_name = {
        "PS2072V": "strongly agree",
        "PS2073V": "somewhat agree",
        "PS2074V": "somewhat disagree",
        "PS2075V": "strongly disagree",
        "PS2076V": "don't know / no answer"
    }
    df['indic_ur'] = df['indic_ur'].replace(indic_ur_name)
    
    if city == "DE004C":
        city = "Köln"
    elif city == "FI001C":
        city = "Helsinki"
    elif city == "SK006C":
        city = "Zilina"
    elif city == "PT001C":
        city = "Lisbon"
    else:
        city = "Paris"
        
    df = df.groupby('indic_ur')['values'].sum().reset_index()
    total = df['values'].sum()
    df['normalized_values'] = df['values'] / total * 100
    df['normalized_values'] = df['normalized_values'].round(2)
    
    colors = ['#6272A4', '#8BE9FD', '#FFB86C', '#FF79C6', '#BD93F9']
    result = [
        {'value': row['normalized_values'], 'name': row['indic_ur']}
        for _, row in df.iterrows()
    ]
    kpi = "This city is a clean city"
    
    option = donut_chart(kpi, city, result, colors)
    return Response(option)


# ----------------------- Energy -----------------------

@api_view(["GET"])
def dash2_q22(request):
    dataset_code = "sdg_07_40"
    df = json_to_dataframe(dataset_code)
    nrg_bal = request.GET.get("nrg_bal")
    return d2_line_chart_energy(nrg_bal, df)


def d2_line_chart_energy(kpi, df):
    
    geo_nat = ["DE", "FI", "SK", "PT", "FR"]
    df = df[df['geo'].isin(geo_nat)]
    
    df = df[(df['values'].notnull()) & (df['nrg_bal'] == kpi)]
    df = df[["values", "geo", "time"]]

    geo_name = {
            "DE": "Germany",
            "FI": "Finland",
            "FR": "France",
            "PT": "Portugal",
            "SK": "Slovakia"
    }    
    df['geo'] = df['geo'].replace(geo_name)
    
    geo_list = df['geo'].unique().tolist()   
    
    last_10_years = sorted(df['time'].unique())[-10:]
    df_filtered = df[df['time'].isin(last_10_years)]
    year_list = df_filtered['time'].unique().tolist()
    
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
    if kpi == 'REN_TRA':
        kpi = 'Renewable energy sources in transport'
    elif kpi == 'REN_ELC':
        kpi = 'Renewable energy sources in electricity'
    else:
        kpi = 'Renewable energy sources in heating and cooling'
        
    option = line_chart(kpi, geo_list, year_list, result)
    return Response(option)


@api_view(["GET"])
def dash2_q31(request):
    dataset_code = "sdg_07_40"
    df = json_to_dataframe(dataset_code)
    geo = request.GET.get("geo")
    year = request.GET.get("year")
    return d2_donut_chart_energy(geo, year, df)


def d2_donut_chart_energy(geo, year, df):

    geo_nat = ["DE", "FI", "SK", "PT", "FR"]
    df = df[df['geo'].isin(geo_nat)]
    
    df = df[(df['values'].notnull()) &(df['geo'] == geo) & (df['nrg_bal'] != 'REN') & (df['time'] == year)]
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
    
    option = donut_chart("Renewable energy by Sector in " + geo, 'Year: ' + year, result, colors)
    return Response(option)


# ----------------------- Biodiversity -----------------------

@api_view(["GET"])
def dash2_q32(request):
    dataset_code = "env_bio4"
    df = json_to_dataframe(dataset_code)
    areaprot = request.GET.get("areaprot")
    return d2_line_chart_protected_areas(areaprot, df)


def d2_line_chart_protected_areas(kpi, df):

    geo_nat = ["DE", "FI", "SK", "PT", "FR"]
    df = df[df['geo'].isin(geo_nat)]
    
    df = df[(df['values'].notnull()) &(df['areaprot'] == kpi) & (df['unit'] != 'KM2')]
    df = df[["values", 'geo', "time"]]
    
    geo_name = {
            "DE": "Germany",
            "FI": "Finland",
            "FR": "France",
            "PT": "Portugal",
            "SK": "Slovakia"
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
        
    if kpi == 'TPA':
        kpi = 'Terrestrial protected area'
    if kpi == 'MPA':
        kpi = 'Marine protected area'
        
    option = line_chart(kpi, geo_list, year_list, result)  
    return Response(option)


@api_view(["GET"])
def dash2_q41(request):
    dataset_code = "env_bio4"
    df = json_to_dataframe(dataset_code)
    year = request.GET.get("year")
    return d2_bar_chart_protected_areas(year, df)


def d2_bar_chart_protected_areas(year, df):
    
    geo_nat = ["DE", "FI", "SK", "PT", "FR"]
    df = df[df['geo'].isin(geo_nat)]
    
    df = df[(df['values'].notnull()) &(df['unit'] == 'KM2') & (df['time'] == year)]
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
    
    df['areaprot'] = df['areaprot'].replace({'TPA': 'Terrestrial area', 'MPA': 'Maritime area'})
    
    dimensions = ['geo'] + ['Maritime area'] + ['Terrestrial area']
    pivot_df = df.pivot(index='geo', columns='areaprot', values='values').reset_index()
    source = pivot_df.to_dict(orient='records')
    
    option = bar_chart("Protected Areas in " + year, dimensions, source)
    return Response(option)


# ----------------------- Waste Management -----------------------

@api_view(["GET"])
def dash2_q42(request):
    dataset_code = "env_wastrt"
    df = json_to_dataframe(dataset_code)
    wst_oper = request.GET.get("wst_oper")
    return d2_line_chart_waste_management(wst_oper, df)


def d2_line_chart_waste_management(kpi, df):

    geo_nat = ["DE", "FI", "SK", "PT", "FR"]
    df = df[df['geo'].isin(geo_nat)]
    
    df = df[(df['values'].notnull()) 
            &(df['waste'] == 'TOTAL') 
            & (df['hazard'] == 'HAZ_NHAZ') 
            & (df['unit'] == 'T') 
            & (df['wst_oper'] == kpi)]
    df = df[["values", 'geo', "time"]]

    geo_name = {
            "DE": "Germany",
            "FI": "Finland",
            "FR": "France",
            "PT": "Portugal",
            "SK": "Slovakia"
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
        
    if kpi == "TRT":
        kpi = "Total"
    elif kpi == "DSP_L_OTH": 
        kpi = "Disposal - landfill and others"
    elif kpi == "DSP_L": 
        kpi = "Disposal - landfill"
    elif kpi == "DSP_I": 
        kpi = "Disposal - incineration"
    elif kpi == "DSP_OTH": 
        kpi = "Disposal - other"
    elif kpi == "RCV_E": 
        kpi = "Recovery - energy recovery"
    elif "RCV_R_B":
        kpi = "Recovery - recycling and backfilling"
    elif kpi == "RCV_R": 
        kpi = "Recovery - recycling"
    else:
        kpi = "Recovery - backfilling"
        
    option = line_chart("Waste treatment: " + kpi, geo_list, year_list, result)
    return Response(option)


@api_view(["GET"])
def dash2_q51(request):
    dataset_code = "env_wastrt"
    df = json_to_dataframe(dataset_code)
    geo = request.GET.get("geo")
    year = request.GET.get("year")
    return d2_bar_chart_waste_management(geo, year, df)


def d2_bar_chart_waste_management(geo, year, df):

    geo_nat = ["DE", "FI", "SK", "PT", "FR"]
    df = df[df['geo'].isin(geo_nat)]
    
    df = df[(df['values'].notnull()) 
            &(df['waste'] == 'TOTAL') 
            & (df['hazard'] == 'HAZ_NHAZ') 
            & (df['unit'] == 'T') 
            & (df['wst_oper'] != 'TRT')
            & (df['geo'] == geo)
            & (df['time'] == year)
            ]
    df = df[["wst_oper", 'values']]
    
    wst_oper_name = {
            "DSP_L_OTH": "Disposal - landfill and others",
            "DSP_L": "Disposal - landfill",
            "DSP_I": "Disposal - incineration",
            "DSP_OTH": "Disposal - other",
            "RCV_E": "Recovery - energy recovery",
            "RCV_R_B": "Recovery - recycling and backfilling",
            "RCV_R": "Recovery - recycling",
            "RCV_B": "Recovery - backfilling"
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
        
    option = horizontal_bar_chart("Treatment of waste by waste management operations in " + geo, 
                                  "Year: " + year, wst_oper_list, data)
    return Response(option)


@api_view(["GET"])
def dash2_q52(request):
    dataset_code = "env_wastrt"
    df = json_to_dataframe(dataset_code)
    geo = request.GET.get("geo")
    year = request.GET.get("year")
    return d2_pie_chart_waste_dim(geo, year, df)


def d2_pie_chart_waste_dim(geo, year, df):
    
    geo_nat = ["DE", "FI", "SK", "PT", "FR"]
    df = df[df['geo'].isin(geo_nat)]
    
    df = df[(df['values'].notnull()) 
            &(df['waste'] == 'TOTAL') 
            & (df['hazard'] == 'HAZ_NHAZ') 
            & (df['unit'] == 'T') 
            & (df['wst_oper'] != 'TRT')
            & (df['geo'] == geo)
            & (df['time'] == year)
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
    
    option = donut_chart('Treatment of waste operation domain in ' + geo, "Year: " + year, data, colors)
    return Response(option)


# ----------------------- Employment -----------------------

def dash2_q61():
    dataset_code = "tgs00007"
    df = json_to_dataframe(dataset_code)
    return d2_line_chart_employment_rate(df)


def d2_line_chart_employment_rate(df):
    
    geo_nuts2 = ["DEA2", "FI1B", "SK03", "PT17", "FR10"]
    df = df[df['geo'].isin(geo_nuts2)]
    
    df = df[(df['values'].notnull()) & (df['sex'] == 'T')]
    df = df[['values', 'geo', 'time']]
    
    geo_name = {
        "DEA2": "Köln",
        "FI1B": "Helsinki-Uusimaa",
        "SK03": "Stredné Slovensko",
        "PT17": "Área Metropolitana de Lisboa",
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
    
    option = line_chart("Employment rate of population in productive age", geo_list, year_list, result)
    return Response(option)


def dash2_q62(request):
    dataset_code = "tgs00007"
    df = json_to_dataframe(dataset_code)
    year = request.GET.get("year")
    return d2_bar_chart_employment_rate_by_sex(year, df)


def d2_bar_chart_employment_rate_by_sex(year, df):
    
    geo_nuts2 = ["DEA2", "FI1B", "SK03", "PT17", "FR10"]
    df = df[df['geo'].isin(geo_nuts2)]
    
    df = df[(df['values'].notnull()) & (df['sex'] != 'T') & (df['time'] == year)]
    df = df[['values', 'geo', 'sex']]
    
    geo_name = {
        "DEA2": "Köln",
        "FI1B": "Helsinki-Uusimaa",
        "SK03": "Stredné Slovensko",
        "PT17": "Área M. de Lisboa",
        "FR10": "Ile de France"
    }
    df['geo'] = df['geo'].replace(geo_name)
    
    df['sex'] = df['sex'].replace({'M': 'Male', 'F': 'Female'})
    
    dimensions = ['geo'] + ['Male'] + ['Female']
    pivot_df = df.pivot(index='geo', columns='sex', values='values').reset_index()
    source = pivot_df.to_dict(orient='records')
    
    option = donut_chart("Employment rate by sex", year, dimensions, source)
    return Response(option)