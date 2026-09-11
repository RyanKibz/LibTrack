import argparse
import sys
import secrets
from typing import Any, Dict

ADMIN_USERNAME = "Anastacia"
ADMIN_PASSWORD = "admin@2045"


def _require_admin(user: Dict[str, Any]):
    if not user.get("is_admin"):
        raise PermissionError("Admin privileges required.")


def create_branch(user: Dict[str, Any], branch_id: str, name: str, branches: Dict[str, str]):
    #Create a new branch entry.
    _require_admin(user)
    if branch_id in branches:
        raise ValueError(f"Branch ID '{branch_id}' already exists.")
    branches[branch_id] = name
    return f"Branch '{name}' created."


def update_branch(user: Dict[str, Any], branch_id: str, name: str, branches: Dict[str, str]):
    #update an existing branch
    _require_admin(user)
    if branch_id not in branches:
        raise KeyError(f"Branch ID '{branch_id}' not found.")
    branches[branch_id] = name
    return f"Branch '{branch_id}' updated to '{name}'."


def remove_branch(user: Dict[str, Any], branch_id: str, branches: Dict[str, str]):
    #Remove a branch entry.
    _require_admin(user)
    if branch_id not in branches:
        raise KeyError(f"Branch ID '{branch_id}' not found.")
    del branches[branch_id]
    return f"Branch '{branch_id}' removed."


def _authenticate() -> Dict[str, Any]:
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    is_admin = secrets.compare_digest(username, ADMIN_USERNAME) and secrets.compare_digest(password, ADMIN_PASSWORD)
    return {"is_admin": is_admin, "username": username}


def cli():
    branches: Dict[str, str] = {"B1": "Central Library", "B2": "Nairobi Branch"}

    current_user = _authenticate()

    print("\nLibrary Control Management System")

    while True:
        print("\nOptions:")
        print("1. List all branches")
        print("2. Create a branch")
        print("3. Update a branch")
        print("4. Remove a branch")
        print("5. Exit")

        choice = input("\nSelect an option (1-5): ").strip()

        try:
            if choice == "1":
                print("\nCurrent Branches:")
                if not branches:
                    print("  No branches registered.")
                for bid, bname in branches.items():
                    print(f"  [{bid}] {bname}")

            elif choice == "2":
                bid = input("Enter new Branch ID: ").strip()
                bname = input("Enter Branch Name: ").strip()
                msg = create_branch(current_user, bid, bname, branches)
                print(f"Success: {msg}")

            elif choice == "3":
                bid = input("Enter Branch ID to update: ").strip()
                bname = input("Enter new Branch Name: ").strip()
                msg = update_branch(current_user, bid, bname, branches)
                print(f"Success: {msg}")

            elif choice == "4":
                bid = input("Enter Branch ID to remove: ").strip()
                msg = remove_branch(current_user, bid, branches)
                print(f"Success: {msg}")

            elif choice == "5":
                print("Exiting branch management system. Goodbye!")
                break

            else:
                print("Invalid selection. Please choose options 1 to 5.")

        except (PermissionError, ValueError, KeyError) as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    cli()