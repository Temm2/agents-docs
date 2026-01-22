# RAMM Agent State Change & Security Analysis

## State-Changing vs Non-State-Changing Operations

### State-Changing Operations (Mutations)

**Performative: `command`** - Direct state mutations:
- `VALET → PAYME`: `campaign.funding.configure` - Configures escrow pool
- `VALET → FOLIO`: `campaign.assets.register` - Registers PVT rules
- `SHOPI → FOLIO`: `folio.buy_or_sell` - Mints/transfers PVT tokens
- `SHOPI → PAYME`: `payme.authorize` - Locks funds in escrow
- `FOLIO → RIDIM`: `redeem.request` - Initiates redemption state machine
- `RIDIM → PORTE`: `dpp.mint` - Mints DPP NFT (irreversible)
- `PAYME → DEFIME`: `defi.route.locked_funds` - Moves funds to DeFi
- `PAYOUT → PAYME`: `payme.disburse` - Transfers funds to brand

**State Transitions** (AgentPhase changes):
- `IDLE → CONFIGURING → ACTIVE → SETTLING → COMPLETED`
- `* → ERROR` (any phase can error)

### Non-State-Changing Operations (Read-Only)

**Performative: `query`** - Pure reads:
- `RIDIM → VALET`: `campaign.redemption.validate` - Checks redemption eligibility
- `DASHB → PAYOUT`: `payout.status` - Reads payout state
- `* → ICP_ID`: `auth.verify_principal` - Validates permissions (no state change)

**Performative: `request`** - May be read-only or mutate:
- `SHOPI → MARKT`: `market.swap.quote_or_execute` - Quote is read-only, execute mutates

**Performative: `event`** - Informational broadcasts (listeners may mutate):
- `VALET → DASHB`: `campaign.state.updated` - DASHB updates its view (read-only from VALET's perspective)
- `MARKT → DASHB`: `market.trade.logged` - DASHB appends to log (read-only from MARKT's perspective)
- `SHOPI → DASHC`: `analytics.shopper.action` - DASHC updates metrics (read-only from SHOPI's perspective)
- `MARKT → PAYOUT`: `pool.settlement.trigger` - PAYOUT may mutate settlement state

**Performative: `notify`** - Informational (may trigger side effects):
- `VALET → PROMO`: `campaign.created` - PROMO may generate content (side effect, not direct mutation)

---

## Exposure & Attack Factors

### 1. **Unauthorized State Mutations**
- **Risk**: Commands executed without proper auth checks
- **Vectors**: 
  - Bypassing ICP_ID verification
  - Forged principal/role claims
  - Missing authorization checks before state changes
- **Critical Commands**: PVT minting, fund disbursement, DPP minting

### 2. **Replay Attacks**
- **Risk**: Reusing old commands to duplicate state changes
- **Vectors**:
  - Re-minting PVTs with same transaction
  - Re-redeeming same PVT multiple times
  - Re-disbursing funds
- **Mitigation Needed**: Nonce/timestamp validation, idempotency keys

### 3. **Race Conditions**
- **Risk**: Concurrent operations corrupting state
- **Vectors**:
  - Simultaneous PVT purchases exceeding supply
  - Concurrent redemption requests for same PVT
  - Parallel fund withdrawals
- **Critical Areas**: FOLIO (PVT registry), PAYME (escrow), MARKT (swap execution)

### 4. **Invalid State Transitions**
- **Risk**: Agents moving to illegal states
- **Vectors**:
  - Redemption before campaign starts
  - Redemption after campaign ends
  - PVT minting after sell-out
  - Disbursement before settlement conditions met
- **Critical**: RIDIM redemption state machine, PAYOUT settlement logic

### 5. **Boundary Condition Attacks**
- **Risk**: Edge cases causing unexpected behavior
- **Vectors**:
  - Zero-amount transactions
  - Negative amounts
  - Exceeding max supply
  - Expired campaign operations
  - Invalid wallet addresses
- **Critical**: MARKT (swap math), FOLIO (supply limits), PAYME (amount validation)

### 6. **Double-Spending**
- **Risk**: Same asset used multiple times
- **Vectors**:
  - PVT used for multiple redemptions
  - Funds withdrawn multiple times
  - DPP minted multiple times for same PVT
- **Critical**: RIDIM redemption tracking, PAYOUT disbursement logs

### 7. **Timing Attacks**
- **Risk**: Exploiting time-based logic
- **Vectors**:
  - Redemption window manipulation
  - Campaign start/end time manipulation
  - Settlement condition timing
- **Critical**: VALET campaign timing, RIDIM redemption windows

### 8. **Data Exposure**
- **Risk**: Unauthorized access to sensitive data
- **Vectors**:
  - Querying other users' portfolios
  - Accessing brand financial data
  - Reading campaign configs without permission
- **Critical**: FOLIO portfolio queries, DASHB brand data, PAYME balance queries

### 9. **Escrow Manipulation**
- **Risk**: Unauthorized fund movement
- **Vectors**:
  - Bypassing escrow for direct transfers
  - Premature fund release
  - Incorrect escrow calculations
- **Critical**: PAYME escrow logic, DEFIME routing

### 10. **State Corruption Recovery**
- **Risk**: No rollback mechanism for failed operations
- **Vectors**:
  - Partial state updates (e.g., PVT minted but payment failed)
  - Inter-canister call failures mid-flow
  - Network partitions causing inconsistent state
- **Critical**: Multi-agent flows (purchase, redemption)

---

## Recommended Additional Test Scenarios

### Security & Attack Vector Tests

1. **Unauthorized Command Execution**
   - Attempt commands without ICP_ID auth
   - Verify all state-changing operations require auth

2. **Replay Attack Prevention**
   - Replay same command multiple times
   - Verify idempotency or rejection

3. **Race Condition Detection**
   - Concurrent PVT purchases at supply limit
   - Concurrent redemption requests
   - Verify atomicity or proper locking

4. **Invalid State Transition Prevention**
   - Redemption before campaign start
   - Redemption after campaign end
   - Operations on completed campaigns

5. **Boundary Condition Validation**
   - Zero/negative amounts
   - Exceeding max supply
   - Invalid wallet addresses
   - Expired campaign operations

6. **Double-Spending Prevention**
   - Multiple redemptions of same PVT
   - Multiple fund withdrawals
   - Verify single-use tracking

### State Consistency Tests

7. **Partial Failure Recovery**
   - PVT minted but payment fails
   - DPP minted but redemption fails
   - Verify rollback or compensation

8. **Concurrent Operation Consistency**
   - Multiple agents updating same state
   - Verify eventual consistency or conflict resolution

9. **State Machine Integrity**
   - Invalid phase transitions
   - Missing required phases
   - Verify state machine rules

### Edge Case Tests

10. **Zero-Supply Campaign**
    - Campaign with 0 total supply
    - Verify graceful handling

11. **Immediate Redemption**
    - Redemption window starts immediately
    - Verify timing logic

12. **Maximum Supply Purchase**
    - Purchase exactly at supply limit
    - Verify boundary handling

13. **Empty Wallet Operations**
    - Operations with insufficient balance
    - Verify proper error handling

14. **Cross-Campaign Contamination**
    - Operations mixing campaign IDs
    - Verify isolation

### Integration Tests

15. **Multi-Agent Flow Integrity**
    - Full purchase flow with all agents
    - Full redemption flow with all agents
    - Verify end-to-end state consistency

16. **Error Propagation**
    - Error in one agent propagates correctly
    - Verify error handling doesn't corrupt state

17. **Timeout Handling**
    - Inter-agent call timeouts
    - Verify timeout recovery

---

## State Change Matrix

| Agent | State-Changing Operations | Non-State-Changing Operations |
|-------|--------------------------|------------------------------|
| VALET | Campaign config, funding setup | Campaign queries |
| SHOPI | Purchase authorization | Campaign queries, recommendations |
| FOLIO | PVT mint/transfer | Portfolio queries |
| PAYME | Escrow lock/release, disbursement | Balance queries |
| RIDIM | Redemption state machine | Redemption validation queries |
| PORTE | DPP NFT minting | DPP template queries |
| MARKT | Swap execution | Swap quotes |
| PROMO | Content generation (side effect) | Campaign queries |
| DASHB | Metrics aggregation (append-only) | Analytics queries |
| DASHC | Metrics aggregation (append-only) | Analytics queries |
| PAYOUT | Fund disbursement | Payout status queries |
| DEFIME | Fund routing | Yield calculation queries |
| ICP_ID | None (pure auth layer) | Principal verification |

---

## Critical State Change Points

1. **PVT Minting** (FOLIO) - Irreversible token creation
2. **Fund Escrow** (PAYME) - Locking user funds
3. **DPP Minting** (PORTE) - Irreversible NFT creation
4. **Redemption Completion** (RIDIM) - Consuming PVT
5. **Fund Disbursement** (PAYOUT/PAYME) - Transferring funds
6. **Campaign Activation** (VALET) - Making campaign live

All of these require:
- ✅ Authorization checks (ICP_ID)
- ✅ Idempotency/nonce validation
- ✅ Boundary condition checks
- ✅ State machine validation
- ✅ Atomicity guarantees (or rollback)
