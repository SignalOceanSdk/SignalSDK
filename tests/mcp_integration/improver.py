"""Improvement agent: reads failed test results, extracts the relevant server.py
sections, and asks Claude to suggest targeted fixes (docstring improvements,
composite tools, or bug fixes). Does NOT auto-apply — prints diffs for review."""
import re
from pathlib import Path

import anthropic

from .runner import TestResult

SERVER_PY = Path(__file__).parents[2] / "signal_ocean_mcp" / "server.py"
MODEL = "claude-sonnet-4-6"


def _extract_tool_source(tool_name: str, source: str) -> str:
    """Extract the source of a single @mcp.tool() function by name."""
    pattern = rf"(@mcp\.tool\(\)\nasync def {re.escape(tool_name)}\b.*?)(?=\n@mcp\.tool\(\)|\ndef main\(\))"
    match = re.search(pattern, source, re.DOTALL)
    return match.group(1).strip() if match else f"# {tool_name} not found"


def _build_prompt(failures: list[TestResult], server_source: str) -> str:
    lines = [
        "You are a Signal Ocean MCP server maintainer. The test suite below "
        "has failed. For each failure, the relevant tool source is shown. "
        "Suggest the minimal targeted fix: a docstring improvement, a new "
        "composite tool, or a bug fix. Output only the changed/added code "
        "blocks with a one-sentence explanation for each.",
        "",
    ]

    for result in failures:
        lines.append(f"## Test: {result.case.id}")
        lines.append(f"Question: {result.case.question}")
        lines.append(f"Failures: {result.failures}")
        lines.append(f"Calls made: {result.tool_names}")
        lines.append(f"Required: {result.case.required_tools}")
        lines.append(f"Forbidden: {result.case.forbidden_tools}")
        lines.append("")

        # Include source of all tools involved
        involved = set(result.tool_names + result.case.required_tools + result.case.forbidden_tools)
        for tool in sorted(involved):
            src = _extract_tool_source(tool, server_source)
            lines.append(f"### {tool}")
            lines.append("```python")
            lines.append(src[:2000])  # cap to avoid huge prompts
            lines.append("```")
            lines.append("")

    return "\n".join(lines)


def suggest_improvements(failures: list[TestResult]) -> str:
    if not failures:
        return "All tests passed — no improvements needed."

    server_source = SERVER_PY.read_text()
    prompt = _build_prompt(failures, server_source)

    client = anthropic.Anthropic()
    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text
