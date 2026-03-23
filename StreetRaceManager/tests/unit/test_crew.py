import pytest

from code.crew import CrewManager


def test_assign_role_to_registered_user():
    manager = CrewManager()

    assigned = manager.assign_role("Jordan", "Driver")

    assert assigned["name"] == "Jordan"
    assert assigned["role"] == "Driver"
    assert manager.get_role("Jordan") == "Driver"


def test_assign_role_to_unregistered_user_should_fail():
    manager = CrewManager()

    manager.assign_role("Kai", "Mechanic")

    # Logical expectation: assigning a role to an unregistered user should fail.
    # Actual behavior (intentional bug): it succeeds and stores the role.
    assert manager.get_role("Kai") is None
