import pytest

from code.race import RaceController


def test_race_controller_instantiation():
    controller = RaceController()
    assert controller is not None

