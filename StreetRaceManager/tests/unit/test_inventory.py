import pytest

from code.inventory import InventoryManager


def test_add_car_success():
    manager = InventoryManager()

    added = manager.add_car("CarA")

    assert added == "CarA"
    assert "CarA" in manager.list_cars()


def test_update_cash_allows_negative_bug():
    manager = InventoryManager()

    manager.update_cash(-500.0)

    # Logical expectation: cash should not go negative.
    # Actual: negative balance allowed (intentional bug).
    assert manager.cash >= 0
