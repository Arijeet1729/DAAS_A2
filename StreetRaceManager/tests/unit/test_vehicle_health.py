import pytest

from code.vehicle_health import VehicleHealthMonitor


def test_vehicle_health_monitor_instantiation():
    monitor = VehicleHealthMonitor()
    assert monitor is not None

