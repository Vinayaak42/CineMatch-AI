from pathlib import Path

import pandas as pd
import streamlit as st

from src.preprocessing import prepare_datasets
from src.recommender import MovieRecommender
from src.tmdb_client import TMDBClient
from src.ui import (
    apply_custom_css,
    render_hero,
    render_section_header,
    render_movie_card,
)
from src.user_store import initialize_database
from src.personalized import generate_personalized_recommendations
from src.profile_ui import (
    render_profile_selector,
    render_user_stats,
    render_movie_rating,
    render_rating_history,
    render_watchlist,
    add_movie_to_watchlist,
)


# ============================================================
# 1. CONFIGURATION
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"
MODEL_DIR = ROOT_DIR / "models"

MOVIES_FILE = DATA_DIR / "movies.csv"
RATINGS_FILE = DATA_DIR / "ratings.csv"
MODEL_FILE = MODEL_DIR / "movie_recommender.joblib"

st.set_page_config(
    page_title="CineMatch AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_custom_css()


# ============================================================
# 2. DATABASE
# ============================================================

@st.cache_resource
def setup_database():
    initialize_database()
    return True


try:
    setup_database()
except Exception as exc:
    st.error(f"Database initialization failed: {exc}")
    st.stop()


# ============================================================
# 3. LOAD DATA
# ============================================================

@st.cache_data(show_spinner="Loading movie datasets...")
def load_data():
    if not MOVIES_FILE.exists():
        raise FileNotFoundError(
            f"Missing file: {MOVIES_FILE}"
        )

    if not RATINGS_FILE.exists():
        raise FileNotFoundError(
            f"Missing file: {RATINGS_FILE}"
        )

    raw_movies = pd.read_csv(MOVIES_FILE)
    raw_ratings = pd.read_csv(RATINGS_FILE)

    movies, ratings = prepare_datasets(
        raw_movies,
        raw_ratings,
    )

    return movies, ratings, raw_movies, raw_ratings


# ============================================================
# 4. LOAD RECOMMENDATION MODEL
# ============================================================

@st.cache_resource
def load_recommender():
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    if MODEL_FILE.exists():
        try:
            return MovieRecommender.load(str(MODEL_FILE))
        except Exception:
            pass

    movies, _, _, _ = load_data()

    recommender = MovieRecommender()
    recommender.fit(movies)
    recommender.save(str(MODEL_DIR))

    return recommender


# ============================================================
# 5. TMDB API
# ============================================================

@st.cache_resource
def get_tmdb_client():
    try:
        return TMDBClient()
    except (ValueError, RuntimeError):
        return None


@st.cache_data(ttl=3600, show_spinner=False)
def search_tmdb_cached(query):
    client = TMDBClient()
    return client.search_movies(query)


@st.cache_data(ttl=3600, show_spinner=False)
def popular_tmdb_cached():
    client = TMDBClient()
    return client.get_popular_movies()


@st.cache_data(ttl=3600, show_spinner=False)
def movie_details_cached(movie_id):
    client = TMDBClient()
    return client.get_movie_details(int(movie_id))


def require_tmdb():
    client = get_tmdb_client()

    if client is None:
        st.warning(
            "TMDB credentials are missing. Add TMDB_API_KEY or "
            "TMDB_READ_ACCESS_TOKEN to your .env file."
        )

    return client


# ============================================================
# 6. HOME PAGE
# ============================================================

def page_home(movies, ratings):
    render_hero(
        title="CineMatch AI",
        subtitle=(
            "Discover your next favorite movie with AI-powered "
            "recommendations and personalized movie discovery."
        ),
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🎬 Movies", f"{len(movies):,}")

    with col2:
        st.metric("⭐ Ratings", f"{len(ratings):,}")

    with col3:
        users = (
            ratings["userId"].nunique()
            if "userId" in ratings.columns
            else 0
        )
        st.metric("👥 Dataset Users", f"{users:,}")

    with col4:
        average = (
            ratings["rating"].mean()
            if not ratings.empty and "rating" in ratings.columns
            else 0
        )
        st.metric("📊 Average Rating", f"{average:.2f}/5")

    st.markdown("---")

    render_section_header(
        "Discover CineMatch",
        "Your personal movie discovery platform.",
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🤖 AI Recommendations")
        st.write(
            "Find movies similar to your favorite titles "
            "using machine learning."
        )

    with col2:
        st.markdown("### 🔎 Explore Movies")
        st.write(
            "Search movies by title, genre, release year, "
            "and rating information."
        )

    with col3:
        st.markdown("### 💜 Personalization")
        st.write(
            "Rate movies, build your watchlist, and discover "
            "recommendations based on your preferences."
        )

    st.markdown("---")

    render_section_header(
        "Popular Movies",
        "Popular titles from The Movie Database.",
    )

    client = require_tmdb()

    if client is None:
        return

    try:
        popular = popular_tmdb_cached()

        if not popular:
            st.info("No popular movies were returned.")
            return

        columns = st.columns(5)

        for index, movie in enumerate(popular[:10]):
            with columns[index % 5]:
                render_movie_card(movie, client)

    except Exception as exc:
        st.warning(f"Could not load popular movies: {exc}")


# ============================================================
# 7. EXPLORE MOVIES
# ============================================================

def page_explore(movies):
    render_hero(
        title="Explore Movies",
        subtitle="Search and filter the MovieLens dataset.",
    )

    query = st.text_input(
        "Search movie title",
        placeholder="Example: Toy Story",
        key="explore_query",
    )

    filtered = movies.copy()

    if query.strip():
        filtered = filtered[
            filtered["title"].astype(str).str.contains(
                query.strip(),
                case=False,
                regex=False,
                na=False,
            )
        ]

    available_genres = sorted(
        {
            genre.strip()
            for value in filtered["genres"].dropna()
            for genre in str(value).split("|")
            if genre.strip() != "(no genres listed)"
            and genre.strip()
        }
    )

    selected_genres = st.multiselect(
        "Filter by genre",
        options=available_genres,
        key="explore_genres",
    )

    if selected_genres:
        filtered = filtered[
            filtered["genres"].fillna("").apply(
                lambda value: any(
                    genre in str(value).split("|")
                    for genre in selected_genres
                )
            )
        ]

    if "year" in filtered.columns:
        years = pd.to_numeric(
            filtered["year"],
            errors="coerce",
        ).dropna()

        if not years.empty:
            minimum_year = int(years.min())
            maximum_year = int(years.max())

            if minimum_year < maximum_year:
                year_range = st.slider(
                    "Release year",
                    min_value=minimum_year,
                    max_value=maximum_year,
                    value=(minimum_year, maximum_year),
                    key="explore_years",
                )

                numeric_years = pd.to_numeric(
                    filtered["year"],
                    errors="coerce",
                )

                filtered = filtered[
                    numeric_years.between(
                        year_range[0],
                        year_range[1],
                    )
                    | numeric_years.isna()
                ]

    st.subheader(f"🎞️ {len(filtered):,} movies found")

    display_columns = [
        column
        for column in [
            "movieId",
            "title",
            "genres",
            "year",
            "rating_count",
            "avg_rating",
        ]
        if column in filtered.columns
    ]

    st.dataframe(
        filtered[display_columns],
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "⬇️ Download Movies CSV",
        data=filtered[display_columns].to_csv(
            index=False
        ).encode("utf-8"),
        file_name="cinematch_movies.csv",
        mime="text/csv",
    )


# ============================================================
# 8. AI RECOMMENDATIONS
# ============================================================

def page_recommendations(recommender):
    render_hero(
        title="AI Movie Recommendations",
        subtitle=(
            "Select a movie to find similar titles using "
            "TF-IDF and cosine similarity."
        ),
    )

    model_movies = recommender.movies.copy()

    if model_movies.empty:
        st.warning("No movies are available in the recommendation model.")
        return

    query = st.text_input(
        "Search for a movie",
        placeholder="Enter a movie title...",
        key="ai_movie_query",
    )

    options = model_movies[
        ["movieId", "title"]
    ].drop_duplicates("movieId").sort_values("title")

    if query.strip():
        options = options[
            options["title"].astype(str).str.contains(
                query.strip(),
                case=False,
                regex=False,
                na=False,
            )
        ]

    if options.empty:
        st.warning("No matching movies found.")
        return

    selected_id = st.selectbox(
        "Select a movie",
        options=options["movieId"].tolist(),
        format_func=lambda movie_id: options.loc[
            options["movieId"] == movie_id,
            "title",
        ].iloc[0],
        key="ai_selected_movie",
    )

    number = st.slider(
        "Number of recommendations",
        min_value=5,
        max_value=20,
        value=10,
        key="ai_number",
    )

    if st.button(
        "✨ Recommend Movies",
        type="primary",
    ):
        try:
            recommendations = recommender.recommend(
                movie_id=int(selected_id),
                top_n=number,
            )

            st.session_state["ai_recommendations"] = recommendations
            st.session_state["ai_recommendation_id"] = int(selected_id)

        except Exception as exc:
            st.error(f"Recommendation failed: {exc}")

    recommendations = st.session_state.get(
        "ai_recommendations"
    )

    if recommendations is not None:
        selected_movie = model_movies[
            model_movies["movieId"]
            == st.session_state.get("ai_recommendation_id")
        ]

        if not selected_movie.empty:
            st.subheader(
                f"Movies similar to {selected_movie.iloc[0]['title']}"
            )

        if recommendations.empty:
            st.info("No similar movies found.")
        else:
            st.dataframe(
                recommendations,
                use_container_width=True,
                hide_index=True,
            )


# ============================================================
# 9. LIVE TMDB SEARCH
# ============================================================

def page_tmdb_search():
    render_hero(
        title="Live Movie Search",
        subtitle="Search movies using TMDB.",
    )

    client = require_tmdb()

    if client is None:
        return

    query = st.text_input(
        "Movie title",
        placeholder="Example: Inception",
        key="tmdb_query",
    )

    if st.button("🔎 Search Movies", type="primary"):
        if not query.strip():
            st.warning("Enter a movie title.")
        else:
            try:
                st.session_state["tmdb_results"] = (
                    search_tmdb_cached(query.strip())
                )
            except Exception as exc:
                st.error(f"TMDB search failed: {exc}")
                st.session_state["tmdb_results"] = []

    results = st.session_state.get("tmdb_results", [])

    if not results:
        return

    for start in range(0, len(results), 3):
        columns = st.columns(3)

        for column, movie in zip(columns, results[start:start + 3]):
            with column:
                render_movie_card(movie, client)

                movie_id = movie.get("id")

                if movie_id is not None:
                    with st.expander("Movie details"):
                        try:
                            details = movie_details_cached(movie_id)

                            st.write(
                                "**Release date:**",
                                details.get("release_date") or "Unknown",
                            )

                            runtime = details.get("runtime")

                            st.write(
                                "**Runtime:**",
                                f"{runtime} minutes"
                                if runtime
                                else "Unknown",
                            )

                            genres = [
                                item["name"]
                                for item in details.get("genres", [])
                                if item.get("name")
                            ]

                            st.write(
                                "**Genres:**",
                                ", ".join(genres) or "Unknown",
                            )

                            st.write(
                                details.get("overview")
                                or "No overview available."
                            )

                        except Exception as exc:
                            st.warning(f"Could not load details: {exc}")


# ============================================================
# 10. POPULAR MOVIES
# ============================================================

def page_popular():
    render_hero(
        title="Popular Movies",
        subtitle="Browse popular movies from TMDB.",
    )

    client = require_tmdb()

    if client is None:
        return

    try:
        movies = popular_tmdb_cached()
    except Exception as exc:
        st.error(f"Could not retrieve popular movies: {exc}")
        return

    if not movies:
        st.info("No popular movies available.")
        return

    sort_option = st.selectbox(
        "Sort by",
        ["Popularity", "Rating", "Release Date"],
        key="popular_sort",
    )

    if sort_option == "Popularity":
        movies = sorted(
            movies,
            key=lambda item: item.get("popularity") or 0,
            reverse=True,
        )
    elif sort_option == "Rating":
        movies = sorted(
            movies,
            key=lambda item: item.get("vote_average") or 0,
            reverse=True,
        )
    else:
        movies = sorted(
            movies,
            key=lambda item: item.get("release_date") or "",
            reverse=True,
        )

    for start in range(0, len(movies), 4):
        columns = st.columns(4)

        for column, movie in zip(columns, movies[start:start + 4]):
            with column:
                render_movie_card(movie, client)


# ============================================================
# 11. DATA ANALYTICS
# ============================================================

def page_analytics(movies, ratings):
    render_hero(
        title="Movie Data Analytics",
        subtitle="Explore genres, ratings, and release-year trends.",
    )

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "🎭 Genres",
            "⭐ Ratings",
            "📅 Release Years",
            "🏆 Top Movies",
        ]
    )

    with tab1:
        render_section_header("Genre Distribution")

        genre_counts = (
            movies["genres"]
            .fillna("")
            .str.split("|")
            .explode()
        )

        genre_counts = genre_counts[
            genre_counts.ne("")
            & genre_counts.ne("(no genres listed)")
        ]

        genre_counts = genre_counts.value_counts()

        st.bar_chart(genre_counts)
        st.dataframe(
            genre_counts.rename_axis("Genre").reset_index(
                name="Movie Count"
            ),
            use_container_width=True,
            hide_index=True,
        )

    with tab2:
        render_section_header("Rating Distribution")

        if "rating" in ratings.columns:
            distribution = (
                ratings["rating"]
                .value_counts()
                .sort_index()
            )

            st.bar_chart(distribution)

            st.dataframe(
                distribution.rename_axis("Rating").reset_index(
                    name="Count"
                ),
                use_container_width=True,
                hide_index=True,
            )

            st.metric(
                "Average Rating",
                f"{ratings['rating'].mean():.2f}/5",
            )

    with tab3:
        render_section_header("Movies by Release Year")

        if "year" in movies.columns:
            years = pd.to_numeric(
                movies["year"],
                errors="coerce",
            ).dropna()

            if not years.empty:
                distribution = years.astype(int).value_counts().sort_index()
                st.line_chart(distribution)
            else:
                st.info("No release-year data available.")
        else:
            st.info("The dataset does not contain a year column.")

    with tab4:
        render_section_header("Top-Rated Movies")

        if {"avg_rating", "rating_count"}.issubset(movies.columns):
            minimum_ratings = st.slider(
                "Minimum rating count",
                min_value=1,
                max_value=100,
                value=20,
                key="top_min_ratings",
            )

            top_movies = movies.copy()

            top_movies["avg_rating"] = pd.to_numeric(
                top_movies["avg_rating"],
                errors="coerce",
            )

            top_movies["rating_count"] = pd.to_numeric(
                top_movies["rating_count"],
                errors="coerce",
            )

            top_movies = top_movies[
                top_movies["rating_count"] >= minimum_ratings
            ].sort_values(
                "avg_rating",
                ascending=False,
            )

            st.dataframe(
                top_movies.head(30),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info(
                "Average-rating or rating-count columns are unavailable."
            )


# ============================================================
# 12. DATA QUALITY
# ============================================================

def page_data_quality(
    raw_movies,
    raw_ratings,
    movies,
    ratings,
):
    render_hero(
        title="Data Quality",
        subtitle="Inspect missing values, duplicates, and data types.",
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Raw Movies", f"{len(raw_movies):,}")

    with col2:
        st.metric("Clean Movies", f"{len(movies):,}")

    with col3:
        st.metric("Raw Ratings", f"{len(raw_ratings):,}")

    with col4:
        st.metric("Clean Ratings", f"{len(ratings):,}")

    tab1, tab2, tab3 = st.tabs(
        ["Missing Values", "Duplicates", "Data Types"]
    )

    with tab1:
        st.subheader("Movies: Missing Values")

        missing_movies = raw_movies.isnull().sum().to_frame(
            "Missing Count"
        )

        st.dataframe(
            missing_movies,
            use_container_width=True,
        )

        st.subheader("Ratings: Missing Values")

        missing_ratings = raw_ratings.isnull().sum().to_frame(
            "Missing Count"
        )

        st.dataframe(
            missing_ratings,
            use_container_width=True,
        )

    with tab2:
        movie_duplicates = (
            raw_movies["movieId"].duplicated().sum()
            if "movieId" in raw_movies.columns
            else 0
        )

        rating_duplicates = (
            raw_ratings.duplicated(
                subset=["userId", "movieId"]
            ).sum()
            if {"userId", "movieId"}.issubset(raw_ratings.columns)
            else 0
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Duplicate Movie IDs",
                int(movie_duplicates),
            )

        with col2:
            st.metric(
                "Duplicate User-Movie Pairs",
                int(rating_duplicates),
            )

    with tab3:
        st.subheader("Movies Data Types")

        st.dataframe(
            movies.dtypes.astype(str).rename(
                "Data Type"
            ).to_frame(),
            use_container_width=True,
        )

        st.subheader("Ratings Data Types")

        st.dataframe(
            ratings.dtypes.astype(str).rename(
                "Data Type"
            ).to_frame(),
            use_container_width=True,
        )


# ============================================================
# 13. PERSONALIZED RECOMMENDATIONS
# ============================================================

def page_personalized(username, recommender):
    render_hero(
        title="Personalized For You",
        subtitle="Discover movies based on your ratings.",
    )

    render_user_stats(username)

    from src.user_store import get_user_ratings, get_watchlist

    user_ratings = get_user_ratings(username)
    watchlist = get_watchlist(username)

    if not user_ratings:
        st.info(
            "You have not rated any movies yet. Go to Rate Movies, "
            "rate some movies, and return here."
        )
        return

    st.write(f"Movies rated: {len(user_ratings)}")

    number = st.slider(
        "Recommendations to generate",
        min_value=5,
        max_value=20,
        value=10,
        key="personalized_number",
    )

    if st.button(
        "💜 Generate Personalized Recommendations",
        type="primary",
    ):
        try:
            results = generate_personalized_recommendations(
                recommender=recommender,
                user_ratings=user_ratings,
                watchlist=watchlist,
                top_n=number,
            )

            st.session_state["personalized_results"] = results

        except Exception as exc:
            st.error(f"Could not generate recommendations: {exc}")
            return

    results = st.session_state.get("personalized_results")

    if results is not None:
        if results.empty:
            st.info(
                "No recommendations are available yet. "
                "Try rating more movies."
            )
        else:
            st.dataframe(
                results,
                use_container_width=True,
                hide_index=True,
            )

            st.download_button(
                "⬇️ Download Recommendations",
                data=results.to_csv(index=False).encode("utf-8"),
                file_name="personalized_recommendations.csv",
                mime="text/csv",
            )


# ============================================================
# 14. RATE MOVIES
# ============================================================

def page_rate_movies(username, movies):
    render_hero(
        title="Rate Movies",
        subtitle="Rate movies to improve your recommendations.",
    )

    query = st.text_input(
        "Search for a movie",
        placeholder="Enter a movie title...",
        key="rate_query",
    )

    filtered = movies.copy()

    if query.strip():
        filtered = filtered[
            filtered["title"].astype(str).str.contains(
                query.strip(),
                case=False,
                regex=False,
                na=False,
            )
        ]

    if filtered.empty:
        st.info("No matching movies found.")
    else:
        options = (
            filtered[["movieId", "title"]]
            .drop_duplicates("movieId")
            .sort_values("title")
            .head(500)
        )

        selected_id = st.selectbox(
            "Select a movie",
            options=options["movieId"].tolist(),
            format_func=lambda movie_id: options.loc[
                options["movieId"] == movie_id,
                "title",
            ].iloc[0],
            key="rate_selected_id",
        )

        selected_rows = movies[
            movies["movieId"] == selected_id
        ]

        if not selected_rows.empty:
            movie = selected_rows.iloc[0]

            st.subheader(f"🎬 {movie['title']}")

            render_movie_rating(
                username=username,
                movie_id=int(selected_id),
                title=str(movie["title"]),
            )

            if st.button(
                "➕ Add to Watchlist",
                key="rate_add_watchlist",
            ):
                try:
                    add_movie_to_watchlist(
                        username=username,
                        movie_id=int(selected_id),
                    )
                    st.success("Movie added to your watchlist.")
                except Exception as exc:
                    st.error(f"Could not add movie: {exc}")

    st.markdown("---")

    render_section_header(
        "Your Rating History",
        "Review your ratings and remove ratings when needed.",
    )

    render_rating_history(username, movies)


# ============================================================
# 15. WATCHLIST
# ============================================================

def page_watchlist(username, movies):
    render_hero(
        title="My Watchlist",
        subtitle="Keep track of movies you want to watch.",
    )

    render_watchlist(username, movies)

    st.markdown("---")

    render_section_header("Add Movies")

    query = st.text_input(
        "Search for a movie to add",
        placeholder="Enter a movie title...",
        key="watchlist_query",
    )

    filtered = movies.copy()

    if query.strip():
        filtered = filtered[
            filtered["title"].astype(str).str.contains(
                query.strip(),
                case=False,
                regex=False,
                na=False,
            )
        ]

    if filtered.empty:
        st.info("No matching movies found.")
        return

    options = (
        filtered[["movieId", "title"]]
        .drop_duplicates("movieId")
        .sort_values("title")
        .head(500)
    )

    selected_id = st.selectbox(
        "Select a movie",
        options["movieId"].tolist(),
        format_func=lambda movie_id: options.loc[
            options["movieId"] == movie_id,
            "title",
        ].iloc[0],
        key="watchlist_selected_id",
    )

    if st.button(
        "➕ Add to My Watchlist",
        type="primary",
    ):
        try:
            add_movie_to_watchlist(
                username=username,
                movie_id=int(selected_id),
            )

            st.success("Movie added to your watchlist.")
            st.rerun()

        except Exception as exc:
            st.error(f"Could not add movie: {exc}")


# ============================================================
# 16. MAIN APPLICATION
# ============================================================

def main():
    with st.sidebar:
        st.title("🎬 CineMatch AI")
        st.caption("Your intelligent movie companion")
        st.markdown("---")

        page = st.radio(
            "Navigation",
            [
                "🏠 Home",
                "🔎 Explore Movies",
                "🤖 AI Recommendations",
                "🌐 Live TMDB Search",
                "🔥 Popular Movies",
                "📊 Data Analytics",
                "🧪 Data Quality",
                "💜 Personalized For You",
                "⭐ Rate Movies",
                "📋 My Watchlist",
            ],
            key="navigation",
        )

        st.markdown("---")
        st.subheader("👤 User Profile")

        active_profile = render_profile_selector()

        st.markdown("---")
        st.caption("Built with Python, Streamlit, and scikit-learn.")

    try:
        movies, ratings, raw_movies, raw_ratings = load_data()

    except Exception as exc:
        st.error("Could not load the datasets.")
        st.exception(exc)

        st.info(
            "Verify that data/movies.csv and data/ratings.csv exist."
        )
        st.stop()

    if page == "🏠 Home":
        page_home(movies, ratings)

    elif page == "🔎 Explore Movies":
        page_explore(movies)

    elif page == "🤖 AI Recommendations":
        try:
            recommender = load_recommender()
            page_recommendations(recommender)
        except Exception as exc:
            st.error(f"Could not load the recommendation model: {exc}")

    elif page == "🌐 Live TMDB Search":
        page_tmdb_search()

    elif page == "🔥 Popular Movies":
        page_popular()

    elif page == "📊 Data Analytics":
        page_analytics(movies, ratings)

    elif page == "🧪 Data Quality":
        page_data_quality(
            raw_movies,
            raw_ratings,
            movies,
            ratings,
        )

    elif page == "💜 Personalized For You":
        if not active_profile:
            st.warning(
                "Create or select a profile in the sidebar first."
            )
        else:
            try:
                recommender = load_recommender()
                page_personalized(
                    active_profile,
                    recommender,
                )
            except Exception as exc:
                st.error(
                    f"Could not load personalized recommendations: {exc}"
                )

    elif page == "⭐ Rate Movies":
        if not active_profile:
            st.warning(
                "Create or select a profile in the sidebar first."
            )
        else:
            page_rate_movies(active_profile, movies)

    elif page == "📋 My Watchlist":
        if not active_profile:
            st.warning(
                "Create or select a profile in the sidebar first."
            )
        else:
            page_watchlist(active_profile, movies)


if __name__ == "__main__":
    main()
