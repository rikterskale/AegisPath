# capability-reporter

**First reference tool family for AegisPath.**

## Purpose

Print the tool’s capability declaration and authorized-use notice.  
Used to exercise Design → Implement → Verify and as a zero-risk example.

## Authorized-Use Statement

This tool is intended **only** for authorized testing, training, and harness validation.  
It performs no network, filesystem, process, credential, or persistence actions.  
Unauthorized use against systems you do not own or lack permission to test is prohibited.

## Capabilities

| Family       | Level |
|--------------|-------|
| network      | none  |
| filesystem   | none  |
| process      | none  |
| credentials  | none  |
| persistence  | none  |

## Usage

```bash
python -m capability_reporter.cli --show-notice
python -m capability_reporter.cli --show-capabilities
python -m capability_reporter.cli
```

## Verification

```bash
aegispath verify examples/capability-reporter
```

## Design notes

Hand-authored reference package (not model-generated) so CI can always validate a known-good, zero-capability artifact.
