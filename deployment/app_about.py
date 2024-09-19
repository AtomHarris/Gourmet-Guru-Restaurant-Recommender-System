import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_option_menu import option_menu
from deployment.app_feedback import display_contact_info,contact_form



def about_us():
    # # Custom CSS to reduce the size of the tabs
    # st.markdown(
    #     """
    #     <style>
    #     .nav-pills .nav-link {
    #         font-size: 12px;
    #         padding: 5px 10px;
    #     }
    #     </style>
    #     """,
    #     unsafe_allow_html=True
    # )

    selected1 = option_menu(
        menu_title=None,
        options=["Company History", "Our Team", "Feedback"],
        icons=["bookmark", "pencil-square", "tools"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical",
        styles={
        
        "icon": {"color": "orange"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
        "nav-link-selected": {"background-color": "blue"},
    }
    )

    
    if selected1 == "Company History":
        tab1, tab2, tab3= st.tabs(["Company History","Mission Statement", "Vision"])
        with tab1:
            with st.container(border=True):
                st.header('Company History', divider=True)
                st.write("Gourmet Guru, a dynamic enterprise birthed in 2024, is a testament to the ingenuity and problem-solving spirit of Moringa students. Founded by a group of passionate young minds, the company is committed to addressing global challenges through the innovative lens of culinary arts.")
                st.write("Recognizing the power of food to connect, nourish, and inspire, Gourmet Guru is on a mission to redefine the culinary landscape. By harnessing the creativity and expertise cultivated during their Moringa education, the founders are developing innovative food solutions that cater to diverse tastes and dietary needs.")
                st.write("From the heart of the classroom to the forefront of the food industry, Gourmet Guru embodies the entrepreneurial drive of a new generation. The company's dedication to global problem-solving is evident in its commitment to sustainability, ethical sourcing, and community development. By combining culinary excellence with a strong social conscience, Gourmet Guru aims to create a positive impact on both individuals and the planet.")
        with tab2:
            with st.container(border=True):
                st.header("Mission Statement", divider=True)
                st.write("Gourmet Guru is dedicated to creating exceptional culinary experiences while addressing global challenges. By harnessing the power of food, we strive to nourish bodies, minds, and communities through innovative and sustainable solutions.")
        with tab3:
            with st.container(border=True):
                st.header("Vision",divider=True)
                st.write('To be a global leader in culinary innovation, transforming the way the world eats by creating delicious, sustainable, and accessible food solutions that inspire and empower communities.')
            
            
                st.header('Motto', divider=True)
                st.write('Savor the Solution')
            

    elif selected1 == "Our Team":
        st.header('Our Team', divider=True)
        display_contact_info()

    elif selected1 == "Feedback":
        st.header('Feedback', divider=True)
        contact_form()


