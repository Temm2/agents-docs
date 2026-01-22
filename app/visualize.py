"""
Enhanced visualization using Mermaid, Rich, and Pydantic for RAMM agents.
"""

from __future__ import annotations

from typing import Dict, List

from rich.console import Console
from rich.table import Table
from rich.tree import Tree
from rich.panel import Panel
from rich import box

from .agents import Agent, ramm_agents, ramm_edges
from .icp_architecture import get_canister_mapping, get_canister_groups
from .test_logic import run_all_tests, TestScore
from .business_logic import run_all_business_logic_tests
from .validate import run_all_checks
from .nanda_validator import validate_nanda_compliance


def generate_mermaid_architecture() -> str:
    """Generate Mermaid diagram showing agents → canisters → ICP."""

    mapping = get_canister_mapping()
    groups = get_canister_groups()
    edges = ramm_edges()

    mermaid = """graph TB
    subgraph ICP["🌐 Internet Computer (ICP)"]
        subgraph Subnet1["Subnet: Brand Services"]
            VALET_Can["VALET Canister<br/>Campaign Orchestrator"]
            PORTE_Can["PORTE Canister<br/>DPP Engine"]
            DASHB_Can["DASHB Canister<br/>Brand Dashboard"]
            PROMO_Can["PROMO Canister<br/>Promotion Engine"]
        end
        
        subgraph Subnet2["Subnet: Shopper Services"]
            SHOPI_Can["SHOPI Canister<br/>Shopping Assistant"]
            DASHC_Can["DASH-C Canister<br/>Shopper Analytics"]
            FOLIO_Can["FOLIO Canister<br/>Portfolio Manager"]
            MIRO_Can["MIRO Canister<br/>Visual Feedback"]
        end
        
        subgraph Subnet3["Subnet: Finance (High Security)"]
            PAYME_Can["PAYME Canister<br/>Payments & Escrow"]
            DEFIME_Can["DEFIME Canister<br/>Yield Engine"]
            PAYOUT_Can["PAYOUT Canister<br/>Settlement"]
        end
        
        subgraph Subnet4["Subnet: Marketplace"]
            MARKT_Can["MARKT Canister<br/>AMM Marketplace"]
        end
        
        subgraph Subnet5["Subnet: Redemption"]
            RIDIM_Can["RIDIM Canister<br/>Redemption Engine"]
        end
        
        subgraph Subnet6["Subnet: Identity"]
            ICP_ID_Can["ICP_ID Canister<br/>Auth & Traceability"]
        end
    end
    
    %% A2A Communication (key flows)
    VALET_Can -->|notify| PROMO_Can
    VALET_Can -->|command| PAYME_Can
    VALET_Can -->|event| DASHB_Can
    SHOPI_Can -->|request| MARKT_Can
    SHOPI_Can -->|command| FOLIO_Can
    SHOPI_Can -->|command| PAYME_Can
    FOLIO_Can -->|command| RIDIM_Can
    RIDIM_Can -->|query| VALET_Can
    RIDIM_Can -->|command| PORTE_Can
    MARKT_Can -->|event| PAYOUT_Can
    PAYME_Can -->|command| DEFIME_Can
    
    %% Auth layer (all agents authenticate)
    VALET_Can -.->|auth| ICP_ID_Can
    SHOPI_Can -.->|auth| ICP_ID_Can
    FOLIO_Can -.->|auth| ICP_ID_Can
    PAYME_Can -.->|auth| ICP_ID_Can
    
    style VALET_Can fill:#667eea,stroke:#764ba2,color:#fff
    style SHOPI_Can fill:#667eea,stroke:#764ba2,color:#fff
    style PAYME_Can fill:#e74c3c,stroke:#c0392b,color:#fff
    style MARKT_Can fill:#f39c12,stroke:#d68910,color:#fff
    style ICP_ID_Can fill:#2ecc71,stroke:#27ae60,color:#fff
"""

    return mermaid


def generate_mermaid_test_flow() -> str:
    """Generate Mermaid flowchart showing test execution flow."""

    mermaid = """flowchart TD
    Start([Start Testing]) --> Logic[Run Logic Tests<br/>16 Scenarios]
    Start --> Business[Run Business Logic Tests<br/>11 Calculations]
    Start --> Graph[Run Graph Validation]
    Start --> NANDA[Run NANDA Compliance]
    
    Logic --> LogicResults{All Pass?}
    Business --> BusinessResults{All Pass?}
    Graph --> GraphResults{All Pass?}
    NANDA --> NANDAResults{All Pass?}
    
    LogicResults -->|Yes| LogicPass[✅ Logic Tests Pass]
    LogicResults -->|No| LogicFail[❌ Logic Tests Fail<br/>Check individual scenarios]
    
    BusinessResults -->|Yes| BusinessPass[✅ Business Logic Pass]
    BusinessResults -->|No| BusinessFail[❌ Business Logic Fail<br/>Check calculations]
    
    GraphResults -->|Yes| GraphPass[✅ Graph Valid]
    GraphResults -->|No| GraphFail[❌ Graph Invalid<br/>Check edges/nodes]
    
    NANDAResults -->|Yes| NANDAPass[✅ NANDA Compliant]
    NANDAResults -->|No| NANDAFail[❌ NANDA Issues<br/>Fix intents/performatives]
    
    LogicPass --> Report[Generate Report]
    BusinessPass --> Report
    GraphPass --> Report
    NANDAPass --> Report
    
    LogicFail --> Report
    BusinessFail --> Report
    GraphFail --> Report
    NANDAFail --> Report
    
    Report --> End([End])
    
    style Start fill:#667eea,stroke:#764ba2,color:#fff
    style End fill:#667eea,stroke:#764ba2,color:#fff
    style LogicPass fill:#2ecc71,stroke:#27ae60,color:#fff
    style BusinessPass fill:#2ecc71,stroke:#27ae60,color:#fff
    style GraphPass fill:#2ecc71,stroke:#27ae60,color:#fff
    style NANDAPass fill:#2ecc71,stroke:#27ae60,color:#fff
    style LogicFail fill:#e74c3c,stroke:#c0392b,color:#fff
    style BusinessFail fill:#e74c3c,stroke:#c0392b,color:#fff
    style GraphFail fill:#e74c3c,stroke:#c0392b,color:#fff
    style NANDAFail fill:#e74c3c,stroke:#c0392b,color:#fff
"""

    return mermaid


def print_rich_test_summary() -> None:
    """Print beautiful test summary using Rich."""

    console = Console()

    # Run all tests
    logic_results = run_all_tests()
    business_results = run_all_business_logic_tests()
    validation_ok, validation_messages = run_all_checks()
    nanda_ok, nanda_messages = validate_nanda_compliance()

    # Create summary table
    table = Table(title="RAMM Agent Test Summary", box=box.ROUNDED)
    table.add_column("Test Category", style="cyan", no_wrap=True)
    table.add_column("Total", justify="right", style="magenta")
    table.add_column("Passed", justify="right", style="green")
    table.add_column("Failed", justify="right", style="red")
    table.add_column("Status", justify="center")

    # Logic tests
    logic_passed = sum(1 for _, (_, score) in logic_results.items() if score.result.value == "PASS")
    logic_failed = len(logic_results) - logic_passed
    logic_status = "✅" if logic_failed == 0 else "⚠️"
    table.add_row("Logic Tests", str(len(logic_results)), str(logic_passed), str(logic_failed), logic_status)

    # Business logic
    table.add_row(
        "Business Logic",
        str(business_results["total"]),
        str(business_results["passed"]),
        str(business_results["failed"]),
        "✅" if business_results["failed"] == 0 else "❌",
    )

    # Graph validation
    table.add_row("Graph Validation", "1", "1" if validation_ok else "0", "0" if validation_ok else "1", "✅" if validation_ok else "❌")

    # NANDA compliance
    table.add_row("NANDA Compliance", "1", "1" if nanda_ok else "0", "0" if nanda_ok else "1", "✅" if nanda_ok else "❌")

    console.print(table)

    # Detailed logic test results
    console.print("\n[bold cyan]Logic Test Details:[/bold cyan]")
    for name, (timeline, score) in logic_results.items():
        status_color = "green" if score.result.value == "PASS" else ("yellow" if score.result.value == "PARTIAL" else "red")
        status_icon = "✅" if score.result.value == "PASS" else ("⚠️" if score.result.value == "PARTIAL" else "❌")
        console.print(
            f"{status_icon} [bold]{name}[/bold]: {score.earned_points}/{score.total_points} ({score.percentage:.1f}%)",
            style=status_color,
        )


def generate_agent_state_tree() -> Tree:
    """Generate Rich tree showing agent states and relationships."""

    agents = ramm_agents()
    edges = ramm_edges()
    tree = Tree("🌐 RAMM Agent Ecosystem")

    # Group by role
    by_role: Dict[str, List[Agent]] = {}
    for agent in agents:
        role = agent.role.value
        if role not in by_role:
            by_role[role] = []
        by_role[role].append(agent)

    for role, role_agents in by_role.items():
        role_node = tree.add(f"📦 {role.replace('-', ' ').title()}")
        for agent in role_agents:
            # Count outbound edges
            outbound_count = len([e for e in edges if e.source == agent.code])
            inbound_count = len([e for e in edges if e.target == agent.code])
            agent_node = role_node.add(
                f"{agent.code} - {agent.name} [dim](→{outbound_count} ←{inbound_count})[/dim]"
            )
            if agent.tools:
                tools_node = agent_node.add("Tools")
                for tool in agent.tools[:3]:  # Show first 3
                    tools_node.add(tool)
                if len(agent.tools) > 3:
                    tools_node.add(f"... and {len(agent.tools) - 3} more")

    return tree


if __name__ == "__main__":
    console = Console()
    console.print(generate_agent_state_tree())
    console.print("\n")
    print_rich_test_summary()
