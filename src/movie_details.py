import streamlit as st


def display_movie_details(movie, client):
    """
    Display a TMDB movie result as a detailed Streamlit card.
    """

    title = movie.get("title") or "Unknown title"
    overview = movie.get("overview") or "No overview available."
    release_date = movie.get("release_date") or "Unknown"
    rating = movie.get("vote_average")

    poster_path = movie.get("poster_path")
    poster_url = client.get_image_url(poster_path)

    with st.container(border=True):
        left, right = st.columns([1, 2])

        with left:
            if poster_url:
                st.image(poster_url, use_container_width=True)
            else:
                st.info("Poster unavailable")

        with right:
            st.subheader(title)

            st.caption(f"Release date: {release_date}")

            if rating is not None:
                st.metric(
                    "TMDB rating",
                    f"{float(rating):.1f}/10"
                )

            st.write(overview)

            genres = movie.get("genres", [])

            if genres:
                genre_names = [
                    genre.get("name", "")
                    for genre in genres
                    if genre.get("name")
                ]

                if genre_names:
                    st.caption(
                        "Genres: " + ", ".join(genre_names)
                    )