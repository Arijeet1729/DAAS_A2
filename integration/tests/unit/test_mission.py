import pytest

from code.mission import MissionPlanner


def test_assign_required_role_success():
    planner = MissionPlanner()
    planner.create_mission("mission-1", ["Driver"])

    assignment = planner.assign_mission("mission-1", "Alex", "Driver")

    assert assignment["name"] == "Alex"
    assert assignment["role"] == "Driver"
    assert assignment in planner.list_assignees("mission-1")


def test_assign_non_required_role_should_fail():
    planner = MissionPlanner()
    planner.create_mission("mission-2", ["Driver"])

    with pytest.raises(ValueError):
        planner.assign_mission("mission-2", "Sam", "Mechanic")
