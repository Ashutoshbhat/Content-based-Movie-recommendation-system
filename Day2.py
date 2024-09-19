import pandas as pd
import streamlit as st
import pickle
import requests

# API key
a = st.secrets["API_KEY"]

@st.cache
def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={a}')
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

# Sidebar Menu
with st.sidebar:
    st.header("Menu")
    st.selectbox("Select an Option", ["Home", "Recommendations", "About"])

    st.markdown("""
        <style>
        .sidebar .sidebar-content {
            background-color: #F4F4F4;
        }
        </style>
        """, unsafe_allow_html=True)

# Custom styles
st.markdown("""
    <style>
    .header {
        font-size: 30px !important;
        color: white;
        text-align: center;
        font-family: 'Arial', sans-serif;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .title {
        font-size: 50px !important;
        color: #FFFC4B;
        text-align: center;
        font-family: 'Arial', sans-serif;
        margin-bottom: 20px;
    }
    .subheader {
        font-size: 20px !important;
        text-align: center;
        margin-bottom: 40px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="title">Movie Recommendation System by Ashutosh Bhat</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="subheader">Discover your favourite movie</h2>', unsafe_allow_html=True)

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
if st.session_state.recommendations:
    cols = st.columns(5)
    for i in range(min(5, len(st.session_state.recommendations))):
        with cols[i]:
            st.text(st.session_state.recommendations[i])
            st.image(st.session_state.posters[i], use_column_width=True)
else:
    st.write("No recommendations available.")
