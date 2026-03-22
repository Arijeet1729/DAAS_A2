import requests

from .conftest import BASE_URL, TIMEOUT, assert_keys, created_ticket, request_headers


def test_create_support_ticket_returns_ticket_payload():
    response = requests.post(
        f"{BASE_URL}/support/ticket",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"subject": "Delay issue", "message": "Package has not arrived yet"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 201
    payload = response.json()
    assert_keys(payload, ["ticket_id", "subject", "message", "status"])
    assert payload["status"] == "OPEN"


def test_get_support_tickets_returns_list():
    response = requests.get(f"{BASE_URL}/support/tickets", headers=request_headers(1), timeout=TIMEOUT)

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)


def test_update_support_ticket_status_returns_updated_payload(created_ticket):
    ticket_id = created_ticket["ticket_id"]

    response = requests.put(
        f"{BASE_URL}/support/tickets/{ticket_id}",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"status": "IN_PROGRESS"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 200
    payload = response.json()
    assert_keys(payload, ["ticket_id", "status"])
    assert payload["status"] == "IN_PROGRESS"


def test_create_support_ticket_with_short_subject_returns_400():
    response = requests.post(
        f"{BASE_URL}/support/ticket",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"subject": "1234", "message": "Valid message"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    assert "error" in response.json()


def test_update_unknown_ticket_returns_404():
    response = requests.put(
        f"{BASE_URL}/support/tickets/999999",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"status": "IN_PROGRESS"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 404
    assert "error" in response.json()


def test_support_ticket_invalid_status_transition_returns_400(created_ticket):
    ticket_id = created_ticket["ticket_id"]

    response = requests.put(
        f"{BASE_URL}/support/tickets/{ticket_id}",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"status": "CLOSED"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    assert "error" in response.json()
