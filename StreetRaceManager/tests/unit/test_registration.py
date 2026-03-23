import pytest

from code.registration import RegistrationManager


def test_register_member_success():
    manager = RegistrationManager()
    from code import registration
    registration.REGISTERED_NAMES.clear()
    member = manager.register_member("Alex", "Driver")

    assert member["name"] == "Alex"
    assert member["role"] == "Driver"
    assert member in manager.list_members()


def test_get_member_success():
    manager = RegistrationManager()
    from code import registration
    registration.REGISTERED_NAMES.clear()
    manager.register_member("Blake", "Mechanic")

    fetched = manager.get_member("Blake")

    assert fetched is not None
    assert fetched["name"] == "Blake"
    assert fetched["role"] == "Mechanic"


def test_duplicate_registration_should_fail():
    manager = RegistrationManager()
    manager.register_member("Casey", "Navigator")
    with pytest.raises(ValueError):
        manager.register_member("Casey", "Navigator")
