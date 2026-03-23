import pytest

from code.registration import RegistrationManager


def test_registration_manager_instantiation():
    manager = RegistrationManager()
    assert manager is not None

