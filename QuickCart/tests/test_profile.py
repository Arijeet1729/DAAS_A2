import requests

from .conftest import BASE_URL, TIMEOUT, assert_keys, request_headers


def test_get_profile_returns_expected_fields():
    response = requests.get(f"{BASE_URL}/profile", headers=request_headers(1), timeout=TIMEOUT)

    assert response.status_code == 200
    payload = response.json()
    assert_keys(
        payload,
        ["user_id", "name", "email", "phone", "wallet_balance", "loyalty_points"],
    )
    assert payload["user_id"] == 1


def test_put_profile_with_existing_values_succeeds():
    current = requests.get(f"{BASE_URL}/profile", headers=request_headers(1), timeout=TIMEOUT)
    profile = current.json()

    response = requests.put(
        f"{BASE_URL}/profile",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"name": profile["name"], "phone": profile["phone"]},
        timeout=TIMEOUT,
    )

    assert response.status_code == 200
    payload = response.json()
    assert_keys(payload, ["user_id", "name", "phone"])
    assert payload["name"] == profile["name"]


def test_put_profile_with_short_name_returns_400():
    response = requests.put(
        f"{BASE_URL}/profile",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"name": "A", "phone": "9876543210"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    assert "error" in response.json()


def test_put_profile_with_invalid_phone_returns_400():
    response = requests.put(
        f"{BASE_URL}/profile",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"name": "Valid Name", "phone": "12345"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    assert "error" in response.json()
