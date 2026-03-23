import pytest

from code.crew import CrewManager


def test_assign_role_to_registered_user():
    manager = CrewManager()
    from code.registration import RegistrationManager

    RegistrationManager().register_member("Jordan", "Driver")

    assigned = manager.assign_role("Jordan", "Driver")

    assert assigned["name"] == "Jordan"
    assert assigned["role"] == "Driver"
    assert manager.get_role("Jordan") == "Driver"


def test_assign_role_to_unregistered_user_should_fail():
    manager = CrewManager()

    with pytest.raises(ValueError):
        manager.assign_role("Kai", "Mechanic")
