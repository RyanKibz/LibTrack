from services.librarian_service import LibrarianService


def test_librarian_can_search_book_by_title():
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

    results = service.search_books("Things Fall Apart")

    assert len(results) == 1
    assert results[0].title == "Things Fall Apart"