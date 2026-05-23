# Demo Scenarios

These scenarios turn the project from a backend-only API into an actionable endpoint and identity operations lab. Each walkthrough uses committed synthetic data only and is designed to map to realistic early-career IT work: imaging, endpoint support, Active Directory-style lifecycle hygiene, identity escalation, and compliance triage.

Run the terminal demo:

```bash
endpoint-identity-demo --list
endpoint-identity-demo --scenario failed-imaging
endpoint-identity-demo --scenario disabled-user-device-assignment
endpoint-identity-demo --scenario privileged-user-missing-mfa
endpoint-identity-demo --scenario endpoint-compliance-queue
```

## Scenarios

1. [Failed imaging / endpoint provisioning triage](01-failed-imaging-triage.md)
2. [Disabled user still assigned to a device](02-disabled-user-device-assignment.md)
3. [Privileged identity missing MFA](03-privileged-user-missing-mfa.md)
4. [Endpoint compliance remediation queue](04-endpoint-compliance-queue.md)

## Public-safety boundary

The scenarios do not use employer data, real usernames, real hostnames, real Microsoft tenant data, exported SCCM/MECM inventory, Intune exports, Entra ID exports, screenshots, secrets, or connection strings. They are synthetic examples meant to demonstrate workflow thinking and technician-level triage discipline.
