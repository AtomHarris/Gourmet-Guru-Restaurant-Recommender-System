import streamlit as st
import pandas as pd
from deployment.app_about import about_us
from streamlit_option_menu import option_menu
from deployment.home import render_home_page
from deployment.app_rating import ratings

# Company Logo
st.sidebar.image('Images/image5.png', use_column_width=True)

# Home Page Option Menu Initialization
selected = option_menu(
    menu_title=None,
    options=["Taste Of Home", "Try Something New", "About Us"],
    icons=["house", "award", "three-dots"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

if selected == "Taste Of Home":
    render_home_page()

elif selected == "Try Something New":
    ratings()
    # st.write("Help!")

elif selected == "About Us":
    about_us()


