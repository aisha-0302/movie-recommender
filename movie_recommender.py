import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ast

# Load datasets
movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')

# Merge datasets on ID
movies = movies.merge(credits, left_on='id', right_on='movie_id')

# Keep necessary columns
movies = movies[['title_x', 'genres', 'keywords', 'tagline', 'cast', 'crew']]
movies.columns = ['title', 'genres', 'keywords', 'tagline', 'cast', 'crew']

# Fill missing values
for feature in ['genres', 'keywords', 'tagline', 'cast', 'crew']:
    movies[feature] = movies[feature].fillna('')

# Function to get director from crew
def get_director(text):
    try:
        crew = ast.literal_eval(text)
        for member in crew:
            if member['job'] == 'Director':
                return member['name']
    except:
        pass
    return ''

# Function to get top 3 names from a list field
def get_top_names(text):
    try:
        names = [entry['name'] for entry in ast.literal_eval(text)]
        return " ".join(names[:3])
    except:
        return ''

# Process each field
movies['director'] = movies['crew'].apply(get_director)
movies['cast'] = movies['cast'].apply(get_top_names)
movies['genres'] = movies['genres'].apply(get_top_names)
movies['keywords'] = movies['keywords'].apply(get_top_names)

# Combine all features into one
def combine_features(row):
    return f"{row['genres']} {row['keywords']} {row['tagline']} {row['cast']} {row['director']}"

movies['combined_features'] = movies.apply(combine_features, axis=1)

# Vectorize the text
cv = CountVectorizer(stop_words='english')
count_matrix = cv.fit_transform(movies['combined_features'])

# Compute cosine similarity
cosine_sim = cosine_similarity(count_matrix)

# Get title from index
def get_title_from_index(index):
    return movies.iloc[index]['title']

# Recommend function
def recommend(movie_title):
    movie_title = movie_title.lower()
    matched_movies = movies[movies['title'].str.lower() == movie_title]
    
    if matched_movies.empty:
        return ["Movie not found."]
    
    movie_index = matched_movies.index[0]
    similar_movies = list(enumerate(cosine_sim[movie_index]))
    sorted_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:6]
    
    recommended = [get_title_from_index(i[0]) for i in sorted_movies]
    return recommended

# Main program
if __name__ == "__main__":
    user_input = input("Enter a movie title: ")
    print("\nRecommended Movies:")
    for title in recommend(user_input):
        print("•", title)
