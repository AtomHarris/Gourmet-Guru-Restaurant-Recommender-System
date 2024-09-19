# GOURMET GURU RESTAURANT RECOMMENDER SYSTEM
***



https://github.com/user-attachments/assets/27c82469-5fff-4c59-bf3d-cdd627928a0e





# Introduction

In today's world, where culinary diversity and dining out have become integral to our lives, choosing the right restaurant can be both exciting and overwhelming. With countless options from quaint bistros to exotic eateries, making a dining decision is increasingly challenging.

Traditional restaurant websites use basic filters based on amenities, location, or cuisine types, offering users numerous options to sift through. However, as the restaurant industry evolves, there's a growing need for a more personalized approach to restaurant discovery.

This is where restaurant recommendation systems come in. These advanced systems utilize data science, machine learning, and user preferences to provide tailored dining suggestions that align with individual tastes. By going beyond simple filters, they enhance the dining experience, saving time and offering personalized options that traditional methods cannot match.

This project explores the importance, functionality, and impact of restaurant recommendation systems, highlighting how they are transforming the way we discover and enjoy food. By catering to evolving diner preferences, these intelligent algorithms are revolutionizing the art of restaurant selection, offering a glimpse into the future of dining exploration. Join us as we unravel the potential of these systems in reshaping the culinary landscape.

# Problem Statement
This project aims to address the challenge faced by individuals in making informed choices about restaurants and dining experiences by developing a user-friendly restaurant recommendation system that empowers individuals to make informed dining decisions, ultimately enhancing their overall restaurant experience.

# Main Objective

To develop an interactive and user-friendly restaurant recommendation system.

# Specific Objective
1. **Analyze Key Factors Influencing Restaurant Ratings:** 

2. **Develop Content-Based Recommendation Algorithms:** 

3. **Implement filtering techniques to refine recommendations** 

4. **Create an intuitive, responsive web and mobile application.** 

# Data understanding

The data used in this project was sourced from [YELP](https://www.yelp.com/dataset/download), which is publicly available and contains a large number of reviews across various restaurants and locations.  It is a collective dataset of various businesses and user information gotten from Yelp's website. It contains 6,990,280 reviews, 150,346 businesses, 200,100 pictures across 11 metropolitan areas and 19 states and their attributes like hours, parking, availability, and ambience aggregated check-ins over time for each. 

The dataset contains five json files namely:-

> 1. business.json
> 2. checkin.json 
> 3. review.json,
> 4. tips.json
> 5. user.json**

The original data was filtered by concentrating only on restaurant businesses and on reviews made within the year and split into two datasets as shown 
[here](Preliminary_notebook.ipynb).

The two datasets have information on 
> 1. Restaurant Informational Data
> 2. User Review Data

For download of the dataset's, view the [Link](https://www.yelp.com/dataset) and for complete [documentation](https://www.yelp.com/dataset/documentation/main) of all the datasets.


# Exploratory Data Analysis

Conducting a thorough exploratory data analysis (EDA) is pivotal in crafting an interactive and user-friendly restaurant recommendation system. The analysis delved into critical dataset features, examining the distribution of ratings, categories, and restaurants across cities and states, as well as popular restaurants.

Visualizations, including histograms, box plots, and hexbin plots, were employed for a comprehensive understanding. This EDA offered vital insights, identifying key dataset features. 

![Alt text](./Images/res%20by%20state.png)


**Observations**
***

- Pennsylvania (PA), Florida (FL), and Tennessee (TN) have the highest concentrations of restaurants, marking them as key markets in the restaurant industry.

- In contrast, there is a clear decline in the number of restaurants as you move from left to right on the graph. States such as North Carolina (NC), Colorado (CO), Hawaii (HI), and Montana (MT) show incomplete data for these regions.



![Alt text](./Images/open%20vs%20closed.png)

**Observations**
***

- **66.9% Operational Restaurants:** The majority of restaurants in our dataset are currently open, indicating a strong industry presence with many active establishments available for recommendations.

- **33.1% Closed Restaurants:** A significant portion of the restaurants are no longer operational. This information is vital for enhancing our recommendation system by excluding closed restaurants, which will improve both user experience and system accuracy.

**Strategic Recommendations**
***

To ensure the recommendation system remains accurate, it is essential to regularly update and verify the dataset. This will involve removing closed restaurants from the active list to maintain the reliability and relevance of recommendations.


![Alt text](./Images/Review%20Counts%20Over%20Time.png)

**Observations**
***

- **Seasonal Patterns:** There are noticeable peaks in customer engagement from April to July, suggesting increased activity during these months.
- **Engagement Decline:** Reviews tend to drop significantly after July, with particular declines observed in September and December.
- **COVID-19 Impact:** A marked decrease in restaurant reviews was recorded in 2020 due to the COVID-19 pandemic.
# Data Preparation

In this section, we will perform data cleaning to prepare the dataset for analysis, the various data cleaning methods that are to be used will be;

- Renaming columns
- Checking Dealing with missing data
- Checking and removing duplicates 
- Feature Engineering
- Selecting the Relevant Columns
- Dropping Irrelevant columns
- Selecting relevant rows

# Modelling

In this project, we will concentrate on three specific types of recommendation models:

- Content-Based Recommender Systems


- Collaborative Filtering Systems


- Deep Neural Networks


Within each category, we will evaluate and compare different models to determine which performs the best. For validation and comparison, we will use the RMSE (root mean squared error) metric to measure how closely the predictions align with the actual values.We will pickle our desired data for deployment.

# Content-based Recommendation system

Using the cosine similarity matrix, our content-based recommendation system suggests restaurants to users based on the similarity between restaurant names or specified attributes. This involves comparing user preferences with various restaurants and recommending the top similar options to cater to individual tastes.

# Collaborative filtering

In building a collaborative filtering recommendation system with the Surprise library, we selected relevant columns and initialized a Reader object to format the data. Subsequently, we loaded the data into a Surprise Dataset for further analysis and model creation.
The following steps were taken:
Firstly , we modelled a   Normal Predictor  model from the surprise library which was used provided an RMSE of 0.8201. 

Then we tried another model that is Non-Negative Matrix Factorization (NMF) model as it is ideal when ratings are non-negative (i.e, ratings from 1 to 5). The model was able to achieve an RMSE of 0.3479 which was a great improvement on the Normal Predictor.A single value Decomposition (SVD) was used as it works well with explicit feedback (i.e ratings). The model was able to achieve an RMSE of 0.119 which further improved the RMSE. The model was then cross validated and it achieved an RMSE mean of 0.113. Using the GridSearchCv we will tune the SVD model in order to improve the training RMSE scores.

The SVD collaborative filtering model undergoes hyperparameter tuning through grid search and cross-validation. The optimized model achieves an RMSE of approximately 0.0709, signifying good predictive  accuracy. The MAE value is around 0.026, indicating improved prediction accuracy. The best-performing hyperparameter values are as follows:                       
For optimal RMSE, the optimal hyperparameters are 'n_factors' = 20,'reg_all' = 0.01 and 'n_epochs': 40.
  
These results indicate that the SVD collaborative filtering model, when configured with these hyperparameters, provides a relatively low prediction error and is well-suited for making personalized recommendations based on user ratings.

This model was then saved in a pickle file for deployment

# Deep - Neural Networks

A deep neural network was also incoperated in the modeling section, where is user and restaurant embeddings/latent factors were multiplied together to predict the user rating which was then passed into a dense connected layers. The model was tunned and regularized to reduce ovefitting and improve validation RMSE scores. 

# RESULTS AND CONCLUSIONS

# Evaluation

Despite improvements, the DNN’s final RMSE is higher than the SVD model's, suggesting that the SVD model performs better with this dataset and may require less tuning.

We will deploy the optimized SVD.

# Conclusions

In conclusion, this project successfully developed an interactive, user-friendly restaurant recommendation system. It provides personalized dining suggestions by considering factors influencing restaurant ratings and user preferences. The advanced recommendation algorithm enhances user experiences with tailored recommendations.

We met key objectives by creating a user-friendly website for easy interaction with the system and analyzing factors affecting ratings and preferences to refine our algorithms. Additionally, we utilized Folium for geographical data visualization, creating interactive maps that reveal geographic trends in restaurant recommendations. This project has achieved its goals, offering a valuable service that enriches users' dining experiences with personalized and location-based recommendations.


# Future works

a) Expansion of Dataset 

b) Enhanced User Interface and Experience eg:-Augmented Reality (AR), Voice Interaction

c) Integration with Other Services eg:-Reservation Systems

d) Feedback and Continuous Improvement:User Feedback Loops, A/B Testing

e) Expanding Geographical Coverage for Data Collection

# Resources

1: For the complete analysis, here is the [Notebook](https://github.com/AtomHarris/Restaurant-Recommendation-System/blob/main/Final%20Notebook.ipynb)

2: The presentation slides are in this [Link](https://github.com/AtomHarris/Restaurant-Recommendation-System/blob/main/Gourment%20Guros%20refined.pptx)

3: The link to the [data report](https://github.com/AtomHarris/Restaurant-Recommendation-System/blob/main/Gourmet%20Guru%20Project%20Report.docx)



## INSTALLATION AND USAGE
1. Clone the repository
    ```sh
    git clone https://github.com/AtomHarris/Restaurant-Recommendation-System.git
    ```
2. Navigate to the project directory
    ```sh
    cd Restaurant-Recommendation-System
    ```
3. Install dependencies
   ```sh
   pip install -r requirements.txt
    ```
4. Execute the app on streamlit
To run the application, execute:
    ```sh
    streamlit run app.py 
    ```


# CONTRIBUTORS

| Name            | Github                             | Email                                      |
|-----------------|------------------------------------|--------------------------------------------|
| Brian Muthama   | [Github](https://github.com/Muthama42) | [Email](brian.muthama@student.moringaschool.com) |
| Laaria  Chris | [Github](https://github.com/laaria-chris) | [Email](laaria.chris@student.moringaschool.com) |
| Harris Lukundi  | [Github](https://github.com/AtomHarris) | [Email](harris.lukundi@student.moringaschool.com) |
| Beryl Agai   | [Github](https://github.com/Agai-Beryl) | [Email](beryl.agai@student.moringaschool.com) |
| Henry  Rono | [Github](https://github.com/RonoHenry) | [Email](henry.rono@student.moringaschool.com) |
| Lynette Wangari  | [Github](https://github.com/Wangari-web) | [Email](lynette.wangari@student.moringaschool.com) |

