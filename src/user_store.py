import sqlite3
from pathlib import Path
from datetime import datetime, timezone


ROOT_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = ROOT_DIR / "data" / "cinematch.db"


def get_connection():
    """Create a connection to the CineMatch SQLite database."""

    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(
        DATABASE_PATH,
        timeout=10,
    )

    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA busy_timeout = 10000")

    return connection


def initialize_database():
    """Create the required tables if they do not exist."""

    with get_connection() as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                username TEXT PRIMARY KEY,
                created_at TEXT NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS user_ratings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                movie_id INTEGER NOT NULL,
                rating REAL NOT NULL
                    CHECK (rating >= 0.5 AND rating <= 5.0),
                updated_at TEXT NOT NULL,
                UNIQUE(username, movie_id),
                FOREIGN KEY(username)
                    REFERENCES user_profiles(username)
                    ON DELETE CASCADE
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS watchlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                movie_id INTEGER NOT NULL,
                added_at TEXT NOT NULL,
                UNIQUE(username, movie_id),
                FOREIGN KEY(username)
                    REFERENCES user_profiles(username)
                    ON DELETE CASCADE
            )
        """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_ratings_username
            ON user_ratings(username)
        """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_watchlist_username
            ON watchlist(username)
        """)


def normalize_username(username):
    """Normalize a local profile name."""

    if not isinstance(username, str):
        raise ValueError("Username must be text.")

    username = username.strip()

    if not username:
        raise ValueError("Please enter a profile name.")

    if len(username) > 40:
        raise ValueError("Profile name must be 40 characters or fewer.")

    return username


def create_profile(username):
    """Create a profile if it does not already exist."""

    username = normalize_username(username)

    now = datetime.now(timezone.utc).isoformat()

    with get_connection() as connection:
        connection.execute(
            """
            INSERT OR IGNORE INTO user_profiles
            (username, created_at)
            VALUES (?, ?)
            """,
            (username, now),
        )

    return username


def get_profiles():
    """Return all locally stored profile names."""

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT username
            FROM user_profiles
            ORDER BY username COLLATE NOCASE
            """
        ).fetchall()

    return [row["username"] for row in rows]


def save_rating(username, movie_id, rating):
    """Save a rating or update the existing rating."""

    username = create_profile(username)

    movie_id = int(movie_id)
    rating = float(rating)

    if not 0.5 <= rating <= 5.0:
        raise ValueError("Rating must be between 0.5 and 5.0.")

    if round(rating * 2) != rating * 2:
        raise ValueError("Ratings must use increments of 0.5.")

    now = datetime.now(timezone.utc).isoformat()

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO user_ratings
                (username, movie_id, rating, updated_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(username, movie_id)
            DO UPDATE SET
                rating = excluded.rating,
                updated_at = excluded.updated_at
            """,
            (username, movie_id, rating, now),
        )


def get_user_ratings(username):
    """Return all ratings saved by a profile."""

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT movie_id, rating, updated_at
            FROM user_ratings
            WHERE username = ?
            ORDER BY updated_at DESC
            """,
            (username,),
        ).fetchall()

    return [dict(row) for row in rows]


def remove_rating(username, movie_id):
    """Delete a user's rating for a movie."""

    with get_connection() as connection:
        connection.execute(
            """
            DELETE FROM user_ratings
            WHERE username = ? AND movie_id = ?
            """,
            (username, int(movie_id)),
        )


def add_to_watchlist(username, movie_id):
    """Save a movie to a user's watchlist."""

    username = create_profile(username)

    now = datetime.now(timezone.utc).isoformat()

    with get_connection() as connection:
        connection.execute(
            """
            INSERT OR IGNORE INTO watchlist
                (username, movie_id, added_at)
            VALUES (?, ?, ?)
            """,
            (username, int(movie_id), now),
        )


def get_watchlist(username):
    """Return a user's saved movie IDs."""

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT movie_id, added_at
            FROM watchlist
            WHERE username = ?
            ORDER BY added_at DESC
            """,
            (username,),
        ).fetchall()

    return [dict(row) for row in rows]


def remove_from_watchlist(username, movie_id):
    """Remove a movie from a user's watchlist."""

    with get_connection() as connection:
        connection.execute(
            """
            DELETE FROM watchlist
            WHERE username = ? AND movie_id = ?
            """,
            (username, int(movie_id)),
        )


def get_user_stats(username):
    """Return basic profile statistics."""

    with get_connection() as connection:

        rating_count = connection.execute(
            """
            SELECT COUNT(*)
            FROM user_ratings
            WHERE username = ?
            """,
            (username,),
        ).fetchone()[0]

        watchlist_count = connection.execute(
            """
            SELECT COUNT(*)
            FROM watchlist
            WHERE username = ?
            """,
            (username,),
        ).fetchone()[0]

        average_rating = connection.execute(
            """
            SELECT AVG(rating)
            FROM user_ratings
            WHERE username = ?
            """,
            (username,),
        ).fetchone()[0]

    return {
        "rating_count": rating_count,
        "watchlist_count": watchlist_count,
        "average_rating": (
            round(average_rating, 2)
            if average_rating is not None
            else None
        ),
    }