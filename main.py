# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

from utils.P2MSW import *
from utils.P3Map import *
from utils.P1Intro import *
from utils.P2Plastic import *
from utils.P3Emission import *


st.set_page_config(page_title='Waste Management',
                   # page_icon='https://www.google.com/s2/favicons?domain=https://transitapp.com/',
                   page_icon='🚮',
                   initial_sidebar_state ='collapsed',
                   layout='wide') # wide, centered


# st.sidebar.image('src/GTFS.png', width=200)
st.sidebar.header('Waste Management')

st.sidebar.markdown('')

menu = st.sidebar.radio(
    "",
    ('Introduction','MSW and Waste Management','Greenhouse Gas Emissions'),
)

# st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

st.sidebar.markdown('---')
# st.sidebar.write('xxx | Dec 2022')

if menu == 'Introduction':
    set_Intro()
if menu == 'MSW and Waste Management':
    set_Plastic()
if menu == 'Greenhouse Gas Emissions':
    set_Emission()
