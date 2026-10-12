import pandas as pd


def generate_personalized_recommendations(
    recommender,
    user_ratings,
    watchlist,
    top_n=10,
):
    """
    Generate personalized recommendations using the user's
    rating history and the existing content-based recommender.

    Rating preference:
        High rating -> positive preference
        Low rating  -> negative preference

    This is a content-based personalization strategy, not
    collaborative filtering between different users.
    """

    if not user_ratings:
        return pd.DataFrame(
            columns=[
                "movieId",
                "title",
                "genres",
                "personalized_score",
            ]
        )

    model_movies = recommender.movies.copy()

    if model_movies.empty or "movieId" not in model_movies.columns:
        return pd.DataFrame()

    rating_df = pd.DataFrame(user_ratings)

    if rating_df.empty:
        return pd.DataFrame()

    rating_df["movie_id"] = pd.to_numeric(
        rating_df["movie_id"],
        errors="coerce",
    )

    rating_df["rating"] = pd.to_numeric(
        rating_df["rating"],
        errors="coerce",
    )

    rating_df = rating_df.dropna(
        subset=["movie_id", "rating"]
    )

    if rating_df.empty:
        return pd.DataFrame()

    rating_df["movie_id"] = rating_df["movie_id"].astype(int)

    known_movie_ids = set(
        pd.to_numeric(
            model_movies["movieId"],
            errors="coerce",
        ).dropna().astype(int)
    )

    rating_df = rating_df[
        rating_df["movie_id"].isin(known_movie_ids)
    ]

    if rating_df.empty:
        return pd.DataFrame()

    rated_ids = set(rating_df["movie_id"].tolist())

    watchlist_ids = {
        int(item["movie_id"])
        for item in watchlist
        if item.get("movie_id") is not None
    }

    excluded_ids = rated_ids | watchlist_ids

    # Center ratings around 3.0:
    # 5.0 -> +2.0
    # 4.0 -> +1.0
    # 3.0 ->  0.0
    # 2.0 -> -1.0
    # 1.0 -> -2.0

    scores = {}

    for row in rating_df.itertuples(index=False):

        movie_id = int(row.movie_id)
        rating = float(row.rating)

        preference = rating - 3.0

        if preference == 0:
            continue

        try:
            recommendations = recommender.recommend(
                movie_id=movie_id,
                top_n=50,
            )

        except (ValueError, KeyError, IndexError):
            continue

        if recommendations is None or recommendations.empty:
            continue

        if "movieId" not in recommendations.columns:
            continue

        if "similarity_score" not in recommendations.columns:
            continue

        for rec in recommendations.itertuples(index=False):

            candidate_id = int(rec.movieId)

            if candidate_id in excluded_ids:
                continue

            similarity = float(rec.similarity_score)

            # Weight each recommendation by both similarity
            # and the user's preference for the source movie.
            contribution = preference * similarity

            scores[candidate_id] = (
                scores.get(candidate_id, 0.0) + contribution
            )

    if not scores:
        return pd.DataFrame(
            columns=[
                "movieId",
                "title",
                "genres",
                "personalized_score",
            ]
        )

    ranked = pd.DataFrame(
        [
            {
                "movieId": movie_id,
                "personalized_score": score,
            }
            for movie_id, score in scores.items()
        ]
    )

    ranked = ranked.sort_values(
        "personalized_score",
        ascending=False,
    )

    ranked = ranked[
        ranked["personalized_score"] > 0
    ]

    ranked = ranked.head(top_n)

    result = ranked.merge(
        model_movies,
        on="movieId",
        how="left",
    )

    columns = [
        column
        for column in [
            "movieId",
            "title",
            "genres",
            "personalized_score",
        ]
        if column in result.columns
    ]

    return result[columns].reset_index(drop=True)