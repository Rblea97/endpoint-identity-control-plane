---
name: Feature request
description: Suggest a small, reviewable improvement.
title: "Feature: "
labels: ["enhancement"]
body:
  - type: markdown
    attributes:
      value: |
        Please keep requests scoped. This project is intentionally local/stateless and uses fake data only.
  - type: textarea
    id: problem
    attributes:
      label: Problem or opportunity
      description: What user, security, documentation, or developer-experience problem would this solve?
    validations:
      required: true
  - type: textarea
    id: proposal
    attributes:
      label: Proposed solution
      description: Describe the smallest useful version.
    validations:
      required: true
  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives considered
      description: What simpler or safer alternatives exist?
  - type: textarea
    id: security
    attributes:
      label: Security and data handling impact
      description: Does this affect validation, logging, dependencies, auth, persistence, CI, or public data exposure?
    validations:
      required: true
  - type: checkboxes
    id: fit
    attributes:
      label: Scope check
      options:
        - label: This request can be implemented as a narrow, reviewable lane.
          required: true
        - label: This request does not require real sensitive data in examples, tests, or logs.
          required: true
