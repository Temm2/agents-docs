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

**All agent tests (16 logic scenarios + 11 business logic tests) are protocol-agnostic and validate the core system behavior regardless of deployment target.**

### Multi-Protocol Deployment Strategy

The system can be deployed on multiple blockchain protocols, each with protocol-specific implementation considerations:

1. **Internet Computer (ICP)** - Canister-based deployment
2. **Base** - Smart contract deployment on Ethereum L2
3. **Optimism** - Smart contract deployment on Ethereum L2
4. **Any L2** - General Layer 2 deployment considerations

Each protocol section below details how the same agent logic maps to protocol-specific deployment units and communication mechanisms.

### Architecture Model

The system is implemented as a Python modeling framework that maps conceptually to protocol-specific deployment units:
- **ICP**: Canisters (inter-canister calls, stable memory, Internet Identity)
- **Base/Optimism/L2**: Smart contracts (contract calls, storage, wallet authentication)
- **Common**: Agent behavior, state machines, business logic (protocol-agnostic)

The Python framework focuses on agent behavior, state transitions, and decision flows, providing a testable model before protocol-specific deployment.

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
- **Protocol-Specific Deployment**: 
  - **ICP**: Canisters with inter-canister calls, stable memory, Internet Identity
  - **Base/Optimism/L2**: Smart contracts with contract calls, storage, wallet authentication
- Agents communicate via structured A2A protocol (NANDA) using protocol-specific mechanisms
- State persistence handled by protocol-native storage (stable memory for ICP, contract storage for L2s)
- All operations authenticated via protocol-native identity systems
- Business logic is deterministic and testable before protocol deployment
- Multi-chain token operations enabled via protocol-specific bridges/technologies
- Self-writing AI capabilities for dynamic campaign generation (VALET agent)
- Protocol-native security features (network-enforced for ICP, smart contract security for L2s)

---

## Goals and Non-Goals

### Goals

1. **Modular Agent Architecture on ICP**
   - Each agent is independently deployable as an ICP canister
   - Canisters communicate via inter-canister calls (structured A2A protocol)
   - Clear separation of concerns (brand, shopper, finance, data, identity)
   - Network-enforced isolation and security
   - Canister upgrades without state loss (stable memory persistence)

2. **Deterministic State Management on ICP**
   - All state transitions are validated and stored in stable memory
   - State-changing operations are authenticated via Internet Identity
   - State machine rules are enforced at the canister level
   - Certified data ensures data integrity and tamperproof verification
   - State persists across canister upgrades

3. **Comprehensive Testing**
   - Logic tests validate agent behavior (16 scenarios)
   - Business logic tests validate calculations (11 tests)
   - Graph validation ensures network integrity

4. **Security & Compliance on ICP**
   - All commands require Internet Identity authentication (ICP_ID agent)
   - Network-enforced tamperproof execution prevents traditional attacks
   - Replay attack prevention via idempotency and nonce validation
   - Race condition handling with canister-level atomicity
   - Boundary condition validation enforced at execution layer
   - Guaranteed uptime and unstoppable execution

5. **Business Logic Correctness**
   - Bonding curve pricing (linear, exponential, logarithmic)
   - Reward calculations (tiered, attribution-based)
   - Yield calculations (simple, compound)
   - ROI metrics (campaign ROI, PVT velocity)

### Non-Goals

1. **Not a Full ICP Canister Implementation (Current Phase)**
   - This is a Python modeling framework for testing logic and behavior
   - Actual ICP canister deployment (Motoko/Rust) is the next phase
   - Focus is on validating agent logic, state transitions, and business rules before ICP deployment
   - Python model serves as specification for canister implementation

2. **Not a Production System (Yet)**
   - No real wallet integration (uses mock data)
   - No actual blockchain transactions (simulated)
   - Mock data only for testing agent logic
   - Production deployment requires ICP canister implementation

3. **Not a Complete Feature Set**
   - Some NANDA intents are "unspecified" (work in progress - 35 edges need specification)
   - Not all edge cases are fully handled in Python model
   - Some agents have minimal implementation (focus on core flows)

4. **Not a User Interface**
   - No frontend implementation
   - Streamlit dashboard is for testing/visualization only
   - Production UI/UX will be built on ICP (canister-hosted web assets)

---

## Functional Requirements

### FR1: Agent Network Architecture (Protocol-Agnostic)

**Requirement:** The system must support 14 distinct agents with defined roles and responsibilities. The agent logic is protocol-agnostic, but deployment architecture varies by protocol.

**Protocol-Agnostic Agent Definitions:**

**ICP Deployment Model:**
- Agents may share canisters (sub-agents share parent canister)
- Canisters communicate via inter-canister calls (A2A protocol)
- State stored in stable memory (persistent across upgrades)
- Authentication via Internet Identity (ICP_ID canister)
- Network-enforced security and resilience

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
| **PAYME Canister** | PAYME | Finance | Escrow handling, payment execution |
| **DEFIME Canister** | DEFIME | Finance | Yield management, DeFi integration |
| **ICP_ID Canister** | ICP_ID | Identity | Internet Identity integration |
| **PAYOUT Canister** | PAYOUT | Finance | Fund withdrawal (under consideration) |
| **MIRO/BRAT** | External | External | Visual feedback agent (external integration) |

**Agent Details:**
- **VALET**: Campaign orchestrator, brand onboarding, AI-generated campaigns (main agent)
- **PORTE**: Digital Product Passport (DPP) creation and NFT minting (VALET sub-agent, shared canister)
- **DASHB**: Brand dashboard, campaign analytics, portfolio view (main agent)
- **DASHC**: Shopper analytics, engagement metrics (DASHB sub-agent, shared canister)
- **SHOPI**: Shopping journey, personalization, product recommendations
- **MARKT**: Core AMM, manages swaps (USDC ↔ PVT), liquidity tracking
- **RIDIM**: PVT redemption orchestration, DPP minting coordination
- **PROMO**: Influencer & affiliate management, attribution logic
- **FOLIO**: PVT wallet management, redemption, gifting, reselling
- **PAYME**: Escrow handling, payment execution, reward payouts
- **DEFIME**: Yield management, DeFi integration
- **ICP_ID**: Identity and authentication layer (Internet Identity wrapper)
- **MIRO/BRAT**: Visual feedback agent for shoppers (external to marketplace, integration TBD)
- **PAYOUT**: Fund withdrawal and settlement (under consideration)

**ICP Canister Subnet Distribution:**
- **Brand Services Subnet**: VALET (with PORTE), DASHB (with DASHC), PROMO canisters
- **Shopper Services Subnet**: SHOPI, FOLIO canisters
- **Finance Services Subnet**: PAYME, DEFIME, PAYOUT canisters (high-security)
- **Marketplace Subnet**: MARKT canister
- **Redemption Subnet**: RIDIM canister
- **Identity Layer**: ICP_ID canister (Internet Identity integration)
- **External Integration**: MIRO/BRAT (external agent, integration method TBD)

**Sub-Agent Architecture:**
- **PORTE as VALET Sub-Agent**: PORTE shares VALET canister, handles DPP operations as part of VALET's campaign lifecycle
- **DASHC as DASHB Sub-Agent**: DASHC shares DASHB canister, provides shopper analytics alongside brand analytics
- **Shared State**: Sub-agents share stable memory with parent agent for efficient data access
- **Internal Communication**: Sub-agents communicate with parent via internal canister methods (not inter-canister calls)

**MIRO/BRAT External Integration:**
- MIRO/BRAT is an external agent already built outside the marketplace
- Integration options:
  1. **External Service Call**: SHOPI canister calls MIRO/BRAT via HTTP/API (not inter-canister)
  2. **Separate Canister**: Deploy MIRO/BRAT as independent ICP canister if needed
  3. **Embedded Module**: Integrate MIRO/BRAT functionality into SHOPI canister
- Decision pending based on MIRO/BRAT architecture and requirements

**PAYOUT Status:**
- Currently under consideration
- If implemented, will be deployed as separate finance canister
- May share canister with PAYME if functionality overlaps

**ICP Validation:** Graph integrity checks ensure all agents are reachable and have valid A2A edges. Python model validates canister communication patterns before ICP deployment. Sub-agent relationships are modeled as internal canister operations.

#### FR1.2: Base (Ethereum L2) Deployment

**Base Deployment Model:**
- Each agent deployed as smart contract(s) on Base
- Contracts communicate via contract calls (A2A protocol via function calls)
- State stored in contract storage (persistent, gas-optimized)
- Authentication via wallet signatures (EIP-712, wallet-based)
- EVM security model (reentrancy guards, access control)

**Base Agent-to-Contract Mapping:**

| Contract | Agents | Type | Description |
|----------|--------|------|-------------|
| **ValetContract** | VALET, PORTE | Main + Library | VALET (main contract) + PORTE (library/module) |
| **DashboardContract** | DASHB, DASHC | Main + Library | DASHB (main contract) + DASHC (library/module) |
| **ShopiContract** | SHOPI | Standalone | Shopping journey, personalization |
| **MarktContract** | MARKT | Standalone | Core AMM, swaps (USDC ↔ PVT) |
| **RidimContract** | RIDIM | Standalone | PVT redemption orchestration |
| **PromoContract** | PROMO | Standalone | Influencer & affiliate management |
| **FolioContract** | FOLIO | Standalone | PVT wallet management (ERC-721/1155) |
| **PaymeContract** | PAYME | Standalone | Escrow handling, payment execution |
| **DefimeContract** | DEFIME | Standalone | Yield management, DeFi integration |
| **IdentityContract** | ICP_ID | Standalone | Identity verification (wallet-based) |
| **PayoutContract** | PAYOUT | Standalone | Fund withdrawal (under consideration) |

**Base-Specific Considerations:**
- **Gas Optimization**: Sub-agents (PORTE, DASHC) implemented as libraries to reduce gas costs
- **Storage**: Contract storage for state (optimized for gas efficiency)
- **Authentication**: Wallet signatures (MetaMask, WalletConnect) instead of Internet Identity
- **Token Standards**: ERC-20 for PVTs, ERC-721/1155 for DPP NFTs
- **Bridge Integration**: Base's native bridge for multi-chain operations
- **L2 Benefits**: Lower gas costs, faster transactions, Ethereum security

**Base Validation:** Python model validates contract interaction patterns. Smart contract security audits required before deployment.

#### FR1.3: Optimism (Ethereum L2) Deployment

**Optimism Deployment Model:**
- Similar to Base (Ethereum L2 with optimistic rollups)
- Each agent deployed as smart contract(s) on Optimism
- Contracts communicate via contract calls (A2A protocol)
- State stored in contract storage
- Authentication via wallet signatures
- Optimistic rollup security model

**Optimism Agent-to-Contract Mapping:**
- Same structure as Base (see FR1.2)
- Contracts deployed on Optimism mainnet
- Optimism-specific bridge for multi-chain operations

**Optimism-Specific Considerations:**
- **Optimistic Rollups**: Faster finality, lower costs, Ethereum security
- **Bridge Integration**: Optimism's native bridge for cross-chain operations
- **Gas Optimization**: Similar to Base (libraries for sub-agents)
- **Token Standards**: Same as Base (ERC-20, ERC-721/1155)
- **Fault Proofs**: Optimism's security model for dispute resolution

**Optimism Validation:** Python model validates contract interaction patterns. Smart contract security audits required before deployment.

#### FR1.4: General L2 Deployment

**L2 Deployment Model:**
- Applicable to any Ethereum-compatible L2 (Arbitrum, Polygon, zkSync, etc.)
- Each agent deployed as smart contract(s) on chosen L2
- Contracts communicate via contract calls (A2A protocol)
- State stored in contract storage
- Authentication via wallet signatures
- L2-specific security and bridge mechanisms

**L2-Specific Considerations:**
- **L2 Type**: zk-rollup, optimistic rollup, or sidechain
- **Bridge Integration**: L2-specific bridge for cross-chain operations
- **Token Standards**: ERC-20 for PVTs, ERC-721/1155 for DPP NFTs
- **Gas Costs**: L2-specific gas optimization strategies
- **Finality**: L2-specific finality times and security guarantees
- **Compatibility**: EVM-compatible L2s preferred for code reuse

**L2 Validation:** Python model validates contract interaction patterns. L2-specific security audits and bridge testing required.

**Protocol-Agnostic Validation:** Graph integrity checks ensure all agents are reachable and have valid A2A edges. Python model validates agent communication patterns before protocol-specific deployment. Sub-agent relationships are modeled as internal operations (canister methods for ICP, library calls for L2s).

---

### FR2: A2A Communication Protocol (NANDA) - Protocol-Agnostic

**Requirement:** All agent-to-agent communication must use NANDA protocol structure. The protocol is protocol-agnostic, but implementation mechanism varies by deployment target.

**Protocol-Agnostic NANDA Structure:**
- All A2A edges use NANDA protocol (protocol-agnostic)
- Protocol-specific implementation varies by deployment target
- All calls authenticated via protocol-native identity systems
- Message delivery and execution handled by protocol-native mechanisms

**Protocol-Specific Implementations:**

#### FR2.1: ICP Implementation (Inter-Canister Calls)

**ICP Implementation:**
- A2A edges map to inter-canister calls on ICP
- Calls are async and non-atomic (require state machines)
- All calls authenticated via Internet Identity (ICP_ID canister)
- Network-enforced message delivery and execution
- Certified data ensures message integrity

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

**ICP Inter-Canister Call Flow:**
```
Python Model: SHOPI → VALET (query, campaign.list_active)
    ↓
ICP Canister: shopi-canister → valet-canister (inter-canister call)
    ↓
Method: query_campaigns(filters, limit, offset)
    ↓
Storage: Query from stable memory (read-only, no state change)
    ↓
Response: Certified data returned to shopi-canister
```

#### FR2.2: Base/Optimism/L2 Implementation (Contract Calls)

**L2 Implementation:**
- A2A edges map to smart contract function calls
- Calls are synchronous (EVM) or async (depending on L2)
- All calls authenticated via wallet signatures (EIP-712)
- Contract-level access control ensures message integrity
- Events emitted for cross-contract communication

**L2 Contract Call Flow:**
```
Python Model: SHOPI → VALET (query, campaign.list_active)
    ↓
L2 Contracts: ShopiContract → ValetContract (function call)
    ↓
Function: queryCampaigns(filters, limit, offset)
    ↓
Storage: Query from contract storage (read-only, no state change)
    ↓
Response: Return data to ShopiContract
    ↓
Event: CampaignQuery event emitted (optional)
```

**Protocol-Agnostic Validation:** NANDA compliance validator checks all edges comply with protocol structure. Python model validates communication patterns before protocol-specific deployment.

**Current Status:** 35 edges have "unspecified" intents (work in progress - must be specified before any protocol deployment).

---

### FR3: State Management (Protocol-Agnostic)

**Requirement:** Agents must manage state transitions according to defined state machine. State machine logic is protocol-agnostic, but storage mechanism varies by protocol.

**Protocol-Agnostic State Machine:**
- State transitions (IDLE → CONFIGURING → ACTIVE → SETTLING → COMPLETED) are protocol-independent
- State machine logic tested in Python model (protocol-agnostic)
- State persistence handled by protocol-native storage mechanisms

**Protocol-Specific State Storage:**

#### FR3.1: ICP State Storage

**ICP State Storage:**
- **Stable Memory**: Persistent storage for critical state (campaigns, transactions, ownership)
  - Survives canister upgrades
  - Used for: campaign configs, transaction logs, PVT ownership, redemption records
- **Heap Memory**: Temporary storage (cleared on upgrade)
  - Used for: AI model caching (VALET), temporary calculations, query results
- **Certified Data**: Integrity-verified data (ICP_ID, critical validations)

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

**ICP State Persistence:**
- State changes written to stable memory atomically
- Canister upgrades preserve state in stable memory
- State machine transitions validated before execution
- Certified data ensures state integrity

#### FR3.2: Base/Optimism/L2 State Storage

**L2 State Storage:**
- **Contract Storage**: Persistent storage for critical state (campaigns, transactions, ownership)
  - Stored in contract state variables
  - Used for: campaign configs, transaction logs, PVT ownership, redemption records
  - Gas-optimized storage patterns (packed structs, mappings)
- **Memory**: Temporary storage (cleared after transaction)
  - Used for: Temporary calculations, query results
  - No persistent caching (recalculate on each call)

**L2 State Persistence:**
- State changes written to contract storage (on-chain, immutable)
- Contract upgrades require proxy patterns or migration
- State machine transitions validated in smart contract logic
- Blockchain immutability ensures state integrity

**Protocol-Agnostic Validation:** Test scenarios validate state transitions match expected behavior. Python model ensures state machine logic is correct before protocol-specific deployment.

---

### FR4: Authentication & Authorization (Protocol-Specific)

**Requirement:** All state-changing operations must be authenticated. Authentication mechanism is protocol-specific, but authorization logic is protocol-agnostic.

**ICP Internet Identity Integration:**
- ICP_ID canister wraps ICP's Internet Identity system
- Decentralized identity without private key management
- Principal-based authentication for all canister calls
- Network-enforced authentication (tamperproof)

**Flow:**
1. Agent (canister) wants to execute command
2. Agent → ICP_ID canister: `auth.verify_principal(principal)` (inter-canister call)
3. ICP_ID validates principal via Internet Identity
4. ICP_ID → Agent: Authentication result (certified data)
5. If valid, command proceeds; if invalid, command rejected (network-enforced)

**Critical Commands Requiring Auth:**
- PVT minting (FOLIO)
- Fund disbursement (PAYOUT/PAYME)
- DPP minting (PORTE)
- Campaign activation (VALET)

**ICP Security Benefits:**
- Network-enforced authentication (cannot be bypassed)
- No private key management required (Internet Identity handles this)
- Tamperproof principal verification
- Certified authentication results

**Validation:** Security test scenarios verify unauthorized commands are rejected. Python model validates authentication logic before ICP deployment.

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

#### Option A: Internet Computer (ICP) Deployment
- **Languages**: Motoko (primary) or Rust (alternative)
- **Network**: Internet Computer (ICP) mainnet
- **Deployment**: Each agent as ICP canister
- **Storage**: Stable memory for persistent state
- **Authentication**: Internet Identity via ICP_ID canister
- **Communication**: Inter-canister calls (A2A protocol)
- **Security**: Network-enforced tamperproof execution
- **Multi-chain**: Chain Fusion for token operations across blockchains

#### Option B: Base (Ethereum L2) Deployment
- **Languages**: Solidity (primary) or Vyper (alternative)
- **Network**: Base mainnet (Ethereum L2)
- **Deployment**: Each agent as smart contract(s)
- **Storage**: Contract storage (gas-optimized)
- **Authentication**: Wallet signatures (EIP-712) via IdentityContract
- **Communication**: Contract function calls (A2A protocol)
- **Security**: Smart contract security (reentrancy guards, access control)
- **Multi-chain**: Base bridge for cross-chain operations

#### Option C: Optimism (Ethereum L2) Deployment
- **Languages**: Solidity (primary) or Vyper (alternative)
- **Network**: Optimism mainnet (Ethereum L2)
- **Deployment**: Each agent as smart contract(s)
- **Storage**: Contract storage (gas-optimized)
- **Authentication**: Wallet signatures (EIP-712) via IdentityContract
- **Communication**: Contract function calls (A2A protocol)
- **Security**: Optimistic rollup security model
- **Multi-chain**: Optimism bridge for cross-chain operations

#### Option D: General L2 Deployment
- **Languages**: Solidity (for EVM-compatible L2s) or L2-specific languages
- **Network**: Any Ethereum-compatible L2 (Arbitrum, Polygon, zkSync, etc.)
- **Deployment**: Each agent as smart contract(s)
- **Storage**: L2-specific storage mechanisms
- **Authentication**: L2-specific authentication (wallet-based for EVM L2s)
- **Communication**: L2-specific communication mechanisms
- **Security**: L2-specific security model (zk-proofs, optimistic rollups, etc.)
- **Multi-chain**: L2-specific bridge mechanisms

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

3. **Multi-Protocol Deployment Strategy**: Support multiple blockchain protocols
   - **ICP**: Canister-based deployment (isolation, stable memory, network-enforced security)
   - **Base/Optimism/L2**: Smart contract deployment (gas-optimized, wallet-based auth)
   - Same agent logic, different deployment mechanisms
   - Protocol-specific optimizations (libraries for L2s, sub-agents for ICP)

4. **Protocol-Specific Authentication**: Decentralized authentication per protocol
   - **ICP**: Internet Identity (no private keys, network-enforced)
   - **Base/Optimism/L2**: Wallet signatures (EIP-712, user-controlled keys)
   - Same authorization logic, different authentication mechanisms

5. **Mock Data Testing**: Test logic without external dependencies (protocol-agnostic)
   - Validates business rules before any protocol deployment
   - Tests state transitions and agent coordination
   - Scoring system for quantitative validation
   - All tests are protocol-agnostic

6. **Graph Validation**: Ensure network integrity before deployment (protocol-agnostic)
   - Validates agent communication patterns (protocol-agnostic)
   - Ensures all agents are reachable
   - Prevents deployment of broken agent networks on any protocol

### Known Limitations

1. **Incomplete NANDA Compliance**: 35 edges have unspecified intents (must be specified before ICP deployment)
2. **Mock Data Only**: No real wallet/blockchain integration (Python model phase)
3. **Python Model Only**: Not actual ICP canister deployment (next phase)
4. **Limited Error Handling**: Some edge cases may not be fully handled (to be addressed in canister implementation)
5. **No Performance Testing**: Focus is on logic validation, not canister performance
6. **No Chain Fusion Implementation**: Multi-chain token operations not yet implemented (Python model phase)
7. **No Self-Writing AI Integration**: VALET's AI capabilities are modeled but not connected to actual AI services

### Protocol Deployment Readiness

**Ready for Any Protocol Deployment (Protocol-Agnostic):**
- ✅ Agent architecture defined (14 agents with roles and responsibilities)
- ✅ A2A communication patterns validated (NANDA protocol - protocol-agnostic)
- ✅ State machine logic tested (16 test scenarios - protocol-agnostic)
- ✅ Business logic validated (11 business logic tests - protocol-agnostic)
- ✅ Security patterns tested (10 security scenarios - protocol-agnostic)
- ✅ Graph integrity validated (all agents reachable - protocol-agnostic)

**Before Protocol-Specific Deployment:**

**For ICP Deployment:**
- ⚠️ Specify all NANDA intents (35 edges need specification)
- ⚠️ Implement canisters in Motoko/Rust
- ⚠️ Integrate Internet Identity (ICP_ID canister)
- ⚠️ Implement stable memory storage
- ⚠️ Add Chain Fusion for multi-chain operations
- ⚠️ Connect VALET to AI services for self-writing capabilities

**For Base/Optimism/L2 Deployment:**
- ⚠️ Specify all NANDA intents (35 edges need specification)
- ⚠️ Implement smart contracts in Solidity/Vyper
- ⚠️ Integrate wallet authentication (EIP-712 signatures)
- ⚠️ Implement contract storage (gas-optimized)
- ⚠️ Add bridge integration for multi-chain operations
- ⚠️ Implement access control patterns (RBAC, modifiers)
- ⚠️ Security audits (reentrancy, access control, gas optimization)
- ⚠️ Connect VALET to AI services for self-writing capabilities

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

### B. Agent Roles and Canister Mapping

**Brand-Facing:**
- VALET (main agent, own canister with PORTE sub-agent)
- PORTE (sub-agent, shares VALET canister)
- DASHB (main agent, own canister with DASHC sub-agent)
- DASHC (sub-agent, shares DASHB canister)
- PROMO (own canister)

**Shopper-Facing:**
- SHOPI (own canister)
- FOLIO (own canister)
- RIDIM (own canister)
- MIRO/BRAT (external, integration TBD)

**Finance:**
- MARKT (own canister)
- PAYME (own canister)
- DEFIME (own canister)
- PAYOUT (under consideration, own canister if implemented)

**Identity:**
- ICP_ID (own canister)

**Canister Summary:**
- 10 confirmed canisters (VALET+PORTE, DASHB+DASHC, SHOPI, MARKT, RIDIM, PROMO, FOLIO, PAYME, DEFIME, ICP_ID)
- 1 under consideration (PAYOUT)
- 1 external integration (MIRO/BRAT)

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
