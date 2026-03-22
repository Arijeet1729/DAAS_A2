Bug ID: BUG-001
Endpoint: POST /api/v1/addresses
Request:
  Method: POST
  URL: /api/v1/addresses
  Headers: X-Roll-Number: 123, X-User-ID: 1, Content-Type: application/json
  Body: {"label":"OTHER","street":"QA Street 12345678","city":"Pune","pincode":"400001","is_default":false}

Expected Result:
The API should accept the request because the pincode is a valid 6-digit value and return the created address object including address_id.
Actual Result:
The API returns {"error":"Invalid pincode"}.
Impact:
Users may be blocked from adding valid addresses, which breaks checkout preparation and address management flows.
Severity: High

Bug ID: BUG-002
Endpoint: PUT /api/v1/addresses/{address_id}
Request:
  Method: PUT
  URL: /api/v1/addresses/1
  Headers: X-Roll-Number: 123, X-User-ID: 1, Content-Type: application/json
  Body: {"city":"Delhi"}

Expected Result:
The API should reject the request with 400 Bad Request because only street and is_default are allowed to be updated.
Actual Result:
The API returns 200 OK and accepts the forbidden field update.
Impact:
The endpoint violates its update contract and allows unauthorized changes to immutable address fields.
Severity: High

Bug ID: BUG-003
Endpoint: POST /api/v1/cart/add
Request:
  Method: POST
  URL: /api/v1/cart/add
  Headers: X-Roll-Number: 123, X-User-ID: 1, Content-Type: application/json
  Body: {"product_id":1,"quantity":0}

Expected Result:
The API should reject the request with 400 Bad Request because quantity must be at least 1.
Actual Result:
The API returns 200 OK.
Impact:
Invalid cart state can be created, which can corrupt totals and downstream checkout behavior.
Severity: High

Bug ID: BUG-004
Endpoint: PUT /api/v1/profile
Request:
  Method: PUT
  URL: /api/v1/profile
  Headers: X-Roll-Number: 123, X-User-ID: 1, Content-Type: application/json
  Body: {"name":"Anita Johnson","phone":"8753591149"}

Expected Result:
The API should return the updated profile object, including fields such as user_id, name, and phone.
Actual Result:
The API returns {"message":"Profile updated successfully"} without the updated profile data.
Impact:
Clients cannot reliably confirm the final saved profile state from the update response.
Severity: Medium

Bug ID: BUG-005
Endpoint: POST /api/v1/products/{product_id}/reviews
Request:
  Method: POST
  URL: /api/v1/products/1/reviews
  Headers: X-Roll-Number: 123, X-User-ID: 1, Content-Type: application/json
  Body: {"rating":5,"comment":"pytest-review-sample"}

Expected Result:
The API should return a resource-creation style response with status 201 and the created review details.
Actual Result:
The API returns 200 OK.
Impact:
Clients expecting standard creation semantics may mis-handle successful review creation responses.
Severity: Low

Bug ID: BUG-006
Endpoint: POST /api/v1/products/{product_id}/reviews
Request:
  Method: POST
  URL: /api/v1/products/1/reviews
  Headers: X-Roll-Number: 123, X-User-ID: 1, Content-Type: application/json
  Body: {"rating":0,"comment":"bad"}

Expected Result:
The API should reject the request with 400 Bad Request because rating must be between 1 and 5.
Actual Result:
The API returns 200 OK.
Impact:
Invalid review data can be stored, which can corrupt product rating calculations and review quality.
Severity: High

Bug ID: BUG-007
Endpoint: GET /api/v1/products/{product_id}/reviews
Request:
  Method: GET
  URL: /api/v1/products/999999/reviews
  Headers: X-Roll-Number: 123, X-User-ID: 1
  Body: None

Expected Result:
The API should return 404 Not Found because the product does not exist.
Actual Result:
The API returns 200 OK.
Impact:
Clients cannot distinguish between a valid product with no reviews and an invalid product identifier.
Severity: Medium

Bug ID: BUG-008
Endpoint: POST /api/v1/support/ticket
Request:
  Method: POST
  URL: /api/v1/support/ticket
  Headers: X-Roll-Number: 123, X-User-ID: 1, Content-Type: application/json
  Body: {"subject":"Delay issue","message":"Package has not arrived yet"}

Expected Result:
The API should return a resource-creation style response with status 201 and the created ticket payload.
Actual Result:
The API returns 200 OK with the ticket payload.
Impact:
Clients relying on standard create semantics may not interpret support-ticket creation consistently.
Severity: Low
