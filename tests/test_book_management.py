from services.librarian_service import LibrarianService
import pytest

def test_librarian_can_update_book_availability():
    service = LibrarianService()

    service.add_book(
        "Things Fall Apart",
        "Chinua Achebe",
        "9780385474542",
        "Fiction"
    )

    book = service.update_availability(
        "9780385474542",
        "Unavailable"
    )

    assert book.availability == "Unavailable"

def test_cannot_update_unknown_book():
    service = LibrarianService()

    with pytest.raises(ValueError):
        service.update_availability(
            "9999999999999",
            "Unavailable"
        )


def update_book_details():
    service = LibrarianService()

    service.add_book(
        "Things Fall Apart",
        "Chinua Achebe",
        "9780385474542",
        "Fiction"
    )
    book = service.update_book(
        "",
        "African Literature"
    )
    assert book.category == "African Literature"

def cannot_use_invalid_availability():
    service = LibrarianService()

    service.add_book(
      "Things Fall Apart",
        "Chinua Achebe",
        "9780385474542",
        "Fiction"   
    )
    with pytest.raises(ValueError):
        service.update_availability(
            "9780385474542",
            "Banana"
        )
