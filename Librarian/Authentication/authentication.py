import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def authenticate_librarian(username, password, librarians):
    for librarian in librarians:
        if (
            librarian["username"] == username
            and librarian["password"] == hash_password(password)
            and librarian.get("role") == "Librarian"
            and librarian.get("is_active", True)
        ):
            return {
                "success": True,
                "user": librarian
            }

    return {
        "success": False,
        "error": "Invalid username or password"
    }


def require_librarian(user):
    if not user:
        raise PermissionError("You must be logged in.")

    if user.get("role") != "Librarian":
        raise PermissionError("Librarian privileges required.")

    if not user.get("is_active", True):
        raise PermissionError("This account is inactive.")

    return True


def librarian_login():
    librarians = [
        {
            "id": 1,
            "username": "librarian1",
            "password": hash_password("library123"),
            "role": "Librarian",
            "is_active": True
        }
    ]

    print("\n--- LIBRARIAN LOGIN ---")

    username = input("Username: ").strip()
    password = input("Password: ").strip()

    result = authenticate_librarian(
        username,
        password,
        librarians
    )

    if result["success"]:
        user = result["user"]
        print(f"\nWelcome, {user['username']}!")
        return user

    print(f"\nLogin failed: {result['error']}")
    return None


if __name__ == "__main__":
    librarian_login()