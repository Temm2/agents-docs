"""
Sequence diagram helpers for RAMM agent flows.

These return Mermaid sequence definitions that can be rendered in docs or
inside the Streamlit dashboard. They focus on behavior and A2A calls, not
ICP canister internals.
"""

from __future__ import annotations

from typing import Dict


def purchase_sequence() -> str:
    """
    Shopper-led purchase flow: SHOPI → FOLIO/PAYME → DEFIME → VALET/DASHB.
    """

    return "\n".join(
        [
            "sequenceDiagram",
            "    participant Shopper",
            "    participant SHOPI",
            "    participant FOLIO",
            "    participant PAYME",
            "    participant DEFIME",
            "    participant VALET",
            "    participant DASHB",
            "",
            "    Shopper->>SHOPI: Browse marketplace",
            "    SHOPI->>VALET: Query active campaigns",
            "    VALET-->>SHOPI: Return campaign list",
            "    SHOPI->>Shopper: Show recommendations",
            "    Shopper->>SHOPI: Select campaign & buy",
            "    SHOPI->>FOLIO: Request Buy(PVT)",
            "    SHOPI->>PAYME: Authorize payment",
            "    PAYME->>FOLIO: Confirm escrow lock",
            "    PAYME->>DEFIME: Route locked funds for yield",
            "    FOLIO-->>SHOPI: Mint/transfer PVT",
            "    PAYME-->>SHOPI: Payment settled",
            "    DEFIME-->>PAYME: Return principal + yield",
            "    PAYME-->>FOLIO: Settlement update",
            "    FOLIO-->>VALET: Campaign state update",
            "    FOLIO-->>DASHB: Emit portfolio/campaign event",
            "    VALET-->>DASHB: Sync campaign metrics",
        ]
    )


def redemption_sequence() -> str:
    """
    Redemption flow: FOLIO triggers RIDIM; PORTE mints DPP; VALET issues PromoCode.
    """

    return "\n".join(
        [
            "sequenceDiagram",
            "    participant Shopper",
            "    participant FOLIO",
            "    participant RIDIM",
            "    participant VALET",
            "    participant PORTE",
            "    participant PAYME",
            "",
            "    Shopper->>FOLIO: Request redeem(PVT)",
            "    FOLIO->>RIDIM: Redemption command",
            "    RIDIM->>VALET: Validate redemption window & rules",
            "    RIDIM->>PORTE: Mint DPP NFT with metadata",
            "    RIDIM->>VALET: Request PromoCode issuance",
            "    VALET-->>RIDIM: PromoCode issued",
            "    PORTE-->>Shopper: Deliver DPP NFT",
            "    RIDIM-->>FOLIO: Redemption completed",
            "    FOLIO-->>PAYME: Finalize settlement if needed",
        ]
    )


def sequence_catalog() -> Dict[str, str]:
    """Available sequence diagrams keyed by label for UI selection."""

    return {
        "Purchase flow (SHOPI → FOLIO/PAYME)": purchase_sequence(),
        "Redemption flow (FOLIO → RIDIM → PORTE)": redemption_sequence(),
    }

