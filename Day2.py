import pandas as pd
import streamlit as st
import pickle
import requests

# API key
a = st.secrets["API_KEY"]

# Caching the fetch_poster function to reduce API calls
@st.cache_data
def fetch_poster(movie_id):
    try:
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={a}')
        response.raise_for_status()
        data = response.json()
        return 'http://image.tmdb.org/t/p/w500' + data['poster_path']
    except requests.RequestException as e:
        st.error(f"Error fetching poster: {e}")
        return 'default_poster_url'  # Add a default poster URL or placeholder

# Recommendation function with caching for optimization
@st.cache_data
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
@st.cache_resource  # Cache the data loading as it's a heavy operation
def load_data():
    movies_list = pickle.load(open('Day_1.pkl', 'rb'))
    movies = pd.DataFrame(movies_list)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return movies, similarity, movies['title'].values

movies, similarity, movies_list = load_data()

# Streamlit UI
st.set_page_config(layout="wide")

# Sidebar Menu
with st.sidebar:
    st.header("Menu")
    option = st.selectbox("Select an Option", ["Home", "About"])

    st.markdown("""
        <style>
        .sidebar .sidebar-content {
            background-color: #F4F4F4;
        }
        </style>
        """, unsafe_allow_html=True)

    if option == "About":
        st.markdown("""
        <h2>About</h2>
        <p>Welcome to the Movie Recommendation System – your ultimate gateway to discovering cinematic gems that suit your tastes perfectly. Our cutting-edge recommendation engine leverages advanced machine learning algorithms to offer you tailored movie suggestions based on your preferences.</p>
        <h3>How It Works</h3>
        <p>Our system analyzes a vast database of movies, considering factors such as genre, ratings, and user reviews to curate a list of recommendations just for you. By inputting your favorite movie, you'll receive a set of personalized suggestions along with high-quality movie posters, ensuring a visually appealing and engaging experience.</p>
        <h3>Features</h3>
        <ul>
            <li>Personalized Recommendations: Receive movie suggestions that match your viewing history and preferences.</li>
            <li>High-Quality Posters: Enjoy detailed movie posters to help you make informed choices.</li>
            <li>User-Friendly Interface: Navigate effortlessly through our intuitive design and interactive elements.</li>
        </ul>
        <h3>Our Mission</h3>
        <p>At the heart of our Movie Recommendation System is the passion for bringing people closer to the films they love. Whether you're seeking a classic blockbuster or an under-the-radar indie gem, our goal is to enhance your movie-watching experience by offering smart, relevant recommendations tailored just for you.</p>
        <h3>Contact Us</h3>
        <p>For any inquiries, feedback, or support, please reach out to us at <a href="https://www.linkedin.com/in/ashutosh-bhat-800470288?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3B70OiPe7xTQqDtH5X%2BnAcvg%3D%3D">LinkedIn</a>. We are committed to continuously improving our service and would love to hear from you.</p>
        <p>Thank you for choosing our Movie Recommendation System. Dive into the world of movies and let us help you find your next favorite film!</p>
        """, unsafe_allow_html=True)

# Custom styles
st.markdown("""
    <style>
    .header {
        font-size: 30px !important;
        color: white;
        text-align: left;
        font-family: 'Arial', sans-serif;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .title {
        font-size: 50px !important;
        color: #FFFC4B;
        text-align: left;
        font-family: 'Arial', sans-serif;
        margin-bottom: 20px;
    }
    .subheader {
        font-size: 20px !important;
        text-align: left;
        margin-bottom: 40px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Home page with movie recommendation functionality
if option == "Home":
    st.markdown('<h1 class="title">Movie Recommendation System</h1>', unsafe_allow_html=True)
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
        st.write("What to Watch?")
