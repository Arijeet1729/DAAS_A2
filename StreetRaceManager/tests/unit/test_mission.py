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

    planner.assign_mission("mission-2", "Sam", "Mechanic")

    assignees = planner.list_assignees("mission-2")

    # Logical expectation: only required roles should be accepted.
    # Actual (intentional bug): non-required role is accepted.
    assert all(a["role"] in ["Driver"] for a in assignees)
