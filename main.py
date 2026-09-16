import json, hashlib
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

BRANCHES_FILE, BOOKS_FILE = "branches.json", "Librarian/data/books.json"

def load_system_data():
    try:
        with open(BRANCHES_FILE, "r") as file: return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError): return {"branches": [], "users": []}

def save_system_data(data):
    with open(BRANCHES_FILE, "w") as file: json.dump(data, file, indent=4)

def load_books():
    try:
        with open(BOOKS_FILE, "r") as file: return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError): return []

def client_registration():
    data = load_system_data()
    users = data.get("users", [])
    print("\n--- CLIENT REGISTRATION ---")
    username, email, password = input("Username: ").strip(), input("Email: ").strip(), input("Password: ").strip()
    result = register_client(username, email, password, users)
    if result["success"]:
        new_user = result["user"]
        new_user["id"] = max((user.get("id", 0) for user in users), default=0) + 1
        new_user["role"], new_user["is_active"] = "Client", True
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
    username, password = input("Username: ").strip(), input("Password: ").strip()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    for user in users:
        if (user.get("username") == username and user.get("password") == hashed_password and 
                user.get("role") == "Client" and user.get("is_active", True)):
            print(f"\nWelcome, {username}!")
            return user
    print("\nInvalid username or password.")
    return None

def client_search():
    engine, discovery = SearchEngine(), LibraryDiscovery()
    while True:
        print("\n--- SEARCH BOOKS ---\n1. Search by Title\n2. Search by Author\n3. Search by ISBN\n4. Back")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            discovery.display_results(engine.search_by_title(input("Enter book title: ").strip()))
        elif choice == "2":
            discovery.display_results(engine.search_by_author(input("Enter author: ").strip()))
        elif choice == "3":
            discovery.display_results(engine.search_by_isbn(input("Enter ISBN: ").strip()))
        elif choice == "4": break
        else: print("Invalid option.")

def client_available_books():
    engine, discovery = SearchEngine(), LibraryDiscovery()
    query = input("\nEnter book title to find available copies: ").strip()
    discovery.display_results(engine.filter_available_only(engine.search_by_title(query)))

def client_book_details():
    books = load_books()
    if not books: return print("\nNo books available.")
    isbn = input("Enter ISBN: ").strip()
    book = next((item for item in books if item.get("isbn") == isbn), None)
    if not book: return print("\nBook not found.")
    LibraryDiscovery().display_results([book])

def client_library_details():
    LibraryDiscovery().view_library_details(input("Enter Library Branch ID: ").strip())

def client_menu():
    while True:
        print("\n" + "=" * 40 + "\n            CLIENT MENU\n" + "=" * 40)
        print("1. Search Books\n2. Find Available Books\n3. View Book Details\n4. View Library Details\n5. Logout")
        choice = input("\nChoose an option: ").strip()
        if choice == "1": client_search()
        elif choice == "2": client_available_books()
        elif choice == "3": client_book_details()
        elif choice == "4": client_library_details()
        elif choice == "5":
            print("\nClient logged out.")
            break
        else: print("Invalid option.")

def client_access():
    while True:
        print("\n--- CLIENT ACCESS ---\n1. Register\n2. Login\n3. Back")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            user = client_registration()
            if user: client_menu()
        elif choice == "2":
            user = client_login()
            if user: client_menu()
        elif choice == "3": break
        else: print("Invalid option.")

def librarian_menu():
    manage = LibrarianService()
    while True:
        print("\n" + "=" * 40 + "\n           LIBRARIAN MENU\n" + "=" * 40)
        print("1. Add Book\n2. View Catalogue\n3. Search Book\n4. Update Availability\n5. Update Book Category\n6. Archive Book\n7. Logout")
        choice = input("\nChoose an option: ").strip()
        if choice == "1":
            t, a, i, c, b = input("Enter book title: ").strip(), input("Enter author: ").strip(), input("Enter ISBN: ").strip(), input("Enter category: ").strip(), input("Enter Branch ID: ").strip()
            try: print(f"\n{manage.add_book(t, a, i, c, b).title} added successfully.")
            except ValueError as error: print(f"\nError: {error}")
        elif choice == "2":
            books = manage.view_catalogue()
            if not books: print("\nCatalogue is empty.")
            else:
                print("\n--- CATALOGUE ---")
                for b in books: print(f"{b.title} | {b.author} | {b.isbn} | {b.category} | {b.branch_id} | {b.availability}")
        elif choice == "3":
            results = manage.search_books(input("Enter title, author or ISBN: ").strip())
            if not results: print("\nNo books found.")
            else:
                for b in results: print(f"{b.title} | {b.author} | {b.isbn} | {b.branch_id} | {b.availability}")
        elif choice == "4":
            try: print(f"\n{manage.update_availability(input('Enter ISBN: ').strip(), input('Enter status (Available/Unavailable/Missing/Archived): ').strip()).title} is now available.")
            except ValueError as error: print(f"\nError: {error}")
        elif choice == "5":
            try:
                b = manage.update_book(input("Enter ISBN: ").strip(), input("Enter new category: ").strip())
                print(f"\n{b.title} category updated to {b.category}.")
            except ValueError as error: print(f"\nError: {error}")
        elif choice == "6":
            try: print(f"\n{manage.archive_book(input('Enter ISBN: ').strip()).title} has been archived.")
            except ValueError as error: print(f"\nError: {error}")
        elif choice == "7":
            print("\nLibrarian logged out.")
            break
        else: print("Invalid option.")

def librarian_access():
    if librarian_login(): librarian_menu()

def admin_branch_management():
    data = load_system_data()
    branches = {b["id"]: b["name"] for b in data.get("branches", [])}
    admin_user = {"is_admin": True}
    while True:
        print("\n--- BRANCH MANAGEMENT ---\n1. List Branches\n2. Create Branch\n3. Update Branch\n4. Remove Branch\n5. Back")
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                if not branches: print("\nNo branches registered.")
                else:
                    print("\nRegistered Branches:")
                    for b_id, name in branches.items(): print(f"{b_id} | {name}")
            elif choice == "2": print(create_branch(admin_user, input("Enter Branch ID: ").strip(), input("Enter Branch Name: ").strip(), branches))
            elif choice == "3": print(update_branch(admin_user, input("Enter Branch ID: ").strip(), input("Enter new Branch Name: ").strip(), branches))
            elif choice == "4": print(remove_branch(admin_user, input("Enter Branch ID: ").strip(), branches))
            elif choice == "5": break
            else:
                print("Invalid option.")
                continue
            data["branches"] = [{"id": b_id, "name": name} for b_id, name in branches.items()]
            save_system_data(data)
        except (PermissionError, ValueError, KeyError) as error: print(f"Error: {error}")

def admin_user_management():
    data = load_system_data()
    users = data.get("users", [])
    while True:
        print("\n--- USER MANAGEMENT ---\n1. List Users\n2. Create User\n3. Update User\n4. Assign Role\n5. Deactivate User\n6. Back")
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                all_users = get_all_users(users)
                if not all_users: print("\nNo users registered.")
                for u in all_users:
                    status = "Active" if u.get("is_active", True) else "Inactive"
                    print(f"ID: {u.get('id')} | Name: {u.get('name', u.get('username', 'N/A'))} | Role: {u.get('role', 'N/A')} | Status: {status}")
            elif choice == "2":
                new_u = create_user({"name": input("Name: ").strip(), "role": input("Role (Client/Librarian/Admin): ").strip()}, users)
                print(f"User created. ID: {new_u['id']}")
            elif choice == "3":
                update_user(int(input("Enter User ID: ")), {input("Field to update: ").strip(): input("New value: ").strip()}, users)
                print("User updated.")
            elif choice == "4":
                assign_role(int(input("Enter User ID: ")), input("Enter new role: ").strip(), users)
                print("Role updated.")
            elif choice == "5":
                deactivate_user(int(input("Enter User ID: ")), users)
                print("User deactivated.")
            elif choice == "6": break
            else:
                print("Invalid option.")
                continue
            data["users"] = users
            save_system_data(data)
        except ValueError: print("User ID must be an integer.")
        except KeyError as error: print(f"Error: {error}")

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
        else: print("Invalid option.")

def administrator_access():
    print("\n--- ADMINISTRATOR LOGIN ---")
    user = _authenticate()
    if user.get("is_admin"):
        print(f"\nWelcome, {user['username']}!")
        administrator_menu()
    else: print("\nAccess denied. Invalid administrator credentials.")

def main():
    while True:
        print("\n" + "=" * 45 + "\n                LIBTRACK\n        Library Control System\n" + "=" * 45)
        print("1. Client\n2. Librarian\n3. Administrator\n4. Exit")
        choice = input("\nChoose an option: ").strip()
        if choice == "1": client_access()
        elif choice == "2": librarian_access()
        elif choice == "3": administrator_access()
        elif choice == "4":
            print("\nThank you for using LibTrack. Goodbye!")
            break
        else: print("\nInvalid option. Please choose 1 to 4.")

if __name__ == "__main__":
    main()