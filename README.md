# 🎬 CineMatch AI

### Real-Time Movie Discovery and Recommendation System

CineMatch AI is a data science project designed to help users discover movies through interactive search, genre exploration, rating analysis, and machine learning-based recommendations.

## Project Objectives

* Analyze movie metadata and user ratings.
* Explore movie genres and rating patterns.
* Build a content-based recommendation engine.
* Integrate real-time movie metadata through an external API.
* Develop an interactive Streamlit application.
* Evaluate recommendation quality using appropriate ranking metrics.

## Technology Stack

* Python
* Pandas and NumPy
* Scikit-learn
* Streamlit
* Plotly
* SQLite
* TMDB API
* MLflow

## Current Features

* Interactive movie search
* Genre filtering
* Movie and rating statistics
* Dataset exploration
* Rating distribution visualization

## Planned Features

* TF-IDF-based movie recommendations
* Cosine similarity
* Real-time movie metadata and posters
* Personalized recommendations
* User ratings and watchlists
* Hybrid recommendation engine
* MLflow experiment tracking
* Cloud deployment

## Dataset

The initial recommendation experiments use the MovieLens latest-small dataset.

Dataset source: https://grouplens.org/datasets/movielens/

## Run Locally

1. Clone the repository.

2. Create and activate a Python virtual environment.

3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Download and extract the MovieLens dataset.

5. Place `movies.csv` and `ratings.csv` inside the `data/` directory.

6. Launch the application:

   ```bash
   python -m streamlit run app.py
   ```

## Project Status

Phase 1: Project setup and dataset exploration.

Further development will introduce machine learning recommendations, external API integration, personalization, evaluation, and deployment.

## License and Data Attribution

Review the MovieLens dataset terms and the terms of any external API used before redistributing data or deploying the application.

MovieLens: https://grouplens.org/datasets/movielens/

TMDB API: https://developer.themoviedb.org/docs/getting-started
