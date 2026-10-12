import pytest

from src.user_store import (
    initialize_database,
    create_profile,
    save_rating,
    get_user_ratings,
    add_to_watchlist,
    get_watchlist,
)


@pytest.fixture
def test_profile():
    initialize_database()

    username = "cinematch_test_user"

    create_profile(username)

    yield username


def test_save_rating(test_profile):
    save_rating(
        test_profile,
        movie_id=1,
        rating=4.5,
    )

    ratings = get_user_ratings(test_profile)

    assert any(
        row["movie_id"] == 1 and row["rating"] == 4.5
        for row in ratings
    )


def test_update_rating(test_profile):
    save_rating(test_profile, 2, 3.0)
    save_rating(test_profile, 2, 5.0)

    ratings = get_user_ratings(test_profile)

    matching = [
        row for row in ratings
        if row["movie_id"] == 2
    ]

    assert len(matching) == 1
    assert matching[0]["rating"] == 5.0


def test_invalid_rating(test_profile):
    with pytest.raises(ValueError):
        save_rating(test_profile, 3, 6.0)


def test_watchlist(test_profile):
    add_to_watchlist(test_profile, 10)

    watchlist = get_watchlist(test_profile)

    assert any(
        row["movie_id"] == 10
        for row in watchlist
    )