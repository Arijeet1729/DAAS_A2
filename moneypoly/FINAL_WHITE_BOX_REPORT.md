# MoneyPoly White-Box Testing Report

## 1. Control Flow Graph Explanation

### 1.1 Purpose of the CFG

A Control Flow Graph, or CFG, is used to understand how a program moves from one block of code to another during execution. In white-box testing, CFG analysis helps us identify:

- decision points such as `if`, `elif`, and loop conditions
- normal execution paths
- exceptional or edge-case paths
- places where state changes happen

For the MoneyPoly project, the CFG was especially useful because the game logic is state-based and interactive. Many important actions depend on previous state, such as:

- whether a player is in jail
- whether a property is owned or mortgaged
- whether a player has enough money
- which type of board tile or card action is reached

### 1.2 Main Control Centers in the Program

The system is structured around a few central components:

- `main.py` starts the game and collects player names
- `Game` controls turn flow and rule enforcement
- `Player` manages money, position, jail state, and owned properties
- `Board` determines tile types and purchasable positions
- `Bank` manages game funds, payouts, and collections
- `CardDeck` handles Chance and Community Chest cards

At a simplified level, the main program flow is:

`main -> Game.run -> Game.play_turn -> Game._move_and_resolve -> other helpers`

### 1.3 Important Function-Level Flow

The following functions were the most important for CFG analysis because they contained the most branches and state transitions:

#### `Game.play_turn`

This function controls one complete turn:

- gets the current player
- checks whether the player is in jail
- rolls dice
- checks for repeated doubles
- moves the player
- resolves the tile reached
- decides whether the player gets another turn or the game should advance

Important decision points:

- `if player.in_jail`
- `if self.dice.doubles_streak >= 3`
- `if self.dice.is_doubles()`

This function is the central dispatcher of the game.

#### `Game._move_and_resolve`

This function handles the result of movement:

- updates player position
- reads the tile type from the board
- applies the effect of that tile
- checks bankruptcy afterward

Important decision points:

- tile is `go_to_jail`
- tile is `income_tax`
- tile is `luxury_tax`
- tile is `free_parking`
- tile is `chance`
- tile is `community_chest`
- tile is `railroad`
- tile is `property`

This function has many branches because it connects board state to game rules.

#### `Game._handle_property_tile`

This function decides how property interaction works:

- unowned property can be bought, auctioned, or skipped
- owned-by-self property does nothing
- owned-by-other property causes rent payment

Important decision points:

- `if prop.owner is None`
- `if choice == "b"`
- `elif choice == "a"`
- `elif prop.owner == player`

#### `Game._apply_card`

This function applies card actions:

- collect money
- pay money
- go to jail
- get a jail-free card
- move to another tile
- collect money from other players

Important decision points:

- `if card is None`
- branch on `action`
- conditional transfers from other players based on affordability

This function was originally very branch-heavy and became an important target in both design review and later cleanup.

#### `Game._check_bankruptcy`

This function removes bankrupt players and cleans their state:

- checks if a player is bankrupt
- marks player as eliminated
- resets their properties
- removes them from the active player list
- updates turn index if needed

Important decision points:

- `if player.is_bankrupt()`
- `if player in self.players`
- `if self.current_index >= len(self.players)`

### 1.4 Why CFG Analysis Helped

The CFG work helped identify:

- missing validation paths
- incomplete branch handling
- incorrect state transitions
- code that looked correct for one path but failed on another

This was especially important for:

- exact-balance purchases
- pass-Go salary logic
- jail release handling
- card-driven movement
- player removal during bankruptcy
- auction flow

In short, the CFG analysis gave a map of the program behavior before tests were written.

## 2. Code Quality Analysis

### 2.1 Goal of the Analysis

Code quality analysis was performed using `pylint` principles. The focus was not only on style, but also on logic, maintainability, and clarity.

The issues were grouped into three categories:

- Critical: logic bugs or incorrect behavior
- Warning: risky design choices or maintainability problems
- Style: PEP8 and readability issues

### 2.2 Examples of Critical Problems Found

Several important logic problems were identified in the earlier codebase:

- `Player.move` gave salary only when landing exactly on Go, but not when passing it
- `Dice.roll` used `1..5` instead of `1..6`
- `Game.buy_property` rejected exact-balance purchases
- `Game.pay_rent` deducted rent from the tenant but did not credit the owner
- `PropertyGroup.all_owned_by` used `any()` instead of `all()`
- `Game.trade` did not credit the seller with cash
- `Game.find_winner` selected the minimum net worth player instead of the maximum
- `Bank.give_loan` did not reduce bank funds in earlier versions
- `CardDeck.cards_remaining` and `__repr__` could crash on empty decks
- `Game._handle_jail_turn` did not deduct the voluntary jail fine from the player in earlier code

These were not style issues; they affected actual gameplay correctness.

### 2.3 Examples of Warning-Level Problems

The warning-level issues were mainly about design:

- classes with too many attributes
- functions with too many branches
- use of a bare `except`
- dead or confusing code paths
- overloaded responsibilities in the `Game` class

One especially important design issue was the original `_apply_card` function, which had too many branches and mixed many types of behavior in one place. This made testing harder and increased the chance of mistakes.

### 2.4 Examples of Style Issues

The style issues included:

- missing module docstrings
- missing class and function docstrings
- unused imports
- line-length violations
- unnecessary parentheses
- unnecessary `else` after `return`
- missing final newline

These did not always break behavior, but they reduced clarity and lowered static-analysis quality.

### 2.5 Quality Improvement Result

After the iterative cleanup process:

- `pytest` coverage-expanded test suite passed
- `pylint --disable=import-error` reached `10.00/10`

This showed that the code became not only more correct, but also easier to read and maintain.

## 3. Test Case Design

### 3.1 White-Box Testing Strategy

The test design was built around white-box principles:

- cover every important branch
- include edge values
- include state-based behavior
- include invalid inputs
- test transitions between states

The main functions prioritized for test design were:

- `Player.add_money`
- `Player.deduct_money`
- `Player.move`
- `Bank.pay_out`
- `Board.is_purchasable`
- `Game.buy_property`
- `Game.pay_rent`
- `Game._apply_card`
- `Game._check_bankruptcy`

### 3.2 Normal Branch Tests

Normal tests checked expected valid behavior such as:

- adding positive money
- deducting valid money
- buying property when affordable
- rent payment with valid ownership
- collect and pay card behavior
- bankruptcy cleanup

These tests confirmed the normal flow.

### 3.3 Edge Case Tests

Edge case testing included:

- zero money
- zero payouts
- exact-balance purchase
- negative values
- empty decks
- large values
- players with insufficient funds
- multiple bankrupt players
- outbid players in auctions

Examples:

- `Bank.pay_out(0)`
- `Player.add_money(-1)`
- `Game.buy_property` with balance exactly equal to price
- `CardDeck([])` empty deck behavior
- birthday and collect-from-all cards where some players cannot pay

### 3.4 State-Based Tests

State-based tests were very important because this game changes state often:

- a player goes in and out of jail
- a property changes owner
- a property changes mortgage state
- a bankrupt player is removed from the game
- the turn index changes after removal
- the bank funds change after loans and payouts

These tests were not only checking return values. They also checked internal state after each operation.

### 3.5 Test Suite Structure

The final pytest suite was organized per module as required:

- `tests/test_player.py`
- `tests/test_bank.py`
- `tests/test_board.py`
- `tests/test_game.py`

This structure made the suite easier to understand and kept each file focused on one area of the system.

### 3.6 Why the Test Design Was Useful

The white-box test design was useful because it did not assume the code was correct. Instead, it directly targeted:

- each branch condition
- known weak areas
- rule boundaries
- state transitions
- hidden bugs in edge cases

This approach successfully exposed real defects that normal happy-path tests would likely miss.

## 4. Bugs Found & Fixes

### 4.1 Bug Discovery by Pytest

After the stronger pytest suite was created and run, several failures appeared. These were documented in `PYTEST_BUG_ANALYSIS.txt`.

The failing tests showed the following remaining bugs:

1. `Bank.collect` accepted negative values and reduced bank funds
2. `Game.buy_property` allowed direct purchase of a property already owned
3. `_apply_move_to_card` did not resolve special destination tiles like tax squares
4. `_check_bankruptcy` did not preserve turn order when an earlier player was removed
5. `Game.trade` did not reject negative cash amounts safely
6. `Game.auction_property` only supported a single pass and not repeated bidding rounds

These were important because they affected correctness under edge and stress scenarios.

### 4.2 How the Bugs Were Fixed

Each bug was fixed with a minimal change approach:

- no unrelated refactoring
- only the necessary lines changed
- behavior preserved except where the bug required correction

The fixes were documented in `PYTEST_BUG_FIXES.txt`.

#### Fix 1: `Bank.collect`

Old behavior:

- negative values changed bank funds

New behavior:

- negative values are ignored with an early return

#### Fix 2: `Game.buy_property`

Old behavior:

- an already owned property could still be bought directly

New behavior:

- function first checks `prop.owner is not None` and rejects the purchase

#### Fix 3: `Game._apply_move_to_card`

Old behavior:

- only property and railroad destinations were resolved

New behavior:

- special tiles such as income tax, luxury tax, go to jail, chance, and community chest are also resolved after movement

#### Fix 4: `Game._check_bankruptcy`

Old behavior:

- removing an earlier player could shift the current turn to the wrong person

New behavior:

- when a player before the current index is removed, the index is decremented before range correction

#### Fix 5: `Game.trade`

Old behavior:

- negative `cash_amount` values reached lower-level balance logic and caused exceptions

New behavior:

- negative trade amounts are rejected immediately with a clean `False` return

#### Fix 6: `Game.auction_property`

Old behavior:

- bidding happened in one pass only

New behavior:

- repeated rounds continue among active bidders until bidding settles

### 4.3 Verification After Fixes

After the fixes:

- the failing pytest cases were rerun
- all tests passed

Final result:

- `58 passed`

This showed that the discovered bugs were fixed successfully and that the fixes matched the intended game behavior defined by the tests.

## 5. Conclusion

This white-box testing exercise improved the MoneyPoly project in several important ways.

First, the CFG work made the control structure of the game clear. It highlighted where the most important decisions and state changes happen.

Second, the code quality analysis found both style problems and real logic bugs. Some issues were small readability problems, but several were serious gameplay errors.

Third, the test case design created a strong white-box test suite that covered:

- normal behavior
- branches
- edge values
- state transitions
- stress-style cases

Fourth, the stronger pytest suite exposed real hidden bugs that were not obvious from casual reading.

Finally, the bug-fix stage corrected those issues with minimal changes and verified the corrections through automated tests.

### Final Outcomes

- control flow understood
- code quality reviewed
- white-box test cases designed
- module-based pytest suite created
- remaining edge-case bugs identified
- targeted fixes applied
- final pytest result: `58 passed`
- final pylint result without import-error category: `10.00/10`

Overall, the project moved from partially correct game logic with hidden defects to a much more reliable, test-backed implementation. This process also produced useful documentation artifacts that can support maintenance, grading, and future extension of the project.
