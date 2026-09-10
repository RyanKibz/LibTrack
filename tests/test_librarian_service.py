import pytest
from services.librarian_service import LibrarianService

def test_librarian_can_add_book():
    service = LibrarianService()

    book = service.add_book(
        "Things Fall Apart",
        "Chinua Achebe",
        "9780385474542",
        "Fiction"
    )

    with pytest.raises(ValueError):
        service.add_book(
            "Things Fall Apart",
            "Chinua Achebe",
            "9780385474542",
            "African Literature"
        )

    assert book.title == "Things Fall Apart"
    assert book.author == "Chinua Achebe"
    assert book.isbn == "9780385474542"
    assert book.category == "Fiction"
    assert book.availability == "Available"


def test_added_book_is_in_catalogue():
    service = LibrarianService()

    book = service.add_book(
        "Things Fall Apart",
        "Chinua Achebe",
        "9780385474542",
        "Fiction"
    )

    assert book in service.books
    assert len(service.books) == 1


def librarian_can_view_catalogue():
    service = LibrarianService()

    service.add_book(
        "Things Fall Apart",
        "Chinua Achebe",
        "9780385474542",
        "Fiction"
    )
    service.add_book(
         "The River Between",
        "Ngugi wa Thiong'o",
        "9780435905484",
        "Fiction"
    )
    books = service.view_catalogue()

    assert len(books) == 2

def test_empty_catalogue_returns_empty_list():
    manage = LibrarianService()

    books = manage.view_catalogue()

    assert books == []