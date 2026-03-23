import pytest

from code.ranking import RankingCalculator


def test_record_win():
    calc = RankingCalculator()

    wins = calc.record_win("Alex")

    assert wins == 1
    assert calc.get_wins("Alex") == 1


def test_multiple_wins():
    calc = RankingCalculator()
    calc.record_win("Blake")
    calc.record_win("Blake")

    assert calc.get_wins("Blake") == 2


def test_ranking_order():
    calc = RankingCalculator()
    calc.record_win("Alex")           # 1 win
    calc.record_win("Casey")          # 1 win
    calc.record_win("Blake")          # 1 win
    calc.record_win("Blake")          # Blake now 2 wins

    rankings = calc.get_rankings()
    driver_order = [name for name, _ in rankings]

    # Expected: Blake first (most wins). Actual (bug): ascending order puts Blake last.
    assert driver_order[0] == "Blake"


def test_new_driver_default():
    calc = RankingCalculator()

    assert calc.get_wins("Dana") == 0
