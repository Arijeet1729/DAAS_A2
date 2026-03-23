"""Pytest configuration to ensure project imports work from any invocation path."""

import sys
from pathlib import Path
from code import registration

# Add project root (StreetRaceManager/) to sys.path so `import code.*` works
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if PROJECT_ROOT.as_posix() not in sys.path:
    sys.path.insert(0, PROJECT_ROOT.as_posix())


import pytest


@pytest.fixture(autouse=True)
def reset_registration():
    registration.REGISTERED_NAMES.clear()
    yield
    registration.REGISTERED_NAMES.clear()
