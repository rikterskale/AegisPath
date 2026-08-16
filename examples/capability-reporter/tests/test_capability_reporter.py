"""Tests for the capability-reporter reference tool."""

from capability_reporter.cli import AUTHORIZED_USE, CAPABILITIES


def test_all_capabilities_none():
    for key in ("network", "filesystem", "process", "credentials", "persistence"):
        assert CAPABILITIES[key] == "none"


def test_authorized_use_notice():
    lower = AUTHORIZED_USE.lower()
    assert "authorized" in lower or "authorization" in lower
