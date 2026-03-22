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


def test_support_ticket_valid_status_flow_open_to_in_progress_to_closed(created_ticket):
    ticket_id = created_ticket["ticket_id"]

    in_progress_response = requests.put(
        f"{BASE_URL}/support/tickets/{ticket_id}",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"status": "IN_PROGRESS"},
        timeout=TIMEOUT,
    )
    assert in_progress_response.status_code == 200
    assert in_progress_response.json()["status"] == "IN_PROGRESS"

    closed_response = requests.put(
        f"{BASE_URL}/support/tickets/{ticket_id}",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"status": "CLOSED"},
        timeout=TIMEOUT,
    )
    assert closed_response.status_code == 200
    assert closed_response.json()["status"] == "CLOSED"


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


def test_support_ticket_message_is_stored_exactly():
    subject = "Exact message subject"
    message = "Need exact text: 123, punctuation, spaces."

    create_response = requests.post(
        f"{BASE_URL}/support/ticket",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"subject": subject, "message": message},
        timeout=TIMEOUT,
    )

    assert create_response.status_code in (200, 201)
    ticket_id = create_response.json()["ticket_id"]

    list_response = requests.get(f"{BASE_URL}/support/tickets", headers=request_headers(1), timeout=TIMEOUT)
    tickets = list_response.json()
    created = next(ticket for ticket in tickets if ticket["ticket_id"] == ticket_id)
    assert created["message"] == message


def test_support_ticket_subject_length_five_is_valid():
    response = requests.post(
        f"{BASE_URL}/support/ticket",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"subject": "ABCDE", "message": "Z"},
        timeout=TIMEOUT,
    )

    assert response.status_code in (200, 201)
    assert response.json()["subject"] == "ABCDE"
    assert response.json()["message"] == "Z"


def test_support_ticket_subject_length_one_hundred_and_message_length_five_hundred_are_valid():
    subject = "S" * 100
    message = "M" * 500

    response = requests.post(
        f"{BASE_URL}/support/ticket",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"subject": subject, "message": message},
        timeout=TIMEOUT,
    )

    assert response.status_code in (200, 201)
    payload = response.json()
    assert payload["subject"] == subject
    assert payload["message"] == message
