import pytest

from code.inventory import InventoryManager
from code.results import ResultsTracker


def test_record_winner_stores_result():
    tracker = ResultsTracker()

    result = tracker.record_winner("race-1", "Jordan", prize=1000.0)

    assert tracker.get_winner("race-1") == "Jordan"
    assert result["prize"] == 1000.0
    assert {"race_id": "race-1", "winner": "Jordan", "prize": 1000.0} in tracker.get_leaderboard()


def test_prize_cash_updates_inventory_should_fail():
    tracker = ResultsTracker()
    inventory = InventoryManager()

    tracker.record_winner("race-2", "Alex", prize=500.0, inventory=inventory)

    # Logical expectation: inventory cash increases by prize.
    # Actual (intentional bug): cash remains unchanged.
    assert inventory.cash == 500.0
