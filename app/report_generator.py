"""
Generate shareable test reports in HTML and Markdown formats.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

from .business_logic import run_all_business_logic_tests
from .nanda_validator import validate_nanda_compliance
from .test_logic import run_all_tests
from .validate import run_all_checks


def generate_html_report(output_path: str = "test_report.html") -> str:
    """Generate a complete HTML test report."""

    # Run all tests
    logic_results = run_all_tests()
    business_results = run_all_business_logic_tests()
    validation_ok, validation_messages = run_all_checks()
    nanda_ok, nanda_messages = validate_nanda_compliance()

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RAMM Agent Test Report</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #1a1a1a;
            color: #e0e0e0;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
        }}
        .section {{
            background: #2a2a2a;
            padding: 25px;
            margin-bottom: 20px;
            border-radius: 8px;
            border: 1px solid #3a3a3a;
        }}
        .section h2 {{
            margin-top: 0;
            color: #667eea;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        .summary-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        .summary-card h3 {{
            margin: 0;
            font-size: 2em;
        }}
        .summary-card p {{
            margin: 5px 0 0 0;
            opacity: 0.9;
        }}
        .test-result {{
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            border-left: 4px solid;
        }}
        .test-result.pass {{
            background: #3a3a3a;
            border-color: #667eea;
            color: #ffffff;
        }}
        .test-result.partial {{
            background: #3a3a3a;
            border-color: #764ba2;
            color: #ffffff;
        }}
        .test-result.fail {{
            background: #3a3a3a;
            border-color: #e74c3c;
            color: #ffffff;
        }}
        .test-result h3 {{
            margin: 0 0 10px 0;
            font-size: 1.2em;
            color: #ffffff;
        }}
        .test-result .score {{
            font-weight: bold;
            margin: 5px 0;
            color: #ffffff;
        }}
        .test-result .checks {{
            margin-top: 10px;
            font-size: 0.9em;
        }}
        .check-item {{
            margin: 3px 0;
        }}
        .check-item.pass::before {{
            content: "✓ ";
            color: #2ecc71;
            font-weight: bold;
        }}
        .check-item.fail::before {{
            content: "✗ ";
            color: #e74c3c;
            font-weight: bold;
        }}
        .check-item {{
            color: #ffffff;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background: #667eea;
            color: white;
        }}
        tr:hover {{
            background: #3a3a3a;
        }}
        td {{
            color: #e0e0e0;
        }}
        .timestamp {{
            color: #666;
            font-size: 0.9em;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 RAMM Agent Test Report</h1>
        <p>Comprehensive test results for RAMM agentic commerce system</p>
        <p class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
    </div>

    <div class="section">
        <h2>📊 Test Summary</h2>
        <div class="summary">
            <div class="summary-card">
                <h3>{len(logic_results)}</h3>
                <p>Logic Test Scenarios</p>
            </div>
            <div class="summary-card">
                <h3>{business_results['total']}</h3>
                <p>Business Logic Tests</p>
            </div>
            <div class="summary-card">
                <h3>{'✓' if validation_ok else '✗'}</h3>
                <p>Graph Validation</p>
            </div>
            <div class="summary-card">
                <h3>{'✓' if nanda_ok else '✗'}</h3>
                <p>NANDA Compliance</p>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>🧪 Logic Tests (Agent Behavior)</h2>
"""

    # Logic test results
    for name, (timeline, score) in logic_results.items():
        result_class = "pass" if score.result.value == "PASS" else ("partial" if score.result.value == "PARTIAL" else "fail")
        html += f"""
        <div class="test-result {result_class}">
            <h3>[{score.result.value}] {name}</h3>
            <div class="score">Score: {score.earned_points}/{score.total_points} ({score.percentage:.1f}%)</div>
            <div class="checks">
                {''.join(f'<div class="check-item {"pass" if "✓" in check else "fail"}">{check}</div>' for check in score.checks)}
            </div>
        </div>
"""

    html += """
    </div>

    <div class="section">
        <h2>💰 Business Logic Tests (Calculations)</h2>
        <table>
            <thead>
                <tr>
                    <th>Test Name</th>
                    <th>Description</th>
                    <th>Type</th>
                    <th>Result</th>
                </tr>
            </thead>
            <tbody>
"""

    for result in business_results["results"]:
        status = "✓ PASS" if result["passed"] else "✗ FAIL"
        status_class = "pass" if result["passed"] else "fail"
        html += f"""
                <tr>
                    <td><strong>{result['name']}</strong></td>
                    <td>{result['description']}</td>
                    <td>{result['test_type']}</td>
                    <td class="{status_class}">{status}</td>
                </tr>
"""

    html += """
            </tbody>
        </table>
    </div>

    <div class="section">
        <h2>✅ Graph Validation</h2>
        <div class="test-result {'pass' if validation_ok else 'fail'}">
            <h3>Graph Integrity Checks</h3>
            <div class="checks">
"""

    for msg in validation_messages:
        html += f'<div class="check-item pass">{msg}</div>'

    html += """
            </div>
        </div>
    </div>

    <div class="section">
        <h2>📋 NANDA Protocol Compliance</h2>
        <div class="test-result {'pass' if nanda_ok else 'fail'}">
            <h3>NANDA Protocol Validation</h3>
            <div class="checks">
"""

    if nanda_ok:
        html += '<div class="check-item pass">All A2A edges comply with NANDA protocol</div>'
    else:
        for msg in nanda_messages:
            html += f'<div class="check-item fail">{msg}</div>'

    html += """
            </div>
        </div>
    </div>

    <div class="section">
        <h2>📝 Notes</h2>
        <p>This report was generated automatically from the RAMM agent test suite.</p>
        <p>For more information, visit the project repository or run tests locally.</p>
    </div>

</body>
</html>
"""

    # Write to file
    output_file = Path(output_path)
    output_file.write_text(html, encoding="utf-8")
    return str(output_file.absolute())


def generate_markdown_report(output_path: str = "test_report.md") -> str:
    """Generate a Markdown test report."""

    # Run all tests
    logic_results = run_all_tests()
    business_results = run_all_business_logic_tests()
    validation_ok, validation_messages = run_all_checks()
    nanda_ok, nanda_messages = validate_nanda_compliance()

    md = f"""# RAMM Agent Test Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

## Test Summary

- **Logic Test Scenarios:** {len(logic_results)}
- **Business Logic Tests:** {business_results['total']}
- **Graph Validation:** {"✓ PASS" if validation_ok else "✗ FAIL"}

---

## Logic Tests (Agent Behavior)

"""

    for name, (timeline, score) in logic_results.items():
        status_icon = "✅" if score.result.value == "PASS" else ("⚠️" if score.result.value == "PARTIAL" else "❌")
        md += f"""
### {status_icon} {name}

**Score:** {score.earned_points}/{score.total_points} ({score.percentage:.1f}%)

**Checks:**
{chr(10).join(f"- {check}" for check in score.checks)}

"""

    md += """
---

## Business Logic Tests (Calculations)

| Test Name | Description | Type | Result |
|-----------|-------------|------|--------|
"""

    for result in business_results["results"]:
        status = "✅ PASS" if result["passed"] else "❌ FAIL"
        md += f"| {result['name']} | {result['description']} | {result['test_type']} | {status} |\n"

    md += f"""
---

## Graph Validation

{"✅ All checks passed" if validation_ok else "❌ Issues found"}

{chr(10).join(f"- {msg}" for msg in validation_messages)}

---

## NANDA Protocol Compliance

{"✅ All A2A edges comply with NANDA protocol" if nanda_ok else "❌ NANDA compliance issues found"}

{chr(10).join(f"- {msg}" for msg in nanda_messages) if not nanda_ok else ""}

---

## Notes

This report was generated automatically from the RAMM agent test suite.
"""

    # Write to file
    output_file = Path(output_path)
    output_file.write_text(md, encoding="utf-8")
    return str(output_file.absolute())


if __name__ == "__main__":
    print("Generating test reports...")
    html_path = generate_html_report()
    md_path = generate_markdown_report()
    print(f"✓ HTML report: {html_path}")
    print(f"✓ Markdown report: {md_path}")
