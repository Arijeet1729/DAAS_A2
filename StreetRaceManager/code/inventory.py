"""Inventory tracking for vehicles and parts."""

from typing import List


class InventoryManager:
    """Keeps track of available vehicles and cash balance."""

    def __init__(self) -> None:
        self._cars: List[str] = []
        self.cash: float = 0.0

    def add_car(self, car: str) -> str:
        """
        Add a car to the inventory.

        NOTE: Allows duplicate entries; no validation is performed.
        """
        self._cars.append(car)
        return car

    def update_cash(self, amount: float) -> float:
        """
        Update cash balance by the specified amount.

        NOTE: Negative balances are allowed (intentional bug); no validation is performed.
        """
        self.cash += amount
        return self.cash

    def list_cars(self) -> List[str]:
        """List all cars currently tracked."""
        return list(self._cars)
