"""
ICP Canister Architecture Assumptions for RAMM Agents.

This module maps Python agents to ICP canister locations and assumptions.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from .agents import Agent, ramm_agents


class CanisterLocation:
    """Represents where a canister would be deployed on ICP."""

    def __init__(
        self,
        agent_code: str,
        canister_id: Optional[str] = None,
        subnet: str = "mainnet",
        canister_type: str = "application",
        storage_type: str = "stable_memory",
    ):
        self.agent_code = agent_code
        self.canister_id = canister_id or f"{agent_code.lower()}-canister-id"
        self.subnet = subnet
        self.canister_type = canister_type
        self.storage_type = storage_type


def get_canister_mapping() -> Dict[str, CanisterLocation]:
    """
    Map each agent to its assumed ICP canister location.

    Assumptions:
    - Each agent = one canister (or canister group)
    - Canisters communicate via inter-canister calls
    - State stored in stable memory
    - Some agents may share canisters (e.g., data canisters)
    """
    agents = ramm_agents()
    mapping = {}

    for agent in agents:
        # Determine canister type based on agent kind
        if agent.kind.value == "data-canister":
            canister_type = "data"
            storage_type = "stable_memory"  # Append-only logs
        elif agent.kind.value == "finance-canister":
            canister_type = "finance"
            storage_type = "stable_memory"  # Critical financial data
        elif agent.kind.value == "identity-layer":
            canister_type = "identity"
            storage_type = "certified_data"  # ICP Identity integration
        elif agent.kind.value == "self-writing-ai":
            canister_type = "application"
            storage_type = "stable_memory + heap"  # AI models + state
        else:
            canister_type = "application"
            storage_type = "stable_memory"

        mapping[agent.code] = CanisterLocation(
            agent_code=agent.code,
            canister_id=f"{agent.code.lower()}-canister",
            subnet="mainnet",  # Could be different subnets for different agents
            canister_type=canister_type,
            storage_type=storage_type,
        )

    return mapping


def get_canister_groups() -> Dict[str, List[str]]:
    """
    Group agents that might share canisters or be deployed together.

    Assumptions:
    - Brand-facing agents might be in same subnet
    - Finance agents need high security subnet
    - Data analytics can share infrastructure
    """
    return {
        "brand_services": ["VALET", "PORTE", "DASHB", "PROMO"],
        "shopper_services": ["SHOPI", "DASHC", "FOLIO", "MIRO"],
        "finance_services": ["PAYME", "DEFIME", "PAYOUT"],
        "marketplace": ["MARKT"],
        "redemption": ["RIDIM"],
        "identity": ["ICP_ID"],
    }


def explain_canister_assumptions() -> str:
    """Generate human-readable explanation of ICP canister assumptions."""

    mapping = get_canister_mapping()
    groups = get_canister_groups()

    explanation = """
# ICP Canister Architecture Assumptions

## Overview
Each Python agent maps to an ICP canister. Canisters communicate via inter-canister calls (A2A).

## Canister Locations

### Individual Canisters
"""
    for agent_code, location in mapping.items():
        explanation += f"""
**{agent_code}** ({location.canister_type} canister)
- Canister ID: `{location.canister_id}`
- Subnet: {location.subnet}
- Storage: {location.storage_type}
- Communication: Inter-canister calls (A2A)
"""

    explanation += "\n### Canister Groups (Logical Grouping)\n"
    for group_name, agent_codes in groups.items():
        explanation += f"""
**{group_name.replace('_', ' ').title()}**
- Agents: {', '.join(agent_codes)}
- May share subnet or infrastructure
- Coordinate via A2A calls
"""

    explanation += """
## Key Assumptions

1. **One Agent = One Canister** (typically)
   - Each agent has its own canister for isolation
   - Exception: Data canisters may aggregate multiple agents

2. **Inter-Canister Calls = A2A Communication**
   - Python A2A edges → ICP inter-canister calls
   - NANDA protocol structures these calls
   - Async, non-atomic (need state machines)

3. **State Storage**
   - Critical state: Stable memory (persistent)
   - Temporary state: Heap memory (cleared on upgrade)
   - AI models: Stable memory + heap (caching)

4. **Subnet Distribution**
   - Finance canisters: High-security subnet
   - Brand services: Standard subnet
   - Identity: ICP Identity integration

5. **Communication Flow**
   - Agent A (canister) → Inter-canister call → Agent B (canister)
   - All calls authenticated via ICP_ID
   - State changes tracked via events
"""

    return explanation


if __name__ == "__main__":
    print(explain_canister_assumptions())
