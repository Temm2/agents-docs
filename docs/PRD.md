# Product Requirements Document (PRD)
## RAMM Agents - Web3 Agentic E-Commerce Platform

**Version:** 1.0  
**Date:** January 2026  
**Status:** Based on Implementation Analysis

---

## Overview

RAMM Agents is a modular, agent-based architecture for Web3 commerce designed to be **protocol-agnostic** in its core logic, with deployment options across multiple blockchain protocols. The system enables brands to launch tokenized commerce campaigns, shoppers to buy/promote/redeem products, and influencers to earn rewards, all coordinated through peer-to-peer (A2A) communication without a central orchestrator.

### Protocol-Agnostic Core

The Python modeling framework is **protocol-agnostic**, focusing on:
- **Agent behavior and logic** (testable across all protocols)
- **State transitions and decision flows** (independent of deployment target)
- **Business rules and calculations** (bonding curves, rewards, ROI)
- **A2A communication patterns** (NANDA protocol structure)

**All agent tests (16 logic scenarios + 14 business logic tests) are protocol-agnostic and validate the core system behavior regardless of deployment target.**

### Multi-Protocol Deployment Strategy

The system can be deployed on multiple blockchain protocols, each with protocol-specific implementation considerations:

1. **Internet Computer (ICP)** - Canister-based deployment
2. **Base** - Smart contract deployment on Ethereum L2
3. **Optimism** - Smart contract deployment on Ethereum L2
4. **Any L2** - General Layer 2 deployment considerations

Protocol-specific deployment details are documented in the Appendices (A-D). The core agent logic, NANDA protocol structure, and Python tests remain invariant across all protocols.

### Architecture Model

The system is implemented as a Python modeling framework that maps conceptually to protocol-specific deployment units:
- **Core Logic**: Agent behavior, state machines, business logic (protocol-agnostic, tested in Python)
- **Protocol Adapter**: Protocol-specific implementation layer (see Protocol Abstraction Layer section)
- **Deployment Units**: Canisters (ICP), Smart Contracts (L2s), etc. (protocol-specific)

The Python framework focuses on agent behavior, state transitions, and decision flows, providing a testable model before protocol-specific deployment.

### Native Token: $RAMM

**$RAMM** is the native utility token of the RAMM Agents ecosystem, deployed on Base. It serves as a primary medium of exchange for transactions across the platform.

**Supported Currencies:**
- **$RAMM**: Native utility token (primary)
- **USDC**: USD Coin (Base protocol native)
- **USDT**: Tether (stablecoin)
- **Fiat**: Traditional currency support (via payment processors)

**$RAMM Usage:**
- **PAYME**: Can process payments in fiat, stablecoins (USDC/USDT), or $RAMM
- **PAYOUT**: Can disburse funds to brands in fiat, stablecoins (USDC/USDT), or $RAMM
- **DEFIME**: Can generate yield in $RAMM (in addition to other assets)
- **MARKT**: AMM supports swaps involving $RAMM, USDC, USDT, and PVTs
- **LOYLT**: Loyalty tokens can be redeemed for $RAMM or used for partial payments

**Token Standards:**
- **Base Deployment**: ERC-20 standard for $RAMM, USDC, USDT
- **PVTs**: ERC-20 for Product Value Tokens
- **DPP NFTs**: ERC-721/1155 for Digital Product Passports

---

## Problem Statement

### Current State
- Traditional e-commerce platforms are centralized, limiting brand autonomy and creating vendor lock-in
- Cloud infrastructure is vulnerable to attacks and downtime
- Influencer/affiliate attribution and reward systems are opaque and inefficient
- Product authenticity and sustainability tracking is fragmented
- Tokenized commerce campaigns lack standardized agent coordination
- Multi-chain token operations require complex integrations

### Pain Points
1. **Brand Onboarding Complexity**: Brands need to manually configure campaigns, pricing, and bonding curves
2. **Shopper Experience Fragmentation**: Shoppers interact with multiple disconnected systems
3. **Influencer Attribution Challenges**: Attribution logic and reward distribution lack transparency
4. **State Management**: Multi-agent coordination requires robust state management and validation
5. **Security Vulnerabilities**: Unauthorized operations, replay attacks, and race conditions pose risks

### Solution
A decentralized agent-based system deployable across multiple blockchain protocols where:
- **Core Logic**: Protocol-agnostic agent behavior, state machines, and business rules (tested in Python)
- **Protocol Abstraction**: Protocol adapter layer defines required capabilities (see Protocol Abstraction Layer)
- **Protocol-Specific Deployment**: Implementation details vary by protocol (see Appendices A-D)
- Agents communicate via structured A2A protocol (NANDA) using protocol-specific mechanisms
- State persistence handled by protocol-native storage
- All operations authenticated via protocol-native identity systems
- Business logic is deterministic and testable before protocol deployment
- Multi-chain token operations enabled via protocol-specific bridges/technologies
- Self-writing AI capabilities for dynamic campaign generation (VALET agent)
- Protocol-native security features

---

## Goals and Non-Goals

### Goals

1. **Modular Agent Architecture (Protocol-Agnostic)**
   - Each agent is independently deployable (as canister, contract, etc. depending on protocol)
   - Agents communicate via structured A2A protocol (NANDA)
   - Clear separation of concerns (brand, shopper, finance, data, identity)
   - Protocol-native isolation and security
   - State persistence across upgrades (protocol-specific mechanism)

2. **Deterministic State Management (Protocol-Agnostic)**
   - All state transitions are validated (tested in Python)
   - State-changing operations are authenticated (protocol-specific mechanism)
   - State machine rules are enforced (protocol-specific enforcement)
   - Data integrity ensured (protocol-specific guarantees)
   - State persists across upgrades (protocol-specific persistence)

3. **Comprehensive Testing (Protocol-Agnostic)**
   - Logic tests validate agent behavior (16 scenarios - all passing)
   - Business logic tests validate calculations (14 tests - all passing)
   - Graph validation ensures network integrity
   - NANDA compliance validation

4. **Security & Compliance (Protocol-Agnostic Logic, Protocol-Specific Enforcement)**
   - All commands require authentication (protocol-specific mechanism)
   - Protocol-native tamperproof execution
   - Replay attack prevention via idempotency and nonce validation
   - Race condition handling with protocol-native atomicity
   - Boundary condition validation enforced at execution layer
   - Protocol-native uptime and execution guarantees

5. **Business Logic Correctness (Protocol-Agnostic)**
   - Bonding curve pricing (linear, exponential, logarithmic)
   - Reward calculations (tiered, attribution-based)
   - Yield calculations (simple, compound)
   - ROI metrics (campaign ROI, PVT velocity)

### Non-Goals

1. **Not a Full Protocol Implementation (Current Phase)**
   - This is a Python modeling framework for testing logic and behavior
   - Actual protocol deployment (canisters/contracts) is the next phase
   - Focus is on validating agent logic, state transitions, and business rules before protocol deployment
   - Python model serves as specification for protocol implementation

2. **Not a Production System (Yet)**
   - No real wallet integration (uses mock data)
   - No actual blockchain transactions (simulated)
   - Mock data only for testing agent logic
   - Production deployment requires protocol-specific implementation

3. **Not a Complete Feature Set**
   - All NANDA intents are now specified (100% compliance achieved)
   - Not all edge cases are fully handled in Python model
   - Some agents have minimal implementation (focus on core flows)

4. **Not a User Interface**
   - No frontend implementation
   - Streamlit dashboard is for testing/visualization only
   - Production UI/UX will be built on protocol-native hosting

---

## Functional Requirements

### FR1: Agent Network Architecture (Protocol-Agnostic)

**Requirement:** The system must support 15 distinct agents with defined roles and responsibilities. The agent logic is protocol-agnostic, but deployment architecture varies by protocol (see Protocol Abstraction Layer and Appendices).

**Protocol-Agnostic Agent Definitions:**

**Agent Details:**
- **VALET**: Campaign orchestrator, brand onboarding, AI-generated campaigns (main agent)
- **PORTE**: Digital Product Passport (DPP) creation and NFT minting (VALET sub-agent)
- **DASHB**: Brand dashboard, campaign analytics, portfolio view (main agent)
- **DASHC**: Shopper analytics, engagement metrics (DASHB sub-agent)
- **SHOPI**: Shopping journey, personalization, product recommendations
- **MARKT**: Core AMM, manages swaps ($RAMM/USDC/USDT ↔ PVT), liquidity tracking
- **RIDIM**: PVT redemption orchestration, DPP minting coordination
- **PROMO**: Influencer & affiliate management, attribution logic
- **FOLIO**: PVT wallet management, redemption, gifting, reselling
- **PAYME**: Escrow handling, payment execution, reward payouts (supports fiat, USDC, USDT, $RAMM)
- **DEFIME**: Yield management, DeFi integration (can generate yield in $RAMM and other assets)
- **LOYLT**: Loyalty & Rewards Manager, manages brand loyalty programs and loyalty tokens
  - Receives loyalty program configuration from VALET during campaign setup
  - Defines loyalty token rules (earn rates, redemption options, transferability)
  - Listens to purchase, promotion, and redemption events from FOLIO and PROMO
  - Issues or updates loyalty token balances for shoppers
  - Optionally enables swaps or secondary usage via MARKT
  - Coordinates partial-payment or reward redemptions with PAYME
  - Emits loyalty metrics and state updates to DASHB for brand visibility
- **ICP_ID**: Identity and authentication layer (protocol-specific implementation)
- **MIRO/BRAT**: Visual feedback agent for shoppers (external to marketplace, integration TBD)
- **PAYOUT**: Fund withdrawal and settlement (can disburse in fiat, USDC, USDT, or $RAMM)

**Sub-Agent Architecture:**
- **PORTE as VALET Sub-Agent**: PORTE shares deployment unit with VALET (canister for ICP, library for L2s)
- **DASHC as DASHB Sub-Agent**: DASHC shares deployment unit with DASHB
- **Shared State**: Sub-agents share storage with parent agent for efficient data access
- **Internal Communication**: Sub-agents communicate with parent via internal methods (not A2A calls)

**MIRO/BRAT External Integration:**
- MIRO/BRAT is an external agent already built outside the marketplace
- Integration method depends on protocol (see protocol-specific appendices)
- Decision pending based on MIRO/BRAT architecture and requirements

**PAYOUT Status:**
- Currently under consideration
- If implemented, will be deployed as separate finance unit
- May share deployment unit with PAYME if functionality overlaps

**Protocol-Agnostic Validation:** Graph integrity checks ensure all agents are reachable and have valid A2A edges. Python model validates agent communication patterns before protocol-specific deployment. Sub-agent relationships are modeled as internal operations.

---

### FR2: A2A Communication Protocol (NANDA) - Protocol-Agnostic

**Requirement:** All agent-to-agent communication must use NANDA protocol structure. The protocol structure is protocol-agnostic, but implementation mechanism varies by deployment target (see Protocol Abstraction Layer and Appendices).

**Protocol-Agnostic NANDA Structure:**
- All A2A edges use NANDA protocol (protocol-agnostic)
- Protocol-specific implementation varies by deployment target
- All calls authenticated via protocol-native identity systems
- Message delivery and execution handled by protocol-native mechanisms

**NANDA Structure:**
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

**Protocol-Agnostic Validation:** NANDA compliance validator checks all edges comply with protocol structure. Python model validates communication patterns before protocol-specific deployment.

**Current Status:** All A2A edges have specified NANDA intents (100% compliance achieved).

---

### FR3: State Management (Protocol-Agnostic)

**Requirement:** Agents must manage state transitions according to defined state machine. State machine logic is protocol-agnostic, but storage mechanism varies by protocol (see Protocol Abstraction Layer and Appendices).

**Protocol-Agnostic State Machine:**
- State transitions (IDLE → CONFIGURING → ACTIVE → SETTLING → COMPLETED) are protocol-independent
- State machine logic tested in Python model (protocol-agnostic)
- State persistence handled by protocol-native storage mechanisms

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
- Loyalty token issuance/update (LOYLT: IDLE → ACTIVE)
- Loyalty token redemption (LOYLT: ACTIVE → SETTLING)

**Non-State-Changing Operations:**
- Campaign queries (read-only)
- Redemption validation (read-only)
- Auth verification (read-only)
- Analytics events (read-only from sender perspective)

**Protocol-Agnostic Validation:** Test scenarios validate state transitions match expected behavior. Python model ensures state machine logic is correct before protocol-specific deployment.

---

### FR4: Authentication & Authorization (Protocol-Agnostic Logic)

**Requirement:** All state-changing operations must be authenticated. Authentication mechanism is protocol-specific, but authorization logic is protocol-agnostic (see Protocol Abstraction Layer and Appendices).

**Protocol-Agnostic Authorization Logic:**
- All state-changing operations require authentication
- Authentication result must be verified before command execution
- Unauthorized commands must be rejected
- Authentication mechanism is protocol-specific (see Protocol Abstraction Layer)

**Critical Commands Requiring Auth:**
- PVT minting (FOLIO)
- Fund disbursement (PAYOUT/PAYME)
- DPP minting (PORTE)
- Campaign activation (VALET)
- Loyalty token issuance/redemption (LOYLT)

**Validation:** Security test scenarios verify unauthorized commands are rejected. Python model validates authentication logic before protocol deployment.

---

### FR5: Campaign Creation Flow

**Requirement:** Brands must be able to create tokenized commerce campaigns.

**Flow:**
1. Brand Manager → VALET: Campaign configuration
2. VALET validates configuration
3. VALET → PROMO: Notify campaign created
4. VALET → LOYLT: Configure loyalty program (earn rates, redemption options, transferability)
5. VALET → DASHB: State update
6. VALET transitions to ACTIVE

**Mock Data Required:**
- Campaign ID
- Brand ID
- Product name
- Target audience
- Price (in USDC, USDT, $RAMM, or fiat)
- Total supply
- Bonding curve type
- Redemption window (start/end)
- Loyalty program configuration (earn rates, redemption options, transferability)

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
6. SHOPI → MARKT: Swap quote/execute ($RAMM/USDC/USDT → PVT)
7. SHOPI → PAYME: Authorize payment (escrow) - accepts fiat, USDC, USDT, or $RAMM
8. SHOPI → FOLIO: Request Buy(PVT)
9. FOLIO mints PVT to shopper wallet
10. FOLIO → LOYLT: Notify purchase event (for loyalty token accrual)
11. LOYLT issues/updates loyalty token balance for shopper
12. PAYME settles escrow

**State Changes:**
- FOLIO: IDLE → ACTIVE (PVT minted)
- PAYME: IDLE → SETTLING (escrow locked)
- LOYLT: IDLE → ACTIVE (loyalty tokens issued/updated)

**Validation:** `purchase_flow` test scenario validates end-to-end flow.

---

### FR7: Redemption Flow

**Requirement:** Shoppers must be able to redeem PVTs for products.

**Flow:**
1. Shopper → FOLIO: Request redemption
2. FOLIO → RIDIM: Redemption request
3. RIDIM → VALET: Validate redemption eligibility (timing, campaign state)
4. VALET → RIDIM: Validation response
5. (Optional) Shopper → LOYLT: Check loyalty token balance for partial payment
6. (Optional) LOYLT → PAYME: Coordinate partial payment (loyalty tokens + $RAMM/USDC/USDT)
7. RIDIM → PORTE: Mint DPP NFT
8. PORTE mints DPP with product/sustainability metadata
9. RIDIM → VALET: Request PromoCode
10. RIDIM finalizes redemption state
11. RIDIM → FOLIO: Confirmation

**State Changes:**
- PORTE: IDLE → COMPLETED (DPP minted)
- RIDIM: IDLE → COMPLETED (redemption completed)

**Validation:** `redemption_flow` test scenario validates flow.

---

### FR8: Business Logic Calculations

**Requirement:** System must correctly calculate pricing, rewards, yield, ROI, and loyalty token operations.

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

#### FR8.5: Loyalty Token Calculations

**Loyalty Token Earnings:**
- Base earnings: `earnings = purchase_amount * earn_rate`
- Promotion bonus: `bonus = base_earnings * promotion_bonus_multiplier`
- Total earnings: `total = base_earnings + bonus_earnings`

**Partial Payment Calculation:**
- Loyalty token redemption rate: `loyalty_token_value = loyalty_tokens * redemption_rate` (in $RAMM/USDC/USDT equivalent)
- Maximum loyalty usage: `max_loyalty_value = total_amount * max_usage_percentage`
- Loyalty used: `min(loyalty_token_value, max_loyalty_value)`
- Payment currency required: `total_amount - loyalty_token_value` (can be $RAMM, USDC, USDT, or fiat)

**Balance Updates:**
- New balance: `current_balance + earnings - redemptions`
- Balance cannot go negative (enforced at calculation level)

**Validation:** 3 business logic tests validate loyalty calculations.

---

### FR9: Security Requirements

**Requirement:** System must prevent unauthorized operations, replay attacks, and race conditions.

#### FR9.1: Unauthorized Command Prevention

**Validation:**
- Commands without authentication must be rejected
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
- Logic test results (16 scenarios - all passing)
- Business logic test results (14 calculations - all passing)
- Graph validation results
- NANDA protocol compliance results
- SHOPI-VALET connection details

**Formats:**
- HTML (self-contained, shareable)
- Markdown (documentation)

**Validation:** Report generator creates reports with all test results.

---

## Protocol Abstraction Layer

**Key Design Choice:** The system defines a protocol abstraction layer that specifies required capabilities, not implementations. This allows the same core agent logic to work across different blockchain protocols.

### Protocol Interface Requirements

Every protocol implementation must provide the following capabilities:

#### 1. Read State
- **Capability**: Read balances, contract/canister state, ownership records
- **Protocol-Agnostic**: Query operations return data structures
- **Protocol-Specific**: Implementation varies (stable memory query for ICP, contract storage read for L2s)

#### 2. Write State
- **Capability**: Execute transactions that mutate state
- **Protocol-Agnostic**: Write operations persist state changes
- **Protocol-Specific**: Implementation varies (inter-canister call for ICP, contract function call for L2s)

#### 3. Identity / Signing
- **Capability**: Authenticate users and verify authorization
- **Protocol-Agnostic**: Authentication result (success/failure)
- **Protocol-Specific**: Implementation varies (Internet Identity for ICP, wallet signatures for L2s)

#### 4. Fee Estimation
- **Capability**: Estimate transaction costs
- **Protocol-Agnostic**: Cost estimate in native currency
- **Protocol-Specific**: Implementation varies (cycles for ICP, gas for L2s)

#### 5. Event Confirmation
- **Capability**: Confirm transaction/operation completion
- **Protocol-Agnostic**: Confirmation with transaction details
- **Protocol-Specific**: Implementation varies (certified data for ICP, transaction receipt for L2s)

### Chain Adapter Layer

The Chain Adapter Layer implements the Protocol Interface for each supported protocol:

- **ICP Adapter**: Implements interface using canisters, inter-canister calls, stable memory, Internet Identity
- **Base Adapter**: Implements interface using smart contracts, contract calls, contract storage, wallet signatures
- **Optimism Adapter**: Implements interface using smart contracts, contract calls, contract storage, wallet signatures
- **L2 Adapter**: Implements interface using L2-specific mechanisms (varies by L2 type)

### Execution Environment

Each protocol provides an execution environment:

- **ICP**: Canister execution environment (tamperproof, serverless, network-enforced)
- **Base/Optimism**: EVM execution environment (smart contract execution, gas-based)
- **L2**: L2-specific execution environment (varies by L2 type)

### Protocol Adapter Contract

Every protocol adapter must satisfy:

```python
class ProtocolAdapter:
    def read_state(self, agent_id: str, query: dict) -> dict:
        """Read state from agent deployment unit."""
        pass
    
    def write_state(self, agent_id: str, operation: dict) -> dict:
        """Write state to agent deployment unit."""
        pass
    
    def authenticate(self, identity: dict) -> bool:
        """Authenticate user/agent identity."""
        pass
    
    def estimate_fee(self, operation: dict) -> float:
        """Estimate operation cost."""
        pass
    
    def confirm_event(self, event_id: str) -> dict:
        """Confirm operation completion."""
        pass
```

This contract ensures protocol-agnostic core logic can work with any protocol implementation.

---

## Non-Functional Requirements

### NFR1: Testability

**Requirement:** All agent logic must be testable with mock data.

**Implementation:**
- Mock data structures (MockCampaign, MockWallet, MockPVT)
- Test scenarios with expected outcomes
- Scoring system for validation

**Metrics:**
- 16 logic test scenarios (all passing)
- 14 business logic tests (all passing)
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

### EC10: NANDA Compliance

**Constraint:** All A2A edges must have specified NANDA intents.

**Current Status:** 100% compliance - all edges have specified intents.

**Handling:**
- NANDA validator validates all edges comply with protocol structure
- All intents are specified with appropriate performatives and payload contracts

---

## Success Metrics

### SM1: Test Coverage

**Metric:** Percentage of test scenarios passing.

**Target:** ≥ 85% pass rate for all test scenarios.

**Current Status:**
- Logic tests: 16/16 scenarios passing (100%)
- Business logic tests: 14/14 passing (100%)
- Graph validation: All checks passing
- NANDA compliance: 100% (all edges have specified intents)

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
- Loyalty: 3/3 passing

**Current Status:** 14/14 passing (100%).

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

**Current Status:** 100% compliance (all edges have specified intents).

---

## Implementation Notes

### Technology Stack

**Current Phase (Python Modeling - Protocol-Agnostic):**
- **Language**: Python 3
- **Purpose**: Logic validation, state machine testing, business rule verification (protocol-agnostic)
- **Libraries**:
  - `networkx`: Agent network modeling (maps to any protocol deployment)
  - `matplotlib`: Graph visualizations
  - `pydantic`: Data validation (ensures data integrity)
  - `rich`: Console output formatting
  - `streamlit`: Interactive dashboard for testing

**Target Phase (Protocol-Specific Deployment):**
- See Appendices A-D for protocol-specific technology stacks

### Architecture Decisions

1. **Protocol-Agnostic Python-First Modeling**: Focus on logic/behavior validation before protocol-specific implementation
   - Validates agent behavior, state machines, and business rules (protocol-agnostic)
   - Maps to protocol-specific deployment units (canisters for ICP, contracts for L2s)
   - Tests agent communication patterns (protocol-agnostic)

2. **NANDA Protocol**: Structured A2A communication for testability (protocol-agnostic)
   - Protocol-agnostic message structure
   - Maps to protocol-specific mechanisms (inter-canister calls for ICP, contract calls for L2s)
   - Ensures consistent message format across all protocols
   - Validates communication contracts before deployment

3. **Protocol Abstraction Layer**: Define capabilities, not implementations
   - Protocol adapter interface ensures core logic works with any protocol
   - Protocol-specific adapters implement interface for each supported protocol
   - Core logic remains invariant across protocols

4. **Multi-Protocol Deployment Strategy**: Support multiple blockchain protocols
   - **ICP**: Canister-based deployment (isolation, stable memory, network-enforced security)
   - **Base/Optimism/L2**: Smart contract deployment (gas-optimized, wallet-based auth)
   - Same agent logic, different deployment mechanisms
   - Protocol-specific optimizations (libraries for L2s, sub-agents for ICP)

5. **Protocol-Specific Authentication**: Decentralized authentication per protocol
   - **ICP**: Internet Identity (no private keys, network-enforced)
   - **Base/Optimism/L2**: Wallet signatures (EIP-712, user-controlled keys)
   - Same authorization logic, different authentication mechanisms

6. **Mock Data Testing**: Test logic without external dependencies (protocol-agnostic)
   - Validates business rules before any protocol deployment
   - Tests state transitions and agent coordination
   - Scoring system for quantitative validation
   - All tests are protocol-agnostic

7. **Graph Validation**: Ensure network integrity before deployment (protocol-agnostic)
   - Validates agent communication patterns (protocol-agnostic)
   - Ensures all agents are reachable
   - Prevents deployment of broken agent networks on any protocol

### Known Limitations

1. **NANDA Compliance**: All edges now have specified intents (100% compliance achieved)
2. **Mock Data Only**: No real wallet/blockchain integration (Python model phase)
3. **Python Model Only**: Not actual protocol deployment (next phase)
4. **Limited Error Handling**: Some edge cases may not be fully handled (to be addressed in protocol implementation)
5. **No Performance Testing**: Focus is on logic validation, not protocol performance
6. **No Multi-Chain Implementation**: Multi-chain token operations not yet implemented (Python model phase)
7. **No Self-Writing AI Integration**: VALET's AI capabilities are modeled but not connected to actual AI services

### Protocol Deployment Readiness

**Ready for Any Protocol Deployment (Protocol-Agnostic):**
- ✅ Agent architecture defined (15 agents with roles and responsibilities)
- ✅ A2A communication patterns validated (NANDA protocol - protocol-agnostic)
- ✅ State machine logic tested (16 test scenarios - protocol-agnostic)
- ✅ Business logic validated (14 business logic tests - protocol-agnostic)
- ✅ Security patterns tested (10 security scenarios - protocol-agnostic)
- ✅ Graph integrity validated (all agents reachable - protocol-agnostic)

**Before Protocol-Specific Deployment:**
- ✅ All NANDA intents specified (100% compliance)
- ⚠️ Implement protocol adapter for target protocol
- ⚠️ Implement protocol-specific deployment units (canisters/contracts)
- ⚠️ Integrate protocol-native authentication
- ⚠️ Implement protocol-native storage
- ⚠️ Add bridge integration for multi-chain operations (if needed)
- ⚠️ Connect VALET to AI services for self-writing capabilities
- ⚠️ Protocol-specific security audits

---

## Appendices

### Appendix A: ICP Implementation

#### Deployment Architecture

**Canister-Based Deployment:**
- Each agent deployed as an ICP canister (or shared canister for sub-agents)
- Canisters are tamperproof, unstoppable, and serverless by design
- Network-enforced security and resilience
- Canister upgrades preserve state in stable memory

**Agent-to-Canister Mapping:**

| Canister | Agents | Type | Description |
|----------|--------|------|-------------|
| **VALET Canister** | VALET, PORTE | Application | VALET (main) + PORTE (sub-agent) share canister |
| **DASHB Canister** | DASHB, DASHC | Data | DASHB (main) + DASHC (sub-agent) share canister |
| **SHOPI Canister** | SHOPI | Application | Shopping journey, personalization |
| **MARKT Canister** | MARKT | Application | Core AMM, swaps (USDC ↔ PVT) |
| **RIDIM Canister** | RIDIM | Application | PVT redemption orchestration |
| **PROMO Canister** | PROMO | Application | Influencer & affiliate management |
| **FOLIO Canister** | FOLIO | Application | PVT wallet management |
| **PAYME Canister** | PAYME | Finance | Escrow handling, payment execution (multi-currency support) |
| **DEFIME Canister** | DEFIME | Finance | Yield management, DeFi integration (multi-asset yield) |
| **LOYLT Canister** | LOYLT | Application | Loyalty & Rewards Manager |
| **ICP_ID Canister** | ICP_ID | Identity | Internet Identity integration |
| **PAYOUT Canister** | PAYOUT | Finance | Fund withdrawal (multi-currency disbursement) |

**Subnet Distribution:**
- **Brand Services Subnet**: VALET (with PORTE), DASHB (with DASHC), PROMO canisters
- **Shopper Services Subnet**: SHOPI, FOLIO canisters
- **Finance Services Subnet**: PAYME, DEFIME, PAYOUT canisters (high-security)
- **Marketplace Subnet**: MARKT canister
- **Redemption Subnet**: RIDIM canister
- **Identity Layer**: ICP_ID canister (Internet Identity integration)
- **External Integration**: MIRO/BRAT (external agent, integration method TBD)

#### Communication (A2A via Inter-Canister Calls)

**NANDA Protocol Implementation:**
- A2A edges map to inter-canister calls on ICP
- Calls are async and non-atomic (require state machines)
- All calls authenticated via Internet Identity (ICP_ID canister)
- Network-enforced message delivery and execution
- Certified data ensures message integrity

**Example Flow:**
```
Python Model: SHOPI → VALET (query, campaign.list_active)
    ↓
ICP: shopi-canister → valet-canister (inter-canister call)
    ↓
Method: query_campaigns(filters, limit, offset)
    ↓
Storage: Query from stable memory (read-only)
    ↓
Response: Certified data returned to shopi-canister
```

#### State Storage

**Stable Memory:**
- Persistent storage for critical state (campaigns, transactions, ownership)
- Survives canister upgrades
- Used for: campaign configs, transaction logs, PVT ownership, redemption records

**Heap Memory:**
- Temporary storage (cleared on upgrade)
- Used for: AI model caching (VALET), temporary calculations, query results

**Certified Data:**
- Integrity-verified data (ICP_ID, critical validations)
- Network-enforced data integrity

#### Authentication & Security

**Internet Identity:**
- ICP_ID canister wraps ICP's Internet Identity system
- Decentralized identity without private key management
- Principal-based authentication for all canister calls
- Network-enforced authentication (tamperproof)

**Security Model:**
- Network-enforced tamperproof execution
- Guaranteed uptime and unstoppable execution
- No traditional attack vectors (DDoS, server compromise, etc.)
- Certified data ensures integrity

#### Technology Stack

- **Languages**: Motoko (primary) or Rust (alternative)
- **Network**: Internet Computer (ICP) mainnet
- **Storage**: Stable memory for persistent state
- **Authentication**: Internet Identity via ICP_ID canister
- **Communication**: Inter-canister calls (A2A protocol)
- **Multi-chain**: Chain Fusion for token operations across blockchains (including $RAMM from Base)
- **Supported Currencies**: Via Chain Fusion - $RAMM (Base), USDC, USDT, and other bridged tokens
- **AI Integration**: Self-writing apps capability for VALET agent

#### Key Advantages

- **Tamperproof & Unstoppable**: Network-enforced security eliminates traditional attacks
- **Serverless**: No server management required
- **Sovereign Cloud**: Escape vendor lock-in
- **Self-Writing Apps**: AI can generate and update apps on demand
- **Chain Fusion**: Trustless multi-chain token operations

#### Known Tradeoffs

- **Async Calls**: Inter-canister calls are async, requiring state machines for multi-step flows
- **Cycle Costs**: Canister operations consume cycles (ICP's resource model)
- **Internet Identity Dependency**: Requires Internet Identity for authentication
- **Learning Curve**: Motoko/Rust development requires protocol-specific knowledge

---

### Appendix B: Base Implementation

#### Deployment Architecture

**Smart Contract-Based Deployment:**
- Each agent deployed as smart contract(s) on Base
- Contracts communicate via contract function calls (A2A protocol)
- State stored in contract storage (gas-optimized)
- EVM-compatible execution environment

**Agent-to-Contract Mapping:**

| Contract | Agents | Type | Description |
|----------|--------|------|-------------|
| **ValetContract** | VALET, PORTE | Main + Library | VALET (main contract) + PORTE (library/module) |
| **DashboardContract** | DASHB, DASHC | Main + Library | DASHB (main contract) + DASHC (library/module) |
| **ShopiContract** | SHOPI | Standalone | Shopping journey, personalization |
| **MarktContract** | MARKT | Standalone | Core AMM, swaps ($RAMM/USDC/USDT ↔ PVT) |
| **RidimContract** | RIDIM | Standalone | PVT redemption orchestration |
| **PromoContract** | PROMO | Standalone | Influencer & affiliate management |
| **FolioContract** | FOLIO | Standalone | PVT wallet management (ERC-721/1155) |
| **PaymeContract** | PAYME | Standalone | Escrow handling, payment execution (fiat/USDC/USDT/$RAMM) |
| **DefimeContract** | DEFIME | Standalone | Yield management, DeFi integration (yield in $RAMM/assets) |
| **LoyltContract** | LOYLT | Standalone | Loyalty & Rewards Manager |
| **IdentityContract** | ICP_ID | Standalone | Identity verification (wallet-based) |
| **PayoutContract** | PAYOUT | Standalone | Fund withdrawal (fiat/USDC/USDT/$RAMM disbursement) |

**Gas Optimization:**
- Sub-agents (PORTE, DASHC) implemented as libraries to reduce gas costs
- Packed structs and mappings for efficient storage
- Batch operations where possible

#### Communication (A2A via Contract Calls)

**NANDA Protocol Implementation:**
- A2A edges map to smart contract function calls
- Calls are synchronous (EVM execution model)
- All calls authenticated via wallet signatures (EIP-712)
- Contract-level access control ensures message integrity
- Events emitted for cross-contract communication

**Example Flow:**
```
Python Model: SHOPI → VALET (query, campaign.list_active)
    ↓
Base: ShopiContract → ValetContract (function call)
    ↓
Function: queryCampaigns(filters, limit, offset)
    ↓
Storage: Query from contract storage (read-only)
    ↓
Response: Return data to ShopiContract
    ↓
Event: CampaignQuery event emitted (optional)
```

#### State Storage

**Contract Storage:**
- Persistent storage for critical state (campaigns, transactions, ownership)
- Stored in contract state variables
- Gas-optimized storage patterns (packed structs, mappings)
- Used for: campaign configs, transaction logs, PVT ownership, redemption records

**Memory:**
- Temporary storage (cleared after transaction)
- Used for: Temporary calculations, query results
- No persistent caching (recalculate on each call)

**Storage Optimization:**
- Packed structs to minimize storage slots
- Mappings for efficient lookups
- Events for off-chain indexing

#### Authentication & Security

**Wallet-Based Authentication:**
- IdentityContract (or access control modifiers) handles authentication
- Wallet signatures (EIP-712) for all contract calls
- Address-based authorization (role-based access control)
- Smart contract-enforced authentication

**Security Model:**
- Smart contract security (reentrancy guards, access control)
- EVM execution guarantees
- Base's L2 security (inherits Ethereum security)
- Lower gas costs than Ethereum mainnet
- Faster transaction finality

#### Technology Stack

- **Languages**: Solidity (primary) or Vyper (alternative)
- **Network**: Base mainnet (Ethereum L2)
- **Storage**: Contract storage (gas-optimized)
- **Authentication**: Wallet signatures (EIP-712) via IdentityContract
- **Communication**: Contract function calls (A2A protocol)
- **Token Standards**: 
  - ERC-20 for $RAMM (native token), USDC, USDT, and PVTs
  - ERC-721/1155 for DPP NFTs
- **Native Token**: $RAMM deployed on Base
- **Supported Currencies**: $RAMM, USDC (Base native), USDT
- **Bridge Integration**: Base's native bridge for multi-chain operations

#### Key Advantages

- **Lower Gas Costs**: L2 benefits reduce transaction costs
- **Faster Transactions**: Quick finality compared to Ethereum mainnet
- **Ethereum Security**: Inherits Ethereum's security model
- **EVM Compatibility**: Standard tooling and libraries
- **Base Bridge**: Native bridge for cross-chain operations

#### Known Tradeoffs

- **Gas Costs**: Still requires gas fees (though lower than Ethereum mainnet)
- **Synchronous Calls**: Contract calls are synchronous, limiting async patterns
- **Storage Costs**: Contract storage is expensive (gas-optimization critical)
- **Upgrade Complexity**: Contract upgrades require proxy patterns or migration
- **Wallet Dependency**: Requires users to manage private keys

---

### Appendix C: Optimism Implementation

#### Deployment Architecture

**Smart Contract-Based Deployment:**
- Similar to Base (Ethereum L2 with optimistic rollups)
- Each agent deployed as smart contract(s) on Optimism
- Contracts communicate via contract function calls (A2A protocol)
- Optimistic rollup security model

**Agent-to-Contract Mapping:**
- Same structure as Base (see Appendix B)
- Contracts deployed on Optimism mainnet
- Optimism-specific bridge for multi-chain operations

#### Communication (A2A via Contract Calls)

**NANDA Protocol Implementation:**
- Same as Base: A2A edges map to smart contract function calls
- Synchronous execution (EVM model)
- Wallet-based authentication (EIP-712)
- Contract-level access control

#### State Storage

**Contract Storage:**
- Same as Base: Contract storage with gas optimization
- Persistent state in contract variables
- Events for off-chain indexing

#### Authentication & Security

**Wallet-Based Authentication:**
- Same as Base: Wallet signatures (EIP-712)
- Address-based authorization
- Smart contract-enforced authentication

**Security Model:**
- Optimistic rollup security (faster finality, lower costs)
- Ethereum security inheritance
- Fault proofs for dispute resolution
- Lower gas costs than Ethereum mainnet

#### Technology Stack

- **Languages**: Solidity (primary) or Vyper (alternative)
- **Network**: Optimism mainnet (Ethereum L2)
- **Storage**: Contract storage (gas-optimized)
- **Authentication**: Wallet signatures (EIP-712) via IdentityContract
- **Communication**: Contract function calls (A2A protocol)
- **Token Standards**: 
  - ERC-20 for $RAMM (if deployed), USDC, USDT, and PVTs
  - ERC-721/1155 for DPP NFTs
- **Supported Currencies**: $RAMM (if deployed), USDC, USDT
- **Bridge Integration**: Optimism's native bridge for cross-chain operations

#### Key Advantages

- **Optimistic Rollups**: Faster finality, lower costs, Ethereum security
- **Fault Proofs**: Dispute resolution mechanism
- **Ethereum Compatibility**: Full EVM compatibility
- **Lower Gas Costs**: L2 benefits reduce transaction costs
- **Optimism Bridge**: Native bridge for cross-chain operations

#### Known Tradeoffs

- **Gas Costs**: Still requires gas fees (though lower than Ethereum mainnet)
- **Synchronous Calls**: Contract calls are synchronous, limiting async patterns
- **Storage Costs**: Contract storage is expensive (gas-optimization critical)
- **Upgrade Complexity**: Contract upgrades require proxy patterns or migration
- **Wallet Dependency**: Requires users to manage private keys
- **Fault Proof Window**: Optimistic rollups have a challenge period for disputes

---

### Appendix D: General L2 Implementation

#### Deployment Architecture

**Smart Contract-Based Deployment:**
- Applicable to any Ethereum-compatible L2 (Arbitrum, Polygon, zkSync, etc.)
- Each agent deployed as smart contract(s) on chosen L2
- Contracts communicate via contract function calls (A2A protocol)
- L2-specific security and bridge mechanisms

**Agent-to-Contract Mapping:**
- Same structure as Base/Optimism (see Appendix B)
- Contracts deployed on chosen L2 mainnet
- L2-specific bridge for cross-chain operations

#### Communication (A2A via Contract Calls)

**NANDA Protocol Implementation:**
- A2A edges map to contract function calls
- L2-specific execution model (zk-rollup, optimistic rollup, or sidechain)
- Wallet-based authentication (EIP-712 for EVM L2s)
- Contract-level access control

#### State Storage

**Contract Storage:**
- L2-specific storage mechanisms
- Contract storage for EVM-compatible L2s
- Gas-optimized patterns
- Events for off-chain indexing

#### Authentication & Security

**Wallet-Based Authentication:**
- Wallet signatures (EIP-712 for EVM L2s)
- Address-based authorization
- Smart contract-enforced authentication

**Security Model:**
- L2-specific security model (zk-proofs, optimistic rollups, sidechain security)
- Inherits security from underlying chain (Ethereum for L2s)
- L2-specific finality times and guarantees

#### Technology Stack

- **Languages**: Solidity (for EVM-compatible L2s) or L2-specific languages
- **Network**: Any Ethereum-compatible L2 (Arbitrum, Polygon, zkSync, etc.)
- **Storage**: L2-specific storage mechanisms
- **Authentication**: L2-specific authentication (wallet-based for EVM L2s)
- **Communication**: L2-specific communication mechanisms
- **Token Standards**: 
  - ERC-20 for $RAMM (if deployed), USDC, USDT, and PVTs (EVM L2s)
  - ERC-721/1155 for DPP NFTs (EVM L2s)
- **Supported Currencies**: $RAMM (if deployed), USDC, USDT, and L2-specific tokens
- **Bridge Integration**: L2-specific bridge mechanisms

#### Key Advantages

- **L2 Benefits**: Lower costs, faster transactions, scalability
- **Ethereum Security**: Inherits security from Ethereum (for L2s)
- **Flexibility**: Choose L2 based on specific needs (cost, speed, features)
- **EVM Compatibility**: Standard tooling for EVM-compatible L2s
- **Bridge Options**: Multiple bridge options for cross-chain operations

#### Known Tradeoffs

- **L2-Specific Considerations**: Each L2 type has unique tradeoffs (see below)
- **Gas Costs**: Varies by L2 (some have very low costs, others moderate)
- **Synchronous Calls**: Contract calls are synchronous for EVM L2s
- **Storage Costs**: Contract storage costs vary by L2
- **Upgrade Complexity**: Contract upgrades require proxy patterns or migration
- **Wallet Dependency**: Requires users to manage private keys

#### L2-Specific Considerations

**zk-Rollups (e.g., zkSync):**
- Zero-knowledge proofs for security
- Fast finality
- Lower costs
- May require different token standards
- **Tradeoffs**: More complex development, may have different execution model

**Optimistic Rollups (e.g., Arbitrum, Optimism):**
- Faster finality than Ethereum
- Lower costs
- Ethereum security inheritance
- Dispute resolution mechanisms
- **Tradeoffs**: Challenge period for disputes, longer finality than zk-rollups

**Sidechains (e.g., Polygon):**
- Independent security model
- Very low costs
- Fast transactions
- Bridge security considerations
- **Tradeoffs**: Less security guarantees than rollups, bridge risks

---

### Appendix E: Test Scenarios Summary

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

### Appendix F: Agent Roles and Deployment Mapping

**Brand-Facing:**
- VALET (main agent, shares deployment unit with PORTE sub-agent)
- PORTE (sub-agent, shares VALET deployment unit)
- DASHB (main agent, shares deployment unit with DASHC sub-agent)
- DASHC (sub-agent, shares DASHB deployment unit)
- PROMO (own deployment unit)
- LOYLT (own deployment unit, Loyalty & Rewards Manager)

**Shopper-Facing:**
- SHOPI (own deployment unit)
- FOLIO (own deployment unit)
- RIDIM (own deployment unit)
- MIRO/BRAT (external, integration TBD)

**Finance:**
- MARKT (own deployment unit)
- PAYME (own deployment unit)
- DEFIME (own deployment unit)
- PAYOUT (under consideration, own deployment unit if implemented)

**Identity:**
- ICP_ID (own deployment unit, protocol-specific implementation)

**Deployment Summary:**
- Protocol-specific deployment unit mapping (see protocol-specific appendices)
- Sub-agent relationships (shared deployment units)
- External integrations

### Appendix G: State Change Matrix

| Agent | State-Changing | Non-State-Changing |
|-------|----------------|---------------------|
| VALET | Campaign config | Campaign queries |
| SHOPI | Purchase auth | Campaign queries |
| FOLIO | PVT mint/transfer | Portfolio queries |
| PAYME | Escrow lock/release | Balance queries |
| RIDIM | Redemption state | Redemption validation |
| PORTE | DPP NFT mint | DPP template queries |
| MARKT | Swap execution | Swap quotes |
| LOYLT | Loyalty token issuance/redemption | Loyalty balance queries |
| ICP_ID | None | Principal verification |

---

**Document Status:** Based on implementation analysis of code and tests as of January 2026.  
**Next Review:** When new agents are added or protocol-specific deployment begins.
