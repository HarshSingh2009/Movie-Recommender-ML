# Importing necessary modules
from movie_recommendation_pipeline import RecommendMovie
from streamlit_option_menu import option_menu
import streamlit as st
import pandas as pd
import pickle

st.set_page_config(page_title='Movie Mood', page_icon='😎')
hide_streamlit_menu = '''
<style>
#MainMenu {
    visibility:hidden;
}
footer {
    visibility:hidden;
}
</style>
'''

# Loading the dataframes and lists from pickle files
movie_info_df = pd.DataFrame.from_dict(pickle.load(open('./pickle files/informative_movies_dict.pkl', 'rb')))
new_df = pd.DataFrame.from_dict(pickle.load(open('./pickle files/movies_dict.pkl', 'rb')))
GENRES_LIST = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Foreign', 'History', 'Horror', 'Music', 'Mystery', 'Romance', 'Science Fiction', 'TV Movie', 'Thriller', 'War', 'Western']

# Creating an instance of the movie recommendation class
movie_recommender = RecommendMovie()

# Defining a function to create some space between the elements
def get_free_space():
    st.text("")
    st.text("")
    st.text("")

# Building the Streamlit app
with st.sidebar:
    # Creating a dropdown menu to select the mode of the app
    selected = option_menu(
        menu_title='Movie Mood 😎',
        options=['Recommend Movies', 'Search Movies']        
    )

# If 'Recommend Movies' mode is selected
if selected == 'Recommend Movies':
    # Creating a title and hiding the Streamlit menu
    st.title('Movie Recommender System : ')
    st.markdown(hide_streamlit_menu, unsafe_allow_html=True)
    selected_movie_name = st.selectbox('Which movie do you want this system to recommend : ', new_df['title'].values)
    recommend_btn = st.button(label='Recommend')

    # If the 'Recommend' button is clicked and a movie is selected
    if recommend_btn and selected_movie_name:
        # Calling the recommend_movies method of the movie recommendation class to get the recommended movies
        recommended_movies_names, recommended_movies_poster_paths =  movie_recommender.recommend_movies(movie=selected_movie_name)
        get_free_space()

        # Displaying the selected movie and its details
        with st.container():
            col1, col2 = st.columns([3, 2])        
            col1.image(movie_recommender.get_poster_path(selected_movie_name), width=350)
            col2.header(selected_movie_name)
            
            overview, genres = movie_recommender.get_selected_movie_description(selected_movie_name)
            with st.expander("Description"):
                col2.write(overview)
            get_free_space()
            get_free_space()
            col2.text(genres)

        # Creating some space between the elements
        get_free_space()
        get_free_space()

        # Displaying the recommended movies
        st.subheader('Movies, you would like to watch too ')
        get_free_space()

        # Slicing it to top 20 movies only from the recommended movies
        recommended_movies_names = recommended_movies_names[:20] if len(recommended_movies_names) > 20 else recommended_movies_names
        recommended_movies_poster_paths = recommended_movies_poster_paths[:20] if len(recommended_movies_poster_paths) > 20 else recommended_movies_poster_paths

        with st.container():
            if len(recommended_movies_names):
                for index, name in enumerate(recommended_movies_names):
                    film_description, film_genres = movie_recommender.get_selected_movie_description(movie_name=name)
                    col1, col2 = st.columns(2)
                    col1.image(recommended_movies_poster_paths[index], width=290)
                    col2.header(name)
                    get_free_space()
                    with st.expander('Overview'):
                        col2.write(film_description)
                    get_free_space()
                    get_free_space()
                    col2.text(film_genres)

    # If the 'Recommend' button is clicked but no movie is selected
    elif recommend_btn and  selected_movie_name == []:
        st.markdown('Please enter something')

# If 'Search Movies' mode is selected
else:
    # Creating a title and hiding the Streamlit menu
    st.title('Search Movies through their Genres')
    st.markdown(hide_streamlit_menu, unsafe_allow_html=True)

    get_free_space()
    st.subheader('Not getting the Movie Name but know it\'s genres,')
    st.subheader('Search here : ')
    get_free_space()
    choices = st.multiselect('', options=GENRES_LIST)
    search_movies = st.button(label='Search Movies')
    if search_movies and choices:
        # Defining recommended movies based on genres based on the choices given by the user
        genres_recommended_movies = movie_recommender.get_movies_based_on_genres(genres_list=choices)
        genres_recommended_movies = genres_recommended_movies[:15] if len(genres_recommended_movies) > 15 else genres_recommended_movies
        genres_recommended_movies_poster_paths = []
        # Running a for loop to get the poster_paths of each movie in genres_recommended_movies
        for genre_movie in genres_recommended_movies:
            if movie_recommender.get_poster_path(genre_movie) != None:
                genres_recommended_movies_poster_paths.append(movie_recommender.get_poster_path(genre_movie))
            else:
                genres_recommended_movies.remove(genre_movie)
                continue
        get_free_space()
        get_free_space()

        # Making the columns to display the recommended movies
        if len(genres_recommended_movies):
            for index, movie in enumerate(genres_recommended_movies):
                c1, c2 = st.columns(2)
                c1.image(genres_recommended_movies_poster_paths[index], width=290)
                movie_description, movie_genres = movie_recommender.get_selected_movie_description(movie)  
                c2.header(movie)
                get_free_space()
                with st.expander('Overview'):
                    c2.write(movie_description)
                get_free_space()
                get_free_space()
                c2.text(movie_genres)
        else:
            st.header('Can\'t find any movies 😞')

    elif search_movies and choices == []:
        st.markdown('Please enter something')

            

        


