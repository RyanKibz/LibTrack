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
def test_librarian_can_search_book_by_author():
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

    results = service.search_books("Chinua Achebe")

    assert len(results) == 1
    assert results[0].author == "Chinua Achebe"

def test_librarian_can_search_book_by_isbn():
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

    results = service.search_books("9780385474542")

    assert len(results) == 1
    assert results[0].isbn == "9780385474542"

def test_search_returns_empty_list_when_book_not_found():
    service = LibrarianService()

    service.add_book(
        "Things Fall Apart",
        "Chinua Achebe",
        "9780385474542",
        "Fiction"
    )

    results = service.search_books("Harry Potter")

    assert results == []