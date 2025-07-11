import streamlit as st
from MoodClassifier import predict_mood
from recommender import get_recommendation
import os
import webbrowser

# Set page title and icon
st.set_page_config(page_title="GrooveIn", page_icon="★", layout="centered")

# App Title & Description
st.title("GrooveIn")
st.markdown("Tell us how you feel and pick a genre and we will recommend music that matches your vibe.")

# Input Section
user_input = st.text_area("How are you feeling today?", placeholder="E.g., I'm feeling sad but calm.")
genre_options = ["pop", "rock", "indie", "hiphop", "jazz", "bollywood", "rnb"]
selected_genre = st.selectbox("What genre do you want to listen to?", genre_options)

if st.button("Recommend"):
    if not user_input.strip():
        st.warning("Please describe your mood first!")
    else:
        # Step 1: Predict mood
        mood = predict_mood(user_input)
        st.success(f"Detected Mood: **{mood.capitalize()}**")

        # Step 2: Get recommendation
        embed_html = get_recommendation(mood, selected_genre)

        if embed_html:
            st.markdown("Song recommended for you:")

            # Save HTML file
            html_file = "recommendation.html"
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(embed_html)

            # Optional: Show player inside Streamlit too
            st.components.v1.html(embed_html, height=400)

        else:
            st.error("No song found for this mood and genre.")
