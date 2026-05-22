# Scenario 03: Privileged Identity Missing MFA

## Fake ticket

> Identity review flags a privileged account without MFA enabled.

## Demo command

```bash
endpoint-identity-demo --scenario privileged-user-missing-mfa
```

## What the demo checks

The CLI flags `jamie.chen@example.example` because the synthetic account belongs to a privileged endpoint administrator group but does not have MFA enabled.

This simulates a junior identity or endpoint administration escalation: the technician may not own policy design, but they should recognize why privileged access without MFA is risky and know how to escalate or remediate through the correct process.

## Technician workflow

1. Confirm privileged group membership.
2. Confirm whether MFA is required by policy.
3. Escalate to identity administration or enable MFA if authorized.
4. Review whether the privileged access is still needed.
5. Document the remediation or approved exception.

## Verification

- MFA is enabled or an approved exception exists.
- Privileged group membership has a documented owner and purpose.
- Ticket notes include who approved or completed the change.

## Interview talking point

“This scenario lets me discuss identity hygiene in a practical way: group membership, MFA enforcement, least privilege, escalation boundaries, and documentation.”
