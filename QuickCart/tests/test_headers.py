import pytest
import requests

from .conftest import BASE_URL, TIMEOUT, assert_keys, request_headers


def test_admin_users_with_valid_roll_number_returns_200_and_list():
    response = requests.get(
        f"{BASE_URL}/admin/users",
        headers={"X-Roll-Number": "123"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert payload
    assert_keys(payload[0], ["user_id", "name", "email", "wallet_balance", "loyalty_points"])


def test_admin_users_without_roll_number_returns_401():
    response = requests.get(f"{BASE_URL}/admin/users", timeout=TIMEOUT)

    assert response.status_code == 401
    assert "error" in response.json()


def test_admin_users_with_invalid_roll_number_raises_http_error():
    response = requests.get(
        f"{BASE_URL}/admin/users",
        headers={"X-Roll-Number": "abc"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    with pytest.raises(requests.HTTPError):
        response.raise_for_status()


def test_profile_without_user_id_returns_400():
    response = requests.get(
        f"{BASE_URL}/profile",
        headers={"X-Roll-Number": "123"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    assert "error" in response.json()


def test_profile_with_zero_user_id_returns_400():
    response = requests.get(
        f"{BASE_URL}/profile",
        headers=request_headers(0),
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    assert "error" in response.json()
