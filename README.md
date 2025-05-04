# 🎬 Movie Recommender System

A content-based movie recommender system built with Streamlit and TMDb/OMDb data.

## Features
- Recommend 5 similar movies based on user input
- Fuzzy matching for movie names
- Movie details and posters from OMDb API

## Setup
1. Clone this repo
2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
3. Add your OMDb API key to `.streamlit/secrets.toml`
4. Run the app:
    ```
    streamlit run app.py
    ```

## Data
- Uses `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` from Kaggle.
