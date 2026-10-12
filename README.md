# CineMatch AI

An AI-powered movie recommendation platform built with Python,
Streamlit, scikit-learn, MovieLens, and TMDB.

## Features

- Content-based movie recommendations
- TF-IDF text feature extraction
- Cosine similarity
- Movie search and filtering
- TMDB movie information and posters
- Movie data analytics
- User profiles and ratings
- Personalized recommendations
- Watchlist management

## Technology Stack

- Python
- Pandas and NumPy
- Scikit-learn
- Streamlit
- SQLite
- TMDB API
- Git and GitHub

## Recommendation Approach

Movie titles and genres are transformed into TF-IDF feature vectors.
Cosine similarity is used to identify movies with similar content.

## Installation

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies from requirements.txt.
4. Download the MovieLens dataset.
5. Configure TMDB credentials in a local .env file.
6. Run the application using Streamlit.

## Run the Application

python -m streamlit run app.py

## Limitations

- Recommendations depend on movie metadata.
- Personalized suggestions improve as users provide ratings.
- TMDB features require valid API credentials.
- Local SQLite data requires persistent storage for reliable
  long-term user profiles.

## Future Improvements

- MLflow experiment tracking
- Model evaluation and versioning
- Collaborative filtering
- Automated testing and CI/CD
- Persistent cloud database
- Production monitoring
