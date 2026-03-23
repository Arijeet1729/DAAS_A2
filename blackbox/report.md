**QuickCart API**

**Comprehensive Black-Box Testing Report**

Testing Methodology: Black-Box / REST API

Server Environment: Docker --- http://localhost:8080/api/v1

Test Framework: pytest + requests (Python)

**Total Bugs Found: 16 (11 High \| 3 Medium \| 2 Low)**

**1. Introduction**

This document is the consolidated testing report for the QuickCart REST
API. It integrates the endpoint analysis, black-box test case design,
execution results, and all formal bug reports into a single reference
document.

The QuickCart API was tested as an external REST service running via
Docker at http://localhost:8080/api/v1. All testing was performed using
a black-box methodology --- no access to source code or internal
implementation was assumed. The test suite was built with pytest and the
requests library in Python.

**2. Testing Approach**

**2.1 Methodology**

Black-box testing was applied across all documented API endpoint groups.
The implementation was treated as an opaque system, and test
expectations were derived entirely from the API specification document.
The approach involved five sequential phases:

-   Endpoint Analysis --- all documented endpoints were catalogued into
    a structured map covering method, URL, headers, request body,
    success response, and error conditions.

-   Test Case Design --- test cases were designed per endpoint group,
    covering valid flows, invalid inputs, missing headers, boundary
    values, wrong data types, and state-based scenarios.

-   Automated Implementation --- test cases were implemented as pytest
    modules, one per functional area.

-   Execution --- tests were executed against the live Docker instance
    and results were collected.

-   Defect Logging --- all failures were logged as formal bug reports
    with reproduction steps, expected vs. actual behavior, and severity
    assessments.

**2.2 Test Focus Areas**

The following correctness dimensions were specifically targeted during
test design:

-   Header validation (X-Roll-Number, X-User-ID)

-   Valid request flows (happy paths)

-   Invalid request flows (wrong types, missing fields, constraint
    violations)

-   Boundary values (min/max lengths, quantity limits, price thresholds)

-   Computed value correctness (cart totals, GST, wallet balance,
    loyalty points, average ratings)

-   Response contract compliance (expected status codes, required fields
    in JSON responses)

-   Edge cases (zero quantities, negative values, non-existent
    resources, duplicate operations)

**2.3 Test Files**

The automated test suite was organized into the following pytest
modules:

test_headers.py, test_admin.py, test_profile.py, test_addresses.py,
test_products.py, test_cart.py, test_coupon.py, test_checkout.py,
test_wallet.py, test_loyalty.py, test_orders.py, test_reviews.py,
test_support.py

**3. Endpoint Coverage Summary**

All 12 documented API modules were exercised. The table below summarises
coverage and high-level execution status per module.

  ------------------------------------------------------------------------------
  **Module**      **Endpoints Covered**                **Test    **Status**
                                                       Cases**   
  --------------- ------------------------------------ --------- ---------------
  **Admin**       GET /api/v1/admin/users,             8         Pass
                  /admin/users/{id}, /admin/carts,               
                  /admin/orders, /admin/products,                
                  /admin/coupons, /admin/tickets,                
                  /admin/addresses                               

  **Profile**     GET & PUT /api/v1/profile            5         **1 Fail
                                                                 (BUG-004)**

  **Addresses**   GET, POST /api/v1/addresses; PUT &   8         **2 Fail
                  DELETE /api/v1/addresses/{id}                  (BUG-001,
                                                                 BUG-002)**

  **Products**    GET /api/v1/products; GET            4         Pass
                  /api/v1/products/{id}                          

  **Cart**        GET, POST add/update/remove, DELETE  12        **5 Fail
                  clear                                          (BUG-003, 009,
                                                                 010, 011)**

  **Coupons**     POST /api/v1/coupon/apply & remove   6         Pass

  **Checkout**    POST /api/v1/checkout                6         **1 Fail
                                                                 (BUG-013)**

  **Wallet**      GET /api/v1/wallet; POST add & pay   6         **1 Fail
                                                                 (BUG-012)**

  **Loyalty**     GET /api/v1/loyalty; POST redeem     5         Pass

  **Orders**      GET, GET/{id}, POST cancel, GET      8         **1 Fail
                  invoice                                        (BUG-014)**

  **Reviews**     GET & POST                           9         **5 Fail
                  /api/v1/products/{id}/reviews                  (BUG-005, 006,
                                                                 007, 015,
                                                                 016)**

  **Support**     POST ticket, GET tickets, PUT        7         **1 Fail
                  tickets/{id}                                   (BUG-008)**
  ------------------------------------------------------------------------------

Overall, broad endpoint coverage was achieved. Many success and error
conditions passed. Failures were concentrated in Cart, Reviews, and
Checkout modules.

**4. Bug Summary**

**4.1 Severity Breakdown**

  ------------------------------------------------------------------------
  **Severity**                 **Count**             **Bug IDs**
  ---------------------------- --------------------- ---------------------
  **High**                     **11**                001--003, 006,
                                                     009--016

  **Medium**                   **3**                 004, 007, 008
                                                     (partial)

  **Low**                      **2**                 005, 008

  **Total**                    **16**                BUG-001 -- BUG-016
  ------------------------------------------------------------------------

A total of 16 bugs were identified. The majority (11) are classified
High severity because they affect core functional correctness, including
financial calculations, cart mathematics, and input validation. Three
are Medium severity (response contract gaps, missing 404 handling). Two
are Low severity (HTTP status code convention differences on resource
creation endpoints).

**4.2 Bug Index**

The following table provides a one-line summary of all discovered bugs.

  ------------------------------------------------------------------------------------------------------------
  **Bug ID**    **Endpoint**                            **Summary**              **Severity**   **Category**
  ------------- --------------------------------------- ------------------------ -------------- --------------
  **BUG-001**   POST /api/v1/addresses                  Valid 6-digit pincode    **High**       Addresses
                                                        rejected as invalid                     

  **BUG-002**   PUT /api/v1/addresses/{address_id}      Forbidden address fields **High**       Addresses
                                                        accepted on update                      

  **BUG-003**   POST /api/v1/cart/add                   Zero quantity accepted   **High**       Cart
                                                        in cart addition                        

  **BUG-004**   PUT /api/v1/profile                     Profile update response  **Medium**     Profile
                                                        omits updated profile                   
                                                        object                                  

  **BUG-005**   POST                                    Review creation returns  **Low**        Reviews
                /api/v1/products/{product_id}/reviews   200 instead of 201                      

  **BUG-006**   POST                                    Rating value 0 accepted  **High**       Reviews
                /api/v1/products/{product_id}/reviews   --- lower bound not                     
                                                        enforced                                

  **BUG-007**   GET                                     Reviews endpoint returns **Medium**     Reviews
                /api/v1/products/{product_id}/reviews   200 for non-existent                    
                                                        product                                 

  **BUG-008**   POST /api/v1/support/ticket             Support ticket creation  **Low**        Support
                                                        returns 200 instead of                  
                                                        201                                     

  **BUG-009**   POST /api/v1/cart/add                   Negative quantity        **High**       Cart
                                                        accepted in cart                        
                                                        addition                                

  **BUG-010**   GET /api/v1/cart                        Cart total does not      **High**       Cart
                                                        match sum of item                       
                                                        subtotals                               

  **BUG-011**   GET /api/v1/cart                        Per-item subtotal        **High**       Cart
                                                        calculation is incorrect                

  **BUG-012**   POST /api/v1/wallet/pay                 Wallet deduction is not  **High**       Wallet
                                                        exact                                   

  **BUG-013**   POST /api/v1/checkout                   GST calculated           **High**       Checkout
                                                        incorrectly (likely                     
                                                        applied more than once)                 

  **BUG-014**   POST /api/v1/orders/{order_id}/cancel   Cancelling a delivered   **High**       Orders
                                                        order causes timeout                    
                                                        instead of returning 400                

  **BUG-015**   GET                                     Reviews endpoint crashes **High**       Reviews
                /api/v1/products/{product_id}/reviews   with connection-aborted                 
                                                        error                                   

  **BUG-016**   POST                                    Rating value 6 accepted  **High**       Reviews
                /api/v1/products/{product_id}/reviews   --- upper bound not                     
                                                        enforced                                
  ------------------------------------------------------------------------------------------------------------

**5. Detailed Bug Reports**

Each bug is documented below with full reproduction details including
endpoint, request, expected result, actual result, and business impact.

**BUG-001 --- Valid 6-digit pincode rejected as invalid**

  -------------- ----------------------------------------------------------
  **Bug ID**     BUG-001

  **Category**   Addresses

  **Endpoint**   POST /api/v1/addresses

  **Summary**    Valid 6-digit pincode rejected as invalid

  **Severity**   **High**

  **Expected**   Pincode \"400001\" is valid per spec (exactly 6 digits);
                 API should return the created address object including
                 address_id.

  **Actual**     API returns {\"error\":\"Invalid pincode\"} for a
                 documentation-compliant pincode.

  **Impact**     Users blocked from adding valid addresses, breaking
                 checkout and address management flows.
  -------------- ----------------------------------------------------------

**BUG-002 --- Forbidden address fields accepted on update**

  -------------- ----------------------------------------------------------
  **Bug ID**     BUG-002

  **Category**   Addresses

  **Endpoint**   PUT /api/v1/addresses/{address_id}

  **Summary**    Forbidden address fields accepted on update

  **Severity**   **High**

  **Expected**   Only street and is_default are allowed; updating city
                 should return 400 Bad Request.

  **Actual**     API returns 200 OK when body contains
                 {\"city\":\"Delhi\"}, silently accepting the forbidden
                 change.

  **Impact**     Violation of the update contract; allows unauthorized
                 mutations to immutable address fields.
  -------------- ----------------------------------------------------------

**BUG-003 --- Zero quantity accepted in cart addition**

  -------------- ----------------------------------------------------------
  **Bug ID**     BUG-003

  **Category**   Cart

  **Endpoint**   POST /api/v1/cart/add

  **Summary**    Zero quantity accepted in cart addition

  **Severity**   **High**

  **Expected**   Quantity 0 should be rejected with 400 Bad Request
                 (minimum is 1).

  **Actual**     API returns 200 OK for {\"product_id\":1,\"quantity\":0}.

  **Impact**     Invalid cart state can be created, corrupting totals and
                 downstream checkout behavior.
  -------------- ----------------------------------------------------------

**BUG-004 --- Profile update response omits updated profile object**

  -------------- ----------------------------------------------------------
  **Bug ID**     BUG-004

  **Category**   Profile

  **Endpoint**   PUT /api/v1/profile

  **Summary**    Profile update response omits updated profile object

  **Severity**   **Medium**

  **Expected**   Response should include the updated profile object
                 (user_id, name, phone, etc.).

  **Actual**     API returns only {\"message\":\"Profile updated
                 successfully\"} without profile data.

  **Impact**     Clients cannot confirm the final saved profile state from
                 the update response.
  -------------- ----------------------------------------------------------

**BUG-005 --- Review creation returns 200 instead of 201**

  -------------- ----------------------------------------------------------
  **Bug ID**     BUG-005

  **Category**   Reviews

  **Endpoint**   POST /api/v1/products/{product_id}/reviews

  **Summary**    Review creation returns 200 instead of 201

  **Severity**   **Low**

  **Expected**   Resource creation should return 201 Created with the
                 created review details.

  **Actual**     API returns 200 OK.

  **Impact**     Clients expecting standard REST creation semantics may
                 mishandle successful review creation.
  -------------- ----------------------------------------------------------

**BUG-006 --- Rating value 0 accepted --- lower bound not enforced**

  -------------- ----------------------------------------------------------
  **Bug ID**     BUG-006

  **Category**   Reviews

  **Endpoint**   POST /api/v1/products/{product_id}/reviews

  **Summary**    Rating value 0 accepted --- lower bound not enforced

  **Severity**   **High**

  **Expected**   Rating 0 should be rejected with 400 Bad Request (valid
                 range: 1--5).

  **Actual**     API returns 200 OK for {\"rating\":0,\"comment\":\"bad\"}.

  **Impact**     Invalid reviews stored; corrupts product rating
                 calculations and review quality.
  -------------- ----------------------------------------------------------

**BUG-007 --- Reviews endpoint returns 200 for non-existent product**

  -------------- ----------------------------------------------------------
  **Bug ID**     BUG-007

  **Category**   Reviews

  **Endpoint**   GET /api/v1/products/{product_id}/reviews

  **Summary**    Reviews endpoint returns 200 for non-existent product

  **Severity**   **Medium**

  **Expected**   Non-existent product ID (e.g., 999999) should return 404
                 Not Found.

  **Actual**     API returns 200 OK.

  **Impact**     Clients cannot distinguish a valid product with no reviews
                 from an invalid product ID.
  -------------- ----------------------------------------------------------

**BUG-008 --- Support ticket creation returns 200 instead of 201**

  -------------- ----------------------------------------------------------
  **Bug ID**     BUG-008

  **Category**   Support

  **Endpoint**   POST /api/v1/support/ticket

  **Summary**    Support ticket creation returns 200 instead of 201

  **Severity**   **Low**

  **Expected**   Resource creation should return 201 Created with the
                 ticket payload.

  **Actual**     API returns 200 OK with the ticket payload.

  **Impact**     Inconsistent REST semantics for create endpoints may
                 confuse clients.
  -------------- ----------------------------------------------------------

**BUG-009 --- Negative quantity accepted in cart addition**

  -------------- ----------------------------------------------------------
  **Bug ID**     BUG-009

  **Category**   Cart

  **Endpoint**   POST /api/v1/cart/add

  **Summary**    Negative quantity accepted in cart addition

  **Severity**   **High**

  **Expected**   Quantity -1 should be rejected with 400 Bad Request.

  **Actual**     API returns 200 OK for {\"product_id\":1,\"quantity\":-1}.

  **Impact**     Negative cart quantities accepted; breaks cart math and
                 downstream checkout.
  -------------- ----------------------------------------------------------

**BUG-010 --- Cart total does not match sum of item subtotals**

  -------------- ----------------------------------------------------------
  **Bug ID**     BUG-010

  **Category**   Cart

  **Endpoint**   GET /api/v1/cart

  **Summary**    Cart total does not match sum of item subtotals

  **Severity**   **High**

  **Expected**   Cart total should equal the sum of all item subtotals.

  **Actual**     Cart returned total 0 while the only item\'s subtotal was
                 -16.

  **Impact**     Broken cart total aggregation; checkout amounts are
                 untrustworthy.
  -------------- ----------------------------------------------------------

**BUG-011 --- Per-item subtotal calculation is incorrect**

  -------------- ----------------------------------------------------------
  **Bug ID**     BUG-011

  **Category**   Cart

  **Endpoint**   GET /api/v1/cart

  **Summary**    Per-item subtotal calculation is incorrect

  **Severity**   **High**

  **Expected**   2 units at unit_price 120 should give subtotal 240.

  **Actual**     API returned subtotal -16 for quantity 2, unit_price 120.

  **Impact**     Invalid cart arithmetic; all dependent calculations
                 (discounts, GST, total) are affected.
  -------------- ----------------------------------------------------------

**BUG-012 --- Wallet deduction is not exact**

  -------------- ----------------------------------------------------------
  **Bug ID**     BUG-012

  **Category**   Wallet

  **Endpoint**   POST /api/v1/wallet/pay

  **Summary**    Wallet deduction is not exact

  **Severity**   **High**

  **Expected**   Paying 7 after adding 7 should return the wallet to its
                 exact original balance.

  **Actual**     Final balance was lower by 0.20 compared to the pre-top-up
                 balance.

  **Impact**     Financial precision bug; small discrepancies accumulate
                 across transactions.
  -------------- ----------------------------------------------------------

**BUG-013 --- GST calculated incorrectly (likely applied more than
once)**

  -------------- ----------------------------------------------------------
  **Bug ID**     BUG-013

  **Category**   Checkout

  **Endpoint**   POST /api/v1/checkout

  **Summary**    GST calculated incorrectly (likely applied more than once)

  **Severity**   **High**

  **Expected**   For subtotal 240 with 5% GST: gst_amount = 12.0,
                 total_amount = 252.0.

  **Actual**     API returned gst_amount 24.6 and total_amount 264.6.

  **Impact**     Customers overcharged; order totals are incorrect across
                 all checkout flows.
  -------------- ----------------------------------------------------------

**BUG-014 --- Cancelling a delivered order causes timeout instead of
returning 400**

  -------------- ----------------------------------------------------------
  **Bug ID**     BUG-014

  **Category**   Orders

  **Endpoint**   POST /api/v1/orders/{order_id}/cancel

  **Summary**    Cancelling a delivered order causes timeout instead of
                 returning 400

  **Severity**   **High**

  **Expected**   Cancelling a delivered order should promptly return 400
                 Bad Request.

  **Actual**     Request timed out with no documented validation response.

  **Impact**     Endpoint is unstable on the delivered-order cancel path;
                 worse than a wrong status code.
  -------------- ----------------------------------------------------------

**BUG-015 --- Reviews endpoint crashes with connection-aborted error**

  -------------- ----------------------------------------------------------
  **Bug ID**     BUG-015

  **Category**   Reviews

  **Endpoint**   GET /api/v1/products/{product_id}/reviews

  **Summary**    Reviews endpoint crashes with connection-aborted error

  **Severity**   **High**

  **Expected**   200 OK with average_rating and reviews list.

  **Actual**     Request failed with connection-aborted /
                 server-disconnected error; no JSON response.

  **Impact**     Endpoint is server-side unstable; complete failure under
                 normal test execution.
  -------------- ----------------------------------------------------------

**BUG-016 --- Rating value 6 accepted --- upper bound not enforced**

  -------------- ----------------------------------------------------------
  **Bug ID**     BUG-016

  **Category**   Reviews

  **Endpoint**   POST /api/v1/products/{product_id}/reviews

  **Summary**    Rating value 6 accepted --- upper bound not enforced

  **Severity**   **High**

  **Expected**   Rating 6 should be rejected with 400 Bad Request (valid
                 range: 1--5).

  **Actual**     API returns 200 OK for {\"rating\":6,\"comment\":\"bad\"}.

  **Impact**     Invalid reviews can inflate product ratings; rating range
                 validation is completely absent.
  -------------- ----------------------------------------------------------

**6. Edge Case and Boundary Testing**

Special attention was given to boundary and stress conditions. The
following areas received targeted edge-case testing beyond standard
happy-path coverage.

**Cart**

-   Quantity 0 --- should reject with 400 (BUG-003: accepted with 200)

-   Negative quantity -1 --- should reject with 400 (BUG-009: accepted
    with 200)

-   Very large quantity exceeding stock

-   Duplicate product addition accumulation

-   Cart total equals sum of item subtotals (BUG-010: total was 0 while
    subtotals summed to -16)

-   Per-item subtotal equals quantity × unit_price (BUG-011: returned
    -16 for 2 × 120)

**Wallet**

-   Add amount 0 --- should reject

-   Add amount greater than 100,000 --- should reject

-   Exact deduction after payment (BUG-012: deduction off by 0.20)

**Checkout**

-   Empty cart checkout --- should reject

-   COD with order total above 5,000 --- should reject

-   Payment status correctness for COD, WALLET, and CARD

-   GST applied exactly once (BUG-013: GST overcharged for subtotal 240)

**Coupons**

-   Expired coupon --- should reject

-   Cart below minimum value --- should reject

-   FIXED coupon arithmetic correctness

-   PERCENT coupon arithmetic and cap enforcement

-   Coupon removal restores original total

**Orders**

-   Invalid order ID --- should return 404

-   Cancel delivered order --- should return 400 (BUG-014: request timed
    out)

-   Stock restoration after cancellation

-   Invoice arithmetic exact match (subtotal + GST = total)

**Reviews**

-   Rating 0 --- should reject with 400 (BUG-006: accepted with 200)

-   Rating 6 --- should reject with 400 (BUG-016: accepted with 200)

-   Comment length exactly 1 --- boundary minimum

-   Comment length exactly 200 --- boundary maximum

-   Comment longer than 200 --- should reject

-   No reviews returns average_rating 0

-   Average rating remains decimal-accurate

-   Connection-aborted error during test execution (BUG-015)

**Support**

-   Valid status transition OPEN → IN_PROGRESS → CLOSED

-   Invalid transition rejection

-   Message body stored exactly as submitted

-   Subject length boundary: exactly 5 characters and exactly 100
    characters

-   Message length boundary: exactly 1 character and exactly 500
    characters

**7. API Endpoint Reference**

The following table documents all analysed endpoints used as the basis
for test case design.

  ----------- ------------------------------- -------------------------------------
  **Admin**                                   

  **GET**     /api/v1/admin/users             Returns all users with wallet
                                              balances and loyalty points

  **GET**     /api/v1/admin/users/{user_id}   Returns one specific user

  **GET**     /api/v1/admin/carts             Returns every cart with items and
                                              computed totals

  **GET**     /api/v1/admin/orders            Returns all orders across all users

  **GET**     /api/v1/admin/products          Returns all products including
                                              inactive ones

  **GET**     /api/v1/admin/coupons           Returns all coupons including expired
                                              ones

  **GET**     /api/v1/admin/tickets           Returns all support tickets across
                                              all users

  **GET**     /api/v1/admin/addresses         Returns all addresses across all
                                              users
  ----------- ------------------------------- -------------------------------------

  ------------- -------------------------- -------------------------------------
  **Profile**                              

  **GET**       /api/v1/profile            Returns the user profile

  **PUT**       /api/v1/profile            Updates and returns the user profile
  ------------- -------------------------- -------------------------------------

  --------------- -------------------------------- -------------------------------------
  **Addresses**                                    

  **GET**         /api/v1/addresses                Returns all addresses for the user

  **POST**        /api/v1/addresses                Creates a new address

  **PUT**         /api/v1/addresses/{address_id}   Updates street or is_default only

  **DELETE**      /api/v1/addresses/{address_id}   Deletes the address
  --------------- -------------------------------- -------------------------------------

  -------------- ------------------------------- -------------------------------------
  **Products**                                   

  **GET**        /api/v1/products                Returns active products; supports
                                                 category, name, price filters

  **GET**        /api/v1/products/{product_id}   Returns one product by ID
  -------------- ------------------------------- -------------------------------------

  ------------ -------------------------- -------------------------------------
  **Cart**                                

  **GET**      /api/v1/cart               Returns cart with items, subtotals,
                                          and total

  **POST**     /api/v1/cart/add           Adds item or increases quantity

  **POST**     /api/v1/cart/update        Updates item quantity

  **POST**     /api/v1/cart/remove        Removes item from cart

  **DELETE**   /api/v1/cart/clear         Clears entire cart
  ------------ -------------------------- -------------------------------------

  ------------- -------------------------- -------------------------------------
  **Coupons**                              

  **POST**      /api/v1/coupon/apply       Applies coupon code to cart

  **POST**      /api/v1/coupon/remove      Removes currently applied coupon
  ------------- -------------------------- -------------------------------------

  -------------- -------------------------- -------------------------------------
  **Checkout**                              

  **POST**       /api/v1/checkout           Creates order with GST; accepts COD,
                                            WALLET, CARD
  -------------- -------------------------- -------------------------------------

  ------------ -------------------------- -------------------------------------
  **Wallet**                              

  **GET**      /api/v1/wallet             Returns current wallet balance

  **POST**     /api/v1/wallet/add         Adds money to wallet

  **POST**     /api/v1/wallet/pay         Deducts payment from wallet
  ------------ -------------------------- -------------------------------------

  ------------- -------------------------- -------------------------------------
  **Loyalty**                              

  **GET**       /api/v1/loyalty            Returns current loyalty points

  **POST**      /api/v1/loyalty/redeem     Redeems loyalty points
  ------------- -------------------------- -------------------------------------

  ------------ ----------------------------------- -------------------------------------
  **Orders**                                       

  **GET**      /api/v1/orders                      Returns all orders for the user

  **GET**      /api/v1/orders/{order_id}           Returns details for one order

  **POST**     /api/v1/orders/{order_id}/cancel    Cancels order and restores stock

  **GET**      /api/v1/orders/{order_id}/invoice   Returns invoice with GST breakdown
  ------------ ----------------------------------- -------------------------------------

  ------------- --------------------------------------- -------------------------------------
  **Reviews**                                           

  **GET**       /api/v1/products/{product_id}/reviews   Returns all reviews and average
                                                        rating

  **POST**      /api/v1/products/{product_id}/reviews   Creates a review (rating 1--5,
                                                        comment 1--200 chars)
  ------------- --------------------------------------- -------------------------------------

  ------------- ------------------------------------- -------------------------------------
  **Support**                                         

  **POST**      /api/v1/support/ticket                Creates support ticket with status
                                                      OPEN

  **GET**       /api/v1/support/tickets               Returns all support tickets for the
                                                      user

  **PUT**       /api/v1/support/tickets/{ticket_id}   Updates ticket status via allowed
                                                      transitions
  ------------- ------------------------------------- -------------------------------------

**8. Conclusion**

The QuickCart API black-box testing process achieved broad coverage
across all 12 documented endpoint modules and found 16 bugs ranging from
critical calculation errors to minor HTTP status code deviations.

**8.1 What Works**

-   Server is reachable and endpoint routing is functional.

-   Required headers (X-Roll-Number, X-User-ID) are correctly enforced
    in most places.

-   Several normal success flows are working correctly.

-   Many JSON response structures are stable and match the documented
    contract.

-   Admin endpoints are broadly functional for data retrieval.

-   Loyalty and coupon modules pass basic functional tests.

**8.2 What Needs Fixing**

-   Cart arithmetic is fundamentally broken --- subtotal and total
    calculations are incorrect (BUG-010, BUG-011).

-   GST is applied incorrectly at checkout, resulting in customer
    overcharge (BUG-013).

-   Wallet deductions are inexact, introducing financial precision
    errors (BUG-012).

-   Cart quantity validation is completely absent for zero and negative
    values (BUG-003, BUG-009).

-   Review rating validation is missing for both upper and lower bounds
    (BUG-006, BUG-016).

-   The reviews GET endpoint is server-unstable and crashes under normal
    test execution (BUG-015).

-   Address update permits forbidden field mutations (BUG-002) and
    rejects valid pincodes (BUG-001).

-   Cancelling a delivered order causes a server timeout rather than a
    clean validation error (BUG-014).

-   Profile update and review creation return incorrect response
    structures (BUG-004, BUG-005).

**8.3 Priority Recommendations**

The following bugs should be addressed first due to their high business
impact:

-   **BUG-010, BUG-011, BUG-013 --- Cart math and GST errors**
    (financial correctness at risk)

-   **BUG-012 --- Wallet deduction inexact** (financial precision)

-   **BUG-015, BUG-014 --- Server instability** (reliability risk)

-   **BUG-001, BUG-002, BUG-003, BUG-009 --- Input validation failures**
    (data integrity risk)

-   **BUG-006, BUG-016 --- Review rating validation absent** (data
    quality risk)

The testing process successfully validated working behavior and exposed
important implementation gaps. The final output is a structured,
reusable black-box testing package with formal defect documentation that
can guide remediation and regression testing.