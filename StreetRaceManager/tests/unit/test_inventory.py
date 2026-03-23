import pytest

from code.inventory import InventoryManager


def test_inventory_manager_instantiation():
    manager = InventoryManager()
    assert manager is not None

