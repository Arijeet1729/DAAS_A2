import requests

from .conftest import BASE_URL, TIMEOUT, assert_keys, created_address, request_headers


def test_get_addresses_returns_list_of_address_objects():
    response = requests.get(f"{BASE_URL}/addresses", headers=request_headers(1), timeout=TIMEOUT)

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert payload
    assert_keys(payload[0], ["address_id", "label", "street", "city", "pincode", "is_default"])


def test_create_address_returns_created_address(created_address):
    address = created_address.get("address", created_address)

    assert "address_id" in address
    assert address["label"] == "OTHER"
    assert address["city"] == "Pune"


def test_create_address_with_invalid_label_returns_400():
    response = requests.post(
        f"{BASE_URL}/addresses",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={
            "label": "HOUSE",
            "street": "12 Park Street",
            "city": "Hyderabad",
            "pincode": "500001",
        },
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    assert "error" in response.json()


def test_update_address_with_forbidden_field_returns_400():
    response = requests.put(
        f"{BASE_URL}/addresses/1",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"city": "Delhi"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    assert "error" in response.json()


def test_delete_unknown_address_returns_404():
    response = requests.delete(
        f"{BASE_URL}/addresses/999999",
        headers=request_headers(1),
        timeout=TIMEOUT,
    )

    assert response.status_code == 404
    assert "error" in response.json()
