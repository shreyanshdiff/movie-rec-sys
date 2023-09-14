import pandas as pd
import streamlit as st
import pickle
import requests
import os

# Function to fetch movie poster
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=34a5f6e371513053bb6b1d48603f4915&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# Function to recommend similar movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = sim[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommend_movies, recommended_movies_poster

# Get the current working directory
current_directory = os.getcwd()

# Construct absolute paths to the data files
movies_dict_path = os.path.join(current_directory, 'movies_dict.pkl')
similarity_path = os.path.join(current_directory, 'similarity.pkl')

# Check if the data files exist
if not os.path.exists(movies_dict_path) or not os.path.exists(similarity_path):
    st.error("One or both of the data files 'movies_dict.pkl' and 'similarity.pkl' not found.")
else:
    # Load data from the absolute paths
    movies_dict = pickle.load(open(movies_dict_path, 'rb'))
    movies = pd.DataFrame(movies_dict)
    sim = pickle.load(open(similarity_path, 'rb'))

    st.title('Movie Recommender System')

    selected_movie_name = st.selectbox(
        'Find Your Movie',
        movies['title'].values)

    if st.button('Recommend'):
        names, posters = recommend(selected_movie_name)

        cols = st.columns(5)
        with cols[0]:
            st.text(names[0])
            st.image(posters[0])
        with cols[1]:
            st.text(names[1])
            st.image(posters[1])
        with cols[2]:
            st.text(names[2])
            st.image(posters[2])
        with cols[3]:
            st.text(names[3])
            st.image(posters[3])
        with cols[4]:
            st.text(names[4])
            st.image(posters[4])
