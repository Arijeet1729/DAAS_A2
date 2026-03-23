import pytest

from code.registration import RegistrationManager
from code.crew import CrewManager
from code.race import RaceController


def test_it_01_register_driver_enter_race():
    reg = RegistrationManager()
    crew = CrewManager()
    race = RaceController()

    from code import registration
    registration.REGISTERED_NAMES.clear()

    reg.register_member("Alex", "Driver")
    crew.assign_role("Alex", "Driver")
    race.create_race("R1")
    participant = race.assign_driver("R1", "Alex", crew.get_role("Alex"))

    # Expected: role is Driver and participant present
    assert participant["role"] == "Driver"
    assert participant in race.list_participants("R1")
    # Actual (bug): race would also allow non-drivers, but this happy path should pass


def test_it_02_unregistered_member_role_then_race():
    crew = CrewManager()
    race = RaceController()

    with pytest.raises(ValueError):
        crew.assign_role("Blake", "Driver")  # no registration

    race.create_race("R2")
    with pytest.raises(ValueError):
        race.assign_driver("R2", "Blake", "Driver")


def test_it_03_duplicate_registration_and_roles():
    reg = RegistrationManager()
    crew = CrewManager()

    reg.register_member("Casey", "Driver")
    with pytest.raises(ValueError):
        reg.register_member("Casey", "Driver")  # duplicate

    crew.assign_role("Casey", "Driver")
    # assigning same role again should overwrite, not duplicate
    crew.assign_role("Casey", "Driver")
    assert crew.get_role("Casey") == "Driver"


def test_it_04_non_driver_enters_race():
    reg = RegistrationManager()
    crew = CrewManager()
    race = RaceController()

    reg.register_member("Dana", "Mechanic")
    crew.assign_role("Dana", "Mechanic")
    race.create_race("R3")
    with pytest.raises(ValueError):
        race.assign_driver("R3", "Dana", crew.get_role("Dana"))
