# Tool Design Template

**Tool family / name**:  
**Author / date**:  
**Status**: Draft | Review | Accepted

## 1. Purpose

One-paragraph description of what the tool does and why it is needed for authorized testing.

## 2. Authorized-Use Statement

This tool is intended **only** for use against systems for which the operator has explicit authorization. Unauthorized use is prohibited.

## 3. Capability Declaration

```yaml
network: none | limited | unrestricted
filesystem: none | limited | unrestricted
process: none | limited | unrestricted
credentials: none | limited | unrestricted
persistence: none | limited | unrestricted
required_privileges: []
notes: ""
```

## 4. High-Level Design

- Architecture overview
- Key components
- Data flow
- Trust boundaries

## 5. Threat Model (Tool Itself)

- What could go wrong if the tool is misconfigured or abused?
- How does the design mitigate those risks?
- Residual risks that operators must accept

## 6. Acceptance Criteria

- Functional requirements
- Non-functional (performance, safety, auditability)
- Verification requirements (tests that must pass)

## 7. Out of Scope

Explicit list of things this tool will **not** do.

## 8. References

Links to related designs, prior art, or standards.
