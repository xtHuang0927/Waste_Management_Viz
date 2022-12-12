import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import plotly.graph_objects as go

   
def get_AreaChart(data, tooltip):
    areas = (
        alt.Chart(data).mark_area(opacity=0.45,line=True,point=alt.OverlayMarkDef(filled=False, fill='white')).encode(
        x="Year:N",
        y=alt.Y("Thousands of Tons:Q"),
        color="Material:N",
        # tooltip=tooltip,
        tooltip = ['Material','Thousands of Tons']
    )).properties(width=800,height=350)
    
    return areas.interactive()


def get_PieChart(data, colors, selected_method):
    fig = go.Figure(data=[go.Pie(labels=data.index, values=data.values, hole=.3, textinfo='percent')])
    
    fig.update_traces(hovertemplate = '<br><b>Material</b>: %{label}<br>' + '<i>Value</i>: %{value}<extra></extra>',
                      textfont_size=12, marker=dict(colors=colors, line=dict(color='white', width=0.5)))
    fig.update(layout_title_text='Total MSW {} by Material, 2018'.format(selected_method), layout_showlegend=False)
    fig.update(layout_showlegend=False)
    fig.update_layout(margin=dict(t=50, l=30, r=30, b=20))
    return fig

def pie(data):
    alt.Chart(data).mark_arc(innerRadius=50).encode(
    theta=alt.Theta(field="Tons", type="quantitative"),
    color=alt.Color(field="category", type="nominal"),
)


def get_LineChart(data):
    data.Year = data['Year'].astype(str)
    hover = alt.selection_single(
        fields=["Year"],
        nearest=True,
        on="mouseover",
        empty="none")

    lines = (
        alt.Chart(data, height=500, title="MSW Management Trends from 1970 to 2018")
        .mark_line(interpolate='basis')
        .encode(
            x=alt.X("Year",title="Year"),
            y=alt.Y("Tons", title="Thousands of Tons"),
            # x='Year:T',
            # y='Tons:Q',
            color='Type:N',
            strokeDash="Type:N"
        )).properties(width=900,height=350)

    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="Year",
            y="Tons",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Year", title="Date"),
                alt.Tooltip("Tons", title="Thousands of Tons"),
                alt.Tooltip("Type", title="Type"),
            ],
        )
        .add_selection(hover)
    )
    return (lines+points+tooltips).interactive()


def set_EPA():
    st.header('MSW and Waste Management')
    st.subheader('What is Municipal Solid Waste?')
    # st.write('<span style="color:blue">some *blue* text</span>. hahahahaha', unsafe_allow_html=True)
    st.write('Municipal Solid Waste (MSW), commonly called **trash** or **garbage**. This category generally refers to <span style="color:blue">common household waste</span>. \
        as well as <span style="color:blue">office and retail wastes</span>, but excludes industrial, hazardous, and construction wastes.', unsafe_allow_html=True)

    st.image('src/msw.png')

    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.subheader('Which Waste Management is used for MSW?')
    
    col1, col2 = st.columns(2)
    col1.markdown('##### ♻️ Recycling')
    col1.markdown('''Recycling is a series of activities that includes collecting used, reused, or unused items that would otherwise be considered waste; sorting and processing the recyclable products into raw materials; and remanufacturing the recycled raw materials into new products.''')
    col2.markdown('##### 🍂 Composting')
    col2.markdown('Composting is a process by which organic wastes are broken down by microorganisms, generally bacteria and fungi, into simpler forms. The microorganisms use the carbon in the waste as an energy source.')
    st.markdown("")
    col1, col2 = st.columns(2)
    col1.markdown('##### 🔥 Combustion')
    col1.markdown('Combustion is the controlled burning of substances in an enclosed area, as a means of treating and disposing of hazardous waste. ')
    col2.markdown('##### ⚠️ Landfilling')
    col2.markdown('Modern landfills are well-engineered and managed facilities for the disposal of solid waste.')

    st.markdown(" ")
    st.markdown(" ")
    col1, col2, col3 = st.columns([0.25, 4.5, 0.27])
    col2.image('src/method.png')


    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")

    st.markdown('#### Trends')
    st.write(''' <span style="color:blue">Landfilling</span> of MSW is currently and has been the most common waste management practice. 
    A large portion of materials in the waste stream are recovered for recycling and composting, which is becoming an increasingly prevalent trend throughout the country.
    ''', unsafe_allow_html=True)
    df = pd.read_excel('src/dataNew.xlsx')
    line = get_LineChart(df)
    st.markdown("")
    st.markdown("")
    # st.subheader("What Waste Management is used for MSW?")
    st.altair_chart(line.interactive(), use_container_width=True)

    st.markdown("")
    st.markdown('#### Management Type')
    
    # generation = pd.read_csv('src/test.csv') # /src/data.csv
    generation = pd.read_excel('src/Type.xlsx',sheet_name='Generation')
    recycling = pd.read_excel('src/Type.xlsx',sheet_name='Recycling')
    composting = pd.read_excel('src/Type.xlsx',sheet_name='Composting')
    combustion = pd.read_excel('src/Type.xlsx',sheet_name='Combustion')
    landfilling = pd.read_excel('src/Type.xlsx',sheet_name='Landfilling')

    piedata = pd.read_csv('src/Pie.csv')
    
    
    selected_method = st.selectbox(
        "Select one",
        ['Generation', 'Recycling', 'Composting', 'Combustion', 'Landfilling']
        )
    piedata = piedata[piedata['Type']==selected_method]

    colors = ['#A9CCE3','#FDEBD0','#F5B7B1','#A3E4D7','#ABEBC6','#FCF3CF','#F5EEF8','#FCCEEF','#A9977C','#D6DBDF','#D6EAF8'] # 11
    tooltip = ['Paper', 'Glass', 'Metals', 'Plastics', 'Rubber and Leather', 'Textiles', 'Wood', 'Food', 'Yard Trimmings', 'Miscellaneous Inorganic Wastes', 'Other']
    
    if selected_method == 'Generation':
        area = generation
        pie = piedata.drop(['Type'], axis=1).iloc[0]
        selected_text = 'Generated'
        text = 'The total generation of MSW in 2018 was **292.4 million tons**, \
            which was approximately 23.7 million tons more than the amount generated in 2017.  This is an increase from the 268.7 million tons generated in 2017 and the 208.3 million tons in 1990.\
            \n\n In 2018, <span style="color:blue">Plastic</span> products generation was 35.7 million tons, or 12.2 percent of generation. This was an increase of 4.3 million tons from 2010 to 2018, and it came from durable goods and the containers and packaging categories. \
            **Plastics generation has grown from 8.2 percent of generation in 1990 to 12.2 percent in 2018.** \
            Plastics generation as a percent of total generation has varied from 12.2 to 13.2 percent over the past eight years.'
    
    if selected_method == 'Recycling':
        area = recycling
        pie = piedata.drop(['Type'], axis=1).iloc[0]
        selected_text = 'Recycling'
        text = 'The total MSW recycled was **more than 69 million tons**, with paper and paperboard accounting for approximately 67 percent of that amount. \
            Metals comprised about 13 percent, while glass, plastic and wood made up between 4 and 5 percent. \
            \n\n Measured by tonnage, the most-recycled products and materials in 2018 were corrugated boxes (32.1 million tons), \
            mixed nondurable paper products (8.8 million tons), newspapers/mechanical papers (3.3 million tons), \
            lead-acid batteries (2.9 million tons), major appliances (3.1 million tons), wood packaging (3.1 million tons) and glass containers (3 million tons).'

    if selected_method == 'Composting':
        area = composting
        tooltip = ['Food', 'Yard Trimmings', 'Food Other Management']
        pie = piedata[['Food', 'Yard Trimmings', 'Food Other Management']].iloc[0]
        selected_text = 'Composting'
        colors = ['#EAF2F8','#D0ECE7','#A9CCE3','#A2D9CE']
        text = 'The total MSW composted was **25 million tons**. This included approximately 22.3 million tons of yard trimmings (more than a five-fold increase since 1990) and 2.6 million tons of food waste (4.1 percent of generation of wasted food).\
            Other methods of food management were estimated for the first time in 2018. \
            \n\n In 2018, 17.7 million tons of food (28.1 percent of generation of wasted food) was managed through animal feed, co-digestion/anaerobic digestion, bio-based materials/biochemical processing, donation, land application and sewer/wastewater treatment.'

    if selected_method == 'Combustion':
        area = combustion
        pie = piedata.drop(['Type'], axis=1).iloc[0]
        selected_text = 'Combusted'
        text = 'In 2018, **34.6 million tons** of MSW were combusted with energy recovery. Food made up the largest component of MSW combusted at approximately 22 percent. \
            Rubber, leather and textiles accounted for over 16 percent of MSW combustion.\
            <span style="color:blue">Plastic</span> comprised about **16 percent**, and paper and paperboard made up about 12 percent.\
            The other materials accounted for less than 10 percent each.'

    if selected_method == 'Landfilling':
        area = landfilling
        pie = piedata.drop(['Type'], axis=1).iloc[0]
        selected_text = 'Landfill'
        text = 'Landfilling of waste has **decreased** from 94 percent of the amount generated in 1960 to 50 percent of the amount generated in 2018.\
            \n\n In 2018, about **146.1 million tons** of MSW were landfilled. Food was the largest component at about 24 percent. \
            <span style="color:blue">Plastic</span> accounted for over 18 percent, paper and paperboard made up about 12 percent, and rubber, leather and textiles comprised over 11 percent. \
            Other materials accounted for less than 10 percent each.'
        
    area = get_AreaChart(area, tooltip)
    pie = get_PieChart(pie, colors, selected_text)

    st.altair_chart(area.interactive(), use_container_width=True)

    col1, col2 = st.columns((6,5))

    with col1:
        st.plotly_chart(pie, use_container_width=True)
    with col2:
        st.markdown('')
        st.markdown('')
        st.markdown('')
        st.write(text, unsafe_allow_html=True)
    



