# Recover one eventless anchored turn by default

## Why

The default HTTP bridge behavior exposes a terminal disconnect when upstream
does not acknowledge an anchored `response.create` before the client-safe
deadline. The durable operation ledger is already enabled by default and can
fence one retry, but the recovery mode that uses it is disabled by default.

## What Changes

- Make the existing `server_anchored_replay_once` mode the default.
- Keep recovery bounded to one eventless anchored retry.
- Preserve same-owner, file-ownership, durable-operation, and no-visible-output
  guards.

## Impact

Anchored HTTP Responses bridge turns recover from one transient silent upstream
attempt without disconnecting the client. A second ambiguous attempt remains a
typed terminal timeout.
