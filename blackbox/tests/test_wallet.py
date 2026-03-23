import requests

from .conftest import BASE_URL, TIMEOUT, assert_keys, request_headers


def test_get_wallet_returns_balance_field():
    response = requests.get(f"{BASE_URL}/wallet", headers=request_headers(1), timeout=TIMEOUT)

    assert response.status_code == 200
    payload = response.json()
    assert_keys(payload, ["wallet_balance"])


def test_add_money_to_wallet_returns_updated_balance():
    response = requests.post(
        f"{BASE_URL}/wallet/add",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"amount": 1},
        timeout=TIMEOUT,
    )

    assert response.status_code == 200
    assert "wallet_balance" in response.json()


def test_pay_from_wallet_returns_updated_balance():
    requests.post(
        f"{BASE_URL}/wallet/add",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"amount": 5},
        timeout=TIMEOUT,
    )

    response = requests.post(
        f"{BASE_URL}/wallet/pay",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"amount": 5},
        timeout=TIMEOUT,
    )

    assert response.status_code == 200
    assert "wallet_balance" in response.json()


def test_add_zero_wallet_amount_returns_400():
    response = requests.post(
        f"{BASE_URL}/wallet/add",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"amount": 0},
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    assert "error" in response.json()


def test_wallet_pay_with_insufficient_balance_returns_400():
    response = requests.post(
        f"{BASE_URL}/wallet/pay",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"amount": 999999},
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    assert "error" in response.json()


def test_add_more_than_max_wallet_amount_returns_400():
    response = requests.post(
        f"{BASE_URL}/wallet/add",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"amount": 100001},
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    assert "error" in response.json()


def test_wallet_deduction_is_exact():
    before_response = requests.get(f"{BASE_URL}/wallet", headers=request_headers(1), timeout=TIMEOUT)
    before_balance = before_response.json()["wallet_balance"]

    add_response = requests.post(
        f"{BASE_URL}/wallet/add",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"amount": 7},
        timeout=TIMEOUT,
    )
    after_add_balance = add_response.json()["wallet_balance"]

    pay_response = requests.post(
        f"{BASE_URL}/wallet/pay",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"amount": 7},
        timeout=TIMEOUT,
    )
    after_pay_balance = pay_response.json()["wallet_balance"]

    assert after_add_balance == before_balance + 7
    assert after_pay_balance == before_balance
