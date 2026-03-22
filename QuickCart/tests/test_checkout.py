import requests

from .conftest import BASE_URL, TIMEOUT, assert_keys, clean_cart, request_headers


def test_checkout_with_card_returns_order_payload(clean_cart):
    requests.post(
        f"{BASE_URL}/cart/add",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"product_id": 1, "quantity": 2},
        timeout=TIMEOUT,
    )

    response = requests.post(
        f"{BASE_URL}/checkout",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"payment_method": "CARD"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 200
    payload = response.json()
    assert_keys(payload, ["gst_amount", "order_id", "order_status", "payment_status", "total_amount"])
    assert payload["payment_status"] == "PAID"


def test_checkout_with_empty_cart_returns_400(clean_cart):
    response = requests.post(
        f"{BASE_URL}/checkout",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"payment_method": "CARD"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    assert response.json()["error"] == "Cart is empty"


def test_checkout_with_invalid_payment_method_returns_400(clean_cart):
    response = requests.post(
        f"{BASE_URL}/checkout",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"payment_method": "UPI"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    assert "error" in response.json()


def test_checkout_with_cod_over_5000_returns_400(clean_cart):
    requests.post(
        f"{BASE_URL}/cart/add",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"product_id": 5, "quantity": 21},
        timeout=TIMEOUT,
    )

    response = requests.post(
        f"{BASE_URL}/checkout",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"payment_method": "COD"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    assert "error" in response.json()


def test_checkout_adds_gst_exactly_once(clean_cart):
    requests.post(
        f"{BASE_URL}/cart/add",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"product_id": 1, "quantity": 2},
        timeout=TIMEOUT,
    )

    response = requests.post(
        f"{BASE_URL}/checkout",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"payment_method": "CARD"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 200
    payload = response.json()
    expected_subtotal = 120 * 2
    expected_gst = round(expected_subtotal * 0.05, 2)
    expected_total = round(expected_subtotal + expected_gst, 2)
    assert payload["gst_amount"] == expected_gst
    assert payload["total_amount"] == expected_total
