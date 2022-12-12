import streamlit as st
import pandas as pd
import altair as alt
from utils.P3Bar import *
from utils.P3Map import *


def set_Emission():

    st.title("Waste Management and Green House Gas Emissions")

    set_ghg()

    st.markdown("")
    st.markdown("---")
    st.markdown("")

    set_Map()

    st.markdown("")
    st.markdown("---")
    st.markdown("")

    CO2 = pd.read_csv('src/CO2_Emissions_Subsector.csv')
        
    # description:
    st.subheader("Waste Sector: Emissions Trends, 2011 to 2021")
    # regression plot
    input_dropdown = alt.binding_select(options=[None]+['MSW Landfills','Solid Waste Combustion',
            'Industrial Waste Landfills','Industrial Wastewater Treatment'], labels = ['All'] + ['MSW Landfills','Solid Waste Combustion',
            'Industrial Waste Landfills','Industrial Wastewater Treatment']
            ,name='Waste Sector ')
    selection = alt.selection_single(fields=['Source'], bind=input_dropdown)
    
    scatterCO2 = alt.Chart(CO2).mark_point().encode(
        x=alt.X('Year', scale=alt.Scale(zero=False)),
        y=alt.Y('Emissions', scale=alt.Scale(zero=False), axis=alt.Axis(title = 'Emissions (metric tons CO2e)')),
        color='Source:N'   
    )  

    lineCO2 = alt.Chart(CO2).mark_line().encode(
        x=alt.X('Year', scale=alt.Scale(zero=False)),
        y=alt.Y('Emissions', scale=alt.Scale(zero=False), axis=alt.Axis(title = 'Emissions (metric tons CO2e)')),
        color='Source:N',opacity=alt.value(0.3)
    )
    reg = scatterCO2.transform_regression('Year', 'Emissions').mark_line().transform_fold(
        ["Regression Line"], 
        as_=["Regression", "y"]
    ).encode(alt.Color("Regression:N"))

    reg_params = scatterCO2.transform_regression('Year', 'Emissions',
                                    method="linear",
                                    params=True   
    ).mark_text(align='left', lineBreak='\n'
    ).encode(
        x=alt.value(50),  # pixels from left
        y=alt.value(230),  # pixels from top
        text='params:N'
    ).transform_calculate(
        params='"r² = " + round(datum.rSquared * 100)/100 + \
        "      y = " + round(datum.coef[0],0)  + " + (" + \
        round(datum.coef[1],0)  + ")"+ "x"').transform_fold(
        ["Regression Result"], 
        as_=["Regression", "y"]
    ).encode(alt.Color("Regression:N"))

    reg_c = alt.layer(scatterCO2, lineCO2,reg,reg_params
        ).properties(
            width=600, height=350
        ).add_selection(
                selection
            ).transform_filter(
                selection
            ).interactive().properties(
title="Trend of Annual Reported GHG Emissions by Waste Sector, Fitted by Linear Regression")        

    st.altair_chart(reg_c,use_container_width=True)

    st.markdown("(Carbon dioxide equivalent or CO2e means the number of metric tons of CO2 emissions with the same global warming potential as one metric ton of another greenhouse gas)")
    st.subheader("Percentage Change of Emissions from 2011 to 2021")
    st.metric(label ="Total Emissions", value = "103.3 MMT CO2e", delta = "-10.1%", delta_color="inverse")
    st.markdown("Decreased of total emissions is mainly due to the notable drop in emissions from MSW landfills.")

    col1, col2 = st.columns(2)
    col1.metric(label ="MSW Landfills", value = "84.7 MMT CO2e", delta = "-9.6%", delta_color="inverse")
    col1.metric(label ="Solid Waste Combustion", value = "9.3 MMT CO2e", delta = "-3.1%", delta_color="inverse")
    col2.metric(label ="Industrial Waste Landfills", value = "7.4 MMT CO2e", delta = "-16.9%", delta_color="inverse")
    col2.metric(label ="Industrial Wastewater Treatment", value = "1.9 MMT CO2e", delta = "-28.5%", delta_color="inverse")

    st.markdown('''
    All waste sectors experienced decrease of CO2e emissioins form 2011 to 2020.
    The decrease in reproted emissions from MSW landfills is due to changes to the rule for calculating methane emissions from MSW landfills.
    Starting in reporting year 2013, MSW landfills are allowed to assume that a higher percentage of methane generated by the landfill is oxidized to
    CO2 as it passes through the landfill soil cover, resulting in lower reported methane emissions.''')
    
    st.subheader('Emissions Prediction for 2022')
    predict = pd.read_csv('src/emissions_prediction_2022.csv')
    st.dataframe(predict, use_container_width =False)
