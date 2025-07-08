import pandas as pd
import random

# Load your CSV file
df = pd.read_csv("songsDataSet.csv", encoding="utf-8")

# Strip whitespace from column names only
df.columns = df.columns.str.strip()

# Clean only 'mood' and 'genre' columns for matching (keep 'track_id' untouched)
df['mood'] = df['mood'].str.strip().str.lower()
df['genre'] = df['genre'].str.strip().str.lower()


def get_recommendation(mood, genre):
    # Filter for rows matching the mood and genre
    match = df[(df['mood'] == mood.strip().lower()) &
               (df['genre'] == genre.strip().lower())]

    if match.empty:
        return None

    # Randomly choose one track from the matches
    track_id = random.choice(match['track_id'].tolist())

    # Generate Spotify embed HTML for that track
    embed_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Spotify Track Embed</title>
  <style>
    body {{
      margin: 0;
      padding: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      background-color: #000000;
    }}
    iframe {{
      border-radius: 12px;
      box-shadow: 0 0 10px rgba(0,0,0,0.2);
    }}
  </style>
</head>
<body>
  <iframe 
    src="https://open.spotify.com/embed/track/{track_id}?utm_source=generator"
    width="100%" 
    height="352" 
    frameborder="0" 
    allowfullscreen 
    allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
    loading="lazy">
  </iframe>
</body>
</html>"""

    return embed_html