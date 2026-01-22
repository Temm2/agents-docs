from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field
from rich.console import Console
from rich.table import Table


class AgentPhase(str, Enum):
    IDLE = "idle"
    CONFIGURING = "configuring"
    ACTIVE = "active"
    SETTLING = "settling"
    COMPLETED = "completed"
    ERROR = "error"


class AgentSnapshot(BaseModel):
    """Snapshot of an agent's state at a point in time."""

    agent_code: str
    phase: AgentPhase
    ts: datetime = Field(default_factory=datetime.utcnow)
    data: Dict[str, Any] = Field(default_factory=dict)


class EventKind(str, Enum):
    COMMAND = "command"
    A2A_CALL = "a2a-call"
    STATE_TRANSITION = "state-transition"
    ERROR = "error"


class AgentEvent(BaseModel):
    """Timeline event for visualization and logging."""

    ts: datetime = Field(default_factory=datetime.utcnow)
    agent_code: str
    kind: EventKind
    summary: str
    details: Dict[str, Any] = Field(default_factory=dict)


class Timeline(BaseModel):
    """In-memory timeline of events for a single scenario/run."""

    events: List[AgentEvent] = Field(default_factory=list)

    def add(self, event: AgentEvent) -> None:
        self.events.append(event)

    def to_table(self) -> Table:
        table = Table(title="RAMM Agent Timeline")
        table.add_column("Time")
        table.add_column("Agent")
        table.add_column("Kind")
        table.add_column("Summary")
        for e in sorted(self.events, key=lambda x: x.ts):
            table.add_row(
                e.ts.isoformat(timespec="seconds"),
                e.agent_code,
                e.kind.value,
                e.summary,
            )
        return table

    def print_rich(self, console: Optional[Console] = None) -> None:
        console = console or Console()
        console.print(self.to_table())


def simulate_sample_campaign_timeline() -> Timeline:
    """
    Create a simple, deterministic sample timeline that shows:
    - VALET configuring a campaign
    - PROMO preparing influencer content
    - SHOPI driving a purchase
    - FOLIO + PAYME executing and settling
    """

    tl = Timeline()

    tl.add(
        AgentEvent(
            agent_code="VALET",
            kind=EventKind.COMMAND,
            summary="Brand Manager configures SMART CAMPAIGN PopUpz #1",
            details={"campaignId": "CAMP-001"},
        )
    )
    tl.add(
        AgentEvent(
            agent_code="VALET",
            kind=EventKind.STATE_TRANSITION,
            summary="VALET → ACTIVE (campaign published)",
            details={"phase": AgentPhase.ACTIVE.value},
        )
    )
    tl.add(
        AgentEvent(
            agent_code="VALET",
            kind=EventKind.A2A_CALL,
            summary="VALET notifies PROMO about new SMART CAMPAIGN",
            details={"target": "PROMO"},
        )
    )
    tl.add(
        AgentEvent(
            agent_code="PROMO",
            kind=EventKind.COMMAND,
            summary="PROMO generates influencer content & reward tiers",
            details={"campaignId": "CAMP-001"},
        )
    )
    tl.add(
        AgentEvent(
            agent_code="SHOPI",
            kind=EventKind.COMMAND,
            summary="SHOPI recommends campaign PopUpz #1 to shopper",
            details={"campaignId": "CAMP-001"},
        )
    )
    tl.add(
        AgentEvent(
            agent_code="SHOPI",
            kind=EventKind.A2A_CALL,
            summary="SHOPI calls FOLIO + PAYME to execute purchase",
            details={"targets": ["FOLIO", "PAYME"]},
        )
    )
    tl.add(
        AgentEvent(
            agent_code="FOLIO",
            kind=EventKind.STATE_TRANSITION,
            summary="FOLIO mints PVT for shopper portfolio",
            details={"pvtId": "PVT-001"},
        )
    )
    tl.add(
        AgentEvent(
            agent_code="PAYME",
            kind=EventKind.STATE_TRANSITION,
            summary="PAYME settles escrow and routes funds to DEFIME",
            details={"amount": "100 USDC"},
        )
    )

    return tl

