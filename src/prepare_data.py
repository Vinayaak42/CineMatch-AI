from pathlib import Path

import pandas as pd

from src.preprocessing import prepare_datasets


BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"

movies_path = DATA_DIR / "movies.csv"
ratings_path = DATA_DIR / "ratings.csv"


def main():

    movies = pd.read_csv(movies_path)

    ratings = pd.read_csv(ratings_path)

    cleaned_movies, cleaned_ratings = prepare_datasets(
        movies,
        ratings
    )

    cleaned_movies.to_csv(
        DATA_DIR / "cleaned_movies.csv",
        index=False
    )

    cleaned_ratings.to_csv(
        DATA_DIR / "cleaned_ratings.csv",
        index=False
    )

    print("Data preparation completed.")

    print(f"Cleaned movies: {len(cleaned_movies):,}")

    print(f"Cleaned ratings: {len(cleaned_ratings):,}")

    print(
        "Saved:",
        DATA_DIR / "cleaned_movies.csv"
    )

    print(
        "Saved:",
        DATA_DIR / "cleaned_ratings.csv"
    )


if __name__ == "__main__":
    main()
