"""Entry point for running the MCP server via python -m signal_ocean_mcp."""

import warnings
warnings.filterwarnings("ignore")

# Patch MCP stdio transport to filter blank lines sent by Claude Desktop on Windows
import sys
import anyio
from io import TextIOWrapper
from contextlib import asynccontextmanager
import mcp.server.stdio as _mcp_stdio

_orig_stdio_server = _mcp_stdio.stdio_server


@asynccontextmanager
async def _filtered_stdio_server(stdin=None, stdout=None):
    if stdin is None:
        _raw = anyio.wrap_file(
            TextIOWrapper(sys.stdin.buffer, encoding="utf-8", errors="replace")
        )

        class _FilteredStdin:
            def __aiter__(self):
                return self

            async def __anext__(self):
                while True:
                    line = await _raw.readline()
                    if line == "":
                        raise StopAsyncIteration
                    if line.strip():
                        return line

        stdin = _FilteredStdin()

    async with _orig_stdio_server(stdin=stdin, stdout=stdout) as streams:
        yield streams


_mcp_stdio.stdio_server = _filtered_stdio_server

# FastMCP imports stdio_server by name, so patch that namespace too
import mcp.server.fastmcp.server as _fastmcp_server
_fastmcp_server.stdio_server = _filtered_stdio_server

from .server import main

main()
