import requests


BASE_URL = "http://localhost:8080"


def test_admin_users_with_valid_roll_number_returns_200():
    response = requests.get(
        f"{BASE_URL}/api/v1/admin/users",
        headers={"X-Roll-Number": "1"},
        timeout=10,
    )

    assert response.status_code == 200
