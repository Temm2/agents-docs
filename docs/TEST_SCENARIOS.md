# RAMM Agent Test Scenarios

## Overview

This document describes all test scenarios available for validating RAMM agent logic, state changes, and security.

## Test Categories

### 1. **Happy Path Scenarios** (Baseline Functionality)

#### `campaign_creation`
- **Purpose**: Validate campaign setup flow
- **Mock Data**: Campaign configuration
- **Validates**: VALET creates campaign → notifies PROMO/DASHB → transitions to ACTIVE
- **Threshold**: 80%
- **State Changes**: VALET (IDLE → ACTIVE)

#### `purchase_flow`
- **Purpose**: Validate end-to-end purchase flow
- **Mock Data**: Campaign + Shopper wallet
- **Validates**: SHOPI → MARKT swap → PAYME escrow → FOLIO PVT mint
- **Threshold**: 85%
- **State Changes**: FOLIO (IDLE → ACTIVE), PAYME (IDLE → SETTLING)

#### `redemption_flow`
- **Purpose**: Validate redemption flow
- **Mock Data**: Campaign + Wallet + PVT
- **Validates**: FOLIO → RIDIM → VALET validation → PORTE DPP mint
- **Threshold**: 80%
- **State Changes**: PORTE (IDLE → COMPLETED)

---

### 2. **Security & Attack Vector Tests**

#### `unauthorized_command`
- **Purpose**: Prevent unauthorized state mutations
- **Attack Vector**: Command execution without ICP_ID auth
- **Expected Behavior**: Command rejected before state change
- **Threshold**: 90%
- **Key Checks**: Auth check performed, unauthorized command rejected

#### `replay_attack`
- **Purpose**: Prevent duplicate state changes from replay
- **Attack Vector**: Reusing same command/nonce multiple times
- **Expected Behavior**: Idempotency check rejects replay
- **Threshold**: 85%
- **Key Checks**: Idempotency check, replay rejection

#### `race_condition_supply_limit`
- **Purpose**: Handle concurrent operations at supply limits
- **Attack Vector**: Simultaneous purchases exceeding supply
- **Expected Behavior**: One succeeds, others rejected
- **Threshold**: 80%
- **Key Checks**: Supply check, race condition handling

#### `invalid_redemption_timing`
- **Purpose**: Prevent redemptions outside valid window
- **Attack Vector**: Redemption before start or after end
- **Expected Behavior**: Timing validation rejects invalid attempts
- **Threshold**: 85%
- **Key Checks**: Timing validation, rejection of invalid timing

#### `boundary_zero_amount`
- **Purpose**: Validate transaction amounts
- **Attack Vector**: Zero or negative amounts
- **Expected Behavior**: Amount validation rejects invalid amounts
- **Threshold**: 90%
- **Key Checks**: Amount validation, zero amount rejection

#### `double_redemption`
- **Purpose**: Prevent same PVT being redeemed twice
- **Attack Vector**: Multiple redemption attempts for same PVT
- **Expected Behavior**: First succeeds, subsequent attempts rejected
- **Threshold**: 90%
- **Key Checks**: Redemption state tracking, double redemption rejection

#### `exceed_supply_limit`
- **Purpose**: Enforce campaign supply limits
- **Attack Vector**: Purchase exceeding total supply
- **Expected Behavior**: Supply check rejects exceeded purchases
- **Threshold**: 85%
- **Key Checks**: Supply limit check, exceeded supply rejection

#### `insufficient_balance`
- **Purpose**: Validate wallet balance before transactions
- **Attack Vector**: Purchase with insufficient funds
- **Expected Behavior**: Balance check rejects insufficient funds
- **Threshold**: 90%
- **Key Checks**: Balance check, insufficient balance rejection

#### `invalid_state_transition`
- **Purpose**: Enforce valid state machine transitions
- **Attack Vector**: Invalid phase transitions (e.g., COMPLETED → ACTIVE)
- **Expected Behavior**: State machine validation rejects invalid transitions
- **Threshold**: 85%
- **Key Checks**: State machine validation, invalid transition rejection

#### `cross_campaign_contamination`
- **Purpose**: Prevent operations with wrong campaign IDs
- **Attack Vector**: Using PVT from one campaign with another campaign
- **Expected Behavior**: Campaign ID validation rejects mismatches
- **Threshold**: 85%
- **Key Checks**: Campaign ID validation, mismatch rejection

---

### 3. **Resilience & Recovery Tests**

#### `partial_failure_recovery`
- **Purpose**: Handle partial failures gracefully
- **Scenario**: PVT minted but payment fails
- **Expected Behavior**: Rollback or compensation mechanism
- **Threshold**: 80%
- **Key Checks**: Partial failure detection, rollback execution

#### `immediate_redemption`
- **Purpose**: Handle edge case of immediate redemption window
- **Scenario**: Redemption window starts immediately
- **Expected Behavior**: Timing logic handles immediate start correctly
- **Threshold**: 80%
- **Key Checks**: Immediate timing handling, successful redemption

#### `concurrent_redemption`
- **Purpose**: Handle multiple concurrent redemption requests
- **Scenario**: Multiple PVTs redeemed simultaneously
- **Expected Behavior**: All processed without state corruption
- **Threshold**: 75%
- **Key Checks**: Concurrent request handling, no state corruption

---

## State Change Analysis

### State-Changing Operations (Commands)

| Operation | Agent | State Change | Irreversible |
|-----------|-------|--------------|--------------|
| Campaign config | VALET | IDLE → ACTIVE | No |
| PVT mint | FOLIO | IDLE → ACTIVE | Yes* |
| Escrow lock | PAYME | IDLE → SETTLING | No |
| DPP mint | PORTE | IDLE → COMPLETED | Yes |
| Fund disbursement | PAYOUT | IDLE → SETTLING | Yes |
| Redemption | RIDIM | IDLE → COMPLETED | Yes |

*PVT can be burned in rollback scenarios

### Non-State-Changing Operations (Queries/Events)

| Operation | Agent | Type | State Change |
|-----------|-------|------|--------------|
| Campaign validation | VALET | Query | No |
| Redemption validation | RIDIM → VALET | Query | No |
| Payout status | DASHB → PAYOUT | Query | No |
| Auth verification | * → ICP_ID | Query | No |
| Trade logging | MARKT → DASHB | Event | No (listener may mutate) |
| Analytics event | SHOPI → DASHC | Event | No (listener may mutate) |

---

## Running Tests

### CLI
```bash
python -m app.test_logic
```

### Dashboard
1. Go to "Logic Testing" tab
2. Click "Run all logic tests" for batch results
3. Or select individual scenario and click "Run [scenario_name]"

---

## Test Results Interpretation

- **PASS**: Score ≥ threshold, all critical checks passed
- **PARTIAL**: Score ≥ 70% but < threshold, some checks failed
- **FAIL**: Score < 70%, critical checks failed

### Scoring Breakdown
- **Critical checks**: 3 points each (auth, state transitions, security)
- **Important checks**: 2 points each (A2A calls, validations)
- **Standard checks**: 1 point each (event keywords, basic operations)

---

## Adding New Test Scenarios

1. Define mock data in `get_test_scenarios()`
2. Create `TestScenario` with:
   - `name`: Unique identifier
   - `description`: Human-readable description
   - `mock_data`: Dict of mock objects
   - `expected_a2a_calls`: List of (source, target) tuples
   - `expected_state_transitions`: Dict mapping agent_code → list of phases
   - `expected_events`: List of keywords to find in timeline
   - `min_score_threshold`: Minimum percentage to pass
3. Add simulation logic in `simulate_scenario()` for your scenario name
4. Add scoring checks using `score.add_check(name, passed, points, detail)`

---

## Coverage Summary

- ✅ **Happy Path**: 3 scenarios
- ✅ **Security**: 10 scenarios
- ✅ **Resilience**: 3 scenarios
- **Total**: 16 test scenarios

### Coverage Areas
- State mutations (commands)
- Read-only operations (queries)
- Attack vectors (unauthorized, replay, race conditions)
- Boundary conditions (zero amounts, supply limits)
- Error handling (partial failures, invalid states)
- Concurrent operations (race conditions, parallel requests)
