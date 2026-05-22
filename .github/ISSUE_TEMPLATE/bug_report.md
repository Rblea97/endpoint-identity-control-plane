---
name: Bug report
description: Report a reproducible problem using fake/sanitized data only.
title: "Bug: "
labels: ["bug"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for reporting a bug. Do not include secrets, tokens, real ticket contents, employer/customer data, personal data, or sensitive incident details.
  - type: textarea
    id: summary
    attributes:
      label: Summary
      description: What happened?
      placeholder: The API returned ... when I expected ...
    validations:
      required: true
  - type: textarea
    id: reproduce
    attributes:
      label: Steps to reproduce
      description: Use fake/sanitized sample data only.
      placeholder: |
        1. Start the API with ...
        2. Send this fake request ...
        3. Observe ...
    validations:
      required: true
  - type: textarea
    id: expected
    attributes:
      label: Expected behavior
    validations:
      required: true
  - type: textarea
    id: actual
    attributes:
      label: Actual behavior
    validations:
      required: true
  - type: textarea
    id: environment
    attributes:
      label: Environment
      description: Python version, OS, command used, and any relevant safe configuration values.
      placeholder: |
        Python:
        OS:
        Command:
        Safe config values:
  - type: checkboxes
    id: safety
    attributes:
      label: Safety check
      options:
        - label: I did not include secrets, tokens, private keys, real personal data, employer/customer data, or sensitive incident details.
          required: true
