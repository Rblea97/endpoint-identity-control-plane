# Branch Protection Guide

Use this as the baseline when a repository becomes public-facing or portfolio-grade.

## Recommended GitHub settings for `main`

Enable:

- Require a pull request before merging.
- Require at least one approving review for public-facing or security-sensitive changes.
- Dismiss stale approvals when new commits are pushed.
- Require status checks to pass before merging.
- Require branches to be up to date before merging.
- Block force pushes.
- Block branch deletion.
- Restrict direct pushes to `main` where practical.

Recommended required checks:

- CI validation workflow
- lint
- format check
- typecheck
- tests
- security/dependency gate where configured as blocking

## Workflow and security file ownership

Add CODEOWNERS coverage for:

- `.github/workflows/`
- `.github/dependabot.yml`
- `.github/CODEOWNERS`
- `SECURITY.md`
- `docs/security-posture.md`
- `docs/threat-model.md`
- deployment, container, or IaC files when present

## Notes

For private learning sandboxes, these controls may be documented but not enforced until the repo is used for public portfolio evidence. Public repos should not rely only on local hooks; GitHub branch protection should enforce the merge policy remotely.
