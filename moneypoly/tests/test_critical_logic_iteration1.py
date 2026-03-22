from unittest.mock import patch

from moneypoly.dice import Dice
from moneypoly.game import Game
from moneypoly.player import Player
from moneypoly.property import Property


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
