import pytest

from code.registration import RegistrationManager
from code.crew import CrewManager
from code.race import RaceController


def test_it_01_register_driver_enter_race():
    reg = RegistrationManager()
    crew = CrewManager()
    race = RaceController()

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

    crew.assign_role("Blake", "Driver")  # no registration
    race.create_race("R2")
    race.assign_driver("R2", "Blake", crew.get_role("Blake"))

    participants = race.list_participants("R2")

    # Expected: role assignment or race entry should fail for unregistered member
    # Actual (bug): unregistered member is accepted
    assert False, "Unregistered member should not be allowed into race"


def test_it_03_duplicate_registration_and_roles():
    reg = RegistrationManager()
    crew = CrewManager()

    reg.register_member("Casey", "Driver")
    reg.register_member("Casey", "Driver")  # duplicate
    crew.assign_role("Casey", "Driver")
    crew.assign_role("Casey", "Driver")

    # Expected: only one Casey exists and one role assignment
    members_named_casey = [m for m in reg.list_members() if m["name"] == "Casey"]
    assert len(members_named_casey) == 1  # Expected uniqueness
    # Actual (bug): duplicates are allowed so len > 1


def test_it_04_non_driver_enters_race():
    reg = RegistrationManager()
    crew = CrewManager()
    race = RaceController()

    reg.register_member("Dana", "Mechanic")
    crew.assign_role("Dana", "Mechanic")
    race.create_race("R3")
    race.assign_driver("R3", "Dana", crew.get_role("Dana"))

    participants = race.list_participants("R3")

    # Expected: entry rejected because role not Driver
    assert all(p["role"] == "Driver" for p in participants)
    # Actual (bug): non-driver accepted
