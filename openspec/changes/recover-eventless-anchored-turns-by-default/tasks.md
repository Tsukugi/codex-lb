## 1. Specification

- [x] 1.1 Define the single fenced recovery requirement and its bounded failure case.

## 2. Implementation

- [x] 2.1 Make one server-anchored replay the canonical recovery mode.

## 3. Verification

- [x] 3.1 Verify default activation, replay bounds, and the live silent-then-acknowledged path.
- [x] 3.2 Prove a stale anchor after the bounded retry is terminal through `/v1/responses`.
- [x] 3.3 Prove that a verified plaintext full resend recovers once on an alternate account while non-portable state stays terminal.
