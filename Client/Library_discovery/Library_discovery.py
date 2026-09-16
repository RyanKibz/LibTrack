import json


class LibraryDiscovery:
    """Handles displaying books and their library information."""

    def __init__(self, branches_file="branches.json"):
        self.branches_file = branches_file

    def load_branches(self):
        try:
            with open(self.branches_file, "r") as file:
                data = json.load(file)
                return data.get("branches", [])

        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def get_branch_name(self, branch_id):
        branches = self.load_branches()

        for branch in branches:
            if branch.get("id") == branch_id:
                return branch.get("name", "Unknown Library")

        return "Unknown Library"

    def display_results(self, search_results):
        if not search_results:
            print("\nNo books found matching your search.")
            return

        print("\n--- SEARCH RESULTS ---")

        for book in search_results:
            branch_id = book.get("branch_id", "N/A")
            branch_name = self.get_branch_name(branch_id)

            print("\n" + "-" * 50)
            print(f"Title: {book.get('title', 'N/A')}")
            print(f"Author: {book.get('author', 'N/A')}")
            print(f"ISBN: {book.get('isbn', 'N/A')}")
            print(f"Category: {book.get('category', 'N/A')}")
            print(f"Library: {branch_name}")
            print(f"Branch ID: {branch_id}")
            print(f"Availability: {book.get('availability', 'Unknown')}")

        print("-" * 50)

    def view_library_details(self, branch_id):
        branches = self.load_branches()

        for branch in branches:
            if branch.get("id") == branch_id:
                print("\n--- LIBRARY DETAILS ---")
                print(f"Branch ID: {branch.get('id', 'N/A')}")
                print(f"Name: {branch.get('name', 'N/A')}")

                if branch.get("location"):
                    print(f"Location: {branch.get('location')}")

                return branch

        print(f"\nLibrary with Branch ID '{branch_id}' not found.")
        return None