# Add client conversation handoff recovery

## Why

A Responses continuation can be pinned to an account that is temporarily
unavailable. Another account cannot use that account's `previous_response_id`.
The client needs a way to continue on an available account without asking the
proxy to retain every conversation transcript.

## What Changes

- Define a client-owned handoff document for a recoverable conversation.
- On the explicit owner-unavailable error, create a new conversation without
  `previous_response_id` and provide the handoff as its context.
- Keep the proxy fail-closed for account-owned continuation IDs.

## Impact

This design preserves portable, visible conversation context while making the
loss of account-scoped upstream state explicit. It does not add proxy-side
transcript storage or change normal continuation routing.
