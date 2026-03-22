from unittest.mock import patch

import pytest

from moneypoly.cards import CardDeck
from moneypoly.dice import Dice
from moneypoly.game import Game
from moneypoly.player import Player
from moneypoly.property import Property, PropertyGroup


def test_player_collects_salary_when_passing_go():
    player = Player("Alice", balance=1000)
    player.position = 39

    new_position = player.move(2)

    assert new_position == 1
    assert player.balance == 1200


def test_dice_roll_uses_full_six_sided_range():
    dice = Dice()

    with patch("moneypoly.dice.random.randint", side_effect=[6, 6]):
        total = dice.roll()

    assert dice.die1 == 6
    assert dice.die2 == 6
    assert total == 12


def test_buy_property_allows_exact_balance_purchase():
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    prop = Property("Test Avenue", 1, 100, 10)
    player.balance = 100

    bought = game.buy_property(player, prop)

    assert bought is True
    assert player.balance == 0
    assert prop.owner == player


def test_pay_rent_credits_owner():
    game = Game(["Alice", "Bob"])
    tenant = game.players[0]
    owner = game.players[1]
    prop = Property("Test Avenue", 1, 100, 25)
    prop.owner = owner
    owner.add_property(prop)

    game.pay_rent(tenant, prop)

    assert tenant.balance == 1475
    assert owner.balance == 1525


def test_find_winner_returns_highest_net_worth_player():
    game = Game(["Alice", "Bob", "Cara"])
    game.players[0].balance = 100
    game.players[1].balance = 300
    game.players[2].balance = 200

    winner = game.find_winner()

    assert winner.name == "Bob"


def test_group_bonus_requires_full_group_ownership():
    group = PropertyGroup("Test", "test")
    owner = Player("Alice")
    other = Player("Bob")
    first = Property("First", 1, 100, 10, group)
    second = Property("Second", 3, 100, 10, group)
    first.owner = owner
    second.owner = other

    assert first.get_rent() == 10


def test_empty_card_deck_is_safe_to_query():
    deck = CardDeck([])

    assert deck.cards_remaining() == 0
    assert repr(deck) == "CardDeck(0 cards, next=empty)"


def test_unmortgage_does_not_change_state_when_player_cannot_afford_it():
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    prop = Property("Test Avenue", 1, 100, 10)
    prop.owner = player
    player.add_property(prop)
    prop.is_mortgaged = True
    player.balance = 54

    success = game.unmortgage_property(player, prop)

    assert success is False
    assert prop.is_mortgaged is True


def test_trade_credits_seller_with_cash_amount():
    game = Game(["Alice", "Bob"])
    seller = game.players[0]
    buyer = game.players[1]
    prop = Property("Test Avenue", 1, 100, 10)
    prop.owner = seller
    seller.add_property(prop)

    success = game.trade(seller, buyer, prop, 200)

    assert success is True
    assert seller.balance == 1700
    assert buyer.balance == 1300


def test_voluntary_jail_fine_deducts_player_balance():
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    player.in_jail = True

    with patch("moneypoly.ui.confirm", return_value=True), patch.object(
        game.dice, "roll", return_value=2
    ), patch.object(game, "_move_and_resolve") as move_and_resolve:
        game._handle_jail_turn(player)

    assert player.balance == 1450
    move_and_resolve.assert_called_once_with(player, 2)


def test_game_requires_at_least_two_players():
    with pytest.raises(ValueError):
        Game(["Solo"])


def test_bank_loan_reduces_bank_funds():
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    before = game.bank.get_balance()

    game.bank.give_loan(player, 200)

    assert player.balance == 1700
    assert game.bank.get_balance() == before - 200


def test_railroad_tiles_have_properties():
    game = Game(["Alice", "Bob"])

    assert game.board.get_property_at(5) is not None
    assert game.board.get_property_at(15) is not None
    assert game.board.get_property_at(25) is not None
    assert game.board.get_property_at(35) is not None


def test_move_to_card_resolves_railroad_property():
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    player.position = 4
    railroad = game.board.get_property_at(5)

    with patch.object(game, "_handle_property_tile") as handle_property_tile:
        game._apply_card(player, {"description": "Move", "action": "move_to", "value": 5})

    assert player.position == 5
    handle_property_tile.assert_called_once_with(player, railroad)


def test_net_worth_includes_property_values():
    player = Player("Alice", balance=100)
    player.add_property(Property("Test Avenue", 1, 200, 10))

    assert player.net_worth() == 300
