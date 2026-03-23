# Registration Module Unit Tests

Environment: Python 3.14, virtualenv `.venv`, pytest 9.0.2.

## Test Cases
- `test_register_member_success`  
  Expectation: registering a member stores their name and role.  
  Result: **Pass**.

- `test_get_member_success`  
  Expectation: fetching an existing member returns the correct record.  
  Result: **Pass**.

- `test_duplicate_registration_should_fail`  
  Expectation (logical): duplicate registrations should be rejected.  
  Actual run (pytest -q tests/unit/test_registration.py): **Failed** — duplicates are allowed (intentional bug), assertion `len(duplicates) == 1` fails because two entries are present.

- `test_assign_role_to_registered_user`  
  Expectation: assigning a role to an existing user stores and retrieves the role.  
  Result: **Pass** (`pytest -q tests/unit/test_crew.py`).

- `test_assign_role_to_unregistered_user_should_fail`  
  Expectation (logical): assigning a role to an unregistered user should fail.  
  Actual: **Failed** — role is stored for unregistered user (intentional bug), assertion `get_role('Kai') is None` fails because value is `"Mechanic"`.

- `test_add_car_success`  
  Expectation: adding a car stores it and it appears in listings.  
  Result: **Pass** (`pytest -q tests/unit/test_inventory.py`).

- `test_update_cash_allows_negative_bug`  
  Expectation (logical): cash balance should not become negative.  
  Actual: **Failed** — balance goes to `-500.0` (intentional bug), assertion `cash >= 0` fails.

## Notes / Issues Encountered
- Initial `pytest` invocation without setting the working directory tried to collect sibling project tests (`QuickCart`, `moneypoly`) and failed due to missing `requests`. Running from the project root avoids this.
- Pytest’s built-in debugging plugin imports the stdlib `code` module; our package name `code` shadowed it, causing an `AttributeError` during configuration. Added `addopts = -p no:debugging` in `pytest.ini` to skip that plugin.
- After the above adjustments, only the intentional duplicate-registration test fails; other registration tests pass.
