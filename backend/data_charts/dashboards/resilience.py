from rest_framework.decorators import api_view
from rest_framework.response import Response
from data_charts.scripts.utils import *
from data_charts.scripts.charts import *
import plotly.express as px
import plotly.io as pio

# ----------------------- Social Resilience -----------------------

@api_view(["GET"])
def line_chart_social_resilience(request):
    
    kpi = request.GET.get("dataset_code")
    
    if kpi in ["tgs00109", "tran_r_vehst"]:
        
        df = json_to_dataframe(kpi, 'nuts2')
        
        geo_name = {
        "DEA2": "Köln",
        "FI1B": "Helsinki-U.",
        "SK03": "S. Slovensko",
        "PT17": "A.M. de Lisboa",
        "FR10": "Ile de France"
        }
        if kpi == "tgs00109":
            df = df[(df['sex'] == 'T')]
            kpi = "Population Aged 25-64 with Tertiary Education (%)"
        else:
            df = df[(df['vehicle'] == 'TOT_X_TM') & (df['unit'] == 'NR')]
            kpi = "Number of Vehicles"
    
    if kpi in ["demo_r_pjangrp3", "demo_r_pjangrp3_aged", "demo_r_d3dens"]:
        geo_name = {
            "FI1B1":"Helsinki",
            "PT170":"Lisboa",
            "FR101":"Paris",
            "DEA23":"Köln",
            "SK031":"Zilina"
        }
        if kpi == "demo_r_pjangrp3":
            df = json_to_dataframe('demo_r_pjangrp3', 'nuts3_1')
            df = df[
                (df['sex']== 'T') &
                (df['age'].isin([
                    'Y15-19','Y20-24','Y25-29',
                    'Y30-34','Y35-39','Y40-44',
                    'Y45-49','Y50-54', 'Y55-59', 'Y60-64'])
                )
            ]
            kpi = "Population in productive age (%)"
        elif kpi == "demo_r_pjangrp3_aged":
            df = json_to_dataframe('demo_r_pjangrp3', 'nuts3_1')
            df = df[
                (df['sex']== 'T') &
                (~df['age'].isin([ 'TOTAL', 'Y_LT5', 'Y5-9', 'Y10-14',
                    'Y15-19','Y20-24','Y25-29',
                    'Y30-34','Y35-39','Y40-44',
                    'Y45-49','Y50-54', 'Y55-59', 'Y60-64', 'UNK'])
                )
            ]
            kpi = "Population aged 65 years and older (%)"
        else:
            df = json_to_dataframe('demo_r_d3dens', 'nuts3_1')
            kpi = "Number of Residents per km²"

        
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
        "PT17": "A.M. de Lisboa",
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
        "PT170":"Lisboa",
        "FR101":"Paris",
        "DEA23":"Köln",
        "SK031":"Zilina"
    }
    df['geo'] = df['geo'].replace(geo_name)
    
    df = df[["values", "geo"]]
    
    df = df.groupby('geo')['values'].sum().reset_index()
    total = df['values'].sum()
    df['normalized_values'] = df['values'] / total * 100
    df['normalized_values'] = df['normalized_values'].round(2)
    
    colors = ['#50FA7B', '#6272A4', '#FF79C6', '#BD93F9', '#FFB86C']

    result = [
        {'value': row['normalized_values'], 'name': row['geo']}
        for _, row in df.iterrows()
    ]
    
    option = donut_chart("Population in productive age (%)", 'Year: ' + str(max_year), result, colors)
    
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
        "PT170":"Lisboa",
        "FR101":"Paris",
        "DEA23":"Köln",
        "SK031":"Zilina"
    }
    df['geo'] = df['geo'].replace(geo_name)
    
    df = df[["values", "geo"]]
    
    df = df.groupby('geo')['values'].sum().reset_index()
    total = df['values'].sum()
    df['normalized_values'] = df['values'] / total * 100
    df['normalized_values'] = df['normalized_values'].round(2)
    
    colors = ['#50FA7B', '#6272A4', '#FF79C6', '#BD93F9', '#FFB86C']

    result = [
        {'value': row['normalized_values'], 'name': row['geo']}
        for _, row in df.iterrows()
    ]
    
    option = donut_chart("Population aged 65 years and older (%)", 'Year: ' + str(max_year), result, colors)
    
    return Response(option)


@api_view(["GET"])
def bar_chart_demo_pop_density(request):

    df = json_to_dataframe("demo_r_d3dens", "nuts3_1")
    
    max_year = df['time'].max()
    df = df[df['time'] == max_year]
    
    geo_name = {
        "FI1B1":"Helsinki",
        "PT170":"Lisboa",
        "FR101":"Paris",
        "DEA23":"Köln",
        "SK031":"Zilina"
    }
    df['geo'] = df['geo'].replace(geo_name)
    
    df = df[["values", "geo"]]
    
    df = df.sort_values(by='values')

    geo_list = df['geo'].unique().tolist()
    values_list = df['values'].tolist()
    
    option = basic_bar_chart("Number of Residents per km²", "Year: " + str(max_year), geo_list, values_list)
    
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
        "PT17": "A.M. Lisboa",
        "FR10": "Ile de France"
    }
    df['geo'] = df['geo'].replace(geo_name)
    
    df = df.groupby('geo')['values'].sum().reset_index()
    total = df['values'].sum()
    df['normalized_values'] = df['values'] / total * 100
    df['normalized_values'] = df['normalized_values'].round(2)
    
    colors = ['#50FA7B', '#6272A4', '#FF79C6', '#BD93F9', '#FFB86C']

    result = [
        {'value': row['normalized_values'], 'name': row['geo']}
        for _, row in df.iterrows()
    ]
    
    option = donut_chart("Stock of Vehicles (%)", 'Year: ' + str(max_year), result, colors)
    
    return Response(option)


@api_view(["GET"])
def grouped_bar_chart_transportation_access(request):
    
    dataset_code = "tran_r_vehst"
    df = json_to_dataframe(dataset_code, 'nuts2')

    df = df[(df['vehicle'].isin(['CAR', 'MOTO', 'BUS_TOT'])) & (df['unit'] == 'NR')]

    max_year = df['time'].max()
    df = df[df['time'] == max_year]
    
    df = df[["values", 'geo', 'vehicle']]

    geo_name = {
        "DEA2": "Köln",
        "FI1B": "Helsinki-U.",
        "SK03": "S. Slovensko",
        "PT17": "A.M. Lisboa",
        "FR10": "Ile de France"
    }
    df['geo'] = df['geo'].replace(geo_name)
    
    df['vehicle'] = df['vehicle'].replace({'CAR': 'Passenger cars', 'MOTO': 'Motorcycles', 'BUS_TOT': 'Buses'})
    
    dimensions = ['geo'] + ['Passenger cars'] + ['Motorcycles'] + ['Buses']
    pivot_df = df.pivot(index='geo', columns='vehicle', values='values').fillna(0).reset_index()
    source = pivot_df.to_dict(orient='records')
    
    option = grouped_bar_chart_3("Number of Vehicles by Type", "Year: " + str(max_year), dimensions, source)
    
    return Response(option)


# ----------------------- Economic Resilience -----------------------

























# ----------------------- Economic & Infrastructure Resilience -----------------------

@api_view(["GET"])
def line_chart_by_resilience_kpis(request):
    dataset_code = request.GET.get("dataset_code")
    df = json_to_dataframe(dataset_code, "nuts2")
    return d3_line_chart_by_resilience_kpis(df, dataset_code)


def d3_line_chart_by_resilience_kpis(df, kpi):
        
    if kpi in ["hlth_rs_physreg", "tgs00006", "tgs00064"]:
        if kpi == "hlth_rs_physreg":
            df = df[(df['unit'] == 'NR')]
            df = df[['values', 'geo', 'time']]
            kpi = "Number of Physicians"
        elif kpi == "tgs00006":
            df = df[['values', 'geo', 'time']]
            kpi = "Regional gross domestic product"
        else:
            df = df[['values', 'geo', 'time']]
            kpi = "Available beds in hospitals by NUTS 2 regions"

    geo_name = {
        "DEA2": "Köln",
        "FI1B": "Helsinki-U.",
        "SK03": "S. Slovensko",
        "PT17": "A. M. de Lisboa",
        "FR10": "Ile de France"
    }
    df['geo'] = df['geo'].replace(geo_name)

    common_years = df.groupby('geo')['time'].apply(set).reset_index()
    common_years = set.intersection(*common_years['time'])
    df = df[df['time'].isin(common_years)]

    df_grouped = df.groupby('geo').agg(list).reset_index()

    series = []
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
        series.append(data_dict)
                            
    geo_list = df['geo'].unique().tolist()    
    year_list = df['time'].unique().tolist()
    
    option = line_chart(kpi, "", geo_list, year_list, series)
    return Response(option)


@api_view(["GET"])
def grouped_bar_chart_physi_vs_hosp_beds(request):

    df_1 = json_to_dataframe('hlth_rs_physreg', 'nuts2')
    df_1 = df_1[(df_1['time'] == 2022) & (df_1['unit'] == 'P_HTHAB')]
    df_1 = df_1[['values', 'geo', 'indicator_label']]
    
    df_2 = json_to_dataframe('tgs00064', 'nuts2')
    df_2 = df_2[(df_2['time'] == 2022)]
    df_2 = df_2[['values', 'geo', 'indicator_label']]
    
    df = pd.merge(df_1, df_2, on='geo', suffixes=('_df1', '_df2'))
    df = pd.melt(
        df,
        id_vars=['geo'],
        value_vars=['values_df1', 'values_df2'],
        var_name='indicator_label',
        value_name='values'
    )
    df['ind_label'] = df['indicator_label'].replace({
        'values_df1': 'Number of physicians',
        'values_df2': 'Available beds'
    })
    df = df.drop(columns=['indicator_label'])
    
    geo_name = {
        "DEA2": "Köln",
        "FI1B": "Helsinki-U.",
        "SK03": "S. Slovensko",
        "PT17": "A. M. de Lisboa",
        "FR10": "Ile de France"
    }    
    df['geo'] = df['geo'].replace(geo_name)
    
    dimensions = ['geo'] + ['Number of physicians'] + ['Available beds']
    pivot_df = df.pivot(index='geo', columns='ind_label', values='values').reset_index()
    source = pivot_df.to_dict(orient='records')
    
    option = bar_chart("Number of physicians vs Available hospital beds: 2022", "(per 100 000 inhabitants)", dimensions, source)
    return Response(option)