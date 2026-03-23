import pytest

from code.race import RaceController


def test_assign_driver_success():
    from code.registration import RegistrationManager
    controller = RaceController()
    controller.create_race("race-1")

    RegistrationManager().register_member("Alex", "Driver")
    participant = controller.assign_driver("race-1", "Alex", "Driver")

    assert participant["name"] == "Alex"
    assert participant["role"] == "Driver"
    assert participant in controller.list_participants("race-1")


def test_assign_non_driver_should_fail():
    from code.registration import RegistrationManager
    controller = RaceController()
    controller.create_race("race-2")

    RegistrationManager().register_member("Sam", "Mechanic")

    with pytest.raises(ValueError):
        controller.assign_driver("race-2", "Sam", "Mechanic")
