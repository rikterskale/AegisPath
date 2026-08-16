# Threat Model Template (for tools produced under AegisPath)

**Tool**:  
**Version**:  
**Date**:

## 1. Assets

What are we protecting? (authorization tokens, test data, operator credentials, target integrity, audit logs, etc.)

## 2. Actors

- Authorized operator
- Malicious operator (insider or compromised account)
- External attacker who obtains the tool binary/source
- Compromised dependency or build pipeline

## 3. Entry Points

- CLI / configuration files
- Network listeners (if any)
- Plugin or extension mechanisms
- Model-generated configuration

## 4. Trust Boundaries

List the boundaries and what crosses them.

## 5. Threats & Mitigations

| Threat | Impact | Mitigation | Residual Risk |
|--------|--------|------------|---------------|
| ...    | ...    | ...        | ...           |

## 6. Security Controls Required by AegisPath

- Capability declaration present and accurate
- Authorized-use notice present
- Secrets scanning clean
- Verification suite passed
- Human review completed for capability increases

## 7. Residual Risks Accepted by Operator

Explicit list.
