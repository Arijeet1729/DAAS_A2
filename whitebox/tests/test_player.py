"""White-box tests for player behavior."""

import pytest

from moneypoly.player import Player
from moneypoly.property import Property


def test_add_money_increases_balance_for_positive_amount():
    player = Player("Alice", balance=1000)

    player.add_money(200)

    assert player.balance == 1200


def test_add_money_accepts_zero_amount():
    player = Player("Alice", balance=1000)

    player.add_money(0)

    assert player.balance == 1000


def test_add_money_raises_for_negative_amount():
    player = Player("Alice", balance=1000)

    with pytest.raises(ValueError):
        player.add_money(-1)


def test_add_money_handles_very_large_positive_amount():
    player = Player("Alice", balance=1500)

    player.add_money(1_000_000)

    assert player.balance == 1_001_500


def test_deduct_money_reduces_balance_for_positive_amount():
    player = Player("Alice", balance=1000)

    player.deduct_money(200)

    assert player.balance == 800


def test_deduct_money_accepts_zero_amount():
    player = Player("Alice", balance=1000)

    player.deduct_money(0)

    assert player.balance == 1000


def test_deduct_money_raises_for_negative_amount():
    player = Player("Alice", balance=1000)

    with pytest.raises(ValueError):
        player.deduct_money(-1)


def test_deduct_money_allows_balance_to_go_negative():
    player = Player("Alice", balance=10)

    player.deduct_money(1000)

    assert player.balance == -990


def test_move_without_passing_go_keeps_balance_unchanged():
    player = Player("Alice", balance=1000)
    player.position = 5

    new_position = player.move(6)

    assert new_position == 11
    assert player.balance == 1000


def test_move_landing_exactly_on_go_awards_salary():
    player = Player("Alice", balance=1000)
    player.position = 38

    new_position = player.move(2)

    assert new_position == 0
    assert player.balance == 1200


def test_move_passing_go_awards_salary():
    player = Player("Alice", balance=1000)
    player.position = 39

    new_position = player.move(2)

    assert new_position == 1
    assert player.balance == 1200


def test_net_worth_includes_property_values():
    player = Player("Alice", balance=100)
    player.add_property(Property("Test Avenue", 1, 200, 10))

    assert player.net_worth() == 300
