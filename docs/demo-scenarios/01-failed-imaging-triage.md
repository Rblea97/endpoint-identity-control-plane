# Scenario 01: Failed Imaging / Endpoint Provisioning Triage

## Fake ticket

> User reports a newly imaged laptop is not ready for use.

## Demo command

```bash
endpoint-identity-demo --scenario failed-imaging
```

## What the demo checks

The CLI loads the synthetic inventory and flags `DEMO-WIN10-003` because it has multiple endpoint lifecycle problems:

- failed imaging state;
- stale device check-in;
- unsupported Windows 10 baseline for the demo timeline;
- encryption disabled;
- excessive local administrator exposure;
- missing patch status.

## Technician workflow

1. Confirm the device exists in endpoint inventory or SCCM/MECM.
2. Review deployment or task-sequence logs for the failed imaging state.
3. Confirm whether the endpoint checks in after remediation.
4. Validate encryption, compliance, and patch visibility before handoff.
5. Update the ticket with evidence and next action.

## Verification

- Imaging is complete or a reimage path is documented.
- Device check-in is current.
- Encryption and patch status are acceptable for handoff.
- Ticket notes explain what was checked and what changed.

## Interview talking point

“I built a synthetic endpoint operations demo that walks through how I would triage a failed imaging or provisioning issue: inventory presence, deployment state, check-in freshness, patch status, encryption, and ticket documentation.”
