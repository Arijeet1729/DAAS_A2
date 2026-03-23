import pytest

from code.vehicle_health import VehicleHealthMonitor
from code.mission import MissionPlanner
from code.crew import CrewManager
from code.registration import RegistrationManager


def test_it_07_damage_then_mechanic_mission():
    health = VehicleHealthMonitor()
    mission = MissionPlanner()
    crew = CrewManager()

    health.add_vehicle("CarA")
    health.apply_damage("CarA", 80)
    mission.create_mission("M1", ["Mechanic"])
    crew.assign_role("Morgan", "Mechanic")
    mission.assign_mission("M1", "Morgan", crew.get_role("Morgan"))

    # Expected: car health = 20, mission only proceeds with mechanic
    assert health.get_health("CarA") == 20
    assignees = mission.list_assignees("M1")
    assert all(a["role"] == "Mechanic" for a in assignees)
    # Actual (bug): damage halved -> health 60; mission accepts any role


def test_it_08_heavy_damage_blocks_mission():
    health = VehicleHealthMonitor()
    mission = MissionPlanner()

    health.add_vehicle("CarB")
    health.apply_damage("CarB", 200)
    mission.create_mission("M2", ["Mechanic"])
    mission.assign_mission("M2", "Alex", "Mechanic")

    # Expected: car unusable (0 health) so mission should be blocked
    assert health.is_usable("CarB") is False
    # Actual (bug): damage halved so car may still be usable


def test_it_13_damage_repair_then_race_readiness():
    health = VehicleHealthMonitor()
    mission = MissionPlanner()
    crew = CrewManager()

    health.add_vehicle("CarC")
    health.apply_damage("CarC", 90)
    mission.create_mission("M3", ["Mechanic"])
    crew.assign_role("Jamie", "Mechanic")
    mission.assign_mission("M3", "Jamie", crew.get_role("Jamie"))
    health.repair_vehicle("CarC", 90)

    # Expected: car repaired to 100 before race use
    assert health.get_health("CarC") == 100
    # Actual (bug): damage halved earlier; repair may over-shoot logic but here still 100


def test_it_17_health_zero_retires_driver():
    health = VehicleHealthMonitor()

    health.add_vehicle("CarD")
    health.apply_damage("CarD", 200)

    # Expected: health 0, unusable
    assert health.get_health("CarD") == 0
    assert health.is_usable("CarD") is False
    # Actual (bug): health > 0 because damage halved


def test_it_18_mechanic_repairs_car_reenters():
    reg = RegistrationManager()
    crew = CrewManager()
    mission = MissionPlanner()
    health = VehicleHealthMonitor()

    reg.register_member("Pat", "Mechanic")
    crew.assign_role("Pat", "Mechanic")
    health.add_vehicle("CarE")
    health.apply_damage("CarE", 60)
    mission.create_mission("M4", ["Mechanic"])
    mission.assign_mission("M4", "Pat", crew.get_role("Pat"))
    health.repair_vehicle("CarE", 60)

    # Expected: car back to 100 and usable
    assert health.get_health("CarE") == 100
    assert health.is_usable("CarE") is True
    # Actual (bug): damage halved earlier; flows still allow role bypass


def test_it_25_race_with_partially_damaged_car():
    health = VehicleHealthMonitor()

    health.add_vehicle("CarF")
    health.apply_damage("CarF", 30)

    # Expected: health 70 after damage
    assert health.get_health("CarF") == 70
    # Actual (bug): damage halved -> health 85
