# RAMM Agents – Web3 Agentic E‑Commerce (Python + ICP)

This repository models the **RAMM.AI agentic commerce stack** in Python, designed to map cleanly onto ICP canisters later. It focuses on **agent behavior, state transitions, and decision flows**, not low-level canister plumbing.

## 🎯 Overview

RAMM Agents is a modular, agent-based architecture for Web3 commerce built on the Internet Computer (ICP). The system enables brands to launch tokenized commerce campaigns, shoppers to buy/promote/redeem products, and influencers to earn rewards, all coordinated through peer-to-peer (A2A) communication.

### Key Agents

- **VALET** – Campaign management, brand onboarding, AI-generated campaigns
- **SHOPI** – Shopping journey, personalization, product recommendations
- **MARKT** – Core AMM, manages swaps (USDC ↔ PVT), liquidity tracking
- **FOLIO** – PVT wallet management, redemption, gifting, reselling
- **PROMO** – Influencer & affiliate management, attribution logic
- **PAYME** – Escrow handling, payment execution, reward payouts
- **RIDIM** – PVT redemption orchestration, DPP minting
- **PORTE** – Digital Product Passport (DPP) creation and NFT minting
- **DASHB** – Brand dashboard, campaign analytics, portfolio view
- **DASH-C** – Shopper analytics, engagement metrics
- **DEFIME** – Yield management, DeFi integration
- **ICP_ID** – Identity and authentication layer
- **MIRO/BRAT** – Visual feedback agent for shoppers
- **PAYOUT** – Fund withdrawal and settlement

## 🛠️ Tech Stack

- **Language**: Python 3
- **Network target**: Internet Computer (ICP) – modeled conceptually here
- **Core libraries**:
  - `networkx` – agent network & decision graph modeling
  - `matplotlib` – static visualizations of agent graphs
  - `pymermaid` – export Mermaid diagrams from Python
  - `python-dotenv` – environment / config loading
  - `rich` – timelines & structured state logs
  - `pydantic` – agent state & snapshots
  - `streamlit` – agent dashboard & live exploration

## 🚀 Quickstart

### Installation

```bash
cd /Users/admin/Documents/rammagents
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run the Streamlit Dashboard

```bash
streamlit run ramm_dashboard.py
```

This loads the RAMM agents, builds an **agent interaction graph**, and renders:
- Agent list + roles
- A2A communication edges
- State machine and decision flow snapshots
- Logic testing results
- Business logic calculations

### Run Tests

```bash
# Logic tests with mock data
python -m app.test_logic

# Business logic tests
python -m app.business_logic

# Generate test report
python -m app.report_generator
```

## 📁 Project Layout

- `app/`
  - `agents.py` – Pydantic models for all core agents and A2A edges
  - `state.py` – generic agent state, events, and timelines
  - `graph.py` – `networkx` models of A2A communication & decision flows
  - `viz_mermaid.py` – Mermaid diagram generation for docs
  - `dashboard.py` – Streamlit dashboard for interactive exploration
  - `test_logic.py` – Logic testing with mock data and scoring
  - `business_logic.py` – Business calculations (bonding curves, rewards, ROI)
  - `validate.py` – Graph integrity checks
  - `nanda_validator.py` – NANDA protocol compliance validation
  - `report_generator.py` – HTML/Markdown test report generation
- `docs/` – Documentation files for GitHub Pages
- `test_report.html` – Comprehensive test results
- `.env.example` – configuration template

## 🔗 ICP Alignment (Conceptual)

- Each Python `Agent` instance corresponds conceptually to an **ICP canister**.
- A2A calls are represented as **directed edges** in `networkx`.
- **State transitions** and **decision flows** are logged as timelines and can be replayed or visualized without needing a live ICP subnet.
- See `app/icp_architecture.py` for detailed canister mapping assumptions.

## 📚 Documentation

- **[Test Guide](TEST_GUIDE.md)** – Step-by-step explanation of agent logic tests
- **[Implementation Summary](IMPLEMENTATION_SUMMARY.md)** – What was implemented
- **[Testing](TESTING.md)** – Test pass criteria and scoring
- **[Test Scenarios](TEST_SCENARIOS.md)** – All 16 test scenarios documented
- **[State Analysis](STATE_ANALYSIS.md)** – State changes and security analysis
- **[Test Types](TEST_TYPES.md)** – Logic tests vs other test types
- **[SHOPI-VALET Connection](SHOPI_VALET_CONNECTION.md)** – How SHOPI queries campaigns

## 🌐 Live Documentation

View the complete documentation and test reports at:
**https://temm2.github.io/agents-docs/**

## 📊 Test Results

The test suite includes:
- **16 Logic Test Scenarios** (Happy Path, Security, Resilience)
- **11 Business Logic Tests** (Bonding curves, rewards, ROI, yield)
- **Graph Validation** (Missing nodes, isolated agents, reachability)
- **NANDA Protocol Compliance** (A2A communication structure)

See `test_report.html` for complete results.

## 🤝 Contributing

This is a modeling and testing framework for RAMM agents. Each agent is designed to be implemented as an ICP canister with deterministic state rules and peer-to-peer communication.

