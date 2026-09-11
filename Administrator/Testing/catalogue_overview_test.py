import pytest
from Administrator.Catalogue_overview.catalogue_overview import get_global_catalogue


@pytest.fixture
def all_libraries_catalogue():
    return [
        {
            "book_id": 1,
            "title": "Clean Code",
            "isbn": "9780132350884",
            "library_id": 10,
            "library_name": "Central Library",
            "available_copies": 3,
        },
        {
            "book_id": 2,
            "title": "Design Patterns",
            "isbn": "9780201633610",
            "library_id": 11,
            "library_name": "Westside Branch",
            "available_copies": 1,
        },
    ]


def test_view_global_catalogue(all_libraries_catalogue):
    """View catalogue information across all registered libraries."""
    catalogue = get_global_catalogue(all_libraries_catalogue)
    assert len(catalogue) == 2
    assert catalogue[0]["library_name"] == "Central Library"
    assert catalogue[1]["title"] == "Design Patterns"


def test_filter_global_catalogue_by_library(all_libraries_catalogue):
    """Filter catalogue across specific libraries."""
    filtered_catalogue = get_global_catalogue(all_libraries_catalogue, library_id=10)
    assert len(filtered_catalogue) == 1
    assert filtered_catalogue[0]["library_id"] == 10