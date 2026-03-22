Category: Admin
  Endpoint:
    Method: GET
    URL: /api/v1/admin/users
    Headers: X-Roll-Number
    Body: None
    Success: 200 OK, returns all users with wallet balances and loyalty points
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is not a valid integer
  Endpoint:
    Method: GET
    URL: /api/v1/admin/users/{user_id}
    Headers: X-Roll-Number
    Body: None
    Success: 200 OK, returns one specific user
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is not a valid integer
  Endpoint:
    Method: GET
    URL: /api/v1/admin/carts
    Headers: X-Roll-Number
    Body: None
    Success: 200 OK, returns every cart with all items and computed totals
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is not a valid integer
  Endpoint:
    Method: GET
    URL: /api/v1/admin/orders
    Headers: X-Roll-Number
    Body: None
    Success: 200 OK, returns all orders across all users, including payment and order status
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is not a valid integer
  Endpoint:
    Method: GET
    URL: /api/v1/admin/products
    Headers: X-Roll-Number
    Body: None
    Success: 200 OK, returns all products including inactive ones
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is not a valid integer
  Endpoint:
    Method: GET
    URL: /api/v1/admin/coupons
    Headers: X-Roll-Number
    Body: None
    Success: 200 OK, returns all coupons including expired ones with discount rules
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is not a valid integer
  Endpoint:
    Method: GET
    URL: /api/v1/admin/tickets
    Headers: X-Roll-Number
    Body: None
    Success: 200 OK, returns all support tickets across all users
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is not a valid integer
  Endpoint:
    Method: GET
    URL: /api/v1/admin/addresses
    Headers: X-Roll-Number
    Body: None
    Success: 200 OK, returns all addresses across all users
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is not a valid integer

Category: Profile
  Endpoint:
    Method: GET
    URL: /api/v1/profile
    Headers: X-Roll-Number, X-User-ID
    Body: None
    Success: 200 OK, returns the user's profile
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is invalid, 400 if X-User-ID is missing, invalid, non-positive, or does not match an existing user
  Endpoint:
    Method: PUT
    URL: /api/v1/profile
    Headers: X-Roll-Number, X-User-ID
    Body: JSON body for profile updates, including name and phone when changing them
    Success: 200 OK, updates and returns the user's profile
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is invalid, 400 if X-User-ID is missing, invalid, non-positive, or does not match an existing user, 400 if name is shorter than 2 or longer than 50 characters, 400 if phone is not exactly 10 digits

Category: Addresses
  Endpoint:
    Method: GET
    URL: /api/v1/addresses
    Headers: X-Roll-Number, X-User-ID
    Body: None
    Success: 200 OK, returns all addresses for the user
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is invalid, 400 if X-User-ID is missing, invalid, non-positive, or does not match an existing user
  Endpoint:
    Method: POST
    URL: /api/v1/addresses
    Headers: X-Roll-Number, X-User-ID
    Body: JSON body with label, street, city, pincode, and optionally is_default
    Success: 200 OK or 201 Created, returns a message and the full created address object including address_id, label, street, city, pincode, and is_default
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is invalid, 400 if X-User-ID is missing, invalid, non-positive, or does not match an existing user, 400 if label is not HOME, OFFICE, or OTHER, 400 if street is shorter than 5 or longer than 100 characters, 400 if city is shorter than 2 or longer than 50 characters, 400 if pincode is not exactly 6 digits
  Endpoint:
    Method: PUT
    URL: /api/v1/addresses/{address_id}
    Headers: X-Roll-Number, X-User-ID
    Body: JSON body that can update only street and is_default
    Success: 200 OK, returns the updated address data
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is invalid, 400 if X-User-ID is missing, invalid, non-positive, or does not match an existing user, 400 if forbidden fields such as label, city, or pincode are changed
  Endpoint:
    Method: DELETE
    URL: /api/v1/addresses/{address_id}
    Headers: X-Roll-Number, X-User-ID
    Body: None
    Success: 200 OK, deletes the address
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is invalid, 400 if X-User-ID is missing, invalid, non-positive, or does not match an existing user, 404 if the address does not exist

Category: Products
  Endpoint:
    Method: GET
    URL: /api/v1/products
    Headers: X-Roll-Number, X-User-ID
    Body: None
    Success: 200 OK, returns active products only; may support category filter, name search, and price sorting
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is invalid, 400 if X-User-ID is missing, invalid, non-positive, or does not match an existing user
  Endpoint:
    Method: GET
    URL: /api/v1/products/{product_id}
    Headers: X-Roll-Number, X-User-ID
    Body: None
    Success: 200 OK, returns one product by ID
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is invalid, 400 if X-User-ID is missing, invalid, non-positive, or does not match an existing user, 404 if the product does not exist

Category: Cart
  Endpoint:
    Method: GET
    URL: /api/v1/cart
    Headers: X-Roll-Number, X-User-ID
    Body: None
    Success: 200 OK, returns the cart with items, subtotals, and total
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is invalid, 400 if X-User-ID is missing, invalid, non-positive, or does not match an existing user
  Endpoint:
    Method: POST
    URL: /api/v1/cart/add
    Headers: X-Roll-Number, X-User-ID
    Body: JSON body including product_id and quantity
    Success: 200 OK or 201 Created, adds the item to the cart or increases quantity if the product is already present
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is invalid, 400 if X-User-ID is missing, invalid, non-positive, or does not match an existing user, 400 if quantity is 0 or negative, 404 if the product does not exist, 400 if requested quantity exceeds stock
  Endpoint:
    Method: POST
    URL: /api/v1/cart/update
    Headers: X-Roll-Number, X-User-ID
    Body: JSON body including product_id and new quantity
    Success: 200 OK, updates the cart quantity
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is invalid, 400 if X-User-ID is missing, invalid, non-positive, or does not match an existing user, 400 if quantity is less than 1
  Endpoint:
    Method: POST
    URL: /api/v1/cart/remove
    Headers: X-Roll-Number, X-User-ID
    Body: JSON body including product_id
    Success: 200 OK, removes the item from the cart
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is invalid, 400 if X-User-ID is missing, invalid, non-positive, or does not match an existing user, 404 if the product is not in the cart
  Endpoint:
    Method: DELETE
    URL: /api/v1/cart/clear
    Headers: X-Roll-Number, X-User-ID
    Body: None
    Success: 200 OK, clears the whole cart
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is invalid, 400 if X-User-ID is missing, invalid, non-positive, or does not match an existing user

Category: Coupons
  Endpoint:
    Method: POST
    URL: /api/v1/coupon/apply
    Headers: X-Roll-Number, X-User-ID
    Body: JSON body including the coupon code
    Success: 200 OK, applies the coupon and returns the updated cart or discount details
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is invalid, 400 if X-User-ID is missing, invalid, non-positive, or does not match an existing user, 400 if the coupon is expired, 400 if minimum cart value is not met, 400 if coupon rules are otherwise invalid
  Endpoint:
    Method: POST
    URL: /api/v1/coupon/remove
    Headers: X-Roll-Number, X-User-ID
    Body: None or minimal JSON body depending on implementation
    Success: 200 OK, removes the currently applied coupon
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is invalid, 400 if X-User-ID is missing, invalid, non-positive, or does not match an existing user

Category: Checkout
  Endpoint:
    Method: POST
    URL: /api/v1/checkout
    Headers: X-Roll-Number, X-User-ID
    Body: JSON body with payment_method set to COD, WALLET, or CARD
    Success: 200 OK or 201 Created, creates the order with correct GST and payment status
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is invalid, 400 if X-User-ID is missing, invalid, non-positive, or does not match an existing user, 400 if payment_method is not COD, WALLET, or CARD, 400 if the cart is empty, 400 if COD is used for totals above 5000

Category: Wallet
  Endpoint:
    Method: GET
    URL: /api/v1/wallet
    Headers: X-Roll-Number, X-User-ID
    Body: None
    Success: 200 OK, returns the current wallet balance
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is invalid, 400 if X-User-ID is missing, invalid, non-positive, or does not match an existing user
  Endpoint:
    Method: POST
    URL: /api/v1/wallet/add
    Headers: X-Roll-Number, X-User-ID
    Body: JSON body including amount
    Success: 200 OK, adds money to the wallet
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is invalid, 400 if X-User-ID is missing, invalid, non-positive, or does not match an existing user, 400 if amount is less than or equal to 0, 400 if amount is greater than 100000
  Endpoint:
    Method: POST
    URL: /api/v1/wallet/pay
    Headers: X-Roll-Number, X-User-ID
    Body: JSON body including amount
    Success: 200 OK, deducts the requested payment from the wallet
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is invalid, 400 if X-User-ID is missing, invalid, non-positive, or does not match an existing user, 400 if amount is less than or equal to 0, 400 if wallet balance is insufficient

Category: Loyalty
  Endpoint:
    Method: GET
    URL: /api/v1/loyalty
    Headers: X-Roll-Number, X-User-ID
    Body: None
    Success: 200 OK, returns current loyalty points
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is invalid, 400 if X-User-ID is missing, invalid, non-positive, or does not match an existing user
  Endpoint:
    Method: POST
    URL: /api/v1/loyalty/redeem
    Headers: X-Roll-Number, X-User-ID
    Body: JSON body including amount or points to redeem
    Success: 200 OK, redeems loyalty points successfully
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is invalid, 400 if X-User-ID is missing, invalid, non-positive, or does not match an existing user, 400 if redeem amount is less than 1, 400 if the user does not have enough points

Category: Orders
  Endpoint:
    Method: GET
    URL: /api/v1/orders
    Headers: X-Roll-Number, X-User-ID
    Body: None
    Success: 200 OK, returns all orders for the user
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is invalid, 400 if X-User-ID is missing, invalid, non-positive, or does not match an existing user
  Endpoint:
    Method: GET
    URL: /api/v1/orders/{order_id}
    Headers: X-Roll-Number, X-User-ID
    Body: None
    Success: 200 OK, returns details for one order
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is invalid, 400 if X-User-ID is missing, invalid, non-positive, or does not match an existing user, 404 if the order does not exist
  Endpoint:
    Method: POST
    URL: /api/v1/orders/{order_id}/cancel
    Headers: X-Roll-Number, X-User-ID
    Body: None or minimal JSON body depending on implementation
    Success: 200 OK, cancels the order and restores stock
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is invalid, 400 if X-User-ID is missing, invalid, non-positive, or does not match an existing user, 400 if the order is already delivered, 404 if the order does not exist
  Endpoint:
    Method: GET
    URL: /api/v1/orders/{order_id}/invoice
    Headers: X-Roll-Number, X-User-ID
    Body: None
    Success: 200 OK, returns invoice details including subtotal, GST amount, and total
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is invalid, 400 if X-User-ID is missing, invalid, non-positive, or does not match an existing user, 404 if the order does not exist

Category: Reviews
  Endpoint:
    Method: GET
    URL: /api/v1/products/{product_id}/reviews
    Headers: X-Roll-Number, X-User-ID
    Body: None
    Success: 200 OK, returns all reviews for the product and its average rating
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is invalid, 400 if X-User-ID is missing, invalid, non-positive, or does not match an existing user, 404 if the product does not exist
  Endpoint:
    Method: POST
    URL: /api/v1/products/{product_id}/reviews
    Headers: X-Roll-Number, X-User-ID
    Body: JSON body including rating and comment
    Success: 200 OK or 201 Created, creates a review for the product
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is invalid, 400 if X-User-ID is missing, invalid, non-positive, or does not match an existing user, 400 if rating is outside 1 to 5, 400 if comment length is outside 1 to 200 characters, 404 if the product does not exist

Category: Support
  Endpoint:
    Method: POST
    URL: /api/v1/support/ticket
    Headers: X-Roll-Number, X-User-ID
    Body: JSON body including subject and message
    Success: 200 OK or 201 Created, creates a support ticket with status OPEN
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is invalid, 400 if X-User-ID is missing, invalid, non-positive, or does not match an existing user, 400 if subject length is outside 5 to 100 characters, 400 if message length is outside 1 to 500 characters
  Endpoint:
    Method: GET
    URL: /api/v1/support/tickets
    Headers: X-Roll-Number, X-User-ID
    Body: None
    Success: 200 OK, returns all support tickets for the user
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is invalid, 400 if X-User-ID is missing, invalid, non-positive, or does not match an existing user
  Endpoint:
    Method: PUT
    URL: /api/v1/support/tickets/{ticket_id}
    Headers: X-Roll-Number, X-User-ID
    Body: JSON body including the new status
    Success: 200 OK, updates the ticket status following allowed progression
    Errors: 401 if X-Roll-Number is missing, 400 if X-Roll-Number is invalid, 400 if X-User-ID is missing, invalid, non-positive, or does not match an existing user, 400 if the status transition is not allowed, 404 if the ticket does not exist
