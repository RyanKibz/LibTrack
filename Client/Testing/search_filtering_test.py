import pytest
from Client.Search_filtering.search_filtering import SearchEngine


@pytest.fixture
def sample_catalog():
    return [
        {
            "title": "Atomic Habits",
            "author": "James Clear",
            "isbn": "9780385474542",
            "libraries": [
                {"name": "Nairobi Central", "available": True},
                {"name": "Community Library", "available": False}
            ]
        },
        {
            "title": "No Longer at Ease",
            "author": "Chinua Achebe",
            "isbn": "9780385043206",
            "libraries": [
                {"name": "University Library", "available": False}
            ]
        }
    ]


@pytest.fixture
def engine():
    return SearchEngine(catalog_file="dummy_path.json")


def test_search_by_title_found(engine, sample_catalog, mocker):
    mocker.patch.object(
        SearchEngine, 
        'load_catalog', 
        return_value=sample_catalog
    )
    results = engine.search_by_title("Atomic")
    
    assert len(results) == 1
    assert results[0]["title"] == "Atomic Habits"


def test_search_by_author_case_insensitive(engine, sample_catalog, mocker):
    mocker.patch.object(
        SearchEngine, 
        'load_catalog', 
        return_value=sample_catalog
    )
    results = engine.search_by_author("james clear")
    
    assert len(results) == 1
    assert results[0]["author"] == "James Clear"


def test_search_by_isbn(engine, sample_catalog, mocker):
    mocker.patch.object(
        SearchEngine, 
        'load_catalog', 
        return_value=sample_catalog
    )
    results = engine.search_by_isbn("9780385474542")
    
    assert len(results) == 1
    assert results[0]["author"] == "James Clear"


def test_filter_available_only(engine, sample_catalog):
    filtered = engine.filter_available_only(sample_catalog)
    
    # Only "Atomic Habits" has an available library copy
    assert len(filtered) == 1
    assert len(filtered[0]["libraries"]) == 1
    assert filtered[0]["libraries"][0]["name"] == "Nairobi Central"