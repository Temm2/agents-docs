from __future__ import annotations

from typing import Tuple

import matplotlib.pyplot as plt
import networkx as nx

from .agents import AgentRole, ramm_agents, ramm_edges


def build_agent_graph() -> nx.DiGraph:
    """Construct directed A2A graph of all RAMM agents."""

    g = nx.DiGraph()

    for agent in ramm_agents():
        g.add_node(
            agent.code,
            label=agent.name,
            role=agent.role.value,
        )

    for edge in ramm_edges():
        g.add_edge(edge.source, edge.target, label=edge.description)

    return g


def role_color(role: str) -> str:
    """Simple palette keyed by AgentRole."""

    return {
        AgentRole.BRAND.value: "#FF8C42",
        AgentRole.SHOPPER.value: "#3FA7D6",
        AgentRole.FINANCE.value: "#7AC74F",
        AgentRole.DATA.value: "#9B5DE5",
        AgentRole.IDENTITY.value: "#FF6F91",
        AgentRole.UTILITY.value: "#F9C74F",
    }.get(role, "#CCCCCC")


def draw_agent_graph(g: nx.DiGraph) -> Tuple[plt.Figure, plt.Axes]:
    """
    Visualize the A2A agent network with matplotlib.

    - Node color encodes agent role (brand, shopper, finance, etc.)
    - Directed edges show who calls whom.
    """

    pos = nx.spring_layout(g, seed=42, k=0.8)

    fig, ax = plt.subplots(figsize=(10, 8))
    roles = nx.get_node_attributes(g, "role")

    node_colors = [role_color(roles.get(n, "")) for n in g.nodes]

    nx.draw_networkx_nodes(
        g,
        pos,
        node_color=node_colors,
        node_size=900,
        ax=ax,
        linewidths=1.0,
        edgecolors="black",
    )
    nx.draw_networkx_labels(g, pos, labels={n: n for n in g.nodes}, font_size=8, ax=ax)
    nx.draw_networkx_edges(
        g,
        pos,
        arrowstyle="->",
        arrowsize=12,
        width=1.0,
        edge_color="#555555",
        ax=ax,
    )

    ax.set_title("RAMM Agent A2A Network (Python Model)")
    ax.axis("off")

    fig.tight_layout()
    return fig, ax


if __name__ == "__main__":
    graph = build_agent_graph()
    fig, _ = draw_agent_graph(graph)
    fig.savefig("ramm_agents_graph.png", dpi=150)

