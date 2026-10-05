# Verification: switch-unavailable-bridge-owner-automatically

Verified on 2026-10-04 in the main project using its locked Python environment.

| Dimension | Result |
| --- | --- |
| Completeness | All implementation and validation tasks executed. |
| Correctness | All six automatic-switch route cases and portability/retirement unit cases pass. Broader suite has nine unresolved failures. |
| Coherence | Implementation follows the design. Main specs and delta specs pass strict validation. |

## Requirement evidence

- Supplied-history projection: `owner_switch.py` removes the response anchor,
  projects known response-owned bookkeeping, and runs the existing strict
  portability validator. Unit coverage includes tool pairs, reasoning, files,
  stored conversations, stored items, and unresolved tool output.
- Immediate retirement: the coordinator/repository no longer use a request
  reset deadline. The persisted unavailable-status lock and owner CAS remain.
  Unit coverage protects healthy and concurrently replaced owners.
- Route recovery: the six cases in
  `test_backend_responses_http_bridge_switches_unavailable_owner_automatically`
  prove missing metadata, near resets, paused ownership, client anchors,
  rejected orphan tools, and no replacement. Success cases assert old-owner
  exclusion, removed affinity headers, canonical durable rebind, and a later
  turn on the replacement.
- Circuit settlement: retirement reads the current durable generation directly,
  avoiding the planning cache's recent-miss window. The concurrent-circuit
  route case writes against the actual base version, checks that the newer
  count persisted, and proves a 503 without replacement dispatch.
- Policy, capacity, and post-dispatch boundaries continue through their existing
  typed error gates. Adjacent replay, continuity, and accepted-capacity cases pass.

## Passed checks

- Focused regression run: 38 passed.
- Adjacent replay/continuity run: 217 passed, 193 deselected.
- Changed-file Ruff lint, Ruff formatting, and ty type checks.
- Cancellation safety and proxy timing seams.
- All 66 main OpenSpec capabilities and strict change validation.
- Diff whitespace checks.

## Unresolved validation failures

Full `tests/integration/test_http_responses_bridge.py`: 195 passed, 9 failed.

1. `test_v1_responses_http_bridge_retries_unanchored_request_when_upstream_never_acknowledges_response_create`: 502 instead of 200.
2. `test_v1_responses_http_bridge_idle_recovery_hands_reader_to_replacement`: 502 instead of 200.
3. `test_retry_http_bridge_precreated_request_releases_pending_lock_before_reconnect`: reconnect event timed out.
4. `test_v1_responses_http_bridge_stale_anchor_after_bounded_retry_is_terminal`: ambiguous replay persistence error instead of the expected stale-anchor error.
5. `test_v1_responses_http_bridge_stops_reinjecting_an_anchor_upstream_denied`: 200 instead of 502.
6. `test_native_codex_http_bridge_denied_anchor_refusal_returns_502_before_commit`: expected refusal fence did not fire.
7. `test_native_codex_http_bridge_denied_anchor_refusal_emits_terminal_after_commit`: expected refusal fence did not fire.
8. `test_non_native_http_bridge_denied_anchor_refusal_still_returns_502_json`: expected refusal fence did not fire.
9. `test_forwarded_denied_anchor_refusal_marks_the_owner_error_as_a_local_refusal`: expected refusal fence did not fire.

Failures 1 and 2 reproduced in a separate test run. Failures 4 through 9
reproduced under coverage; none executed the retirement body, the fresh replay
switch helper, or the new owner-switch settlement block. This rules out those
new paths as their trigger, but does not establish a fully passing baseline.
Their causes remain outside this verification's conclusions.

The proxy architecture gate also fails on unchanged `load_balancer.py`:
3,071 lines against a 3,021-line limit. Its HEAD version has the same size.

## Final assessment

Automatic switching passes its focused regressions. Repository-wide bridge
verification is not green. Keep the change active and do not call it ready for
release or archive. The running Docker image has not been rebuilt or replaced.
