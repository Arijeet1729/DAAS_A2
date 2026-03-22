"""White-box tests for bank behavior."""

import pytest

from moneypoly.bank import Bank
from moneypoly.player import Player


def test_pay_out_returns_amount_and_reduces_funds():
    bank = Bank()
    before = bank.get_balance()

    amount = bank.pay_out(500)

    assert amount == 500
    assert bank.get_balance() == before - 500


def test_pay_out_returns_zero_for_zero_amount():
    bank = Bank()
    before = bank.get_balance()

    amount = bank.pay_out(0)

    assert amount == 0
    assert bank.get_balance() == before


def test_pay_out_returns_zero_for_negative_amount():
    bank = Bank()
    before = bank.get_balance()

    amount = bank.pay_out(-10)

    assert amount == 0
    assert bank.get_balance() == before


def test_pay_out_raises_when_amount_exceeds_funds():
    bank = Bank()

    with pytest.raises(ValueError):
        bank.pay_out(bank.get_balance() + 1)


def test_collect_ignores_negative_amounts_per_docstring():
    bank = Bank()
    before = bank.get_balance()

    bank.collect(-100)

    assert bank.get_balance() == before


def test_give_loan_reduces_bank_funds_and_increases_player_balance():
    bank = Bank()
    player = Player("Alice")
    before = bank.get_balance()

    bank.give_loan(player, 200)

    assert player.balance == 1700
    assert bank.get_balance() == before - 200
