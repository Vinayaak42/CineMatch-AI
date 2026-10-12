import html
import streamlit as st


def apply_custom_css():
    """
    Apply the CineMatch AI cinematic design.
    """

    st.markdown(
        """
        <style>
        /* Main application */

        .stApp {
            background:
                radial-gradient(
                    ellipse at top left,
                    rgba(91, 33, 182, 0.12),
                    transparent 35%
                ),
                #0B1020;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1400px;
        }

        /* Typography */

        h1, h2, h3 {
            color: #F8FAFC !important;
            letter-spacing: -0.4px;
        }

        p, label, .stMarkdown {
            color: #CBD5E1;
        }

        /* Hero section */

        .hero {
            padding: 2.4rem 2rem;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-radius: 24px;
            background: linear-gradient(
                125deg,
                rgba(30, 41, 78, 0.96),
                rgba(58, 28, 95, 0.85),
                rgba(17, 24, 39, 0.96)
            );
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.18);
        }

        .hero h1 {
            font-size: clamp(2rem, 4vw, 3.5rem);
            font-weight: 800;
            margin-bottom: 0.7rem;
        }

        .hero p {
            font-size: 1.05rem;
            line-height: 1.7;
            color: #CBD5E1;
        }

        .hero-badge {
            display: inline-block;
            padding: 6px 12px;
            border: 1px solid rgba(196, 181, 253, 0.35);
            border-radius: 20px;
            color: #DDD6FE;
            font-size: 0.8rem;
            margin-bottom: 1rem;
        }

        /* Metric cards */

        div[data-testid="stMetric"] {
            background: rgba(21, 27, 46, 0.88);
            border: 1px solid rgba(148, 163, 184, 0.14);
            padding: 18px;
            border-radius: 16px;
        }

        div[data-testid="stMetricLabel"] {
            color: #94A3B8;
        }

        div[data-testid="stMetricValue"] {
            color: #F8FAFC;
        }

        /* Buttons */

        .stButton > button {
            border-radius: 10px;
            border: 1px solid rgba(139, 92, 246, 0.55);
            font-weight: 600;
            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            border-color: #A78BFA;
            color: #FFFFFF;
            transform: translateY(-1px);
        }

        /* Movie cards */

        .movie-card {
            overflow: hidden;
            border-radius: 16px;
            border: 1px solid rgba(148, 163, 184, 0.17);
            background: linear-gradient(
                180deg,
                rgba(30, 41, 59, 0.78),
                rgba(15, 23, 42, 0.96)
            );
            margin-bottom: 1rem;
            transition: border-color 0.2s ease;
        }

        .movie-card:hover {
            border-color: rgba(167, 139, 250, 0.75);
        }

        .movie-card-content {
            padding: 12px;
        }

        .movie-card-title {
            color: #F8FAFC;
            font-size: 1rem;
            font-weight: 700;
            line-height: 1.4;
            margin-bottom: 6px;
            overflow-wrap: anywhere;
        }

        .movie-card-meta {
            color: #94A3B8;
            font-size: 0.83rem;
            margin-bottom: 8px;
        }

        .movie-card-rating {
            color: #FBBF24;
            font-size: 0.9rem;
            font-weight: 700;
        }

        /* Sidebar */

        section[data-testid="stSidebar"] {
            background: #0F172A;
            border-right: 1px solid rgba(148, 163, 184, 0.12);
        }

        /* Input fields */

        div[data-baseweb="input"] > div,
        div[data-baseweb="select"] > div {
            background-color: #151B2E;
            border-color: #334155;
            border-radius: 10px;
        }

        /* Separators */

        hr {
            border-color: rgba(148, 163, 184, 0.16);
        }

        /* Mobile adjustments */

        @media (max-width: 768px) {
            .block-container {
                padding-top: 1rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .hero {
                padding: 1.5rem 1rem;
                border-radius: 16px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero(
    title="Discover Your Next Favorite Movie",
    subtitle=(
        "Explore movies, discover similar titles, "
        "and find your next cinematic experience."
    ),
):
    """
    Display the main cinematic banner.
    """

    safe_title = html.escape(title)
    safe_subtitle = html.escape(subtitle)

    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-badge">
                AI-POWERED MOVIE DISCOVERY
            </div>
            <h1>{safe_title}</h1>
            <p>{safe_subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_header(title, description=None):
    """
    Display a consistent section heading.
    """

    st.subheader(title)

    if description:
        st.caption(description)


def render_movie_card(movie, client=None):
    """
    Render a movie poster card.

    Accepts a TMDB movie dictionary.
    """

    title = html.escape(str(movie.get("title") or "Untitled"))

    release_date = movie.get("release_date") or ""
    release_date = html.escape(str(release_date))

    overview = movie.get("overview") or "No description available."
    overview = html.escape(str(overview))

    rating = movie.get("vote_average")

    if rating is not None:
        try:
            rating_text = f"⭐ {float(rating):.1f}/10"
        except (ValueError, TypeError):
            rating_text = "Rating unavailable"
    else:
        rating_text = "Rating unavailable"

    poster_url = None

    if client is not None:
        poster_url = client.get_image_url(
            movie.get("poster_path")
        )

    if poster_url:
        st.image(poster_url, use_container_width=True)
    else:
        st.markdown(
            """
            <div style="
                min-height: 180px;
                display: flex;
                align-items: center;
                justify-content: center;
                background: #151B2E;
                border-radius: 12px;
                color: #94A3B8;
            ">
                🎬 Poster unavailable
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="movie-card-content">
            <div class="movie-card-title">{title}</div>
            <div class="movie-card-meta">{release_date}</div>
            <div class="movie-card-rating">
                {html.escape(rating_text)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Movie overview"):
        st.write(overview)