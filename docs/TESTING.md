# RAMM Agent Testing & Validation

## Current Test Pass Criteria

### 1. Graph Integrity Validation (`app/validate.py`)

**Pass Criteria:** All checks must return zero errors.

- ✅ **No Missing Nodes**: All A2A edges reference agents that exist in the graph
- ✅ **No Isolated Agents**: Every agent has at least one incoming or outgoing A2A edge
- ✅ **Reachability**: All agents are reachable from entry points (VALET for brands, SHOPI for shoppers)

**Run:** `python -m app.validate` or use the "Validation & Tests" tab in the dashboard.

---

## 2. Logic Testing with Mock Data & Scoring (`app/test_logic.py`)

**Pass Criteria:** Each scenario must score ≥ its threshold (typically 70-85%).

### Scoring System

Each test scenario validates:
- **Expected A2A calls** occur (points per call)
- **Expected state transitions** happen (points per transition)
- **Event keywords** appear in timeline (points per keyword)
- **Agent behavior** matches expectations (points for correct actions)

**Scoring Breakdown:**
- Each check earns 1-3 points depending on importance
- **PASS**: Score ≥ threshold (typically 70-85%)
- **PARTIAL**: Score between 50-70%
- **FAIL**: Score < 50%

### Predefined Test Scenarios

#### 1. `campaign_creation`
- **Mock Data**: Campaign configuration
- **Validates**: VALET creates campaign → notifies PROMO/DASHB → transitions to ACTIVE
- **Threshold**: 80%
- **Key Checks**: VALET config, state transition, A2A calls to PROMO/DASHB

#### 2. `purchase_flow`
- **Mock Data**: Campaign + Shopper wallet
- **Validates**: SHOPI → MARKT swap → PAYME escrow → FOLIO PVT mint
- **Threshold**: 85%
- **Key Checks**: SHOPI recommendations, A2A calls to MARKT/PAYME/FOLIO, PVT minting, escrow settlement

#### 3. `redemption_flow`
- **Mock Data**: Campaign + Wallet + PVT
- **Validates**: FOLIO → RIDIM → VALET validation → PORTE DPP mint
- **Threshold**: 80%
- **Key Checks**: Redemption request chain, VALET validation, DPP NFT minting

### Running Tests

**CLI:**
```bash
python -m app.test_logic
```

**Dashboard:**
- Go to "Logic Testing" tab
- Click "Run all logic tests" for batch results
- Or select individual scenario and click "Run [scenario_name]"

### Adding New Test Scenarios

1. Create mock data (campaign, wallet, PVT) in `get_test_scenarios()`
2. Define `TestScenario` with:
   - `expected_a2a_calls`: List of (source, target) tuples
   - `expected_state_transitions`: Dict mapping agent_code → list of phases
   - `expected_events`: List of keywords to find in timeline
   - `min_score_threshold`: Minimum percentage to pass
3. Add simulation logic in `simulate_scenario()` for your scenario name
4. Add scoring checks using `score.add_check(name, passed, points, detail)`

---

## Example Output

```
[PASS] campaign_creation
Score: 14/14 (100.0%)
Threshold: 80.0%
  ✓ VALET receives campaign config
  ✓ VALET transitions to ACTIVE
  ✓ VALET → PROMO notification
  ✓ VALET → DASHB state update
  ✓ A2A call VALET → PROMO
  ✓ A2A call VALET → DASHB
  ✓ VALET → active
  ✓ Event keyword 'campaign' found
  ✓ Event keyword 'VALET' found
  ✓ Event keyword 'PROMO' found
```

---

## Integration with Dashboard

The dashboard (`app/dashboard.py`) provides:
- **Validation & Tests tab**: Run graph integrity checks
- **Logic Testing tab**: Run scenarios with mock data, view scores, inspect timelines

All tests can be run interactively without leaving the browser.
