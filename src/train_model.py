from pathlib import Path

import pandas as pd

from src.recommender import MovieRecommender


BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"

MODEL_DIR = BASE_DIR / "models"


def main():

    movies_path = DATA_DIR / "cleaned_movies.csv"

    if not movies_path.exists():
        movies_path = DATA_DIR / "movies.csv"

    print("Loading movie dataset...")

    movies = pd.read_csv(movies_path)

    print(f"Movies loaded: {len(movies):,}")

    print("Training TF-IDF recommendation engine...")

    recommender = MovieRecommender()

    recommender.fit(movies)

    print("Training completed.")

    print(
        "TF-IDF matrix shape:",
        recommender.feature_matrix.shape
    )

    print(
        "Number of extracted features:",
        len(recommender.vectorizer.get_feature_names_out())
    )

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    recommender.save(MODEL_DIR)

    print("\nModel saved successfully.")

    print(
        "Artifact:",
        MODEL_DIR / "movie_recommender.joblib"
    )

    print("\nExample recommendations for Toy Story:")

    toy_story = recommender.search_movies(
        "Toy Story",
        limit=10
    )

    print(
        toy_story[
            ["movieId", "title", "genres"]
        ].to_string(index=False)
    )

    if not toy_story.empty:

        movie_id = toy_story.iloc[0]["movieId"]

        recommendations = recommender.recommend(
            movie_id=movie_id,
            top_n=10
        )

        print("\nRecommended movies:")

        print(
            recommendations.to_string(index=False)
        )


if __name__ == "__main__":
    main()
