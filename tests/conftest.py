"""Pytest configuration for the Storylinez SDK test suite.

Pure unit tests against src/storylinez — no network, no API keys needed.
Ad-hoc junk (notebooks, dumps) goes in tests/_scratch/ (gitignored).
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC))

collect_ignore_glob = ["_scratch/*"]
