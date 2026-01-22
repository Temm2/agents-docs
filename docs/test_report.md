# RAMM Agent Test Report

**Generated:** 2026-01-22 16:20:27 UTC

## Test Summary

- **Logic Test Scenarios:** 16
- **Business Logic Tests:** 11
- **Graph Validation:** ✓ PASS

---

## Logic Tests (Agent Behavior)


### ✅ campaign_creation

**Score:** 14/14 (100.0%)

**Checks:**
- ✓ VALET receives campaign config
- ✓ VALET transitions to ACTIVE
- ✓ VALET → PROMO notification
- ✓ VALET → DASHB state update
- ✓ A2A call VALET → PROMO
- ✓ A2A call VALET → DASHB
- ✓ VALET → active
- ✓ Event keyword 'campaign' found
- ✓ Event keyword 'VALET' found
- ✓ Event keyword 'PROMO' found


### ✅ purchase_flow

**Score:** 24/24 (100.0%)

**Checks:**
- ✓ SHOPI recommends campaign
- ✓ SHOPI → MARKT swap request
- ✓ SHOPI → PAYME authorization
- ✓ SHOPI → FOLIO mint request
- ✓ FOLIO mints PVT
- ✓ PAYME settles escrow
- ✓ A2A call SHOPI → MARKT
- ✓ A2A call SHOPI → PAYME
- ✓ A2A call SHOPI → FOLIO
- ✓ FOLIO → active
- ✓ PAYME → settling
- ✓ Event keyword 'SHOPI' found
- ✓ Event keyword 'MARKT' found
- ✓ Event keyword 'PAYME' found
- ✓ Event keyword 'FOLIO' found
- ✓ Event keyword 'PVT' found


### ✅ redemption_flow

**Score:** 16/16 (100.0%)

**Checks:**
- ✓ FOLIO → RIDIM redemption request
- ✓ RIDIM → VALET validation
- ✓ RIDIM → PORTE DPP mint
- ✓ PORTE mints DPP
- ✓ A2A call FOLIO → RIDIM
- ✓ A2A call RIDIM → VALET
- ✓ A2A call RIDIM → PORTE
- ✓ PORTE → completed
- ✓ Event keyword 'RIDIM' found
- ✓ Event keyword 'PORTE' found
- ✓ Event keyword 'DPP' found


### ⚠️ unauthorized_command

**Score:** 8/9 (88.9%)

**Checks:**
- ✓ Auth check performed
- ✓ Unauthorized command rejected
- ✓ Event keyword 'auth' found
- ✓ Event keyword 'unauthorized' found
- ✗ Event keyword 'rejected' found
-   → Not found in timeline


### ⚠️ replay_attack

**Score:** 9/10 (90.0%)

**Checks:**
- ✓ Idempotency check performed
- ✓ Replay attack rejected
- ✓ A2A call SHOPI → FOLIO
- ✓ Event keyword 'idempotency' found
- ✓ Event keyword 'replay' found
- ✗ Event keyword 'rejected' found
-   → Not found in timeline


### ⚠️ race_condition_supply_limit

**Score:** 8/11 (72.7%)

**Checks:**
- ✓ Supply check performed
- ✓ Race condition handled
- ✗ A2A call SHOPI → MARKT
-   → Expected call not found in timeline
- ✗ A2A call SHOPI → FOLIO
-   → Expected call not found in timeline
- ✓ Event keyword 'concurrent' found
- ✓ Event keyword 'supply' found
- ✓ Event keyword 'limit' found
- ✗ Event keyword 'rejected' found
-   → Not found in timeline


### ⚠️ invalid_redemption_timing

**Score:** 10/12 (83.3%)

**Checks:**
- ✓ Timing validation performed
- ✓ Invalid timing rejected
- ✓ A2A call FOLIO → RIDIM
- ✓ A2A call RIDIM → VALET
- ✓ Event keyword 'redemption' found
- ✓ Event keyword 'timing' found
- ✗ Event keyword 'invalid' found
-   → Not found in timeline
- ✗ Event keyword 'rejected' found
-   → Not found in timeline


### ⚠️ boundary_zero_amount

**Score:** 8/10 (80.0%)

**Checks:**
- ✓ Amount validation performed
- ✓ Zero amount rejected
- ✓ A2A call SHOPI → PAYME
- ✓ Event keyword 'amount' found
- ✓ Event keyword 'zero' found
- ✗ Event keyword 'invalid' found
-   → Not found in timeline
- ✗ Event keyword 'rejected' found
-   → Not found in timeline


### ⚠️ double_redemption

**Score:** 9/10 (90.0%)

**Checks:**
- ✓ Redemption state tracked
- ✓ Double redemption rejected
- ✓ A2A call FOLIO → RIDIM
- ✓ Event keyword 'double' found
- ✓ Event keyword 'redemption' found
- ✗ Event keyword 'rejected' found
-   → Not found in timeline


### ⚠️ exceed_supply_limit

**Score:** 7/10 (70.0%)

**Checks:**
- ✓ Supply limit check performed
- ✓ Exceeded supply rejected
- ✗ A2A call SHOPI → MARKT
-   → Expected call not found in timeline
- ✓ A2A call SHOPI → FOLIO
- ✓ Event keyword 'supply' found
- ✗ Event keyword 'exceeded' found
-   → Not found in timeline
- ✗ Event keyword 'rejected' found
-   → Not found in timeline


### ⚠️ insufficient_balance

**Score:** 8/9 (88.9%)

**Checks:**
- ✓ Balance check performed
- ✓ Insufficient balance rejected
- ✓ A2A call SHOPI → PAYME
- ✓ Event keyword 'insufficient' found
- ✓ Event keyword 'balance' found
- ✗ Event keyword 'rejected' found
-   → Not found in timeline


### ⚠️ invalid_state_transition

**Score:** 8/10 (80.0%)

**Checks:**
- ✓ State machine validation performed
- ✓ Invalid transition rejected
- ✗ A2A call VALET → DASHB
-   → Expected call not found in timeline
- ✓ Event keyword 'state' found
- ✓ Event keyword 'transition' found
- ✓ Event keyword 'invalid' found
- ✗ Event keyword 'rejected' found
-   → Not found in timeline


### ⚠️ cross_campaign_contamination

**Score:** 9/10 (90.0%)

**Checks:**
- ✓ Campaign ID validation performed
- ✓ Campaign mismatch rejected
- ✓ A2A call FOLIO → RIDIM
- ✓ A2A call RIDIM → VALET
- ✓ Event keyword 'campaign' found
- ✓ Event keyword 'mismatch' found
- ✗ Event keyword 'rejected' found
-   → Not found in timeline


### ❌ partial_failure_recovery

**Score:** 5/10 (50.0%)

**Checks:**
- ✓ Partial failure detected
- ✓ Rollback executed
- ✗ A2A call SHOPI → FOLIO
-   → Expected call not found in timeline
- ✗ A2A call SHOPI → PAYME
-   → Expected call not found in timeline
- ✗ Event keyword 'rollback' found
-   → Not found in timeline
- ✗ Event keyword 'compensation' found
-   → Not found in timeline
- ✗ Event keyword 'recovery' found
-   → Not found in timeline


### ⚠️ immediate_redemption

**Score:** 10/11 (90.9%)

**Checks:**
- ✓ Immediate redemption timing handled
- ✓ Redemption succeeds
- ✓ A2A call FOLIO → RIDIM
- ✓ A2A call RIDIM → VALET
- ✓ A2A call RIDIM → PORTE
- ✓ PORTE → completed
- ✓ Event keyword 'redemption' found
- ✓ Event keyword 'immediate' found
- ✗ Event keyword 'success' found
-   → Not found in timeline


### ⚠️ concurrent_redemption

**Score:** 8/9 (88.9%)

**Checks:**
- ✓ Concurrent requests handled
- ✓ No state corruption
- ✓ A2A call FOLIO → RIDIM
- ✓ Event keyword 'concurrent' found
- ✓ Event keyword 'redemption' found
- ✗ Event keyword 'handled' found
-   → Not found in timeline


---

## Business Logic Tests (Calculations)

| Test Name | Description | Type | Result |
|-----------|-------------|------|--------|
| linear_curve_start | Linear bonding curve at start (0 supply) | bonding_curve | ✅ PASS |
| linear_curve_midpoint | Linear bonding curve at midpoint (50% sold) | bonding_curve | ✅ PASS |
| linear_curve_near_sellout | Linear bonding curve near sellout (90% sold) | bonding_curve | ✅ PASS |
| exponential_curve_start | Exponential bonding curve at start | bonding_curve | ✅ PASS |
| tier_1_reward | Tier 1 (lowest) reward calculation | reward | ✅ PASS |
| tier_3_reward | Tier 3 reward calculation | reward | ✅ PASS |
| attribution_reward | Attribution reward with direct and indirect sales | reward | ✅ PASS |
| simple_yield_30_days | Simple yield for 30 days at 5% APY | yield | ✅ PASS |
| compounding_yield_90_days | Compound yield for 90 days at 5% APY | yield | ✅ PASS |
| positive_roi | Campaign with positive ROI | roi | ✅ PASS |
| pvt_velocity_50_percent | PVT velocity at 50% sellout | roi | ✅ PASS |

---

## Graph Validation

✅ All checks passed

- All graph integrity checks passed.

---

## NANDA Protocol Compliance

❌ NANDA compliance issues found

- Edge PORTE → VALET: intent is 'unspecified', must be specified
- Edge PORTE → PROMO: intent is 'unspecified', must be specified
- Edge PORTE → RIDIM: intent is 'unspecified', must be specified
- Edge DASHB → VALET: intent is 'unspecified', must be specified
- Edge DASHB → MARKT: intent is 'unspecified', must be specified
- Edge DASHB → PROMO: intent is 'unspecified', must be specified
- Edge RIDIM → FOLIO: intent is 'unspecified', must be specified
- Edge MARKT → FOLIO: intent is 'unspecified', must be specified
- Edge SHOPI → PROMO: intent is 'unspecified', must be specified
- Edge SHOPI → VALET: intent is 'unspecified', must be specified
- Edge SHOPI → MIRO: intent is 'unspecified', must be specified
- Edge DASHC → VALET: intent is 'unspecified', must be specified
- Edge DASHC → PAYME: intent is 'unspecified', must be specified
- Edge DASHC → PROMO: intent is 'unspecified', must be specified
- Edge DASHC → FOLIO: intent is 'unspecified', must be specified
- Edge FOLIO → PAYME: intent is 'unspecified', must be specified
- Edge FOLIO → PROMO: intent is 'unspecified', must be specified
- Edge PROMO → VALET: intent is 'unspecified', must be specified
- Edge PROMO → PAYME: intent is 'unspecified', must be specified
- Edge PROMO → SHOPI: intent is 'unspecified', must be specified
- Edge PAYME → FOLIO: intent is 'unspecified', must be specified
- Edge PAYME → PROMO: intent is 'unspecified', must be specified
- Edge PAYME → SHOPI: intent is 'unspecified', must be specified
- Edge PAYME → VALET: intent is 'unspecified', must be specified
- Edge DEFIME → PAYME: intent is 'unspecified', must be specified
- Edge DEFIME → FOLIO: intent is 'unspecified', must be specified
- Edge ICP_ID → VALET: intent is 'unspecified', must be specified
- Edge ICP_ID → SHOPI: intent is 'unspecified', must be specified
- Edge ICP_ID → FOLIO: intent is 'unspecified', must be specified
- Edge ICP_ID → PAYME: intent is 'unspecified', must be specified
- Edge ICP_ID → PROMO: intent is 'unspecified', must be specified
- Edge ICP_ID → MARKT: intent is 'unspecified', must be specified
- Edge ICP_ID → RIDIM: intent is 'unspecified', must be specified
- Edge PAYOUT → DASHB: intent is 'unspecified', must be specified
- Edge PAYOUT → VALET: intent is 'unspecified', must be specified
- Edge MIRO → SHOPI: intent is 'unspecified', must be specified

---

## Notes

This report was generated automatically from the RAMM agent test suite.
