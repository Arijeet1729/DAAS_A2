"""White-box tests for board behavior."""

from moneypoly.board import Board
from moneypoly.player import Player


def test_is_purchasable_returns_false_for_non_property_tile():
    board = Board()

    assert board.is_purchasable(0) is False


def test_is_purchasable_returns_false_for_mortgaged_property():
    board = Board()
    prop = board.get_property_at(1)
    prop.owner = Player("Alice")
    prop.is_mortgaged = True

    assert board.is_purchasable(1) is False


def test_is_purchasable_returns_true_for_unowned_unmortgaged_property():
    board = Board()
    prop = board.get_property_at(1)
    prop.owner = None
    prop.is_mortgaged = False

    assert board.is_purchasable(1) is True


def test_is_purchasable_returns_false_for_owned_unmortgaged_property():
    board = Board()
    prop = board.get_property_at(1)
    prop.owner = Player("Alice")
    prop.is_mortgaged = False

    assert board.is_purchasable(1) is False


def test_railroad_tiles_have_properties():
    board = Board()

    assert board.get_property_at(5) is not None
    assert board.get_property_at(15) is not None
    assert board.get_property_at(25) is not None
    assert board.get_property_at(35) is not None
