## Implementation

- [x] Add a client-history projection for automatic bridge switching.
- [x] Retire unavailable durable owners without the reset-horizon gate.
- [x] Clear old affinity, exclude the failed owner, and rebind within the request.
- [x] Settle the captured old circuit and quarantine without clearing newer evidence.
- [x] Add route regression coverage and update retirement coverage.
- [x] Reconcile main specs and context with the approved behavior.

## Validation

- [x] Run focused regression tests, lint, types, and strict OpenSpec validation.
- [x] Finish the full HTTP bridge suite and record verification evidence.
