# responses-api-compat Delta

## ADDED Requirements

### Requirement: Default bounded recovery for eventless anchored continuations

When an HTTP bridge continuation with a durable `previous_response_id` reaches
the client-safe acknowledgement deadline without a response event, the service
MUST reconnect to the same continuity owner and replay it once under the
durable operation fence. The retry MUST preserve file ownership and MUST NOT
run after any response lifecycle event or downstream-visible output. A second
eventless attempt MUST terminate without another replay.

#### Scenario: Transient silence does not disconnect the client

- **GIVEN** the first anchored upstream send is eventless
- **WHEN** the single fenced retry receives `response.created`
- **THEN** the original downstream stream continues without a terminal timeout

#### Scenario: Retry discovers a stale anchor

- **GIVEN** the bounded replay has already been sent for an anchored continuation
- **WHEN** the upstream rejects that retry because `previous_response_id` is no longer valid
- **THEN** the proxy returns HTTP 502 with `error.code = "bridge_previous_response_not_found"`
- **AND** sets `error.param = "previous_response_id"`
- **AND** explains that the proxy will not replay the turn again and that the client must start a new turn with the required conversation context
