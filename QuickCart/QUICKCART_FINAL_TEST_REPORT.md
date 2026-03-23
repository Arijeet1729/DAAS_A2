# QuickCart API Final Testing Report

## 1. Testing Approach

The QuickCart API was tested using black-box testing. The system was treated as an external REST API running through Docker on `http://localhost:8080/api/v1`. Testing was performed using `pytest` and `requests`, with each API area placed in its own test file for clarity.

The work started by studying the API specification in [`QuickCart System.md`](./QuickCart%20System.md). Based on that specification, a structured endpoint map was prepared in [`QUICKCART_API_ENDPOINT_ANALYSIS.md`](./QUICKCART_API_ENDPOINT_ANALYSIS.md). After that, black-box test cases were designed in [`QUICKCART_BLACK_BOX_TEST_CASES.md`](./QUICKCART_BLACK_BOX_TEST_CASES.md), and those cases were gradually converted into automated pytest test files under [`tests`](./tests).

The main testing focus areas were:
- header validation
- valid request flows
- invalid request flows
- boundary values
- edge cases
- correctness of returned JSON structures
- correctness of computed values such as totals, GST, discounts, wallet balance, loyalty points, and average rating

## 2. Test Case Design

Test cases were created for all documented endpoint groups:
- Admin
- Profile
- Addresses
- Products
- Cart
- Coupons
- Checkout
- Wallet
- Loyalty
- Orders
- Reviews
- Support

The detailed test design is recorded in [`QUICKCART_BLACK_BOX_TEST_CASES.md`](./QUICKCART_BLACK_BOX_TEST_CASES.md). The design includes:
- valid cases
- invalid cases
- missing-header cases
- wrong data type cases
- boundary-value cases
- state-based cases

Automated pytest coverage was added module by module:
- [`test_headers.py`](./tests/test_headers.py)
- [`test_admin.py`](./tests/test_admin.py)
- [`test_profile.py`](./tests/test_profile.py)
- [`test_addresses.py`](./tests/test_addresses.py)
- [`test_products.py`](./tests/test_products.py)
- [`test_cart.py`](./tests/test_cart.py)
- [`test_coupon.py`](./tests/test_coupon.py)
- [`test_checkout.py`](./tests/test_checkout.py)
- [`test_wallet.py`](./tests/test_wallet.py)
- [`test_loyalty.py`](./tests/test_loyalty.py)
- [`test_orders.py`](./tests/test_orders.py)
- [`test_reviews.py`](./tests/test_reviews.py)
- [`test_support.py`](./tests/test_support.py)

## 3. Execution Summary

The API server was loaded from Docker image and executed locally. The endpoint `/api/v1/admin/users` was used early to confirm the server was running correctly.

During execution, many tests passed successfully, which showed that:
- the API server was reachable
- required headers were enforced in many places
- several normal success flows were working
- many JSON responses had stable structures

At the same time, test execution also exposed multiple logic and contract problems. These failures were not caused by the test environment. They reflected differences between the documented API behavior and the actual API behavior.

The execution outcome can be summarized as:
- broad endpoint coverage was achieved
- many success and error conditions were exercised
- edge cases and correctness checks exposed important defects

The defect summaries produced during execution are recorded in:
- [`QUICKCART_BUG_REPORT.md`](./QUICKCART_BUG_REPORT.md)
- [`QUICKCART_FORMAL_BUG_REPORTS.md`](./QUICKCART_FORMAL_BUG_REPORTS.md)

## 4. Bugs Found

The testing found several meaningful bugs. The full details are documented in:
- [`QUICKCART_BUG_REPORT.md`](./QUICKCART_BUG_REPORT.md)
- [`QUICKCART_FORMAL_BUG_REPORTS.md`](./QUICKCART_FORMAL_BUG_REPORTS.md)

Important bugs discovered include:
- valid address creation rejected a valid 6-digit pincode
- forbidden address fields could still be updated
- cart accepted quantity `0` and negative quantities
- cart subtotal and total calculations were incorrect
- profile update did not return the updated profile object
- wallet deduction was not exact
- GST calculation was incorrect
- delivered-order cancel did not return the documented failure cleanly
- review validation was weak or incorrect
- review endpoints showed unstable behavior in some cases
- support ticket creation returned a different success status than expected
- loyalty redemption rejected valid positive redemption values
- some coupon rules appeared to be applied incorrectly below minimum cart value

These bugs affect both functional correctness and contract reliability for client applications.

## 5. Edge Case Testing

Special attention was given to edge and stress conditions. The key edge-case areas tested were:

- Cart:
  - quantity `0`
  - negative quantity
  - very large quantity
  - duplicate add accumulation
  - stock limit
  - total equals sum of subtotals
  - total includes the last item

- Wallet:
  - add `0`
  - add greater than `100000`
  - exact deduction after payment

- Checkout:
  - empty cart
  - COD with total above `5000`
  - payment status correctness for COD, WALLET, and CARD
  - GST added exactly once

- Coupons:
  - expired coupon
  - minimum cart value rule
  - FIXED coupon correctness
  - PERCENT coupon correctness
  - cap enforcement
  - coupon removal restores original total

- Loyalty:
  - missing headers
  - redeem `0`
  - redeem negative values
  - redeem more than available points
  - exact loyalty point decrease

- Orders:
  - invalid order id
  - cancel delivered order
  - stock restore after cancel
  - invoice arithmetic exact match

- Reviews:
  - rating `0`
  - rating `6`
  - comment length `1`
  - comment length `200`
  - comment too long
  - no reviews gives average `0`
  - average rating remains decimal

- Support:
  - valid status flow `OPEN -> IN_PROGRESS -> CLOSED`
  - invalid transition rejection
  - message stored exactly
  - subject length `5` and `100`
  - message length `1` and `500`

These edge-case tests were especially useful because they found defects that simple happy-path testing would not reveal.

## 6. Conclusion

The QuickCart API testing process produced a broad black-box test suite with coverage across all documented endpoint groups. The work combined endpoint analysis, manual test design, automated pytest implementation, execution, defect logging, and boundary-value validation.

Overall, the API is testable and many documented flows work, but the testing clearly shows that the implementation does not fully match the documented contract. Several defects were found in validation logic, calculations, response formats, and endpoint stability.

The final testing artifacts produced for this work are:
- [`QUICKCART_API_ENDPOINT_ANALYSIS.md`](./QUICKCART_API_ENDPOINT_ANALYSIS.md)
- [`QUICKCART_BLACK_BOX_TEST_CASES.md`](./QUICKCART_BLACK_BOX_TEST_CASES.md)
- [`QUICKCART_BUG_REPORT.md`](./QUICKCART_BUG_REPORT.md)
- [`QUICKCART_FORMAL_BUG_REPORTS.md`](./QUICKCART_FORMAL_BUG_REPORTS.md)
- [`QUICKCART_FINAL_TEST_REPORT.md`](./QUICKCART_FINAL_TEST_REPORT.md)

In conclusion, the testing process was successful in both validating working behavior and exposing important bugs. The final result is a structured and reusable black-box testing package for the QuickCart API.
