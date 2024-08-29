import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from data_charts.scripts.utils import *
from data_charts.scripts.charts import *
import plotly.express as px
import plotly.io as pio


@api_view(["GET"])
def line_chart_inclusion_kpis(request):
    dataset_code = request.GET.get("dataset_code")
    
    if dataset_code in ["tessi190", "tepsr_sp200"]:
        df = json_to_dataframe(dataset_code, 'nat')
    if dataset_code in ["ilc_li41", "tepsr_lm220", "tgs00007", "educ_uoe_enra11", "ilc_lvhl21n", "edat_lfse_22"]:
        df = json_to_dataframe(dataset_code, 'nuts2')

    return d1_line_chart_by_inclusion_kpi(df, dataset_code)


def d1_line_chart_by_inclusion_kpi(df, kpi):
    
    if kpi in ["tessi190", "tepsr_sp200"]:
        geo_name = {
            "DE": "Germany",
            "FI": "Finland",
            "SK": "Slovakia",
            "PT": "Portugal",
            "FR": "France"
        }        
        if kpi == "tessi190":
            kpi = "Gini coefficient"
        else:
            df = df[(df['lev_limit'] == 'SM_SEV') & (df['sex'] == 'T')]
            kpi = "Disability employment gap"
        df = df[["values", "geo", "time"]]
    
    if kpi in ["ilc_li41", "tepsr_lm220", "tgs00007", "educ_uoe_enra11", "ilc_lvhl21n", "edat_lfse_22"]:
        geo_name = {
            "DEA2": "Köln",
            "FI1B": "Helsinki-U.",
            "SK03": "S. Slovensko",
            "PT17": "A. M. Lisboa",
            "FR10": "Ile France"
        }
        if kpi == "ilc_li41":
            kpi = "People at risk of poverty rate"
        elif kpi == "tepsr_lm220":
            kpi = "Gender employment gap"
        elif kpi == "tgs00007":
            df = df[(df['sex'] == 'T')]
            kpi = "People employed in productive age"
        elif kpi == "educ_uoe_enra11":
            df = df[(df['sex'] == 'T') & (df['isced11'] == 'ED6')]
            kpi = "Equitable Bachelor's Enrolment"
        elif kpi == "ilc_lvhl21n":
            kpi = "Slum Household"
        else:
            df = df[(df['sex'] == 'T') & (df['age'] == 'Y18-29')]
            kpi = "Youth Unemployment "
        df = df[["values", "geo", "time"]]
    
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


@api_view(["GET"])
def cloropleth_map_inclusion(request):
    
    dataset_code = request.GET.get("dataset_code")
    
    if dataset_code in ["tessi190", "tepsr_sp200"]:
        df = json_to_dataframe(dataset_code, 'nat')
    if dataset_code in ["ilc_li41", "tepsr_lm220", "tgs00007", "educ_uoe_enra11", "ilc_lvhl21n", "edat_lfse_22"]:
        df = json_to_dataframe(dataset_code, 'nuts2')
    
    fig = d1_cloropleth_map_inclusion(df, dataset_code)
    fig_json = pio.to_json(fig)
    
    return Response(fig_json, content_type="application/json")


def d1_cloropleth_map_inclusion(df, kpi):
    if kpi in ["tessi190", "tepsr_sp200"]:
        geo_code = {
            'PT': 'PRT',
            'DE': 'DEU',
            'FR': 'FRA',
            'FI': 'FIN',
            'SK': 'SVK'
        }
        if kpi == "tessi190":
            kpi = "Gini coefficient"
        else:
            df = df[(df['lev_limit'] == 'SM_SEV') & (df['sex'] == 'T')]
            kpi = "Disability employment gap"
        
        df = df[["values", "geo", "time"]]
        
        df['geo'] = df['geo'].replace(geo_code)
    
        geojson_url = 'https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/world-countries.json'
        response = requests.get(geojson_url)
        geojson = response.json()
        
        fig = px.choropleth_mapbox(
            df, 
            geojson=geojson, 
            locations='geo', 
            color='values',
            color_continuous_scale="YlGnBu",
            mapbox_style="carto-positron",
            zoom=2.2, 
            center = {"lat": 54.5260, "lon": 15.2551},
            opacity=0.5,
            labels={'values': kpi},
            animation_frame="time",
            )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        
    
    if kpi in ["ilc_li41", "tepsr_lm220", "tgs00007", "educ_uoe_enra11", "ilc_lvhl21n", "edat_lfse_22"]:
        
        geo_name = {
            'PT17': 'Área Metropolitana de Lisboa',
            'DEA2': 'Köln',
            'FR10': 'Ile de France',
            'FI1B': 'Helsinki-Uusimaa',
            'SK03': 'Stredné Slovensko'
        }
        df['geo_name'] = df['geo'].replace(geo_name)

        geo_code = {
            'PT17': 'PRT',
            'DEA2': 'DEU',
            'FR10': 'FRA',
            'FI1B': 'FIN',
            'SK03': 'SVK'
        }
        df['geo'] = df['geo'].replace(geo_code)
        
        if kpi == "ilc_li41":
            kpi = "People at risk of poverty rate"
        elif kpi == "tepsr_lm220":
            kpi = "Gender employment gap"
        elif kpi == "tgs00007":
            df = df[(df['sex'] == 'T')]
            kpi = "People employed in productive age"
        elif kpi == "educ_uoe_enra11":
            df = df[(df['sex'] == 'T') & (df['isced11'] == 'ED6')]
            kpi = "Equitable Bachelor's Enrolment"
        elif kpi == "ilc_lvhl21n":
            kpi = "Slum Household"
        else:
            df = df[(df['sex'] == 'T') & (df['age'] == 'Y18-29')]
            kpi = "Youth Unemployment"
        
        df = df[['geo', 'time', 'geo_name', 'values']]
        
        fig = px.scatter_geo(
            df, 
            locations="geo", 
            color="geo_name",
            color_continuous_scale="YlGnBu",
            hover_name="geo_name", 
            size="values",
            animation_frame="time",
            projection="natural earth", 
            scope="europe",
            labels={'values': kpi, 'geo_name': 'Nuts2 region', 'time': 'year'}
        )

    return fig

@api_view(["GET"])
def bar_chart_inclusion_kpis_ranking(request):
    dataset_code = request.GET.get("dataset_code")
    
    if dataset_code in ["tessi190", "tepsr_sp200", "tespm010"]:
        df = json_to_dataframe(dataset_code, 'nat')
    if dataset_code in ["ilc_li41", "tepsr_lm220"]:
        df = json_to_dataframe(dataset_code, 'nuts2')
        
    return d1_bar_chart_cities_ranking_by_kpi(df, dataset_code)


def d1_bar_chart_cities_ranking_by_kpi(df, kpi):
    
    if kpi in ["tessi190", "tepsr_sp200", "tespm010"]:
        geo_name = {
            "DE": "Germany",
            "FI": "Finland",
            "SK": "Slovakia",
            "PT": "Portugal",
            "FR": "France"
        }  
        if kpi == "tessi190":
            df = df[(df['time'] == 2023)]
            df = df[["values", "geo"]]
            kpi = "Gini coefficient of equivalized disposable income"
        elif kpi == "tepsr_sp200":
            df = df[(df['lev_limit'] == 'SM_SEV') & (df['sex'] == 'T') & (df['time'] == 2023)]
            df = df[["values", "geo"]]
            kpi = "Disability employment gap"
        else:
            df = df[(df['time'] == 2023)]
            df = df[["values", "geo"]]
            kpi = "At risk of poverty rate"
    
    if kpi in ["ilc_li41", "tepsr_lm220"]:
        geo_name = {
            "DEA2": "Köln",
            "FI1B": "Helsinki-U.",
            "SK03": "S. Slovensko",
            "PT17": "A. M. Lisboa",
            "FR10": "Ile France"
        }
        df = df[(df['time'] == 2023)]
        df = df[["values", "geo"]]
        if kpi == "ilc_li41":
            kpi = "At risk of poverty rate by NUTS 2 regions"
        else:
            kpi = "Gender employment gap by NUTS 2 regions"
    
    df['geo'] = df['geo'].replace(geo_name)
    
    df = df.sort_values(by='values')

    geo_list = df['geo'].unique().tolist()
    values_list = df['values'].tolist()
    
    option = basic_bar_chart(kpi, "Year: 2023", geo_list, values_list)
    
    return Response(option)


@api_view(["GET"])
def scatter_plot_gini_vs_poverty(request):
    
    gini_df = json_to_dataframe('tessi190', 'nat')
    poverty_df = json_to_dataframe('tespm010', 'nat')
    
    gini_df = gini_df[["values", "geo", "time"]]
    
    poverty_df = poverty_df[(poverty_df['time'] >= 2014)]
    poverty_df = poverty_df[["values", "geo", "time"]]
    
    df = pd.merge(gini_df, poverty_df, on=['geo', 'time'], suffixes=('_gini', '_poverty'))
    
    geo_name = {
        "DE": "Germany",
        "FI": "Finland",
        "SK": "Slovakia",
        "PT": "Portugal",
        "FR": "France"
    }
    df['geo'] = df['geo'].replace(geo_name)
    
    return Response(df)


@api_view(["GET"])
def grouped_bar_chart_disability_employ_gap_by_sex(request):
    
    lev_limit = request.GET.get("lev_limit")
    
    df = json_to_dataframe('tepsr_sp200', 'nat')
    
    df = df[(df["sex"] != "T") & (df["lev_limit"] == lev_limit) & (df["time"] == 2023)]
    df = df[["values", "geo", "sex"]]
    
    geo_name = {
        "DE": "Germany",
        "FI": "Finland",
        "SK": "Slovakia",
        "PT": "Portugal",
        "FR": "France"
    }
    df['geo'] = df['geo'].replace(geo_name)

    df['sex'] = df['sex'].replace({'M': 'Male', 'F': 'Female'})
    
    dimensions = ['geo'] + ['Male'] + ['Female']
    pivot_df = df.pivot(index='geo', columns='sex', values='values').reset_index()
    source = pivot_df.to_dict(orient='records')
    
    option = bar_chart("Disability employment gap by sex", "Year: 2023", dimensions, source)
    return Response(option)