import os
import pickle
import requests
import numpy as np
import pandas as pd
import streamlit as st
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

@st.cache_data
def load_data():
    return pd.read_pickle('pickled_files/new_df.pkl')

new_df = load_data()

# Yelp API key
API_KEY = os.getenv('API_KEY')

# Yelp Business Endpoint
YELP_BUSINESS_URL = "https://api.yelp.com/v3/businesses/"

# Headers for the API request
headers = {
    'Authorization': f'Bearer {API_KEY}',
}

def get_business_info(business_id):

    """
    Function to generate business information including, name, phone number, business operating hours and website url
    """
    response = requests.get(f'{YELP_BUSINESS_URL}{business_id}', headers=headers)
    
    if response.status_code == 200:
        business_data = response.json()
        
        # Extract basic information
        name = business_data.get('name', '')
        phone = business_data.get('display_phone', '')
        website = business_data.get('url', '')
        hours = business_data.get('hours', '')
        address = business_data.get('address', '')


        image_urls = business_data.get('photos', [])
        return {
            'name': name,
            'phone': phone,
            'website': website,
            'hours': hours,
            'image_urls': image_urls,
            'address': address
        }
    
    elif response.status_code == 429:
        print("Rate limit exceeded. Please try again later.")
    else:
        print(f"Failed to retrieve data for Business ID: {business_id}, Status Code: {response.status_code}")
    
    return {}

def get_yelp_reviews(business_id):
    """
    Function to generate restaruant reviews for each restaurant
    """

    url = f'https://api.yelp.com/v3/businesses/{business_id}/reviews'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
    }

    response = requests.get(url, headers=headers)

    reviews_info = []
    if response.status_code == 200:
        reviews = response.json().get('reviews', [])
        for review in reviews:
            reviews_info.append({
                'user': review['user']['name'],
                'rating': review['rating'],
                'text': review['text'],
                'time_created': review['time_created']
            })
    else:
        print(f"Failed to retrieve reviews: {response.status_code}")

    return reviews_info


def preprocess(df):
    """
    Function to preprocess the data to combine the needed features into one column
    """
    filtered_df=df 
    filtered_df['combined_features'] = (
                                        
                                        filtered_df['categories'] + " " +
                                        filtered_df['attributes_true'] 
    )
    filtered_df = filtered_df.reset_index(drop=True)
    return filtered_df

def create_feature_vectors(df):
    """
    Performing vectorization of the preprocessed categorical features 
    and combining with the numerical features
    """
    
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['combined_features'])
    
    
    numerical_features = df[['stars']].values
    combined_features = np.hstack((tfidf_matrix.toarray(), numerical_features))
    # combined_features=tfidf_matrix
    
    return combined_features

def recommendation(df, state, name=None, category=None):
    """
    Function to generate the recommendations based on restaurant names by using cosine similarity 
    as well as filtering based on cuisine types
    """
    preprocessed = preprocess(df)
    
    def cuisines(cuisine=None, state=state):
        preprocessed=df[df["state"]==state]
        cuisine_df = preprocessed[preprocessed['categories'] == cuisine]
        cuisine_df_sorted = cuisine_df.sort_values(by=["stars", "city"], ascending=False)
        return cuisine_df_sorted[['name', 'state', 'city', 'stars', 'address', 'categories']]
    
    if name:
        if name not in preprocessed['name'].values:
            raise ValueError(f"Restaurant with name '{name}' not found in the filtered data.")
        
        idx = preprocessed[preprocessed['name'] == name].index[0]
        exclude_names = [name]

        row_to_add = preprocessed.iloc[idx]
        row_to_add_df = pd.DataFrame([row_to_add])     
        specific_state= preprocessed[preprocessed["state"] == state]
        specific_state = pd.concat([specific_state, row_to_add_df]).reset_index(drop=True)
        idx = specific_state[specific_state['name'] == name].index[0]
    
        combined_features = create_feature_vectors(specific_state)
        cosine_sim = cosine_similarity(combined_features, combined_features)
        
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        top_indices = [i[0] for i in sim_scores]  
        
        recommended_restaurants = specific_state.iloc[top_indices]
        recommended_restaurants = recommended_restaurants[~recommended_restaurants['name'].isin(exclude_names)]        
        
        return recommended_restaurants[['name', 'state', 'city', 'stars', 'address','categories']].drop_duplicates(subset='name')
    
    elif category:
        return cuisines(category)


def pagenation(df, filter_column):
    """
    Function to create pagenation on recommended dataframe and filter the dataframe
    """
    
    filter_values = sorted(df[filter_column].unique())
    filter_values.insert(0, 'All')  
    selected_value = st.selectbox(f"Filter by {filter_column}", filter_values)

    if selected_value == 'All':
        filtered_df = df
    else:
        filtered_df = df[df[filter_column] == selected_value]
    
    rows_per_page = 10
    total_pages = len(filtered_df) // rows_per_page + (len(filtered_df) % rows_per_page > 0)
    page = st.number_input('Page Number:', min_value=1, max_value=total_pages, value=1)
   
    start_idx = (page - 1) * rows_per_page
    end_idx = start_idx + rows_per_page
    page_df = filtered_df.iloc[start_idx:end_idx]
    column_map = {
        'name': 'Restaurant Name',
        'state': 'State',
        'city': 'City',
        'stars': 'Ratings',
        'address': 'Address',
        'categories': 'Cuisine'
    }
    page_df = page_df.rename(columns=column_map)
    st.dataframe(page_df, hide_index= True)
    
    return page_df


def collect_ratings(df, state=None):
    """
    Function to collect 3 necessary ratings for the collaborative function to recommend 
    """
    num_ratings = 3

    # Initialize session state for user ratings and sampled restaurants
    if 'user_ratings' not in st.session_state:
        st.session_state.user_ratings = []  # List to store tuples of (business_id, rating)

    if 'sampled_restaurants' not in st.session_state:
        sampled_df = df if state is None else df[df['state'] == state]
        st.session_state.sampled_restaurants = sampled_df.sample(num_ratings).reset_index(drop=True)

    # Create 3 columns layout
    cols = st.columns(num_ratings)

    for i in range(num_ratings):
        restaurant = st.session_state.sampled_restaurants.iloc[i]
        with cols[i]:
            with st.container(border=True, height= 300):
                st.write(f"**Restaurant:** {restaurant['name']} ({restaurant['city']}, {restaurant['state']})")
                st.write(f"**Cuisine:** {restaurant['categories']}")  
                rating = st.number_input(
                    f"Rate {restaurant['name']}",
                    min_value=1.0,  
                    max_value=5.0,  
                    value=3.0,
                    step=0.5,  
                    key=f"rating_{restaurant['business_id']}"
                )
            # Update the ratings list in session state
            # Remove old rating for this restaurant if exists
            st.session_state.user_ratings = [
                (r_id, r) for r_id, r in st.session_state.user_ratings if r_id != restaurant['business_id']
            ]
            st.session_state.user_ratings.append((restaurant['business_id'], rating))

def recommend_restaurants(user_id, rated_restaurants, all_restaurants_df, state=None):
    """
    Recommend restaurants based on user ratings and state.
    """
    # # Debugging: Check if rated_restaurants is being passed correctly
    # st.write("Rated Restaurants Received:")
    # st.write(rated_restaurants)

    if state:
        all_restaurants_df = all_restaurants_df[all_restaurants_df["state"] == state]

    # Get all restaurant IDs
    all_restaurant_ids = all_restaurants_df['business_id'].unique()

    # Prepare the data for training the model
    user_ratings_df = pd.DataFrame(rated_restaurants, columns=['business_id', 'rating'])
    user_ratings_df['user_id'] = user_id

    # Debugging: Display the user ratings DataFrame
    # st.write("User Ratings DataFrame:")
    # st.dataframe(user_ratings_df)

    # Combine user-specific ratings with the full dataset
    combined_df = pd.concat([new_df, user_ratings_df]) 

    # Filter combined_df to include only relevant restaurants
    filtered_df = combined_df[combined_df['business_id'].isin(all_restaurant_ids)]

    # Define the Reader and Dataset
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(filtered_df[['user_id', 'business_id', 'rating']], reader)

    trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

    # Retrain the model
    model_4 = SVD(n_factors=20, reg_all=0.01, n_epochs=40, random_state=42)
    model_4.fit(trainset)

    # Filter out the restaurants that the user has already rated
    rated_restaurant_ids = [rid for rid, _ in rated_restaurants]
    unrated_restaurants = [rid for rid in all_restaurant_ids if rid not in rated_restaurant_ids]

    # Predict ratings for all unrated restaurants
    predictions = [model_4.predict(user_id, rid) for rid in unrated_restaurants]

    # Create a DataFrame for the predictions
    pred_df = pd.DataFrame({
        'business_id': [pred.iid for pred in predictions],
        'predicted_rating': [pred.est for pred in predictions]
    })

    # Merge with the original restaurants DataFrame to get more information
    recommendations = pred_df.merge(all_restaurants_df, on='business_id', how='left')

    # Sort by predicted rating and get top recommendations
    recommendations = recommendations.sort_values(by='predicted_rating', ascending=False)

    return recommendations[['name', 'state', 'city', 'stars', 'address', 'categories', 'predicted_rating']].drop_duplicates(subset='name')
