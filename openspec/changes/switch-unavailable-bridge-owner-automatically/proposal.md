## Why

Request `ffd3ef70-8875-4649-af49-9ec65afb6982` returned 502 while other accounts
were active. Repeated eventless failures had cleared its replay metadata. The
owner was rate-limited, but its reset fell inside the request budget, so the
request-path retirement refused to release it. The user chose automatic
switching with the history the client sends, accepting missing earlier context.

## What Changes

- Switch a bridged continuation before dispatch when its durable owner is
  unavailable, regardless of the owner's reset horizon.
- Use the client's untrimmed body without `previous_response_id`. Project
  response-owned bookkeeping through the existing replay projection and check
  that the remaining body is portable. Do not require saved prefix metadata.
- Exclude the failed owner and clear old affinity and turn-state headers while
  rebinding the durable thread to the replacement account.
- Keep file pins, stored conversations, unresolved tools, policy conflicts,
  local capacity failures, and post-dispatch failures outside this path.

## Impact

Changes HTTP session bridge routing and its request-path retirement contract.
Adds no setting or schema. Automatic switching can lose context that the client
did not send. Direct WebSocket routing is outside this change.
