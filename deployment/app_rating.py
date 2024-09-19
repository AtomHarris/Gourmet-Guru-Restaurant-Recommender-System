import time
import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
from deployment.app_classes import pagenation, recommend_restaurants, collect_ratings, get_business_info, get_yelp_reviews

# Loading the restaurant data
@st.cache_data
def load_data():
    return pd.read_pickle('pickled_files/restaurants_data.pkl')

df = load_data()

# Loading the user review data
@st.cache_data
def load_data():
    return pd.read_pickle('pickled_files/new_df.pkl')

new_df = load_data()



def reset_state():
    """
    Function to reset session state
    """
    st.session_state.selected_restaurant = None
    st.session_state.ratings = []
    st.session_state.ratings_confirmed = False
    st.session_state.recommendations = pd.DataFrame()

def ratings():
    """
    Function to use the ratings for the sampled restaurants and recommend restaurants similar to those restaurants
    """
    with st.container(border=True):
        st.header('🍴 Restaurant Recommendations', divider=True)

        # Initializing the session states
        if 'selected_restaurant' not in st.session_state:
            st.session_state.selected_restaurant = None

        if 'ratings' not in st.session_state:
            st.session_state.ratings = []

        if 'ratings_confirmed' not in st.session_state:
            st.session_state.ratings_confirmed = False  

        if 'recommendations' not in st.session_state:
            st.session_state.recommendations = pd.DataFrame() 

        # re-assigning the variable df to all_restaurants
        all_restaurants_df = df

        # Get user input
        user_id = st.text_input("Enter your user ID")

        if user_id:
            # Filter states
            states = sorted(all_restaurants_df['state'].unique())
            state = st.selectbox('Choose Your State:', ['Select a State'] + states, index=0)

            if state == 'Select a State':
                state = sorted(all_restaurants_df['city'].unique())
            else:
                cities = sorted(all_restaurants_df[all_restaurants_df['state'] == state]['city'].unique())
                city = st.selectbox('Choose Your City:', ['Select a City'] + cities, index=0)

                if city != 'Select a City':
                
                    filtered_df = all_restaurants_df[(all_restaurants_df['state'] == state) & (all_restaurants_df['city'] == city)]
                        
                    if not st.session_state.get('ratings_confirmed', False):
                        if filtered_df.empty:
                            st.write("No restaurants available for the selected criteria.")
                        else:
                            collect_ratings(filtered_df, state)

                    # st.write("Current Ratings:", st.session_state.get('user_ratings', {}))

                    if st.button("Confirm Ratings"):
                        with st.spinner('Cooking something up for you...'):
                            st.session_state.ratings_confirmed = True
                            time.sleep(2)
                            st.session_state.recommendations = recommend_restaurants(user_id, st.session_state.get('user_ratings', []), all_restaurants_df, state)
                    
            # Get the top recommendations and pagenate them
            if not st.session_state.recommendations.empty:
                st.write("Top Recommendations:")
                filtered_df = pagenation(st.session_state.recommendations, 'city')

                # Selecting restaurant to view details on
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
                            col1, col2 = st.columns([2, 1])

                            # Metainformation on the restaurant
                            with col2:
                                with st.container(height=520, border=True):
                                    st.write(f"**State:** {info['state']}")
                                    st.write(f"**City:** {info['city']}")
                                    st.write(f"**Address:** {info['address']}")
                                    st.write(f"**Phone:** {get_business_info(info['business_id'])['phone']}")
                                    st.write(f"**Cuisine:** {info['categories']}")
                                    st.write(f"**Rating:** {info['stars']}")
                                    st.link_button("Visit Website", get_business_info(info["business_id"])["website"])

                            # Folium map for the restaurant location
                            with col1:
                                with st.container(border=True):    
                                    if 'latitude' in info and 'longitude' in info:
                                        latitude = info['latitude']
                                        longitude = info['longitude']

                                        if pd.notna(latitude) and pd.notna(longitude):
                                            m = folium.Map(location=[latitude, longitude], zoom_start=16, dragging=True, zoom_control=True, scrollWheelZoom=True)
                                            icon = folium.Icon(icon='star', color='red') 
                                            folium.Marker(location=[latitude, longitude], popup=info['name'], tooltip=info['name'], icon=icon).add_to(m)
                                            st_folium(m, width=700, height=400)
                                            route = f"http://maps.google.com/maps?z=12&t=m&q=loc:{latitude}+{longitude}"
                                            st.button(f"[Get Directions]({route})")
                                    else:
                                        st.write("Location data is not available for this restaurant.")

                            # Scrapped images from the choosen restaurant on Yelp
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

                            # More scrapped information on the restaurant
                            with st.expander("More Information", expanded=False):
                                tab1, tab2 = st.tabs(["Hours", "Reviews"])

                                # Working hours if available
                                with tab1:
                                    day_mapping = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
                                    if 'hours' in get_business_info(info["business_id"]) and get_business_info(info["business_id"])['hours']:
                                        st.subheader("**Open Hours:**", divider= True)
                                        hours_dict = {day: 'Closed' for day in day_mapping.values()}
                                        for item in get_business_info(info["business_id"])['hours'][0]['open']:
                                            day_num = item.get('day', '')
                                            start = item.get('start', '')
                                            end = item.get('end', '')
                                            if day_num in day_mapping:
                                                day_name = day_mapping[day_num]
                                                hours_dict[day_name] = f"{start} - {end}"
                                        for day, hours in hours_dict.items():
                                            st.write(f"{day}: {hours}")
                                # Reviews on the restaurant
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

    # Reset Button
    if st.button("Reset"):
        reset_state()
        st.experimental_rerun()
