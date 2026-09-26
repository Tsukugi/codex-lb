# Goal

Allow a continuation to move to another account when its current account reports
confirmed usage exhaustion and the proxy already holds a verified, complete,
account-neutral resend body.

# Scope

- Cover direct WebSocket and HTTP bridge continuation replay.
- Cover pre-acceptance and accepted-but-output-free quota terminals.
- Permit one replacement-account dispatch.
- Keep files, turn-state owners, unsettled tools, incomplete history, visible
  output, and sequenced WebSocket lifecycles fail-closed.
- Do not add a compatibility mode, fallback projection, or setting.

# /grill me

The plan was challenged against the current ownership and replay contracts.

- A raw `previous_response_id` cannot move between accounts. The replay must
  remove it and use a verified complete body.
- `response.created` does not prove model output. Replay is allowed only when
  the terminal reports no output, output tokens, or reasoning tokens.
- A client-supplied anchor is not enough proof. The retained body must pass the
  existing strict account-neutral fresh-replay predicate.
- Delta-only continuations have incomplete history on direct WebSocket. They
  remain fail-closed.
- File pins and turn-state ownership remain hard account boundaries.
- `replay_count` limits the replacement dispatch to one.

The user approved these constraints on 2026-09-26.

# Progress

| Phase | Status | Notes |
| --- | --- | --- |
| 1. Investigate | done | Confirmed the accepted quota refusal and retained verified resend body. |
| 2. Update OpenSpec | done | Added accepted output-free quota relocation and WebSocket verified-resend coverage. |
| 3. Implement | done | Added strict usage classification, anchor release, and sticky reallocation. |
| 4. Add regression coverage | done | Added direct WebSocket and HTTP bridge regression cases. |
| 5. Validate | pending | Validation commands require explicit user request. |
| 6. Finalize docs | done | Reconciled the targeted OpenSpec task and implementation state. |

# Phases

## Phase 1. Investigate

Trace continuation ownership, accepted replay classification, full-resend
verification, output detection, and replacement-account selection.

## Phase 2. Update OpenSpec

Record the approved behavior in the active change without weakening the strict
replay predicate or the ownership exclusions.

## Phase 3. Implement

Classify confirmed usage-limit and quota terminals as replayable only through
the existing output-free accepted lifecycle. Release a client-supplied anchor
only when the retained fresh body is verified and account-neutral.

## Phase 4. Add regression coverage

Cover successful one-shot account movement and refusal for output, incomplete
history, files, turn-state ownership, and a consumed replay budget.

## Phase 5. Validate

Do not automatically build or test. When explicitly requested, run focused
tests first, then OpenSpec validation and repository lint gates.

## Phase 6. Finalize docs

Update this plan, the OpenSpec task list, and the final implementation notes.

# Validation

Not run. Repository instructions prohibit automatic builds and tests.

# Final State

Implementation is complete but unvalidated. Tests, builds, lint, and OpenSpec
validation were not run because repository instructions require an explicit
user request.
