import pandas as pd
import plotly.express as px


def get_genre_counts(movies):
    """Count movies belonging to each genre."""

    genres = (
        movies["genres"]
        .dropna()
        .str.split("|")
        .explode()
    )

    genres = genres[
        ~genres.isin([
            "(no genres listed)",
            ""
        ])
    ]

    return (
        genres
        .value_counts()
        .rename_axis("Genre")
        .reset_index(name="Movie Count")
    )


def get_rating_distribution(ratings):
    """Count ratings at each rating level."""

    return (
        ratings["rating"]
        .value_counts()
        .sort_index()
        .rename_axis("Rating")
        .reset_index(name="Number of Ratings")
    )


def get_top_rated_movies(movies, min_ratings=20, top_n=10):
    """
    Find top-rated movies using a minimum rating-count threshold.

    The threshold helps avoid ranking movies based on
    very small numbers of ratings.
    """

    eligible = movies[
        (movies["rating_count"] >= min_ratings)
        & (movies["average_rating"].notna())
    ]

    return (
        eligible
        .sort_values(
            ["average_rating", "rating_count"],
            ascending=[False, False]
        )
        .head(top_n)
    )


def get_most_rated_movies(movies, top_n=10):
    """Find movies with the highest number of ratings."""

    return (
        movies[
            movies["rating_count"] > 0
        ]
        .sort_values(
            ["rating_count", "average_rating"],
            ascending=[False, False]
        )
        .head(top_n)
    )


def get_year_distribution(movies):
    """Count movies released each year."""

    valid_years = movies.dropna(subset=["year"])

    return (
        valid_years
        .groupby("year")
        .size()
        .reset_index(name="Movie Count")
        .sort_values("year")
    )


def create_genre_chart(genre_counts):
    return px.bar(
        genre_counts.head(15).sort_values("Movie Count"),
        x="Movie Count",
        y="Genre",
        orientation="h",
        title="Movies by Genre",
        template="plotly_dark"
    )


def create_rating_chart(rating_distribution):
    return px.bar(
        rating_distribution,
        x="Rating",
        y="Number of Ratings",
        title="User Rating Distribution",
        template="plotly_dark"
    )


def create_year_chart(year_distribution):
    return px.line(
        year_distribution,
        x="year",
        y="Movie Count",
        markers=True,
        title="Movies Released Over Time",
        template="plotly_dark"
    )
