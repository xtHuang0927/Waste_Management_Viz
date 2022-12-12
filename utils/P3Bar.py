import pandas as pd
import altair as alt
import streamlit as st
import json


def set_globalBar():
    
    st.subheader('How much plastic waste globally is recycled,mismanged, incinerated, landfilled ?')
    st.markdown('Globally, only **_9_%** of plastic waste is recycled while **_22_%** is mismanaged. Another 19% is incinerated, 50% ends up in landfill and 22% evades waste management systems and goes into uncontrolled dumpsites, is burned in open pits or ends up in terrestrial or aquatic environments, especially in poorer countries.')

    df_plastic = pd.read_json('src/plasticpollution_outlook.json')

    bar_chart = alt.Chart(df_plastic, title = "Plastic Pollution OECD countries").mark_bar().encode(
        x=alt.X('sum(plastic)', stack='zero', scale=alt.Scale(domain=[0, 100])),
        y='Location',
        color='type',
        tooltip=['Location', 'type']

    ).properties( 
        width=1000,
        height=400
    ).interactive()

    text = alt.Chart(df_plastic).mark_text(dx=-15, dy=3, color='white').encode(
        x=alt.X('sum(plastic):Q', stack='zero'),
        y=alt.Y('Location:N'),
        detail='type:N',
        text=alt.Text('sum(plastic):Q', format='.1f')
    )

    st.altair_chart(bar_chart + text)

    df_plastic_world = pd.read_json('src/world_outlook.json')

    bar_chart = alt.Chart(df_plastic_world, title = "Plastic Pollution World").mark_bar(size=50).encode(
        x=alt.X('sum(plastic)', stack='zero', scale=alt.Scale(domain=[0, 100])),
        y='Location',
        color='type',
        tooltip=['Location', 'type']

    ).properties( 
        width=900,
        height=250
    ).interactive()

    text = alt.Chart(df_plastic_world).mark_text(dx=-15, dy=3, color='white').encode(
        x=alt.X('sum(plastic):Q', stack='zero'),
        y=alt.Y('Location:N'),
        detail='type:N',
        text=alt.Text('sum(plastic):Q', format='.1f')
    )

    col1, col2 = st.columns([0.5, 4.5])
    col2.altair_chart(bar_chart + text)




def set_ghg():
    
    st.subheader('GHG by Emission & Number of Facilities')
    genre = st.radio(
        " Direct GHG Emissions Reported by Sector (2021):",
        ('Emission', 'Number of Facilities'))

    if genre == 'Emission':
        # st.markdown('#### GHG Waste By different sector')
        st.markdown('GHG production by Waste such as landfills is 70,000 metric ton of carbon dioxide, \
            in scale 70,000 GREAT White Sharks!')

        df_emission = pd.read_csv('src/GHG_emission.csv')

        bar_chart = alt.Chart(df_emission, title = "Direct GHG by Emission by Sector").mark_bar().encode(
            x = 'Emission (million metric tons CO2):Q' ,
            y=alt.Y('Sector:N', sort='-x')  ,
            color='Sector:N'  ,
            tooltip=['Emission (million metric tons CO2)', 'Number of Facilities']
        ).properties( 
            width=1000,
            height=400
        ).interactive()
        st.altair_chart(bar_chart)

    if genre == 'Number of Facilities':
        # st.markdown('#### GHG Waste has 1460 facilities. ')
        st.markdown('103.3 million metric ton of CO2 from 1462 facilities.')

        df_number_of_facilities = pd.read_csv('src/GHG_emission.csv')

        bar_chart = alt.Chart(df_number_of_facilities, title = "Direct GHG by Number of Facilities by Sector").mark_bar().encode(
            x = 'Number of Facilities:Q' ,
            y=alt.Y('Sector:N', sort='-x'),
            color='Sector:N'  ,
            tooltip=['Emission (million metric tons CO2)', 'Number of Facilities']

        ).properties( 
            width=1000,
            height=400
        ).interactive()

        st.altair_chart(bar_chart)    
