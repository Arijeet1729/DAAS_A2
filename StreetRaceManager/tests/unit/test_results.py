import pytest

from code.results import ResultsTracker


def test_results_tracker_instantiation():
    tracker = ResultsTracker()
    assert tracker is not None

