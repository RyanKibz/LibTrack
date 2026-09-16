from Client.Authentication.authentication import register_client
from Client.BookSearch.booksearch import search_books
from Client.BookDetails.bookdetails import get_book_details
from Client.Search_filtering.search_filtering import SearchEngine
from Client.Library_discovery.Library_discovery import LibraryDiscovery
from Librarian.Authentication.authentication import librarian_login
from Librarian.services.librarian_service import LibrarianService
import json

from Administrator.Authentication.authentication import (
    _authenticate,
    create_branch,
    update_branch,
    remove_branch,
)
from Administrator.UserManagement.userManagement import (
    get_all_users,
    create_user,
    update_user,
    deactivate_user,
    assign_role,
)
from Administrator.Catalogue_overview.catalogue_overview import (
    get_global_catalogue,
    display_catalogue,
)

BRANCHES_FILE = "branches.json"
BOOKS_FILE = "Librarian/data/books.json"

def load_system_data():
    try:
        with open(BRANCHES_FILE, "r") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "branches": [],
            "users": []
        }
def save_system_data(data):
    with open(BRANCHES_FILE, "w") as file:
        json.dump(data, file, indent=4)


def load_books():
    try:
        with open(BOOKS_FILE, "r") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return []

def client_registration():
    data = load_system_data()
    users = data.get("users", [])

    print("\n--- CLIENT REGISTRATION ---")

    username = input("Username: ").strip()
    email = input("Email: ").strip()
    password = input("Password: ").strip()

    result = register_client(
        username,
        email,
        password,
        users
    )

    if result["success"]:
        new_user = result["user"]

        new_user["id"] = max(
            (user.get("id", 0) for user in users),
            default=0
        ) + 1

        new_user["role"] = "Client"
        new_user["is_active"] = True

        users.append(new_user)

        data["users"] = users
        save_system_data(data)

        print("\nRegistration successful.")
        return new_user

    print(f"\nRegistration failed: {result['error']}")
    return None


def client_login():
    data = load_system_data()
    users = data.get("users", [])
    print("\n--- CLIENT LOGIN ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    import hashlib
    hashed_password = hashlib.sha256(
        password.encode()
    ).hexdigest()
    for user in users:
        if (
            user.get("username") == username
            and user.get("password") == hashed_password
            and user.get("role") == "Client"
            and user.get("is_active", True)
        ):
            print(f"\nWelcome, {username}!")
            return user

    print("\nInvalid username or password.")
    return None

def client_search():
    engine = SearchEngine()
    discovery = LibraryDiscovery()
    while True:
        print("\n--- SEARCH BOOKS ---")
        print("1. Search by Title")
        print("2. Search by Author")
        print("3. Search by ISBN")
        print("4. Back")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            query = input("Enter book title: ").strip()
            results = engine.search_by_title(query)
            discovery.display_results(results)
        elif choice == "2":
            query = input("Enter author: ").strip()
            results = engine.search_by_author(query)
            discovery.display_results(results)
        elif choice == "3":
            query = input("Enter ISBN: ").strip()
            results = engine.search_by_isbn(query)
            discovery.display_results(results)
        elif choice == "4":
            break
        else:
            print("Invalid option.")

def client_available_books():
    engine = SearchEngine()
    discovery = LibraryDiscovery()
    query = input(
        "\nEnter book title to find available copies: "
    ).strip()
    results = engine.search_by_title(query)
    available = engine.filter_available_only(results)
    discovery.display_results(available)

def client_book_details():
    books = load_books()
    if not books:
        print("\nNo books available.")
        return
    isbn = input("Enter ISBN: ").strip()
    book = None
    for item in books:
        if item.get("isbn") == isbn:
            book = item
            break
    if not book:
        print("\nBook not found.")
        return
    discovery = LibraryDiscovery()
    discovery.display_results([book])


def client_library_details():
    discovery = LibraryDiscovery()
    branch_id = input(
        "Enter Library Branch ID: "
    ).strip()
    discovery.view_library_details(branch_id)

def client_menu():
    while True:
        print("\n" + "=" * 40)
        print("             CLIENT MENU")
        print("=" * 40)
        print("1. Search Books")
        print("2. Find Available Books")
        print("3. View Book Details")
        print("4. View Library Details")
        print("5. Logout")
        choice = input("\nChoose an option: ").strip()
        if choice == "1":
            client_search()
        elif choice == "2":
            client_available_books()
        elif choice == "3":
            client_book_details()
        elif choice == "4":
            client_library_details()
        elif choice == "5":
            print("\nClient logged out.")
            break
        else:
            print("Invalid option.")

def client_access():
    while True:
        print("\n--- CLIENT ACCESS ---")
        print("1. Register")
        print("2. Login")
        print("3. Back")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            user = client_registration()
            if user:
                client_menu()
        elif choice == "2":
            user = client_login()
            if user:
                client_menu()
        elif choice == "3":
            break
        else:
            print("Invalid option.")

def librarian_menu():
    manage = LibrarianService()
    while True:
        print("\n" + "=" * 40)
        print("           LIBRARIAN MENU")
        print("=" * 40)
        print("1. Add Book")
        print("2. View Catalogue")
        print("3. Search Book")
        print("4. Update Availability")
        print("5. Update Book Category")
        print("6. Archive Book")
        print("7. Logout")
        choice = input("\nChoose an option: ").strip()
        if choice == "1":
            title = input("Enter book title: ").strip()
            author = input("Enter author: ").strip()
            isbn = input("Enter ISBN: ").strip()
            category = input("Enter category: ").strip()
            branch_id = input("Enter Branch ID: ").strip()
            try:
                book = manage.add_book(
                    title,
                    author,
                    isbn,
                    category,
                    branch_id
                )
                print(
                    f"\n{book.title} added successfully."
                )
            except ValueError as error:
                print(f"\nError: {error}")
        elif choice == "2":
            books = manage.view_catalogue()
            if not books:
                print("\nCatalogue is empty.")
            else:
                print("\n--- CATALOGUE ---")
                for book in books:
                    print(
                        f"{book.title} | "
                        f"{book.author} | "
                        f"{book.isbn} | "
                        f"{book.category} | "
                        f"{book.branch_id} | "
                        f"{book.availability}"
                    )
        elif choice == "3":
            search_term = input(
                "Enter title, author or ISBN: "
            ).strip()
            results = manage.search_books(search_term)
            if not results:
                print("\nNo books found.")
            else:
                for book in results:
                    print(
                        f"{book.title} | "
                        f"{book.author} | "
                        f"{book.isbn} | "
                        f"{book.branch_id} | "
                        f"{book.availability}"
                    )
        elif choice == "4":
            isbn = input("Enter ISBN: ").strip()
            status = input(
                "Enter status "
                "(Available/Unavailable/Missing/Archived): "
            ).strip()
            try:
                book = manage.update_availability(
                    isbn,
                    status
                )
                print(
                    f"\n{book.title} is now "
                    f"{book.availability}."
                )
            except ValueError as error:
                print(f"\nError: {error}")
        elif choice == "5":
            isbn = input("Enter ISBN: ").strip()

            category = input(
                "Enter new category: "
            ).strip()
            try:
                book = manage.update_book(
                    isbn,
                    category
                )
                print(
                    f"\n{book.title} category updated "
                    f"to {book.category}."
                )
            except ValueError as error:
                print(f"\nError: {error}")
        elif choice == "6":
            isbn = input("Enter ISBN: ").strip()
            try:
                book = manage.archive_book(isbn)
                print(
                    f"\n{book.title} has been archived."
                )
            except ValueError as error:
                print(f"\nError: {error}")
        elif choice == "7":
            print("\nLibrarian logged out.")
            break
        else:
            print("Invalid option.")

def librarian_access():
    user = librarian_login()
    if user:
        librarian_menu()

def admin_branch_management():
    data = load_system_data()
    branch_list = data.get("branches", [])
    branches = {
        branch["id"]: branch["name"]
        for branch in branch_list
    }
    admin_user = {
        "is_admin": True
    }
    while True:
        print("\n--- BRANCH MANAGEMENT ---")
        print("1. List Branches")
        print("2. Create Branch")
        print("3. Update Branch")
        print("4. Remove Branch")
        print("5. Back")
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                if not branches:
                    print("\nNo branches registered.")
                else:
                    print("\nRegistered Branches:")
                    for branch_id, name in branches.items():
                        print(
                            f"{branch_id} | {name}"
                        )
            elif choice == "2":
                branch_id = input(
                    "Enter Branch ID: "
                ).strip()
                name = input(
                    "Enter Branch Name: "
                ).strip()
                message = create_branch(
                    admin_user,
                    branch_id,
                    name,
                    branches
                )
                print(message)
            elif choice == "3":
                branch_id = input(
                    "Enter Branch ID: "
                ).strip()
                name = input(
                    "Enter new Branch Name: "
                ).strip()
                message = update_branch(
                    admin_user,
                    branch_id,
                    name,
                    branches
                )
                print(message)
            elif choice == "4":
                branch_id = input(
                    "Enter Branch ID: "
                ).strip()
                message = remove_branch(
                    admin_user,
                    branch_id,
                    branches
                )
                print(message)
            elif choice == "5":
                break
            else:
                print("Invalid option.")
                continue
            data["branches"] = [
                {
                    "id": branch_id,
                    "name": name
                }
                for branch_id, name in branches.items()
            ]
            save_system_data(data)
        except (
            PermissionError,
            ValueError,
            KeyError
        ) as error:
            print(f"Error: {error}")

def admin_user_management():
    data = load_system_data()
    users = data.get("users", [])
    while True:
        print("\n--- USER MANAGEMENT ---")
        print("1. List Users")
        print("2. Create User")
        print("3. Update User")
        print("4. Assign Role")
        print("5. Deactivate User")
        print("6. Back")
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                all_users = get_all_users(users)
                if not all_users:
                    print("\nNo users registered.")
                for user in all_users:
                    status = (
                        "Active"
                        if user.get("is_active", True)
                        else "Inactive"
                    )
                    print(
                        f"ID: {user.get('id')} | "
                        f"Name: "
                        f"{user.get('name', user.get('username', 'N/A'))} | "
                        f"Role: {user.get('role', 'N/A')} | "
                        f"Status: {status}"
                    )
            elif choice == "2":
                name = input("Name: ").strip()
                role = input(
                    "Role (Client/Librarian/Admin): "
                ).strip()
                new_user = create_user(
                    {
                        "name": name,
                        "role": role
                    },
                    users
                )
                print(
                    f"User created. "
                    f"ID: {new_user['id']}"
                )
            elif choice == "3":
                user_id = int(
                    input("Enter User ID: ")
                )
                field = input(
                    "Field to update: "
                ).strip()
                value = input(
                    "New value: "
                ).strip()
                update_user(
                    user_id,
                    {field: value},
                    users
                )
                print("User updated.")
            elif choice == "4":
                user_id = int(
                    input("Enter User ID: ")
                )
                role = input(
                    "Enter new role: "
                ).strip()
                assign_role(
                    user_id,
                    role,
                    users
                )
                print("Role updated.")
            elif choice == "5":
                user_id = int(
                    input("Enter User ID: ")
                )
                deactivate_user(
                    user_id,
                    users
                )
                print("User deactivated.")
            elif choice == "6":
                break
            else:
                print("Invalid option.")
                continue
            data["users"] = users
            save_system_data(data)
        except ValueError:
            print("User ID must be an integer.")
        except KeyError as error:
            print(f"Error: {error}")

def admin_catalogue():
    catalogue = load_books()
    entries = get_global_catalogue(catalogue)
    print(
        f"\nGlobal Catalogue "
        f"({len(entries)} books)"
    )
    display_catalogue(entries)

def administrator_menu():
    while True:
        print("\n" + "=" * 40)
        print("         ADMINISTRATOR MENU")
        print("=" * 40)
        print("1. Manage Users")
        print("2. Manage Libraries")
        print("3. View Global Catalogue")
        print("4. Logout")
        choice = input(
            "\nChoose an option: "
        ).strip()
        if choice == "1":
            admin_user_management()
        elif choice == "2":
            admin_branch_management()
        elif choice == "3":
            admin_catalogue()
        elif choice == "4":
            print("\nAdministrator logged out.")
            break
        else:
            print("Invalid option.")

def administrator_access():
    print("\n--- ADMINISTRATOR LOGIN ---")
    user = _authenticate()
    if user.get("is_admin"):
        print(
            f"\nWelcome, {user['username']}!"
        )
        administrator_menu()
    else:
        print(
            "\nAccess denied. "
            "Invalid administrator credentials."
        )

def main():
    while True:
        print("\n" + "=" * 45)
        print("                LIBTRACK")
        print("        Library Control System")
        print("=" * 45)
        print("1. Client")
        print("2. Librarian")
        print("3. Administrator")
        print("4. Exit")
        choice = input(
            "\nChoose an option: "
        ).strip()
        if choice == "1":
            client_access()

        elif choice == "2":
            librarian_access()

        elif choice == "3":
            administrator_access()

        elif choice == "4":
            print(
                "\nThank you for using LibTrack. "
                "Goodbye!"
            )
            break
        else:
            print(
                "\nInvalid option. "
                "Please choose 1 to 4."
            )

if __name__ == "__main__":
    main()