import json
from pathlib import Path

import pytest


@pytest.fixture
def testdata_dir():
    """Return the testdata directory."""
    return Path(__file__).parent.parent / "testdata"


@pytest.fixture
def testdata_golden_dir(testdata_dir):
    """Return the testdata golden directory."""
    return testdata_dir / "golden"
