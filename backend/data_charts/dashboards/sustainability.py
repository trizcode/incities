from rest_framework.decorators import api_view
from rest_framework.response import Response
from data_charts.scripts.utils import *
from data_charts.scripts.charts import *
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from django.views.decorators.cache import cache_page


# ----------------------- Air Quality -----------------------


@api_view(["GET"])
def bar_chart_air_quality(request):
    
    df = get_openweather_api_data()
    kpi = request.GET.get("kpi")

    color_mapping = {
        "Cologne": "#6272A4",
        "Helsinki": "#8BE9FD",
        "Zilina": "#FFB86C",
        "Lisbon": "#FF79C6",
        "Paris": "#BD93F9"
    }
    
    if kpi == "no2":
        kpi = "Concentration of NO2 (µg/m³)"
        df = df[df["indicator_name"] == "no2"]
    if kpi == "pm10":
        kpi = "Concentration of PM10 (µg/m³)"
        df = df[df["indicator_name"] == "pm10"]
    
    df = df[["values", "cities", "date"]]
    df = df.sort_values(by='values')
    
    cities_list = df['cities'].unique().tolist()
    values_list = df['values'].tolist()
    
    colors = [color_mapping.get(region) for region in cities_list]
    
    option = basic_bar_chart(kpi, "Last update at: " + df['date'].unique()[0], cities_list, values_list, colors)
    
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
def line_chart_GHG(request):
    
    dataset_code = request.GET.get("dataset_code")
    df = json_to_dataframe(dataset_code, 'nat')
    
    df = df[["values", "geo", "time"]]
    kpi = "Greenhouse gases emissions from production activities (Kilograms per capita)"

    geo_name = {
        "DE": "Germany",
        "FI": "Finland",
        "SK": "Slovakia",
        "PT": "Portugal",
        "FR": "France"
    }
    color_mapping = {
        "Germany": "#6272A4",
        "Finland": "#8BE9FD",
        "Slovakia": "#FFB86C",
        "Portugal": "#FF79C6",
        "France": "#BD93F9"
    } 
    df['geo'] = df['geo'].replace(geo_name)
            
    df["values"] = df["values"].round(2)
    
    common_years = df.groupby('geo')['time'].apply(set).reset_index()
    common_years = set.intersection(*common_years['time'])
    df = df[df['time'].isin(common_years)]
    
    df_grouped = df.groupby('geo').agg(list).reset_index()
    
    result = []
    for index, row in df_grouped.iterrows():
        region_name = row['geo']
        color = color_mapping.get(region_name)
        data_dict = {
            'name': region_name,
            'type': 'line',
            'data': row['values'],
            'itemStyle': {'color': color}
        }
        result.append(data_dict)
    
    geo_list = df['geo'].unique().tolist()    
    year_list = df['time'].unique().tolist()
    
    option = line_chart(kpi, "", geo_list, year_list, result)
    
    return Response(option)


@api_view(["GET"])
def bar_chart_GHG(request):
    
    dataset_code = request.GET.get("dataset_code")
    df = json_to_dataframe(dataset_code, 'nat')

    kpi = "Greenhouse gases emissions from production activities (Kilograms per capita)"

    geo_name = {
        "DE": "Germany",
        "FI": "Finland",
        "SK": "Slovakia",
        "PT": "Portugal",
        "FR": "France"
    }
    color_mapping = {
        "Germany": "#6272A4",
        "Finland": "#8BE9FD",
        "Slovakia": "#FFB86C",
        "Portugal": "#FF79C6",
        "France": "#BD93F9"
    } 
    
    max_year = df['time'].max()
    df = df[df['time'] == max_year]
    
    df = df[["values", "geo"]]
    
    df['geo'] = df['geo'].replace(geo_name)
    
    df = df.sort_values(by='values')
    
    geo_list = df['geo'].unique().tolist()
    values_list = df['values'].tolist()
    
    colors = [color_mapping.get(region) for region in geo_list]
    
    option = basic_bar_chart(kpi, f"Year: {max_year}", geo_list, values_list, colors)
    
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
    color_mapping = {
        "Germany": "#6272A4",
        "Finland": "#8BE9FD",
        "Slovakia": "#FFB86C",
        "Portugal": "#FF79C6",
        "France": "#BD93F9"
    } 
    df['geo'] = df['geo'].replace(geo_name)
    
    df = df[["values", "geo", "time"]]
    df['geo'] = df['geo'].replace(geo_name)

    common_years = df.groupby('geo')['time'].apply(set).reset_index()
    common_years = set.intersection(*common_years['time'])
    df = df[df['time'].isin(common_years)]
    
    df_grouped = df.groupby('geo').agg(list).reset_index()
    
    result = []
    for index, row in df_grouped.iterrows():
        region_name = row['geo']
        color = color_mapping.get(region_name)
        data_dict = {
            'name': region_name,
            'type': 'line',
            'data': row['values'],
            'itemStyle': {'color': color}
        }
        result.append(data_dict)
                
    geo_list = df['geo'].unique().tolist()    
    year_list = df['time'].unique().tolist()
        
    if kpi == 'REN':
        kpi = ' Total renewable energy sources (%)'
    elif kpi == 'REN_TRA':
        kpi = 'Renewable energy sources in transport (%)'
    elif kpi == 'REN_ELC':
        kpi = 'Renewable energy sources in electricity (%)'
    else:
        kpi = 'Renewable energy sources in heating and cooling (%)'
        
    option = line_chart("Share of renewable energy in gross final energy consumption by Sector", kpi, geo_list, year_list, result)
    
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
    
    color_mapping = {
        "Germany": "#6272A4",
        "Finland": "#8BE9FD",
        "Slovakia": "#FFB86C",
        "Portugal": "#FF79C6",
        "France": "#BD93F9"
    }

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
           
    colors = [color_mapping.get(region) for region in geo_list]
    
    option = basic_bar_chart("Share of renewable energy in gross final energy consumption by Sector", kpi + " - " + str(max_year), geo_list, values_list, colors)
    
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
    
    color_mapping = {
        "Germany": "#6272A4",
        "Finland": "#8BE9FD",
        "Slovakia": "#FFB86C",
        "Portugal": "#FF79C6",
        "France": "#BD93F9"
    }
    
    df = df.sort_values(by='values')
    df['values'] = ((df['values'] / df['values'].sum()) * 100).round(2)
    
    geo_list = df['geo'].unique().tolist()   
    values_list = df['values'].unique().tolist()
    
    colors = [color_mapping.get(region) for region in geo_list]
        
    option = basic_bar_chart("Protected Terrestrial Area (%)", "Year: " + str(max_year), geo_list, values_list, colors)
    
    return Response(option)


# ----------------------- Environmental quality -----------------------

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
    
    color_mapping = {
        "Germany": "#6272A4",
        "Finland": "#8BE9FD",
        "Slovakia": "#FFB86C",
        "Portugal": "#FF79C6",
        "France": "#BD93F9"
    }  
    
    common_years = df.groupby('geo')['time'].apply(set).reset_index()
    common_years = set.intersection(*common_years['time'])
    df = df[df['time'].isin(common_years)]
    
    df_grouped = df.groupby('geo').agg(list).reset_index()
    
    result = []
    for index, row in df_grouped.iterrows():
        region_name = row['geo']
        color = color_mapping.get(region_name)
        data_dict = {
            'name': region_name,
            'type': 'line',
            'data': row['values'],
            'itemStyle': {'color': color}
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
    
    color_mapping = {
        "Germany": "#6272A4",
        "Finland": "#8BE9FD",
        "Slovakia": "#FFB86C",
        "Portugal": "#FF79C6",
        "France": "#BD93F9"
    }  
    df = df.sort_values(by='values')

    geo_list = df['geo'].unique().tolist()
    values_list = df['values'].tolist()
    
    colors = [color_mapping.get(region) for region in geo_list]

    option = basic_bar_chart("Share of Waste Recycled (Tonne)", "Year: " + str(max_year), geo_list, values_list, colors)
    
    return Response(option)


# ----------------------- Employment -----------------------

@cache_page(60 * 60 * 24 * 365)
@api_view(["GET"])
def line_chart_employment(request):
    
    df = json_to_dataframe("tgs00007", 'nuts2')
    
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
    
    color_mapping = {
        "Cologne": "#6272A4",
        "Helsinki-U.": "#8BE9FD",
        "S. Slovensko": "#FFB86C",
        "A. M. Lisboa": "#FF79C6",
        "Ile de France": "#BD93F9"
    } 
    
    common_years = df.groupby('geo')['time'].apply(set).reset_index()
    common_years = set.intersection(*common_years['time'])
    df = df[df['time'].isin(common_years)]
    
    df_grouped = df.groupby('geo').agg(list).reset_index()
    
    result = []
    for index, row in df_grouped.iterrows():
        region_name = row['geo']
        color = color_mapping.get(region_name)
        data_dict = {
            'name': region_name,
            'type': 'line',
            'data': row['values'],
            'itemStyle': {'color': color}
        }
        result.append(data_dict)
                
    geo_list = df['geo'].unique().tolist()    
    year_list = df['time'].unique().tolist()
    
    option = line_chart("Persons employed in productive age (%)", "", geo_list, year_list, result)
       
    return Response(option)


@api_view(["GET"])
def bar_chart_employment(request):
    
    df = json_to_dataframe("tgs00007", 'nuts2')
     
    df = df[(df['sex'] != 'T')]
    max_year = df['time'].max()
    df = df[df['time'] == max_year]
    df = df[["values", "geo", "sex"]]
    geo_name = {
        "DEA2": "Köln",
        "FI1B": "Helsinki-U.",
        "SK03": "S. Slovensko",
        "PT17": "A. M. de Lisboa",
        "FR10": "Ile de France"
    }
    df['geo'] = df['geo'].replace(geo_name)
    
    sex_name = {"M": "Male", "F": "Female"}
    df['sex'] = df['sex'].replace(sex_name)
    
    color_map = {
        'Male': '#6272A4',
        'Female': '#FF79C6'
    }
    
    fig = px.bar(
        df,
        x='geo',
        y='values',
        color='sex',
        color_discrete_map=color_map, 
        barmode='stack',
        title='Persons employed in productive age (%) - ' + str(max_year),
        text='values'
    )

    fig.update_layout(
        xaxis_title='Nuts 2 regions',
        yaxis_title='% of Persons',
        xaxis=dict(tickmode='array', tickvals=df['geo'].unique(), ticktext=df['geo'].unique())
    )

    fig = pio.to_json(fig)
    
    return Response(fig)


# ----------------------- Health -----------------------

@api_view(["GET"])
def line_chart_health(request):
    
    kpi = request.GET.get("dataset_code")
    if kpi in ["hlth_cd_yro", "hlth_cd_yinfr"]:
        df = json_to_dataframe(kpi, 'nuts2')
    
    if kpi in ["hlth_cd_yro", "hlth_cd_yinfr"]:
        if kpi == "hlth_cd_yro":
            df = df[(df['age'] == 'TOTAL') & (df['icd10'] == 'U071') & (df['resid'] == 'TOT_IN') & (df['sex'] == 'T')]    
            kpi = "Share of Total deaths"
        else:
            df = df[(df['age'] == 'TOTAL') & (df['icd10'] == 'U071') & (df['resid'] == 'TOT_IN') & (df['sex'] == 'T') & (df["unit"] == "NR")]
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
            df = df[(df['sex'] == 'T') & (df['resid'] == 'TOT_IN') & (df['icd10'] == 'A-R_V-Y') & (df['age'] == 'TOTAL') & (df['unit'] == 'NR')]
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
        "PT001C":"Lisbon",
        "FR001C":"Paris",
        "DE004C":"Cologne",
        "SK006C":"Zilina"
    }
    df['cities'] = df['cities'].replace(geo_name)
    
    color_mapping = {
        "Cologne": "#6272A4",
        "Helsinki": "#8BE9FD",
        "Zilina": "#FFB86C",
        "Lisbon": "#FF79C6",
        "Paris": "#BD93F9"
    } 

    common_years = df.groupby('cities')['time'].apply(set).reset_index()
    common_years = set.intersection(*common_years['time'])
    df = df[df['time'].isin(common_years)]
    
    df_grouped = df.groupby('cities').agg(list).reset_index()
    
    result = []
    for index, row in df_grouped.iterrows():
        region_name = row['cities']
        color = color_mapping.get(region_name)
        data_dict = {
            'name': region_name,
            'type': 'line',
            'data': row['values'],
            'itemStyle': {'color': color}
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
        "PT001C":"Lisbon",
        "FR001C":"Paris",
        "DE004C":"Cologne",
        "SK006C":"Zilina"
    }
    df['cities'] = df['cities'].replace(geo_name)
    
    color_mapping = {
        "Cologne": "#6272A4",
        "Helsinki": "#8BE9FD",
        "Zilina": "#FFB86C",
        "Lisbon": "#FF79C6",
        "Paris": "#BD93F9"
    } 
    
    df = df[df['time'] == 2020]
    
    df = df[["values", "cities"]]
    
    df['cities'] = df['cities'].replace(geo_name)

    df = df.sort_values(by='values')

    geo_list = df['cities'].unique().tolist()
    values_list = df['values'].tolist()
    
    colors = [color_mapping.get(region) for region in geo_list]

    option = basic_bar_chart("Number of murders and violent deaths", "Year: 2020", geo_list, values_list, colors)

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
        "PT001C":"Lisbon",
        "FR001C":"Paris",
        "DE004C":"Cologne",
        "SK006C":"Zilina"
    }
    df['cities'] = df['cities'].replace(geo_name)
    
    color_mapping = {
        "Cologne": "#6272A4",
        "Helsinki": "#8BE9FD",
        "Zilina": "#FFB86C",
        "Lisbon": "#FF79C6",
        "Paris": "#BD93F9"
    }

    common_years = df.groupby('cities')['time'].apply(set).reset_index()
    common_years = set.intersection(*common_years['time'])
    df = df[df['time'].isin(common_years)]
    
    df_grouped = df.groupby('cities').agg(list).reset_index()
    
    result = []
    for index, row in df_grouped.iterrows():
        region_name = row['cities']
        color = color_mapping.get(region_name)
        data_dict = {
            'name': region_name,
            'type': 'line',
            'data': row['values'],
            'itemStyle': {'color': color}
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
        "PT001C":"Lisbon",
        "FR001C":"Paris",
        "DE004C":"Cologne",
        "SK006C":"Zilina"
    }
    df['cities'] = df['cities'].replace(geo_name)
    
    color_mapping = {
        "Cologne": "#6272A4",
        "Helsinki": "#8BE9FD",
        "Zilina": "#FFB86C",
        "Lisbon": "#FF79C6",
        "Paris": "#BD93F9"
    }
    
    df = df[df['time'] == 2020]
    
    df = df[["values", "cities"]]
    
    df['cities'] = df['cities'].replace(geo_name)
    
    df = df.sort_values(by='values')

    geo_list = df['cities'].unique().tolist()
    values_list = df['values'].tolist()
    
    colors = [color_mapping.get(region) for region in geo_list]
    
    option = basic_bar_chart("Share of students in higher education", "Year: 2020", geo_list, values_list, colors)
    
    return Response(option)