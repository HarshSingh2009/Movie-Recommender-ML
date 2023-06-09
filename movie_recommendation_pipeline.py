# Import necessary libraries
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
import pickle
import pandas as pd
import requests
import os

# Load data from pickle files
movie_info_df = pd.DataFrame.from_dict(pickle.load(open('./pickle files/informative_movies_dict.pkl', 'rb')))
new_df = pd.DataFrame.from_dict(pickle.load(open('./pickle files/movies_dict.pkl', 'rb')))

# Define constants
# Load API key from environment variable
if os.getenv('auth_token') != None:
    API_KEY = os.getenv('auth_token')
else:
    API_KEY = st.secrets['secrets']["auth_token"]

GENRES_LIST = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Foreign', 'History', 'Horror', 'Music', 'Mystery', 'Romance', 'Science Fiction', 'TV Movie', 'Thriller', 'War', 'Western']

# Initialize count vectorizer and calculate cosine similarity matrix
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()
similarity = cosine_similarity(vectors)

# Create class to recommend movies
class RecommendMovie():
    def __init__(self) -> None:
        # Load data into class variables
        global movie_info_df, new_df
        self.df = new_df
        self.info_df = movie_info_df
    
    def recommend_movies(self, movie):
        '''Returns recommended movies based on the movie name given '''
        # Find movie index and calculate similarity scores
        global similarity
        movie_index = self.df[self.df['title'] == movie].index[0]
        movie_similarity = similarity[movie_index]
        # Sort movies by similarity score and select top 6
        self.movies = sorted(list(enumerate(movie_similarity)), reverse=True, key=lambda x:x[1])[1:7]
        recommended_movies = []
        posters = []
        # Retrieve poster path for recommended movies
        for movie in self.movies:
            movie_id = self.df['movie_id'][movie[0]]
            response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US')
            data = response.json()
            if data['poster_path'] is not None:
                posters.append('http://image.tmdb.org/t/p/w500' + data['poster_path'])
            else:
                posters.append('https://previews.123rf.com/images/urfandadashov/urfandadashov1806/urfandadashov180601827/150417827-photo-not-available-vector-icon-isolated-on-transparent-background-photo-not-available-logo-concept.jpg')
            recommended_movies.append(self.df['title'][movie[0]])
        return recommended_movies, posters
    
    def get_poster_path(self, film):
        '''Returns the movie's poster path based on the tmdb api'''
        # Find movie index and retrieve poster path
        film_index = self.df[self.df['title'] == film].index[0]
        film_id = self.df['movie_id'][film_index]
        response = requests.get(f'https://api.themoviedb.org/3/movie/{film_id}?api_key={API_KEY}&language=en-US')
        data = response.json()
        if data['poster_path'] is not None:
            return 'http://image.tmdb.org/t/p/w500' + data['poster_path']
        return 'https://previews.123rf.com/images/urfandadashov/urfandadashov1806/urfandadashov180601827/150417827-photo-not-available-vector-icon-isolated-on-transparent-background-photo-not-available-logo-concept.jpg'


    def get_selected_movie_description(self, movie_name):
        '''returns the selected movie's description'''
        movie_index = self.df[self.df['title'] == movie_name].index[0]
        movie_overview = self.info_df['overview'][movie_index]
        genres = self.info_df['genres'][movie_index]
        if len(movie_overview) < 60:movie_overview = movie_overview
        else:
            movie_overview = movie_overview[:60]
            movie_overview.append('.....')
        return ' '.join(movie_overview), ', '.join(genres) 
    
    def get_movies_based_on_genres(self, genres_list):
        '''returns list of movies that have the same genres given in the parameter genres_list'''
        genres_recommended_movies = []
        for movie in self.info_df['title']:
            movie_index = self.info_df[self.info_df['title'] == movie].index[0]
            # Finding Movie genres
            movie_genres = self.info_df['genres'][movie_index]
            total_math_percentage = 0.0
            for movie_genres in movie_genres:
                match_count = 0
                for selected_genre in genres_list:
                    if selected_genre in movie_genres:
                        match_count += 1
                total_math_percentage +=  match_count / len(genres_list)
            # Seeing if the total match is more than 60%
            if total_math_percentage >= 0.8:
                genres_recommended_movies.append(movie)
        return genres_recommended_movies
