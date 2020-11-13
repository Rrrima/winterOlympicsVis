import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plot1 import get_gdp_subplots
from plot2 import get_domain_plot,get_overall,get_sample
from plot3 import get_athplot
from streamlit_echarts import st_echarts,st_pyecharts
import streamlit.components.v1 as components
from PIL import Image

titleim = Image.open('assets/title.png')
im1 = Image.open('assets/1.png')
im2 = Image.open('assets/2.png')
im3 = Image.open('assets/3.png')
im4 = Image.open('assets/4.png')
im5 = Image.open('assets/5.png')
im6 = Image.open('assets/6.png')
im7 = Image.open('assets/7.png')
im8 = Image.open('assets/8.png')
im9 = Image.open('assets/9.png')

st.image(titleim,use_column_width=True)

st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        max-width: {1000}px;
    }}
</style>
""",
        unsafe_allow_html=True,
    )




st.markdown("# Who's the best at what ?")
st.markdown("---")
# top = st.slider('Select year of interest:',min_value=10,max_value=30,value=20)
st.markdown("### An overview")
st.image(im5,use_column_width=True)
top = 25
htmap,bar,country_list = get_overall(top)
st.plotly_chart(bar, use_container_width=True)
st.image(im6,use_column_width=True)
st.plotly_chart(htmap, use_container_width=True)

st.markdown("### Country's medal in discipline over year")
st.image(im7,use_column_width=True)
country = st.selectbox(
    'Choose the country you want to explore:',
     country_list)
st.write("Performance by year of ", country)
options = get_domain_plot(country)
st_echarts(options=options,height="600px")
st.image(im4,use_column_width=True)

st.markdown("### Performance in each sports")
st.image(im8,use_column_width=True)
options_sample = get_sample()
st_echarts(options=options_sample,height="500px")

st.markdown("# The wealthier, the better?")
st.markdown("---")
st.image(im1,use_column_width=True)
gdp_years = [1992,1994,1998,2002,2006,2010,2014]
# the first part: gdp - rank
year = st.slider('',min_value=1994,max_value=2014,step=4)
st.sidebar.markdown("### Customize the score calculation methods here:")

fsl = st.sidebar.slider('',min_value=0,max_value=100,value=60)
st.sidebar.write("1 silver =", fsl/100,  "gold")

fbr = st.sidebar.slider('',min_value=0,max_value=100,value=30)
st.sidebar.write("1 Bronze =", fbr/100,  "gold")

st.sidebar.markdown("#### Score = ")
st.sidebar.write("  #gold + ", fsl/100, " #silver + ",fbr/100, " #bronze")
# fig,fig_bar = get_gdp(year)
# st.plotly_chart(fig, use_container_width=True)
# st.plotly_chart(fig_bar, use_container_width=True)
fig_gdp = get_gdp_subplots(year,fsl/100,fbr/100)
st.plotly_chart(fig_gdp, use_container_width=True)
st.image(im9,use_column_width=True)

st.markdown("# Who has the best athletes ?")
st.markdown("---")
st.image(im3,use_column_width=True)
# fsl2 = st.slider('1 silver equals ()% gold:',min_value=0,max_value=100,value=60)
# fbr2 = st.slider('1 bronze equals ()% gold:',min_value=0,max_value=100,value=30)
fig_ath = get_athplot(fsl/100,fbr/100)
st.plotly_chart(fig_ath, use_container_width=True)
st.image(im2,use_column_width=True)






