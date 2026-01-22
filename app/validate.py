"""
Lightweight integrity checks across RAMM agents and edges.

These checks are meant to catch missing nodes/edges or orphaned references in
the Python model before you align with ICP canisters.
"""

from __future__ import annotations

from typing import List, Tuple

import networkx as nx

from .agents import ramm_agents, ramm_edges
from .graph import build_agent_graph


def check_missing_nodes() -> List[str]:
    """Find edges that point to unknown agents."""

    codes = {a.code for a in ramm_agents()}
    errors: List[str] = []
    for edge in ramm_edges():
        if edge.source not in codes or edge.target not in codes:
            errors.append(f"Edge {edge.source} -> {edge.target} references unknown agent")
    return errors


def check_isolated_agents(g: nx.DiGraph) -> List[str]:
    """Agents with no in/out edges."""

    isolated = list(nx.isolates(g))
    return [f"Agent {code} is isolated (no A2A edges)" for code in isolated]


def check_reachability(g: nx.DiGraph) -> List[str]:
    """
    Report agents unreachable from brand/consumer entry points.

    Entry points considered: VALET (brand), SHOPI (shopper).
    """

    errors: List[str] = []
    entry_points = ["VALET", "SHOPI"]
    reachable = set()
    for src in entry_points:
        if src in g:
            reachable |= nx.descendants(g, src) | {src}

    for node in g.nodes:
        # ICP_ID is a shared infra layer; we still expect it to be reachable, but
        # it may only be called (edges into it), not called *from* entry points.
        # Our A2A model includes explicit edges to ICP_ID now, so keep it strict.
        if node not in reachable:
            errors.append(f"Agent {node} unreachable from VALET/SHOPI entry points")
    return errors


def run_all_checks() -> Tuple[bool, List[str]]:
    """Run all integrity checks and aggregate results."""

    messages: List[str] = []
    g = build_agent_graph()

    messages.extend(check_missing_nodes())
    messages.extend(check_isolated_agents(g))
    messages.extend(check_reachability(g))

    ok = len(messages) == 0
    if ok:
        messages.append("All graph integrity checks passed.")
    return ok, messages


if __name__ == "__main__":
    ok, msgs = run_all_checks()
    header = "[PASS]" if ok else "[FAIL]"
    print(header)
    for m in msgs:
        print(f"- {m}")

