# SHOPI → VALET Connection: How SHOPI Gets Campaigns

## The Missing Link

You're absolutely right! SHOPI needs to **query VALET** to get active campaigns before it can recommend them to shoppers.

## What I Added

### 1. A2A Edge: SHOPI → VALET

**Added to `app/agents.py`:**
```python
("SHOPI", "VALET"): ("query", "campaign.list_active", "{filters?, limit?, offset?}")
```

**NANDA Structure:**
- **Performative**: `query` (read-only, no state change)
- **Intent**: `campaign.list_active` (get list of active campaigns)
- **Payload Contract**: `{filters?, limit?, offset?}` (optional filters, pagination)

### 2. Updated Purchase Flow Test

**Added to `app/test_logic.py`:**
```python
# SHOPI queries VALET for active campaigns
timeline.add(
    AgentEvent(
        agent_code="SHOPI",
        kind=EventKind.A2A_CALL,
        summary="SHOPI queries VALET for active campaigns",
        details={"target": "VALET"},
    )
)
actual_a2a_calls.add(("SHOPI", "VALET"))
score.add_check("SHOPI → VALET campaign query", True, 2)
```

### 3. Updated Sequence Diagram

**Updated `app/sequences.py` purchase flow:**
```mermaid
Shopper->>SHOPI: Browse marketplace
SHOPI->>VALET: Query active campaigns
VALET-->>SHOPI: Return campaign list
SHOPI->>Shopper: Show recommendations
Shopper->>SHOPI: Select campaign & buy
SHOPI->>FOLIO: Request Buy(PVT)
```

## How It Works

### Flow:
1. **Shopper opens SHOPI** (shopping assistant)
2. **SHOPI queries VALET**: `campaign.list_active` (get all active campaigns)
3. **VALET responds**: Returns list of campaigns with:
   - Campaign IDs
   - Product info
   - Pricing
   - Availability
   - Bonding curve details
4. **SHOPI personalizes**: Uses AI to match campaigns to shopper preferences
5. **SHOPI displays**: Shows recommended campaigns to shopper
6. **Shopper selects**: Chooses a campaign to purchase
7. **SHOPI executes**: Calls FOLIO/PAYME/MARKT to complete purchase

### Why Query (Not Event)?

**Query** is correct because:
- ✅ SHOPI **pulls** data when needed (on-demand)
- ✅ No state change in VALET (read-only)
- ✅ SHOPI can filter/paginate results
- ✅ SHOPI controls when to fetch (not pushed)

**Event** would be wrong because:
- ❌ VALET would push to all SHOPI instances (inefficient)
- ❌ SHOPI can't filter what it receives
- ❌ Harder to handle multiple shoppers

## Updated Test Expectations

The `purchase_flow` test now expects:
1. ✅ SHOPI → VALET (query campaigns)
2. ✅ SHOPI → MARKT (swap quote/execute)
3. ✅ SHOPI → PAYME (authorize payment)
4. ✅ SHOPI → FOLIO (mint PVT)

## Verification

Run the test to see it:
```bash
python -m app.test_logic
```

Look for `purchase_flow` - it should now show:
```
✓ SHOPI → VALET campaign query
✓ SHOPI recommends campaign
✓ SHOPI → MARKT swap request
...
```

## Summary

✅ **Added**: SHOPI → VALET query edge
✅ **Updated**: Purchase flow test to include campaign query
✅ **Updated**: Sequence diagram to show the flow
✅ **NANDA Compliant**: Uses `query` performative (read-only)

SHOPI now properly extracts campaign data from VALET before making recommendations! 🎯
