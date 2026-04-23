"""MCP test runner: spins up the signal-ocean MCP server, feeds questions to
Claude via the Anthropic API, captures the tool call trail, and evaluates
results against the test case expectations."""
import asyncio
import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

import anthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from .cases import TestCase

MODEL = "claude-sonnet-4-6"
MAX_TURNS = 20
MCP_JSON = Path(__file__).parents[2] / ".mcp.json"


def _load_signal_ocean_env() -> dict[str, str]:
    """Read SIGNAL_OCEAN_API_KEY from .mcp.json so the runner uses the same
    key as Claude Desktop without requiring a separate env var."""
    try:
        config = json.loads(MCP_JSON.read_text())
        return config["mcpServers"]["signal-ocean"].get("env", {})
    except Exception:
        return {}


def _server_params() -> StdioServerParameters:
    env = {**os.environ, **_load_signal_ocean_env()}
    return StdioServerParameters(
        command=sys.executable,
        args=["-m", "signal_ocean_mcp"],
        env=env,
    )


@dataclass
class ToolCall:
    name: str
    inputs: dict
    result_preview: str  # first 300 chars
    errored: bool = False


@dataclass
class TestResult:
    case: TestCase
    passed: bool = False
    tool_calls: list[ToolCall] = field(default_factory=list)
    final_response: str = ""
    failures: list[str] = field(default_factory=list)

    @property
    def call_count(self) -> int:
        return len(self.tool_calls)

    @property
    def tool_names(self) -> list[str]:
        return [tc.name for tc in self.tool_calls]


def _convert_tool(mcp_tool) -> dict:
    return {
        "name": mcp_tool.name,
        "description": mcp_tool.description or "",
        "input_schema": mcp_tool.inputSchema,
    }


def _evaluate(case: TestCase, result: TestResult) -> list[str]:
    failures = []

    if result.call_count > case.max_calls:
        failures.append(
            f"call_count={result.call_count} exceeds max={case.max_calls} "
            f"(calls: {result.tool_names})"
        )

    for tool in case.required_tools:
        if tool not in result.tool_names:
            failures.append(
                f"required tool '{tool}' was never called "
                f"(calls: {result.tool_names})"
            )

    for tool in case.forbidden_tools:
        if tool in result.tool_names:
            failures.append(f"forbidden tool '{tool}' was called")

    errored = [tc.name for tc in result.tool_calls if tc.errored]
    if errored:
        failures.append(f"tool errors: {errored}")

    return failures


async def run_case(case: TestCase, verbose: bool = False) -> TestResult:
    result = TestResult(case=case)

    async with stdio_client(_server_params()) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools_resp = await session.list_tools()
            tools = [_convert_tool(t) for t in tools_resp.tools]

            client = anthropic.Anthropic()
            messages: list[dict] = [{"role": "user", "content": case.question}]

            for _turn in range(MAX_TURNS):
                response = client.messages.create(
                    model=MODEL,
                    max_tokens=4096,
                    tools=tools,
                    messages=messages,
                )
                messages.append({"role": "assistant", "content": response.content})

                if response.stop_reason == "end_turn":
                    for block in response.content:
                        if hasattr(block, "text"):
                            result.final_response = block.text
                    break

                if response.stop_reason != "tool_use":
                    break

                tool_results = []
                for block in response.content:
                    if block.type != "tool_use":
                        continue

                    if verbose:
                        print(f"  → {block.name}({json.dumps(block.input)[:120]})")

                    try:
                        mcp_result = await session.call_tool(block.name, block.input)
                        content = (
                            mcp_result.content[0].text
                            if mcp_result.content and hasattr(mcp_result.content[0], "text")
                            else str(mcp_result.content)
                        )
                    except Exception as exc:
                        content = json.dumps({"error": str(exc)})

                    # Heuristic: a result starting with {"error" is an error
                    errored = content.lstrip().startswith('{"error"')

                    result.tool_calls.append(ToolCall(
                        name=block.name,
                        inputs=block.input,
                        result_preview=content[:300],
                        errored=errored,
                    ))

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": content,
                    })

                messages.append({"role": "user", "content": tool_results})

    result.failures = _evaluate(case, result)
    result.passed = not result.failures
    return result


async def run_cases(
    cases: list[TestCase],
    verbose: bool = False,
) -> list[TestResult]:
    results = []
    for case in cases:
        print(f"\n{'─' * 60}")
        print(f"[{case.id}] {case.description}")
        print(f"Q: {case.question[:100]}")
        try:
            result = await run_case(case, verbose=verbose)
        except Exception as exc:
            result = TestResult(case=case, failures=[f"runner error: {exc}"])

        status = "✅ PASS" if result.passed else "❌ FAIL"
        print(f"{status}  {result.call_count} calls: {result.tool_names}")
        for f in result.failures:
            print(f"   ✗ {f}")

        results.append(result)
    return results
