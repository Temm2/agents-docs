from __future__ import annotations

from typing import List

from .agents import ramm_agents, ramm_edges


def mermaid_agent_flow() -> str:
    """
    Build a Mermaid diagram definition focusing on agent behavior & flows.

    This is meant for docs / whiteboarding – rendered by tools that support
    Mermaid (e.g. Markdown preview, pymermaid, or web UIs).
    """

    lines: List[str] = []
    lines.append("flowchart LR")

    for agent in ramm_agents():
        label = f"{agent.code}:::{agent.role.value.replace('-', '_')}"
        lines.append(f"  {agent.code}[\"{agent.name}\"]")
        lines.append(f"  class {agent.code} {agent.role.value.replace('-', '_')}")

    for edge in ramm_edges():
        lines.append(f"  {edge.source} -->|{edge.description}| {edge.target}")

    # Simple CSS classes by role
    lines.append("  classDef brand-facing fill:#FFECB3,stroke:#FF8C42,stroke-width:2px;")
    lines.append("  classDef shopper-facing fill:#BBDEFB,stroke:#3FA7D6,stroke-width:2px;")
    lines.append("  classDef finance fill:#C8E6C9,stroke:#7AC74F,stroke-width:2px;")
    lines.append("  classDef data-analytics fill:#EDE7F6,stroke:#9B5DE5,stroke-width:2px;")
    lines.append("  classDef identity fill:#F8BBD0,stroke:#FF6F91,stroke-width:2px;")
    lines.append("  classDef utility fill:#FFF9C4,stroke:#F9C74F,stroke-width:2px;")

    return "\n".join(lines)


if __name__ == "__main__":
    print(mermaid_agent_flow())

