import json

class SearchEngine:
    """Handles searching the catalog by Title, Author, ISBN, and filtering available copies."""
    def __init__(self, catalog_file="data/catalog.json"):
        self.catalog_file = catalog_file

    def load_catalog(self):
        """Loads catalog data from JSON file."""
        try:
            with open(self.catalog_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def search_by_title(self, query):
        """Search books by title (case-insensitive substring)."""
        catalog = self.load_catalog()
        return [book for book in catalog if query.lower() in book.get('title', '').lower()]

    def search_by_author(self, query):
        """Search books by author name (case-insensitive substring)."""
        catalog = self.load_catalog()
        return [book for book in catalog if query.lower() in book.get('author', '').lower()]

    def search_by_isbn(self, query):
        """Search books by exact ISBN match."""
        catalog = self.load_catalog()
        return [book for book in catalog if query.strip() == book.get('isbn', '').strip()]

    def filter_available_only(self, results):
        """Filters results to include only libraries with available copies."""
        filtered_results = []
        for book in results:
            available_libraries = [
                lib for lib in book.get('libraries', []) if lib.get('available', False)
            ]
            if available_libraries:
                book_copy = book.copy()
                book_copy['libraries'] = available_libraries
                filtered_results.append(book_copy)
        return filtered_results


# PUT IT HERE (At the bottom, touching the left margin)
if __name__ == "__main__":
    engine = SearchEngine()
    print("Testing SearchEngine directly...")

    sample_catalog = [
        {
            "title": "Atomic Habits",
            "author": "James Clear",
            "isbn": "9780385474542",
            "libraries": [
                {"name": "Nairobi Central", "available": True},
                {"name": "Community Library", "available": False}
            ]
        }
    ]

    engine.load_catalog = lambda: sample_catalog

    results = engine.search_by_title("Atomic")
    print(f"Results found: {len(results)}")
    if results:
        print(f"Found book: {results[0]['title']} by {results[0]['author']}")