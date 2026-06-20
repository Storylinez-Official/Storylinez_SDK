"""
Storylinez MCP server package.

Exposes a curated set of Storylinez SDK operations over the Model Context Protocol
so MCP-capable agents (Claude Desktop, Cursor, Codex, etc.) can drive a user's
Storylinez account using their configured API key/secret.

Launch with the `storylinez-mcp` console script (see setup.py), or:

    python -m storylinez.mcp

Credentials are read from the environment:
    STORYLINEZ_API_KEY, STORYLINEZ_API_SECRET, STORYLINEZ_ORG_ID (optional),
    STORYLINEZ_BASE_URL (optional, defaults to production).
"""

from .server import build_server, main

__all__ = ["build_server", "main"]
