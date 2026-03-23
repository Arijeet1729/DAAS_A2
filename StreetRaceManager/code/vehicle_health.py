"""Vehicle health monitoring."""

from typing import Dict


class VehicleHealthMonitor:
    """Tracks vehicle health and maintenance records."""

    def __init__(self) -> None:
        self.vehicles: Dict[str, int] = {}

    def add_vehicle(self, car_name: str) -> int:
        """Add a vehicle with full health."""
        self.vehicles[car_name] = 100
        return self.vehicles[car_name]

    def apply_damage(self, car_name: str, damage: int) -> int:
        """
        Apply damage to a vehicle.
        """
        current = self.vehicles.get(car_name, 100)
        self.vehicles[car_name] = max(0, current - damage)
        return self.vehicles[car_name]

    def get_health(self, car_name: str) -> int:
        """Return current health for a vehicle (defaults to 0 if unknown)."""
        return self.vehicles.get(car_name, 0)

    def is_usable(self, car_name: str) -> bool:
        """Return True if the vehicle health is above 0."""
        return self.get_health(car_name) > 0

    def repair_vehicle(self, car_name: str, amount: int) -> int:
        """Repair a vehicle; health cannot exceed 100."""
        current = self.vehicles.get(car_name, 0)
        self.vehicles[car_name] = min(100, current + amount)
        return self.vehicles[car_name]
