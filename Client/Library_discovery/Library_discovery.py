import json

class LibraryDiscovery:
    """Handles displaying search results, formatting availability, and showing library details."""
    def __init__(self, libraries_file="data/libraries.json"):
        self.libraries_file = libraries_file

    def load_libraries(self):
        try:
            with open(self.libraries_file, 'r') as f:
                data = json.load(f)
                return {lib['id']: lib for lib in data}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def display_results(self, search_results):
        """Prints formatted search results and availability matrix."""
        if not search_results:
            print("\nNo libraries found matching your search query.")
            return

        for book in search_results:
            print(f"\nTitle:  {book.get('title', 'N/A')}")
            print(f"Author: {book.get('author', 'N/A')} | ISBN: {book.get('isbn', 'N/A')}")
            print("-" * 48)
            print(f"{'Library':<28} {'Availability':<20}")
            print("-" * 48)
            for lib_status in book.get('libraries', []):
                status = "Available" if lib_status.get('available') else "Not Available"
                print(f"{lib_status.get('name', 'N/A'):<28} {status:<20}")
            print("-" * 48)

    def view_library_details(self, library_id):
        """Displays full information for a specific library ID."""
        libraries = self.load_libraries()
        lib = libraries.get(library_id)

        if not lib:
            print(f"\nLibrary ID '{library_id}' not found.")
            return

        print("=" * 48)


# NO INDENTATION - Start completely flush against the left margin:
if __name__ == "__main__":
    discovery = LibraryDiscovery()

    print("Testing LibraryDiscovery class directly...")
    sample_data = [{
        "title": "Atomic Habits",
        "author": "James Clear",
        "isbn": "978038547542",
        "libraries": [{"name": "Nairobi Central", "available": True}]
    }]
    discovery.display_results(sample_data)
       