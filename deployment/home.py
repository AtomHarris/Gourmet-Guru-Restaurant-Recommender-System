

import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
from deployment.app_classes import recommendation, pagenation, get_business_info, get_yelp_reviews

# Loading the restaurant data
@st.cache_data
def load_data():
    return pd.read_pickle('pickled_files/restaurants_data.pkl')

df = load_data()


def render_home_page():
    """
    Function to recommend restaurants based on restaurant name or cuisine in any state in the database
    """
    with st.container(border=True):
        # Initialize session state variables
        if 'recommendations' not in st.session_state:
            st.session_state.recommendations = pd.DataFrame()
        if 'selected_restaurant' not in st.session_state:
            st.session_state.selected_restaurant = None
            

        st.markdown(
            """
            <style>
            .center-text {
                text-align: center;
                        }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.markdown('<h2 class="center-text" style="color: royal blue;">GOURMET GURUS</h2>', unsafe_allow_html=True)
        st.markdown('<h3 class="center-text" style="color: royal blue;">A Revolution In Restaurant Recommendation</h3>', unsafe_allow_html=True)
        # st.markdown('<h6 class="center-text" style="color: royal blue;">Are you in a new city and are craving your favourite meal? Do you miss a taste of home?</h2>', unsafe_allow_html=True)
        # st.markdown('<h6 class="center-text" style="color: royal blue;">Well look no further! Gourmet Guru has got you covered!!!</h2>', unsafe_allow_html=True)
        st.write('Do you miss a taste of your favourite restaurants?')
        st.write("Are you in a new city and are craving your favourite meal?")
        st.write("Well look no further! Gourmet Guru has got you covered!!!")

        
        # Sidebar for user inputs
        st.sidebar.header('Search for a Restaurant', divider= "rainbow")

        # Get unique states, cities, and restaurant names and sort them
        states = sorted(df['state'].unique())

        # State selection
        state = st.sidebar.selectbox('Choose Your State:', ['All'] + states)

        # Filter cities based on selected state
        if state == 'All':
            filtered_cities = sorted(df['city'].unique())
        else:
            filtered_cities = sorted(df[df['state'] == state]['city'].unique())

        # City selection
        city = st.sidebar.selectbox('Choose Your City', ['All'] + filtered_cities)

        if city != 'All':
            # Option to either choose a restaurant name or enter a category
            search_option = st.sidebar.radio(
                "Search by",
                ('Restaurant Name', 'Cuisine')
            )

            if search_option == 'Restaurant Name':
                # Filter restaurant names based on selected state and city
                restaurants = sorted(df[(df['state'] == state) & (df['city'] == city)]['name'].unique())
                restaurant_name = st.sidebar.selectbox('Restaurant Name', ['All'] + restaurants)
            

                on = st.sidebar.toggle("Recommendation In Another State")

                if on:
                    # st.write("Feature activated!")
                
                    state = st.sidebar.selectbox('Choose Your State:', ['All'] + states, key="new_state")

                    # Filter cities based on selected state
                    if state == 'All':
                        filtered_cities = sorted(df['city'].unique())
                    else:
                        filtered_cities = sorted(df[df['state'] == state]['city'].unique())

            elif search_option =='Cuisine':

                # Extracting unique categories and creating a selectbox
                categories = sorted(df[(df['state'] == state) & (df['city'] == city)]['categories'].unique())
                selected_category = st.sidebar.selectbox("Choose a Cuisine", ['All'] + categories)
                



            # Adding a "Recommend" button
            recommend_button = st.sidebar.button('Recommend')

            if recommend_button:
                if search_option == 'Restaurant Name' and restaurant_name != 'All':
                    # Use content-based filtering to find similar restaurants by name
                    st.session_state.recommendations = recommendation(df, state=state, name= restaurant_name)
                elif search_option == 'Cuisine' and selected_category != 'All':
                    # Use content-based filtering to find restaurants by category
                    st.session_state.recommendations = recommendation(df, state=state, category=selected_category)
                else:
                    st.sidebar.warning("Please select a valid restaurant name or cuisine to get recommendations.")

        # Display the filtered DataFrame with selected columns
        if not st.session_state.recommendations.empty:
            # st.spinner("COOKING SOMETHING UP FOR YOU!!!!!")
            st.subheader('Recommended Restaurants', divider= True)
            
            # Paginate the filtered recommendations
            filtered_df = pagenation(st.session_state.recommendations, 'city')

            # Add a dropdown to select a restaurant from the filtered DataFrame on the current page
            if not filtered_df.empty:
                selected_restaurant = st.selectbox(
                    'Select a Restaurant to View Details',
                    options=['Select a Restaurant'] + list(filtered_df['Restaurant Name']),
                    index=0
                )
            # Update the session state for the selected restaurant
            st.session_state.selected_restaurant = selected_restaurant

            if st.session_state.selected_restaurant != 'Select a Restaurant':
                info = df[df['name'] == st.session_state.selected_restaurant].iloc[0]
                
                with st.container(border=True):
                    st.subheader(f"{info['name']} Information", divider=True)
                    col1, col2 = st.columns([2,1])
                    # Displaying metainformation on selected restaurant 
                    with col2:
                        with st.container(height=520,border=True):
                            # st.write(f"**Restaurant Name:** {info['name']}")
                            st.write(f"**State:** {info['state']}")
                            st.write(f"**City:** {info['city']}")
                            st.write(f"**Address:** {(info['address'])}")
                            st.write(f"**Phone:** {get_business_info(info['business_id'])['phone']}")
                            st.write(f"**Cuisine:** {info['categories']}")
                            st.write(f"**Rating:** {info['stars']}")
                            st.link_button("Visit Website", get_business_info(info["business_id"])["website"])

                            
                    # Plotting a folium map of the restaurant location with google maps route attached                           
                    with col1:
                        with st.container(height=520, border=True):    
                            if 'latitude' in info and 'longitude' in info:
                                latitude = info['latitude']
                                longitude = info['longitude']

                                if pd.notna(latitude) and pd.notna(longitude):
                                    
                                    m = folium.Map(location=[latitude, longitude], zoom_start=16, dragging=True, zoom_control=True,
                                                scrollWheelZoom=True)

                                    icon = folium.Icon(icon='star', color='red') 

                                    folium.Marker(
                                        location=[latitude, longitude],
                                        popup=info['name'],
                                        tooltip=info['name'],
                                        icon=icon  
                                    ).add_to(m)

                                    
                                    st_folium(m, width=700, height=400)

                                    route = f"http://maps.google.com/maps?z=12&t=m&q=loc:{latitude}+{longitude}"
                                    st.link_button('Get Directions',route)
                            else:
                                st.write("Location data is not available for this restaurant.")
                    
                    # Scrapping the restaurant images from yelp
                    with st.expander("Restaurant Images", expanded=False):
                        image_urls = get_business_info(info["business_id"])["image_urls"]
                        if image_urls:
                            
                            num_cols = 3  
                            cols = st.columns(num_cols)
                            for i, url in enumerate(image_urls):
                                col_index = i % num_cols
                                with cols[col_index]:
                                    st.image(url, use_column_width=True)
                        else:
                            st.write("No images available for this restaurant.")

                    with st.expander("More Information", expanded=False):
                        tab1,tab2 =st.tabs(["Hours","Reviews"])
                        #Display business hours if available
                        with tab1:
                            
                            day_mapping = {
                                    0: 'Monday',
                                    1: 'Tuesday',
                                    2: 'Wednesday',
                                    3: 'Thursday',
                                    4: 'Friday',
                                    5: 'Saturday',
                                    6: 'Sunday'
                                }
                            if 'hours' in get_business_info(info["business_id"]) and get_business_info(info["business_id"])['hours']:
                                st.subheader("**Open Hours:**", divider= True)
                                # Initialize dictionary to store hours
                                hours_dict = {day: 'Closed' for day in day_mapping.values()}
                                for item in get_business_info(info["business_id"])['hours'][0]['open']:
                                    day_num = item.get('day', '')
                                    start = item.get('start', '')
                                    end = item.get('end', '')
                                    if day_num in day_mapping:
                                        day_name = day_mapping[day_num]
                                        hours_dict[day_name] = f"{start} - {end}"
                                
                                # Display hours in a readable format
                                for day, hours in hours_dict.items():
                                    st.write(f"{day}: {hours}")
                        # Display restaurant reviews
                        with tab2:
                            st.subheader("Restaurant Reviews", divider=True)
                            reviews = get_yelp_reviews(info["business_id"])
                            if reviews:
                                for review in reviews:
                                    st.subheader(f"Review by {review['user']}")
                                    st.write(f"Rating: {review['rating']}")
                                    st.write(f"Date: {review['time_created']}")
                                    st.write(f"Review: {review['text']}")
                                    st.write("---")
                            else:
                                st.write("No reviews found or an error occurred.")
                        