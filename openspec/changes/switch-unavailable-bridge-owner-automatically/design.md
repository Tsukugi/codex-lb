## Decision

Use the existing request-path retirement and replay switch machinery. Replace
the reset-horizon rule with an atomic persisted-status check. A small pure
helper projects supplied input and validates portability without requiring a
durable completeness proof. The accepted context-loss behavior is recorded in
[context.md](context.md) and the [/grill me session](implementation-plan.md).

## Flow

1. Bridge creation reports an unavailable required owner before dispatch.
2. Validate the untrimmed client body without its response anchor.
3. Capture the old circuit episode and quarantine fence.
4. Atomically retire the still-current unavailable durable owner.
5. Reuse the replay switch helper while retaining the canonical thread key.
   It removes old headers and affinity, excludes the failed account, resets
   anchor state, and forces local replacement creation.
6. Settle the captured circuit and quarantine after replacement ownership is
   claimed. Refuse dispatch if the circuit advanced concurrently.
7. Submit the supplied portable history on the replacement account. Later
   turns resolve the replacement through the canonical durable thread.

## Boundaries

Only one retirement is attempted per request. Existing account assignment,
model and security selection remain in force. Non-portable input and
post-dispatch outcomes do not enter this path. No new setting, migration,
transport mode, or alternate runtime is added.
