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
        kpi = ' Total renewable energy sources'
    elif kpi == 'REN_TRA':
        kpi = 'Renewable energy sources in transport'
    elif kpi == 'REN_ELC':
        kpi = 'Renewable energy sources in electricity'
    else:
        kpi = 'Renewable energy sources in heating and cooling'
        
    option = line_chart("Share of renewable energy in gross final energy consumption (%)", kpi, geo_list, year_list, result)
    
    return Response(option)


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
        kpi = 'Total renewable energy sources'
    elif kpi == 'REN_TRA':
        kpi = 'Renewable energy sources in transport'
    elif kpi == 'REN_ELC':
        kpi = 'Renewable energy sources in electricity'
    else:
        kpi = 'Renewable energy sources in heating and cooling'
           
    colors = [color_mapping.get(region) for region in geo_list]
    
    option = basic_bar_chart("Share of renewable energy in gross final energy consumption (%)", kpi + " - " + str(max_year), geo_list, values_list, colors)
    
    return Response(option)


# ----------------------- Biodiversity -----------------------

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

@api_view(["GET"])
def line_chart_waste_recycled(request):

    df = json_to_dataframe("env_wastrt", 'nat')
    
    df = df[(df['waste'] == 'TOTAL')
            & (df['hazard'] == 'HAZ_NHAZ')
            & (df['unit'] == 'KG_HAB')
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
    
    option = line_chart("Share of Waste Recycled (Kilograms per capita)", "", geo_list, year_list, result)
    
    return Response(option)


@api_view(["GET"])
def bar_chart_waste_recycled(request):
    
    df = json_to_dataframe("env_wastrt", 'nat')
    
    df = df[(df['waste'] == 'TOTAL')
        & (df['hazard'] == 'HAZ_NHAZ')
        & (df['unit'] == 'KG_HAB')
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

    option = basic_bar_chart("Share of Waste Recycled (Kilograms per capita)", "Year: " + str(max_year), geo_list, values_list, colors)
    
    return Response(option)


@api_view(['GET'])
def donut_chart_waste_recycled(request):
    
    df = json_to_dataframe("env_wastrt", 'nat')
    
    df = df[(df['waste'] == 'TOTAL')
        & (df['hazard'] == 'HAZ_NHAZ')
        & (df['unit'] == 'KG_HAB')
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

    total = df['values'].sum()
    df['normalized_values'] = df['values'] / total * 100
    df['normalized_values'] = df['normalized_values'].round(2)
    
    data = [
        {
            'value': row['normalized_values'], 
            'name': row['geo'],
            'itemStyle': {'color': color_mapping.get(row['geo'])}
        }
        for _, row in df.iterrows()
    ]
    
    option = donut_chart("Share of Waste Recycled (%)", 'Year: ' + str(max_year), data)
    
    return Response(option)


# ----------------------- Economic Sustainability -----------------------

@api_view(["GET"])
def line_chart_economic_sustainability(request):
    
    kpi = request.GET.get("dataset_code")
    
    if kpi in ["tgs00007", "tgs00047", "tgs00038"]:
        
        df = json_to_dataframe(kpi, 'nuts2')
    
        geo_name = {
            "DEA2": "Köln",
            "FI1B": "Helsinki-U.",
            "SK03": "S. Slovensko",
            "PT17": "A. M. Lisboa",
            "FR10": "Ile de France"
        }
        color_mapping = {
            "Köln": "#6272A4",
            "Helsinki-U.": "#8BE9FD",
            "S. Slovensko": "#FFB86C",
            "A. M. Lisboa": "#FF79C6",
            "Ile de France": "#BD93F9"
        }
        
        if kpi == "tgs00007":
            df = df[(df['sex'] == 'T')]
            kpi = "Employment rate between the ages of 15 and 64 (%)"
        elif kpi == "tgs00047":
            kpi = "Household level of internet access (%)"
        else:
            kpi = "Human resources in science and technology (%)"
    
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
    
    option = line_chart(kpi, "", geo_list, year_list, result)
    
    return Response(option) 
    



@api_view(["GET"])
def bar_chart_economic_sustainability(request):
    
    kpi = request.GET.get("dataset_code")
    
    if kpi in ["tgs00007", "tgs00047", "tgs00038"]:
        
        df = json_to_dataframe(kpi, 'nuts2')
    
        geo_name = {
            "DEA2": "Köln",
            "FI1B": "Helsinki-U.",
            "SK03": "S. Slovensko",
            "PT17": "A. M. Lisboa",
            "FR10": "Ile de France"
        }
        color_mapping = {
            "Köln": "#6272A4",
            "Helsinki-U.": "#8BE9FD",
            "S. Slovensko": "#FFB86C",
            "A. M. Lisboa": "#FF79C6",
            "Ile de France": "#BD93F9"
        }
        
        if kpi == "tgs00007":
            df = df[(df['sex'] == 'T')]
            kpi = "Employment rate between the ages of 15 and 64 (%)"
        elif kpi == "tgs00047":
            kpi = "Household level of internet access (%)"
        else:
            kpi = "Human resources in science and technology (%)"
    
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


@api_view(["GET"])
def stacked_bar_chart_employment(request):
    
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
        title='Persons employed in productive age by gender (%) - ' + str(max_year),
        text='values'
    )

    fig.update_layout(
        xaxis_title='Nuts 2 regions',
        yaxis_title='% of Persons',
        xaxis=dict(tickmode='array', tickvals=df['geo'].unique(), ticktext=df['geo'].unique())
    )

    fig = pio.to_json(fig)
    
    return Response(fig)


# ----------------------- Social Sustainability -----------------------

@api_view(["GET"])
def line_chart_social_sustainability(request):
    
    kpi = request.GET.get("dataset_code")
    
    if kpi in ["urb_clivcon", "urb_ceduc"]:
        df = json_to_dataframe(kpi, 'nuts3')
        
    if kpi in ["urb_clivcon", "urb_ceduc"]:
        
        geo_name = {
            "FI001C":"Helsinki",
            "PT001C":"Lisbon",
            "FR001C":"Paris",
            "DE004C":"Cologne",
            "SK006C":"Zilina"
        }
        color_mapping = {
            "Cologne": "#6272A4",
            "Helsinki": "#8BE9FD",
            "Zilina": "#FFB86C",
            "Lisbon": "#FF79C6",
            "Paris": "#BD93F9"
        } 
        
        if kpi == "urb_clivcon":
            df = df[df['indic_ur'] == 'SA3005V']
            kpi = "Number of murders and violent deaths"
        else:
            df = df[df['indic_ur'] == 'TE1026I']
            kpi = "Number of students in higher education"
        
        df = df[["values", "cities", "time"]]
        df['cities'] = df['cities'].replace(geo_name)

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
        
        option = line_chart(kpi, "", geo_list, year_list, result)
        
    if kpi in ["hlth_cd_yro", "hlth_cd_yinfr"]:

        if kpi == "hlth_cd_yro":
            option = {
                'title': {'text': 'Number of total deaths', 'subtext': ''},
                'tooltip': {'trigger': 'axis'},
                'legend': {'data': ['Köln',
                'Ile de France',
                'A. M. Lisboa',
                'S. Slovensko',
                'Helsinki-U.'],
                'bottom': '1%'},
                'grid': {'top': '15%',
                'right': '5%',
                'bottom': '8%',
                'left': '1%',
                'containLabel': 'true'},
                'xAxis': {'type': 'category',
                'data': ['2017', '2018', '2019', '2020', '2021']},
                'yAxis': {'type': 'value'},
                'series': [{'name': 'A. M. Lisboa',
                'type': 'line',
                'data': [26495.0, 26797.0, 27004.0, 28306.0, 29759.0],
                'itemStyle': {'color': '#FF79C6'}},
                {'name': 'Helsinki-U.',
                'type': 'line',
                'data': [11871.0, 12021.0, 12126.0, 12495.0, 12920.0],
                'itemStyle': {'color': '#8BE9FD'}},
                {'name': 'Ile de France',
                'type': 'line',
                'data': [76045.0, 76397.0, 76846.0, 81698.0, 83726.0],
                'itemStyle': {'color': '#BD93F9'}},
                {'name': 'Köln',
                'type': 'line',
                'data': [46448.0, 47346.0, 47976.0, 48792.0, 49441.0],
                'itemStyle': {'color': '#6272A4'}},
                {'name': 'S. Slovensko',
                'type': 'line',
                'data': [13321.0, 13274.0, 13392.0, 13787.0, 15365.0],
                'itemStyle': {'color': '#FFB86C'}}]}
        else:
            option = {
                'title': {'text': 'Infant mortality', 'subtext': ''},
                'tooltip': {'trigger': 'axis'},
                'legend': {'data': ['Köln',
                'Ile de France',
                'A. M. Lisboa',
                'S. Slovensko',
                'Helsinki-U.'],
                'bottom': '1%'},
                'grid': {'top': '15%',
                'right': '5%',
                'bottom': '8%',
                'left': '1%',
                'containLabel': 'true'},
                'xAxis': {'type': 'category',
                'data': ['2013',
                '2014',
                '2015',
                '2016',
                '2017',
                '2018',
                '2019',
                '2020',
                '2021']},
                'yAxis': {'type': 'value'},
                'series': [{'name': 'A. M. Lisboa',
                'type': 'line',
                'data': [102.0, 93.0, 88.0, 94.0, 96.0, 107.0, 106.0, 96.0, 82.0],
                'itemStyle': {'color': '#FF79C6'}},
                {'name': 'Helsinki-U.',
                'type': 'line',
                'data': [37.0, 33.0, 28.0, 30.0, 30.0, 31.0, 30.0, 29.0, 29.0],
                'itemStyle': {'color': '#8BE9FD'}},
                {'name': 'Ile de France',
                'type': 'line',
                'data': [681.0, 663.0, 682.0, 679.0, 708.0, 712.0, 708.0, 688.0, 678.0],
                'itemStyle': {'color': '#BD93F9'}},
                {'name': 'Köln',
                'type': 'line',
                'data': [131.0, 121.0, 129.0, 140.0, 155.0, 157.0, 157.0, 147.0, 135.0],
                'itemStyle': {'color': '#6272A4'}},
                {'name': 'S. Slovensko',
                'type': 'line',
                'data': [60.0, 62.0, 57.0, 49.0, 43.0, 43.0, 51.0, 55.0, 55.0],
                'itemStyle': {'color': '#FFB86C'}}]}
    
    return Response(option)


@api_view(["GET"])
def bar_chart_social_sustainability(request):
    
    kpi = request.GET.get("dataset_code")
    
    if kpi in ["urb_clivcon", "urb_ceduc"]:
        df = json_to_dataframe(kpi, 'nuts3')
        
    if kpi in ["urb_clivcon", "urb_ceduc"]:
        
        geo_name = {
            "FI001C":"Helsinki",
            "PT001C":"Lisbon",
            "FR001C":"Paris",
            "DE004C":"Cologne",
            "SK006C":"Zilina"
        }
        color_mapping = {
            "Cologne": "#6272A4",
            "Helsinki": "#8BE9FD",
            "Zilina": "#FFB86C",
            "Lisbon": "#FF79C6",
            "Paris": "#BD93F9"
        } 
        
        if kpi == "urb_clivcon":
            df = df[df['indic_ur'] == 'SA3005V']
            kpi = "Number of murders and violent deaths"
        else:
            df = df[df['indic_ur'] == 'TE1026I']
            kpi = "Number of students in higher education"
        
        max_year = df['time'].max()
        df = df[df['time'] == max_year]
        
        df = df[["values", "cities"]]
        
        df['cities'] = df['cities'].replace(geo_name)
        
        df = df.sort_values(by='values')
        
        geo_list = df['cities'].unique().tolist()
        values_list = df['values'].tolist()
        
        colors = [color_mapping.get(region) for region in geo_list]
        
        option = basic_bar_chart(kpi, f"Year: {max_year}", geo_list, values_list, colors)
        
    if kpi in ["hlth_cd_yro", "hlth_cd_yinfr"]:
        
        if kpi == "hlth_cd_yro":
            option = {
                'title': {'text': 'Number of deaths', 'subtext': 'All causes of death (A00-Y89) excluding S00-T98 - Year: 2021'},
                'grid': {'top': '15%',
                'right': '5%',
                'bottom': '5%',
                'left': '5%',
                'containLabel': 'true'},
                'tooltip': {},
                'xAxis': {'type': 'category',
                'data': ['Helsinki-U.',
                'S. Slovensko',
                'A. M. Lisboa',
                'Köln',
                'Ile de France']},
                'yAxis': {'type': 'value'},
                'series': [{'data': [{'value': 12920.0, 'itemStyle': {'color': '#8BE9FD'}},
                    {'value': 15365.0, 'itemStyle': {'color': '#FFB86C'}},
                    {'value': 29759.0, 'itemStyle': {'color': '#FF79C6'}},
                    {'value': 49441.0, 'itemStyle': {'color': '#6272A4'}},
                    {'value': 83726.0, 'itemStyle': {'color': '#BD93F9'}}],
                'type': 'bar'}]}
        else:
            option = {
                'title': {'text': 'Infant mortality', 'subtext': 'All causes of death (A00-Y89) excluding S00-T98 - Year: 2021'},
                'grid': {'top': '15%',
                'right': '5%',
                'bottom': '5%',
                'left': '5%',
                'containLabel': 'true'},
                'tooltip': {},
                'xAxis': {'type': 'category',
                'data': ['Helsinki-U.',
                'S. Slovensko',
                'A. M. Lisboa',
                'Köln',
                'Ile de France']},
                'yAxis': {'type': 'value'},
                'series': [{'data': [{'value': 29.0, 'itemStyle': {'color': '#8BE9FD'}},
                    {'value': 55.0, 'itemStyle': {'color': '#FFB86C'}},
                    {'value': 82.0, 'itemStyle': {'color': '#FF79C6'}},
                    {'value': 135.0, 'itemStyle': {'color': '#6272A4'}},
                    {'value': 678.0, 'itemStyle': {'color': '#BD93F9'}}],
                'type': 'bar'}]}
    
    return Response(option)