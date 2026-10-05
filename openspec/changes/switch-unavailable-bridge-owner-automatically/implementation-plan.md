# Goal

Automatically switch a bridged continuation off an unavailable account using
the history the client supplies.

# Scope

HTTP session bridge pre-dispatch owner failures, durable retirement, replacement
selection, portability checks, route regression coverage, and OpenSpec updates.

# /grill me

The user chose option 2 on 2026-10-04 and clarified that switching must be
automatic. Missing earlier context is accepted. Account-owned files and stored
conversations still cannot move. A tool result without its call cannot move.
Clearing an anchor must not leave the request trapped by its missing prefix
metadata. A short reset horizon must not block an automatic switch. Replacement
must exclude the unavailable owner and persist the new thread owner. No
post-dispatch replay or additional settings are needed.

# Progress

| Phase | Status | Notes |
| --- | --- | --- |
| 1. Investigate | done | Traced the exact request, durable row, retry circuit, and reset gate. |
| 2. Implement | done | Supplied-history projection, immediate atomic retirement, canonical rebind, exclusion, and fenced circuit settlement. |
| 3. Regression coverage | done | Six route cases, portability unit cases, and near-reset retirement coverage pass. |
| 4. Validate | done with failures | 38 focused and 217 adjacent tests pass. Full bridge suite: 195 passed, 9 failed. Existing architecture size gate fails. |
| 5. Finalize docs | done | Main specs and delta specs are valid. Verification evidence recorded. Change remains active. |

# Phases

1. Trace the actual failure and challenge the behavior through /grill me.
2. Project client history, retire unavailable ownership, and retry on a replacement.
3. Cover the route and atomic retirement boundaries.
4. Run the requested regression tests and check types, lint, architecture, and specs.
5. Update main specs, context, tasks, and this plan.

# Validation

The user requested tests and replaced the earlier instruction prohibiting
automatic test execution. Synced the locked Python environment, then ran the
regressions against the main project. The first run found that a cached circuit
miss could hide a durable circuit at retirement. Owner switching now reads the
current generation directly before retirement. The test setup also now writes
circuits with their actual base version and verifies the writes took effect.

The 38 focused tests and 217 adjacent tests pass. Changed-file lint, format,
types, cancellation safety, timing seams, all 66 main specs, and strict change
validation pass. The full HTTP bridge suite finished with 195 passed and 9
failed. Six stale/denied-anchor failures reproduced under coverage without
entering the retirement body, fresh replay switch, or new settlement block.
Two reader-recovery failures also reproduced separately. The architecture gate
fails because unchanged `load_balancer.py` has 3,071 lines against a 3,021-line
limit; the same file at HEAD has 3,071 lines. The running Docker image was not
rebuilt or replaced.

# Final State

Implementation and regression coverage are complete in the workspace.
Automatic switching uses portable client history even when prefix metadata is
missing or the old owner's reset is near. It removes old account affinity,
excludes the unavailable owner, retains the canonical thread, and supersedes
only the captured old circuit episode before dispatch. Account-owned input and
concurrent newer circuit evidence remain protected.

The change remains active because broader tests and the architecture gate are
not green. See [verification.md](verification.md). The running container still
uses its previous image. History absent from the client body is not recovered.
