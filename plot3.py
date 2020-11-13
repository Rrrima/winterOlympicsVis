import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go

athdata = pd.read_csv('data-processing/athlete.csv')
countries = athdata['Country'].unique()
colors =  list(px.colors.qualitative.Set3) + list(px.colors.qualitative.Set2) + list(px.colors.qualitative.Set1)+ list(px.colors.qualitative.Set1) +  list(px.colors.qualitative.Set2)
map_dict = {}
for i in range(len(countries)):
    map_dict[countries[i]] = colors[i]

def get_athplot(fsl,fbr):
    athdata['Score'] = fsl * athdata['Silver'] + fbr * athdata['Bronze'] + athdata['Gold']
    athdata_colors = map(lambda x:map_dict[x],athdata['Country'])
    athdata_colors = np.array(list(athdata_colors))
    bubble = go.Scatter(
            x=athdata['Year'],
            y=athdata['Score'],
            mode='markers',
            text=athdata['Athlete'],
            customdata=np.transpose([athdata['Gold'], athdata['Silver'],athdata['Bronze'],athdata['Country']]),
            marker=dict(
                size=athdata['Score']**3*1.2,
                sizemode='area',
                sizemin=4,
                color = athdata_colors
                ),
            name = '',
            hovertemplate = 
            "<b> %{text}</b><br>" +
            " Country: %{customdata[3]} <br>" 
            " #Gold: %{customdata[0]}<br> "  + 
            " #Silver: %{customdata[1]}<br> "  + 
            " #Bronze: %{customdata[2]}"
            )

    grouped = athdata.groupby(['Country']).sum().reset_index()
    sorted_data = grouped.sort_values(['Score','Total','Gold'])
    data_colors = map(lambda x:map_dict[x],sorted_data['Country'])
    data_colors = np.array(list(data_colors))
    bar = go.Bar(
            x=sorted_data['Score'],
            y=sorted_data['Country'],
            orientation='h',
            marker = dict(
                 color = data_colors,
            ),
            opacity = 0.8,
            name = ''
            )
    fig_all = make_subplots(rows=1, cols=2,column_widths=[0.7, 0.3])
    fig_all.add_trace(bubble,row=1, col=1)
    fig_all.add_trace(bar,row=1, col=2)
    fig_all.update_layout(template = 'plotly_white',showlegend=False,height=600,
                            xaxis1 = dict(dtick=10,title_text = "Year"),
                            yaxis1 = dict(title_text="Score"),
                            xaxis2 = dict(dtick=10,title_text = "Total Score"),
                            )
    return fig_all




