from __future__ import annotations

import io

import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image

from .agents import Agent, ramm_agents
from .business_logic import get_business_logic_tests, run_all_business_logic_tests, run_business_logic_test
from .graph import build_agent_graph, draw_agent_graph
from .sequences import sequence_catalog
from .state import simulate_sample_campaign_timeline
from .test_logic import get_test_scenarios, run_all_tests, simulate_scenario, TestResult
from .validate import run_all_checks
from .viz_mermaid import mermaid_agent_flow


def render_agent_sidebar(agents: list[Agent]) -> Agent:
    st.sidebar.title("RAMM Agents")
    codes = [a.code for a in agents]
    selected_code = st.sidebar.selectbox("Select agent", codes, index=0)
    return next(a for a in agents if a.code == selected_code)


def render_agent_details(agent: Agent) -> None:
    st.subheader(f"{agent.code} – {agent.name}")
    st.markdown(f"**Role**: `{agent.role.value}`  |  **Kind**: `{agent.kind.value}`")
    st.write(agent.description)

    if agent.interacts_with:
        st.markdown("**Interacts with (humans):** " + ", ".join(agent.interacts_with))
    if agent.tools:
        st.markdown("**Tools / Capabilities:**")
        for t in agent.tools:
            st.markdown(f"- {t}")

    if agent.a2a_outbound:
        st.markdown("**Outbound A2A calls:** " + ", ".join(agent.a2a_outbound))


def render_graph_section() -> None:
    st.subheader("Agent A2A Network (Python view of ICP canisters)")
    graph = build_agent_graph()
    fig, _ = draw_agent_graph(graph)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=140, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    st.image(Image.open(buf), caption="RAMM Agent Network", use_column_width=True)


def render_timeline_section() -> None:
    st.subheader("Sample Campaign Timeline")
    # Simple "live" rerun hook to simulate test-time refresh
    if st.button("Replay sample scenario"):
        st.toast("Scenario replayed")
    tl = simulate_sample_campaign_timeline()

    st.markdown(
        "This deterministic run shows how agents move through **state transitions** "
        "and **A2A calls** during a single SMART CAMPAIGN."
    )

    records = [
        {
            "time": e.ts.isoformat(timespec="seconds"),
            "agent": e.agent_code,
            "kind": e.kind.value,
            "summary": e.summary,
        }
        for e in tl.events
    ]
    st.dataframe(records, hide_index=True, use_container_width=True)


def render_mermaid_section() -> None:
    st.subheader("Mermaid Definition (for docs / design)")
    md = mermaid_agent_flow()
    st.code(md, language="mermaid")


def render_sequence_section() -> None:
    st.subheader("Sequence Diagrams (Mermaid)")
    catalog = sequence_catalog()
    labels = list(catalog.keys())
    choice = st.selectbox("Choose flow", labels, index=0)
    st.code(catalog[choice], language="mermaid")


def render_validation_section() -> None:
    st.subheader("Agent Graph Validation")
    st.markdown(
        "**Current Pass Criteria:**\n"
        "- ✅ No missing nodes (all edges reference existing agents)\n"
        "- ✅ No isolated agents (all agents have at least one A2A edge)\n"
        "- ✅ All agents reachable from VALET/SHOPI entry points\n"
        "\n"
        "Quick integrity checks to spot missing/isolated agents or bad edges "
        "before wiring ICP canisters."
    )
    if st.button("Run validation checks"):
        ok, messages = run_all_checks()
        status = "✅ All checks passed" if ok else "⚠️ Issues found"
        st.write(status)
        st.write("\n".join(f"- {m}" for m in messages))
    else:
        st.info("Press 'Run validation checks' to test the current graph.")


def render_logic_testing_section() -> None:
    st.subheader("Logic Testing with Mock Data & Scoring")
    st.markdown(
        "Test agent behavior with mock campaigns, wallets, and PVTs. "
        "Each scenario validates:\n"
        "- ✅ Expected A2A calls occur\n"
        "- ✅ Expected state transitions happen\n"
        "- ✅ Event flow matches expectations\n"
        "- ✅ Security & attack vectors are handled\n"
        "- ✅ Boundary conditions are validated\n"
        "\n"
        "**Scoring:** Each check earns points. Scenarios pass if score ≥ threshold (typically 70-90%).\n"
        "\n"
        "**Test Categories:**\n"
        "- 🟢 **Happy Path** (3): Baseline functionality\n"
        "- 🔴 **Security** (10): Attack vectors & unauthorized access\n"
        "- 🟡 **Resilience** (3): Error handling & recovery"
    )

    scenarios = get_test_scenarios()
    scenario_names = [s.name for s in scenarios]

    if st.button("Run all logic tests"):
        results = run_all_tests()
        for name, (timeline, score) in results.items():
            with st.expander(f"[{score.result.value}] {name} - {score.percentage:.1f}% ({score.earned_points}/{score.total_points})", expanded=True):
                st.markdown(f"**Description:** {next(s.description for s in scenarios if s.name == name)}")
                st.markdown(f"**Threshold:** {score.details.get('min_score_threshold', 70.0)}%")
                st.markdown("**Checks:**")
                for check in score.checks:
                    st.markdown(f"- {check}")
                st.markdown("**Details:**")
                st.json(score.details)

    st.markdown("---")
    st.subheader("Run Individual Scenario")
    selected_scenario_name = st.selectbox("Choose scenario", scenario_names, index=0)
    selected_scenario = next(s for s in scenarios if s.name == selected_scenario_name)

    st.markdown(f"**{selected_scenario.name}**")
    st.write(selected_scenario.description)
    st.markdown("**Mock Data:**")
    st.json(selected_scenario.mock_data)

    if st.button(f"Run {selected_scenario_name}"):
        timeline, score = simulate_scenario(selected_scenario)
        st.markdown(f"### Result: [{score.result.value}] {score.percentage:.1f}% ({score.earned_points}/{score.total_points} points)")
        st.markdown("**Checks:**")
        for check in score.checks:
            st.markdown(f"- {check}")
        st.markdown("**Timeline:**")
        records = [
            {
                "time": e.ts.isoformat(timespec="seconds"),
                "agent": e.agent_code,
                "kind": e.kind.value,
                "summary": e.summary,
            }
            for e in timeline.events
        ]
        st.dataframe(records, hide_index=True, use_container_width=True)


def render_business_logic_section() -> None:
    st.subheader("Business Logic Tests (Calculations)")
    st.markdown(
        "Test mathematical correctness of:\n"
        "- 💰 **Bonding Curve Pricing**: Linear, exponential, logarithmic curves\n"
        "- 🎁 **Reward Calculations**: Tier-based and attribution rewards\n"
        "- 📈 **Yield Calculations**: Simple and compound interest\n"
        "- 📊 **ROI Metrics**: Campaign ROI and PVT velocity\n"
    )

    if st.button("Run all business logic tests", key="bl_all"):
        results = run_all_business_logic_tests()
        st.markdown(f"**Summary:** {results['passed']}/{results['total']} passed, {results['failed']} failed")

        for result in results["results"]:
            status = "✅" if result["passed"] else "❌"
            with st.expander(f"{status} {result['name']} - {result['test_type']}", expanded=not result["passed"]):
                st.markdown(f"**Description:** {result['description']}")
                if result["passed"]:
                    st.success("Test passed!")
                    st.json(result["actual"])
                else:
                    st.error("Test failed!")
                    st.markdown("**Expected:**")
                    st.json(result["expected"])
                    st.markdown("**Actual:**")
                    st.json(result["actual"])
                    if result["error"]:
                        st.error(f"Error: {result['error']}")

    st.markdown("---")
    st.subheader("Run Individual Business Logic Test")
    tests = get_business_logic_tests()
    test_names = [t.name for t in tests]
    selected_test_name = st.selectbox("Choose test", test_names, index=0, key="bl_test_select")
    selected_test = next(t for t in tests if t.name == selected_test_name)

    st.markdown(f"**{selected_test.name}**")
    st.write(selected_test.description)
    st.markdown("**Input Data:**")
    st.json(selected_test.input_data)
    st.markdown("**Expected Output:**")
    st.json(selected_test.expected_output)

    if st.button(f"Run {selected_test_name}", key="bl_test_run"):
        result = run_business_logic_test(selected_test)
        if result["passed"]:
            st.success("✅ Test passed!")
            st.json(result["actual"])
        else:
            st.error("❌ Test failed!")
            st.markdown("**Expected:**")
            st.json(result["expected"])
            st.markdown("**Actual:**")
            st.json(result["actual"])
            if result["error"]:
                st.error(f"Error: {result['error']}")


def main() -> None:
    st.set_page_config(page_title="RAMM Agent Dashboard", layout="wide")
    st.title("RAMM Agentic Commerce – Python/ICP Model")

    st.markdown(
        "This dashboard focuses on **agent behavior**, **state transitions**, and "
        "**decision flows**. Each Python agent maps conceptually onto an ICP canister, "
        "but we avoid protocol details here."
    )

    agents = ramm_agents()
    selected_agent = render_agent_sidebar(agents)

    tab_network, tab_sequences, tab_validation, tab_logic = st.tabs(
        ["Network & Agent", "Sequences", "Validation & Tests", "Logic Testing"]
    )

    with tab_network:
        col1, col2 = st.columns([2, 3])
        with col1:
            render_agent_details(selected_agent)
        with col2:
            render_graph_section()

        st.markdown("---")
        col3, col4 = st.columns(2)
        with col3:
            render_timeline_section()
        with col4:
            render_mermaid_section()

    with tab_sequences:
        render_sequence_section()

    with tab_validation:
        render_validation_section()

    with tab_logic:
        render_logic_testing_section()
        st.markdown("---")
        render_business_logic_section()


if __name__ == "__main__":
    main()

