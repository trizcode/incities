from rest_framework.decorators import api_view
from rest_framework.response import Response
from data_charts.scripts.utils import *
from data_charts.scripts.charts import *
import plotly.io as pio
import plotly.graph_objects as go
from django.views.decorators.cache import cache_page


# Adicionar expansão com tabela de indicadores -> explicar indicadores de sustentabilidade

# ----------------------- Air Quality -----------------------

@api_view(["GET"])
def grouped_bar_chart_air_quality(request):

    df = get_openweather_api_data()

    df = df[['values', 'cities', 'indicator_name', 'date']]
    
    dimensions = ['cities'] + ['no2'] + ['pm10'] + ['pm2_5']
    pivot_df = df.pivot(index='cities', columns='indicator_name', values='values').reset_index()
    source = pivot_df.to_dict(orient='records')
    
    option = grouped_bar_chart_3("Concentration of NO2, PM10 and PM2.5 (µg/m³)", "Last update at: " + df['date'].unique()[0], dimensions, source)
    
    return Response(option)


@api_view(["GET"])
def bar_chart_air_quality(request):
    
    df = get_openweather_api_data()
    kpi = request.GET.get("kpi")
    
    return d2_bar_chart_air_quality(df, kpi)

def d2_bar_chart_air_quality(df, kpi):
    
    if kpi == "no2":
        kpi = "Concentration of NO2 (µg/m³)"
        df = df[df["indicator_name"] == "no2"]
    elif kpi == "pm10":
        kpi = "Concentration of PM10 (µg/m³)"
        df = df[df["indicator_name"] == "pm10"]
    else:
        kpi = "Concentration of PM2.5 (µg/m³)"
        df = df[df["indicator_name"] == "pm2_5"]
    
    df = df[["values", "cities", "date"]]
    df = df.sort_values(by='values')
    
    cities_list = df['cities'].unique().tolist()
    values_list = df['values'].tolist()
    
    option = basic_bar_chart(kpi, "Last update at: " + df['date'].unique()[0], cities_list, values_list)
    
    return Response(option)


@api_view(["GET"])
def card_air_quality(request): 
    df = get_openweather_api_data()
    kpi = request.GET.get("kpi")
    return d2_card_air_quality(df, kpi)


def d2_card_air_quality(df, kpi):

    if kpi == "no2":
        df = df[df["indicator_name"] == "no2"]
        ranges = [(0, 20), (20, 70), (70, 150), (150, 200), (200, float('inf'))]
    elif kpi == "pm10":
        df = df[df["indicator_name"] == "pm10"]
        ranges = [(0, 20), (20, 50), (50, 100), (100, 200), (200, float('inf'))]
    else:
        df = df[df["indicator_name"] == "pm2_5"]
        ranges = [(0, 10), (10, 25), (25, 50), (50, 75), (75, float('inf'))]

    df = df[["values", "cities"]]
    df = df.sort_values(by='values')
    
    scale_labels = ["Good", "Fair", "Moderate", "Poor", "Very Poor"]
    
    figures_json = []
    for _, row in df.iterrows():
        value = row["values"]
        city = row["cities"]
        
        if value < ranges[1][0]:
            color = "green"
            scale = scale_labels[0]
        elif value < ranges[2][0]:
            color = "orange"
            scale = scale_labels[1]
        elif value < ranges[3][0]:
            color = "orange"
            scale = scale_labels[2]
        elif value < ranges[4][0]:
            color = "red"
            scale = scale_labels[3]
        else:
            color = "red"
            scale = scale_labels[4]
        
        fig = go.Figure(go.Indicator(
            mode="number",
            value=value,
            title={'text': f"{city}<br><span style='font-size:20px;color:{color}'>{scale}</span>",
                   'font': {'size': 18}},
            number={'font': {'color': color, 'size': 48}},
        ))
        
        fig.update_layout(
            margin={'t': 0, 'b': 0, 'l': 0, 'r': 0},
            height=150,
            width=200,
        )
        
        figures_json.append(pio.to_json(fig))
    
    return Response(figures_json)


@api_view(["GET"])
def line_chart_air_quality(request):
    
    dataset_code = "cei_gsr011"
    df = json_to_dataframe(dataset_code, 'nat')
    
    return d2_line_chart_air_quality(df)


def d2_line_chart_air_quality(df):
    
    df = df[["values", "geo", "time"]]
    kpi = "Greenhouse gases emissions from production activities (Kilograms per capita)"

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


# ----------------------- Energy -----------------------

@cache_page(60 * 60 * 24 * 365)
@api_view(["GET"])
def line_chart_energy(request):
    
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
        kpi = ' Total renewable energy sources (%)'
    elif kpi == 'REN_TRA':
        kpi = 'Renewable energy sources in transport (%)'
    elif kpi == 'REN_ELC':
        kpi = 'Renewable energy sources in electricity (%)'
    else:
        kpi = 'Renewable energy sources in heating and cooling (%)'
        
    option = line_chart(kpi, "", geo_list, year_list, result)
    
    return Response(option)


@cache_page(60 * 60 * 24 * 365)
@api_view(["GET"])
def bar_chart_energy(request):
    
    dataset_code = "sdg_07_40"
    df = json_to_dataframe(dataset_code, 'nat')
    kpi = request.GET.get("nrg_bal")

    df = df[df['nrg_bal'] == kpi]
    
    max_year = df['time'].max()
    df = df[df['time'] == max_year]
    
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
        kpi = 'Total renewable energy sources (%)'
    elif kpi == 'REN_TRA':
        kpi = 'Renewable energy sources in transport (%)'
    elif kpi == 'REN_ELC':
        kpi = 'Renewable energy sources in electricity (%)'
    else:
        kpi = 'Renewable energy sources in heating and cooling (%)'
           
    option = basic_bar_chart(kpi, "Year: " + str(max_year), geo_list, values_list, color="#50FA7B")
    
    return Response(option)


@cache_page(60 * 60 * 24 * 365)
@api_view(["GET"])
def donut_chart_energy(request):

    df = json_to_dataframe("sdg_07_40", 'nat')
    geo = request.GET.get("geo")
    
    df = df[(df['nrg_bal'] != 'REN') & (df['geo'] == geo)]
    
    max_year = df['time'].max()
    df = df[df['time'] == max_year]
    
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
    
    option = donut_chart("Renewable energy source by sector in " + geo, 'Year: ' + str(max_year), result, colors)
    
    return Response(option)


# ----------------------- Biodiversity -----------------------

@cache_page(60 * 60 * 24 * 365)
@api_view(["GET"])
def bar_chart_TPA_prot_area(request):
    
    dataset_code = "env_bio4"
    df = json_to_dataframe(dataset_code, 'nat')
    
    df = df[(df['areaprot'] == 'TPA') & (df['unit'] == 'KM2')]
    max_year = df['time'].max()
    df = df[df['time'] == max_year]
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
        
    option = basic_bar_chart("Terrestrial protected area (Km)", "Year: " + str(max_year), geo_list, values_list)
    
    return Response(option)


@cache_page(60 * 60 * 24 * 365)
@api_view(["GET"])
def bar_chart_MPA_prot_area(request):
    
    dataset_code = "env_bio4"
    df = json_to_dataframe(dataset_code, 'nat')
    
    df = df[(df['areaprot'] == 'MPA') & (df['unit'] == 'KM2')]
    max_year = df['time'].max()
    df = df[df['time'] == max_year]
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
        
    option = basic_bar_chart("Marine protected area (Km)", "Year: " + str(max_year), geo_list, values_list, color='#FF79C6')
    
    return Response(option)


@cache_page(60 * 60 * 24 * 365)
@api_view(["GET"])
def grouped_bar_chart_prot_area(request):
    
    dataset_code = "env_bio4"
    df = json_to_dataframe(dataset_code, 'nat')
    
    df = df[df['unit'] == 'KM2']
    max_year = df['time'].max()
    df = df[df['time'] == max_year]    
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
    
    
    option = grouped_bar_chart_2("Protected Areas", "Year: " + str(max_year), dimensions, source)
    
    return Response(option)


@cache_page(60 * 60 * 24 * 365)
@api_view(["GET"])
def donut_chart_prot_area(request):
    
    dataset_code = "env_bio4"
    df = json_to_dataframe(dataset_code, 'nat')
    geo = request.GET.get("geo")
    
    df = df[(df['unit'] == 'PC') & (df['geo'] == geo)]
    max_year = df['time'].max()
    df = df[df['time'] == max_year]
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
    
    option = donut_chart("Protected Area (%) in " + geo, 'Year: ' + str(max_year), result, colors)
    
    return Response(option)


# ----------------------- Waste Management -----------------------

@cache_page(60 * 60 * 24 * 365)
@api_view(["GET"])
def line_chart_waste(request):
    
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
        "DSP_L": "Landfill (disposal)",
        "DSP_I": "Incineration (disposal)",
        "RCV_E": "Energy (recovery)",
        "RCV_R_B": "Recycling (recovery)"
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
        
    option = line_chart("Treatment of Waste by Disposal and Recovery Operations (Tonne)", geo, wst_oper_list, year_list, result)
    
    return Response(option)


@cache_page(60 * 60 * 24 * 365)
@api_view(["GET"])
def line_chart_waste_recycled(request):

    dataset_code = "env_wastrt"
    df = json_to_dataframe(dataset_code, 'nat')
    
    df = df[(df['waste'] == 'TOTAL')
            & (df['hazard'] == 'HAZ_NHAZ')
            & (df['unit'] == 'T')
            & (df['wst_oper'] == "RCV_R_B")]
    
    df = df[["values", "geo", "time"]]
    
    geo_name = {
        "DE": "Germany",
        "FI": "Finland",
        "SK": "Slovakia",
        "PT": "Portugal",
        "FR": "France"
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
            'itemStyle': {'color': colors[index % len(colors)]}
        }
        result.append(data_dict)
                
    geo_list = df['geo'].unique().tolist()    
    year_list = df['time'].unique().tolist()
    
    option = line_chart("Share of Waste Recycled (Tonne)", "", geo_list, year_list, result)
    
    return Response(option)


@cache_page(60 * 60 * 24 * 365)
@api_view(["GET"])
def bar_chart_waste_recycled(request):
    
    dataset_code = "env_wastrt"
    df = json_to_dataframe(dataset_code, 'nat')
    
    df = df[(df['waste'] == 'TOTAL')
            & (df['hazard'] == 'HAZ_NHAZ')
            & (df['unit'] == 'T')
            & (df['wst_oper'] == "RCV_R_B")]
    
    max_year = df['time'].max()
    df = df[df['time'] == max_year]
    
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

    option = basic_bar_chart("Share of Waste Recycled (Tonne)", "Year: " + str(max_year), geo_list, values_list)
    
    return Response(option)


@cache_page(60 * 60 * 24 * 365)
@api_view(["GET"])
def donut_chart_waste(request):
    
    dataset_code = "env_wastrt"
    df = json_to_dataframe(dataset_code, 'nat')
    geo = request.GET.get("geo")
    
    df = df[(df['waste'] == 'TOTAL')
            & (df['hazard'] == 'HAZ_NHAZ')
            & (df['unit'] == 'T')
            & (df['wst_oper'].isin(["DSP_L", "DSP_I", "RCV_E", "RCV_R_B"]))
            & (df['geo'] == geo)]
    
    max_year = df['time'].max()
    df = df[df['time'] == max_year]
    
    df = df[["wst_oper", 'values']]
    
    df["values"] = df["values"].astype('int')
    
    wst_oper_name = {
        "DSP_L": "Landfill",
        "DSP_I": "Incineration",
        "RCV_E": "Energy recovery",
        "RCV_R_B": "Recycling"
    }
    df['wst_oper'] = df['wst_oper'].replace(wst_oper_name)
    
    total = df['values'].sum()
    df['normalized_values'] = df['values'] / total * 100
    df['normalized_values'] = df['normalized_values'].round(2)

    data = [{"value": row['normalized_values'], "name": row['wst_oper']} for _, row in df.iterrows()]

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
        
    colors = ['#50FA7B', '#44475A', '#FF79C6', '#FFB86C']
    
    option = donut_chart('Share of Waste Treatment (%) - ' + geo, "Year: " + str(max_year), data, colors)
    
    return Response(option)


# ----------------------- Employment -----------------------

@cache_page(60 * 60 * 24 * 365)
@api_view(["GET"])
def line_chart_employment(request):
    
    dataset_code = "tgs00007"
    df = json_to_dataframe(dataset_code, 'nuts2')
    
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
    
    option = line_chart("Persons employed in productive age (%)", "Between the ages of 20 and 64", geo_list, year_list, result)
    
    return Response(option)


@cache_page(60 * 60 * 24 * 365)
@api_view(["GET"])
def donut_chart_employment(request): # Susbtituir por gráfico de barras a separar sexos
    
    dataset_code = "tgs00007"
    df = json_to_dataframe(dataset_code, 'nuts2')
    geo = request.GET.get("geo")
    
    df = df[(df['sex'] != 'T') & (df['geo'] == geo)]
    max_year = df['time'].max()
    df = df[df['time'] == max_year]
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
    
    option = donut_chart("% of persons employed in productive age: " + geo, "Year: " + str(max_year), result, colors)
    
    return Response(option)


# ----------------------- Infrastructure -----------------------

@cache_page(60 * 60 * 24 * 365)
@api_view(["GET"])
def line_chart_infrastructure(request):
    
    dataset_code = "tgs00047"
    df = json_to_dataframe(dataset_code, 'nuts2')
    
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
    
    option = line_chart("% of Households that have Internet access at home", "", geo_list, year_list, result)
    
    return Response(option)


@cache_page(60 * 60 * 24 * 365)
@api_view(["GET"])
def bar_chart_infrastructure(request):
    
    dataset_code = "tgs00047"
    df = json_to_dataframe(dataset_code, 'nuts2')
    
    max_year = df['time'].max()
    df = df[df['time'] == max_year]
    
    df = df[["values", "geo"]]
    
    geo_name = {
        "DEA2": "Köln",
        "FI1B": "Helsinki-U.",
        "SK03": "S. Slovensko",
        "PT17": "A. M. Lisboa",
        "FR10": "Ile de France"
    }
    df['geo'] = df['geo'].replace(geo_name)
    
    df = df.sort_values(by='values')

    geo_list = df['geo'].unique().tolist()
    values_list = df['values'].tolist()
    
    option = basic_bar_chart("% of Households that have Internet access at home", "Year: " + str(max_year), geo_list, values_list)
    
    return Response(option)


# ----------------------- Innovation -----------------------

@cache_page(60 * 60 * 24 * 365)
@api_view(["GET"])
def line_chart_innovation(request):
    
    dataset_code = "rd_p_persreg"
    df = json_to_dataframe(dataset_code, 'nuts2')

    df = df[(df['prof_pos'] == 'RSE') & (df['sectperf'] == 'TOTAL') & (df['geo'] != 'FR10') & (df['sex'] == 'T') & (df['unit'] == 'HC')]
    df = df[['values', 'geo', 'time']]

    geo_name = {
        "DEA2": "Köln",
        "FI1B": "Helsinki-U.",
        "SK03": "S. Slovensko",
        "PT17": "A. M. Lisboa"
    }
    df['geo'] = df['geo'].replace(geo_name)
    
    common_years = df.groupby('geo')['time'].apply(set).reset_index()
    common_years = set.intersection(*common_years['time'])
    df = df[df['time'].isin(common_years)]
    
    df_grouped = df.groupby('geo').agg(list).reset_index()
    
    result = []
    colors = ['#282A36', '#6272A4', '#FF79C6', '#50FA7B', '#BD93F9']
    
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
    
    option = line_chart("Head Count of Researchers", "All sectors of performance", geo_list, year_list, result)
    
    return Response(option)


@cache_page(60 * 60 * 24 * 365)
@api_view(["GET"])
def grouped_bar_chart_innovation(request):
    
    dataset_code = "rd_p_persreg"
    df = json_to_dataframe(dataset_code, 'nuts2')
    
    df = df[(df['prof_pos'] == 'RSE') & (df['sectperf'] != 'TOTAL') & (df['geo'] != 'FR10') & (df['sex'] == 'T') & (df['unit'] == 'HC')]    
    max_year = df['time'].max()
    df = df[df['time'] == max_year]
    df = df[["values", 'geo', 'sectperf', "time"]]
    
    geo_name = {
        "DEA2": "Köln",
        "FI1B": "Helsinki-U.",
        "SK03": "S. Slovensko",
        "PT17": "A. M. Lisboa"
    }
    df['geo'] = df['geo'].replace(geo_name)
    
    df['sectperf'] = df['sectperf'].replace({
        'BES': 'Business enterprise', 
        'GOV': 'Government',
        'HES': 'Higher education',
        'PNP': 'Private non-profit'
    })
    
    dimensions = ['geo'] + ['Business enterprise'] + ['Government'] + ['Higher education'] + ['Private non-profit']
    pivot_df = df.pivot(index='geo', columns='sectperf', values='values').fillna(0).reset_index()
    source = pivot_df.to_dict(orient='records')
    
    option = grouped_bar_chart_4("Head Count of Researchers by Sector of Performance", "Year: " + str(max_year), dimensions, source)
    
    return Response(option)


# ----------------------- Health -----------------------

@api_view(["GET"])
def line_chart_health(request):
    
    kpi = request.GET.get("dataset_code")
    df = json_to_dataframe(kpi, 'nuts2')
    
    if kpi in ["hlth_cd_yro", "hlth_cd_yinfr"]:
        if kpi == "hlth_cd_yro":
            df = df[(df['age'] == 'TOTAL') & (df['icd10'] == 'A-R_V-Y') & (df['resid'] == 'TOT_IN') & (df['sex'] == 'T')]    
            kpi = "Share of Total deaths"
        else:
            df = df[(df['age'] == 'TOTAL') & (df['icd10'] == 'A-R_V-Y') & (df['resid'] == 'TOT_IN') & (df['sex'] == 'T') & (df["unit"] == "PC")]
            kpi = "Infant mortality"
        
    df = df[["values", "geo", "time"]]
    geo_name = {
        "DEA2": "Köln",
        "FI1B": "Helsinki-U.",
        "SK03": "S. Slovensko",
        "PT17": "A. M. Lisboa",
        "FR10": "Ile France"
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
            'itemStyle': {'color': colors[index % len(colors)]}
        }
        result.append(data_dict)
                
    geo_list = df['geo'].unique().tolist()    
    year_list = df['time'].unique().tolist()
    
    option = line_chart(kpi, "", geo_list, year_list, result)
    
    return Response(option)


@cache_page(60 * 60 * 24 * 365)
@api_view(["GET"])
def bar_chart_health(request):
    
    kpi = request.GET.get("dataset_code")
    if kpi in ["hlth_cd_yro", "hlth_cd_yinfr"]:
        df = json_to_dataframe(kpi, 'nuts2')
        geo_name = {
            "DEA2": "Köln",
            "FI1B": "Helsinki-U.",
            "SK03": "S. Slovensko",
            "PT17": "A. M. Lisboa",
            "FR10": "Ile France"
        }
        if kpi == "hlth_cd_yro":
            df = df[(df['sex'] == 'T') & (df['resid'] == 'TOT_IN') & (df['icd10'] == 'A-R_V-Y') & (df['age'] == 'TOTAL')]
            kpi = "Share of Total deaths"
        else:
            df = df[(df['sex'] == 'T') & (df['resid'] == 'TOT_IN') & (df['icd10'] == 'A-R_V-Y') & (df['age'] == 'TOTAL') & (df['unit'] == 'PC')]
            kpi = "Infant mortality"
    
    max_year = df['time'].max()
    df = df[df['time'] == max_year]
    
    df = df[["values", "geo"]]
    
    df['geo'] = df['geo'].replace(geo_name)
    
    df = df.sort_values(by='values')

    geo_list = df['geo'].unique().tolist()
    values_list = df['values'].tolist()
    
    option = basic_bar_chart(kpi, "Year: " + str(max_year), geo_list, values_list)
    
    return Response(option)


# ----------------------- Safety -----------------------

@cache_page(60 * 60 * 24 * 365)
@api_view(["GET"])
def line_chart_safety(request):
    
    df = json_to_dataframe("urb_clivcon", 'nuts3')
    df = df[df['indic_ur'] == 'SA3005V']
    df = df[["values", "cities", "time"]]
    
    geo_name = {
        "FI001C":"Helsinki",
        "PT001C":"Lisboa",
        "FR001C":"Paris",
        "DE004C":"Köln",
        "SK006C":"Zilina"
    }
    df['cities'] = df['cities'].replace(geo_name)

    common_years = df.groupby('cities')['time'].apply(set).reset_index()
    common_years = set.intersection(*common_years['time'])
    df = df[df['time'].isin(common_years)]
    
    df_grouped = df.groupby('cities').agg(list).reset_index()
    
    result = []
    colors = ['#6272A4', '#8BE9FD', '#FFB86C', '#FF79C6', '#BD93F9']
    
    for index, row in df_grouped.iterrows():
        data_dict = {
            'name': row['cities'],
            'type': 'line',
            'data': row['values'],
            'itemStyle': {'color': colors[index % len(colors)]}
        }
        result.append(data_dict)
                
    geo_list = df['cities'].unique().tolist()    
    year_list = df['time'].unique().tolist()
    
    option = line_chart("Number of murders and violent deaths", "", geo_list, year_list, result)
    
    return Response(option)


@cache_page(60 * 60 * 24 * 365)
@api_view(["GET"])
def bar_chart_safety(request):

    df = json_to_dataframe("urb_clivcon", 'nuts3')
    df = df[df['indic_ur'] == 'SA3005V']
    
    geo_name = {
        "FI001C":"Helsinki",
        "PT001C":"Lisboa",
        "FR001C":"Paris",
        "DE004C":"Köln",
        "SK006C":"Zilina"
    }
    df['cities'] = df['cities'].replace(geo_name)
    
    max_year = df['time'].max()
    df = df[df['time'] == max_year]
    
    df = df[["values", "cities"]]
    
    df['cities'] = df['cities'].replace(geo_name)
    
    df = df.sort_values(by='values')

    geo_list = df['cities'].unique().tolist()
    values_list = df['values'].tolist()
    
    option = basic_bar_chart("Number of murders and violent deaths", "Year: " + str(max_year), geo_list, values_list)
    
    return Response(option)


# ----------------------- Education -----------------------

@cache_page(60 * 60 * 24 * 365)
@api_view(["GET"])
def line_chart_education(request):
    
    df = json_to_dataframe("urb_ceduc", 'nuts3')
    df = df[df['indic_ur'] == 'TE1026I']
    
    df = df[["values", "cities", "time"]]
    
    geo_name = {
        "FI001C":"Helsinki",
        "PT001C":"Lisboa",
        "FR001C":"Paris",
        "DE004C":"Köln",
        "SK006C":"Zilina"
    }
    df['cities'] = df['cities'].replace(geo_name)

    common_years = df.groupby('cities')['time'].apply(set).reset_index()
    common_years = set.intersection(*common_years['time'])
    df = df[df['time'].isin(common_years)]
    
    df_grouped = df.groupby('cities').agg(list).reset_index()
    
    result = []
    colors = ['#6272A4', '#8BE9FD', '#FFB86C', '#FF79C6', '#BD93F9']
    
    for index, row in df_grouped.iterrows():
        data_dict = {
            'name': row['cities'],
            'type': 'line',
            'data': row['values'],
            'itemStyle': {'color': colors[index % len(colors)]}
        }
        result.append(data_dict)
                
    geo_list = df['cities'].unique().tolist()    
    year_list = df['time'].unique().tolist()
    
    option = line_chart("Share of students in higher education", "In the total population (per 1000 persons) (%)", geo_list, year_list, result)
    
    return Response(option)


@cache_page(60 * 60 * 24 * 365)
@api_view(["GET"])
def bar_chart_education(request):

    df = json_to_dataframe("urb_ceduc", 'nuts3')
    df = df[df['indic_ur'] == 'TE1026I']
    
    geo_name = {
        "FI001C":"Helsinki",
        "PT001C":"Lisboa",
        "FR001C":"Paris",
        "DE004C":"Köln",
        "SK006C":"Zilina"
    }
    df['cities'] = df['cities'].replace(geo_name)
    
    max_year = df['time'].max()
    df = df[df['time'] == max_year]
    
    df = df[["values", "cities"]]
    
    df['cities'] = df['cities'].replace(geo_name)
    
    df = df.sort_values(by='values')

    geo_list = df['cities'].unique().tolist()
    values_list = df['values'].tolist()
    
    option = basic_bar_chart("Share of students in higher education", "Year: " + str(max_year), geo_list, values_list)
    
    return Response(option)