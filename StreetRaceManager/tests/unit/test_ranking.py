import pytest

from code.ranking import RankingCalculator


def test_ranking_calculator_instantiation():
    calculator = RankingCalculator()
    assert calculator is not None

