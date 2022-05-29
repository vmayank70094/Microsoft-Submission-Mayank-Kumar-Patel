import streamlit as st
import json
import requests

st.set_page_config(page_title='Movieflex++', page_icon=':smiley:', )

hide_menu_style ="""
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

from streamlit_option_menu import option_menu

with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Movie Recommendation","Guidline for user"], 
        icons=["house", "film", "book"], 
        menu_icon="cast", 
        default_index=0, 
        orientation="horizontal",
        styles={
                "container": {"padding": "0!important", "background-color": "#564d4d"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {
                    "font-size": "25px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "#E35335"},
            },
    )

from streamlit_lottie import st_lottie

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()

lottie_hello = load_lottiefile("lottiefiles/hello.json")


if selected == "Home":

    st.title('Movieflex++')
    st.header("Hello peeps! Let's have movie time")
    st_lottie(
        lottie_hello,
        speed=1,
        reverse=False,
        loop=True,
        quality="low",
        height=None,
        width=None,
        key=None,
   )

if selected == "Movie Recommendation":
    from KNN_classifier import KNearestNeighbors
    from operator import itemgetter

    with open(r'movie_data.json', 'r+', encoding='utf-8') as f:
        data = json.load(f)
    with open(r'movie_titles.json', 'r+', encoding='utf-8') as f:
        movie_titles = json.load(f)

    def knn_algo(test_point, k):

    
        target = [0 for item in movie_titles]
        model = KNearestNeighbors(data, target, test_point, k=k)
        model.fit()
        max_dist = sorted(model.distances, key=itemgetter(0))[-1]
        table = list()
        for i in model.indices:
        
            table.append([movie_titles[i][0], movie_titles[i][2]])
        return table

    if __name__ == '__main__':
        genres_list = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
                    'Fantasy', 'Film-Noir', 'Game-Show', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News',
                    'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Thriller', 'War', 'Western']


    movies = [title[0] for title in movie_titles]
    st.header('Movie Recommendation System') 
    
    apps = ['--Select--', 'Genres based','Movie based']   
    app_options = st.selectbox('Select mode of recommendation:', apps)
    
    if app_options == 'Movie based':
        movie_select = st.selectbox('Select a movie of your choice:', ['--Select--'] + movies)
        if movie_select == '--Select--':
            st.write('Select a movie')
        else:
            n = st.number_input('Add number of movies you want to see (maximum limit - 30):', min_value=5, max_value=20, step=1)
            genres = data[movies.index(movie_select)]
            test_point = genres
            table = knn_algo(test_point, n)
            for movie, link in table:
                # Displays movie title with link to imdb
                st.markdown(f"[{movie}]({link})")
    elif app_options == apps[1]:
        options = st.multiselect('Select genres:', genres_list)
        if options:
            imdb_score = st.slider('IMDb score:', 1, 10, 5)
            n = st.number_input('Add number of movies you want to see (maximum limit - 20):', min_value=5, max_value=20, step=1)
            test_point = [1 if genre in options else 0 for genre in genres_list]
            test_point.append(imdb_score)
            table = knn_algo(test_point, n)
            for movie, link in table:
                st.markdown(f"[{movie}]({link})")

        else:
                st.write("Please select the genres and change the IMDb score as your wish to get movies recommendation.")

    else:
        st.write('Select option')

if selected == "Guidline for user":
    st.header("Guidline to use Movie recommendation system")
    st.write("  Their are two modes of selection for movie recommendation")
    st.write("1.Genres Based - Here you have to select the genres and the IMDb rating, and based on that, you will get movie recommendations.")
    st.write("2.Movie Based - Here you have to select any movie, and you will get movie recommendation similar to the movie you have chosen.")
    st.write("There is a link attached to those movie names, which was recommended to you, which will redirect you to the IMDb website when you click on the name of that movie. ")
