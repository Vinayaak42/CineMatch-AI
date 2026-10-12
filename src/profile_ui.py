import streamlit as st

from src.user_store import (
    initialize_database,
    create_profile,
    get_profiles,
    save_rating,
    get_user_ratings,
    remove_rating,
    add_to_watchlist,
    get_watchlist,
    remove_from_watchlist,
    get_user_stats,
)


def initialize_user_database():
    initialize_database()


def render_profile_selector():
    """
    Allow a visitor to create or select a local profile.
    """

    st.sidebar.divider()
    st.sidebar.subheader("👤 Your Profile")

    profiles = get_profiles()

    selected_profile = st.sidebar.selectbox(
        "Select profile",
        options=[""] + profiles,
        key="profile_selector",
    )

    new_profile = st.sidebar.text_input(
        "Or create a profile",
        placeholder="Enter a profile name",
        key="new_profile_name",
    )

    if st.sidebar.button(
        "Create / Select Profile",
        key="create_profile_button",
    ):

        username = new_profile.strip() or selected_profile.strip()

        if not username:
            st.sidebar.warning("Enter or select a profile name.")
            return None

        try:
            create_profile(username)
            st.session_state["active_profile"] = username
            st.rerun()

        except ValueError as exc:
            st.sidebar.error(str(exc))
            return None

    return st.session_state.get("active_profile")


def render_user_stats(username):
    stats = get_user_stats(username)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Movies Rated",
        stats["rating_count"],
    )

    col2.metric(
        "Watchlist",
        stats["watchlist_count"],
    )

    col3.metric(
        "Average Rating",
        (
            f"{stats['average_rating']:.2f}/5"
            if stats["average_rating"] is not None
            else "N/A"
        ),
    )


def render_movie_rating(username, movie_id, title):
    """
    Display a rating input and save the rating.
    """

    st.markdown(f"**Rate: {title}**")

    rating = st.select_slider(
        "Your rating",
        options=[
            0.5, 1.0, 1.5, 2.0, 2.5,
            3.0, 3.5, 4.0, 4.5, 5.0,
        ],
        value=4.0,
        key=f"rating_slider_{username}_{movie_id}",
    )

    if st.button(
        "Save Rating",
        key=f"save_rating_{username}_{movie_id}",
    ):
        try:
            save_rating(username, movie_id, rating)

            st.success(
                f"Saved your {rating:.1f}/5 rating for {title}."
            )

            st.rerun()

        except (ValueError, TypeError) as exc:
            st.error(str(exc))


def render_rating_history(username, movies):
    """
    Display a user's rating history.
    """

    ratings = get_user_ratings(username)

    if not ratings:
        st.info("You have not rated any movies yet.")
        return

    rating_df = __import__("pandas").DataFrame(ratings)

    rating_df = rating_df.merge(
        movies[["movieId", "title"]],
        left_on="movie_id",
        right_on="movieId",
        how="left",
    )

    for row in rating_df.itertuples(index=False):

        title = (
            row.title
            if isinstance(row.title, str)
            else f"Movie ID {row.movie_id}"
        )

        with st.container(border=True):

            col1, col2, col3 = st.columns([3, 1, 1])

            col1.write(f"🎬 {title}")
            col2.write(f"⭐ {row.rating:.1f}/5")

            if col3.button(
                "Remove",
                key=f"remove_rating_{username}_{row.movie_id}",
            ):
                remove_rating(username, row.movie_id)
                st.rerun()


def render_watchlist(username, movies):
    """
    Display a user's saved watchlist.
    """

    items = get_watchlist(username)

    if not items:
        st.info("Your watchlist is empty.")
        return

    watchlist_df = __import__("pandas").DataFrame(items)

    watchlist_df = watchlist_df.merge(
        movies[["movieId", "title", "genres"]],
        left_on="movie_id",
        right_on="movieId",
        how="left",
    )

    for row in watchlist_df.itertuples(index=False):

        title = (
            row.title
            if isinstance(row.title, str)
            else f"Movie ID {row.movie_id}"
        )

        with st.container(border=True):

            col1, col2 = st.columns([4, 1])

            col1.write(f"🎬 **{title}**")

            if isinstance(row.genres, str):
                col1.caption(row.genres)

            if col2.button(
                "Remove",
                key=f"remove_watchlist_{username}_{row.movie_id}",
            ):
                remove_from_watchlist(username, row.movie_id)
                st.rerun()


def add_movie_to_watchlist(username, movie_id):
    """Save a selected movie to the current profile's watchlist."""

    add_to_watchlist(username, movie_id)
    st.success("Movie added to your watchlist.")