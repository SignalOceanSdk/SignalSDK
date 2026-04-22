"""Entry point for running the MCP server via python -m signal_ocean_mcp."""

import warnings
warnings.filterwarnings("ignore")

from .server import main

main()
