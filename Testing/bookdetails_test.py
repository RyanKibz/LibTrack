import pytest
from Client.BookDetails.bookdetails import get_book_details


def test_view_book_details_returns_full_info(sample_books):
    details = get_book_details(book_id=1, books=sample_books)
    assert details["title"] == "Things Fall Apart"
    assert details["author"] == "Chinua Achebe"
    assert details["isbn"] == "9780435905255"


def test_view_book_details_lists_all_libraries_holding_it(sample_books):
    details = get_book_details(book_id=1, books=sample_books)
    assert len(details["libraries"]) == 2


def test_view_book_details_shows_per_library_availability(sample_books):
    details = get_book_details(book_id=1, books=sample_books)
    statuses = [lib["status"] for lib in details["libraries"]]
    assert "available" in statuses
    assert "checked out" in statuses


def test_view_nonexistent_book_returns_404(sample_books):
    details = get_book_details(book_id=999, books=sample_books)
    assert details is None or details.get("error") == "not found"