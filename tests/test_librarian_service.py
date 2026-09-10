import pytest
from services.librarian_service import librarian_service

def test_librarian_can_add_book():
    service = librarian_service()

    book = service.add_book(
        "Things Fall Apart",
        "Chinua Achebe",
        "9780385474542",
        "Fiction"
    )
    assert book.title == "Things Fall Apart"
    assert book.author == "Chinua Achebe"
    assert book.isbn == "9780385474542"
    assert book.category == "Fiction"
    assert book.availability == "Available"


def test_added_book_is_in_catalogue():
    service = librarian_service()

    book = service.add_book(
        "Things Fall Apart",
        "Chinua Achebe",
        "9780385474542",
        "Fiction"
    )

    assert book in service.books
    assert len(service.books) == 1