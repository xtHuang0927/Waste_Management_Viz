import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def PlotCO2(df):

    df['text'] = '<br>CO2e Emissions: ' + df['total'].astype(str)+' metric tons'
    df = df.sort_values(by="total", ascending=True)

    limits = [(0,50),(50,203),(203,451),(451,672),(672,1111),(1111,1204)]
    colors = ["#F2D7D5","#E6B0AA","#D98880","#CD6155","#C0392B","#922B21"]


    fig = go.Figure()
    names = ['< 5000','5,000 - 20,000','20,000 - 40,000','40,000 - 60,000','40,000 - 60,000','> 200,000']

    for i in range(len(limits)):

        lim = limits[i]
        df_sub = df[lim[0]:lim[1]]
        fig.add_trace(go.Scattergeo(
            locationmode = 'USA-states',
            lon = df_sub['lon'],
            lat = df_sub['lat'],
            text = df_sub['text'],
            marker = dict(
                size = df_sub['size'] * 1.75,
                color = colors[i],
                line_color='rgb(40,40,40)',
                line_width=0.5,
                sizemode = 'area'
            ),
            name = '{}'.format(names[i])))

    fig.update_layout(
            showlegend = True,
            margin=dict(t=0, l=0, r=0, b=0),
            geo = dict(
                scope = 'usa',
                landcolor = 'rgb(217, 217, 217)'))

    return fig


def set_Map():

    st.subheader('Location and emissions for each reporting facility in the waste sector')

    df1 = pd.read_csv('src/CO2.csv')
    fig1 = PlotCO2(df1)
    st.markdown('Sizes of each circle corresponding to a specified range of emissions in **Metric Tons of CO2e** reported by that particular facility. Many large industrial waste landfills are in southeastern states and along the coastline of the Gulf of Mexico, which is also where numerous petroleum refineries, pulp and paper, and chemical manufacturing facilities are located. ')
    st.plotly_chart(fig1, use_container_width=True)
