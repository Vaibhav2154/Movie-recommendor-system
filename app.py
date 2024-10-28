import streamlit as st
import pickle
import pandas as pd


# Load data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))


# Define recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movies_list:
        movie_id = i[0]
        recommended_movies.append({
            'title': movies.iloc[i[0]].title
        })

    return recommended_movies

# Set background image using CSS
background_image_url = "https://duckduckgo.com/?q=movie+wallpaper+collage+4k&t=ffab&iar=images&iax=images&ia=images&iai=https%3A%2F%2Fwallpapercave.com%2Fwp%2Fwp9011504.jpg"  # Replace with your image URL
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{background_image_url}");
        background-attachment: fixed;
        background-size: cover;
        background-position: center;
        opacity: 0.8;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
# UI Layout
st.title('🎬 Movie Recommender System')
st.write("Get personalized movie recommendations by selecting a movie you love!")

# Movie Selection
selected_movie_name = st.selectbox(
    'Choose a movie you like:',
    movies['title'].values,
    help="Select a movie to get similar movie recommendations"
)

if st.button('Recommend 🎉'):
    # Recommendations display
    with st.spinner('Fetching recommendations...'):
        try:
            recommendations = recommend(selected_movie_name)
            st.subheader(f"Because you liked **{selected_movie_name}**:")

            # Display each recommendation with title, genre, and rating
            for movie in recommendations:
                with st.container():
                    st.markdown(f"**🎬 {movie['title']}**")


        except IndexError:
            st.error("Sorry, we couldn't find recommendations for this movie.")

st.markdown("#### Powered by Vaibhav M N ", unsafe_allow_html=True)
