import pytest

from code.mission import MissionPlanner


def test_mission_planner_instantiation():
    planner = MissionPlanner()
    assert planner is not None

