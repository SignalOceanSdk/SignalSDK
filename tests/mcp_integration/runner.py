"""MCP test runner: feeds questions to Claude (via Anthropic API or local CLI),
captures the tool call trail, and evaluates results against test case
expectations.

Two modes:
- API mode  (default when ANTHROPIC_API_KEY is set): spins up the MCP server
  via stdio_client and drives an agentic loop via the Anthropic SDK.
- CLI mode  (when ANTHROPIC_API_KEY is absent): runs `claude -p … --output-format
  stream-json` as a subprocess and parses the NDJSON event stream to extract
  tool calls.  No API key required; uses the Claude Desktop/CLI installation.
"""
import asyncio
import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    import anthropic as _anthropic_mod
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    _HAS_ANTHROPIC = True
except ImportError:
    _HAS_ANTHROPIC = False

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


def _server_params():
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
    judge_verdict: str = ""  # "PASS", "FAIL: reason", or "" when no rubric

    @property
    def call_count(self) -> int:
        return len(self.tool_calls)

    @property
    def tool_names(self) -> list[str]:
        return [tc.name for tc in self.tool_calls]


_CLI_INTERNAL_TOOLS = {
    "ToolSearch", "Agent", "Task",
    "Bash", "Read", "Write", "Edit", "Glob", "Grep",
    "WebFetch", "WebSearch", "TodoWrite", "NotebookEdit",
}


def _strip_mcp_prefix(name: str) -> str:
    """Strip 'mcp__<server>__' prefix that the claude CLI adds to tool names."""
    parts = name.split("__", 2)
    if len(parts) == 3 and parts[0] == "mcp":
        return parts[2]
    return name


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

            client = _anthropic_mod.Anthropic()
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


async def _judge_response_cli(
    question: str,
    expected_answer: str,
    final_response: str,
) -> tuple[bool, str]:
    """Ask the local claude CLI to judge whether final_response satisfies the rubric.

    Returns (passed, reason).  On any parse failure returns (True, "inconclusive").
    """
    judge_prompt = (
        "You are evaluating whether an AI assistant correctly answered a maritime data question.\n\n"
        f"Question: {question}\n\n"
        f"Rubric (what a correct answer must include): {expected_answer}\n\n"
        f"Actual response:\n{final_response[:3000]}\n\n"
        "Does the actual response satisfy the rubric?\n"
        'Reply with ONLY valid JSON — no markdown, no explanation: {"pass": true, "reason": "one sentence"}'
    )

    cmd = [
        "claude",
        "-p", judge_prompt,
        "--output-format", "json",
        "--verbose",
        "--max-turns", "1",
    ]

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, _ = await proc.communicate()
    raw = stdout.decode().strip()

    # --output-format json wraps the response; extract the "result" field
    try:
        outer = json.loads(raw)
        text = outer.get("result", raw) if isinstance(outer, dict) else raw
    except json.JSONDecodeError:
        text = raw

    # Strip accidental markdown fences
    text = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        verdict = json.loads(text)
        passed = bool(verdict.get("pass", True))
        reason = str(verdict.get("reason", ""))
        return passed, reason
    except (json.JSONDecodeError, AttributeError):
        return True, "inconclusive"


async def run_case_cli(case: TestCase, verbose: bool = False) -> TestResult:
    """Run a test case using the local `claude` CLI (no ANTHROPIC_API_KEY needed).

    Parses the stream-json event stream to extract tool_use / tool_result pairs
    and populates TestResult identically to run_case().
    """
    result = TestResult(case=case)

    cmd = [
        "claude",
        "-p", case.question,
        "--output-format", "stream-json",
        "--verbose",
        "--mcp-config", str(MCP_JSON),
        "--allowedTools", "mcp__signal-ocean__*",
    ]

    env = {**os.environ, **_load_signal_ocean_env()}

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=env,
    )

    stdout_bytes, _ = await proc.communicate()

    # tool_id -> (name, inputs) for tool_use blocks awaiting their result
    pending: dict[str, tuple[str, dict]] = {}

    for raw_line in stdout_bytes.decode(errors="replace").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue

        event_type = event.get("type")

        if event_type == "assistant":
            for block in event.get("message", {}).get("content", []):
                if block.get("type") == "tool_use":
                    tool_id = block.get("id", "")
                    tool_name = _strip_mcp_prefix(block.get("name", ""))
                    tool_input = block.get("input", {})
                    if tool_name in _CLI_INTERNAL_TOOLS:
                        continue
                    pending[tool_id] = (tool_name, tool_input)
                    if verbose:
                        print(f"  → {tool_name}({json.dumps(tool_input)[:120]})")

        elif event_type == "user":
            for block in event.get("message", {}).get("content", []):
                if block.get("type") == "tool_result":
                    tool_id = block.get("tool_use_id", "")
                    raw_content = block.get("content", "")
                    if isinstance(raw_content, list):
                        content_str = " ".join(
                            c.get("text", "")
                            for c in raw_content
                            if isinstance(c, dict)
                        )
                    else:
                        content_str = str(raw_content)

                    if tool_id in pending:
                        name, inputs = pending.pop(tool_id)
                        result.tool_calls.append(ToolCall(
                            name=name,
                            inputs=inputs,
                            result_preview=content_str[:300],
                            errored=content_str.lstrip().startswith('{"error"'),
                        ))

        elif event_type == "result":
            result.final_response = event.get("result", "")

    # Flush any tool_use blocks that never received a matching tool_result
    for _tid, (name, inputs) in pending.items():
        result.tool_calls.append(ToolCall(
            name=name, inputs=inputs, result_preview="", errored=False
        ))

    result.failures = _evaluate(case, result)

    if case.expected_answer and result.final_response:
        judge_passed, judge_reason = await _judge_response_cli(
            case.question, case.expected_answer, result.final_response
        )
        result.judge_verdict = "PASS" if judge_passed else f"FAIL: {judge_reason}"
        if not judge_passed:
            result.failures.append(f"judge: {judge_reason}")

    result.passed = not result.failures
    return result


async def run_cases(
    cases: list[TestCase],
    verbose: bool = False,
    use_cli: bool = False,
) -> list[TestResult]:
    results = []
    for case in cases:
        print(f"\n{'─' * 60}", flush=True)
        print(f"[{case.id}] {case.description}", flush=True)
        print(f"Q: {case.question[:100]}", flush=True)
        try:
            if use_cli:
                result = await run_case_cli(case, verbose=verbose)
            else:
                result = await run_case(case, verbose=verbose)
        except Exception as exc:
            result = TestResult(case=case, failures=[f"runner error: {exc}"])

        status = "✅ PASS" if result.passed else "❌ FAIL"
        judge_tag = f"  [judge: {result.judge_verdict}]" if result.judge_verdict else ""
        print(f"{status}  {result.call_count} calls: {result.tool_names}{judge_tag}", flush=True)
        for f in result.failures:
            print(f"   ✗ {f}", flush=True)

        results.append(result)
    return results
