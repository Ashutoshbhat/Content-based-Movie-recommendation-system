import pandas as pd
import streamlit as st
import pickle
import requests
from streamlit-star-rating-component import st_star_rating

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=1277338b2607071c2fcef117cd53cf3e&language=en-US')
    data = response.json()
    return 'http://image.tmdb.org/t/p/w500' + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommend_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_posters.append(fetch_poster(movie_id))

    return recommend_movies, recommend_movies_posters

# Load the movie data and similarity matrix
movies_list = pickle.load(open('Day_1.pkl', 'rb'))
movies = pd.DataFrame(movies_list)
movies_list = movies['title'].values

similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.set_page_config(layout="wide")
st.markdown("""
    <style>
    .big-font {
        font-size:50px !important;
        color: #FF6347; 
        font-family: 'Arial', sans-serif;
    }
    .sidebar .sidebar-content {
        background-color: #F4F4F4;
    }
    </style>
    """, unsafe_allow_html=True)
st.title("Movie Recommendation System by Ashutosh Bhat")
st.subheader("Discover your favourite movie")

# Initialize session state for recommendations and posters
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []
    st.session_state.posters = []

# Handle movie selection and recommendation
selected_movie_name = st.selectbox('Search movie Name', movies_list)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    st.session_state.recommendations = names
    st.session_state.posters = posters

# Display recommendations
cols = st.columns(5)
for i in range(min(5, len(st.session_state.recommendations))):
    with cols[i]:
        st.text(st.session_state.recommendations[i])
        st.image(st.session_state.posters[i])

# Rating section
rating = st_star_rating(label="Review Us:", maxValue=5, defaultValue=0,)
sentiment_mapping = ["one", "two", "three", "four", "five"]

if rating:
    st.markdown(f"You rated us {sentiment_mapping[rating - 1]} star(s).")
