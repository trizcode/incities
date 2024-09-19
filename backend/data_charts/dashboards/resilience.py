from rest_framework.decorators import api_view
from rest_framework.response import Response
from data_charts.scripts.utils import *
from data_charts.scripts.charts import *
import plotly.express as px
import plotly.io as pio

# ----------------------- Social Resilience -----------------------

# Educational equality

@api_view(["GET"])
def bar_chart_educational_equality_by_sex(request):
    
    df = json_to_dataframe("tgs00109", "nuts2")
     
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
        title='Population Aged 25-64 with Tertiary Education (%) in ' + str(max_year),
        text='values'
    )

    fig.update_layout(
        xaxis_title='Nuts 2 regions',
        yaxis_title='% of Population',
        xaxis=dict(tickmode='array', tickvals=df['geo'].unique(), ticktext=df['geo'].unique())
    )

    fig = pio.to_json(fig)
    
    return Response(fig)


# Demography

@api_view(["GET"])
def donut_chart_demo_pop_productive_age(request):

    df = json_to_dataframe("demo_r_pjangrp3", "nuts3_1")

    df = df[
        (df['sex']== 'T') &
        (df['age'].isin([
            'Y15-19','Y20-24','Y25-29',
            'Y30-34','Y35-39','Y40-44',
            'Y45-49','Y50-54', 'Y55-59', 'Y60-64'])
        )
    ]
    max_year = df['time'].max()
    df = df[df['time'] == max_year]
    
    geo_name = {
        "FI1B1":"Helsinki",
        "PT170":"Lisbon",
        "FR101":"Paris",
        "DEA23":"Cologne",
        "SK031":"Zilina"
    }
    df['geo'] = df['geo'].replace(geo_name)
    
    color_mapping = {
        "Cologne": "#6272A4",
        "Helsinki": "#8BE9FD",
        "Zilina": "#FFB86C",
        "Lisbon": "#FF79C6",
        "Paris": "#BD93F9"
    }

    df = df[["values", "geo"]]
    
    df = df.groupby('geo')['values'].sum().reset_index()
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
    
    option = donut_chart("Population in productive age (%)", 'Year: ' + str(max_year), data)
    
    return Response(option)


@api_view(["GET"])
def donut_chart_demo_pop_aged_65(request):

    df = json_to_dataframe("demo_r_pjangrp3", "nuts3_1")

    df = df[
        (df['sex']== 'T') &
        (~df['age'].isin([ 'TOTAL', 'Y_LT5', 'Y5-9', 'Y10-14',
            'Y15-19','Y20-24','Y25-29',
            'Y30-34','Y35-39','Y40-44',
            'Y45-49','Y50-54', 'Y55-59', 'Y60-64', 'UNK'])
        )
    ]
    max_year = df['time'].max()
    df = df[df['time'] == max_year]
    
    geo_name = {
        "FI1B1":"Helsinki",
        "PT170":"Lisbon",
        "FR101":"Paris",
        "DEA23":"Cologne",
        "SK031":"Zilina"
    }
    df['geo'] = df['geo'].replace(geo_name)
    
    color_mapping = {
        "Cologne": "#6272A4",
        "Helsinki": "#8BE9FD",
        "Zilina": "#FFB86C",
        "Lisbon": "#FF79C6",
        "Paris": "#BD93F9"
    }
    
    df = df[["values", "geo"]]
    
    df = df.groupby('geo')['values'].sum().reset_index()
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
    
    option = donut_chart("Population aged 65 years and older (%)", 'Year: ' + str(max_year), data)
    
    return Response(option)


@api_view(["GET"])
def bar_chart_demo_pop_density(request):

    df = json_to_dataframe("demo_r_d3dens", "nuts3_1")
    
    max_year = df['time'].max()
    df = df[df['time'] == max_year]
    
    geo_name = {
        "FI1B1":"Helsinki",
        "PT170":"Lisbon",
        "FR101":"Paris",
        "DEA23":"Cologne",
        "SK031":"Zilina"
    }
    df['geo'] = df['geo'].replace(geo_name)
    
    color_mapping = {
        "Cologne": "#6272A4",
        "Helsinki": "#8BE9FD",
        "Zilina": "#FFB86C",
        "Lisbon": "#FF79C6",
        "Paris": "#BD93F9"
    }
    
    df = df[["values", "geo"]]
    
    df = df.sort_values(by='values')

    geo_list = df['geo'].unique().tolist()
    values_list = df['values'].tolist()
    
    colors = [color_mapping.get(region) for region in geo_list]
    
    option = basic_bar_chart("Population density", "Number of Residents per km² - " + str(max_year), geo_list, values_list, colors)
    
    return Response(option)


# Transportation access

@api_view(["GET"])
def donut_chart_transportation_access(request):
    
    dataset_code = "tran_r_vehst"
    df = json_to_dataframe(dataset_code, 'nuts2')

    df = df[(df['vehicle'] == 'TOT_X_TM') & (df['unit'] == 'NR')]

    max_year = df['time'].max()
    df = df[df['time'] == max_year]
    
    df = df[["values", 'geo']]

    geo_name = {
        "DEA2": "Köln",
        "FI1B": "Helsinki-U.",
        "SK03": "S. Slovensko",
        "PT17": "A. M. Lisboa",
        "FR10": "Ile de France"
    }
    df['geo'] = df['geo'].replace(geo_name)
    
    color_mapping = {
        "Köln": "#6272A4",
        "Helsinki-U.": "#8BE9FD",
        "S. Slovensko": "#FFB86C",
        "A. M. Lisboa": "#FF79C6",
        "Ile de France": "#BD93F9"
    }
    
    df = df.groupby('geo')['values'].sum().reset_index()
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
    
    option = donut_chart("Stock of Vehicles (%)", 'Year: ' + str(max_year), data)
    
    return Response(option)


# ----------------------- Economic Resilience -----------------------

@api_view(["GET"])
def line_chart_economic_resilience(request):
    
    kpi = request.GET.get("dataset_code")
    df = json_to_dataframe(kpi, "nuts2")
        
    if kpi in ["hlth_rs_physreg", "tgs00006"]:
        if kpi == "hlth_rs_physreg":
            df = df[(df['unit'] == 'P_HTHAB')]
            df = df[['values', 'geo', 'time']]
            kpi = "Number of Physicians (per 100,000 inhabitants)"
        else:
            df = df[['values', 'geo', 'time']]
            kpi = "Regional gross domestic product"

    geo_name = {
        "DEA2": "Köln",
        "FI1B": "Helsinki-U.",
        "SK03": "S. Slovensko",
        "PT17": "A. M. de Lisboa",
        "FR10": "Ile de France"
    }
    df['geo'] = df['geo'].replace(geo_name)
    color_mapping = {
        "Köln": "#6272A4",
        "Helsinki-U.": "#8BE9FD",
        "S. Slovensko": "#FFB86C",
        "A. M. de Lisboa": "#FF79C6",
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
    
    option = line_chart(kpi, "", geo_list, year_list, result)
    return Response(option)


@api_view(["GET"])
def bar_chart_economic_resilience(request):

    kpi = request.GET.get("dataset_code")
    df = json_to_dataframe(kpi, "nuts2")
        
    if kpi in ["hlth_rs_physreg", "tgs00006"]:
        if kpi == "hlth_rs_physreg":
            df = df[(df['unit'] == 'P_HTHAB')]
            kpi = "Number of Physicians (per 100,000 inhabitants)"
        else:
            kpi = "Regional gross domestic product"

    geo_name = {
        "DEA2": "Köln",
        "FI1B": "Helsinki-U.",
        "SK03": "S. Slovensko",
        "PT17": "A. M. de Lisboa",
        "FR10": "Ile de France"
    }
    df['geo'] = df['geo'].replace(geo_name)
    
    color_mapping = {
        "Köln": "#6272A4",
        "Helsinki-U.": "#8BE9FD",
        "S. Slovensko": "#FFB86C",
        "A. M. de Lisboa": "#FF79C6",
        "Ile de France": "#BD93F9"
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


# ----------------------- Infrastructure Resilience -----------------------


@api_view(["GET"])
def line_chart_infrastructure_resilience(request):
    
    df = json_to_dataframe("tgs00064", "nuts2")
    df = df[['values', 'geo', 'time']]

    geo_name = {
        "DEA2": "Köln",
        "FI1B": "Helsinki-U.",
        "SK03": "S. Slovensko",
        "PT17": "A. M. de Lisboa",
        "FR10": "Ile de France"
    }
    df['geo'] = df['geo'].replace(geo_name)
    
    color_mapping = {
        "Köln": "#6272A4",
        "Helsinki-U.": "#8BE9FD",
        "S. Slovensko": "#FFB86C",
        "A. M. de Lisboa": "#FF79C6",
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
    
    option = line_chart("Number of hospital beds", "Per 100,000 inhabitants", geo_list, year_list, result)
    return Response(option)



@api_view(["GET"])
def bar_chart_infrastructure_resilience(request):

    df = json_to_dataframe("tgs00064", "nuts2")

    geo_name = {
        "DEA2": "Köln",
        "FI1B": "Helsinki-U.",
        "SK03": "S. Slovensko",
        "PT17": "A. M. de Lisboa",
        "FR10": "Ile de France"
    }
    df['geo'] = df['geo'].replace(geo_name)
    
    color_mapping = {
        "Köln": "#6272A4",
        "Helsinki-U.": "#8BE9FD",
        "S. Slovensko": "#FFB86C",
        "A. M. de Lisboa": "#FF79C6",
        "Ile de France": "#BD93F9"
    }
    
    max_year = df['time'].max()
    df = df[df['time'] == max_year]
    
    df = df[["values", "geo"]]
    
    df['geo'] = df['geo'].replace(geo_name)
    
    df = df.sort_values(by='values')
    
    geo_list = df['geo'].unique().tolist()
    values_list = df['values'].tolist()
    
    colors = [color_mapping.get(region) for region in geo_list]
    
    option = basic_bar_chart("Number of hospital beds", f"Per 100,000 inhabitant - {max_year}", geo_list, values_list, colors)
    
    return Response(option)


# ----------------------- Hazard Resilience -----------------------





# ----------------------- Institutional Resilience -----------------------

@api_view(["GET"])
def line_chart_institutional_resilience(request):
    
    df = json_to_dataframe('tin00129', 'nat')
    df = df[df['ind_type'] == "IND_TOTAL"]

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
    
    option = line_chart(
        "Individuals using the internet for taking part in online consultations or voting", 
        "Percentage of individuals (%)", 
        geo_list, 
        year_list, 
        result)
    
    return Response(option)


@api_view(["GET"])
def bar_chart_institutional_resilience(request):
    
    df = json_to_dataframe('tin00129', 'nat')
    df = df[df['ind_type'] == "IND_TOTAL"]
    
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
    
    option = basic_bar_chart(
        "Individuals using the internet for taking part in online consultations or voting", 
        f"Percentage of individuals (%) - {max_year}", 
        geo_list, 
        values_list, 
        colors)
    
    return Response(option)