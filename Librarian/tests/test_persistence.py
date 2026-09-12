from services.librarian_service import LibrarianService


def test_book_is_saved_and_loaded(tmp_path):
    test_file = tmp_path / "books.json"

    manage = LibrarianService(test_file)

    manage.add_book(
        "Things Fall Apart",
        "Chinua Achebe",
        "9780385474542",
        "Fiction"
    )

    new_manage = LibrarianService(test_file)

    assert len(new_manage.books) == 1
    assert new_manage.books[0].title == "Things Fall Apart"


def test_updated_availability_is_saved(tmp_path):
    test_file = tmp_path / "books.json"

    manage = LibrarianService(test_file)

    manage.add_book(
        "Things Fall Apart",
        "Chinua Achebe",
        "9780385474542",
        "Fiction"
    )

    manage.update_availability(
        "9780385474542",
        "Unavailable"
    )

    new_manage = LibrarianService(test_file)

    assert new_manage.books[0].availability == "Unavailable"


def test_archived_book_is_saved(tmp_path):
    test_file = tmp_path / "books.json"

    manage = LibrarianService(test_file)

    manage.add_book(
        "Things Fall Apart",
        "Chinua Achebe",
        "9780385474542",
        "Fiction"
    )

    manage.archive_book("9780385474542")

    new_manage = LibrarianService(test_file)

    assert new_manage.books[0].availability == "Archived"
    