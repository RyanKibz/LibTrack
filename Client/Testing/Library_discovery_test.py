import pytest
from Client.Library_discovery.Library_discovery import LibraryDiscovery


@pytest.fixture
def sample_libraries():
    return {
        "LIB01": {
            "id": "LIB01",
            "name": "Nairobi Central",
            "address": "123 Processional Way",
            "contact": "+254700000000",
            "hours": "8 AM - 5 PM"
        }
    }


@pytest.fixture
def discovery():
    return LibraryDiscovery(libraries_file="dummy_path.json")


def test_display_results_empty(discovery, capsys):
    discovery.display_results([])
    captured = capsys.readouterr()
    
    assert "No libraries found matching your search query." in captured.out


def test_display_results_success(discovery, capsys):
    sample_results = [{
        "title": "Atomic Habits",
        "author": "James Clear",
        "isbn": "9780385474542",
        "libraries": [
            {"name": "Nairobi Central", "available": True}
        ]
    }]
    
    discovery.display_results(sample_results)
    captured = capsys.readouterr()
    
    assert "Atomic Habits" in captured.out
    assert "Nairobi Central" in captured.out
    assert "Available" in captured.out


def test_view_library_details_found(discovery, sample_libraries, mocker, capsys):
    mocker.patch.object(
        LibraryDiscovery, 
        'load_libraries', 
        return_value=sample_libraries
    )
    
    discovery.view_library_details("LIB01")
    captured = capsys.readouterr()
    
    assert "LIBRARY DETAILS: Nairobi Central" in captured.out
    assert "123 Processional Way" in captured.out


def test_view_library_details_not_found(discovery, sample_libraries, mocker, capsys):
    mocker.patch.object(
        LibraryDiscovery, 
        'load_libraries', 
        return_value=sample_libraries
    )
    
    discovery.view_library_details("LIB99")
    captured = capsys.readouterr()
    
    assert "Library ID 'LIB99' not found." in captured.out