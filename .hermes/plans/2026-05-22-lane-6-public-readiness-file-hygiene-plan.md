# Lane 6 Public Readiness and File Hygiene Plan

> **For Hermes:** Prepare the repo for a later human publication decision. Do not publish, deploy, push to a public remote, or change repo visibility in this lane.

**Goal:** Audit tracked files, tighten ignore coverage, render diagram assets, classify public-safety findings, and record evidence for a public-readiness decision.

**Architecture:** No application behavior changes. This lane is repository hygiene, documentation asset generation, and validation only.

**Tech Stack:** Git, Markdown docs, Mermaid CLI rendered assets, Python/FastAPI validation gates, Docker/CI lint checks where tools are available.

---

## Scope

### In scope

- Inventory tracked files.
- Scan suspicious filenames and sensitive terms.
- Tighten `.gitignore`/`.dockerignore` coverage for local/generated artifacts.
- Render Mermaid diagrams to SVG and PNG fallbacks.
- Embed rendered diagrams in architecture docs.
- Remove or classify template/private/noisy artifacts that should not be public.
- Run validation and record evidence.

### Out of scope

- Making the repository public.
- Publishing a package, container, release, or live demo.
- Changing application behavior.
- Adding auth, persistence, dashboard, or real Microsoft integrations.
- Claiming GitHub branch protection is enforced without checking the actual remote settings.

## Tasks

### Task 1: Inventory files

Run tracked-file and ignored-file inventory commands. Classify suspicious filenames and expected policy/test-language hits.

### Task 2: Tighten ignore coverage

Update ignore files for generated reports, scan output, caches, local databases, local env files, and temporary Hermes artifacts while preserving safe placeholder files.

### Task 3: Curate public docs artifacts

Review `.hermes` plans/checklists and docs for raw prompt/transcript/private-process leakage. Remove or rewrite artifacts that are template carryover rather than useful project evidence.

### Task 4: Render diagrams

Render every Mermaid source under `docs/diagrams/` to SVG and PNG. Verify outputs and link them from `docs/architecture.md`.

### Task 5: Validate and record

Run whitespace, link/asset, file-hygiene, local quality/security, workflow/container, and publication-gate checks where tools are available. Record all findings and classifications in a Lane 6 checklist.
