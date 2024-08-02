def line_chart(title, subtitle="", legend_list=[], xaxis_list=[], series=[]):
    option = {
        "title": {"text": title, "subtext": subtitle},
        "tooltip": {"trigger": 'axis'},
        "legend": {"data": legend_list, 'bottom': '1%'},
        "grid": {'top': '15%', 'right': '5%', 'bottom': '8%', 'left': '1%', 'containLabel': 'true'},
        "xAxis": {"type": 'category', "data": xaxis_list},
        "yAxis": {"type": 'value'},
        "series": series
    }
    return option

def heatmap(kpi, xaxis_list, yaxis_list, min_value, max_value, series_data):
    option = { "title": {"text": kpi},
    "tooltip": {
        "position": 'top'
    },
    "grid": {
        "height": '65%',
        "top": '15%',
        'left': '10%',
        'right': '15%'
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
        'type': 'heatmap',
        'data': series_data,
    }]
    }
    return option


def bar_chart(title, dimensions, source):
    
    option = {
      "title": {"text": title},
      "legend": {'bottom': '1%'},
      "grid": {'top': '15%', 'right': '1%', 'bottom': '8%', 'left': '1%', 'containLabel': 'true'},
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
  
  
def horizontal_bar_chart(title, subtitle, yaxis_data, series_data):
    
  option = { "title": {"text": title, 
                        "subtext": subtitle},
    "xAxis": {
      "type": 'value'
    },
    "yAxis": {
      "type": 'category',
      "data": yaxis_data
    },
    "grid": {
      "left": '2%',
      "right": '5%',
      "bottom": '1%',
      "containLabel": "true"
    },
    "tooltip": {
      "trigger": 'axis',
      "axisPointer": {
        "type": 'shadow'
      }
    },
    "series": [
      {
        "data": series_data,
        "type": 'bar',
        "itemStyle": {
          "color": '#BD93F9'
        }
      }
    ]
  }
  return option