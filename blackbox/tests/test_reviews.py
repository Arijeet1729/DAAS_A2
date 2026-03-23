import uuid

import pytest
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


def test_post_review_with_rating_six_returns_400():
    response = requests.post(
        f"{BASE_URL}/products/1/reviews",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"rating": 6, "comment": "bad"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    assert "error" in response.json()


def test_post_review_with_too_long_comment_returns_400():
    response = requests.post(
        f"{BASE_URL}/products/1/reviews",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"rating": 5, "comment": "x" * 201},
        timeout=TIMEOUT,
    )

    assert response.status_code == 400
    assert "error" in response.json()


def test_post_review_with_comment_length_one_is_valid():
    response = requests.post(
        f"{BASE_URL}/products/1/reviews",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"rating": 5, "comment": "a"},
        timeout=TIMEOUT,
    )

    assert response.status_code in (200, 201)
    payload = response.json()
    assert "review_id" in payload


def test_post_review_with_comment_length_two_hundred_is_valid():
    response = requests.post(
        f"{BASE_URL}/products/1/reviews",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"rating": 5, "comment": "x" * 200},
        timeout=TIMEOUT,
    )

    assert response.status_code in (200, 201)
    payload = response.json()
    assert "review_id" in payload


def test_no_reviews_returns_average_rating_zero():
    response = requests.get(
        f"{BASE_URL}/products/250/reviews",
        headers=request_headers(1),
        timeout=TIMEOUT,
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["average_rating"] == 0
    assert payload["reviews"] == []


def test_review_post_response_structure_contains_review_identifier():
    response = requests.post(
        f"{BASE_URL}/products/1/reviews",
        headers=request_headers(1, {"Content-Type": "application/json"}),
        json={"rating": 5, "comment": f"review-structure-{uuid.uuid4().hex[:8]}"},
        timeout=TIMEOUT,
    )

    assert response.status_code in (200, 201)
    payload = response.json()
    assert isinstance(payload, dict)
    assert "review_id" in payload


def test_average_rating_is_correct_decimal():
    response = requests.get(
        f"{BASE_URL}/products/1/reviews",
        headers=request_headers(1),
        timeout=TIMEOUT,
    )

    assert response.status_code == 200
    payload = response.json()
    ratings = [review["rating"] for review in payload["reviews"]]
    expected_average = sum(ratings) / len(ratings) if ratings else 0
    assert payload["average_rating"] == pytest.approx(expected_average)
