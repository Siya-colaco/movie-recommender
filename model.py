import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# load dataset
movies = pd.read_csv("top10K-TMDB-movies.csv")

# keep important columns
movies = movies[['title','overview','genre','original_language','release_date']]

# drop missing values
movies.dropna(inplace=True)

# convert release date to year
movies['year'] = movies['release_date'].astype(str).str[:4].astype(int)

# filter by year
movies = movies[(movies['year'] >= 2015) & (movies['year'] <= 2026)]

# filter by language
movies = movies[(movies['original_language'] == 'en') | (movies['original_language'] == 'hi')]

# combine text for AI
movies['tags'] = movies['overview'] + " " + movies['genre']

# vectorize text
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['tags']).toarray()

# similarity matrix
similarity = cosine_similarity(vectors)

# save files
pickle.dump(movies, open('movies.pkl','wb'))
pickle.dump(similarity, open('similarity.pkl','wb'))

print("✔ Model ready with Hindi + English movies (2015-2026)")