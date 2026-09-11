import pytest
from Client.BookSearch.booksearch import search_books


def test_search_by_title_returns_matches(sample_books):
    results = search_books(query="Things Fall Apart", books=sample_books)
    assert len(results) == 1
    assert results[0]["title"] == "Things Fall Apart"


def test_search_by_author_returns_matches(sample_books):
    results = search_books(query="Adichie", books=sample_books)
    assert len(results) == 1
    assert results[0]["author"] == "Chimamanda Ngozi Adichie"


def test_search_by_isbn_returns_exact_match(sample_books):
    results = search_books(query="9780435905255", books=sample_books)
    assert len(results) == 1
    assert results[0]["isbn"] == "9780435905255"


def test_search_results_include_library_and_availability(sample_books):
    results = search_books(query="Things Fall Apart", books=sample_books)
    assert "libraries" in results[0]
    assert results[0]["libraries"][0]["status"] in ("available", "checked out")


def test_search_no_results_returns_clear_message(sample_books):
    results = search_books(query="Nonexistent Book Title", books=sample_books)
    assert results == [] or "message" in results


def test_search_case_insensitive(sample_books):
    results = search_books(query="things fall apart", books=sample_books)
    assert len(results) == 1


def test_search_partial_title_match(sample_books):
    results = search_books(query="Yellow Sun", books=sample_books)
    assert len(results) == 1