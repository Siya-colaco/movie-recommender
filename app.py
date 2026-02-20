import streamlit as st
import pandas as pd

# -------------------------
# PAGE SETTINGS
# -------------------------
st.set_page_config(page_title="Movie Recommendation", page_icon="🎬", layout="wide")

# -------------------------
# NETFLIX STYLE CSS (UNCHANGED)
# -------------------------
st.markdown("""
<style>
html, body { background-color: #141414 !important; }
.stApp { background-color: #141414 !important; }
section[data-testid="stAppViewContainer"] { background-color: #141414 !important; }
.block-container { background-color: #141414 !important; }

.header-box {
    background: linear-gradient(90deg, #E50914, #b20710);
    padding: 22px;
    border-radius: 14px;
    text-align: center;
    margin-bottom: 25px;
    box-shadow: 0 0 25px rgba(229,9,20,0.7);
}

.header-box h1 {
    color: white;
    font-size: 46px;
    margin: 0;
}

label, .stMarkdown, .stText { color: white !important; }

.stButton>button {
    background-color: #E50914;
    color: white;
    border-radius: 10px;
    height: 50px;
    width: 240px;
    font-size: 18px;
    border: none;
}

.movie-card {
    background: #1f1f1f;
    padding: 18px;
    border-radius: 12px;
    text-align: center;
    font-size: 18px;
    color: white;
    margin: 10px;
}
/* RADIO BUTTON TEXT BLACK */
div[role="radiogroup"] label {
    color: white !important;
    font-weight: 600;
}

/* Also make the heading black if needed */
.stRadio label p {
    color: white
     !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# HEADER
# -------------------------
st.markdown(
    '<div class="header-box"><h1>🎬 Movie Recommendation platform</h1></div>',
    unsafe_allow_html=True
)

# -------------------------
# LOAD DATA
# -------------------------
try:
    movies = pd.read_csv("top10K-TMDB-movies.csv")
except:
    st.error("CSV file not found. Put it in project folder.")
    st.stop()

if "title" not in movies.columns:
    st.error("Dataset must contain a 'title' column.")
    st.stop()

# -------------------------
# FILTER INDUSTRY
# -------------------------
industry = st.radio(
    "Select Industry",
    ["Both", "Bollywood", "Hollywood"]
)

# Language filtering logic
if "original_language" in movies.columns:

    if industry == "Bollywood":
        movies = movies[movies["original_language"] == "hi"]

    elif industry == "Hollywood":
        movies = movies[movies["original_language"] == "en"]

    else:
        movies = movies[movies["original_language"].isin(["hi","en"])]

# Sort by popularity if exists
if "popularity" in movies.columns:
    movies = movies.sort_values(by="popularity", ascending=False)

movies = movies.dropna(subset=["title"])

# -------------------------
# SELECT MOVIE
# -------------------------
selected_movie = st.selectbox(
    "Choose a movie you like",
    sorted(movies["title"].unique())
)

# -------------------------
# RECOMMENDER
# -------------------------
def recommend(movie):
    filtered = movies[movies["title"] != movie]

    if "popularity" in filtered.columns:
        return filtered.head(9)["title"].values
    else:
        return filtered.sample(min(9, len(filtered)))["title"].values

# -------------------------
# BUTTON
# -------------------------
if st.button("Show Recommendations"):

    st.subheader("🎥 Recommended Movies")

    recommendations = recommend(selected_movie)

    cols = st.columns(3)

    for i, r in enumerate(recommendations):
        with cols[i % 3]:
            st.markdown(
                f'<div class="movie-card">🎬 {r}</div>',
                unsafe_allow_html=True
            )