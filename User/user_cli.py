
from Client.Authentication.authentication import register_client
from Client.BookSearch.booksearch import search_books
from Client.BookDetails.bookdetails import get_book_details



LIBRARIES = [
    {"library_name": "Nairobi Central Library", "location": "Nairobi CBD", "contact": "020-1234567"},
    {"library_name": "Westlands Community Library", "location": "Westlands", "contact": "020-7654321"},
]

BOOKS = [
    {
        "id": 1,
        "title": "Things Fall Apart",
        "author": "Chinua Achebe",
        "isbn": "9780435905255",
        "category": "Fiction",
        "libraries": [
            {**LIBRARIES[0], "status": "available"},
            {**LIBRARIES[1], "status": "checked out"},
        ],
    },
    {
        "id": 2,
        "title": "Half of a Yellow Sun",
        "author": "Chimamanda Ngozi Adichie",
        "isbn": "9780007200283",
        "category": "Fiction",
        "libraries": [
            {**LIBRARIES[0], "status": "available"},
        ],
    },
]

USERS = []


def print_book_summary(book):
    print(f"  [{book['id']}] {book['title']} by {book['author']} (ISBN: {book['isbn']})")


def handle_register():
    print("\n Register a new account ")
    username = input("Username: ").strip()
    email = input("Email: ").strip()
    password = input("Password: ").strip()

    result = register_client(
        username=username, email=email, password=password, existing_users=USERS
    )

    if result["success"]:
        USERS.append(result["user"])
        print(f"Registered successfully! Welcome, {username}.")
    else:
        print(f"Registration failed: {result['error']}")


def handle_search():
    print("\n Search books ")
    query = input("Search by title, author, or ISBN: ").strip()
    results = search_books(query=query, books=BOOKS)

    if not results:
        print("No books matched your search.")
        return

    print(f"\nFound {len(results)} result(s):")
    for book in results:
        print_book_summary(book)


def handle_details():
    print("\n View book details ")
    raw_id = input("Enter book ID: ").strip()

    try:
        book_id = int(raw_id)
    except ValueError:
        print("Please enter a numeric book ID.")
        return

    details = get_book_details(book_id=book_id, books=BOOKS)

    if details is None:
        print("Book not found.")
        return

    print(f"\nTitle:    {details['title']}")
    print(f"Author:   {details['author']}")
    print(f"ISBN:     {details['isbn']}")
    print(f"Category: {details['category']}")
    print("Availability by library:")
    for lib in details["libraries"]:
        print(f"  - {lib['library_name']} ({lib['location']}): {lib['status']}")


def main():
    actions = {
        "1": handle_register,
        "2": handle_search,
        "3": handle_details,
    }

    while True:
        print("\n LibTrack Client CLI ")
        print("1. Register a new account")
        print("2. Search for a book")
        print("3. View book details")
        print("4. Exit")

        choice = input("Select an option (1-4): ").strip()

        if choice == "4":
            print("Goodbye!")
            break

        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid option, please choose 1-4.")


if __name__ == "__main__":
    main()