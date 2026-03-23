# Integration Test Scenarios

Scenarios are organized by cross-module themes. Expected vs. actual outcomes reflect the current known behavior of the system (tests not executed yet).

## 1. Registration → Crew → Race Integration

### IT-01: Register, Assign Driver, Enter Race
**Modules Involved:** registration, crew, race  
**Scenario Description:** Register a member, give them the Driver role, and enter them into a race.  
**Steps:**  
1. Register member "Alex".  
2. Assign Driver role to Alex.  
3. Create race "R1" and enter Alex.  
**Expected Result (Correct Behavior):** Alex appears in race R1 as a Driver.  
**Actual Result (With Current Implementation):** Alex enters successfully; non-drivers would also be accepted.  
**Why This Test Is Important:** Ensures core race entry and role gating.

### IT-02: Unregistered Member Assigned and Entered
**Modules Involved:** crew, race  
**Scenario Description:** Assign a role to an unregistered member and enter them into a race.  
**Steps:**  
1. Assign Driver role to "Blake" without registering.  
2. Create race "R2" and enter Blake.  
**Expected Result (Correct Behavior):** Role assignment and race entry are rejected.  
**Actual Result (With Current Implementation):** Both actions succeed.  
**Why This Test Is Important:** Prevents unverified participants in races.

### IT-03: Duplicate Registration then Role Assignment
**Modules Involved:** registration, crew  
**Scenario Description:** Register the same member twice and assign roles to both entries.  
**Steps:**  
1. Register "Casey" twice.  
2. Assign Driver role to each record.  
**Expected Result (Correct Behavior):** Second registration rejected; only one role assignment exists.  
**Actual Result (With Current Implementation):** Both records persist and hold roles.  
**Why This Test Is Important:** Avoids identity duplication.

### IT-04: Non-Driver Entered in Race
**Modules Involved:** registration, crew, race  
**Scenario Description:** Register a member, assign Mechanic role, attempt race entry.  
**Steps:**  
1. Register "Dana".  
2. Assign Mechanic role.  
3. Enter race "R3".  
**Expected Result (Correct Behavior):** Entry rejected because role is not Driver.  
**Actual Result (With Current Implementation):** Entry accepted.  
**Why This Test Is Important:** Protects race safety and fairness.

### IT-14: Two Members, Only One Driver Enters
**Modules Involved:** registration, crew, race  
**Scenario Description:** Register two members; only one is a Driver; attempt to enter both.  
**Steps:**  
1. Register MemberA (Driver) and MemberB (Mechanic).  
2. Enter both into a race.  
**Expected Result (Correct Behavior):** Only MemberA is accepted.  
**Actual Result (With Current Implementation):** Both can be accepted.  
**Why This Test Is Important:** Verifies role-based admission.

### IT-21: Duplicate Role Assignment to Same Member
**Modules Involved:** registration, crew  
**Scenario Description:** Assign the same role twice to one member.  
**Steps:**  
1. Register "MemberA".  
2. Assign Driver role twice.  
**Expected Result (Correct Behavior):** Single Driver role stored.  
**Actual Result (With Current Implementation):** Duplicate role entries can persist.  
**Why This Test Is Important:** Prevents redundant role data.

### IT-22: Unregistered Driver Attempts Race Entry Directly
**Modules Involved:** race  
**Scenario Description:** Enter a race with a name that was never registered or assigned a role.  
**Steps:**  
1. Call race entry for "Ghost".  
**Expected Result (Correct Behavior):** Race module rejects unknown participant.  
**Actual Result (With Current Implementation):** Participant may be accepted.  
**Why This Test Is Important:** Ensures race trusts upstream validation.

## 2. Race → Results → Inventory Integration

### IT-05: Prize Money Credited After Win
**Modules Involved:** race, results, inventory  
**Scenario Description:** Record a winner with prize money and verify cash.  
**Steps:**  
1. Create race "R4".  
2. Record winner "Alex" with prize 500.  
3. Check inventory cash.  
**Expected Result (Correct Behavior):** Cash increases by 500.  
**Actual Result (With Current Implementation):** Cash unchanged.  
**Why This Test Is Important:** Aligns finances with race outcomes.

### IT-06: Cash Should Not Go Negative
**Modules Involved:** inventory, results  
**Scenario Description:** Expenses exceed balance, then a small prize is awarded.  
**Steps:**  
1. Set cash to 100.  
2. Deduct 300 for race costs.  
3. Record prize 50.  
**Expected Result (Correct Behavior):** Cash floors at 0 or transaction blocked.  
**Actual Result (With Current Implementation):** Cash goes negative; prize not applied.  
**Why This Test Is Important:** Prevents invalid financial state.

### IT-15: Multiple Wins Sum Prize Money
**Modules Involved:** race, results, inventory, ranking  
**Scenario Description:** Same driver wins three races with prizes.  
**Steps:**  
1. Run three races; same driver wins each with prize 200.  
2. Check inventory cash (expect +600).  
3. Check ranking wins (expect 3).  
**Expected Result (Correct Behavior):** Cash +600; wins = 3.  
**Actual Result (With Current Implementation):** Cash unchanged; ranking order still ascending.  
**Why This Test Is Important:** Verifies cumulative payouts and ranking alignment.

### IT-16: Expenses Then Prize Net Balance
**Modules Involved:** race, inventory, results  
**Scenario Description:** Deduct entry fee then add prize.  
**Steps:**  
1. Cash 1000.  
2. Deduct 300 entry fee.  
3. Add prize 500.  
**Expected Result (Correct Behavior):** Cash = 1200.  
**Actual Result (With Current Implementation):** Cash can go negative or ignore prize.  
**Why This Test Is Important:** Checks ordering of debits/credits.

### IT-19: Mission Charges Inventory
**Modules Involved:** mission, inventory  
**Scenario Description:** Complete a mission that costs money.  
**Steps:**  
1. Set cash baseline.  
2. Start mission costing 400; mark complete.  
3. Verify cash deduction.  
**Expected Result (Correct Behavior):** Cash reduced by 400 without going negative.  
**Actual Result (With Current Implementation):** Cash can drop negative unchecked.  
**Why This Test Is Important:** Ensures missions respect financial limits.

### IT-20: Mission Cost Exceeds Cash
**Modules Involved:** inventory, mission  
**Scenario Description:** Attempt a mission costing more than available cash.  
**Steps:**  
1. Cash = 100.  
2. Attempt mission cost 500.  
**Expected Result (Correct Behavior):** Mission rejected.  
**Actual Result (With Current Implementation):** Mission may proceed; cash negative.  
**Why This Test Is Important:** Prevents insolvency states.

### IT-28: Prize Then Mission Cost Sequential Balance
**Modules Involved:** results, inventory, mission  
**Scenario Description:** Apply prize, then deduct mission cost.  
**Steps:**  
1. Cash 0.  
2. Add prize 1000.  
3. Deduct mission cost 400.  
**Expected Result (Correct Behavior):** Cash = 600.  
**Actual Result (With Current Implementation):** Prize ignored; cash may be negative.  
**Why This Test Is Important:** Validates sequential financial operations.

## 3. Vehicle Health → Mission (and Race) Integration

### IT-07: Damage Then Mechanic Mission Before Next Race
**Modules Involved:** vehicle_health, mission, crew  
**Scenario Description:** Damage a car and require a mechanic mission before reuse.  
**Steps:**  
1. Add car "CarA"; apply damage 80.  
2. Create repair mission requiring Mechanic.  
3. Assign a Mechanic.  
**Expected Result (Correct Behavior):** Car reflects full damage; mission only runs with Mechanic.  
**Actual Result (With Current Implementation):** Damage halved; any role accepted.  
**Why This Test Is Important:** Couples safety with staffing.

### IT-08: Heavy Damage Should Block Mission
**Modules Involved:** vehicle_health, mission  
**Scenario Description:** Apply very large damage then attempt mission using the car.  
**Steps:**  
1. Add car "CarB"; apply damage 200.  
2. Start mission requiring a usable car.  
**Expected Result (Correct Behavior):** Car unusable; mission blocked.  
**Actual Result (With Current Implementation):** Car may stay usable; mission proceeds.  
**Why This Test Is Important:** Prevents unsafe vehicle use.

### IT-13: Damage, Repair, Then Race
**Modules Involved:** registration, crew, vehicle_health, mission, race, results  
**Scenario Description:** Damage a car, repair it, race, and record results.  
**Steps:**  
1. Register Driver Alex; assign Driver role.  
2. Add car; apply damage 90.  
3. Assign Mechanic to repair mission; repair car.  
4. Enter race; record Alex as winner with prize 500.  
**Expected Result (Correct Behavior):** Car unusable until repaired; prize applied; ranking correct.  
**Actual Result (With Current Implementation):** Car remains usable; mission role unchecked; prize ignored; ranking ascending.  
**Why This Test Is Important:** Integrates safety, staffing, finance, ranking.

### IT-17: Health Drops to Zero Mid-Race
**Modules Involved:** vehicle_health, race, results  
**Scenario Description:** Apply enough damage during race to retire a car.  
**Steps:**  
1. Add car; apply race damage to reach 0.  
2. Attempt to record driver as winner.  
**Expected Result (Correct Behavior):** Driver retired; no win recorded.  
**Actual Result (With Current Implementation):** Damage halved; driver may still win.  
**Why This Test Is Important:** Ensures race outcomes respect vehicle state.

### IT-18: Mechanic Repairs, Car Re-enters Race
**Modules Involved:** registration, crew, mission, vehicle_health, race  
**Scenario Description:** Damage a car, run a repair mission with a Mechanic, race again.  
**Steps:**  
1. Register Mechanic.  
2. Damage car.  
3. Run repair mission.  
4. Enter repaired car in race.  
**Expected Result (Correct Behavior):** Car restored to usable; race entry allowed.  
**Actual Result (With Current Implementation):** Car may have stayed usable all along; role checks skipped.  
**Why This Test Is Important:** Verifies repair loop realism.

### IT-25: Race with Partially Damaged Car
**Modules Involved:** vehicle_health, race, results  
**Scenario Description:** Enter a car after moderate damage and record result.  
**Steps:**  
1. Damage car by 30.  
2. Enter race and record outcome.  
**Expected Result (Correct Behavior):** Health reflects 70; race proceeds; result stored.  
**Actual Result (With Current Implementation):** Health ~85 (damage halved); state inconsistent.  
**Why This Test Is Important:** Ensures health data integrity in races.

### IT-07/IT-08 Variants: Role/Availability Checks After Damage
**Modules Involved:** race, vehicle_health, mission  
**Scenario Description:** Damage car in race; start repair mission requiring a specific role.  
**Steps:**  
1. Apply race damage.  
2. Launch mission requiring Mechanic.  
3. Verify role availability.  
**Expected Result (Correct Behavior):** Mission only proceeds if required role available.  
**Actual Result (With Current Implementation):** Role not enforced; car may still be usable.  
**Why This Test Is Important:** Cross-checks damage effects with staffing.

## 4. Results → Ranking Integration

### IT-10: Winner Ranking Order
**Modules Involved:** results, ranking  
**Scenario Description:** Record multiple winners and check ranking order.  
**Steps:**  
1. Record wins: Blake (3), Casey (1), Alex (2).  
2. Retrieve rankings.  
**Expected Result (Correct Behavior):** Order Blake, Alex, Casey (descending wins).  
**Actual Result (With Current Implementation):** Rankings sorted ascending.  
**Why This Test Is Important:** Leaderboard accuracy.

### IT-11: Loser Should Not Gain Wins
**Modules Involved:** results, ranking  
**Scenario Description:** Record a winner and verify the loser’s wins stay at zero.  
**Steps:**  
1. Record winner Alex; participant Jordan loses.  
2. Check Jordan’s wins.  
**Expected Result (Correct Behavior):** Jordan = 0; Alex = 1.  
**Actual Result (With Current Implementation):** Ascending sort can misorder standings.  
**Why This Test Is Important:** Prevents crediting non-winners.

### IT-23: Loser Ranking Check After Single Race
**Modules Involved:** race, results, ranking  
**Scenario Description:** Two drivers race; only winner should rank higher.  
**Steps:**  
1. Run race; record Driver A as winner over Driver B.  
2. Check ranking.  
**Expected Result (Correct Behavior):** Driver A above Driver B.  
**Actual Result (With Current Implementation):** Ascending sort may place B above A.  
**Why This Test Is Important:** Confirms single-race ordering.

### IT-24: Rankings After Zero Races
**Modules Involved:** registration, ranking  
**Scenario Description:** Register drivers, run no races, inspect rankings.  
**Steps:**  
1. Register three drivers.  
2. Fetch rankings immediately.  
**Expected Result (Correct Behavior):** All at 0 wins; stable order.  
**Actual Result (With Current Implementation):** Ascending sort still applied; ordering may be arbitrary.  
**Why This Test Is Important:** Baseline leaderboard stability.

### IT-26: Winner vs. Non-Winner with Prize
**Modules Involved:** race, results, inventory, ranking  
**Scenario Description:** Two drivers finish; only winner gets prize and ranking boost.  
**Steps:**  
1. Run race; record Driver A as winner with prize 300; Driver B loses.  
2. Check inventory and rankings.  
**Expected Result (Correct Behavior):** Inventory +300; A ranked above B; B’s wins unchanged.  
**Actual Result (With Current Implementation):** Prize not applied; ascending sort may misorder.  
**Why This Test Is Important:** Differentiates winners from participants.

### IT-29: Ranking After Zero Races (Stability Check)
**Modules Involved:** registration, ranking  
**Scenario Description:** Same as IT-24, emphasized for stability.  
**Steps:**  
1. Register multiple drivers.  
2. Fetch rankings with no wins.  
**Expected Result (Correct Behavior):** Stable ordering; no crashes.  
**Actual Result (With Current Implementation):** Ascending sort may shuffle; still 0 wins.  
**Why This Test Is Important:** Ensures system handles empty-win state.

## 5. Full System Integration (End-to-End)

### IT-12: End-to-End Race, Prize, Ranking
**Modules Involved:** registration, crew, race, results, inventory, ranking  
**Scenario Description:** Run a complete race flow from registration to ranking.  
**Steps:**  
1. Register Alex and Blake; assign Driver roles.  
2. Enter race "R5"; record Alex as winner with prize 1000.  
3. Check inventory cash and rankings.  
**Expected Result (Correct Behavior):** Cash +1000; Alex ranked above Blake.  
**Actual Result (With Current Implementation):** Cash unchanged; ranking ascending may not show Alex first.  
**Why This Test Is Important:** Combines finance and leaderboard effects.

### IT-30: Full Crew Lifecycle with Damage, Repair, Race, Prize
**Modules Involved:** all modules  
**Scenario Description:** Complete lifecycle: register roles, mission repair, race, prize, ranking, inventory.  
**Steps:**  
1. Register Driver and Mechanic.  
2. Driver races; car damaged.  
3. Mechanic repairs via mission (cost deducted).  
4. Driver races again and wins; prize applied; ranking updated.  
**Expected Result (Correct Behavior):** Mission cost deducted; prize added; Driver ranked first; cash = prize - cost; car health correct.  
**Actual Result (With Current Implementation):** Damage halved; mission accepts any role; prize ignored; cash can go negative; ranking ascending.  
**Why This Test Is Important:** Stress-tests all cross-module interactions.

### IT-27: Mechanic Allowed in Mission, Blocked in Race
**Modules Involved:** registration, crew, race, mission  
**Scenario Description:** Ensure role-specific pathways: race vs. mission.  
**Steps:**  
1. Register MemberA; assign Mechanic role.  
2. Attempt race entry (should fail).  
3. Assign to a mechanic mission (should succeed).  
**Expected Result (Correct Behavior):** Race rejects; mission accepts.  
**Actual Result (With Current Implementation):** Race may accept; mission accepts.  
**Why This Test Is Important:** Confirms divergent role rules by context.

### IT-28 (already listed in Section 2): Prize Then Mission Cost
**Note:** Covered above for sequential balance; referenced here for end-to-end cash consistency.

### IT-23/IT-26 Combined Check
**Modules Involved:** race, results, ranking, inventory  
**Scenario Description:** Winner/loser differentiation with prize handling.  
**Steps:**  
1. Run race with two drivers.  
2. Record winner with prize.  
3. Verify loser wins stay 0; prize applied to inventory; rankings ordered.  
**Expected Result (Correct Behavior):** Winner rewarded and ranked above loser.  
**Actual Result (With Current Implementation):** Prize ignored; ascending ranking may misorder.  
**Why This Test Is Important:** Consolidates prize and ranking correctness in one flow.
