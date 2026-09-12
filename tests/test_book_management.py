from services.librarian_service import LibrarianService
import pytest

def test_librarian_can_update_book_availability():
    manage = LibrarianService()

    manage.add_book(
        "Things Fall Apart",
        "Chinua Achebe",
        "9780385474542",
        "Fiction"
    )

    book = manage.update_availability(
        "9780385474542",
        "Unavailable"
    )

    assert book.availability == "Unavailable"

def test_cannot_update_unknown_book():
    manage = LibrarianService()

    with pytest.raises(ValueError):
        manage.update_availability(
            "9999999999999",
            "Unavailable"
        )


def test_update_book_details():
    manage = LibrarianService()

    manage.add_book(
        "Things Fall Apart",
        "Chinua Achebe",
        "9780385474542",
        "Fiction"
    )
    book = manage.update_book(
        "9780385474542",
        "African Literature"
    )
    assert book.category == "African Literature"

def test_cannot_use_invalid_availability():
    manage = LibrarianService()

    manage.add_book(
      "Things Fall Apart",
        "Chinua Achebe",
        "9780385474542",
        "Fiction"   
    )
    with pytest.raises(ValueError):
        manage.update_availability(
            "9780385474542",
            "Banana"
        )
def test_librarian_can_archive_book():
    manage = LibrarianService()

    manage.add_book(
        "Things Fall Apart",
        "Chinua Achebe",
        "9780385474542",
        "Fiction"
    )

    book = manage.archive_book("9780385474542")

    assert book.availability == "Archive"