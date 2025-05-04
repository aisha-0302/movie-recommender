



import streamlit as st
from recommender import recommend, fetch_movie_details

# Set up the Streamlit page layout and title
st.set_page_config(page_title="🎬 Movie Recommender", layout="centered")
st.title("🎬 Movie Recommender System")
st.markdown("Enter a movie name and get 5 similar recommendations along with posters and details.")

# Text input to accept the movie name
movie_input = st.text_input("Enter a movie title:")

# Button to trigger movie recommendation
if st.button("🔍Recommend"):
    if movie_input.strip() == "":
        st.warning("Please enter a movie title.")
    else:
        # Fetch movie recommendations and details
        recommendations, matched_title = recommend(movie_input)
        if not recommendations:
            st.error("Movie not found or too different.")
        else:
            # Show results for each recommendation
            st.success(f"Showing recommendations for: **{matched_title}**")
            for rec in recommendations:
                details = fetch_movie_details(rec)
                if details:
                    st.image(details['poster'], width=200)
                    st.markdown(f"**{details['title']} ({details['year']})**")
                    st.markdown(f"🎭 Genre: *{details['genre']}*")
                    st.markdown(f"📝 Plot: {details['plot']}")
                    st.markdown("---")
                else:
                    st.write("👉", rec)
