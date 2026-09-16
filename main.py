import json
import hashlib
from Client.Authentication.authentication import register_client
from Client.BookSearch.booksearch import search_books
from Client.BookDetails.bookdetails import get_book_details
from Client.Search_filtering.search_filtering import SearchEngine
from Client.Library_discovery.Library_discovery import LibraryDiscovery
from Librarian.Authentication.authentication import librarian_login
from Librarian.services.librarian_service import LibrarianService
from Administrator.Authentication.authentication import _authenticate, create_branch, update_branch, remove_branch
from Administrator.UserManagement.userManagement import get_all_users, create_user, update_user, deactivate_user, assign_role
from Administrator.Catalogue_overview.catalogue_overview import get_global_catalogue, display_catalogue

BRANCHES_FILE = "branches.json"
BOOKS_FILE = "Librarian/data/books.json"


def load_system_data():
    try:
        with open(BRANCHES_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"branches": [], "users": []}


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

    result = register_client(username, email, password, users)
    if result["success"]:
        new_user = result["user"]
        new_user["id"] = max((u.get("id", 0) for u in users), default=0) + 1
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
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    for user in users:
        if (user.get("username") == username and 
            user.get("password") == hashed_password and 
            user.get("role") == "Client" and 
            user.get("is_active", True)):
            print(f"\nWelcome, {username}!")
            return user

    print("\nInvalid username or password.")
    return None


def client_search():
    engine = SearchEngine()
    discovery = LibraryDiscovery()
    while True:
        print("\n--- SEARCH BOOKS ---\n1. Search by Title\n2. Search by Author\n3. Search by ISBN\n4. Back")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            discovery.display_results(engine.search_by_title(input("Enter book title: ").strip()))
        elif choice == "2":
            discovery.display_results(engine.search_by_author(input("Enter author: ").strip()))
        elif choice == "3":
            discovery.display_results(engine.search_by_isbn(input("Enter ISBN: ").strip()))
        elif choice == "4":
            break
        else:
            print("Invalid option.")


def client_available_books():
    engine = SearchEngine()
    query = input("\nEnter book title to find available copies: ").strip()
    results = engine.search_by_title(query)
    LibraryDiscovery().display_results(engine.filter_available_only(results))


def client_book_details():
    books = load_books()
    if not books:
        print("\nNo books available.")
        return
    
    isbn = input("Enter ISBN: ").strip()
    book = next((item for item in books if item.get("isbn") == isbn), None)
    if not book:
        print("\nBook not found.")
        return
    LibraryDiscovery().display_results([book])


def client_library_details():
    branch_id = input("Enter Library Branch ID: ").strip()
    LibraryDiscovery().view_library_details(branch_id)


def client_menu():
    while True:
        print("\n" + "=" * 40 + "\n             CLIENT MENU\n" + "=" * 40)
        print("1. Search Books\n2. Find Available Books\n3. View Book Details\n4. View Library Details\n5. Logout")
        choice = input("\nChoose an option: ").strip()
        if choice == "1": client_search()
        elif choice == "2": client_available_books()
        elif choice == "3": client_book_details()
        elif choice == "4": client_library_details()
        elif choice == "5":
            print("\nClient logged out.")
            break
        else:
            print("Invalid option.")


def client_access():
    while True:
        print("\n--- CLIENT ACCESS ---\n1. Register\n2. Login\n3. Back")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            if client_registration(): client_menu()
        elif choice == "2":
            if client_login(): client_menu()
        elif choice == "3":
            break
        else:
            print("Invalid option.")


def librarian_menu():
    manage = LibrarianService()
    while True:
        print("\n" + "=" * 40 + "\n           LIBRARIAN MENU\n" + "=" * 40)
        print("1. Add Book\n2. View Catalogue\n3. Search Book\n4. Update Availability\n5. Update Book Category\n6. Archive Book\n7. Logout")
        choice = input("\nChoose an option: ").strip()
        try:
            if choice == "1":
                book = manage.add_book(
                    input("Enter book title: ").strip(),
                    input("Enter author: ").strip(),
                    input("Enter ISBN: ").strip(),
                    input("Enter category: ").strip(),
                    input("Enter Branch ID: ").strip()
                )
                print(f"\n{book.title} added successfully.")
            elif choice == "2":
                books = manage.view_catalogue()
                if not books:
                    print("\nCatalogue is empty.")
                else:
                    print("\n--- CATALOGUE ---")
                    for b in books:
                        print(f"{b.title} | {b.author} | {b.isbn} | {b.category} | {b.branch_id} | {b.availability}")
            elif choice == "3":
                results = manage.search_books(input("Enter title, author or ISBN: ").strip())
                if not results:
                    print("\nNo books found.")
                else:
                    for b in results:
                        print(f"{b.title} | {b.author} | {b.isbn} | {b.branch_id} | {b.availability}")
            elif choice == "4":
                isbn = input("Enter ISBN: ").strip()
                status = input("Enter status (Available/Unavailable/Missing/Archived): ").strip()
                book = manage.update_availability(isbn, status)
                print(f"\n{book.title} is now {book.availability}.")
            elif choice == "5":
                isbn = input("Enter ISBN: ").strip()
                category = input("Enter new category: ").strip()
                book = manage.update_book(isbn, category)
                print(f"\n{book.title} category updated to {book.category}.")
            elif choice == "6":
                book = manage.archive_book(input("Enter ISBN: ").strip())
                print(f"\n{book.title} has been archived.")
            elif choice == "7":
                print("\nLibrarian logged out.")
                break
            else:
                print("Invalid option.")
        except ValueError as error:
            print(f"\nError: {error}")


def librarian_access():
    if librarian_login():
        librarian_menu()


def admin_branch_management():
    data = load_system_data()
    branches = {b["id"]: b["name"] for b in data.get("branches", [])}
    admin_user = {"is_admin": True}

    while True:
        print("\n--- BRANCH MANAGEMENT ---\n1. List Branches\n2. Create Branch\n3. Update Branch\n4. Remove Branch\n5. Back")
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                if not branches:
                    print("\nNo branches registered.")
                else:
                    print("\nRegistered Branches:")
                    for branch_id, name in branches.items():
                        print(f"{branch_id} | {name}")
            elif choice == "2":
                print(create_branch(admin_user, input("Enter Branch ID: ").strip(), input("Enter Branch Name: ").strip(), branches))
            elif choice == "3":
                print(update_branch(admin_user, input("Enter Branch ID: ").strip(), input("Enter new Branch Name: ").strip(), branches))
            elif choice == "4":
                print(remove_branch(admin_user, input("Enter Branch ID: ").strip(), branches))
            elif choice == "5":
                break
            else:
                print("Invalid option.")
                continue

            data["branches"] = [{"id": b_id, "name": name} for b_id, name in branches.items()]
            save_system_data(data)
        except (PermissionError, ValueError, KeyError) as error:
            print(f"Error: {error}")


def admin_user_management():
    data = load_system_data()
    users = data.get("users", [])

    while True:
        print("\n--- USER MANAGEMENT ---\n1. List Users\n2. Create User\n3. Update User\n4. Assign Role\n5. Deactivate User\n6. Back")
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                all_users = get_all_users(users)
                if not all_users:
                    print("\nNo users registered.")
                for user in all_users:
                    status = "Active" if user.get("is_active", True) else "Inactive"
                    print(f"ID: {user.get('id')} | Name: {user.get('name', user.get('username', 'N/A'))} | Role: {user.get('role', 'N/A')} | Status: {status}")
            elif choice == "2":
                name = input("Name: ").strip()
                role = input("Role (Client/Librarian/Admin): ").strip()
                new_user = create_user({"name": name, "role": role}, users)
                print(f"User created. ID: {new_user['id']}")
            elif choice == "3":
                user_id = int(input("Enter User ID: "))
                field = input("Field to update: ").strip()
                value = input("New value: ").strip()
                update_user(user_id, {field: value}, users)
                print("User updated.")
            elif choice == "4":
                user_id = int(input("Enter User ID: "))
                role = input("Enter new role: ").strip()
                assign_role(user_id, role, users)
                print("Role updated.")
            elif choice == "5":
                user_id = int(input("Enter User ID: "))
                deactivate_user(user_id, users)
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
    entries = get_global_catalogue(load_books())
    print(f"\nGlobal Catalogue ({len(entries)} books)")
    display_catalogue(entries)


def administrator_menu():
    while True:
        print("\n" + "=" * 40 + "\n          ADMINISTRATOR MENU\n" + "=" * 40)
        print("1. Manage Users\n2. Manage Libraries\n3. View Global Catalogue\n4. Logout")
        choice = input("\nChoose an option: ").strip()
        if choice == "1": admin_user_management()
        elif choice == "2": admin_branch_management()
        elif choice == "3": admin_catalogue()
        elif choice == "4":
            print("\nAdministrator logged out.")
            break
        else:
            print("Invalid option.")


def administrator_access():
    print("\n--- ADMINISTRATOR LOGIN ---")
    user = _authenticate()
    if user.get("is_admin"):
        print(f"\nWelcome, {user['username']}!")
        administrator_menu()
    else:
        print("\nAccess denied. Invalid administrator credentials.")


def main():
    while True:
        print("\nLIBTRACK\nLibrary Control System")
        print("1. Client\n2. Librarian\n3. Administrator\n4. Exit")
        choice = input("\nChoose an option: ").strip()
        if choice == "1":
            client_access()
        elif choice == "2":
            librarian_access()
        elif choice == "3":
            administrator_access()
        elif choice == "4":
            print("\nThank you for using LibTrack. Goodbye!")
            break
        else:
            print("\nInvalid option. Please choose 1 to 4.")

if __name__ == "__main__":
    main()