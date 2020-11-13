import random
from streamlit_echarts import JsCode
import pandas as pd
import plotly.express as px

winterdata = pd.read_csv('data-processing/data/winter.csv')
def aggmulti(x):
    names = {
        'Gold': x[x['Medal']=='Gold']['Medal'].count(),
        'Silver': x[x['Medal']=='Silver']['Medal'].count(),
        'Bronze': x[x['Medal']=='Bronze']['Medal'].count(),
        'Total': x['Medal'].count()
        }
    return pd.Series(names)
agg_data = winterdata.groupby(['Country','Year','Discipline']).apply(aggmulti)
agg_data = agg_data.reset_index()
dislist = list(winterdata.groupby(['Sport','Discipline']).sum().reset_index()['Discipline'].unique())
yearlist2 = ["",1972, 1976, 1980, 1984, 1988, 1992, 1994, 1998,
       2002, 2006, 2010, 2014]
yearlist_str = [str(y) for y in yearlist2]

sum_data = winterdata.groupby(['Country','Discipline']).apply(aggmulti)
sum_data = sum_data.reset_index()
cty_data = winterdata.groupby(['Country']).apply(aggmulti)

def get_domain_plot(c):
    nordata = agg_data[agg_data['Country']==c]
    data = []
    for i in range(len(dislist)):
        for j in range(len(yearlist2)):
            temp = nordata[(nordata['Year']==yearlist2[j]) & (nordata['Discipline']== dislist[i])]['Total'].to_list()
            if not temp:
                temp = 0
            else:
                temp = int(temp[0])
            data.append([j,i,temp])
    options = get_option(data)
    return options

def get_option(data):
    option = {
        "polar": {},
        "tooltip":{
            "trigger":"item",
            "axisPointer": {
                "type": "cross"
            },
        },
        "angleAxis": {
            "type": 'category',
            "data": dislist,
            "boundaryGap": False,
            "startAngle":25,
            "splitLine": {
                "show": True,
                "lineStyle": {
                    "color": '#999',
                    "type": 'dashed'
                }
            },
            "axisLine": {
                "show": False
            },
        },
        "radiusAxis":{
            "type": 'category',
            "data": yearlist_str,
            "axisLine": {
                "show": False
            },
            "axisLabel": {
                "rotate": 45
            },
            "splitNumber":10,
            "axisTick": {
                "interval":5
            }
        },
        "series": [{
            "name": 'Medals',
            "type": 'scatter',
            "coordinateSystem": 'polar',
            "symbolSize":JsCode("function (val) {return val[2] * 2;}").js_code,
            "data": data,
        }]
    }
    return option

def get_sample():
    option = {
            "legend": {},
            "tooltip": {},
            "title":[{
                "text": 'USA',
                "textAlign": 'center',
                "left":'20%',
                "top":'42%'

            },
            {
                "text": 'CAN',
                "textAlign": 'center',
                "left":'50%',
                "top":'42%'
            },
            {
                "text": 'NOR',
                "textAlign": 'center',
                "left":'80%',
                "top":'42%'
            },
            {
                "text": 'URS',
                "textAlign": 'center',
                "left":'20%',
                "top":'88%'
            },
            {
                "text": 'FIN',
                "textAlign": 'center',
                "left":'50%',
                "top":'88%'
            },
            {
                "text": 'SWE',
                "textAlign": 'center',
                "left":'80%',
                "top":'88%'
            }
            ],
            "dataset": {
                "source": [
                    ['country',   'USA', 'CAN', 'NOR', 'URS', 'FIN', 'SWE'],
                    ['Biathlon',    0,     3,     62,    37,    16,   16],
                    ['Bobsleigh',   93,    22,     0,    8,     0,    0 ],
                    ['Curling',     5,     50,    15,    0,     5,    0 ],
                    ['Ice Hockey', 269,    351,   0,     168,   181,  218],
                    ['Luge',        9,      0,    0,      7,    0,    0],
                    ['Skating',    179,    159,   83,    104,   26,   20],
                    ['Skiing',      98,     40,   297,   116,   206,  146],
                ]
            },
            "series": [
                {
                "name":"USA",
                "type": 'pie',
                "radius": 50,
                "center": ['20%', '30%'],
                "encode": {
                    "itemName": 'country',
                    "value": 'USA'
                }
            }, {
                "name":"CAN",   
                "type": 'pie',
                "radius": 50,
                "center": ['50%', '30%'],
                "encode": {
                    "itemName": 'country',
                    "value": 'CAN'
                }
            }, {
                "name":"NOR",
                "type": 'pie',
                "radius": 50,
                "center": ['80%', '30%'],
                "encode": {
                    "itemName": 'country',
                    "value": 'NOR'
                }
            }, {
                "name":"URS",
                "type": 'pie',
                "radius": 50,
                "center": ['20%', '75%'],
                "encode": {
                    "itemName": 'country',
                    "value": 'URS'
                }
            }, {
                "name":"FIN",
                "type": 'pie',
                "radius": 50,
                "center": ['50%', '75%'],
                "encode": {
                    "itemName": 'country',
                    "value": 'FIN'
                }
            },{
                "name":"SWE",
                "type": 'pie',
                "radius": 50,
                "center": ['80%', '75%'],
                "encode": {
                    "itemName": 'country',
                    "value": 'SWE'
                }
            }],
             "color":['#ffbc7f','#c5c1dc', '#eed1e6','#ff9188' , '#b8e185','#8bb9d5','#a1dcd3'],
             # "color":px.colors.qualitative.Plotly
        };
    return option

def get_overall(top):
    head_data = cty_data.sort_values(['Total'],ascending=False).head(top)
    head_data = head_data.reset_index()
    cty_list = list(head_data['Country'].unique())
    data = sum_data[sum_data['Country'].isin(cty_list)]
    data = []
    for i in range(len(dislist)):
        temp_data = []
        for j in range(len(cty_list)):
            temp = sum_data[(sum_data['Country']==cty_list[j]) & (sum_data['Discipline']== dislist[i])]['Total'].to_list()
            if not temp:
                temp = 0
            else:
                temp = int(temp[0])
            temp_data.append(temp)
        data.append(temp_data)
    fig = px.imshow(data,
                labels=dict(x="Country", y="Discipline", color="#Medals"),
                x=cty_list,
                y=dislist,
                color_continuous_scale=px.colors.sequential.PuBu,
               )
    fig.update_xaxes(side="bottom")
    wide_data = sum_data.groupby(['Country']).sum()
    wide_data = wide_data.reset_index().sort_values(['Total'],ascending=False).head(top)
    fig_bar = px.bar(wide_data, x="Country", y=["Gold", "Silver", "Bronze"],
        color_discrete_sequence=['rgba(235,185,66,0.8)','rgba(112,110,100,0.6)','rgba(148,118,62,0.8)'],
        hover_data=["Country"])
    fig_bar.update_layout(width=600, height=460,template = 'plotly_white', yaxis = dict(title_text = "#Medals"),legend_title_text='')
    return fig,fig_bar,cty_list



