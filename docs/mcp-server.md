# MCP Server

The Signal Ocean MCP Server lets you query Signal Ocean APIs using natural language from any AI assistant that supports the [Model Context Protocol](https://modelcontextprotocol.io/) (MCP), including Claude, Cursor, Windsurf, Cline, and others.

## Installation

```bash
pip install signal-ocean[mcp]
```

## Configuration

Add the server to your AI client's MCP configuration with your Signal Ocean API key:

### Claude Code

**Global configuration (recommended)** — makes the MCP server available in all Claude Code sessions.

Edit the Claude Code global config file and add the server under the `mcpServers` key:

- **Linux / macOS:** `~/.claude.json` (e.g. `/home/<username>/.claude.json`)
- **Windows:** `%USERPROFILE%\.claude.json` (e.g. `C:\Users\<username>\.claude.json`)

```json
{
  "mcpServers": {
    "signal-ocean": {
      "type": "stdio",
      "command": "python3",
      "args": ["-m", "signal_ocean_mcp"],
      "env": {
        "SIGNAL_OCEAN_API_KEY": "<your-api-key>"
      }
    }
  }
}
```

> **Note:** Use the Python executable that has `signal-ocean` installed. If `python3` is not found, use the full path (e.g. `python3.11` on Linux or `py` on Windows). Run `which python3` (Linux/macOS) or `where python` (Windows) to confirm.

Restart Claude Code after editing the file. The Signal Ocean tools will appear as `mcp__signal-ocean__*` in your session.

**Per-project configuration** — create a `.mcp.json` file in your project root to limit the server to a specific project:

```json
{
  "mcpServers": {
    "signal-ocean": {
      "type": "stdio",
      "command": "python3",
      "args": ["-m", "signal_ocean_mcp"],
      "env": {
        "SIGNAL_OCEAN_API_KEY": "<your-api-key>"
      }
    }
  }
}
```

### Claude Desktop

Add to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "signal-ocean": {
      "command": "python",
      "args": ["-m", "signal_ocean_mcp"],
      "env": {
        "SIGNAL_OCEAN_API_KEY": "<your-api-key>"
      }
    }
  }
}
```

### Cursor / VS Code

Add to your `.cursor/mcp.json` or VS Code MCP settings:

```json
{
  "mcpServers": {
    "signal-ocean": {
      "command": "python",
      "args": ["-m", "signal_ocean_mcp"],
      "env": {
        "SIGNAL_OCEAN_API_KEY": "<your-api-key>"
      }
    }
  }
}
```

## Examples

Once configured, you can ask your AI assistant questions in natural language. The assistant will automatically call the appropriate Signal Ocean APIs.

### Voyages

> "What are the voyages for vessel Nasledie?"

The assistant will look up the vessel's IMO number and fetch all its voyages.

> "Show me recent VLCC voyages from the last 30 days"

### Market Rates

> "What routes are available for VLCC tankers?"

> "What were the VLCC dirty cargo market rates on January 2nd, 2020?"

> "How did MR2 clean cargo market rates evolve from October through December 2020?"

### Distances

> "What is the sailing distance from Fujairah to Singapore for a VLCC in ballast?"

The assistant will resolve port names to IDs and calculate the distance.

### Vessel Emissions

> "What are the emission metrics for vessel IMO 9412036?"

> "What's the CII rating for IMO 9412036 in 2022?"

### Vessel Valuations

> "What's the latest valuation for vessel IMO 9453315?"

> "Show me the historical valuations for IMO 9318084"

### Port Expenses

> "What are the port expenses for vessel IMO 9867621 at Ningbo?"

### Companies

> "Tell me about company Signal Maritime"

> "Search for companies with 'maritime' in their name"

### Combined Queries

The assistant can chain multiple API calls together to answer complex questions:

> "Find the vessel Nasledie, get its emissions data, and tell me its CII rating trend"

> "What are the available Aframax routes and their current market rates?"
