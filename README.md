# AegisPath

**AI-powered security-tool factory**

AegisPath is a development harness that turns a language model into a disciplined accelerator for designing, implementing, testing, and documenting *authorized* red-team and offensive-security tooling.

The model proposes.  
The harness verifies, constrains, records, and releases.

## Core Principles

1. **Model is never the source of truth** — durable state lives in the repository, policies, and CI artifacts.
2. **Verification before acceptance** — every change must pass static, policy, and (where applicable) sandboxed behavioral checks.
3. **Secure development controls by default** — secrets scanning, capability declarations, dual-use notices, and mandatory review gates.
4. **Repeatable, auditable releases** — signed packages, SBOMs, full provenance, and clear authorized-use packaging.
5. **Ethical & legal boundary** — this system exists solely to support *authorized* security testing, research, and defensive improvement. Users are solely responsible for compliance with all applicable laws and organizational policies.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     AegisPath Orchestrator                  │
├──────────────┬──────────────┬──────────────┬────────────────┤
│  Context     │  Agents      │  Verification│  Release       │
│  Engine      │  (Design /   │  Suite       │  Pipeline      │
│  (repo +     │   Implement /│  (static +   │  (package +    │
│   policies + │   Verify)    │   policy +   │   sign +       │
│   history)   │              │   sandbox)   │   document)    │
└──────────────┴──────────────┴──────────────┴────────────────┘
```

## Project Layout

```
AegisPath/
├── docs/                  # Architecture, charter, threat model of the harness
├── src/aegispath/         # Core harness code
│   ├── core/              # Context, policy engine, orchestrator
│   ├── agents/            # Specialized agents
│   └── verification/      # Static, policy, and sandbox checks
├── templates/             # Design, threat-model, and coding-standard templates
├── tests/                 # Harness self-tests
├── examples/              # Non-operational examples & fixtures only
└── .github/workflows/     # CI gates
```

## Status

**v0.3 – Implement agent live**  
- Interactive Design + Implement wizards (questions → confirm → go back → add features)  
- Implement agent produces structured file packages; writes only after explicit confirmation  
- Shared session state, pluggable LLM backends, charter-enforcing prompts, prompt logging  
- CLI + browser GUI  
- Next: stronger verification, decision logging, GUI implement phase

## Quick Start

```bash
# Install
pip install -e ".[dev]"

# 1. Interactive design
aegispath design demo-recon
# (or one-shot)
aegispath design demo-recon --one-shot --save designs/demo-recon.md

# 2. Interactive implement (from an accepted design)
aegispath implement demo-recon --design designs/demo-recon.md
# Files written only after you confirm. Default output: ./generated/demo-recon/

# 3. Verify what was written
aegispath verify generated/demo-recon/

# Browser GUI
pip install -e ".[gui]"
aegispath gui
```

## License & Dual-Use Notice

See [LICENSE](LICENSE).  

**Important**: Any tools produced with AegisPath are intended *only* for authorized security testing, research, and defensive purposes. Unauthorized use against systems you do not own or have explicit permission to test is illegal and strictly prohibited.

## Contributing

See `docs/development-charter.md` for the rules that govern all work in this repository.
