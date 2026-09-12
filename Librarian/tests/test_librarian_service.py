import pytest
from services.librarian_service import LibrarianService


def test_librarian_can_add_book(tmp_path):
    test_file = tmp_path / "books.json"
    manage = LibrarianService(test_file)

    book = manage.add_book(
        "Things Fall Apart",
        "Chinua Achebe",
        "9780385474542",
        "Fiction"
    )

    assert book.title == "Things Fall Apart"