import json


class SearchEngine:
    def __init__(self, catalog_file="Librarian/data/books.json"):
        self.catalog_file = catalog_file

    def load_catalog(self):
        
        try:
            with open(self.catalog_file, "r") as file:
                return json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def search_by_title(self, query):
        catalog = self.load_catalog()

        return [
            book for book in catalog
            if query.lower() in book.get("title", "").lower()
        ]

    def search_by_author(self, query):
        catalog = self.load_catalog()

        return [
            book for book in catalog
            if query.lower() in book.get("author", "").lower()
        ]

    def search_by_isbn(self, query):
        catalog = self.load_catalog()

        return [
            book for book in catalog
            if query.strip() == book.get("isbn", "").strip()
        ]

    def filter_available_only(self, results):
        return [
            book for book in results
            if book.get("availability") == "Available"
        ]