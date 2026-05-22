# ADR-0003: Use Deterministic Risk Rules for the MVP

## Status

Accepted

## Context

The project needs to turn endpoint and identity inventory into findings a reviewer can understand. Possible scoring approaches include deterministic rules, weighted scoring, ML models, LLM-generated analysis, or manual-only reports.

For a public portfolio MVP, the rule engine must be explainable, easy to test, and safe to document. The project should not overclaim advanced detection capability or imply that simplified demo logic replaces enterprise security tooling.

## Decision

Use deterministic Python rules for the MVP risk engine.

Each finding should include:

- stable finding ID;
- severity;
- category;
- title;
- asset type and asset ID;
- evidence;
- recommendation;
- control mapping.

The API risk report uses a deterministic `as_of` timestamp for stable docs and tests.

## Considered options

- Deterministic rules.
- Weighted risk scoring.
- ML model.
- LLM-generated risk summaries.
- Manual static report with no code-based rules.

## Rationale

Deterministic rules are the right fit for this stage because they are explainable and testable. A reviewer can inspect the synthetic data, see why a finding exists, and verify the expected output with tests.

Weighted scoring may be useful later, but it would require additional calibration and documentation. ML or LLM scoring would be less transparent and would distract from the endpoint/identity administration focus. A static report would be easier but would not demonstrate backend logic or testing discipline.

## Consequences

### Positive

- Clear link between inventory evidence and findings.
- Stable test expectations.
- Easier security and code review.
- Honest fit for endpoint hygiene checks such as stale devices, missing MFA, local admin exposure, compliance state, and imaging failures.

### Negative / tradeoffs

- Rules are simplified and do not represent full enterprise detection logic.
- Severity is project-defined, not a formal Microsoft, CVSS, or regulatory severity model.
- No probabilistic prioritization, historical trends, or threat-intelligence context.

## Revisit criteria

Revisit if the project adds larger datasets, trend analysis, import workflows, dashboard prioritization, or more advanced scoring. Any advanced scoring should preserve evidence, testability, and explainability.
