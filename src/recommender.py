from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class MovieRecommender:
    """
    Content-based movie recommendation engine.

    Uses TF-IDF and cosine similarity to identify
    movies with similar genres and titles.
    """

    def __init__(self):
        self.movies = None
        self.vectorizer = None
        self.feature_matrix = None
        self.similarity_matrix = None

    # --------------------------------------------------
    # 1. PREPARE FEATURES
    # --------------------------------------------------

    @staticmethod
    def prepare_features(movies):

        movies = movies.copy()

        if "movieId" not in movies.columns:
            raise ValueError("Dataset must contain movieId.")

        if "title" not in movies.columns:
            raise ValueError("Dataset must contain title.")

        if "genres" not in movies.columns:
            raise ValueError("Dataset must contain genres.")

        movies = movies.dropna(
            subset=["movieId", "title"]
        )

        movies = movies.drop_duplicates(
            subset=["movieId"]
        )

        movies["title"] = (
            movies["title"]
            .astype(str)
            .str.strip()
        )

        movies["genres"] = (
            movies["genres"]
            .fillna("")
            .astype(str)
            .str.replace("|", " ", regex=False)
        )

        # Extract title without its release year
        movies["clean_title"] = (
            movies["title"]
            .str.replace(
                r"\s*\(\d{4}\)\s*$",
                "",
                regex=True
            )
            .str.strip()
        )

        # Use both title and genre features.
        # Genres are repeated to give them more influence.
        movies["features"] = (
            movies["clean_title"] + " "
            + movies["genres"] + " "
            + movies["genres"]
        )

        movies["features"] = (
            movies["features"]
            .str.lower()
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )

        return movies.reset_index(drop=True)

    # --------------------------------------------------
    # 2. TRAIN THE CONTENT REPRESENTATION
    # --------------------------------------------------

    def fit(self, movies):

        self.movies = self.prepare_features(movies)

        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            min_df=1,
            max_features=50000,
            sublinear_tf=True
        )

        self.feature_matrix = self.vectorizer.fit_transform(
            self.movies["features"]
        )

        # Keep the sparse feature matrix instead of
        # constructing a dense all-pairs similarity matrix.
        self.similarity_matrix = None

        return self

    # --------------------------------------------------
    # 3. FIND A MOVIE
    # --------------------------------------------------

    def search_movies(self, query, limit=20):

        if self.movies is None:
            raise RuntimeError(
                "Train the recommender before searching."
            )

        query = str(query).strip()

        if not query:
            return self.movies.iloc[0:0].copy()

        matches = self.movies[
            self.movies["title"].str.contains(
                query,
                case=False,
                na=False,
                regex=False
            )
        ]

        return matches.head(limit).copy()

    # --------------------------------------------------
    # 4. GENERATE RECOMMENDATIONS
    # --------------------------------------------------

    def recommend(
        self,
        movie_id=None,
        title=None,
        top_n=10,
        exclude_same_franchise=False
    ):

        if self.movies is None or self.feature_matrix is None:
            raise RuntimeError(
                "Train the recommender before generating recommendations."
            )

        if top_n < 1:
            raise ValueError("top_n must be at least 1.")

        if movie_id is not None:

            matched = self.movies[
                self.movies["movieId"] == movie_id
            ]

        elif title:

            matched = self.movies[
                self.movies["title"].str.casefold()
                == str(title).strip().casefold()
            ]

            # Allow an exact clean-title match when
            # the original title was not supplied.
            if matched.empty:
                matched = self.movies[
                    self.movies["clean_title"].str.casefold()
                    == str(title).strip().casefold()
                ]

        else:

            raise ValueError(
                "Provide either movie_id or title."
            )

        if matched.empty:
            return pd.DataFrame()

        movie_index = matched.index[0]

        # Compute similarities only for the selected movie.
        selected_vector = self.feature_matrix[movie_index]

        scores = cosine_similarity(
            selected_vector,
            self.feature_matrix
        ).ravel()

        # Exclude the selected movie itself.
        scores[movie_index] = -1.0

        ranked_indices = np.argsort(scores)[::-1]

        selected_title = self.movies.iloc[movie_index]["clean_title"]

        selected_words = set(
            selected_title.casefold().split()
        )

        recommendations = []

        for index in ranked_indices:

            if scores[index] < 0:
                continue

            candidate = self.movies.iloc[index]

            if exclude_same_franchise:

                candidate_words = set(
                    candidate["clean_title"].casefold().split()
                )

                if (
                    selected_words
                    and selected_words.issubset(candidate_words)
                ):
                    continue

            recommendations.append(
                {
                    "movieId": candidate["movieId"],
                    "title": candidate["title"],
                    "genres": candidate["genres"],
                    "similarity_score": round(
                        float(scores[index]),
                        4
                    )
                }
            )

            if len(recommendations) >= top_n:
                break

        return pd.DataFrame(recommendations)

    # --------------------------------------------------
    # 5. SAVE MODEL ARTIFACTS
    # --------------------------------------------------

    def save(self, output_dir="models"):

        if self.movies is None or self.vectorizer is None:
            raise RuntimeError(
                "Train the recommender before saving."
            )

        output_path = Path(output_dir)

        output_path.mkdir(
            parents=True,
            exist_ok=True
        )

        joblib.dump(
            {
                "movies": self.movies,
                "vectorizer": self.vectorizer,
                "feature_matrix": self.feature_matrix
            },
            output_path / "movie_recommender.joblib"
        )

    # --------------------------------------------------
    # 6. LOAD MODEL ARTIFACTS
    # --------------------------------------------------

    @classmethod
    def load(cls, model_path="models/movie_recommender.joblib"):

        artifacts = joblib.load(model_path)

        recommender = cls()

        recommender.movies = artifacts["movies"]

        recommender.vectorizer = artifacts["vectorizer"]

        recommender.feature_matrix = artifacts["feature_matrix"]

        recommender.similarity_matrix = None

        return recommender
