import pytest

from code.inventory import InventoryManager
from code.race import RaceController
from code.results import ResultsTracker


def test_it_05_prize_money_updates_inventory():
    race = RaceController()
    results = ResultsTracker()
    inventory = InventoryManager()
    from code.registration import RegistrationManager

    RegistrationManager().register_member("Alex", "Driver")
    race.create_race("R4")
    race.assign_driver("R4", "Alex", "Driver")
    results.record_winner("R4", "Alex", prize=500, inventory=inventory)

    # Expected: inventory cash increases by 500
    assert inventory.cash == 500
    # Actual (bug): cash remains 0 because prize not applied


def test_it_06_cash_should_not_go_negative():
    inventory = InventoryManager()
    results = ResultsTracker()

    inventory.update_cash(100)
    with pytest.raises(ValueError):
        inventory.update_cash(-300)  # expense beyond balance
    results.record_winner("R6", "Alex", prize=50, inventory=inventory)
    assert inventory.cash == 150


def test_it_15_multiple_wins_sum_prize_money():
    race = RaceController()
    results = ResultsTracker()
    inventory = InventoryManager()
    from code.registration import RegistrationManager

    RegistrationManager().register_member("Champion", "Driver")

    total_prize = 0
    for i in range(3):
        race_id = f"R_multi_{i}"
        race.create_race(race_id)
        race.assign_driver(race_id, "Champion", "Driver")
        prize = 200
        total_prize += prize
        results.record_winner(race_id, "Champion", prize=prize, inventory=inventory)

    assert inventory.cash == total_prize


def test_it_16_expense_then_prize_net_balance():
    inventory = InventoryManager()
    results = ResultsTracker()

    inventory.update_cash(1000)
    inventory.update_cash(-300)  # entry fee
    results.record_winner("R16", "Alex", prize=500, inventory=inventory)

    assert inventory.cash == 1200


def test_it_19_mission_cost_deducts_cash():
    inventory = InventoryManager()

    inventory.update_cash(200)
    with pytest.raises(ValueError):
        inventory.update_cash(-400)  # mission cost simulated


def test_it_20_mission_cost_exceeds_cash():
    inventory = InventoryManager()

    inventory.update_cash(100)
    with pytest.raises(ValueError):
        inventory.update_cash(-500)  # mission cost simulated


def test_it_28_prize_then_mission_cost_balance():
    results = ResultsTracker()
    inventory = InventoryManager()

    results.record_winner("R28", "Alex", prize=1000, inventory=inventory)
    inventory.update_cash(-400)

    assert inventory.cash == 600
