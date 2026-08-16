# AegisPath Coding Standards (v0)

These standards apply to all code produced or accepted under AegisPath.

## Language & Style

- Prefer Python 3.11+ for new tools unless performance or deployment constraints require otherwise.
- Follow PEP 8; use `ruff` for formatting and linting.
- Type hints are required on public functions and methods.
- Docstrings (Google or NumPy style) on all public modules, classes, and functions.

## Security & Safety

- Never hard-code credentials, API keys, or long-lived secrets.
- All network, filesystem, and process interactions must be gated by configuration and capability declarations.
- Prefer explicit allow-lists over deny-lists.
- Fail closed: if authorization or configuration is missing, refuse to operate.
- Log security-relevant decisions (start of privileged action, authorization check result, etc.).

## Structure

- Every tool package must contain:
  - A clear `__main__` or CLI entry point
  - A `CAPABILITIES` (or equivalent) declaration that matches the PolicyEngine schema
  - An authorized-use notice in its README or primary documentation
- Tests must live next to or under a `tests/` directory and must be runnable offline where possible.

## Documentation

- Purpose statement
- Authorized-use / dual-use notice
- Capability summary
- Installation, configuration, and usage examples
- Known limitations and residual risks

## Review Expectations

Any increase in capability surface (new network behavior, credential handling, persistence, privilege requirements) requires human review before merge.
