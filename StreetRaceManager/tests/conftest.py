"""Pytest configuration to ensure project imports work from any invocation path."""

import sys
from pathlib import Path

# Add project root (StreetRaceManager/) to sys.path so `import code.*` works
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if PROJECT_ROOT.as_posix() not in sys.path:
    sys.path.insert(0, PROJECT_ROOT.as_posix())

