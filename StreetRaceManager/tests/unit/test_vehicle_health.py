import pytest

from code.vehicle_health import VehicleHealthMonitor


def test_add_vehicle():
    monitor = VehicleHealthMonitor()

    health = monitor.add_vehicle("CarA")

    assert health == 100
    assert monitor.get_health("CarA") == 100


def test_apply_damage():
    monitor = VehicleHealthMonitor()
    monitor.add_vehicle("CarB")

    monitor.apply_damage("CarB", 50)

    # Expected: 50; Actual: damage is halved, so health stays higher (bug).
    assert monitor.get_health("CarB") == 50


def test_vehicle_unusable():
    monitor = VehicleHealthMonitor()
    monitor.add_vehicle("CarC")

    monitor.apply_damage("CarC", 120)

    # Expected: unusable (health <= 0); Actual: damage halved so may still be usable.
    assert monitor.is_usable("CarC") is False


def test_repair_vehicle():
    monitor = VehicleHealthMonitor()
    monitor.add_vehicle("CarD")
    monitor.apply_damage("CarD", 80)  # With bug, only 40 damage applied

    monitor.repair_vehicle("CarD", 30)

    assert monitor.get_health("CarD") <= 100
