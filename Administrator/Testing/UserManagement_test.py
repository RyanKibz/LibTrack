import pytest
from Administrator.UserManagement.userManagement import (
    get_all_users,
    create_user,
    update_user,
    deactivate_user,
    assign_role,
)


@pytest.fixture
def existing_users():
    return [
        {"id": 1, "email": "user1@test.com", "role": "CLIENT", "is_active": True},
        {"id": 2, "email": "lib1@test.com", "role": "LIBRARIAN", "is_active": True},
    ]


def test_view_all_registered_users(existing_users):
    """View all registered users."""
    users = get_all_users(existing_users)
    assert len(users) == 2
    assert users[0]["email"] == "user1@test.com"


def test_create_new_user(existing_users):
    """Create a new user account."""
    user_data = {
        "email": "new_librarian@library.com",
        "name": "Stacia Ann",
        "role": "LIBRARIAN",
    }
    created_user = create_user(user_data, existing_users)
    assert created_user["is_active"] is True
    assert created_user["email"] == "new_librarian@library.com"


def test_update_existing_user(existing_users):
    """Update user information."""
    updated_user = update_user(1, {"email": "stacia@library.com"}, existing_users)
    assert updated_user["email"] == "stacia@library.com"


def test_deactivate_user_account(existing_users):
    """Deactivate user account."""
    result = deactivate_user(1, existing_users)
    assert result is True
    assert existing_users[0]["is_active"] is False


def test_assign_role_to_user(existing_users):
    """Assign roles to users (e.g., promote Client to Librarian)."""
    updated_user = assign_role(1, "LIBRARIAN", existing_users)
    assert updated_user["role"] == "LIBRARIAN"