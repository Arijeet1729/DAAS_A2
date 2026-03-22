import requests

from .conftest import BASE_URL, TIMEOUT, assert_keys, request_headers


def test_get_loyalty_points_returns_expected_structure():
    response = requests.get(f"{BASE_URL}/loyalty", headers=request_headers(1), timeout=TIMEOUT)

    assert response.status_code == 200
    payload = response.json()
    assert_keys(payload, ["loyalty_points"])
    assert isinstance(payload["loyalty_points"], int)


def test_redeem_valid_points_succeeds():
    before_response = requests.get(f"{BASE_URL}/loyalty", headers=request_headers(1), timeout=TIMEOUT)
    before_points = before_response.json()["loyalty_points"]

    response = requests.post(
        f"{BASE_URL}/loyalty/redeem",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"amount": 1},
        timeout=TIMEOUT,
    )

    assert response.status_code == 200
    payload = response.json()
    assert "loyalty_points" in payload or "message" in payload

    after_response = requests.get(f"{BASE_URL}/loyalty", headers=request_headers(1), timeout=TIMEOUT)
    after_points = after_response.json()["loyalty_points"]
    assert after_points == before_points - 1


def test_redeem_more_points_than_available_returns_400():
    current_points = requests.get(f"{BASE_URL}/loyalty", headers=request_headers(1), timeout=TIMEOUT).json()[
        "loyalty_points"
    ]

    response = requests.post(
        f"{BASE_URL}/loyalty/redeem",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"amount": current_points + 1},
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    assert "error" in response.json()


def test_redeem_zero_points_returns_400():
    response = requests.post(
        f"{BASE_URL}/loyalty/redeem",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"amount": 0},
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    assert "error" in response.json()


def test_redeem_negative_points_returns_400():
    response = requests.post(
        f"{BASE_URL}/loyalty/redeem",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"amount": -5},
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    assert "error" in response.json()


def test_get_loyalty_without_roll_number_returns_401():
    response = requests.get(
        f"{BASE_URL}/loyalty",
        headers={"X-User-ID": "1"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 401
    assert "error" in response.json()


def test_get_loyalty_without_user_id_returns_400():
    response = requests.get(
        f"{BASE_URL}/loyalty",
        headers={"X-Roll-Number": "123"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    assert "error" in response.json()


def test_loyalty_points_decrease_correctly_after_redeem():
    before_points = requests.get(
        f"{BASE_URL}/loyalty",
        headers=request_headers(1),
        timeout=TIMEOUT,
    ).json()["loyalty_points"]

    response = requests.post(
        f"{BASE_URL}/loyalty/redeem",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"amount": 2},
        timeout=TIMEOUT,
    )

    assert response.status_code == 200
    after_points = requests.get(
        f"{BASE_URL}/loyalty",
        headers=request_headers(1),
        timeout=TIMEOUT,
    ).json()["loyalty_points"]

    assert after_points == before_points - 2
