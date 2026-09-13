import pytest


@pytest.fixture
def sample_libraries():
    """A few libraries with book copies for testing search/details."""
    return [
        {"library_name": "Nairobi Central Library", "location": "Nairobi CBD", "contact": "020-1234567"},
        {"library_name": "Westlands Community Library", "location": "Westlands", "contact": "020-7654321"},
    ]


@pytest.fixture
def sample_books(sample_libraries):
    """A small in-memory catalogue for search/details tests."""
    return [
        {
            "id": 1,
            "title": "Things Fall Apart",
            "author": "Chinua Achebe",
            "isbn": "9780435905255",
            "category": "Fiction",
            "libraries": [
                {**sample_libraries[0], "status": "available"},
                {**sample_libraries[1], "status": "checked out"},
            ],
        },
        {
            "id": 2,
            "title": "Half of a Yellow Sun",
            "author": "Chimamanda Ngozi Adichie",
            "isbn": "9780007200283",
            "category": "Fiction",
            "libraries": [
                {**sample_libraries[0], "status": "available"},
            ],
        },
    ]


@pytest.fixture
def existing_users():
    """Pre-registered users to test uniqueness checks against.

    Matches the values used in clientauthentication_test.py's duplicate
    tests (username="jeff", email="jeff@gmail.com") so those tests
    actually exercise the duplicate-detection logic.
    """
    return [
        {"username": "jeff", "email": "jeff@gmail.com", "password": "hashed_pw_here"},
    ]