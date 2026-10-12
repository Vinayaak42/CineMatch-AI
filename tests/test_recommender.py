import pandas as pd

from src.recommender import MovieRecommender


def sample_movies():

    return pd.DataFrame(
        {
            "movieId": [1, 2, 3, 4, 5],

            "title": [
                "Space Adventure (2020)",
                "Galaxy Journey (2021)",
                "Romantic Summer (2022)",
                "Space Adventure 2 (2023)",
                "Funny Friends (2020)"
            ],

            "genres": [
                "Adventure|Science Fiction",
                "Adventure|Science Fiction",
                "Romance|Drama",
                "Adventure|Science Fiction",
                "Comedy"
            ]
        }
    )


def test_model_training():

    recommender = MovieRecommender()

    recommender.fit(sample_movies())

    assert recommender.feature_matrix.shape[0] == 5


def test_recommendations_exclude_selected_movie():

    recommender = MovieRecommender()

    recommender.fit(sample_movies())

    results = recommender.recommend(
        movie_id=1,
        top_n=3
    )

    assert len(results) == 3

    assert 1 not in results["movieId"].tolist()


def test_recommendation_scores_are_valid():

    recommender = MovieRecommender()

    recommender.fit(sample_movies())

    results = recommender.recommend(
        movie_id=1,
        top_n=3
    )

    assert results["similarity_score"].between(0, 1).all()


def test_unknown_movie_returns_empty_results():

    recommender = MovieRecommender()

    recommender.fit(sample_movies())

    results = recommender.recommend(
        movie_id=9999,
        top_n=5
    )

    assert results.empty


def test_title_search():

    recommender = MovieRecommender()

    recommender.fit(sample_movies())

    results = recommender.search_movies("Galaxy")

    assert not results.empty

    assert results.iloc[0]["movieId"] == 2
