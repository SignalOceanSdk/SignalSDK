"""Entry point: python -m tests.mcp_integration [options]

Usage:
    python -m tests.mcp_integration                  # run all cases
    python -m tests.mcp_integration --case port_expenses_compare
    python -m tests.mcp_integration --improve        # suggest fixes for failures
    python -m tests.mcp_integration --verbose        # show each tool call as it happens
    python -m tests.mcp_integration --list           # list available test case IDs

Requires:
    ANTHROPIC_API_KEY in environment
    SIGNAL_OCEAN_API_KEY read from .mcp.json (same key Claude Desktop uses)
"""
import argparse
import asyncio
import os
import sys

from .cases import CASES
from .improver import suggest_improvements
from .runner import run_cases


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Signal Ocean MCP integration test runner"
    )
    parser.add_argument("--case", metavar="ID", help="Run a single test case by ID")
    parser.add_argument("--improve", action="store_true",
                        help="Generate improvement suggestions for failed tests")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Print each tool call as it happens")
    parser.add_argument("--list", action="store_true",
                        help="List available test case IDs and exit")
    args = parser.parse_args()

    if args.list:
        for case in CASES:
            print(f"  {case.id:<30} {case.description}")
        return

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY is not set.", file=sys.stderr)
        sys.exit(1)

    if args.case:
        cases = [c for c in CASES if c.id == args.case]
        if not cases:
            print(f"ERROR: no test case with id '{args.case}'", file=sys.stderr)
            print("Available:", ", ".join(c.id for c in CASES))
            sys.exit(1)
    else:
        cases = CASES

    results = asyncio.run(run_cases(cases, verbose=args.verbose))

    passed = sum(1 for r in results if r.passed)
    total = len(results)
    print(f"\n{'═' * 60}")
    print(f"Results: {passed}/{total} passed")

    failures = [r for r in results if not r.passed]
    if failures and args.improve:
        print(f"\n{'═' * 60}")
        print("Improvement suggestions:")
        print(suggest_improvements(failures))

    sys.exit(0 if not failures else 1)


if __name__ == "__main__":
    main()
