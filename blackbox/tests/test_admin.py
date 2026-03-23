import requests

from .conftest import BASE_URL, TIMEOUT, assert_keys


def test_admin_user_detail_with_valid_header_returns_200():
    response = requests.get(
        f"{BASE_URL}/admin/users/1",
        headers={"X-Roll-Number": "123"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert_keys(payload, ["user_id", "name", "email", "wallet_balance", "loyalty_points"])


def test_admin_user_detail_without_roll_number_returns_401():
    response = requests.get(f"{BASE_URL}/admin/users/1", timeout=TIMEOUT)

    assert response.status_code == 401
    assert "error" in response.json()


def test_admin_user_detail_with_invalid_id_returns_404():
    response = requests.get(
        f"{BASE_URL}/admin/users/999999",
        headers={"X-Roll-Number": "123"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 404
    assert "error" in response.json()


def test_admin_carts_with_valid_header_returns_200():
    response = requests.get(
        f"{BASE_URL}/admin/carts",
        headers={"X-Roll-Number": "123"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert payload
    assert_keys(payload[0], ["cart_id", "user_id", "items", "total"])


def test_admin_carts_without_roll_number_returns_401():
    response = requests.get(f"{BASE_URL}/admin/carts", timeout=TIMEOUT)

    assert response.status_code == 401
    assert "error" in response.json()


def test_admin_coupons_with_valid_header_returns_200():
    response = requests.get(
        f"{BASE_URL}/admin/coupons",
        headers={"X-Roll-Number": "123"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert payload
    assert_keys(
        payload[0],
        ["coupon_code", "discount_type", "discount_value", "min_cart_value", "max_discount", "expiry_date"],
    )


def test_admin_coupons_without_roll_number_returns_401():
    response = requests.get(f"{BASE_URL}/admin/coupons", timeout=TIMEOUT)

    assert response.status_code == 401
    assert "error" in response.json()


def test_admin_tickets_with_valid_header_returns_200():
    response = requests.get(
        f"{BASE_URL}/admin/tickets",
        headers={"X-Roll-Number": "123"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert payload
    assert_keys(payload[0], ["ticket_id", "user_id", "status", "subject", "message"])


def test_admin_tickets_without_roll_number_returns_401():
    response = requests.get(f"{BASE_URL}/admin/tickets", timeout=TIMEOUT)

    assert response.status_code == 401
    assert "error" in response.json()


def test_admin_addresses_with_valid_header_returns_200():
    response = requests.get(
        f"{BASE_URL}/admin/addresses",
        headers={"X-Roll-Number": "123"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert payload
    assert_keys(
        payload[0],
        ["address_id", "user_id", "label", "street", "city", "pincode", "is_default"],
    )


def test_admin_addresses_without_roll_number_returns_401():
    response = requests.get(f"{BASE_URL}/admin/addresses", timeout=TIMEOUT)

    assert response.status_code == 401
    assert "error" in response.json()
