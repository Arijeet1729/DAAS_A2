import pytest

from code.registration import RegistrationManager
from code.crew import CrewManager
from code.race import RaceController
from code.results import ResultsTracker
from code.inventory import InventoryManager
from code.ranking import RankingCalculator
from code.vehicle_health import VehicleHealthMonitor
from code.mission import MissionPlanner


def test_it_12_end_to_end_race_prize_ranking():
    reg = RegistrationManager()
    crew = CrewManager()
    race = RaceController()
    results = ResultsTracker()
    inventory = InventoryManager()
    ranking = RankingCalculator()

    reg.register_member("Alex", "Driver")
    reg.register_member("Blake", "Driver")
    crew.assign_role("Alex", "Driver")
    crew.assign_role("Blake", "Driver")

    race.create_race("R5")
    race.assign_driver("R5", "Alex", crew.get_role("Alex"))
    race.assign_driver("R5", "Blake", crew.get_role("Blake"))

    results.record_winner("R5", "Alex", prize=1000, inventory=inventory)
    ranking.record_win("Alex")

    # Expected: inventory +1000 and Alex ranked above Blake
    assert inventory.cash == 1000
    ordered = [name for name, _ in ranking.get_rankings()]
    assert ordered[0] == "Alex"
    # Actual (bug): prize not applied; rankings ascending could misorder


def test_it_30_full_lifecycle_damage_repair_race_prize():
    reg = RegistrationManager()
    crew = CrewManager()
    health = VehicleHealthMonitor()
    mission = MissionPlanner()
    race = RaceController()
    results = ResultsTracker()
    inventory = InventoryManager()
    ranking = RankingCalculator()

    reg.register_member("DriverOne", "Driver")
    reg.register_member("Fixer", "Mechanic")
    crew.assign_role("DriverOne", "Driver")
    crew.assign_role("Fixer", "Mechanic")

    health.add_vehicle("CarZ")
    health.apply_damage("CarZ", 120)

    mission.create_mission("M_full", ["Mechanic"])
    mission.assign_mission("M_full", "Fixer", crew.get_role("Fixer"))
    health.repair_vehicle("CarZ", 120)

    race.create_race("R_full")
    race.assign_driver("R_full", "DriverOne", crew.get_role("DriverOne"))
    results.record_winner("R_full", "DriverOne", prize=800, inventory=inventory)
    ranking.record_win("DriverOne")

    # Expected: car was unusable until repaired; prize applied; driver ranked first; cash = 800
    assert health.get_health("CarZ") == 100
    assert inventory.cash == 800
    assert ranking.get_rankings()[0][0] == "DriverOne"
    # Actual (bug): damage halved so car never unusable; prize ignored; ranking ascending
