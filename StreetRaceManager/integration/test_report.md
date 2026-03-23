# Integration Testing Report (Concise)

## Test Outcomes
- Expected to pass ideally: IT-01, IT-12, IT-13, IT-15, IT-16  
- Expected to fail (known bugs): IT-02–IT-11, IT-14, IT-17–IT-30

## Scenarios (condensed)

IT-01: Register, assign Driver, enter race  
Modules: registration, crew, race  
Expected: Driver enters. Actual: Passes, but race would also accept non-drivers (role check missing).

IT-02: Unregistered member entered  
Modules: crew, race  
Expected: Rejected. Actual: Accepted (no registration check).

IT-03: Duplicate registration  
Modules: registration, crew  
Expected: Single record/role. Actual: Duplicates allowed.

IT-04: Non-driver in race  
Modules: registration, crew, race  
Expected: Rejected. Actual: Accepted (no role validation).

IT-05: Prize money applied  
Modules: race, results, inventory  
Expected: Cash increases. Actual: Cash unchanged (prize ignored).

IT-06: Cash not negative  
Modules: inventory, results  
Expected: Cash ≥ 0. Actual: Negative allowed; prize ignored.

IT-07: Damage then mechanic mission  
Modules: vehicle_health, mission, crew  
Expected: Low health; only Mechanic allowed. Actual: Damage halved; any role accepted.

IT-08: Heavy damage blocks mission  
Modules: vehicle_health, mission  
Expected: Car unusable; mission blocked. Actual: Car still usable (halved damage).

IT-09: Wrong role on mission  
Modules: registration, crew, mission  
Expected: Reject mismatch. Actual: Accepted (required_roles ignored).

IT-10: Winner ranking order  
Modules: results, ranking  
Expected: Descending wins. Actual: Ascending (inverted).

IT-11: Loser stays below winner  
Modules: results, ranking  
Expected: Non-winner below winner. Actual: Ascending sort can misorder.

IT-12: End-to-end race→prize→ranking  
Modules: registration, crew, race, results, inventory, ranking  
Expected: Prize applied; winner first. Actual: Prize ignored; ranking inverted.

IT-13: Damage, repair, race  
Modules: registration, crew, vehicle_health, mission, race, results  
Expected: Car unusable until repaired; prize applied; ranking correct. Actual: Damage halved; mission role unchecked; prize ignored; ranking inverted.

IT-14: Negative cash propagation  
Modules: inventory, race, results, mission  
Expected: Never negative. Actual: Negative cash; prize ignored.

IT-15: Multiple wins sum prize  
Modules: race, results, inventory, ranking  
Expected: Cash +600; wins=3. Actual: Cash 0; ranking inverted.

IT-16: Expense then prize net  
Modules: race, inventory, results  
Expected: Cash 1200. Actual: Lower/negative (prize ignored; negatives allowed).

IT-17: Health zero retires driver  
Modules: vehicle_health, race, results  
Expected: Health 0, unusable. Actual: Health >0 (halved damage).

IT-18: Mechanic repairs, car re-enters  
Modules: registration, crew, mission, vehicle_health, race  
Expected: Unusable until repaired. Actual: May stay usable; roles unchecked.

IT-19: Mission charges inventory  
Modules: mission, inventory  
Expected: Deduct without negative. Actual: Negative cash possible.

IT-20: Mission cost exceeds cash  
Modules: inventory, mission  
Expected: Mission blocked. Actual: Proceeds; cash negative.

IT-21: Duplicate role on member  
Modules: registration, crew  
Expected: One role entry. Actual: Duplicate roles stored.

IT-22: Unregistered direct race entry  
Modules: race  
Expected: Reject. Actual: Accepted.

IT-23: Loser ranking after one race  
Modules: race, results, ranking  
Expected: Winner above loser. Actual: Ascending sort may invert.

IT-24: Ranking with zero races  
Modules: registration, ranking  
Expected: Stable zero-win list. Actual: Arbitrary order (ascending sort).

IT-25: Partially damaged car racing  
Modules: vehicle_health, race, results  
Expected: Health 70. Actual: ~85 (halved damage).

IT-26: Winner vs non-winner with prize  
Modules: race, results, inventory, ranking  
Expected: Prize to winner; winner first. Actual: Prize ignored; ranking inverted.

IT-27: Mechanic in mission, blocked in race  
Modules: registration, crew, race, mission  
Expected: Race rejects Mechanic; mission accepts. Actual: Race may accept.

IT-28: Prize then mission cost  
Modules: results, inventory, mission  
Expected: Cash 600 after +1000 -400. Actual: Prize ignored; cash negative.

IT-29: Ranking stability at zero wins  
Modules: registration, ranking  
Expected: Stable order. Actual: Arbitrary (ascending).

IT-30: Full crew lifecycle  
Modules: all  
Expected: Correct roles, damage/repair, prize, ranking, cash. Actual: Halved damage, role skips, prize ignored, ranking inverted, possible negative cash.

## Key Bugs Identified

**Registration Issues**  
- Duplicate members allowed.  
- Unregistered entrants accepted in races.

**Role Validation Issues**  
- Roles assignable to unregistered users.  
- Race ignores Driver-only rule.  
- Missions ignore required_roles.

**Inventory / Financial Issues**  
- Prizes not applied to cash.  
- Negative balances allowed; costs can exceed cash.

**Vehicle Health Issues**  
- Damage is halved, rarely reaches 0.  
- Health-based blocking/retirement unreliable.

**Ranking Issues**  
- Rankings sorted ascending instead of descending.  
- Zero-win ordering unstable.



## Conclusion

Integration testing revealed multiple critical issues in the system, particularly in enforcing business rules across modules. 

Key problems include:
- Lack of validation between dependent modules
- Incorrect financial updates
- Inconsistent vehicle state handling
- Incorrect ranking logic

These issues demonstrate the importance of integration testing in identifying defects that are not visible during isolated module testing.

The system requires fixes in validation logic, state management, and data consistency to function correctly as a unified application.