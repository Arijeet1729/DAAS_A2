import requests

from .conftest import BASE_URL, TIMEOUT, assert_keys, clean_cart, request_headers


def test_apply_coupon_returns_discount_payload(clean_cart):
    requests.post(
        f"{BASE_URL}/cart/add",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"product_id": 1, "quantity": 1},
        timeout=TIMEOUT,
    )

    response = requests.post(
        f"{BASE_URL}/coupon/apply",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"coupon_code": "WELCOME50"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 200
    payload = response.json()
    assert_keys(payload, ["coupon_code", "discount", "new_total"])
    assert payload["coupon_code"] == "WELCOME50"


def test_remove_coupon_returns_success_message(clean_cart):
    requests.post(
        f"{BASE_URL}/cart/add",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"product_id": 1, "quantity": 1},
        timeout=TIMEOUT,
    )
    requests.post(
        f"{BASE_URL}/coupon/apply",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"coupon_code": "WELCOME50"},
        timeout=TIMEOUT,
    )

    response = requests.post(f"{BASE_URL}/coupon/remove", headers=request_headers(1), timeout=TIMEOUT)

    assert response.status_code == 200
    assert response.json()["message"] == "Coupon removed successfully"


def test_apply_expired_coupon_returns_400(clean_cart):
    requests.post(
        f"{BASE_URL}/cart/add",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"product_id": 1, "quantity": 1},
        timeout=TIMEOUT,
    )

    response = requests.post(
        f"{BASE_URL}/coupon/apply",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"coupon_code": "EXPIRED50"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    assert "error" in response.json()


def test_apply_coupon_without_user_header_returns_400(clean_cart):
    response = requests.post(
        f"{BASE_URL}/coupon/apply",
        headers={"X-Roll-Number": "123", "Content-Type": "application/json"},
        json={"coupon_code": "WELCOME50"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    assert "error" in response.json()


def test_coupon_discount_respects_max_discount_cap(clean_cart):
    requests.post(
        f"{BASE_URL}/cart/add",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"product_id": 5, "quantity": 4},
        timeout=TIMEOUT,
    )

    response = requests.post(
        f"{BASE_URL}/coupon/apply",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"coupon_code": "PERCENT30"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["coupon_code"] == "PERCENT30"
    assert payload["discount"] == 300
    assert payload["new_total"] == 700
