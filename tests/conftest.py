"""Shared pytest configuration for SURgul tests."""

from __future__ import annotations

import sys
import shutil
import uuid
from pathlib import Path

import pytest


SRC_PATH = Path(__file__).resolve().parents[1] / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


@pytest.fixture
def tmp_path() -> Path:
    """Provide a Windows-friendly temporary directory for file export tests."""
    repo_tmp = Path(__file__).resolve().parents[1] / ".test-tmp"
    temp_root = repo_tmp / f"surgul-test-{uuid.uuid4().hex}"
    temp_root.mkdir(parents=True, exist_ok=False)
    try:
        yield temp_root
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)
