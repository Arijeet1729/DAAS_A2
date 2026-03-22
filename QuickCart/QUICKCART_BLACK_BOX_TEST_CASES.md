Test Case ID: ADM-001
Endpoint: GET /api/v1/admin/users
Type: Valid
Request:
  Method: GET
  URL: /api/v1/admin/users
  Headers: X-Roll-Number: 1
  Body: None
Expected Response: 200 OK, returns a non-empty list of users
Why this test is important: Verifies the primary admin listing endpoint works with the minimum required valid header.

Test Case ID: ADM-002
Endpoint: GET /api/v1/admin/users
Type: Valid
Request:
  Method: GET
  URL: /api/v1/admin/users
  Headers: X-Roll-Number: 99999
  Body: None
Expected Response: 200 OK, returns the full users list
Why this test is important: Confirms the roll number is treated as a valid integer contract field and not tied to a fixed known value.

Test Case ID: ADM-003
Endpoint: GET /api/v1/admin/users
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/admin/users
  Headers: None
  Body: None
Expected Response: 401 Unauthorized
Why this test is important: Verifies the required roll-number header is enforced.

Test Case ID: ADM-004
Endpoint: GET /api/v1/admin/users
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/admin/users
  Headers: X-Roll-Number: abc
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Checks wrong data type handling for the mandatory integer header.

Test Case ID: ADM-005
Endpoint: GET /api/v1/admin/users
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/admin/users
  Headers: X-Roll-Number: 1.5
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Ensures decimal values are rejected when an integer is required.

Test Case ID: ADM-006
Endpoint: GET /api/v1/admin/users
Type: Edge
Request:
  Method: GET
  URL: /api/v1/admin/users
  Headers: X-Roll-Number: 0
  Body: None
Expected Response: 200 OK if zero is accepted as an integer, otherwise 400 Bad Request
Why this test is important: Probes the lower integer boundary because the documentation requires a valid integer but does not explicitly rule out zero.

Test Case ID: ADM-007
Endpoint: GET /api/v1/admin/users/{user_id}
Type: Valid
Request:
  Method: GET
  URL: /api/v1/admin/users/1
  Headers: X-Roll-Number: 1
  Body: None
Expected Response: 200 OK, returns the user with user_id 1
Why this test is important: Verifies normal retrieval of one existing user.

Test Case ID: ADM-008
Endpoint: GET /api/v1/admin/users/{user_id}
Type: Valid
Request:
  Method: GET
  URL: /api/v1/admin/users/800
  Headers: X-Roll-Number: 1
  Body: None
Expected Response: 200 OK if user 800 exists
Why this test is important: Checks the endpoint with a high but likely valid identifier from seeded data.

Test Case ID: ADM-009
Endpoint: GET /api/v1/admin/users/{user_id}
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/admin/users/999999
  Headers: X-Roll-Number: 1
  Body: None
Expected Response: 404 Not Found or empty object/list depending on implementation
Why this test is important: Confirms behavior for a non-existent user identifier.

Test Case ID: ADM-010
Endpoint: GET /api/v1/admin/users/{user_id}
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/admin/users/abc
  Headers: X-Roll-Number: 1
  Body: None
Expected Response: 400 Bad Request or 404 route-level rejection
Why this test is important: Validates path-parameter type checking.

Test Case ID: ADM-011
Endpoint: GET /api/v1/admin/users/{user_id}
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/admin/users/1
  Headers: None
  Body: None
Expected Response: 401 Unauthorized
Why this test is important: Verifies that admin detail endpoints still require the roll-number header.

Test Case ID: ADM-012
Endpoint: GET /api/v1/admin/users/{user_id}
Type: Edge
Request:
  Method: GET
  URL: /api/v1/admin/users/0
  Headers: X-Roll-Number: 1
  Body: None
Expected Response: 404 Not Found or 400 Bad Request
Why this test is important: Exercises the lower boundary for a path ID that should usually be positive.

Test Case ID: ADM-013
Endpoint: GET /api/v1/admin/carts
Type: Valid
Request:
  Method: GET
  URL: /api/v1/admin/carts
  Headers: X-Roll-Number: 1
  Body: None
Expected Response: 200 OK, returns all carts
Why this test is important: Confirms the admin cart inspection endpoint is reachable.

Test Case ID: ADM-014
Endpoint: GET /api/v1/admin/carts
Type: Valid
Request:
  Method: GET
  URL: /api/v1/admin/carts
  Headers: X-Roll-Number: 42
  Body: None
Expected Response: 200 OK
Why this test is important: Verifies the endpoint accepts any valid integer roll number.

Test Case ID: ADM-015
Endpoint: GET /api/v1/admin/carts
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/admin/carts
  Headers: None
  Body: None
Expected Response: 401 Unauthorized
Why this test is important: Confirms missing-header validation.

Test Case ID: ADM-016
Endpoint: GET /api/v1/admin/carts
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/admin/carts
  Headers: X-Roll-Number: xyz
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Checks invalid roll-number format handling.

Test Case ID: ADM-017
Endpoint: GET /api/v1/admin/carts
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/admin/carts
  Headers: X-Roll-Number: @@@
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Verifies symbol-only header values are rejected.

Test Case ID: ADM-018
Endpoint: GET /api/v1/admin/carts
Type: Edge
Request:
  Method: GET
  URL: /api/v1/admin/carts
  Headers: X-Roll-Number: 2147483647
  Body: None
Expected Response: 200 OK or 400 Bad Request if integer parsing has limits
Why this test is important: Tests a very large integer boundary for the required header.

Test Case ID: ADM-019
Endpoint: GET /api/v1/admin/orders
Type: Valid
Request:
  Method: GET
  URL: /api/v1/admin/orders
  Headers: X-Roll-Number: 1
  Body: None
Expected Response: 200 OK, returns all orders
Why this test is important: Covers the main admin order inspection flow.

Test Case ID: ADM-020
Endpoint: GET /api/v1/admin/orders
Type: Valid
Request:
  Method: GET
  URL: /api/v1/admin/orders
  Headers: X-Roll-Number: 77
  Body: None
Expected Response: 200 OK
Why this test is important: Confirms any valid integer header works.

Test Case ID: ADM-021
Endpoint: GET /api/v1/admin/orders
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/admin/orders
  Headers: None
  Body: None
Expected Response: 401 Unauthorized
Why this test is important: Validates mandatory-header enforcement.

Test Case ID: ADM-022
Endpoint: GET /api/v1/admin/orders
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/admin/orders
  Headers: X-Roll-Number: one
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Validates header type checking.

Test Case ID: ADM-023
Endpoint: GET /api/v1/admin/orders
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/admin/orders
  Headers: X-Roll-Number: 1e3
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Ensures scientific notation is not accepted as an integer.

Test Case ID: ADM-024
Endpoint: GET /api/v1/admin/orders
Type: Edge
Request:
  Method: GET
  URL: /api/v1/admin/orders
  Headers: X-Roll-Number: -1
  Body: None
Expected Response: 200 OK if negative integers are accepted, otherwise 400 Bad Request
Why this test is important: Explores whether the implementation validates integer sign or only type.

Test Case ID: ADM-025
Endpoint: GET /api/v1/admin/products
Type: Valid
Request:
  Method: GET
  URL: /api/v1/admin/products
  Headers: X-Roll-Number: 1
  Body: None
Expected Response: 200 OK, returns all products including inactive ones
Why this test is important: Covers admin visibility into product inventory.

Test Case ID: ADM-026
Endpoint: GET /api/v1/admin/products
Type: Valid
Request:
  Method: GET
  URL: /api/v1/admin/products
  Headers: X-Roll-Number: 500
  Body: None
Expected Response: 200 OK
Why this test is important: Confirms normal behavior with another valid header value.

Test Case ID: ADM-027
Endpoint: GET /api/v1/admin/products
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/admin/products
  Headers: None
  Body: None
Expected Response: 401 Unauthorized
Why this test is important: Tests missing admin auth header.

Test Case ID: ADM-028
Endpoint: GET /api/v1/admin/products
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/admin/products
  Headers: X-Roll-Number: test
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Checks wrong-type header handling.

Test Case ID: ADM-029
Endpoint: GET /api/v1/admin/products
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/admin/products
  Headers: X-Roll-Number: ""
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Confirms blank header values are rejected.

Test Case ID: ADM-030
Endpoint: GET /api/v1/admin/products
Type: Edge
Request:
  Method: GET
  URL: /api/v1/admin/products
  Headers: X-Roll-Number: 0001
  Body: None
Expected Response: 200 OK if leading-zero integers are accepted
Why this test is important: Probes integer parsing edge behavior for header normalization.

Test Case ID: ADM-031
Endpoint: GET /api/v1/admin/coupons
Type: Valid
Request:
  Method: GET
  URL: /api/v1/admin/coupons
  Headers: X-Roll-Number: 1
  Body: None
Expected Response: 200 OK, returns all coupons including expired ones
Why this test is important: Covers coupon data inspection.

Test Case ID: ADM-032
Endpoint: GET /api/v1/admin/coupons
Type: Valid
Request:
  Method: GET
  URL: /api/v1/admin/coupons
  Headers: X-Roll-Number: 321
  Body: None
Expected Response: 200 OK
Why this test is important: Confirms generic valid-header behavior.

Test Case ID: ADM-033
Endpoint: GET /api/v1/admin/coupons
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/admin/coupons
  Headers: None
  Body: None
Expected Response: 401 Unauthorized
Why this test is important: Confirms required-header enforcement.

Test Case ID: ADM-034
Endpoint: GET /api/v1/admin/coupons
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/admin/coupons
  Headers: X-Roll-Number: false
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Tests boolean-like invalid string input.

Test Case ID: ADM-035
Endpoint: GET /api/v1/admin/coupons
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/admin/coupons
  Headers: X-Roll-Number: 12-34
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Ensures malformed numeric strings are rejected.

Test Case ID: ADM-036
Endpoint: GET /api/v1/admin/coupons
Type: Edge
Request:
  Method: GET
  URL: /api/v1/admin/coupons
  Headers: X-Roll-Number: 2147483648
  Body: None
Expected Response: 200 OK or 400 Bad Request based on integer-size handling
Why this test is important: Probes extremely large header values.

Test Case ID: ADM-037
Endpoint: GET /api/v1/admin/tickets
Type: Valid
Request:
  Method: GET
  URL: /api/v1/admin/tickets
  Headers: X-Roll-Number: 1
  Body: None
Expected Response: 200 OK, returns all support tickets
Why this test is important: Covers admin visibility into support data.

Test Case ID: ADM-038
Endpoint: GET /api/v1/admin/tickets
Type: Valid
Request:
  Method: GET
  URL: /api/v1/admin/tickets
  Headers: X-Roll-Number: 88
  Body: None
Expected Response: 200 OK
Why this test is important: Confirms consistent behavior across valid integer headers.

Test Case ID: ADM-039
Endpoint: GET /api/v1/admin/tickets
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/admin/tickets
  Headers: None
  Body: None
Expected Response: 401 Unauthorized
Why this test is important: Validates auth precondition.

Test Case ID: ADM-040
Endpoint: GET /api/v1/admin/tickets
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/admin/tickets
  Headers: X-Roll-Number: ticket
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Checks non-numeric header handling.

Test Case ID: ADM-041
Endpoint: GET /api/v1/admin/tickets
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/admin/tickets
  Headers: X-Roll-Number: [1]
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Ensures serialized array-like values are rejected.

Test Case ID: ADM-042
Endpoint: GET /api/v1/admin/tickets
Type: Edge
Request:
  Method: GET
  URL: /api/v1/admin/tickets
  Headers: X-Roll-Number: 000000
  Body: None
Expected Response: 200 OK or 400 Bad Request depending on normalization rules
Why this test is important: Exercises leading-zero and zero-boundary parsing together.

Test Case ID: ADM-043
Endpoint: GET /api/v1/admin/addresses
Type: Valid
Request:
  Method: GET
  URL: /api/v1/admin/addresses
  Headers: X-Roll-Number: 1
  Body: None
Expected Response: 200 OK, returns all addresses
Why this test is important: Covers the final admin inspection endpoint.

Test Case ID: ADM-044
Endpoint: GET /api/v1/admin/addresses
Type: Valid
Request:
  Method: GET
  URL: /api/v1/admin/addresses
  Headers: X-Roll-Number: 333
  Body: None
Expected Response: 200 OK
Why this test is important: Confirms valid integer header acceptance.

Test Case ID: ADM-045
Endpoint: GET /api/v1/admin/addresses
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/admin/addresses
  Headers: None
  Body: None
Expected Response: 401 Unauthorized
Why this test is important: Ensures header enforcement remains consistent.

Test Case ID: ADM-046
Endpoint: GET /api/v1/admin/addresses
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/admin/addresses
  Headers: X-Roll-Number: null
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Tests literal keyword misuse in the integer header.

Test Case ID: ADM-047
Endpoint: GET /api/v1/admin/addresses
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/admin/addresses
  Headers: X-Roll-Number: 1,2
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Ensures comma-separated header values are not accepted as integers.

Test Case ID: ADM-048
Endpoint: GET /api/v1/admin/addresses
Type: Edge
Request:
  Method: GET
  URL: /api/v1/admin/addresses
  Headers: X-Roll-Number: 2147483646
  Body: None
Expected Response: 200 OK or 400 Bad Request
Why this test is important: Covers another high-boundary integer value.

Test Case ID: PRF-001
Endpoint: GET /api/v1/profile
Type: Valid
Request:
  Method: GET
  URL: /api/v1/profile
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 200 OK, returns profile for user 1
Why this test is important: Verifies the normal user-profile read flow.

Test Case ID: PRF-002
Endpoint: GET /api/v1/profile
Type: Valid
Request:
  Method: GET
  URL: /api/v1/profile
  Headers: X-Roll-Number: 2, X-User-ID: 2
  Body: None
Expected Response: 200 OK, returns profile for user 2
Why this test is important: Confirms the endpoint works for multiple valid users.

Test Case ID: PRF-003
Endpoint: GET /api/v1/profile
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/profile
  Headers: X-User-ID: 1
  Body: None
Expected Response: 401 Unauthorized
Why this test is important: Verifies X-Roll-Number is still mandatory on user endpoints.

Test Case ID: PRF-004
Endpoint: GET /api/v1/profile
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/profile
  Headers: X-Roll-Number: 1
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Confirms X-User-ID is mandatory on user-scoped endpoints.

Test Case ID: PRF-005
Endpoint: GET /api/v1/profile
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/profile
  Headers: X-Roll-Number: 1, X-User-ID: abc
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Checks data-type validation for X-User-ID.

Test Case ID: PRF-006
Endpoint: GET /api/v1/profile
Type: Edge
Request:
  Method: GET
  URL: /api/v1/profile
  Headers: X-Roll-Number: 1, X-User-ID: 0
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Tests the positive-integer lower boundary for X-User-ID.

Test Case ID: PRF-007
Endpoint: PUT /api/v1/profile
Type: Valid
Request:
  Method: PUT
  URL: /api/v1/profile
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"name":"Amit Kumar","phone":"9876543210"}
Expected Response: 200 OK, profile updated successfully
Why this test is important: Covers a typical valid profile update.

Test Case ID: PRF-008
Endpoint: PUT /api/v1/profile
Type: Valid
Request:
  Method: PUT
  URL: /api/v1/profile
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"name":"Al","phone":"1234567890"}
Expected Response: 200 OK
Why this test is important: Validates the minimum documented name length boundary with a valid phone number.

Test Case ID: PRF-009
Endpoint: PUT /api/v1/profile
Type: Invalid
Request:
  Method: PUT
  URL: /api/v1/profile
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"name":"A","phone":"9876543210"}
Expected Response: 400 Bad Request
Why this test is important: Verifies rejection below the name minimum boundary.

Test Case ID: PRF-010
Endpoint: PUT /api/v1/profile
Type: Invalid
Request:
  Method: PUT
  URL: /api/v1/profile
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"name":"Valid Name","phone":"12345"}
Expected Response: 400 Bad Request
Why this test is important: Confirms short phone numbers are rejected.

Test Case ID: PRF-011
Endpoint: PUT /api/v1/profile
Type: Invalid
Request:
  Method: PUT
  URL: /api/v1/profile
  Headers: X-Roll-Number: abc, X-User-ID: 1, Content-Type: application/json
  Body: {"name":"Valid Name","phone":"9876543210"}
Expected Response: 400 Bad Request
Why this test is important: Separates header validation from body validation.

Test Case ID: PRF-012
Endpoint: PUT /api/v1/profile
Type: Edge
Request:
  Method: PUT
  URL: /api/v1/profile
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"name":"NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN","phone":"9999999999"}
Expected Response: 200 OK if the name is exactly 50 characters
Why this test is important: Checks the documented upper valid boundary for the name field.

Test Case ID: ADR-001
Endpoint: GET /api/v1/addresses
Type: Valid
Request:
  Method: GET
  URL: /api/v1/addresses
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 200 OK, returns the user's addresses
Why this test is important: Covers normal address retrieval.

Test Case ID: ADR-002
Endpoint: GET /api/v1/addresses
Type: Valid
Request:
  Method: GET
  URL: /api/v1/addresses
  Headers: X-Roll-Number: 1, X-User-ID: 2
  Body: None
Expected Response: 200 OK, returns addresses for user 2
Why this test is important: Confirms the endpoint works across different valid users.

Test Case ID: ADR-003
Endpoint: GET /api/v1/addresses
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/addresses
  Headers: X-Roll-Number: 1
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Verifies missing X-User-ID handling.

Test Case ID: ADR-004
Endpoint: GET /api/v1/addresses
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/addresses
  Headers: X-User-ID: 1
  Body: None
Expected Response: 401 Unauthorized
Why this test is important: Verifies missing X-Roll-Number handling.

Test Case ID: ADR-005
Endpoint: GET /api/v1/addresses
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/addresses
  Headers: X-Roll-Number: 1, X-User-ID: -2
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Confirms the positive-user-ID rule is enforced.

Test Case ID: ADR-006
Endpoint: GET /api/v1/addresses
Type: Edge
Request:
  Method: GET
  URL: /api/v1/addresses
  Headers: X-Roll-Number: 1, X-User-ID: 999999
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Exercises a large non-existent user ID.

Test Case ID: ADR-007
Endpoint: POST /api/v1/addresses
Type: Valid
Request:
  Method: POST
  URL: /api/v1/addresses
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"label":"HOME","street":"12 Park Street","city":"Hyderabad","pincode":"500001","is_default":true}
Expected Response: 200 OK or 201 Created, returns the created address object
Why this test is important: Covers the main address-creation flow with a default address.

Test Case ID: ADR-008
Endpoint: POST /api/v1/addresses
Type: Valid
Request:
  Method: POST
  URL: /api/v1/addresses
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"label":"OTHER","street":"12345","city":"Go","pincode":"400001","is_default":false}
Expected Response: 200 OK or 201 Created
Why this test is important: Uses the minimum valid boundaries for street and city.

Test Case ID: ADR-009
Endpoint: POST /api/v1/addresses
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/addresses
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"label":"HOUSE","street":"12 Park Street","city":"Hyderabad","pincode":"500001"}
Expected Response: 400 Bad Request
Why this test is important: Checks strict enum validation for label.

Test Case ID: ADR-010
Endpoint: POST /api/v1/addresses
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/addresses
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"label":"HOME","street":"1234","city":"Hyderabad","pincode":"500001"}
Expected Response: 400 Bad Request
Why this test is important: Verifies street minimum-length enforcement.

Test Case ID: ADR-011
Endpoint: POST /api/v1/addresses
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/addresses
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"label":"HOME","street":"12 Park Street","city":"H","pincode":"50A001"}
Expected Response: 400 Bad Request
Why this test is important: Combines invalid city length and invalid pincode data type content.

Test Case ID: ADR-012
Endpoint: POST /api/v1/addresses
Type: Edge
Request:
  Method: POST
  URL: /api/v1/addresses
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"label":"OFFICE","street":"SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS","city":"CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC","pincode":"999999"}
Expected Response: 200 OK or 201 Created if street is exactly 100 chars and city is exactly 50 chars
Why this test is important: Verifies documented upper-length boundaries for address fields.

Test Case ID: ADR-013
Endpoint: PUT /api/v1/addresses/{address_id}
Type: Valid
Request:
  Method: PUT
  URL: /api/v1/addresses/1
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"street":"99 New Main Road","is_default":false}
Expected Response: 200 OK, returns updated address data
Why this test is important: Covers the normal allowed update path.

Test Case ID: ADR-014
Endpoint: PUT /api/v1/addresses/{address_id}
Type: Valid
Request:
  Method: PUT
  URL: /api/v1/addresses/1
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"is_default":true}
Expected Response: 200 OK
Why this test is important: Verifies isolated default-flag updates.

Test Case ID: ADR-015
Endpoint: PUT /api/v1/addresses/{address_id}
Type: Invalid
Request:
  Method: PUT
  URL: /api/v1/addresses/1
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"label":"HOME"}
Expected Response: 400 Bad Request
Why this test is important: Confirms forbidden fields cannot be changed.

Test Case ID: ADR-016
Endpoint: PUT /api/v1/addresses/{address_id}
Type: Invalid
Request:
  Method: PUT
  URL: /api/v1/addresses/1
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"city":"Delhi"}
Expected Response: 400 Bad Request
Why this test is important: Confirms city updates are blocked by contract.

Test Case ID: ADR-017
Endpoint: PUT /api/v1/addresses/{address_id}
Type: Invalid
Request:
  Method: PUT
  URL: /api/v1/addresses/999999
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"street":"99 New Main Road"}
Expected Response: 404 Not Found or 400 Bad Request
Why this test is important: Tests updating a non-existent resource.

Test Case ID: ADR-018
Endpoint: PUT /api/v1/addresses/{address_id}
Type: Edge
Request:
  Method: PUT
  URL: /api/v1/addresses/1
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"street":"12345"}
Expected Response: 200 OK if the street minimum is inclusive on update as well
Why this test is important: Verifies boundary consistency between create and update validation.

Test Case ID: ADR-019
Endpoint: DELETE /api/v1/addresses/{address_id}
Type: Valid
Request:
  Method: DELETE
  URL: /api/v1/addresses/1
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 200 OK, address deleted
Why this test is important: Covers a successful delete.

Test Case ID: ADR-020
Endpoint: DELETE /api/v1/addresses/{address_id}
Type: Valid
Request:
  Method: DELETE
  URL: /api/v1/addresses/2
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 200 OK if address 2 belongs to the user
Why this test is important: Confirms deletion works for multiple valid resources.

Test Case ID: ADR-021
Endpoint: DELETE /api/v1/addresses/{address_id}
Type: Invalid
Request:
  Method: DELETE
  URL: /api/v1/addresses/999999
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 404 Not Found
Why this test is important: Verifies not-found handling promised in the spec.

Test Case ID: ADR-022
Endpoint: DELETE /api/v1/addresses/{address_id}
Type: Invalid
Request:
  Method: DELETE
  URL: /api/v1/addresses/1
  Headers: X-Roll-Number: abc, X-User-ID: 1
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Separates header validation from address existence.

Test Case ID: ADR-023
Endpoint: DELETE /api/v1/addresses/{address_id}
Type: Invalid
Request:
  Method: DELETE
  URL: /api/v1/addresses/1
  Headers: X-Roll-Number: 1
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Verifies missing user header handling on deletes.

Test Case ID: ADR-024
Endpoint: DELETE /api/v1/addresses/{address_id}
Type: Edge
Request:
  Method: DELETE
  URL: /api/v1/addresses/0
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 404 Not Found or 400 Bad Request
Why this test is important: Exercises lower path-ID boundary behavior.

Test Case ID: PRD-001
Endpoint: GET /api/v1/products
Type: Valid
Request:
  Method: GET
  URL: /api/v1/products
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 200 OK, returns active products only
Why this test is important: Covers the main product-browse endpoint.

Test Case ID: PRD-002
Endpoint: GET /api/v1/products
Type: Valid
Request:
  Method: GET
  URL: /api/v1/products?sort=asc
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 200 OK, returns a sorted active-product list
Why this test is important: Verifies documented sorting support.

Test Case ID: PRD-003
Endpoint: GET /api/v1/products
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/products
  Headers: X-Roll-Number: 1
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Confirms X-User-ID is mandatory even for browsing products.

Test Case ID: PRD-004
Endpoint: GET /api/v1/products
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/products
  Headers: X-Roll-Number: abc, X-User-ID: 1
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Tests invalid roll-number type.

Test Case ID: PRD-005
Endpoint: GET /api/v1/products
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/products
  Headers: X-Roll-Number: 1, X-User-ID: user1
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Tests invalid user-ID type.

Test Case ID: PRD-006
Endpoint: GET /api/v1/products
Type: Edge
Request:
  Method: GET
  URL: /api/v1/products?search=
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 200 OK, behaves like an unfiltered list or empty-search list
Why this test is important: Probes boundary behavior for optional search input.

Test Case ID: PRD-007
Endpoint: GET /api/v1/products/{product_id}
Type: Valid
Request:
  Method: GET
  URL: /api/v1/products/1
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 200 OK, returns product 1
Why this test is important: Covers valid single-product lookup.

Test Case ID: PRD-008
Endpoint: GET /api/v1/products/{product_id}
Type: Valid
Request:
  Method: GET
  URL: /api/v1/products/2
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 200 OK, returns product 2 if it exists
Why this test is important: Confirms multiple valid products can be fetched.

Test Case ID: PRD-009
Endpoint: GET /api/v1/products/{product_id}
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/products/999999
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 404 Not Found
Why this test is important: Verifies documented missing-product behavior.

Test Case ID: PRD-010
Endpoint: GET /api/v1/products/{product_id}
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/products/abc
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 400 Bad Request or 404 route-level rejection
Why this test is important: Tests path-parameter type handling.

Test Case ID: PRD-011
Endpoint: GET /api/v1/products/{product_id}
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/products/1
  Headers: X-Roll-Number: 1
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Ensures required user-scoping header remains enforced.

Test Case ID: PRD-012
Endpoint: GET /api/v1/products/{product_id}
Type: Edge
Request:
  Method: GET
  URL: /api/v1/products/0
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 404 Not Found or 400 Bad Request
Why this test is important: Exercises lower path-ID boundary behavior.

Test Case ID: CRT-001
Endpoint: GET /api/v1/cart
Type: Valid
Request:
  Method: GET
  URL: /api/v1/cart
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 200 OK, returns the user's cart with totals
Why this test is important: Covers the basic cart read path.

Test Case ID: CRT-002
Endpoint: GET /api/v1/cart
Type: Valid
Request:
  Method: GET
  URL: /api/v1/cart
  Headers: X-Roll-Number: 1, X-User-ID: 2
  Body: None
Expected Response: 200 OK
Why this test is important: Confirms the endpoint works for multiple users.

Test Case ID: CRT-003
Endpoint: GET /api/v1/cart
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/cart
  Headers: X-User-ID: 1
  Body: None
Expected Response: 401 Unauthorized
Why this test is important: Verifies missing X-Roll-Number handling.

Test Case ID: CRT-004
Endpoint: GET /api/v1/cart
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/cart
  Headers: X-Roll-Number: 1
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Verifies missing X-User-ID handling.

Test Case ID: CRT-005
Endpoint: GET /api/v1/cart
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/cart
  Headers: X-Roll-Number: 1, X-User-ID: 0
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Tests the positive-boundary rule for X-User-ID.

Test Case ID: CRT-006
Endpoint: GET /api/v1/cart
Type: Edge
Request:
  Method: GET
  URL: /api/v1/cart
  Headers: X-Roll-Number: 1, X-User-ID: 999999
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Tests a large non-existent user value.

Test Case ID: CRT-007
Endpoint: POST /api/v1/cart/add
Type: Valid
Request:
  Method: POST
  URL: /api/v1/cart/add
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"product_id":1,"quantity":1}
Expected Response: 200 OK or 201 Created, item added to cart
Why this test is important: Covers the standard add-to-cart path.

Test Case ID: CRT-008
Endpoint: POST /api/v1/cart/add
Type: Valid
Request:
  Method: POST
  URL: /api/v1/cart/add
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"product_id":1,"quantity":2}
Expected Response: 200 OK or 201 Created, quantity updated or combined
Why this test is important: Verifies duplicate adds increase quantity rather than replacing it.

Test Case ID: CRT-009
Endpoint: POST /api/v1/cart/add
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/cart/add
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"product_id":1,"quantity":0}
Expected Response: 400 Bad Request
Why this test is important: Checks the minimum quantity rule.

Test Case ID: CRT-010
Endpoint: POST /api/v1/cart/add
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/cart/add
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"product_id":1,"quantity":-5}
Expected Response: 400 Bad Request
Why this test is important: Verifies negative quantities are rejected.

Test Case ID: CRT-011
Endpoint: POST /api/v1/cart/add
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/cart/add
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"product_id":999999,"quantity":1}
Expected Response: 404 Not Found
Why this test is important: Tests behavior for non-existent products.

Test Case ID: CRT-012
Endpoint: POST /api/v1/cart/add
Type: Edge
Request:
  Method: POST
  URL: /api/v1/cart/add
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"product_id":1,"quantity":999999}
Expected Response: 400 Bad Request
Why this test is important: Exercises the stock upper boundary and overflow-risk path.

Test Case ID: CRT-013
Endpoint: POST /api/v1/cart/update
Type: Valid
Request:
  Method: POST
  URL: /api/v1/cart/update
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"product_id":1,"quantity":3}
Expected Response: 200 OK, quantity updated to 3
Why this test is important: Covers normal cart quantity updates.

Test Case ID: CRT-014
Endpoint: POST /api/v1/cart/update
Type: Valid
Request:
  Method: POST
  URL: /api/v1/cart/update
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"product_id":1,"quantity":1}
Expected Response: 200 OK
Why this test is important: Verifies the minimum valid quantity boundary.

Test Case ID: CRT-015
Endpoint: POST /api/v1/cart/update
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/cart/update
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"product_id":1,"quantity":0}
Expected Response: 400 Bad Request
Why this test is important: Confirms zero quantity is rejected.

Test Case ID: CRT-016
Endpoint: POST /api/v1/cart/update
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/cart/update
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"product_id":1,"quantity":"two"}
Expected Response: 400 Bad Request
Why this test is important: Tests data-type validation for quantity.

Test Case ID: CRT-017
Endpoint: POST /api/v1/cart/update
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/cart/update
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"product_id":999999,"quantity":1}
Expected Response: 404 Not Found or 400 Bad Request
Why this test is important: Verifies behavior when updating a non-existent cart item or product.

Test Case ID: CRT-018
Endpoint: POST /api/v1/cart/update
Type: Edge
Request:
  Method: POST
  URL: /api/v1/cart/update
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"product_id":1,"quantity":2147483647}
Expected Response: 400 Bad Request
Why this test is important: Probes extreme numeric boundaries and overflow-risk handling.

Test Case ID: CRT-019
Endpoint: POST /api/v1/cart/remove
Type: Valid
Request:
  Method: POST
  URL: /api/v1/cart/remove
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"product_id":1}
Expected Response: 200 OK, item removed from cart
Why this test is important: Covers the normal remove-item flow.

Test Case ID: CRT-020
Endpoint: POST /api/v1/cart/remove
Type: Valid
Request:
  Method: POST
  URL: /api/v1/cart/remove
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"product_id":2}
Expected Response: 200 OK if product 2 is present in the cart
Why this test is important: Confirms removal works across multiple possible items.

Test Case ID: CRT-021
Endpoint: POST /api/v1/cart/remove
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/cart/remove
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"product_id":999999}
Expected Response: 404 Not Found
Why this test is important: Verifies not-found behavior for missing cart items.

Test Case ID: CRT-022
Endpoint: POST /api/v1/cart/remove
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/cart/remove
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"product_id":"abc"}
Expected Response: 400 Bad Request
Why this test is important: Checks data-type validation for product IDs.

Test Case ID: CRT-023
Endpoint: POST /api/v1/cart/remove
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/cart/remove
  Headers: X-Roll-Number: 1, Content-Type: application/json
  Body: {"product_id":1}
Expected Response: 400 Bad Request
Why this test is important: Verifies user-scoping header is mandatory for cart mutation.

Test Case ID: CRT-024
Endpoint: POST /api/v1/cart/remove
Type: Edge
Request:
  Method: POST
  URL: /api/v1/cart/remove
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"product_id":0}
Expected Response: 404 Not Found or 400 Bad Request
Why this test is important: Exercises the lower path/body ID boundary.

Test Case ID: CRT-025
Endpoint: DELETE /api/v1/cart/clear
Type: Valid
Request:
  Method: DELETE
  URL: /api/v1/cart/clear
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 200 OK, cart cleared
Why this test is important: Covers the normal cart-clear flow.

Test Case ID: CRT-026
Endpoint: DELETE /api/v1/cart/clear
Type: Valid
Request:
  Method: DELETE
  URL: /api/v1/cart/clear
  Headers: X-Roll-Number: 1, X-User-ID: 2
  Body: None
Expected Response: 200 OK
Why this test is important: Confirms multiple valid users can clear their carts.

Test Case ID: CRT-027
Endpoint: DELETE /api/v1/cart/clear
Type: Invalid
Request:
  Method: DELETE
  URL: /api/v1/cart/clear
  Headers: X-User-ID: 1
  Body: None
Expected Response: 401 Unauthorized
Why this test is important: Verifies missing roll-number handling.

Test Case ID: CRT-028
Endpoint: DELETE /api/v1/cart/clear
Type: Invalid
Request:
  Method: DELETE
  URL: /api/v1/cart/clear
  Headers: X-Roll-Number: 1
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Verifies missing user-id handling.

Test Case ID: CRT-029
Endpoint: DELETE /api/v1/cart/clear
Type: Invalid
Request:
  Method: DELETE
  URL: /api/v1/cart/clear
  Headers: X-Roll-Number: 1, X-User-ID: abc
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Checks X-User-ID type validation.

Test Case ID: CRT-030
Endpoint: DELETE /api/v1/cart/clear
Type: Edge
Request:
  Method: DELETE
  URL: /api/v1/cart/clear
  Headers: X-Roll-Number: 1, X-User-ID: 999999
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Tests behavior with a non-existent but well-formed user ID.

Test Case ID: CPN-001
Endpoint: POST /api/v1/coupon/apply
Type: Valid
Request:
  Method: POST
  URL: /api/v1/coupon/apply
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"code":"SAVE10"}
Expected Response: 200 OK, coupon applied if valid and cart conditions are met
Why this test is important: Covers the core coupon-apply path with a plausible valid code.

Test Case ID: CPN-002
Endpoint: POST /api/v1/coupon/apply
Type: Valid
Request:
  Method: POST
  URL: /api/v1/coupon/apply
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"code":"FLAT100"}
Expected Response: 200 OK if the coupon exists and rules are satisfied
Why this test is important: Exercises a second likely coupon type and broadens valid coverage.

Test Case ID: CPN-003
Endpoint: POST /api/v1/coupon/apply
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/coupon/apply
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"code":"EXPIRED50"}
Expected Response: 400 Bad Request
Why this test is important: Verifies coupon expiry is enforced.

Test Case ID: CPN-004
Endpoint: POST /api/v1/coupon/apply
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/coupon/apply
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"code":12345}
Expected Response: 400 Bad Request
Why this test is important: Checks wrong data type for coupon code input.

Test Case ID: CPN-005
Endpoint: POST /api/v1/coupon/apply
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/coupon/apply
  Headers: X-Roll-Number: 1, Content-Type: application/json
  Body: {"code":"SAVE10"}
Expected Response: 400 Bad Request
Why this test is important: Verifies required user-scoping header is enforced.

Test Case ID: CPN-006
Endpoint: POST /api/v1/coupon/apply
Type: Edge
Request:
  Method: POST
  URL: /api/v1/coupon/apply
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"code":""}
Expected Response: 400 Bad Request
Why this test is important: Tests the empty-string boundary for coupon codes.

Test Case ID: CPN-007
Endpoint: POST /api/v1/coupon/remove
Type: Valid
Request:
  Method: POST
  URL: /api/v1/coupon/remove
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 200 OK, current coupon removed
Why this test is important: Covers the normal coupon removal path.

Test Case ID: CPN-008
Endpoint: POST /api/v1/coupon/remove
Type: Valid
Request:
  Method: POST
  URL: /api/v1/coupon/remove
  Headers: X-Roll-Number: 1, X-User-ID: 2
  Body: None
Expected Response: 200 OK
Why this test is important: Confirms the endpoint works for more than one valid user context.

Test Case ID: CPN-009
Endpoint: POST /api/v1/coupon/remove
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/coupon/remove
  Headers: X-User-ID: 1
  Body: None
Expected Response: 401 Unauthorized
Why this test is important: Checks missing roll-number behavior.

Test Case ID: CPN-010
Endpoint: POST /api/v1/coupon/remove
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/coupon/remove
  Headers: X-Roll-Number: 1
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Checks missing user-id behavior.

Test Case ID: CPN-011
Endpoint: POST /api/v1/coupon/remove
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/coupon/remove
  Headers: X-Roll-Number: x, X-User-ID: 1
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Checks invalid header type handling.

Test Case ID: CPN-012
Endpoint: POST /api/v1/coupon/remove
Type: Edge
Request:
  Method: POST
  URL: /api/v1/coupon/remove
  Headers: X-Roll-Number: 1, X-User-ID: 0
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Tests the lower boundary for X-User-ID.

Test Case ID: CHK-001
Endpoint: POST /api/v1/checkout
Type: Valid
Request:
  Method: POST
  URL: /api/v1/checkout
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"payment_method":"COD"}
Expected Response: 200 OK or 201 Created, order created with payment_status PENDING if total <= 5000
Why this test is important: Covers one documented valid payment path.

Test Case ID: CHK-002
Endpoint: POST /api/v1/checkout
Type: Valid
Request:
  Method: POST
  URL: /api/v1/checkout
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"payment_method":"CARD"}
Expected Response: 200 OK or 201 Created, order created with payment_status PAID
Why this test is important: Verifies the alternative payment-status branch.

Test Case ID: CHK-003
Endpoint: POST /api/v1/checkout
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/checkout
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"payment_method":"UPI"}
Expected Response: 400 Bad Request
Why this test is important: Confirms unsupported payment methods are rejected.

Test Case ID: CHK-004
Endpoint: POST /api/v1/checkout
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/checkout
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {}
Expected Response: 400 Bad Request
Why this test is important: Verifies required-body-field validation.

Test Case ID: CHK-005
Endpoint: POST /api/v1/checkout
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/checkout
  Headers: X-Roll-Number: 1, Content-Type: application/json
  Body: {"payment_method":"WALLET"}
Expected Response: 400 Bad Request
Why this test is important: Confirms X-User-ID is required for checkout.

Test Case ID: CHK-006
Endpoint: POST /api/v1/checkout
Type: Edge
Request:
  Method: POST
  URL: /api/v1/checkout
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"payment_method":"COD"}
Expected Response: 200 OK if the cart total is exactly 5000, otherwise behavior should still respect the documented COD limit
Why this test is important: Tests the documented COD monetary boundary.

Test Case ID: WAL-001
Endpoint: GET /api/v1/wallet
Type: Valid
Request:
  Method: GET
  URL: /api/v1/wallet
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 200 OK, returns wallet balance
Why this test is important: Covers normal wallet retrieval.

Test Case ID: WAL-002
Endpoint: GET /api/v1/wallet
Type: Valid
Request:
  Method: GET
  URL: /api/v1/wallet
  Headers: X-Roll-Number: 1, X-User-ID: 2
  Body: None
Expected Response: 200 OK
Why this test is important: Confirms the wallet endpoint works for multiple users.

Test Case ID: WAL-003
Endpoint: GET /api/v1/wallet
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/wallet
  Headers: X-Roll-Number: 1
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Verifies missing X-User-ID handling.

Test Case ID: WAL-004
Endpoint: GET /api/v1/wallet
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/wallet
  Headers: X-User-ID: 1
  Body: None
Expected Response: 401 Unauthorized
Why this test is important: Verifies missing X-Roll-Number handling.

Test Case ID: WAL-005
Endpoint: GET /api/v1/wallet
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/wallet
  Headers: X-Roll-Number: 1, X-User-ID: abc
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Checks bad data types in required headers.

Test Case ID: WAL-006
Endpoint: GET /api/v1/wallet
Type: Edge
Request:
  Method: GET
  URL: /api/v1/wallet
  Headers: X-Roll-Number: 1, X-User-ID: 0
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Exercises the lower positive bound for the user ID.

Test Case ID: WAL-007
Endpoint: POST /api/v1/wallet/add
Type: Valid
Request:
  Method: POST
  URL: /api/v1/wallet/add
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"amount":1}
Expected Response: 200 OK, wallet balance increases by 1
Why this test is important: Covers the minimum valid add-money amount.

Test Case ID: WAL-008
Endpoint: POST /api/v1/wallet/add
Type: Valid
Request:
  Method: POST
  URL: /api/v1/wallet/add
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"amount":100000}
Expected Response: 200 OK, wallet balance increases by 100000
Why this test is important: Covers the maximum documented valid add-money amount.

Test Case ID: WAL-009
Endpoint: POST /api/v1/wallet/add
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/wallet/add
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"amount":0}
Expected Response: 400 Bad Request
Why this test is important: Verifies the lower invalid boundary.

Test Case ID: WAL-010
Endpoint: POST /api/v1/wallet/add
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/wallet/add
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"amount":-10}
Expected Response: 400 Bad Request
Why this test is important: Confirms negative wallet additions are rejected.

Test Case ID: WAL-011
Endpoint: POST /api/v1/wallet/add
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/wallet/add
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"amount":"100"}
Expected Response: 400 Bad Request or implicit type error handling
Why this test is important: Checks wrong body data types.

Test Case ID: WAL-012
Endpoint: POST /api/v1/wallet/add
Type: Edge
Request:
  Method: POST
  URL: /api/v1/wallet/add
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"amount":100001}
Expected Response: 400 Bad Request
Why this test is important: Tests just beyond the documented upper valid boundary.

Test Case ID: WAL-013
Endpoint: POST /api/v1/wallet/pay
Type: Valid
Request:
  Method: POST
  URL: /api/v1/wallet/pay
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"amount":1}
Expected Response: 200 OK, exact amount deducted from balance
Why this test is important: Covers the minimum valid wallet payment path.

Test Case ID: WAL-014
Endpoint: POST /api/v1/wallet/pay
Type: Valid
Request:
  Method: POST
  URL: /api/v1/wallet/pay
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"amount":50}
Expected Response: 200 OK if balance is sufficient
Why this test is important: Covers a normal valid wallet payment.

Test Case ID: WAL-015
Endpoint: POST /api/v1/wallet/pay
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/wallet/pay
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"amount":0}
Expected Response: 400 Bad Request
Why this test is important: Verifies lower invalid boundary.

Test Case ID: WAL-016
Endpoint: POST /api/v1/wallet/pay
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/wallet/pay
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"amount":-5}
Expected Response: 400 Bad Request
Why this test is important: Confirms negative wallet payments are rejected.

Test Case ID: WAL-017
Endpoint: POST /api/v1/wallet/pay
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/wallet/pay
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"amount":999999}
Expected Response: 400 Bad Request
Why this test is important: Verifies insufficient-balance protection.

Test Case ID: WAL-018
Endpoint: POST /api/v1/wallet/pay
Type: Edge
Request:
  Method: POST
  URL: /api/v1/wallet/pay
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"amount":"0.01"}
Expected Response: 400 Bad Request
Why this test is important: Tests decimal/string ambiguity for an amount field expected to be numeric and valid.

Test Case ID: LOY-001
Endpoint: GET /api/v1/loyalty
Type: Valid
Request:
  Method: GET
  URL: /api/v1/loyalty
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 200 OK, returns loyalty points
Why this test is important: Covers normal loyalty retrieval.

Test Case ID: LOY-002
Endpoint: GET /api/v1/loyalty
Type: Valid
Request:
  Method: GET
  URL: /api/v1/loyalty
  Headers: X-Roll-Number: 1, X-User-ID: 2
  Body: None
Expected Response: 200 OK
Why this test is important: Confirms the endpoint works for different users.

Test Case ID: LOY-003
Endpoint: GET /api/v1/loyalty
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/loyalty
  Headers: X-Roll-Number: 1
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Verifies missing X-User-ID handling.

Test Case ID: LOY-004
Endpoint: GET /api/v1/loyalty
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/loyalty
  Headers: X-User-ID: 1
  Body: None
Expected Response: 401 Unauthorized
Why this test is important: Verifies missing X-Roll-Number handling.

Test Case ID: LOY-005
Endpoint: GET /api/v1/loyalty
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/loyalty
  Headers: X-Roll-Number: 1, X-User-ID: user
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Checks wrong data type for X-User-ID.

Test Case ID: LOY-006
Endpoint: GET /api/v1/loyalty
Type: Edge
Request:
  Method: GET
  URL: /api/v1/loyalty
  Headers: X-Roll-Number: 1, X-User-ID: 0
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Tests lower user-ID boundary enforcement.

Test Case ID: LOY-007
Endpoint: POST /api/v1/loyalty/redeem
Type: Valid
Request:
  Method: POST
  URL: /api/v1/loyalty/redeem
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"amount":1}
Expected Response: 200 OK, one unit redeemed if enough points exist
Why this test is important: Covers the minimum valid redemption amount.

Test Case ID: LOY-008
Endpoint: POST /api/v1/loyalty/redeem
Type: Valid
Request:
  Method: POST
  URL: /api/v1/loyalty/redeem
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"amount":50}
Expected Response: 200 OK if enough points exist
Why this test is important: Covers a typical valid redemption flow.

Test Case ID: LOY-009
Endpoint: POST /api/v1/loyalty/redeem
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/loyalty/redeem
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"amount":0}
Expected Response: 400 Bad Request
Why this test is important: Verifies the lower invalid boundary.

Test Case ID: LOY-010
Endpoint: POST /api/v1/loyalty/redeem
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/loyalty/redeem
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"amount":-1}
Expected Response: 400 Bad Request
Why this test is important: Confirms negative redemption requests are rejected.

Test Case ID: LOY-011
Endpoint: POST /api/v1/loyalty/redeem
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/loyalty/redeem
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"amount":999999}
Expected Response: 400 Bad Request
Why this test is important: Verifies insufficient-points validation.

Test Case ID: LOY-012
Endpoint: POST /api/v1/loyalty/redeem
Type: Edge
Request:
  Method: POST
  URL: /api/v1/loyalty/redeem
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"amount":"1"}
Expected Response: 400 Bad Request or type-validation failure
Why this test is important: Checks wrong data type for redemption amount.

Test Case ID: ORD-001
Endpoint: GET /api/v1/orders
Type: Valid
Request:
  Method: GET
  URL: /api/v1/orders
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 200 OK, returns the user's orders
Why this test is important: Covers normal order listing.

Test Case ID: ORD-002
Endpoint: GET /api/v1/orders
Type: Valid
Request:
  Method: GET
  URL: /api/v1/orders
  Headers: X-Roll-Number: 1, X-User-ID: 2
  Body: None
Expected Response: 200 OK
Why this test is important: Confirms the endpoint works for multiple users.

Test Case ID: ORD-003
Endpoint: GET /api/v1/orders
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/orders
  Headers: X-Roll-Number: 1
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Verifies missing X-User-ID handling.

Test Case ID: ORD-004
Endpoint: GET /api/v1/orders
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/orders
  Headers: X-User-ID: 1
  Body: None
Expected Response: 401 Unauthorized
Why this test is important: Verifies missing X-Roll-Number handling.

Test Case ID: ORD-005
Endpoint: GET /api/v1/orders
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/orders
  Headers: X-Roll-Number: 1, X-User-ID: -1
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Tests the positive-user-ID rule.

Test Case ID: ORD-006
Endpoint: GET /api/v1/orders
Type: Edge
Request:
  Method: GET
  URL: /api/v1/orders
  Headers: X-Roll-Number: 1, X-User-ID: 999999
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Probes non-existent but well-formed user IDs.

Test Case ID: ORD-007
Endpoint: GET /api/v1/orders/{order_id}
Type: Valid
Request:
  Method: GET
  URL: /api/v1/orders/1
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 200 OK if order 1 belongs to the user
Why this test is important: Covers valid order-detail lookup.

Test Case ID: ORD-008
Endpoint: GET /api/v1/orders/{order_id}
Type: Valid
Request:
  Method: GET
  URL: /api/v1/orders/2
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 200 OK if order 2 belongs to the user
Why this test is important: Expands valid coverage across multiple orders.

Test Case ID: ORD-009
Endpoint: GET /api/v1/orders/{order_id}
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/orders/999999
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 404 Not Found
Why this test is important: Verifies documented not-found behavior.

Test Case ID: ORD-010
Endpoint: GET /api/v1/orders/{order_id}
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/orders/abc
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 400 Bad Request or 404 route rejection
Why this test is important: Tests path-parameter type validation.

Test Case ID: ORD-011
Endpoint: GET /api/v1/orders/{order_id}
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/orders/1
  Headers: X-Roll-Number: 1
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Verifies required user scope remains enforced.

Test Case ID: ORD-012
Endpoint: GET /api/v1/orders/{order_id}
Type: Edge
Request:
  Method: GET
  URL: /api/v1/orders/0
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 404 Not Found or 400 Bad Request
Why this test is important: Exercises the lower order-ID boundary.

Test Case ID: ORD-013
Endpoint: POST /api/v1/orders/{order_id}/cancel
Type: Valid
Request:
  Method: POST
  URL: /api/v1/orders/1/cancel
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 200 OK if order 1 is cancellable
Why this test is important: Covers the successful cancel flow.

Test Case ID: ORD-014
Endpoint: POST /api/v1/orders/{order_id}/cancel
Type: Valid
Request:
  Method: POST
  URL: /api/v1/orders/2/cancel
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 200 OK if order 2 is cancellable
Why this test is important: Expands valid coverage to another possible order state.

Test Case ID: ORD-015
Endpoint: POST /api/v1/orders/{order_id}/cancel
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/orders/999999/cancel
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 404 Not Found
Why this test is important: Verifies behavior for a non-existent order.

Test Case ID: ORD-016
Endpoint: POST /api/v1/orders/{order_id}/cancel
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/orders/1/cancel
  Headers: X-Roll-Number: 1
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Confirms X-User-ID is required.

Test Case ID: ORD-017
Endpoint: POST /api/v1/orders/{order_id}/cancel
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/orders/1/cancel
  Headers: X-Roll-Number: abc, X-User-ID: 1
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Separates header validation from order-state logic.

Test Case ID: ORD-018
Endpoint: POST /api/v1/orders/{order_id}/cancel
Type: Edge
Request:
  Method: POST
  URL: /api/v1/orders/0/cancel
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 404 Not Found or 400 Bad Request
Why this test is important: Tests lower path-ID boundary handling for cancel.

Test Case ID: ORD-019
Endpoint: GET /api/v1/orders/{order_id}/invoice
Type: Valid
Request:
  Method: GET
  URL: /api/v1/orders/1/invoice
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 200 OK, returns invoice details
Why this test is important: Covers invoice generation/retrieval for an existing order.

Test Case ID: ORD-020
Endpoint: GET /api/v1/orders/{order_id}/invoice
Type: Valid
Request:
  Method: GET
  URL: /api/v1/orders/2/invoice
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 200 OK if order 2 exists and belongs to the user
Why this test is important: Extends valid coverage to another order.

Test Case ID: ORD-021
Endpoint: GET /api/v1/orders/{order_id}/invoice
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/orders/999999/invoice
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 404 Not Found
Why this test is important: Verifies not-found handling for invoice lookup.

Test Case ID: ORD-022
Endpoint: GET /api/v1/orders/{order_id}/invoice
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/orders/abc/invoice
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 400 Bad Request or 404 route rejection
Why this test is important: Exercises order-ID type validation.

Test Case ID: ORD-023
Endpoint: GET /api/v1/orders/{order_id}/invoice
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/orders/1/invoice
  Headers: X-Roll-Number: 1
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Confirms invoice access still needs X-User-ID.

Test Case ID: ORD-024
Endpoint: GET /api/v1/orders/{order_id}/invoice
Type: Edge
Request:
  Method: GET
  URL: /api/v1/orders/0/invoice
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 404 Not Found or 400 Bad Request
Why this test is important: Tests lower path-ID boundary handling.

Test Case ID: REV-001
Endpoint: GET /api/v1/products/{product_id}/reviews
Type: Valid
Request:
  Method: GET
  URL: /api/v1/products/1/reviews
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 200 OK, returns reviews and average rating
Why this test is important: Covers normal review retrieval.

Test Case ID: REV-002
Endpoint: GET /api/v1/products/{product_id}/reviews
Type: Valid
Request:
  Method: GET
  URL: /api/v1/products/2/reviews
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 200 OK if product 2 exists
Why this test is important: Broadens valid product review coverage.

Test Case ID: REV-003
Endpoint: GET /api/v1/products/{product_id}/reviews
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/products/999999/reviews
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 404 Not Found
Why this test is important: Verifies missing-product handling.

Test Case ID: REV-004
Endpoint: GET /api/v1/products/{product_id}/reviews
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/products/abc/reviews
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 400 Bad Request or 404 route rejection
Why this test is important: Tests path-parameter type validation.

Test Case ID: REV-005
Endpoint: GET /api/v1/products/{product_id}/reviews
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/products/1/reviews
  Headers: X-Roll-Number: 1
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Verifies required user context on review retrieval.

Test Case ID: REV-006
Endpoint: GET /api/v1/products/{product_id}/reviews
Type: Edge
Request:
  Method: GET
  URL: /api/v1/products/0/reviews
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 404 Not Found or 400 Bad Request
Why this test is important: Exercises the lower product-ID boundary.

Test Case ID: REV-007
Endpoint: POST /api/v1/products/{product_id}/reviews
Type: Valid
Request:
  Method: POST
  URL: /api/v1/products/1/reviews
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"rating":1,"comment":"a"}
Expected Response: 200 OK or 201 Created
Why this test is important: Covers the minimum valid rating and comment boundaries.

Test Case ID: REV-008
Endpoint: POST /api/v1/products/{product_id}/reviews
Type: Valid
Request:
  Method: POST
  URL: /api/v1/products/1/reviews
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"rating":5,"comment":"Excellent product and delivery"}
Expected Response: 200 OK or 201 Created
Why this test is important: Covers the maximum valid rating with a normal comment.

Test Case ID: REV-009
Endpoint: POST /api/v1/products/{product_id}/reviews
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/products/1/reviews
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"rating":0,"comment":"Too low"}
Expected Response: 400 Bad Request
Why this test is important: Verifies the lower invalid rating boundary.

Test Case ID: REV-010
Endpoint: POST /api/v1/products/{product_id}/reviews
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/products/1/reviews
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"rating":6,"comment":"Too high"}
Expected Response: 400 Bad Request
Why this test is important: Verifies the upper invalid rating boundary.

Test Case ID: REV-011
Endpoint: POST /api/v1/products/{product_id}/reviews
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/products/1/reviews
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"rating":"five","comment":""}
Expected Response: 400 Bad Request
Why this test is important: Simultaneously checks wrong data type and invalid comment length.

Test Case ID: REV-012
Endpoint: POST /api/v1/products/{product_id}/reviews
Type: Edge
Request:
  Method: POST
  URL: /api/v1/products/1/reviews
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"rating":5,"comment":"CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC"}
Expected Response: 200 OK or 201 Created if the comment is exactly 200 characters
Why this test is important: Verifies the documented upper comment-length boundary.

Test Case ID: SUP-001
Endpoint: POST /api/v1/support/ticket
Type: Valid
Request:
  Method: POST
  URL: /api/v1/support/ticket
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"subject":"Delay issue","message":"Package has not arrived yet"}
Expected Response: 200 OK or 201 Created, ticket created with status OPEN
Why this test is important: Covers normal support-ticket creation.

Test Case ID: SUP-002
Endpoint: POST /api/v1/support/ticket
Type: Valid
Request:
  Method: POST
  URL: /api/v1/support/ticket
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"subject":"12345","message":"M"}
Expected Response: 200 OK or 201 Created
Why this test is important: Covers the minimum valid subject and message boundaries.

Test Case ID: SUP-003
Endpoint: POST /api/v1/support/ticket
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/support/ticket
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"subject":"1234","message":"Valid message"}
Expected Response: 400 Bad Request
Why this test is important: Verifies subject minimum-length validation.

Test Case ID: SUP-004
Endpoint: POST /api/v1/support/ticket
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/support/ticket
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"subject":"Valid subject","message":""}
Expected Response: 400 Bad Request
Why this test is important: Verifies message minimum-length validation.

Test Case ID: SUP-005
Endpoint: POST /api/v1/support/ticket
Type: Invalid
Request:
  Method: POST
  URL: /api/v1/support/ticket
  Headers: X-Roll-Number: 1, X-User-ID: abc, Content-Type: application/json
  Body: {"subject":"Valid subject","message":"Valid message"}
Expected Response: 400 Bad Request
Why this test is important: Checks invalid X-User-ID type handling.

Test Case ID: SUP-006
Endpoint: POST /api/v1/support/ticket
Type: Edge
Request:
  Method: POST
  URL: /api/v1/support/ticket
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"subject":"SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS","message":"MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"}
Expected Response: 200 OK or 201 Created if subject is exactly 100 chars and message is exactly 500 chars
Why this test is important: Verifies upper valid boundaries and exact message preservation.

Test Case ID: SUP-007
Endpoint: GET /api/v1/support/tickets
Type: Valid
Request:
  Method: GET
  URL: /api/v1/support/tickets
  Headers: X-Roll-Number: 1, X-User-ID: 1
  Body: None
Expected Response: 200 OK, returns the user's tickets
Why this test is important: Covers normal support-ticket listing.

Test Case ID: SUP-008
Endpoint: GET /api/v1/support/tickets
Type: Valid
Request:
  Method: GET
  URL: /api/v1/support/tickets
  Headers: X-Roll-Number: 1, X-User-ID: 2
  Body: None
Expected Response: 200 OK
Why this test is important: Confirms the endpoint works for multiple users.

Test Case ID: SUP-009
Endpoint: GET /api/v1/support/tickets
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/support/tickets
  Headers: X-Roll-Number: 1
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Verifies missing X-User-ID handling.

Test Case ID: SUP-010
Endpoint: GET /api/v1/support/tickets
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/support/tickets
  Headers: X-User-ID: 1
  Body: None
Expected Response: 401 Unauthorized
Why this test is important: Verifies missing X-Roll-Number handling.

Test Case ID: SUP-011
Endpoint: GET /api/v1/support/tickets
Type: Invalid
Request:
  Method: GET
  URL: /api/v1/support/tickets
  Headers: X-Roll-Number: zzz, X-User-ID: 1
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Checks invalid roll-number type handling.

Test Case ID: SUP-012
Endpoint: GET /api/v1/support/tickets
Type: Edge
Request:
  Method: GET
  URL: /api/v1/support/tickets
  Headers: X-Roll-Number: 1, X-User-ID: 0
  Body: None
Expected Response: 400 Bad Request
Why this test is important: Exercises lower-bound user-ID validation.

Test Case ID: SUP-013
Endpoint: PUT /api/v1/support/tickets/{ticket_id}
Type: Valid
Request:
  Method: PUT
  URL: /api/v1/support/tickets/1
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"status":"IN_PROGRESS"}
Expected Response: 200 OK if the current status is OPEN
Why this test is important: Covers the first valid state transition.

Test Case ID: SUP-014
Endpoint: PUT /api/v1/support/tickets/{ticket_id}
Type: Valid
Request:
  Method: PUT
  URL: /api/v1/support/tickets/1
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"status":"CLOSED"}
Expected Response: 200 OK if the current status is IN_PROGRESS
Why this test is important: Covers the second valid state transition.

Test Case ID: SUP-015
Endpoint: PUT /api/v1/support/tickets/{ticket_id}
Type: Invalid
Request:
  Method: PUT
  URL: /api/v1/support/tickets/1
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"status":"OPEN"}
Expected Response: 400 Bad Request
Why this test is important: Verifies backward or repeated transitions are rejected.

Test Case ID: SUP-016
Endpoint: PUT /api/v1/support/tickets/{ticket_id}
Type: Invalid
Request:
  Method: PUT
  URL: /api/v1/support/tickets/999999
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"status":"IN_PROGRESS"}
Expected Response: 404 Not Found
Why this test is important: Verifies missing-ticket handling.

Test Case ID: SUP-017
Endpoint: PUT /api/v1/support/tickets/{ticket_id}
Type: Invalid
Request:
  Method: PUT
  URL: /api/v1/support/tickets/1
  Headers: X-Roll-Number: 1, Content-Type: application/json
  Body: {"status":"IN_PROGRESS"}
Expected Response: 400 Bad Request
Why this test is important: Confirms required user context remains enforced for updates.

Test Case ID: SUP-018
Endpoint: PUT /api/v1/support/tickets/{ticket_id}
Type: Edge
Request:
  Method: PUT
  URL: /api/v1/support/tickets/0
  Headers: X-Roll-Number: 1, X-User-ID: 1, Content-Type: application/json
  Body: {"status":"IN_PROGRESS"}
Expected Response: 404 Not Found or 400 Bad Request
Why this test is important: Exercises the lower ticket-ID boundary.
