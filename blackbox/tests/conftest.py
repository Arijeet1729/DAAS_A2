import uuid

import pytest
import requests


BASE_URL = "http://localhost:8080/api/v1"
TIMEOUT = 10


def get_headers(user_id=None):
    return {
        "X-Roll-Number": "123",
        "X-User-ID": str(user_id) if user_id else None,
    }


def request_headers(user_id=None, extra=None):
    headers = {k: v for k, v in get_headers(user_id).items() if v is not None}
    if extra:
        headers.update(extra)
    return headers


def assert_keys(data, keys):
    for key in keys:
        assert key in data


@pytest.fixture
def clean_cart():
    headers = request_headers(1)
    requests.delete(f"{BASE_URL}/cart/clear", headers=headers, timeout=TIMEOUT)
    yield
    requests.delete(f"{BASE_URL}/cart/clear", headers=headers, timeout=TIMEOUT)


@pytest.fixture
def created_address():
    response = requests.post(
        f"{BASE_URL}/addresses",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={
            "label": "OTHER",
            "street": f"QA Street {uuid.uuid4().hex[:8]}",
            "city": "Pune",
            "pincode": "400001",
            "is_default": False,
        },
        timeout=TIMEOUT,
    )
    data = response.json()
    yield data
    address = data.get("address", data)
    address_id = address.get("address_id") if isinstance(address, dict) else None
    if address_id:
        requests.delete(
            f"{BASE_URL}/addresses/{address_id}",
            headers=request_headers(1),
            timeout=TIMEOUT,
        )


@pytest.fixture
def created_ticket():
    response = requests.post(
        f"{BASE_URL}/support/ticket",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={
            "subject": f"Delay {uuid.uuid4().hex[:6]}",
            "message": "Package has not arrived yet",
        },
        timeout=TIMEOUT,
    )
    yield response.json()
