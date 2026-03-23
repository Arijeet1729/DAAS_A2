import pytest

from code.inventory import InventoryManager


def test_add_car_success():
    manager = InventoryManager()

    added = manager.add_car("CarA")

    assert added == "CarA"
    assert "CarA" in manager.list_cars()


def test_update_cash_allows_negative_bug():
    manager = InventoryManager()

    with pytest.raises(ValueError):
        manager.update_cash(-500.0)
