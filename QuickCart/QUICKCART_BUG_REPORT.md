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
