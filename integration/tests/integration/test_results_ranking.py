import pytest

from code.results import ResultsTracker
from code.ranking import RankingCalculator


def test_it_10_winner_ranking_order():
    results = ResultsTracker()
    ranking = RankingCalculator()

    ranking.record_win("Blake")
    ranking.record_win("Blake")
    ranking.record_win("Blake")
    ranking.record_win("Alex")
    ranking.record_win("Alex")
    ranking.record_win("Casey")

    ordered = [name for name, _ in ranking.get_rankings()]

    # Expected: Blake first, then Alex, then Casey
    assert ordered == ["Blake", "Alex", "Casey"]
    # Actual (bug): ascending sort puts Casey or Alex before Blake


def test_it_11_loser_no_win_increase():
    results = ResultsTracker()
    ranking = RankingCalculator()

    results.record_winner("R1", "Alex", prize=0)
    ranking.record_win("Alex")
    # Jordan participated but did not win; no record_win for Jordan

    assert ranking.get_wins("Jordan") == 0
    # Actual (bug risk): ascending sort may still order Jordan above Alex when equal/zero


def test_it_23_loser_ranking_after_single_race():
    ranking = RankingCalculator()

    ranking.record_win("DriverA")
    # DriverB loses; no win recorded

    ordered = [name for name, _ in ranking.get_rankings()]

    # Expected: DriverA ahead of DriverB
    assert ordered[0] == "DriverA"
    # Actual (bug): ascending order could place DriverB first with 0 wins


def test_it_24_rankings_after_zero_races():
    ranking = RankingCalculator()

    ranking.rankings["A"] = 0
    ranking.rankings["B"] = 0
    ranking.rankings["C"] = 0

    ordered = [name for name, _ in ranking.get_rankings()]

    # Expected: stable order, but content is all zeros
    assert ordered == ["A", "B", "C"]
    # Actual (bug): order may be arbitrary due to ascending sort on equal values
