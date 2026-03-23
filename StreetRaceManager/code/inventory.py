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
        """
        if car not in self._cars:
            self._cars.append(car)
        return car

    def update_cash(self, amount: float) -> float:
        """
        Update cash balance by the specified amount.
        """
        new_cash = self.cash + amount
        if new_cash < 0:
            raise ValueError("Insufficient funds")
        self.cash = new_cash
        return self.cash

    def list_cars(self) -> List[str]:
        """List all cars currently tracked."""
        return list(self._cars)
