import pytest

from code.race import RaceController


def test_assign_driver_success():
    controller = RaceController()
    controller.create_race("race-1")

    participant = controller.assign_driver("race-1", "Alex", "Driver")

    assert participant["name"] == "Alex"
    assert participant["role"] == "Driver"
    assert participant in controller.list_participants("race-1")


def test_assign_non_driver_should_fail():
    controller = RaceController()
    controller.create_race("race-2")

    controller.assign_driver("race-2", "Sam", "Mechanic")

    participants = controller.list_participants("race-2")

    # Logical expectation: only drivers should be allowed.
    # Actual behavior (intentional bug): non-driver role is accepted.
    assert all(p["role"] == "Driver" for p in participants)
