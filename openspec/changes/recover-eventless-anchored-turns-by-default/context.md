## Purpose

Avoid surfacing a client disconnect for a transient eventless upstream
`response.create` on an anchored HTTP bridge continuation.

## Decision

Use the existing `server_anchored_replay_once` path as the default. It already
holds a durable operation fence, retries only before any response event or
visible output, preserves the required account and file pins, and consumes its
single replay budget before dispatch.

## Constraint

This is at-least-once delivery because upstream has no status or idempotency
endpoint. The retry is deliberately limited to one attempt. A second silent
send remains terminal instead of creating an unbounded loop.

## Example

The first upstream WebSocket accepts the frame but remains silent. The bridge
reconnects, sends the same fenced anchored request once, receives
`response.created`, and continues the existing downstream stream.

## Stale-anchor recovery

An upstream `previous_response_id` rejection is a different failure from an
eventless send. If the client request already carries a complete plaintext
history, the bridge verifies that history, removes response-owned identifiers,
and makes one fresh request after excluding the old owner. This is only valid
for account-neutral requests. Files, hosted tools, and other account-bound
state remain terminal because pretending they can transfer would lose work or
run it under the wrong account.

The Responses WebSocket may omit `error.param` for the exact message
`Invalid \`previous_response_id\`.`. Treat that exact shape as a stale anchor;
do not broaden classification to other invalid-request errors.
