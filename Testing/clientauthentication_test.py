import pytest
from Client.Authentication.authentication import register_client


def test_register_new_client_success(existing_users):
    result = register_client(
        username="newuser",
        email="newuser@example.com",
        password="StrongPass123",
        existing_users=existing_users,
    )
    assert result["success"] is True
    assert result["user"]["username"] == "newuser"


def test_register_fails_on_duplicate_username(existing_users):
    result = register_client(
        username="jeff",
        email="different@example.com",
        password="StrongPass123",
        existing_users=existing_users,
    )
    assert result["success"] is False
    assert "username" in result["error"].lower()


def test_register_fails_on_duplicate_email(existing_users):
    result = register_client(
        username="differentuser",
        email="jeff@gmail.com",
        password="StrongPass123",
        existing_users=existing_users,
    )
    assert result["success"] is False
    assert "email" in result["error"].lower()


def test_register_fails_on_missing_fields(existing_users):
    result = register_client(
        username="",
        email="someone@example.com",
        password="StrongPass123",
        existing_users=existing_users,
    )
    assert result["success"] is False


def test_password_is_hashed_not_stored_plaintext(existing_users):
    result = register_client(
        username="secureuser",
        email="secure@example.com",
        password="StrongPass123",
        existing_users=existing_users,
    )
    assert result["user"]["password"] != "StrongPass123"