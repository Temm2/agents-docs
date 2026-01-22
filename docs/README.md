## RAMM Agents – Web3 Agentic E‑Commerce (Python + ICP)

This repo models the **RAMM.AI agentic commerce stack** in Python, designed to map cleanly onto ICP canisters later. It focuses on **agent behavior, state transitions, and decision flows**, not low-level canister plumbing.

### Tech Stack
- **Language**: Python 3
- **Network target**: Internet Computer (ICP) – modeled conceptually here
- **Core libs**:
  - `networkx` – agent network & decision graph modeling
  - `matplotlib` – static visualizations of agent graphs
  - `pymermaid` – export Mermaid diagrams from Python
  - `python-dotenv` – environment / config loading
  - `rich` – timelines & structured state logs
  - `pydantic` – agent state & snapshots
  - `streamlit` – agent dashboard & live exploration

### Quickstart

```bash
cd /Users/admin/Documents/rammagents
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the **Streamlit agent dashboard**:

```bash
streamlit run app/dashboard.py
```

This loads the RAMM agents, builds an **agent interaction graph**, and renders:
- Agent list + roles
- A2A communication edges
- State machine and decision flow snapshots

### Project Layout

- `app/`
  - `agents.py` – Pydantic models for all core agents (VALET, PORTE, DASHB, RIDIM, MARKT, SHOPI, DASH-C, FOLIO, PROMO, PAYME, DEFIME, ICP_ID, MIRO/BRAT)
  - `state.py` – generic agent state, events, and timelines (Rich + Pydantic)
  - `graph.py` – `networkx` models of A2A communication & decision flows
  - `viz_matplotlib.py` – matplotlib visualizations of the agent network
  - `viz_mermaid.py` – Mermaid diagram generation for docs / design sharing
  - `dashboard.py` – Streamlit dashboard for interactive exploration
- `.env.example` – configuration template (e.g. environment, ICP endpoints)

### ICP Alignment (Conceptual)

- Each Python `Agent` instance corresponds conceptually to an **ICP canister**.
- A2A calls are represented as **directed edges** in `networkx`.
- **State transitions** and **decision flows** are logged as timelines and can be replayed or visualized without needing a live ICP subnet.

