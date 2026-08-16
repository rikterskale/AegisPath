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

## Status

**v0.5 – Decisions, GUI implement, reference tool, CI gates**  
- Decision log (accept / reject / write / back) under `.aegispath/decisions/`  
- Streamlit GUI: Design + Implement + Decisions tabs  
- Reference tool: `examples/capability-reporter` (zero capability)  
- CI: pytest + charter + `aegispath verify` on the reference tool  
- Interactive Design + Implement; hardened verification  

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

# 4. Reference tool + decisions log
aegispath verify examples/capability-reporter
aegispath decisions

# Browser GUI
pip install -e ".[gui]"
aegispath gui
```

## License & Dual-Use Notice

See [LICENSE](LICENSE).  

**Important**: Any tools produced with AegisPath are intended *only* for authorized security testing, research, and defensive purposes. Unauthorized use against systems you do not own or have explicit permission to test is illegal and strictly prohibited.

## Contributing

See `docs/development-charter.md` for the rules that govern all work in this repository.
