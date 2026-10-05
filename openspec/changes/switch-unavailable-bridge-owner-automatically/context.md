# Purpose and decision

The user chose option 2 in the /grill me session on 2026-10-04: use whatever
history the client supplies and make switching automatic. Full historical
coverage is no longer a requirement for this pre-dispatch bridge recovery.

# Evidence

The reported request logged `anchor_metadata_missing`. Its durable row had
no latest response ID, item count, or fingerprint, but still retained the old
account and turn state. The retry circuit had abandoned the anchor after
repeated eventless failures. The owner reset was 39 seconds after the reported
failure, inside the two-hour request budget. Six accounts were marked active
when inspected. These facts explain why both existing recovery gates refused.

# Constraints and failure modes

Incomplete client history can lose earlier context. The existing projection
removes response-owned IDs and reasoning bookkeeping; the strict portability
validator still rejects files, stored conversations, and unresolved tools.
Only a confirmed pre-dispatch owner failure permits this path. No replay of an
already submitted operation is introduced. Atomic retirement protects a
concurrent account recovery or thread rebind.

# Example

A thread remains pinned to rate-limited account A after its anchor is cleared.
The client sends `input: "continue with the current task"`. The proxy retires
that thread's unavailable ownership, selects eligible account B, and submits
that exact supplied text without an anchor. B cannot see older context that
was not included. The durable thread is then owned by B.

# Validation

Added coverage at `/backend-api/codex/responses` for missing metadata, near
reset, client anchors, replacement exclusion, orphan tool output, no eligible
replacement, later turns using the replacement, and a concurrent circuit
update. Portability unit cases cover files, stored conversations, reasoning
projection, and tool pairs. The 38 focused regressions and 217 adjacent tests
pass. Changed-file lint, formatting, types, cancellation safety, timing seams,
all 66 main specs, and strict change validation pass. Tests exposed a cached
planning miss that hid the old durable circuit; retirement now reads its
current generation directly before capturing the fence.

The repository architecture gate fails on unchanged `load_balancer.py`:
3,071 lines against a 3,021-line limit. The full HTTP bridge suite finished
with 195 passed and 9 failed. Six stale/denied-anchor failures reproduced without
executing the new owner-switch path. Two reader-recovery failures reproduced
separately. The broader failures remain unresolved; see
[verification.md](verification.md). The running Docker image was not rebuilt
or replaced.
