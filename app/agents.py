from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class AgentRole(str, Enum):
    BRAND = "brand-facing"
    SHOPPER = "shopper-facing"
    FINANCE = "finance"
    DATA = "data-analytics"
    IDENTITY = "identity"
    UTILITY = "utility"


class AgentKind(str, Enum):
    CANISTER = "canister"
    SELF_WRITING_AI = "self-writing-ai"
    DATA_CANISTER = "data-canister"
    FINANCE_CANISTER = "finance-canister"
    IDENTITY_LAYER = "identity-layer"


class A2AEdge(BaseModel):
    """Directed A2A communication edge between agents."""

    source: str
    target: str
    description: str
    # Project NANDA-style structured message metadata (lightweight, Python-first).
    # This makes A2A interactions testable as contracts rather than ad-hoc calls.
    protocol: str = "NANDA"
    performative: str = Field(
        default="request",
        description="NANDA performative (request/notify/query/respond/command/event)",
    )
    intent: str = Field(
        default="unspecified",
        description="High-level intent name for this message (NANDA intent).",
    )
    payload_contract: str = Field(
        default="dict",
        description="A human-readable payload contract (schema-ish).",
    )


class Agent(BaseModel):
    code: str = Field(..., description="Short codename, e.g. VALET, PAYME")
    name: str
    role: AgentRole
    kind: AgentKind
    description: str
    interacts_with: List[str] = Field(
        default_factory=list,
        description="Human actors (Brand Manager, Shopper, Influencer, etc.)",
    )
    tools: List[str] = Field(default_factory=list, description="Key internal tools")
    a2a_outbound: List[str] = Field(
        default_factory=list, description="Codenames of agents this agent calls"
    )


def ramm_agents() -> List[Agent]:
    """Return the core RAMM agents defined in v1.14 of the spec."""

    return [
        Agent(
            code="VALET",
            name="VALET – Campaign Orchestrator",
            role=AgentRole.BRAND,
            kind=AgentKind.SELF_WRITING_AI,
            description=(
                "End-to-end brand onboarding and SMART CAMPAIGN setup. "
                "Generates campaign pages/assets, syncs state with PROMO, "
                "coordinates PVT fund withdrawal."
            ),
            interacts_with=["Brand Manager"],
            tools=[
                "Brand Identity Config",
                "Target Audience Designer",
                "Pricing & Timing Planner",
                "Product Page Generator",
                "Bonding Curve Selector",
            ],
            a2a_outbound=["PROMO", "PAYME", "FOLIO", "LOYLT"],
        ),
        Agent(
            code="PORTE",
            name="PORTE – Digital Product Passport",
            role=AgentRole.BRAND,
            kind=AgentKind.CANISTER,
            description=(
                "Creates and mints Digital Product Passports (DPP) as NFTs, "
                "embedding product and sustainability metadata for each redemption."
            ),
            interacts_with=["Brand Manager"],
            tools=[
                "DPP Template Engine",
                "NFT Minting Logic",
                "Sustainability & Product Schemas",
                "Stable Memory Storage (DPP records)",
            ],
            a2a_outbound=["VALET", "PROMO", "RIDIM"],
        ),
        Agent(
            code="DASHB",
            name="DASHB – Brand Dashboard",
            role=AgentRole.DATA,
            kind=AgentKind.DATA_CANISTER,
            description=(
                "Real-time campaign reporting & analytics for brands. "
                "Aggregates metrics from VALET, MARKT, PROMO, and PAYOUT."
            ),
            interacts_with=["Brand Manager"],
            tools=[
                "Analytics Aggregator",
                "Time-Series Metrics Engine",
                "Brand Portfolio Selector",
                "Read-Only Query APIs",
            ],
            a2a_outbound=["VALET", "PAYOUT", "MARKT", "PROMO"],
        ),
        Agent(
            code="RIDIM",
            name="RIDIM – Redemption Orchestrator",
            role=AgentRole.SHOPPER,
            kind=AgentKind.CANISTER,
            description=(
                "Handles PVT redemption lifecycle, enforcement of timing rules, "
                "and coordination with PORTE and VALET for DPP and PromoCodes."
            ),
            interacts_with=["Shopper"],
            tools=[
                "Redemption State Machine",
                "Validation & Compliance Checks",
                "PromoCode Orchestration",
                "Inter-Canister Coordination",
            ],
            a2a_outbound=["FOLIO", "VALET", "PORTE"],
        ),
        Agent(
            code="MARKT",
            name="MARKT – Marketplace AMM",
            role=AgentRole.FINANCE,
            kind=AgentKind.CANISTER,
            description=(
                "Core AMM for PVTs vs stablecoins. Tracks trades, wallet metadata, "
                "and coordinates with PAYOUT for pool settlements."
            ),
            interacts_with=[],
            tools=[
                "Pricing Functions (Bonding Curves)",
                "Atomic Swap Execution",
                "Append-Only Transaction Log",
                "Asset Transfer Coordination APIs",
            ],
            a2a_outbound=["DASHB", "FOLIO", "PAYOUT"],
        ),
        Agent(
            code="SHOPI",
            name="SHOPI – Shopper Assistant",
            role=AgentRole.SHOPPER,
            kind=AgentKind.SELF_WRITING_AI,
            description=(
                "AI-powered shopping assistant. Renders marketplace, runs "
                "personalization in-heap, and orchestrates Buy/Promote flows."
            ),
            interacts_with=["Shopper"],
            tools=[
                "Shopper Dashboard Renderer",
                "AI Personalization Engine",
                "Recommendation Cache",
                "External Advisor (RAG) Connector",
            ],
            a2a_outbound=["PROMO", "VALET", "MIRO", "FOLIO", "PAYME", "MARKT", "DASHC"],
        ),
        Agent(
            code="DASHC",
            name="DASH-C – Shopper Analytics",
            role=AgentRole.DATA,
            kind=AgentKind.DATA_CANISTER,
            description=(
                "Aggregates real-time engagement and purchase analytics across "
                "SHOPI, PAYME, PROMO, and FOLIO."
            ),
            interacts_with=[],
            tools=[
                "Query Methods for Aggregates",
                "Event Aggregator Methods",
                "Stable Memory Store for Metrics",
            ],
            a2a_outbound=["VALET", "PAYME", "PROMO", "FOLIO"],
        ),
        Agent(
            code="FOLIO",
            name="FOLIO – Shopper Portfolio",
            role=AgentRole.SHOPPER,
            kind=AgentKind.CANISTER,
            description=(
                "Manages PVT ownership, gifting, lending, reselling, and redemption "
                "triggers. Gateway to marketplace, without direct external access."
            ),
            interacts_with=["Shopper"],
            tools=[
                "PVT Asset Registry",
                "Wallet & Portfolio Manager",
                "Event Log (on-chain)",
                "Marketplace Gateway",
            ],
            a2a_outbound=["PAYME", "RIDIM", "PROMO", "LOYLT"],
        ),
        Agent(
            code="PROMO",
            name="PROMO – Promotion & Influencer Engine",
            role=AgentRole.BRAND,
            kind=AgentKind.SELF_WRITING_AI,
            description=(
                "Manages campaign promotion, influencer attribution, reward tiers, "
                "and AI-generated content for campaigns."
            ),
            interacts_with=["Shopper", "Influencer"],
            tools=[
                "Attribution Engine",
                "Influencer Scoring System",
                "Reward Tier Logic",
                "AI Content Generator",
            ],
            a2a_outbound=["VALET", "PAYME", "SHOPI", "LOYLT"],
        ),
        Agent(
            code="PAYME",
            name="PAYME – Payments & Escrow",
            role=AgentRole.FINANCE,
            kind=AgentKind.FINANCE_CANISTER,
            description=(
                "Executes shopper payments, escrow flows, and influencer payouts. "
                "Synchronizes state with FOLIO and DEFIME."
            ),
            interacts_with=["Shopper", "Influencer"],
            tools=[
                "Escrow & Settlement Engine",
                "Payment Authorization Logic",
                "Reward Distribution Methods",
                "DeFi Routing Interface",
            ],
            a2a_outbound=["FOLIO", "PROMO", "DEFIME", "SHOPI", "VALET"],
        ),
        Agent(
            code="DEFIME",
            name="DEFIME – Yield Engine",
            role=AgentRole.FINANCE,
            kind=AgentKind.FINANCE_CANISTER,
            description=(
                "Routes locked assets into DeFi strategies, calculates yield, and "
                "returns principal + yield to PAYME or FOLIO."
            ),
            interacts_with=[],
            tools=[
                "Yield Strategy Engine",
                "DeFi Protocol Adapters",
                "Return Calculation Logic",
            ],
            a2a_outbound=["PAYME", "FOLIO"],
        ),
        Agent(
            code="ICP_ID",
            name="ICP_ID – Identity & Auth Layer",
            role=AgentRole.IDENTITY,
            kind=AgentKind.IDENTITY_LAYER,
            description=(
                "Wraps ICP Internet Identity and principal verification. "
                "Enforces role-based access and traceability across agents."
            ),
            interacts_with=["Brand", "Shopper", "Promoter", "Finance Agents"],
            tools=[
                "Internet Identity",
                "Principal Verification",
                "Auth & Trace Middleware",
            ],
            a2a_outbound=[
                "VALET",
                "SHOPI",
                "FOLIO",
                "PAYME",
                "PROMO",
                "MARKT",
                "RIDIM",
            ],
        ),
        Agent(
            code="PAYOUT",
            name="PAYOUT – Brand Settlement & Withdrawals (TBD)",
            role=AgentRole.FINANCE,
            kind=AgentKind.FINANCE_CANISTER,
            description=(
                "Settles campaign pools and enables brand withdrawals once payout "
                "conditions are met. Mentioned as interacting with DASHB and MARKT."
            ),
            interacts_with=["Brand Manager"],
            tools=[
                "Payout Condition Engine",
                "Settlement Scheduler",
                "Withdrawal Authorization",
                "Audit Log / Reporting",
            ],
            a2a_outbound=["DASHB", "VALET", "PAYME"],
        ),
        Agent(
            code="MIRO",
            name="BRAT / MIRO – Visual Feedback Agent",
            role=AgentRole.UTILITY,
            kind=AgentKind.SELF_WRITING_AI,
            description=(
                "Image-based style feedback and mockup generation agent. "
                "Gives shoppers visual try-ons and suggestions."
            ),
            interacts_with=["Shopper"],
            tools=[
                "Image Ingestion & Analysis",
                "Garment Mockup Generator",
                "Style Feedback Engine",
            ],
            a2a_outbound=["SHOPI"],
        ),
        Agent(
            code="LOYLT",
            name="LOYLT – Loyalty & Rewards Manager",
            role=AgentRole.BRAND,
            kind=AgentKind.CANISTER,
            description=(
                "Manages brand loyalty programs within the RAMM.AI ecosystem. "
                "Oversees loyalty tokens issued by brands as part of campaigns, enabling users to earn, "
                "store, redeem, and optionally trade these tokens. Loyalty tokens may be distributed "
                "alongside campaign rewards (e.g., PVT + DPP + brand-specific loyalty tokens) and can "
                "function similarly to airline miles—usable as partial payment for future brand campaigns, "
                "perks, or redemptions. Where permitted, loyalty tokens may also be swapped on secondary markets."
            ),
            interacts_with=["Brand Manager", "Shopper"],
            tools=[
                "Loyalty Token Registry (brand-scoped)",
                "Earn & Burn Rules Engine",
                "Reward Accrual & Balance Tracker",
                "Secondary Market Enablement Hooks",
                "Analytics & Loyalty Performance Signals",
            ],
            a2a_outbound=["MARKT", "PAYME", "DASHB"],
        ),
    ]


def ramm_edges() -> List[A2AEdge]:
    """Return canonical A2A communication edges based on the spec (NANDA-structured)."""

    edges: List[A2AEdge] = []

    # NANDA-ish intent/contract registry for key edges (defaults otherwise).
    # Keep contracts human-readable for now; we can promote to Pydantic schemas later.
    registry = {
        ("VALET", "PROMO"): ("notify", "campaign.created", "{campaignId, brandId, configRef}"),
        ("VALET", "PAYME"): ("command", "campaign.funding.configure", "{campaignId, poolRules}"),
        ("VALET", "FOLIO"): ("command", "campaign.assets.register", "{campaignId, pvtRules}"),
        ("VALET", "DASHB"): ("event", "campaign.state.updated", "{campaignId, state, metricsRef}"),
        ("SHOPI", "VALET"): ("query", "campaign.list_active", "{filters?, limit?, offset?}"),
        ("SHOPI", "MARKT"): ("request", "market.swap.quote_or_execute", "{wallet, side, amount, campaignId}"),
        ("SHOPI", "FOLIO"): ("command", "folio.buy_or_sell", "{wallet, action, campaignId, amount}"),
        ("SHOPI", "PAYME"): ("command", "payme.authorize", "{wallet, amount, currency, campaignId}"),
        ("SHOPI", "DASHC"): ("event", "analytics.shopper.action", "{wallet, action, campaignId}"),
        ("FOLIO", "RIDIM"): ("command", "redeem.request", "{wallet, pvtId, campaignId}"),
        ("RIDIM", "PORTE"): ("command", "dpp.mint", "{wallet, productId, campaignId, redemptionMeta}"),
        ("RIDIM", "VALET"): ("query", "campaign.redemption.validate", "{campaignId, wallet, pvtId}"),
        ("MARKT", "PAYOUT"): ("event", "pool.settlement.trigger", "{campaignId, conditionMet, totals}"),
        ("DASHB", "PAYOUT"): ("query", "payout.status", "{campaignId}"),
        ("MARKT", "DASHB"): ("event", "market.trade.logged", "{campaignId, tradeId, wallet}"),
        ("PAYME", "DEFIME"): ("command", "defi.route.locked_funds", "{campaignId, amount, strategy}"),
        ("PAYOUT", "PAYME"): ("command", "payme.disburse", "{campaignId, to, amount}"),
        ("VALET", "LOYLT"): ("notify", "loyalty.program.configure", "{campaignId, brandId, loyaltyRules, earnRates, redemptionOptions}"),
        ("FOLIO", "LOYLT"): ("event", "loyalty.purchase.event", "{wallet, campaignId, purchaseAmount, pvtCount}"),
        ("PROMO", "LOYLT"): ("event", "loyalty.promotion.event", "{wallet, campaignId, promotionType, rewardAmount}"),
        ("LOYLT", "MARKT"): ("request", "loyalty.swap.enable", "{brandId, loyaltyTokenId, swapRules}"),
        ("LOYLT", "PAYME"): ("command", "loyalty.partial_payment", "{wallet, campaignId, loyaltyTokenAmount, usdcAmount}"),
        ("LOYLT", "DASHB"): ("event", "loyalty.metrics.updated", "{brandId, campaignId, metrics, state}"),
        # PORTE edges
        ("PORTE", "VALET"): ("notify", "dpp.minted", "{dppId, campaignId, wallet, metadata}"),
        ("PORTE", "PROMO"): ("event", "dpp.mint.completed", "{dppId, campaignId, wallet}"),
        ("PORTE", "RIDIM"): ("respond", "dpp.mint.response", "{dppId, status, metadata}"),
        # DASHB edges
        ("DASHB", "VALET"): ("query", "campaign.analytics.request", "{campaignId, metricsType}"),
        ("DASHB", "MARKT"): ("query", "market.analytics.request", "{campaignId, timeRange}"),
        ("DASHB", "PROMO"): ("query", "promo.analytics.request", "{campaignId, influencerId}"),
        # RIDIM edges
        ("RIDIM", "FOLIO"): ("notify", "redemption.completed", "{pvtId, campaignId, wallet, status}"),
        # MARKT edges
        ("MARKT", "FOLIO"): ("command", "pvt.transfer", "{from, to, amount, campaignId}"),
        # SHOPI edges
        ("SHOPI", "PROMO"): ("query", "promo.recommendations", "{wallet, campaignId, preferences}"),
        ("SHOPI", "MIRO"): ("request", "visual.feedback.request", "{productId, style, preferences}"),
        # DASHC edges
        ("DASHC", "VALET"): ("event", "analytics.shopper.aggregated", "{campaignId, metrics, timeRange}"),
        ("DASHC", "PAYME"): ("query", "analytics.payment.stats", "{campaignId, wallet}"),
        ("DASHC", "PROMO"): ("event", "analytics.promo.engagement", "{campaignId, influencerId, metrics}"),
        ("DASHC", "FOLIO"): ("query", "analytics.portfolio.stats", "{wallet, campaignId}"),
        # FOLIO edges
        ("FOLIO", "PAYME"): ("notify", "pvt.minted", "{pvtId, campaignId, wallet, amount}"),
        ("FOLIO", "PROMO"): ("event", "pvt.transfer.event", "{pvtId, from, to, campaignId}"),
        # PROMO edges
        ("PROMO", "VALET"): ("notify", "promo.campaign.updated", "{campaignId, influencerId, status}"),
        ("PROMO", "PAYME"): ("command", "promo.reward.distribute", "{wallet, campaignId, rewardAmount}"),
        ("PROMO", "SHOPI"): ("event", "promo.recommendation.updated", "{campaignId, influencerId, score}"),
        # PAYME edges
        ("PAYME", "FOLIO"): ("notify", "payment.settled", "{transactionId, campaignId, amount}"),
        ("PAYME", "PROMO"): ("notify", "reward.paid", "{wallet, campaignId, amount, currency}"),
        ("PAYME", "SHOPI"): ("respond", "payment.authorization.response", "{transactionId, status, amount}"),
        ("PAYME", "VALET"): ("event", "payment.campaign.funded", "{campaignId, amount, currency}"),
        # DEFIME edges
        ("DEFIME", "PAYME"): ("notify", "yield.generated", "{campaignId, amount, yieldAmount, strategy}"),
        ("DEFIME", "FOLIO"): ("notify", "yield.distributed", "{wallet, amount, yieldAmount}"),
        # ICP_ID edges (all are auth responses)
        ("ICP_ID", "VALET"): ("respond", "auth.verify_principal.response", "{principal, verified, role}"),
        ("ICP_ID", "SHOPI"): ("respond", "auth.verify_principal.response", "{principal, verified, role}"),
        ("ICP_ID", "FOLIO"): ("respond", "auth.verify_principal.response", "{principal, verified, role}"),
        ("ICP_ID", "PAYME"): ("respond", "auth.verify_principal.response", "{principal, verified, role}"),
        ("ICP_ID", "PROMO"): ("respond", "auth.verify_principal.response", "{principal, verified, role}"),
        ("ICP_ID", "MARKT"): ("respond", "auth.verify_principal.response", "{principal, verified, role}"),
        ("ICP_ID", "RIDIM"): ("respond", "auth.verify_principal.response", "{principal, verified, role}"),
        # PAYOUT edges
        ("PAYOUT", "DASHB"): ("event", "payout.status.updated", "{campaignId, status, amount}"),
        ("PAYOUT", "VALET"): ("notify", "payout.completed", "{campaignId, amount, currency}"),
        # MIRO edges
        ("MIRO", "SHOPI"): ("respond", "visual.feedback.response", "{productId, mockup, recommendations}"),
    }

    for agent in ramm_agents():
        for target in agent.a2a_outbound:
            perf, intent, contract = registry.get(
                (agent.code, target), ("request", "unspecified", "dict")
            )
            edges.append(
                A2AEdge(
                    source=agent.code,
                    target=target,
                    description=f"{agent.code} → {target}",
                    performative=perf,
                    intent=intent,
                    payload_contract=contract,
                )
            )

    # Explicit auth edges (everyone calls ICP_ID) so the graph is reachable and realistic.
    # This models: "every call is authenticated/authorized via ICP_ID layer".
    auth_sources = ["VALET", "SHOPI", "FOLIO", "PAYME", "PROMO", "MARKT", "RIDIM", "PORTE", "DASHB", "DASHC", "PAYOUT", "LOYLT"]
    for src in auth_sources:
        if src != "ICP_ID":
            edges.append(
                A2AEdge(
                    source=src,
                    target="ICP_ID",
                    description=f"{src} → ICP_ID (auth/trace)",
                    performative="query",
                    intent="auth.verify_principal",
                    payload_contract="{principal, role, resource, action}",
                )
            )
    return edges


def get_agent(code: str) -> Optional[Agent]:
    for agent in ramm_agents():
        if agent.code == code:
            return agent
    return None

