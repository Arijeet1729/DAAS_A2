import pytest

from code.registration import RegistrationManager


def test_register_member_success():
    manager = RegistrationManager()
    member = manager.register_member("Alex", "Driver")

    assert member["name"] == "Alex"
    assert member["role"] == "Driver"
    assert member in manager.list_members()


def test_get_member_success():
    manager = RegistrationManager()
    manager.register_member("Blake", "Mechanic")

    fetched = manager.get_member("Blake")

    assert fetched is not None
    assert fetched["name"] == "Blake"
    assert fetched["role"] == "Mechanic"


def test_duplicate_registration_should_fail():
    manager = RegistrationManager()
    manager.register_member("Casey", "Navigator")
    manager.register_member("Casey", "Navigator")

    duplicates = [m for m in manager.list_members() if m["name"] == "Casey"]

    # Logical expectation: only one entry should exist; current implementation will allow two (intentional bug).
    assert len(duplicates) == 1
