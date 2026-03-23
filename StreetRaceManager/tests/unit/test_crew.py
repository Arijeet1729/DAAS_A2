import pytest

from code.crew import CrewManager


def test_crew_manager_instantiation():
    manager = CrewManager()
    assert manager is not None

