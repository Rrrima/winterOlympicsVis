import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

def aggbycountry(x):
    names = {
        'Gold': x[x['Medal']=='Gold']['Medal'].count(),
        'Silver': x[x['Medal']=='Silver']['Medal'].count(),
        'Bronze': x[x['Medal']=='Bronze']['Medal'].count(),
        }
    return pd.Series(names)

def get_data_by_year(y):
    wd_byyear = winterdata[winterdata['Year']==y]
    gdp_byyear = gdpdata[gdpdata['Year']==y]
    gdps = gdp_byyear[['Code','gdp']]
    medals = wd_byyear.groupby('Country').apply(aggbycountry)
    medals['ctry'] = medals.index
    pops = popdata[['ctry','code',str(y)]]
    merge1 = pd.merge(medals,pops,how='left',left_on='ctry',right_on='code')
    merge2 = pd.merge(merge1,gdps,how='left',left_on='ctry_x',right_on='Code')
    merge3 = merge2.rename(columns={'ctry_x':'abbr','ctry_y':'country',str(y):'population','Code':'c'})
    data = merge3[['country','abbr','Gold','Silver','Bronze','population','gdp']]
#     data['population_log'] = np.log10(data['population'])
    data = data.dropna()
    return data

def get_score(data,fsl,fbr):
    data['pop_log'] = np.log2(data['population'])
    data['gdp_log'] = np.log2(data['gdp'])
    data['Gold'] = fsl * data['Silver'] + fbr * data['Bronze'] + data['Gold']
    return data

winterdata = pd.read_csv('data-processing/data/winter.csv')
popdata = pd.read_csv('data-processing/data/population.csv')
gdpdata = pd.read_csv('data-processing/data/gdp.csv')
year = 2014
data_year = get_data_by_year(year)
data_year = get_score(data_year,0.6,0.3)
countries = list(data_year['country'])
countries.extend(['Spain','Luxembourg','New Zealand','Estonia','Uzbekistan','Belgium'])
colors =  list(px.colors.qualitative.Set3) + list(px.colors.qualitative.Set2) + list(px.colors.qualitative.Set1)



def get_gdp(year,fsl,fbr):
    data_year = get_data_by_year(year)
    data_year = get_score(data_year,fsl,fbr)
    map_dict = {}
    for i in range(len(countries)):
        map_dict[countries[i]] = colors[i]
    data_colors = map(lambda x:map_dict[x],data_year['country'])
    data_colors = np.array(list(data_colors))
    fig = go.Figure(
        data=[go.Scatter(
                x=data_year['gdp'],
                y=data_year['Gold'],
                mode='markers',
                text=data_year['country'],
                marker=dict(
                    size=data_year['population']/1200000,
                    sizemode='area',
                    sizeref=2.*100/(40.**2),
                    sizemin=4,
                    color = data_colors,
                    opacity = 0.5
                )
            )]
    )
    fig.update_layout(width=800, height=700,template = 'plotly_white',yaxis=dict(
                range=[-20, 120]
            ), xaxis=dict(
                range=[-10*1000, 65*1000]
            ))
    data_sorted = data_year.sort_values(['Gold'],ascending=False)
    data_colors_sorted = map(lambda x:map_dict[x],data_sorted['country'])
    data_colors_sorted = np.array(list(data_colors_sorted))
    fig_bar = px.bar(data_sorted, x="Gold", y="country", color="country",color_discrete_sequence = data_colors_sorted,opacity=0.7)
    fig_bar.update_layout(width=800, height=700,template = 'plotly_white')

    return fig,fig_bar


def get_gdp_subplots(year,fsl,fbr):
    data_year = get_data_by_year(year)
    data_year = get_score(data_year,fsl,fbr)
    map_dict = {}
    for i in range(len(countries)):
        map_dict[countries[i]] = colors[i]
    data_colors = map(lambda x:map_dict[x],data_year['country'])
    data_colors = np.array(list(data_colors))
    bubble_plot = go.Scatter(
                x=data_year['gdp'],
                y=data_year['Gold'],
                mode='markers',
                name = '',
                text=data_year['country'],
                marker=dict(
                    size=data_year['population']/1000000,
                    sizemode='area',
                    sizeref=2.*100/(40.**2),
                    sizemin=4,
                    color = data_colors,
                    opacity = 0.5
                ),
                hovertemplate = 
                    "<b> %{text}</b><br>" +
                    " Score: %{y:.2f} <br>"  +
                    " Poluation: %{marker.size:.1fm} " +"m <br>"
            )
    data_sorted = data_year.sort_values(['Gold'])
    data_colors_sorted = map(lambda x:map_dict[x],data_sorted['country'])
    data_colors_sorted = np.array(list(data_colors_sorted))
    bar_plot = go.Bar(
            x=data_sorted['Gold'],
            y=data_sorted['country'],
            text=data_sorted['country'],
            orientation='h',
            name = '',
            marker = dict(
                 color = data_colors_sorted,
            ),
            opacity = 0.8
        )
    fig_all = make_subplots(rows=1, cols=2,column_widths=[0.4, 0.6])
    fig_all.add_trace(bar_plot,row=1, col=1)
    fig_all.add_trace(bubble_plot,row=1, col=2)
    fig_all.update_layout(template = 'plotly_white',showlegend=False,
            yaxis2=dict(range=[-20, 90],dtick=20,title_text = "Total Score"),
            xaxis2=dict(range=[-10*1000, 65*1000],title_text = "GDP per Capita"),
            xaxis1 = dict(dtick=5,title_text = "Total Score"),
            height=560,hovermode="x")
    return fig_all




