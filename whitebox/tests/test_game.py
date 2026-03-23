"""White-box tests for game behavior."""

from unittest.mock import patch

import pytest

from moneypoly.cards import CardDeck
from moneypoly.game import Game
from moneypoly.player import Player
from moneypoly.property import Property, PropertyGroup


def make_game(player_names=None):
    names = player_names or ["Alice", "Bob"]
    return Game(names)


def test_game_requires_at_least_two_players():
    with pytest.raises(ValueError):
        Game(["Solo"])


def test_buy_property_succeeds_with_surplus_balance():
    game = make_game()
    player = game.players[0]
    prop = Property("Test Avenue", 1, 100, 10)
    player.balance = 500

    bought = game.buy_property(player, prop)

    assert bought is True
    assert player.balance == 400
    assert prop.owner == player
    assert prop in player.properties


def test_buy_property_succeeds_with_exact_balance():
    game = make_game()
    player = game.players[0]
    prop = Property("Test Avenue", 1, 100, 10)
    player.balance = 100

    bought = game.buy_property(player, prop)

    assert bought is True
    assert player.balance == 0
    assert prop.owner == player


def test_buy_property_fails_when_balance_is_too_low():
    game = make_game()
    player = game.players[0]
    prop = Property("Test Avenue", 1, 100, 10)
    player.balance = 99

    bought = game.buy_property(player, prop)

    assert bought is False
    assert player.balance == 99
    assert prop.owner is None


def test_buy_property_rejects_property_that_is_already_owned():
    game = make_game()
    buyer = game.players[0]
    owner = game.players[1]
    prop = Property("Test Avenue", 1, 100, 10)
    prop.owner = owner
    owner.add_property(prop)

    bought = game.buy_property(buyer, prop)

    assert bought is False
    assert prop.owner == owner
    assert prop not in buyer.properties


def test_pay_rent_returns_early_for_mortgaged_property():
    game = make_game()
    tenant, owner = game.players
    prop = Property("Test Avenue", 1, 100, 25)
    prop.owner = owner
    prop.is_mortgaged = True

    game.pay_rent(tenant, prop)

    assert tenant.balance == 1500
    assert owner.balance == 1500


def test_pay_rent_returns_early_for_unowned_property():
    game = make_game()
    tenant = game.players[0]
    prop = Property("Test Avenue", 1, 100, 25)

    game.pay_rent(tenant, prop)

    assert tenant.balance == 1500


def test_pay_rent_transfers_money_to_owner():
    game = make_game()
    tenant, owner = game.players
    prop = Property("Test Avenue", 1, 100, 25)
    prop.owner = owner
    owner.add_property(prop)

    game.pay_rent(tenant, prop)

    assert tenant.balance == 1475
    assert owner.balance == 1525


def test_group_bonus_requires_full_group_ownership():
    group = PropertyGroup("Test", "test")
    owner = Player("Alice")
    other = Player("Bob")
    first = Property("First", 1, 100, 10, group)
    second = Property("Second", 3, 100, 10, group)
    first.owner = owner
    second.owner = other

    assert first.get_rent() == 10


def test_apply_card_returns_immediately_for_none_card():
    game = make_game()
    player = game.players[0]
    bank_balance = game.bank.get_balance()

    game._apply_card(player, None)

    assert player.balance == 1500
    assert game.bank.get_balance() == bank_balance


def test_apply_card_collect_increases_player_balance():
    game = make_game()
    player = game.players[0]
    bank_balance = game.bank.get_balance()

    game._apply_card(
        player, {"description": "Collect", "action": "collect", "value": 50}
    )

    assert player.balance == 1550
    assert game.bank.get_balance() == bank_balance - 50


def test_apply_card_pay_decreases_player_balance():
    game = make_game()
    player = game.players[0]
    bank_balance = game.bank.get_balance()

    game._apply_card(player, {"description": "Pay", "action": "pay", "value": 50})

    assert player.balance == 1450
    assert game.bank.get_balance() == bank_balance + 50


def test_apply_card_jail_sends_player_to_jail():
    game = make_game()
    player = game.players[0]
    player.position = 7

    game._apply_card(player, {"description": "Jail", "action": "jail", "value": 0})

    assert player.in_jail is True
    assert player.position == 10


def test_apply_card_jail_free_increments_card_count():
    game = make_game()
    player = game.players[0]

    game._apply_card(
        player, {"description": "Jail Free", "action": "jail_free", "value": 0}
    )

    assert player.get_out_of_jail_cards == 1


def test_apply_card_move_to_property_without_passing_go():
    game = make_game()
    player = game.players[0]
    player.position = 5
    prop = game.board.get_property_at(6)

    with patch.object(game, "_handle_property_tile") as handle_property_tile:
        game._apply_card(
            player, {"description": "Move", "action": "move_to", "value": 6}
        )

    assert player.position == 6
    assert player.balance == 1500
    handle_property_tile.assert_called_once_with(player, prop)


def test_apply_card_move_to_railroad_after_passing_go():
    game = make_game()
    player = game.players[0]
    player.position = 39
    railroad = game.board.get_property_at(5)

    with patch.object(game, "_handle_property_tile") as handle_property_tile:
        game._apply_card(
            player, {"description": "Move", "action": "move_to", "value": 5}
        )

    assert player.position == 5
    assert player.balance == 1700
    handle_property_tile.assert_called_once_with(player, railroad)


def test_apply_card_birthday_collects_only_from_players_who_can_pay():
    game = make_game(["Alice", "Bob", "Cara"])
    current = game.players[0]
    game.players[1].balance = 5
    game.players[2].balance = 20

    game._apply_card(
        current, {"description": "Birthday", "action": "birthday", "value": 10}
    )

    assert current.balance == 1510
    assert game.players[1].balance == 5
    assert game.players[2].balance == 10


def test_apply_card_collect_from_all_skips_players_without_funds():
    game = make_game(["Alice", "Bob", "Cara"])
    current = game.players[0]
    game.players[1].balance = 50
    game.players[2].balance = 30

    game._apply_card(
        current,
        {"description": "Collect", "action": "collect_from_all", "value": 50},
    )

    assert current.balance == 1550
    assert game.players[1].balance == 0
    assert game.players[2].balance == 30


def test_apply_card_collect_from_all_with_zero_money_players_is_no_op():
    game = make_game(["Alice", "Bob", "Cara"])
    current = game.players[0]
    game.players[1].balance = 0
    game.players[2].balance = 0

    game._apply_card(
        current,
        {"description": "Collect", "action": "collect_from_all", "value": 50},
    )

    assert current.balance == 1500
    assert game.players[1].balance == 0
    assert game.players[2].balance == 0


def test_apply_card_birthday_with_large_value_does_not_transfer_money():
    game = make_game(["Alice", "Bob", "Cara"])
    current = game.players[0]

    game._apply_card(
        current, {"description": "Birthday", "action": "birthday", "value": 100000}
    )

    assert current.balance == 1500
    assert game.players[1].balance == 1500
    assert game.players[2].balance == 1500


def test_apply_card_move_to_special_tile_resolves_tile_effect():
    game = make_game()
    player = game.players[0]
    player.position = 5

    game._apply_card(
        player,
        {"description": "Advance to luxury tax", "action": "move_to", "value": 38},
    )

    assert player.position == 38
    assert player.balance == 1425


def test_apply_card_ignores_unknown_action():
    game = make_game()
    player = game.players[0]
    bank_balance = game.bank.get_balance()

    game._apply_card(player, {"description": "Unknown", "action": "other", "value": 0})

    assert player.balance == 1500
    assert game.bank.get_balance() == bank_balance


def test_check_bankruptcy_leaves_solvent_player_unchanged():
    game = make_game()
    player = game.players[0]
    prop = Property("Test Avenue", 1, 100, 10)
    prop.owner = player
    player.add_property(prop)

    game._check_bankruptcy(player)

    assert player.is_eliminated is False
    assert player in game.players
    assert prop.owner == player


def test_check_bankruptcy_removes_bankrupt_player_and_resets_properties():
    game = make_game()
    player = game.players[0]
    prop = Property("Test Avenue", 1, 100, 10)
    prop.owner = player
    prop.is_mortgaged = True
    player.add_property(prop)
    player.balance = 0

    game._check_bankruptcy(player)

    assert player.is_eliminated is True
    assert player not in game.players
    assert prop.owner is None
    assert prop.is_mortgaged is False


def test_check_bankruptcy_resets_current_index_after_last_player_removed():
    game = make_game(["Alice", "Bob", "Cara"])
    player = game.players[2]
    game.current_index = 2
    player.balance = 0

    game._check_bankruptcy(player)

    assert game.current_index == 0


def test_check_bankruptcy_handles_player_missing_from_roster():
    game = make_game()
    player = Player("Ghost", balance=0)
    prop = Property("Test Avenue", 1, 100, 10)
    prop.owner = player
    player.add_property(prop)

    game._check_bankruptcy(player)

    assert player.is_eliminated is True
    assert player not in game.players
    assert prop.owner is None


def test_check_bankruptcy_preserves_current_player_after_earlier_player_removed():
    game = make_game(["Alice", "Bob", "Cara"])
    game.current_index = 2
    removed_player = game.players[0]
    current_player_before = game.players[2]
    removed_player.balance = 0

    game._check_bankruptcy(removed_player)

    assert game.current_player() == current_player_before


def test_check_bankruptcy_handles_multiple_bankrupt_players_sequentially():
    game = make_game(["Alice", "Bob", "Cara"])
    first = game.players[0]
    second = game.players[1]
    first.balance = 0
    second.balance = 0

    game._check_bankruptcy(first)
    game._check_bankruptcy(second)

    assert len(game.players) == 1
    assert game.players[0].name == "Cara"


def test_empty_card_deck_is_safe_to_query():
    deck = CardDeck([])

    assert deck.cards_remaining() == 0
    assert repr(deck) == "CardDeck(0 cards, next=empty)"


def test_unmortgage_does_not_change_state_when_player_cannot_afford_it():
    game = make_game()
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
    game = make_game()
    seller = game.players[0]
    buyer = game.players[1]
    prop = Property("Test Avenue", 1, 100, 10)
    prop.owner = seller
    seller.add_property(prop)

    success = game.trade(seller, buyer, prop, 200)

    assert success is True
    assert seller.balance == 1700
    assert buyer.balance == 1300


def test_trade_rejects_negative_cash_amount():
    game = make_game()
    seller = game.players[0]
    buyer = game.players[1]
    prop = Property("Test Avenue", 1, 100, 10)
    prop.owner = seller
    seller.add_property(prop)

    success = game.trade(seller, buyer, prop, -10)

    assert success is False
    assert prop.owner == seller
    assert seller.balance == 1500
    assert buyer.balance == 1500


def test_voluntary_jail_fine_deducts_player_balance():
    game = make_game()
    player = game.players[0]
    player.in_jail = True

    with patch("moneypoly.ui.confirm", return_value=True), patch.object(
        game.dice, "roll", return_value=2
    ), patch.object(game, "_move_and_resolve") as move_and_resolve:
        game._handle_jail_turn(player)

    assert player.balance == 1450
    move_and_resolve.assert_called_once_with(player, 2)


def test_auction_property_allows_additional_rounds_after_outbid():
    game = make_game()
    prop = Property("Test Avenue", 1, 100, 10)

    with patch("moneypoly.ui.safe_int_input", side_effect=[50, 60, 70, 0]):
        game.auction_property(prop)

    assert prop.owner == game.players[0]
    assert game.players[0].balance == 1430
    assert game.players[1].balance == 1500


def test_find_winner_returns_highest_net_worth_player():
    game = make_game(["Alice", "Bob", "Cara"])
    game.players[0].balance = 100
    game.players[1].balance = 300
    game.players[2].balance = 200

    winner = game.find_winner()

    assert winner.name == "Bob"
