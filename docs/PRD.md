# Product Requirements Document (PRD)
## RAMM Agents - Web3 Agentic E-Commerce Platform

**Version:** 1.0  
**Date:** January 2026  
**Status:** Based on Implementation Analysis

---

## Overview

RAMM Agents is a modular, agent-based architecture for Web3 commerce built on the Internet Computer (ICP). The system enables brands to launch tokenized commerce campaigns, shoppers to buy/promote/redeem products, and influencers to earn rewards, all coordinated through peer-to-peer (A2A) communication without a central orchestrator.

The system is implemented as a Python modeling framework that maps conceptually to ICP canisters, focusing on agent behavior, state transitions, and decision flows rather than low-level canister implementation details.

---

## Problem Statement

### Current State
- Traditional e-commerce platforms are centralized, limiting brand autonomy
- Influencer/affiliate attribution and reward systems are opaque and inefficient
- Product authenticity and sustainability tracking is fragmented
- Tokenized commerce campaigns lack standardized agent coordination

### Pain Points
1. **Brand Onboarding Complexity**: Brands need to manually configure campaigns, pricing, and bonding curves
2. **Shopper Experience Fragmentation**: Shoppers interact with multiple disconnected systems
3. **Influencer Attribution Challenges**: Attribution logic and reward distribution lack transparency
4. **State Management**: Multi-agent coordination requires robust state management and validation
5. **Security Vulnerabilities**: Unauthorized operations, replay attacks, and race conditions pose risks

### Solution
A decentralized agent-based system where:
- Each agent has clearly scoped responsibilities
- Agents communicate via structured A2A protocol (NANDA)
- State changes are validated and tracked
- All operations are authenticated via ICP_ID
- Business logic is deterministic and testable

---

## Goals and Non-Goals

### Goals

1. **Modular Agent Architecture**
   - Each agent is independently deployable (as ICP canister)
   - Agents communicate via structured A2A protocol
   - Clear separation of concerns (brand, shopper, finance, data, identity)

2. **Deterministic State Management**
   - All state transitions are validated
   - State-changing operations are authenticated
   - State machine rules are enforced

3. **Comprehensive Testing**
   - Logic tests validate agent behavior (16 scenarios)
   - Business logic tests validate calculations (11 tests)
   - Graph validation ensures network integrity

4. **Security & Compliance**
   - All commands require ICP_ID authentication
   - Replay attack prevention via idempotency
   - Race condition handling
   - Boundary condition validation

5. **Business Logic Correctness**
   - Bonding curve pricing (linear, exponential, logarithmic)
   - Reward calculations (tiered, attribution-based)
   - Yield calculations (simple, compound)
   - ROI metrics (campaign ROI, PVT velocity)

### Non-Goals

1. **Not a Full ICP Implementation**
   - This is a Python modeling framework
   - Actual ICP canister deployment is out of scope
   - Focus is on logic and behavior, not canister plumbing

2. **Not a Production System**
   - No real wallet integration
   - No actual blockchain transactions
   - Mock data only for testing

3. **Not a Complete Feature Set**
   - Some NANDA intents are "unspecified" (work in progress)
   - Not all edge cases are fully handled
   - Some agents have minimal implementation

4. **Not a User Interface**
   - No frontend implementation
   - Streamlit dashboard is for testing/visualization only
   - No production UI/UX

---

## Functional Requirements

### FR1: Agent Network Architecture

**Requirement:** The system must support 14 distinct agents with defined roles and responsibilities.

**Agents:**
- **VALET**: Campaign orchestrator, brand onboarding, AI-generated campaigns
- **SHOPI**: Shopping journey, personalization, product recommendations
- **MARKT**: Core AMM, manages swaps (USDC ↔ PVT), liquidity tracking
- **FOLIO**: PVT wallet management, redemption, gifting, reselling
- **PROMO**: Influencer & affiliate management, attribution logic
- **PAYME**: Escrow handling, payment execution, reward payouts
- **RIDIM**: PVT redemption orchestration, DPP minting coordination
- **PORTE**: Digital Product Passport (DPP) creation and NFT minting
- **DASHB**: Brand dashboard, campaign analytics, portfolio view
- **DASHC**: Shopper analytics, engagement metrics
- **DEFIME**: Yield management, DeFi integration
- **ICP_ID**: Identity and authentication layer
- **MIRO/BRAT**: Visual feedback agent for shoppers
- **PAYOUT**: Fund withdrawal and settlement

**Validation:** Graph integrity checks ensure all agents are reachable and have valid A2A edges.

---

### FR2: A2A Communication Protocol (NANDA)

**Requirement:** All agent-to-agent communication must use NANDA protocol structure.

**Structure:**
- `protocol`: Must be "NANDA"
- `performative`: One of: request, notify, query, respond, command, event
- `intent`: High-level intent name (e.g., `campaign.list_active`)
- `payload_contract`: Schema definition for message data

**Performative Types:**
- `query`: Read-only data requests (no state change)
- `request`: Ask for action (may mutate state)
- `command`: Direct action execution (state change)
- `notify`: Inform about state change (notification only)
- `respond`: Reply to query/request (no state change)
- `event`: Broadcast state change (event emission)

**Validation:** NANDA compliance validator checks all edges comply with protocol structure.

**Current Status:** 35 edges have "unspecified" intents (work in progress).

---

### FR3: State Management

**Requirement:** Agents must manage state transitions according to defined state machine.

**Agent Phases:**
- `IDLE`: Initial state, no active operations
- `CONFIGURING`: Setting up configuration
- `ACTIVE`: Active operations in progress
- `SETTLING`: Finalizing operations
- `COMPLETED`: Operation completed successfully
- `ERROR`: Error state (can transition from any phase)

**State-Changing Operations:**
- Campaign config (VALET: IDLE → ACTIVE)
- PVT mint (FOLIO: IDLE → ACTIVE)
- Escrow lock (PAYME: IDLE → SETTLING)
- DPP mint (PORTE: IDLE → COMPLETED)
- Fund disbursement (PAYOUT: IDLE → SETTLING)
- Redemption (RIDIM: IDLE → COMPLETED)

**Non-State-Changing Operations:**
- Campaign queries (read-only)
- Redemption validation (read-only)
- Auth verification (read-only)
- Analytics events (read-only from sender perspective)

**Validation:** Test scenarios validate state transitions match expected behavior.

---

### FR4: Authentication & Authorization

**Requirement:** All state-changing operations must be authenticated via ICP_ID.

**Flow:**
1. Agent wants to execute command
2. Agent → ICP_ID: `auth.verify_principal(principal)`
3. ICP_ID validates principal and role
4. If valid, command proceeds; if invalid, command rejected

**Critical Commands Requiring Auth:**
- PVT minting (FOLIO)
- Fund disbursement (PAYOUT/PAYME)
- DPP minting (PORTE)
- Campaign activation (VALET)

**Validation:** Security test scenarios verify unauthorized commands are rejected.

---

### FR5: Campaign Creation Flow

**Requirement:** Brands must be able to create tokenized commerce campaigns.

**Flow:**
1. Brand Manager → VALET: Campaign configuration
2. VALET validates configuration
3. VALET → PROMO: Notify campaign created
4. VALET → DASHB: State update
5. VALET transitions to ACTIVE

**Mock Data Required:**
- Campaign ID
- Brand ID
- Product name
- Target audience
- Price (USDC)
- Total supply
- Bonding curve type
- Redemption window (start/end)

**Validation:** `campaign_creation` test scenario validates flow.

---

### FR6: Purchase Flow

**Requirement:** Shoppers must be able to purchase PVTs through the marketplace.

**Flow:**
1. Shopper → SHOPI: Browse marketplace
2. SHOPI → VALET: Query active campaigns
3. VALET → SHOPI: Return campaign list
4. SHOPI personalizes recommendations
5. Shopper → SHOPI: Select campaign & buy
6. SHOPI → MARKT: Swap quote/execute (USDC → PVT)
7. SHOPI → PAYME: Authorize payment (escrow)
8. SHOPI → FOLIO: Request Buy(PVT)
9. FOLIO mints PVT to shopper wallet
10. PAYME settles escrow

**State Changes:**
- FOLIO: IDLE → ACTIVE (PVT minted)
- PAYME: IDLE → SETTLING (escrow locked)

**Validation:** `purchase_flow` test scenario validates end-to-end flow.

---

### FR7: Redemption Flow

**Requirement:** Shoppers must be able to redeem PVTs for products.

**Flow:**
1. Shopper → FOLIO: Request redemption
2. FOLIO → RIDIM: Redemption request
3. RIDIM → VALET: Validate redemption eligibility (timing, campaign state)
4. VALET → RIDIM: Validation response
5. RIDIM → PORTE: Mint DPP NFT
6. PORTE mints DPP with product/sustainability metadata
7. RIDIM → VALET: Request PromoCode
8. RIDIM finalizes redemption state
9. RIDIM → FOLIO: Confirmation

**State Changes:**
- PORTE: IDLE → COMPLETED (DPP minted)
- RIDIM: IDLE → COMPLETED (redemption completed)

**Validation:** `redemption_flow` test scenario validates flow.

---

### FR8: Business Logic Calculations

**Requirement:** System must correctly calculate pricing, rewards, yield, and ROI.

#### FR8.1: Bonding Curve Pricing

**Curve Types:**
- **Linear**: `price = base_price * (1 + supply_ratio)`
- **Exponential**: `price = base_price * (1 + k)^supply_ratio`
- **Logarithmic**: `price = base_price * (1 + k * log(1 + supply_ratio))`

**Cost Calculation:**
- For buying N PVTs: Integral under curve (exact for linear, approximation for others)

**Validation:** 4 business logic tests validate pricing calculations.

#### FR8.2: Reward Calculations

**Tier-Based Rewards:**
- Exponential scaling by tier level
- Formula: `reward = base_reward * (tier_multiplier ^ tier_level)`

**Attribution Rewards:**
- Direct sales: Full reward
- Indirect sales: Fractional reward based on attribution chain

**Performance Bonuses:**
- Score-based multiplier
- Formula: `bonus = base_reward * performance_score`

**Validation:** 3 business logic tests validate reward calculations.

#### FR8.3: Yield Calculations

**Simple Yield:**
- Formula: `yield = principal * rate * (days / 365)`

**Compound Yield:**
- Formula: `A = P * (1 + r/n)^(n*t)`
- APR to APY conversion supported

**Validation:** 2 business logic tests validate yield calculations.

#### FR8.4: ROI Metrics

**Campaign ROI:**
- Percentage: `(revenue - cost) / cost * 100`
- Multiplier: `revenue / cost`
- Daily ROI: `ROI / campaign_days`
- Break-even days: `cost / daily_revenue`

**PVT Velocity:**
- Sellout rate: `current_supply / total_supply`
- Daily sales rate: `sales / days_active`
- Projected sellout days: `remaining_supply / daily_sales_rate`

**Validation:** 2 business logic tests validate ROI calculations.

---

### FR9: Security Requirements

**Requirement:** System must prevent unauthorized operations, replay attacks, and race conditions.

#### FR9.1: Unauthorized Command Prevention

**Validation:**
- Commands without ICP_ID auth must be rejected
- All state-changing operations require auth check

**Test:** `unauthorized_command` scenario validates rejection.

#### FR9.2: Replay Attack Prevention

**Validation:**
- Same command/nonce reused multiple times must be rejected
- Idempotency check required

**Test:** `replay_attack` scenario validates rejection.

#### FR9.3: Race Condition Handling

**Validation:**
- Concurrent operations at supply limits must be handled
- One succeeds, others rejected

**Test:** `race_condition_supply_limit` scenario validates handling.

#### FR9.4: Boundary Condition Validation

**Validation:**
- Zero/negative amounts rejected
- Exceeding max supply rejected
- Invalid state transitions rejected

**Tests:**
- `boundary_zero_amount`
- `exceed_supply_limit`
- `invalid_state_transition`

#### FR9.5: Double-Spending Prevention

**Validation:**
- Same PVT redeemed multiple times must be rejected
- First succeeds, subsequent attempts rejected

**Test:** `double_redemption` scenario validates prevention.

#### FR9.6: Timing Validation

**Validation:**
- Redemption before start or after end must be rejected
- Timing validation required

**Test:** `invalid_redemption_timing` scenario validates rejection.

#### FR9.7: Balance Validation

**Validation:**
- Purchase with insufficient funds must be rejected
- Balance check required before transactions

**Test:** `insufficient_balance` scenario validates rejection.

#### FR9.8: Campaign Isolation

**Validation:**
- Operations with wrong campaign IDs must be rejected
- Campaign ID validation required

**Test:** `cross_campaign_contamination` scenario validates isolation.

---

### FR10: Resilience Requirements

**Requirement:** System must handle partial failures and concurrent operations gracefully.

#### FR10.1: Partial Failure Recovery

**Validation:**
- PVT minted but payment fails must trigger rollback or compensation
- Partial failure detection required

**Test:** `partial_failure_recovery` scenario validates recovery.

#### FR10.2: Immediate Redemption Handling

**Validation:**
- Redemption window starting immediately must be handled correctly
- Timing logic must support immediate start

**Test:** `immediate_redemption` scenario validates handling.

#### FR10.3: Concurrent Operation Handling

**Validation:**
- Multiple concurrent redemption requests must be processed without state corruption
- Concurrent request handling required

**Test:** `concurrent_redemption` scenario validates handling.

---

### FR11: Graph Integrity

**Requirement:** Agent network must be well-formed and reachable.

**Checks:**
1. **No Missing Nodes**: All A2A edges reference existing agents
2. **No Isolated Agents**: Every agent has at least one incoming or outgoing edge
3. **Reachability**: All agents are reachable from entry points (VALET for brands, SHOPI for shoppers)

**Validation:** Graph validation checks ensure network integrity.

---

### FR12: Test Reporting

**Requirement:** System must generate comprehensive test reports.

**Report Contents:**
- Logic test results (16 scenarios)
- Business logic test results (11 calculations)
- Graph validation results
- NANDA protocol compliance results
- SHOPI-VALET connection details

**Formats:**
- HTML (self-contained, shareable)
- Markdown (documentation)

**Validation:** Report generator creates reports with all test results.

---

## Non-Functional Requirements

### NFR1: Testability

**Requirement:** All agent logic must be testable with mock data.

**Implementation:**
- Mock data structures (MockCampaign, MockWallet, MockPVT)
- Test scenarios with expected outcomes
- Scoring system for validation

**Metrics:**
- 16 logic test scenarios
- 11 business logic tests
- All tests must be runnable without external dependencies

---

### NFR2: Documentation

**Requirement:** System must be well-documented for understanding and maintenance.

**Documentation Types:**
- README with overview and quickstart
- Implementation summary
- Test guide for beginners
- Test scenarios documentation
- State analysis
- NANDA/ICP references

**Accessibility:**
- GitHub Pages hosting
- All documentation accessible via web

---

### NFR3: Visualization

**Requirement:** System must provide visualizations of agent network and flows.

**Visualizations:**
- Agent interaction graph (NetworkX + Matplotlib)
- Mermaid flowcharts
- Sequence diagrams
- Streamlit dashboard for interactive exploration

**Tools:**
- NetworkX for graph modeling
- Matplotlib for static visualizations
- Mermaid for diagram generation
- Streamlit for interactive dashboard

---

### NFR4: Code Quality

**Requirement:** Code must follow Python best practices and use type hints.

**Standards:**
- Pydantic models for data validation
- Type hints throughout
- Enum classes for constants
- Modular structure (one file per concern)

**Validation:**
- Linter checks (implicit via code structure)
- Type checking via Pydantic

---

### NFR5: Extensibility

**Requirement:** System must be extensible for new agents and scenarios.

**Extension Points:**
- Add new agents via `ramm_agents()` function
- Add new A2A edges via `ramm_edges()` function
- Add new test scenarios via `get_test_scenarios()` function
- Add new business logic via `business_logic.py`

**Validation:** Modular structure supports extensions.

---

## Edge Cases and Constraints

### EC1: Supply Limits

**Constraint:** Purchases cannot exceed total supply.

**Handling:**
- Supply check before PVT mint
- Rejection if supply exceeded
- Race condition handling for concurrent purchases

**Test:** `exceed_supply_limit`, `race_condition_supply_limit`

---

### EC2: Redemption Timing

**Constraint:** Redemptions only valid within redemption window.

**Handling:**
- Timing validation before redemption
- Rejection if outside window
- Support for immediate start window

**Test:** `invalid_redemption_timing`, `immediate_redemption`

---

### EC3: Zero/Negative Amounts

**Constraint:** Transaction amounts must be positive.

**Handling:**
- Amount validation before transactions
- Rejection of zero/negative amounts

**Test:** `boundary_zero_amount`

---

### EC4: Insufficient Balance

**Constraint:** Purchases require sufficient wallet balance.

**Handling:**
- Balance check before transactions
- Rejection if insufficient funds

**Test:** `insufficient_balance`

---

### EC5: Double Redemption

**Constraint:** Same PVT cannot be redeemed multiple times.

**Handling:**
- Redemption state tracking
- Rejection of duplicate redemptions

**Test:** `double_redemption`

---

### EC6: Invalid State Transitions

**Constraint:** Agents must follow valid state machine transitions.

**Handling:**
- State machine validation
- Rejection of invalid transitions

**Test:** `invalid_state_transition`

---

### EC7: Cross-Campaign Contamination

**Constraint:** Operations must use correct campaign IDs.

**Handling:**
- Campaign ID validation
- Rejection of mismatched IDs

**Test:** `cross_campaign_contamination`

---

### EC8: Partial Failures

**Constraint:** Multi-agent flows may fail partially.

**Handling:**
- Partial failure detection
- Rollback or compensation mechanism

**Test:** `partial_failure_recovery`

---

### EC9: Concurrent Operations

**Constraint:** Multiple operations may occur simultaneously.

**Handling:**
- Concurrent request handling
- State corruption prevention

**Test:** `concurrent_redemption`, `race_condition_supply_limit`

---

### EC10: Unspecified NANDA Intents

**Constraint:** Some A2A edges have "unspecified" intents.

**Current Status:** 35 edges need intent specification.

**Handling:**
- NANDA validator flags unspecified intents
- Work in progress to specify all intents

---

## Success Metrics

### SM1: Test Coverage

**Metric:** Percentage of test scenarios passing.

**Target:** ≥ 85% pass rate for all test scenarios.

**Current Status:**
- Logic tests: 16 scenarios (mix of PASS/PARTIAL/FAIL)
- Business logic tests: 11/11 passing (100%)
- Graph validation: All checks passing
- NANDA compliance: 35 edges need intent specification

---

### SM2: Graph Integrity

**Metric:** All graph validation checks passing.

**Target:** 100% of checks passing.

**Checks:**
- No missing nodes
- No isolated agents
- Full reachability

**Current Status:** All checks passing.

---

### SM3: Business Logic Correctness

**Metric:** All business logic calculations correct.

**Target:** 100% of business logic tests passing.

**Tests:**
- Bonding curves: 4/4 passing
- Rewards: 3/3 passing
- Yield: 2/2 passing
- ROI: 2/2 passing

**Current Status:** 11/11 passing (100%).

---

### SM4: Security Test Coverage

**Metric:** All security scenarios tested.

**Target:** 10 security scenarios implemented and tested.

**Scenarios:**
- Unauthorized command
- Replay attack
- Race conditions
- Boundary conditions
- Double-spending
- Timing attacks
- Balance validation
- State transition validation
- Campaign isolation
- Invalid redemption timing

**Current Status:** 10 security scenarios implemented.

---

### SM5: Documentation Completeness

**Metric:** All key documentation files present.

**Target:** 8 core documentation files.

**Files:**
- README.md
- IMPLEMENTATION_SUMMARY.md
- TESTING.md
- TEST_SCENARIOS.md
- STATE_ANALYSIS.md
- TEST_GUIDE.md
- SHOPI_VALET_CONNECTION.md
- NANDA_ICP_REFERENCES.md

**Current Status:** All files present.

---

### SM6: NANDA Compliance

**Metric:** Percentage of A2A edges with specified intents.

**Target:** 100% of edges with specified intents.

**Current Status:** ~65% compliance (35 edges need specification).

---

## Implementation Notes

### Technology Stack

- **Language**: Python 3
- **Network Target**: Internet Computer (ICP) - conceptual mapping
- **Libraries**:
  - `networkx`: Agent network modeling
  - `matplotlib`: Graph visualizations
  - `pydantic`: Data validation
  - `rich`: Console output formatting
  - `streamlit`: Interactive dashboard

### Architecture Decisions

1. **Python-First Modeling**: Focus on logic/behavior, not canister implementation
2. **NANDA Protocol**: Structured A2A communication for testability
3. **Mock Data Testing**: Test logic without external dependencies
4. **Scoring System**: Quantitative validation of test scenarios
5. **Graph Validation**: Ensure network integrity before deployment

### Known Limitations

1. **Incomplete NANDA Compliance**: 35 edges have unspecified intents
2. **Mock Data Only**: No real wallet/blockchain integration
3. **Python Model Only**: Not actual ICP canister deployment
4. **Limited Error Handling**: Some edge cases may not be fully handled
5. **No Performance Testing**: Focus is on logic, not performance

---

## Appendix

### A. Test Scenarios Summary

**Happy Path (3):**
- campaign_creation
- purchase_flow
- redemption_flow

**Security (10):**
- unauthorized_command
- replay_attack
- race_condition_supply_limit
- invalid_redemption_timing
- boundary_zero_amount
- double_redemption
- exceed_supply_limit
- insufficient_balance
- invalid_state_transition
- cross_campaign_contamination

**Resilience (3):**
- partial_failure_recovery
- immediate_redemption
- concurrent_redemption

### B. Agent Roles

- **Brand-Facing**: VALET, PORTE, DASHB, PROMO
- **Shopper-Facing**: SHOPI, DASHC, FOLIO, RIDIM, MIRO
- **Finance**: MARKT, PAYME, DEFIME, PAYOUT
- **Data**: DASHB, DASHC
- **Identity**: ICP_ID
- **Utility**: MIRO/BRAT

### C. State Change Matrix

| Agent | State-Changing | Non-State-Changing |
|-------|----------------|---------------------|
| VALET | Campaign config | Campaign queries |
| SHOPI | Purchase auth | Campaign queries |
| FOLIO | PVT mint/transfer | Portfolio queries |
| PAYME | Escrow lock/release | Balance queries |
| RIDIM | Redemption state | Redemption validation |
| PORTE | DPP NFT mint | DPP template queries |
| MARKT | Swap execution | Swap quotes |
| ICP_ID | None | Principal verification |

---

**Document Status:** Based on implementation analysis of code and tests as of January 2026.  
**Next Review:** When NANDA compliance reaches 100% or new agents are added.
