import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process
import requests
import streamlit as st

# Load your OMDb API key from secrets.toml
OMDB_API_KEY = st.secrets["OMDB_API_KEY"]

# Load and merge datasets
movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')
movies = movies.merge(credits, left_on='id', right_on='movie_id')

# Select and rename relevant columns
movies = movies[['title_x', 'genres', 'keywords', 'tagline', 'cast', 'crew']]
movies.columns = ['title', 'genres', 'keywords', 'tagline', 'cast', 'crew']

# Fill missing values
for col in ['genres', 'keywords', 'tagline', 'cast', 'crew']:
    movies[col] = movies[col].fillna('')

# Helper function to extract director
def get_director(text):
    try:
        crew = ast.literal_eval(text)
        for member in crew:
            if member['job'] == 'Director':
                return member['name']
    except:
        return ''
    return ''

# Helper function to get top names (cast, genres, keywords)
def get_top_names(text):
    try:
        return " ".join([entry['name'] for entry in ast.literal_eval(text)][:3])
    except:
        return ''

# Apply extraction functions
movies['director'] = movies['crew'].apply(get_director)
movies['cast'] = movies['cast'].apply(get_top_names)
movies['genres'] = movies['genres'].apply(get_top_names)
movies['keywords'] = movies['keywords'].apply(get_top_names)

# Combine features into a single string
def combine_features(row):
    return f"{row['genres']} {row['keywords']} {row['tagline']} {row['cast']} {row['director']}"

movies['combined_features'] = movies.apply(combine_features, axis=1)

# Vectorize features and calculate similarity
cv = CountVectorizer(stop_words='english')
matrix = cv.fit_transform(movies['combined_features'])
similarity = cosine_similarity(matrix)

# Match user input with closest movie title using fuzzy matching
def match_title(user_input):
    titles = movies['title'].tolist()
    match = process.extractOne(user_input, titles)
    return match[0] if match and match[1] > 70 else None

# Recommend top 5 similar movies
def recommend(title):
    matched = match_title(title)
    if not matched:
        return [], "No close match found."
    index = movies[movies['title'] == matched].index[0]
    distances = list(enumerate(similarity[index]))
    sorted_distances = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]
    recommended = [movies.iloc[i[0]].title for i in sorted_distances]
    return recommended, matched

# Fetch movie details from OMDb API
def fetch_movie_details(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    try:
        res = requests.get(url)
        data = res.json()
        if data['Response'] == 'True':
            return {
                'title': data.get('Title'),
                'poster': data.get('Poster'),
                'year': data.get('Year'),
                'genre': data.get('Genre'),
                'plot': data.get('Plot')
            }
    except:
        return None
    return None
