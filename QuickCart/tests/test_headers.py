import pytest
import requests

from .conftest import BASE_URL, TIMEOUT, assert_keys, request_headers


ADMIN_ENDPOINTS = [
    "/admin/users",
    "/admin/products",
    "/admin/orders",
]

USER_ENDPOINTS = [
    "/profile",
    "/products",
    "/wallet",
]


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


@pytest.mark.parametrize("endpoint", ADMIN_ENDPOINTS + USER_ENDPOINTS)
def test_missing_roll_number_returns_401(endpoint):
    headers = {"X-User-ID": "1"} if endpoint in USER_ENDPOINTS else None

    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, timeout=TIMEOUT)

    assert response.status_code == 401
    assert "error" in response.json()


@pytest.mark.parametrize("endpoint", ADMIN_ENDPOINTS + USER_ENDPOINTS)
def test_invalid_roll_number_string_returns_400(endpoint):
    headers = {"X-Roll-Number": "abc"}
    if endpoint in USER_ENDPOINTS:
        headers["X-User-ID"] = "1"

    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, timeout=TIMEOUT)

    assert response.status_code == 400
    with pytest.raises(requests.HTTPError):
        response.raise_for_status()


@pytest.mark.parametrize("endpoint", USER_ENDPOINTS)
def test_missing_user_id_returns_400(endpoint):
    response = requests.get(
        f"{BASE_URL}{endpoint}",
        headers={"X-Roll-Number": "123"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    assert "error" in response.json()


@pytest.mark.parametrize("endpoint,user_id", [("/profile", "abc"), ("/products", "abc"), ("/wallet", "0")])
def test_invalid_user_id_returns_400(endpoint, user_id):
    response = requests.get(
        f"{BASE_URL}{endpoint}",
        headers=request_headers(user_id),
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    assert "error" in response.json()
