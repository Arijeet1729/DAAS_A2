Bug ID: BUG-001
Endpoint: POST /api/v1/addresses
Test Case: test_create_address_returns_created_address
Expected: A valid address request with label OTHER, street length above 5, city Pune, and a 6-digit pincode should succeed and return the created address object including address_id.
Actual: The API returned {"error":"Invalid pincode"} for the request body using pincode "400001".
Reason: The implementation appears to reject a documentation-valid 6-digit pincode, which violates the documented address creation contract.

Bug ID: BUG-002
Endpoint: PUT /api/v1/addresses/{address_id}
Test Case: test_update_address_with_forbidden_field_returns_400
Expected: Updating forbidden fields such as city should be rejected with 400 Bad Request because only street and is_default are allowed to change.
Actual: The API returned 200 OK when the request attempted to update {"city":"Delhi"}.
Reason: The implementation is allowing unsupported address-field updates instead of enforcing the documented update restrictions.

Bug ID: BUG-003
Endpoint: POST /api/v1/cart/add
Test Case: test_add_to_cart_with_zero_quantity_returns_400
Expected: Quantity 0 should be rejected with 400 Bad Request because quantity must be at least 1.
Actual: The API returned 200 OK for {"product_id":1,"quantity":0}.
Reason: The quantity lower-bound validation is missing or incorrectly implemented for cart addition.

Bug ID: BUG-004
Endpoint: PUT /api/v1/profile
Test Case: test_put_profile_with_existing_values_succeeds
Expected: A successful profile update should update and return the user's profile data structure, including fields such as user_id, name, and phone.
Actual: The API returned {"message":"Profile updated successfully"} without the updated profile object.
Reason: The implementation returns only a success message, which does not match the documented success response contract for profile updates.

Bug ID: BUG-005
Endpoint: POST /api/v1/products/{product_id}/reviews
Test Case: test_post_review_creates_review_payload
Expected: Creating a valid review should return a created-style response consistent with resource creation, and the test expected a 201 response with review details.
Actual: The API returned 200 OK instead of 201.
Reason: The implementation uses a success status that is inconsistent with the expected resource-creation behavior for review submission.

Bug ID: BUG-006
Endpoint: POST /api/v1/products/{product_id}/reviews
Test Case: test_post_review_with_invalid_rating_returns_400
Expected: A rating outside the 1 to 5 range, such as 0, should be rejected with 400 Bad Request.
Actual: The API returned 200 OK for {"rating":0,"comment":"bad"}.
Reason: The rating validation rule documented for reviews is not being enforced.

Bug ID: BUG-007
Endpoint: GET /api/v1/products/{product_id}/reviews
Test Case: test_get_reviews_for_missing_product_returns_404
Expected: Looking up reviews for a non-existent product should return 404 Not Found.
Actual: The API returned 200 OK for product_id 999999.
Reason: The implementation does not distinguish missing products correctly for the reviews endpoint and appears to return a successful response instead.

Bug ID: BUG-008
Endpoint: POST /api/v1/support/ticket
Test Case: test_create_support_ticket_returns_ticket_payload
Expected: Creating a support ticket should return a creation-style response, and the test expected 201 with the created ticket payload.
Actual: The API returned 200 OK with the ticket payload.
Reason: The implementation returns a different success status than expected for support-ticket creation, indicating a contract mismatch in create-endpoint behavior.

Additional Bugs From Extreme Edge And Correctness Testing

Bug ID: BUG-009
Endpoint: POST /api/v1/cart/add
Test Case: test_add_to_cart_with_negative_quantity_returns_400
Expected: A negative quantity such as -1 should be rejected with 400 Bad Request because quantity must be at least 1.
Actual: The API returned 200 OK for {"product_id":1,"quantity":-1}.
Reason: Negative cart quantities are being accepted, which indicates missing lower-bound validation in cart mutation logic.

Bug ID: BUG-010
Endpoint: GET /api/v1/cart
Test Case: test_cart_total_equals_sum_of_item_subtotals
Expected: The cart total should equal the sum of all item subtotals.
Actual: The API returned a cart with total 0 while the only item subtotal sum was -16.
Reason: The total calculation is inconsistent with the returned item subtotals, indicating broken cart total aggregation logic.

Bug ID: BUG-011
Endpoint: GET /api/v1/cart
Test Case: test_cart_item_subtotal_equals_quantity_times_unit_price
Expected: Each item subtotal should equal quantity multiplied by unit_price, so 2 items at unit price 120 should produce subtotal 240.
Actual: The API returned subtotal -16 for quantity 2 and unit_price 120.
Reason: The per-item subtotal calculation is incorrect and can lead to invalid cart mathematics downstream.

Bug ID: BUG-012
Endpoint: POST /api/v1/wallet/pay
Test Case: test_wallet_deduction_is_exact
Expected: Paying 7 after topping up 7 should bring the wallet balance back exactly to the original pre-top-up balance.
Actual: The final wallet balance was lower than the original balance by 0.20 instead of returning exactly to the starting value.
Reason: The wallet deduction logic is not subtracting the exact requested amount, violating the documented payment behavior.

Bug ID: BUG-013
Endpoint: POST /api/v1/checkout
Test Case: test_checkout_adds_gst_exactly_once
Expected: For a subtotal of 240, GST should be 12.0 and total_amount should be 252.0.
Actual: The API returned gst_amount 24.6 and total_amount 264.6.
Reason: GST is being calculated incorrectly, likely added more than once or on an incorrect base amount.

Bug ID: BUG-014
Endpoint: POST /api/v1/orders/{order_id}/cancel
Test Case: test_cancel_delivered_order_returns_400
Expected: Cancelling a delivered order should return 400 Bad Request promptly.
Actual: The request timed out and the API did not return the documented validation response.
Reason: The delivered-order cancel path appears unstable or blocked, which is more severe than simply returning the wrong status code.

Bug ID: BUG-015
Endpoint: GET /api/v1/products/{product_id}/reviews
Test Case: test_get_reviews_returns_average_and_review_list
Expected: The reviews endpoint should return 200 OK with average_rating and a reviews list.
Actual: During the test run, the request failed with a connection-aborted/server-disconnected error instead of returning a JSON response.
Reason: The reviews endpoint appears unstable under test execution, suggesting a server-side failure rather than a simple contract mismatch.

Bug ID: BUG-016
Endpoint: POST /api/v1/products/{product_id}/reviews
Test Case: test_post_review_with_rating_six_returns_400
Expected: A rating of 6 should be rejected with 400 Bad Request because rating must be between 1 and 5.
Actual: The API returned 200 OK for {"rating":6,"comment":"bad"}.
Reason: The upper-bound rating validation rule is not being enforced for review submission.
