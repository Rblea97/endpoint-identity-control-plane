# Scenario 02: Disabled User Still Assigned to a Device

## Fake ticket

> Offboarding review finds a disabled user still assigned to a laptop.

## Demo command

```bash
endpoint-identity-demo --scenario disabled-user-device-assignment
```

## What the demo checks

The CLI identifies `taylor.morgan@example.example` as a disabled synthetic user who is still assigned to `DEMO-WIN10-003`.

This simulates a common lifecycle hygiene question: when an account is disabled, should the endpoint still be assigned to that user, or should it be reclaimed, reassigned, retired, or reviewed?

## Technician workflow

1. Confirm the account is disabled.
2. Confirm the assigned endpoint and asset owner.
3. Check whether the laptop should be reclaimed, reassigned, or retired.
4. Update asset ownership notes after approval.
5. Document the offboarding cleanup in the ticket.

## Verification

- Disabled user no longer has unexplained active endpoint ownership.
- Device ownership is documented.
- Reclaim, reassign, or retirement path is clear.

## Interview talking point

“This scenario shows how endpoint support and identity lifecycle work overlap: account status, device ownership, offboarding evidence, and clean ticket documentation.”
