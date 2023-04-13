from movie_recommendation_pipeline import RecommendMovie
from streamlit_option_menu import option_menu
import streamlit as st
import pandas as pd
import pickle

# Customizing the web app
st.set_page_config(page_title='Movie Mingle', page_icon='😎')
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

movie_info_df = pd.DataFrame.from_dict(pickle.load(open('./pickle files/informative_movies_dict.pkl', 'rb')))
new_df = pd.DataFrame.from_dict(pickle.load(open('./pickle files/movies_dict.pkl', 'rb')))
GENRES_LIST = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Foreign', 'History', 'Horror', 'Music', 'Mystery', 'Romance', 'Science Fiction', 'TV Movie', 'Thriller', 'War', 'Western']

movie_recommender = RecommendMovie()

def get_recommended_movie_columns(names, poster_paths):
    col1, col2, col3 = st.columns(3)
    col1.image(poster_paths[0])
    col1.text(names[0])
    col2.image(poster_paths[1])
    col2.text(names[1])
    col3.image(poster_paths[2])
    col3.text(names[2])
    get_free_space()
    c4, c5, c6 = st.columns(3)
    c4.image(poster_paths[3])
    c4.text(names[3])
    c5.image(poster_paths[4])
    c5.text(names[4])
    c6.image(poster_paths[5])
    c6.text(names[5])

def get_free_space():
    st.text("")
    st.text("")
    st.text("")
## App building 

with st.sidebar:
    selected = option_menu(
        menu_title='Toggle Options',
        options=['Recommend Movies', 'Search Movies']        
    )

if selected == 'Recommend Movies':
    st.title('Movie Recommender System : ')
    st.markdown(hide_streamlit_menu, unsafe_allow_html=True)

    selected_movie_name = st.selectbox('Which movie do you want this system to recommend : ', new_df['title'].values)
    recommend_btn = st.button(label='Recommend')

    if recommend_btn and selected_movie_name:
        names, poster_paths =  movie_recommender.recommend_movies(movie=selected_movie_name)
        get_free_space()
        with st.container():
            col1, col2 = st.columns([2, 3])        
            col1.image(movie_recommender.get_poster_path(selected_movie_name), width=250)
            col2.header(selected_movie_name)
            overview, genres = movie_recommender.get_selected_movie_description(selected_movie_name)
            with st.expander("Description"):
                col2.write(overview)
            get_free_space()
            get_free_space()
            col2.text(genres)

        get_free_space()
        get_free_space()

        st.subheader('Movies, you would like to watch too ')
        get_free_space()
            
        with st.container():
            get_recommended_movie_columns(names=names, poster_paths=poster_paths)
    elif recommend_btn and  selected_movie_name == []:
        st.markdown('Please enter something')

else:
    st.title('Search Movies through their Genres')
    st.markdown(hide_streamlit_menu, unsafe_allow_html=True)
    get_free_space()
    st.subheader('Not getting the Movie Name but know it\'s genres,')
    st.subheader('Search here : ')
    get_free_space()
    choices = st.multiselect('Enter Genres', options=GENRES_LIST)
    search_movies = st.button(label='Search Movies')
    if search_movies and choices:
        genres_recommended_movies = movie_recommender.get_movies_based_on_genres(genres_list=choices)
        genres_recommended_movies = genres_recommended_movies[:15] if len(genres_recommended_movies) > 15 else genres_recommended_movies
        genres_recommended_movies_poster_paths = []
        for genre_movie in genres_recommended_movies:
            if movie_recommender.get_poster_path(genre_movie) != None:
                genres_recommended_movies_poster_paths.append(movie_recommender.get_poster_path(genre_movie))
            else:
                genres_recommended_movies.remove(genre_movie)
                continue
        get_free_space()
        get_free_space()

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

            

        


