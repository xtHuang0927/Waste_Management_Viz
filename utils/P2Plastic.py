import streamlit as st
import pandas as pd
import altair as alt
from utils.P2MSW import *
from utils.P3Bar import *

def set_Plastic():
    
    # headerSection = st.container()
    mainSection = st.container()
    LeftNav = st.sidebar

    with LeftNav:
        # st.title("Chapter")
        # st.markdown("Navigater list")
        # st.button('Menu1', on_click=lambda: st.success("menu1"))
        # st.button('Menu2', on_click=lambda: st.success("menu2"))
        options = st.radio('Topics', options = ['MSP','Example: Plastics'])
    # options2 = st.radio('Platics', options = ['Global Plastics','Plastic Weight'])

    with mainSection:

        # load data
        global_plastic = pd.read_csv('src/global_plastics_production.csv')
        global_plastic['Year'] = global_plastic['Year'].astype(str)

        cumu_plastic = pd.read_csv('src/cumulative_global_plastics.csv')
        cumu_plastic['Year'] = cumu_plastic['Year'].astype(str)

        plastic_weight = pd.read_csv('src/Plastics_MSW_Weight.csv')
        plastic_weight['Year'] = plastic_weight['Year'].astype(str)

        if options == "MSP":
            set_EPA()

        elif options == "Example: Plastics":
            st.header("Waste Example: Plastics")
            st.subheader("How much plastic does the world produce? ")
            st.markdown(''' The chart shows the increase of global plastic production since 1950, measured in million tonnes per year.
            \nThe world production of plastics was 2 million tonnes per year in 1950. Since then, the annual production has increased nearly 230-fold, reaching 460 million tonnes in 2019.
            \nThe short downturn in annual production in 2009 and 2010 was predominantly the result of the 2008 global financial crisis.

            ''')
            line = alt.Chart(global_plastic).mark_line(interpolate='basis').encode(
                x='Year:T',
                y=alt.Y('Global plastics production:Q',title = 'Global plastics production (million tonnes)')
                )
            # Create a selection that chooses the nearest point & selects based on x-value
            nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['Year'], empty='none')
            # Transparent selectors across the chart. This is what tells us the x-value of the cursor
            selectors = alt.Chart(global_plastic).mark_point().encode(
                x='Year:T',
                opacity=alt.value(0),
            ).add_selection(
                nearest
            )
            # Draw points on the line, and highlight based on selection
            points = line.mark_point().encode(
                opacity=alt.condition(nearest, alt.value(1), alt.value(0))
            )

            # Draw text labels near the points, and highlight based on selection
            text = line.mark_text(align='left', dx=5, dy=-20).encode(
                text=alt.condition(nearest, 'Global plastics production:Q', alt.value(' '))
            )

            # Draw a rule at the location of the selection
            rules = alt.Chart(global_plastic).mark_rule(color='gray').encode(
                x='Year:T', 
            ).transform_filter(
                nearest
            )

            # Put the five layers into a chart and bind the data
            line_plot = alt.layer(
                line, selectors, points, rules, text
            ).properties(
                width=600, height=350, title ='Global Plastics Production*'
            ).interactive()
            st.altair_chart(line_plot, use_container_width=True)

            st.markdown("")
            st.markdown("---")
            st.markdown("")
            
    # area plot
            st.subheader("How much plastic has the world produced cumulatively?")
            st.markdown('''The chart shows that the world had produced 9.5 billion tonnes of plastic by 2019, 
            which is equivalent to more than one tonne of plastic for every person alive today. ''')
            area = alt.Chart(cumu_plastic).mark_area(interpolate='basis').encode(
                x='Year:T',
                y=alt.Y('Cumulative global plastics production:Q',title = 'Cumulative global plastics production (million tonnes)'),
                )
            line_area = alt.Chart(cumu_plastic).mark_line(interpolate='basis').encode(
                x='Year:T',
                y='Cumulative global plastics production:Q',
                )
            # Create a selection that chooses the nearest point & selects based on x-value
            nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['Year'], empty='none')
            # Transparent selectors across the chart. This is what tells us the x-value of the cursor
            selectors = alt.Chart(cumu_plastic).mark_point().encode(
                x='Year:T',
                opacity=alt.value(0),
            ).add_selection(
                nearest
            )
            # Draw points on the line, and highlight based on selection
            points = line_area.mark_point().encode(
                opacity=alt.condition(nearest, alt.value(1), alt.value(0))
            )

            # Draw text labels near the points, and highlight based on selection
            text = line_area.mark_text(align='left', dx=5, dy=-25).encode(
                text=alt.condition(nearest, 'Cumulative global plastics production:Q', alt.value(' '))
            )

            # Draw a rule at the location of the selection
            rules = alt.Chart(cumu_plastic).mark_rule(color='gray').encode(
                x='Year:T', 
            ).transform_filter(
                nearest
            )

            # Put the five layers into a chart and bind the data
            area_plot = alt.layer(area,
                line_area, selectors, points, rules, text
            ).properties(
                width=600, height=400, title = "Cumulative Global Production of Plastics*"
            ).interactive()
            st.altair_chart(area_plot, use_container_width=True)
            st.markdown("*Plastic production refers to the annual production of polymer resin and fibers.")

            st.markdown("")
            st.markdown("---")
            st.markdown("")
            
            set_globalBar()

            st.markdown("")
            st.markdown("---")
            st.markdown("")

    # plastics waste management
            st.subheader('How do we manage plastic waste materials in municipal solid waste (MSW) in the US?')
            st.markdown('''
            Plastics are a rapidly growing segment within MSW. In 2018, plastics generation was **35.7 million tons** in the United States, which was **12.2 percent** of MSW generation. 
            \nThe containers and packaging category had the most plastic tonnage at over **14.5 million tons** in 2018, including bags, sacks and wraps; other packaging; polyethylene terephthalate (PET) bottles and jars; high-density polyethylene (HDPE) natural bottles; and other containers. 
            \nPlastics are found in nondurable products, such as disposable diapers, trash bags, cups, utensils, medical devices, and household items such as shower curtains. The plastic food service items are generally made of clear or foamed polystyrene, while trash bags are made of high-density polyethylene (HDPE) or low-density polyethylene (LDPE).
            \nPlastic resins are also used in a variety of container and packaging products, such as PET beverage bottles, HDPE bottles for milk and water, and a wide variety of other resin types used in other plastic containers, bags, sacks, wraps, and lids.
            ''')

            c = alt.Chart(plastic_weight, 
            title = 'Plastics Waste Management: 1960-2018').mark_area().encode(
                x='Year:T',
                y=alt.Y("Weight:Q", stack=True, axis=alt.Axis(title = 'Weight (in thousands of U.S. tons)')),
                color = 'Management Pathway:N', opacity=alt.value(0.7)
            )
            st.altair_chart(c, use_container_width=True)
            with st.expander("See explanation 🧑‍🏫 "):
                st.markdown('''
                \n - Most of the plastic ends up in landfills where it may take up to **500 years** to decompose and potentially leak pollutants into the soil and water :shocked_face_with_exploding_head:
        \n - It’s estimated that there are already **165 million tons** of plastic debris floating around in the oceans threatening the health and safety of marine life. 
        \n - Relatively little plastic waste is recycled because there are various types of plastic with different chemical compositions, and recycled plastics can be contaminated by the mixing of types. 
        \n - Plastic waste is also contaminated by materials such as paper and ink. Separating plastics from other recyclables and different types of plastic from each other is labor-intensive, and so far, there has been no easy solution :heavy_exclamation_mark:
                ''')
