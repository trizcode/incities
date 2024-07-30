def line_chart(kpi, legend_list, xaxis_list, series):
    option = {
        "title": {"text": kpi},
        "tooltip": {"trigger": 'axis'},
        "legend": {"data": legend_list, 'bottom': '1%'},
        "grid": {'top': '10%', 'right': '1%', 'bottom': '8%', 'left': '1%', 'containLabel': 'true'},
        "xAxis": {"type": 'category', "data": xaxis_list},
        "yAxis": {"type": 'value'},
        "series": series
    }
    return option

def heatmap(xaxis_list, yaxis_list, min_value, max_value, series_data):
    option = {
    "tooltip": {
        "position": 'top'
    },
    "grid": {
        "height": '65%',
        "top": '12%',
        'left': '15%',
        'right': '2%'
    },
    "xAxis": {
        "type": 'category',
        "data": xaxis_list,
        "splitArea": {
        "show": "true"
        }
    },
    "yAxis": {
        "type": 'category',
        "data": yaxis_list,
        "splitArea": {
        "show": "true"
        }
    },
    "visualMap": {
        "min": min_value,
        "max": max_value,
        "calculable": "true",
        "orient": 'horizontal',
        "left": 'center',
        "bottom": '1%'
    },
    "series": [{
        'name': 'Risk',
        'type': 'heatmap',
        'data': series_data,
    }]
    }
    return option


def bar_chart(title, dimensions, source):
    
    option = {
      "title": {"text": title},
      "legend": {'bottom': '1%'},
      "grid": {'top': '10%', 'right': '1%', 'bottom': '8%', 'left': '1%', 'containLabel': 'true'},
      "tooltip": {},
      "dataset": {
        "dimensions": dimensions,
        "source": source
      },
      "xAxis": { "type": 'category' },
      "yAxis": {},
       'series': [
        {
            'type': 'bar',
            'itemStyle': {
                'color': '#6272A4'
            }
        },{
            'type': 'bar',
            'itemStyle': {
                'color': '#FF79C6'}}]}
    return option


def donut_chart(title, subtitle, data, color):
    
    option = { 
        "title": {"text": title, "subtext": subtitle},
        "tooltip": {
        "trigger": 'item'
      },
      "legend": {
        "bottom": '1%',
        "left": 'center',
      },
      "series": [
        {
          "name": 'Category',
          "type": 'pie',
          "radius": ['40%', '70%'],
          "padAngle": 1,
          "itemStyle": {
          "borderRadius": 10
          },
          "emphasis": {
            "label": {
              "show": "true",
              "fontSize": 30,
              "fontWeight": 'bold'
            }
          },
          "data": data
        }
      ],
    "color": color
    }
    return option