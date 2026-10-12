from src.tmdb_client import TMDBClient


def main():
    try:
        client = TMDBClient()

        print("Testing TMDB connection...")

        results = client.search_movies("Inception")

        if not results:
            print("Connection successful, but no movies were returned.")
            return

        print("\nTMDB connection successful!")
        print("\nSearch results:\n")

        for movie in results[:5]:
            print(
                f"Title: {movie.get('title')}\n"
                f"Release date: {movie.get('release_date', 'Unknown')}\n"
                f"TMDB rating: {movie.get('vote_average', 0)}\n"
                f"TMDB ID: {movie.get('id')}\n"
            )

    except (ValueError, RuntimeError) as exc:
        print(f"TMDB test failed: {exc}")


if __name__ == "__main__":
    main()