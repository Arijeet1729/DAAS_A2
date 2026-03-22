import uuid

import requests

from .conftest import BASE_URL, TIMEOUT, assert_keys, request_headers


def test_get_reviews_returns_average_and_review_list():
    response = requests.get(
        f"{BASE_URL}/products/1/reviews",
        headers=request_headers(1),
        timeout=TIMEOUT,
    )

    assert response.status_code == 200
    payload = response.json()
    assert_keys(payload, ["average_rating", "reviews"])
    assert isinstance(payload["reviews"], list)


def test_post_review_creates_review_payload():
    response = requests.post(
        f"{BASE_URL}/products/1/reviews",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"rating": 5, "comment": f"pytest-review-{uuid.uuid4().hex[:8]}"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 201
    payload = response.json()
    assert_keys(payload, ["review_id", "user_id", "product_id", "rating", "comment"])
    assert payload["rating"] == 5


def test_post_review_with_invalid_rating_returns_400():
    response = requests.post(
        f"{BASE_URL}/products/1/reviews",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"rating": 0, "comment": "bad"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    assert "error" in response.json()


def test_get_reviews_for_missing_product_returns_404():
    response = requests.get(
        f"{BASE_URL}/products/999999/reviews",
        headers=request_headers(1),
        timeout=TIMEOUT,
    )

    assert response.status_code == 404
    assert "error" in response.json()
