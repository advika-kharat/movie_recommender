import streamlit as st
import pickle
import pandas as pd
import requests
from annotated_text import annotated_text

movies_df = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies_df['title'].values
similarity = pickle.load(open('similarity.pkl', 'rb'))

placeholder_image = "https://via.placeholder.com/150/CCCCCC/FFFFFF/?text=Image+Not+Available"


def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?language=en-US'

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4NDJjMDRiZmYwNzg3MjZlNmI3Njk2ZGFjZDhkMDlhZCIsInN1YiI6IjY2NmRiY2EwNDIyNTQ0MmZjYzMwOWJhOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.JEAmsLKQsNLYC6kYPDk7d0yzMkSGnfaR1V3cu79H2n4"
    }

    response = requests.get(url, headers=headers)

    data = response.json()

    return "https://image.tmdb.org/t/p/w500" + data['poster_path'] if data['poster_path'] else None


def fetch_movie_details(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?language=en-US'

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4NDJjMDRiZmYwNzg3MjZlNmI3Njk2ZGFjZDhkMDlhZCIsInN1YiI6IjY2NmRiY2EwNDIyNTQ0MmZjYzMwOWJhOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.JEAmsLKQsNLYC6kYPDk7d0yzMkSGnfaR1V3cu79H2n4"
    }

    response = requests.get(url, headers=headers)

    data = response.json()

    overview = data['overview']
    genres = data['genres']

    return overview, genres


def recommend(movie, movie_df, similarity_matrix):
    movie_index = movie_df[movie_df['title'] == movie].index[0]
    distances = similarity_matrix[movie_index]
    indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])
    selected_movie_indices = indices[0]
    movie_indices = indices[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    overviews = []
    genres = []
    for i in movie_indices:
        movie_id = movie_df.iloc[i[0]].movie_id
        recommended_movies.append(movie_df.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
        o, g = fetch_movie_details(movie_id)
        overviews.append(o)
        genres.append(g)

    return recommended_movies, recommended_movies_posters, selected_movie_indices, overviews, genres


st.title('recommended by advika :heartpulse:️')

selected_movie_name = st.selectbox(
    "choose a movie",
    movies_list)

if st.button("recommend"):
    st.text(f'if you like {selected_movie_name}')

    names, posters, selected_movie_index, overviews, genres = recommend(selected_movie_name, movies_df, similarity)

    with st.container():
        selected_movie_id = movies_df.iloc[selected_movie_index[0]].movie_id
        cols = st.columns([1, 2])

        with cols[0]:
            if not selected_movie_id:
                st.image(placeholder_image)
            else:
                st.image(fetch_poster(selected_movie_id))

        with cols[1]:
            over, genre = fetch_movie_details(selected_movie_id)
            st.markdown(over)
            for i in genre:
                st.caption(i['name'])

    st.text("you should checkout")

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            if not posters[i]:
                st.image(placeholder_image)
            else:
                st.image(posters[i])
            with st.popover(names[i], use_container_width=True):
                st.markdown(overviews[i])
                for i in genres[i]:
                    st.caption(i['name'])
