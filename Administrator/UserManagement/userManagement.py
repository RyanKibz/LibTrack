

def get_all_users(users):
    return users


def _find_user(user_id, users):
    for user in users:
        if user["id"] == user_id:
            return user
    raise KeyError(f"User ID '{user_id}' not found")


def create_user(user_data, users):
    #Create a new user account and add it to the users list.
    new_user = dict(user_data)
    new_user.setdefault(
        "id", (max((u["id"] for u in users), default=0) + 1)
    )
    new_user["is_active"] = True
    users.append(new_user)
    return new_user


def update_user(user_id, updates, users):
    #Update fields on an existing user
    user = _find_user(user_id, users)
    user.update(updates)
    return user


def deactivate_user(user_id, users):
    #Mark a user account as inactive.
    user = _find_user(user_id, users)
    user["is_active"] = False
    return True


def assign_role(user_id, role, users):
    #Assign a new role to a user 
    user = _find_user(user_id, users)
    user["role"] = role
    return user

def display_menu():
    print("\nLibrary Admin: User Management")
    print("1. List all users")
    print("2. Create a new user")
    print("3. Update user details")
    print("4. Assign role to user")
    print("5. Deactivate a user")
    print("6. Exit")


def main():
    #registered users
    users = [
        {"id": 1, "name": "Anastacia", "role": "Librarian", "is_active": True},
        {"id": 2, "name": "Manira Yakin", "role": "Member", "is_active": True},
        {"id": 3, "name": "Jeff Muange", "role": "Librarian", "is_active": True},
    ]

    while True:
        display_menu()
        choice = input("\nSelect an option (1-6): ").strip()

        if choice == "1":
            all_users = get_all_users(users)
            print("\nRegistered Users:")
            for u in all_users:
                status = "Active" if u["is_active"] else "Inactive"
                print(f" ID: {u['id']} | Name: {u.get('name', 'N/A')} | Role: {u.get('role', 'N/A')} | Status: {status}")

        elif choice == "2":
            name = input("Enter user name: ").strip()
            role = input("Enter user role (Member, Librarian, Admin): ").strip()
            user_data = {"name": name, "role": role}
            created = create_user(user_data, users)
            print(f"User created successfully! Assigned ID: {created['id']}")

        elif choice == "3":
            try:
                user_id = int(input("Enter User ID to update: "))
                _find_user(user_id, users)
                field = input("Enter field name to update (name, role): ").strip()
                val = input(f"Enter new value for {field}: ").strip()
                updated = update_user(user_id, {field: val}, users)
                print(f"User {user_id} updated successfully: {updated}")
            except ValueError:
                print("Error: User ID must be an integer.")
            except KeyError as e:
                print(f"Error: {e}")

        elif choice == "4":
            try:
                user_id = int(input("Enter User ID: "))
                role = input("Enter new role: ").strip()
                updated = assign_role(user_id, role, users)
                print(f"Role updated successfully for user {user_id}: {updated['role']}")
            except ValueError:
                print("Error: User ID must be an integer.")
            except KeyError as e:
                print(f"Error: {e}")

        elif choice == "5":
            try:
                user_id = int(input("Enter User ID to deactivate: "))
                deactivate_user(user_id, users)
                print(f"User ID {user_id} has been deactivated.")
            except ValueError:
                print("Error: User ID must be an integer.")
            except KeyError as e:
                print(f"Error: {e}")

        elif choice == "6":
            print("\nExiting User Management system. Goodbye!")
            break
        else:
            print("Invalid selection. Please choose a number between 1 and 6.")


if __name__ == "__main__":
    main()