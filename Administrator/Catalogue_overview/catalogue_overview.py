import sys
from typing import Any, Dict, List, Optional


def get_global_catalogue(
    catalogue: List[Dict[str, Any]], library_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Return catalogue entries across all libraries."""
    if library_id is None:
        return catalogue

    return [entry for entry in catalogue if entry.get("library_id") == library_id]


def display_catalogue(entries: List[Dict[str, Any]]) -> None:
    #Print catalogue entries in a readable table
    if not entries:
        print("\n  No catalogue entries found.")
        return

    print("\n" + "=" * 60)
    print(f"{'ID':<8} {'Library':<12} {'Title':<25} {'Author'}")
    print("=" * 60)
    for item in entries:
        book_id = str(item.get("id", "N/A"))
        lib_id = str(item.get("library_id", "N/A"))
        title = item.get("title", "Unknown Title")
        author = item.get("author", "Unknown Author")
        print(f"{book_id:<8} {lib_id:<12} {title:<25} {author}")
    print("=" * 60)


def catalogue_cli(catalogue: List[Dict[str, Any]]):
    # view and filter catalogue entries.
    while True:
        print("\n--- Global Catalogue Management ---")
        print("1. View all entries")
        print("2. Filter entries by Library ID")
        print("3. Exit to Main Menu")

        choice = input("\nSelect an option (1-3): ").strip()

        if choice == "1":
            entries = get_global_catalogue(catalogue)
            print(f"\nShowing all entries ({len(entries)} total):")
            display_catalogue(entries)

        elif choice == "2":
            lib_id = input("Enter Library ID to filter by: ").strip()
            entries = get_global_catalogue(catalogue, library_id=lib_id)
            print(f"\nShowing entries for Library ID '{lib_id}' ({len(entries)} found):")
            display_catalogue(entries)

        elif choice == "3":
            print("Exiting catalogue view.")
            break

        else:
            print("Invalid selection. Please choose options 1 to 3.")


if __name__ == "__main__":
    LIB_CATALOGUE = [
        {"id": "B1", "library_id": "L01", "title": "The River and The Source", "author": "Magrate A. Ogolla"},
        {"id": "B2", "library_id": "L01", "title": "Chozi la Heri", "author": "ASumpta K."},
        {"id": "B3", "library_id": "L02", "title": "The Pearl", "author": "Anastacia A."},
        {"id": "B4", "library_id": "L03", "title": "Dune", "author": "Frank Herbert"},
    ]

    try:
        catalogue_cli(LIB_CATALOGUE)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled. Exiting...")
        sys.exit(0)
