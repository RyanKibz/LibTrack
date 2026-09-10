import pytest
from Administrator.Authentication.authentication import (
    create_branch,
    update_branch,
    remove_branch,
)


@pytest.fixture
def initial_branches():
    """Provides a fresh branch dictionary for every test."""
    return {"B1": "Central Library"}


@pytest.fixture
def admin_user():
    return {"username": "Anastacia", "is_admin": True}


@pytest.fixture
def regular_user():
    return {"username": "Stacia ann", "is_admin": False}



def test_admin_can_create_branch(initial_branches, admin_user):
    result = create_branch(admin_user, "B2", "North Branch", initial_branches)
    
    assert result == "Branch 'North Branch' created."
    assert initial_branches["B2"] == "North Branch"


def test_admin_can_update_branch(initial_branches, admin_user):
    result = update_branch(admin_user, "B1", "Central Main Library", initial_branches)
    
    assert result == "Branch 'B1' updated to 'Central Main Library'."
    assert initial_branches["B1"] == "Central Main Library"


def test_admin_can_remove_branch(initial_branches, admin_user):
    result = remove_branch(admin_user, "B1", initial_branches)
    
    assert result == "Branch 'B1' removed."
    assert "B1" not in initial_branches


@pytest.mark.parametrize("action,args", [
    (create_branch, ("B2", "Unauthorized Branch")),
    (update_branch, ("B1", "Hacked Branch Name")),
    (remove_branch, ("B1",)),
])
def test_regular_user_denied_access(initial_branches, regular_user, action, args):
    """Ensures non-admins cannot perform any branch mutations."""
    with pytest.raises(PermissionError, match="Admin privileges required"):
        action(regular_user, *args, initial_branches)


def test_cannot_create_duplicate_branch_id(initial_branches, admin_user):
    """Attempting to add an existing branch ID should raise a ValueError."""
    with pytest.raises(ValueError, match="Branch ID 'B1' already exists"):
        create_branch(admin_user, "B1", "Duplicate Branch", initial_branches)


def test_cannot_update_non_existent_branch(initial_branches, admin_user):
    """Attempting to update a missing branch ID should raise a KeyError."""
    with pytest.raises(KeyError, match="Branch ID 'B99' not found"):
        update_branch(admin_user, "B99", "Ghost Branch", initial_branches)


def test_cannot_remove_non_existent_branch(initial_branches, admin_user):
    """Attempting to remove a missing branch ID should raise a KeyError."""
    with pytest.raises(KeyError, match="Branch ID 'B99' not found"):
        remove_branch(admin_user, "B99", initial_branches)