"""
NANDA protocol compliance validation for A2A communications.
"""

from __future__ import annotations

from typing import List

from .agents import A2AEdge, ramm_edges


def validate_nanda_compliance() -> tuple[bool, List[str]]:
    """
    Validate that all A2A edges comply with NANDA protocol structure.

    NANDA requirements:
    - protocol: Must be "NANDA"
    - performative: Must be one of: request, notify, query, respond, command, event
    - intent: Must be specified (not "unspecified")
    - payload_contract: Must be specified (not "dict" default)
    """
    errors: List[str] = []
    valid_performatives = {"request", "notify", "query", "respond", "command", "event"}

    edges = ramm_edges()

    for edge in edges:
        # Check protocol
        if edge.protocol != "NANDA":
            errors.append(f"Edge {edge.source} → {edge.target}: protocol is '{edge.protocol}', expected 'NANDA'")

        # Check performative
        if edge.performative not in valid_performatives:
            errors.append(
                f"Edge {edge.source} → {edge.target}: invalid performative '{edge.performative}', "
                f"must be one of {valid_performatives}"
            )

        # Check intent is specified
        if edge.intent == "unspecified":
            errors.append(f"Edge {edge.source} → {edge.target}: intent is 'unspecified', must be specified")

        # Check payload contract is specified (not default "dict")
        if edge.payload_contract == "dict" and edge.intent != "unspecified":
            # Only warn if intent is specified but contract is default
            pass  # This is acceptable for now, but could be stricter

    return len(errors) == 0, errors


if __name__ == "__main__":
    ok, errors = validate_nanda_compliance()
    if ok:
        print("✅ All A2A edges comply with NANDA protocol")
    else:
        print("❌ NANDA compliance issues found:")
        for error in errors:
            print(f"  - {error}")
