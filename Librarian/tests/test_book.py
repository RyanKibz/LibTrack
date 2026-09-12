import pytest
from models.book import Book
from services.librarian_service import LibrarianService

def test_create_book():
    book = Book(
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

def test_book_requires_title():
    with pytest.raises(ValueError):
        Book(
            "",
            "Chinua Achebe",
            "9780385474542",
            "Fiction"
        )