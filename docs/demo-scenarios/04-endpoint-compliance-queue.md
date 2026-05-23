# Scenario 04: Endpoint Compliance Remediation Queue

## Fake ticket

> Endpoint support queue needs a prioritized remediation plan.

## Demo command

```bash
endpoint-identity-demo --scenario endpoint-compliance-queue
```

## What the demo checks

The CLI summarizes synthetic endpoints by finding count and severity, then shows which devices should be investigated first. In the current fixture, `DEMO-WIN10-003` rises to the top because it combines imaging, patching, encryption, local admin, unsupported OS, and stale check-in issues.

## Technician workflow

1. Prioritize devices with the most findings and highest severity.
2. Start with compliance blockers such as encryption, patch visibility, and policy state.
3. Separate quick fixes from devices that need reimage, owner review, or escalation.
4. Record remediation evidence before closing tickets.
5. Re-run the report to confirm the queue changed after remediation.

## Verification

- Highest-risk devices have an owner and next action.
- Compliance-impacting findings are remediated or escalated.
- Tickets explain why each device was prioritized.

## Interview talking point

“This scenario shows that I can turn noisy endpoint data into an ordered support queue with evidence, severity, and practical remediation steps.”
