import pandas as pd
import numpy as np


def clean_movies(movies: pd.DataFrame) -> pd.DataFrame:
    """Clean movie metadata and extract release years."""

    movies = movies.copy()

    # Remove duplicate movie IDs
    movies = movies.drop_duplicates(subset=["movieId"])

    # Remove records without essential fields
    movies = movies.dropna(subset=["movieId", "title"])

    # Standardize text
    movies["title"] = movies["title"].astype(str).str.strip()

    movies["genres"] = (
        movies["genres"]
        .fillna("(no genres listed)")
        .astype(str)
        .str.strip()
    )

    # Extract year from titles such as Toy Story (1995)
    movies["year"] = pd.to_numeric(
        movies["title"].str.extract(r"\((\d{4})\)\s*$")[0],
        errors="coerce"
    )

    # Extract title without the year
    movies["clean_title"] = (
        movies["title"]
        .str.replace(r"\s*\(\d{4}\)\s*$", "", regex=True)
        .str.strip()
    )

    return movies.reset_index(drop=True)


def clean_ratings(ratings: pd.DataFrame) -> pd.DataFrame:
    """Clean user rating data."""

    ratings = ratings.copy()

    # Remove duplicate user-movie ratings
    ratings = ratings.drop_duplicates(
        subset=["userId", "movieId"]
    )

    # Convert rating to numeric
    ratings["rating"] = pd.to_numeric(
        ratings["rating"],
        errors="coerce"
    )

    # Remove missing or invalid ratings
    ratings = ratings.dropna(
        subset=["userId", "movieId", "rating"]
    )

    # MovieLens ratings range from 0.5 to 5.0
    ratings = ratings[
        ratings["rating"].between(0.5, 5.0)
    ]

    return ratings.reset_index(drop=True)


def prepare_datasets(movies, ratings):
    """Clean both datasets and return quality reports."""

    cleaned_movies = clean_movies(movies)
    cleaned_ratings = clean_ratings(ratings)

    # Keep only ratings associated with known movies
    cleaned_ratings = cleaned_ratings[
        cleaned_ratings["movieId"].isin(
            cleaned_movies["movieId"]
        )
    ].reset_index(drop=True)

    # Calculate rating statistics for each movie
    movie_stats = (
        cleaned_ratings
        .groupby("movieId")
        .agg(
            rating_count=("rating", "count"),
            average_rating=("rating", "mean")
        )
        .reset_index()
    )

    cleaned_movies = cleaned_movies.merge(
        movie_stats,
        on="movieId",
        how="left"
    )

    cleaned_movies["rating_count"] = (
        cleaned_movies["rating_count"]
        .fillna(0)
        .astype(int)
    )

    # Movies without ratings remain unrated, not zero-rated
    return cleaned_movies, cleaned_ratings

