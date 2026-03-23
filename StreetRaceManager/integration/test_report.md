# Integration Testing Report

## Test Outcomes
- **Expected Pass (should pass if system were correct):**
  - IT-01
  - IT-12 (logical expectation)
  - IT-13 (logical expectation)
  - IT-15 (logical expectation)
  - IT-16 (logical expectation)

- **Expected Fail (due to known bugs):**
  - IT-02, IT-03, IT-04
  - IT-05, IT-06
  - IT-07, IT-08, IT-09
  - IT-10, IT-11
  - IT-14
  - IT-17, IT-18
  - IT-19, IT-20
  - IT-21, IT-22
  - IT-23, IT-24, IT-25, IT-26, IT-27, IT-28, IT-29, IT-30

## Detailed Scenarios

### IT-01: Register, Assign Driver, Enter Race
- Modules: registration, crew, race  
- Expected: Driver enters race.  
- Actual: Passes, but module would also allow non-drivers.  
- Bug: Missing role validation in race.  
- Explanation: RaceController doesn’t enforce Driver-only rule.

### IT-02: Unregistered Member Assigned and Entered
- Modules: crew, race  
- Expected: Unregistered member rejected.  
- Actual: Fails (member accepted).  
- Bug: No registration check.  
- Explanation: Crew and race don’t verify registration.

### IT-03: Duplicate Registration and Roles
- Modules: registration, crew  
- Expected: Single record for Casey.  
- Actual: Fails (duplicates stored).  
- Bug: No uniqueness enforcement.  
- Explanation: Duplicate members and roles allowed.

### IT-04: Non-Driver Enters Race
- Modules: registration, crew, race  
- Expected: Entry rejected.  
- Actual: Fails (accepted).  
- Bug: Race allows non-drivers.  
- Explanation: Role not validated.

### IT-05: Prize Money Credited After Win
- Modules: race, results, inventory  
- Expected: Cash +500.  
- Actual: Fails (cash unchanged).  
- Bug: Results ignore prize application.  
- Explanation: inventory not updated by results.

### IT-06: Cash Should Not Go Negative
- Modules: inventory, results  
- Expected: Cash ≥ 0.  
- Actual: Fails (cash negative, prize ignored).  
- Bug: Negative balances allowed.  
- Explanation: No guard on debits; prize skipped.

### IT-07: Damage Then Mechanic Mission
- Modules: vehicle_health, mission, crew  
- Expected: Health 20; mission only with Mechanic.  
- Actual: Fails (health ~60; any role accepted).  
- Bug: Damage halved; mission role unchecked.  
- Explanation: Safety and staffing not enforced.

### IT-08: Heavy Damage Blocks Mission
- Modules: vehicle_health, mission  
- Expected: Car unusable; mission blocked.  
- Actual: Fails (car usable; mission proceeds).  
- Bug: Damage halved prevents zero health.  
- Explanation: Over-damage is softened.

### IT-09: Wrong Role Assigned to Mission
- Modules: registration, crew, mission  
- Expected: Assignment rejected.  
- Actual: Fails (accepted).  
- Bug: required_roles ignored.  
- Explanation: MissionPlanner doesn’t validate roles.

### IT-10: Winner Ranking Order
- Modules: results, ranking  
- Expected: Descending order (Blake, Alex, Casey).  
- Actual: Fails (ascending order).  
- Bug: Wrong sort order.  
- Explanation: Rankings sorted ascending.

### IT-11: Loser Should Not Gain Wins
- Modules: results, ranking  
- Expected: Non-winner stays at 0 and below winner.  
- Actual: Fails (ordering can misplace).  
- Bug: Ascending sort misorders.  
- Explanation: Leaderboard inverted.

### IT-12: End-to-End Race, Prize, Ranking
- Modules: registration, crew, race, results, inventory, ranking  
- Expected: Cash +1000; Alex ranked first.  
- Actual: Fails (cash unchanged; ranking inverted).  
- Bug: Prize ignored; wrong order.  
- Explanation: Finance and leaderboard both break.

### IT-13: Damage, Repair, Then Race
- Modules: registration, crew, vehicle_health, mission, race, results  
- Expected: Car unusable until repaired; prize applied; correct ranking.  
- Actual: Fails (damage halved; mission role unchecked; prize ignored; ranking inverted).  
- Bug: Combined damage/role/finance/ranking issues.  
- Explanation: Multiple defects surfaced in one flow.

### IT-14: Negative Cash Propagation
- Modules: inventory, race, results, mission  
- Expected: No negative cash.  
- Actual: Fails (cash negative; prize ignored).  
- Bug: No cash guard; prize skipped.  
- Explanation: Sequential finances break.

### IT-15: Multiple Wins Sum Prize Money
- Modules: race, results, inventory, ranking  
- Expected: Cash +600; wins = 3.  
- Actual: Fails (cash 0; ranking ascending).  
- Bug: Prize ignored; order wrong.  
- Explanation: Earnings and leaderboard off.

### IT-16: Expense Then Prize Net
- Modules: race, inventory, results  
- Expected: Cash 1200.  
- Actual: Fails (cash lower/negative).  
- Bug: Prize ignored; negatives allowed.  
- Explanation: Debit/credit sequence not enforced.

### IT-17: Health Zero Retires Driver
- Modules: vehicle_health, race, results  
- Expected: Health 0, unusable.  
- Actual: Fails (health > 0).  
- Bug: Damage halved.  
- Explanation: Car never truly retires.

### IT-18: Mechanic Repairs, Car Re-enters
- Modules: registration, crew, mission, vehicle_health, race  
- Expected: Car unusable until repair; then usable.  
- Actual: Fails (car may stay usable; roles unchecked).  
- Bug: Halved damage; mission role unchecked.  
- Explanation: Repair loop not enforced.

### IT-19: Mission Charges Inventory
- Modules: mission, inventory  
- Expected: Cash deducted but not negative.  
- Actual: Fails (cash negative).  
- Bug: No negative-cash guard.  
- Explanation: Costs deducted regardless of balance.

### IT-20: Mission Cost Exceeds Cash
- Modules: inventory, mission  
- Expected: Mission blocked.  
- Actual: Fails (mission can proceed; cash negative).  
- Bug: Insufficient-funds check missing.  
- Explanation: Missions ignore available balance.

### IT-21: Duplicate Role on Same Member
- Modules: registration, crew  
- Expected: Single role entry.  
- Actual: Fails (duplicates allowed).  
- Bug: No deduplication.  
- Explanation: Roles stack up.

### IT-22: Unregistered Driver Direct Race Entry
- Modules: race  
- Expected: Race rejects unknown participant.  
- Actual: Fails (accepted).  
- Bug: Race doesn’t validate registration.  
- Explanation: No upstream check.

### IT-23: Loser Ranking After Single Race
- Modules: race, results, ranking  
- Expected: Winner above loser.  
- Actual: Fails (ascending order can invert).  
- Bug: Wrong sort order.  
- Explanation: Leaderboard inverted.

### IT-24: Ranking After Zero Races
- Modules: registration, ranking  
- Expected: Stable zero-win list.  
- Actual: Fails (order arbitrary).  
- Bug: Ascending sort on zeros.  
- Explanation: Baseline order unstable.

### IT-25: Race with Partially Damaged Car
- Modules: vehicle_health, race, results  
- Expected: Health 70 after 30 damage.  
- Actual: Fails (health ~85).  
- Bug: Damage halved.  
- Explanation: Car healthier than it should be.

### IT-26: Winner vs. Non-Winner with Prize
- Modules: race, results, inventory, ranking  
- Expected: Prize to winner; winner ranked first.  
- Actual: Fails (prize ignored; ranking inverted).  
- Bug: Prize skipped; wrong ordering.  
- Explanation: Rewards and standings misaligned.

### IT-27: Mechanic in Mission, Blocked in Race
- Modules: registration, crew, race, mission  
- Expected: Race rejects Mechanic; mission accepts.  
- Actual: Fails (race may accept).  
- Bug: Race role validation absent.  
- Explanation: Context-specific rules ignored.

### IT-28: Prize Then Mission Cost Balance
- Modules: results, inventory, mission  
- Expected: Cash 600 after +1000 -400.  
- Actual: Fails (prize ignored; cash negative).  
- Bug: Prize not applied; negatives allowed.  
- Explanation: Sequential balance breaks.

### IT-29: Ranking After Zero Races (Stability Check)
- Modules: registration, ranking  
- Expected: Stable ordering of zero wins.  
- Actual: Fails (order arbitrary).  
- Bug: Ascending sort instability.  
- Explanation: Even empty results are misordered.

### IT-30: Full Crew Lifecycle
- Modules: all  
- Expected: Correct roles, damage, repair, prize, ranking, cash.  
- Actual: Fails (halved damage, role skips, prize ignored, ranking inverted, cash can go negative).  
- Bug: Combined defects across modules.  
- Explanation: End-to-end flow reveals all major issues.

## Summary of Integration Issues
- Registration: Duplicate members allowed; races accept unregistered entrants.
-( Role validation: Roles can be assigned to unregistered users; races ignore Driver-only; missions ignore required_roles.
- Inventory/cash: Prizes not applied; negative balances allowed; costs can exceed balance.
- Vehicle health: Damage is halved, preventing zero-health states and blocking logic.
- Ranking: Sorts ascending instead of descending, misordering leaders and destabilizing zero-win cases.
