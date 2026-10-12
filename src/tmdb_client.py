import os

import requests
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p"


class TMDBClient:
    """
    Client for retrieving movie information from The Movie Database (TMDB).
    """

    def __init__(self, api_key=None):
        self.api_key = (
            api_key
            or os.getenv("TMDB_API_KEY")
            or os.getenv("TMDB_READ_ACCESS_TOKEN")
        )

        self.access_token = (
            os.getenv("TMDB_READ_ACCESS_TOKEN")
            if not api_key
            else None
        )

        if not self.api_key:
            raise ValueError(
                "TMDB credentials are missing. "
                "Add TMDB_API_KEY or TMDB_READ_ACCESS_TOKEN "
                "to your .env file."
            )

        self.session = requests.Session()

        self.session.headers.update({
            "Accept": "application/json"
        })

        # Use Bearer authentication for a read access token.
        if self.access_token and not os.getenv("TMDB_API_KEY"):
            self.session.headers.update({
                "Authorization": f"Bearer {self.access_token}"
            })

    def _get(self, endpoint, params=None):
        """Send a GET request to the TMDB API."""

        url = f"{TMDB_BASE_URL}/{endpoint.lstrip('/')}"
        request_params = dict(params or {})

        # API key authentication uses a query parameter.
        if os.getenv("TMDB_API_KEY"):
            request_params["api_key"] = os.getenv("TMDB_API_KEY")
        elif not self.access_token:
            request_params["api_key"] = self.api_key

        try:
            response = self.session.get(
                url,
                params=request_params,
                timeout=15
            )

            response.raise_for_status()
            return response.json()

        except requests.Timeout as exc:
            raise RuntimeError(
                "TMDB request timed out. Please try again."
            ) from exc

        except requests.HTTPError as exc:
            status = (
                exc.response.status_code
                if exc.response is not None
                else "unknown"
            )

            if status == 401:
                message = (
                    "TMDB authentication failed. "
                    "Check your API credentials."
                )
            elif status == 404:
                message = "The requested movie was not found."
            elif status == 429:
                message = (
                    "TMDB rate limit reached. Please wait and retry."
                )
            else:
                message = f"TMDB returned HTTP status {status}."

            raise RuntimeError(message) from exc

        except requests.RequestException as exc:
            raise RuntimeError(
                "Could not connect to TMDB. "
                "Check your internet connection."
            ) from exc

    def search_movies(self, query, page=1):
        """Search for movies by title."""

        if not query or not query.strip():
            return []

        data = self._get(
            "search/movie",
            params={
                "query": query.strip(),
                "page": page,
                "include_adult": False
            }
        )

        return data.get("results", [])

    def get_movie_details(self, movie_id):
        """Retrieve movie details and credits."""

        return self._get(
            f"movie/{int(movie_id)}",
            params={
                "append_to_response": "credits"
            }
        )

    def get_popular_movies(self, page=1):
        """Retrieve popular movies from TMDB."""

        data = self._get(
            "movie/popular",
            params={"page": page}
        )

        return data.get("results", [])

    def get_image_url(self, image_path, size="w500"):
        """Convert a TMDB image path into a complete URL."""

        if not image_path:
            return None

        return f"{TMDB_IMAGE_BASE_URL}/{size}{image_path}"


@st.cache_data(ttl=3600, show_spinner=False)
def search_tmdb_cached(query, page=1):
    """Cache movie search results for one hour."""

    client = TMDBClient()
    return client.search_movies(query, page=page)