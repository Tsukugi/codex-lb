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
