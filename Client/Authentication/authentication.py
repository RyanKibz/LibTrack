import hashlib


def _hash_password(password):
    """Hashes a password so it's never stored in plaintext."""
    return hashlib.sha256(password.encode()).hexdigest()


def register_client(username, email, password, existing_users):
    """
    Registers a new client if the username/email are unique and all
    required fields are present. Returns a result dict with either
    {"success": True, "user": {...}} or {"success": False, "error": "..."}.
    """
    if not username or not email or not password:
        return {"success": False, "error": "Missing required fields"}

    for user in existing_users:
        if user["username"] == username:
            return {"success": False, "error": "Username already exists"}
        if user["email"] == email:
            return {"success": False, "error": "Email already exists"}

    new_user = {
        "username": username,
        "email": email,
        "password": _hash_password(password),
    }
    return {"success": True, "user": new_user}