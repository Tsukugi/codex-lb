## ADDED Requirements

### Requirement: Unavailable bridge owners switch automatically using client history

When HTTP bridge creation fails before dispatch with
`previous_response_owner_unavailable` and a durable lookup identifies the
unavailable owner, the service MUST attempt one automatic replacement using
the client's untrimmed body without `previous_response_id`. It MUST NOT require
stored prefix metadata or wait for the owner's reset horizon. It MUST project
response-owned bookkeeping with the existing account-neutral replay projection
and require the resulting body to pass the account-neutral request validator.
The client body MAY omit earlier conversation context. Retirement MUST check
the owner's persisted unavailable status atomically and compare the current
session owner before writing. A healthy or concurrently replaced owner MUST
remain unchanged.

#### Scenario: Cleared replay metadata and a near reset

- **GIVEN** a durable thread whose rate-limited owner resets within the request budget
- **AND** its saved response anchor and prefix metadata have been cleared
- **WHEN** the client sends portable history and bridge creation fails before dispatch
- **THEN** the request switches automatically to another eligible account
- **AND** the replacement receives the supplied history without the response anchor

#### Scenario: Client supplies an owner-bound response identifier

- **GIVEN** a durable unavailable owner and portable client input
- **WHEN** the client also supplies `previous_response_id`
- **THEN** automatic switching removes that identifier and sends the supplied input

### Requirement: Automatic bridge switching clears account ownership and is bounded

Automatic switching MUST exclude the unavailable owner from replacement
selection, clear old session affinity and turn-state headers, and rebind the
canonical durable thread to the replacement. It MUST settle only the retry
circuit episode and quarantine generation captured before retirement; newer
concurrent evidence MUST remain protected. It MUST attempt retirement at
most once per request. File-bound input, stored conversation references,
unresolved tool output, unsupported portable projections, policy conflicts,
local capacity errors, and failures after upstream dispatch MUST NOT authorize
this switch. When no replacement is eligible, the request MUST return the
ordinary selection failure without re-dispatching on the unavailable owner.

#### Scenario: Replacement serves later turns

- **WHEN** automatic switching completes on account B
- **THEN** the durable thread records account B as its owner
- **AND** the retired account A is excluded from the replacement attempt

#### Scenario: Old poisoned circuit belongs to the retired owner

- **GIVEN** an unavailable owner whose thread has a poisoned retry circuit and no saved anchor
- **WHEN** the thread rebinds to a replacement account
- **THEN** the captured old circuit is superseded before submitting the supplied history
- **AND** a newer circuit episode is not cleared by that settlement

#### Scenario: Account-owned input cannot move

- **WHEN** the request references an account-owned file or stored conversation, or has unresolved tool output
- **THEN** the service keeps the continuity failure and does not retire its owner

## MODIFIED Requirements

### Requirement: Hard continuity remains owner-bound and bounded

Requests that depend on `previous_response_id`, hard turn-state, nonblank `conversation`, account-scoped `input_file.file_id` pins, live or durable bridge ownership, replay/reattach state, or another required owner continuity source MUST NOT silently reroute to an account that cannot preserve continuity. Pre-dispatch HTTP bridge owner failures MAY instead follow the automatic client-history switch requirement below, which permits missing earlier context only after projecting and validating the supplied body. A resolved required owner MUST override bare process-session locality and MUST be selected without consulting or rewriting that soft mapping. A `previous_response_id` is a stored-object continuation reference and remains owner-bound even when the same request also carries a session header, `prompt_cache_key`, or another soft locality key. If independently resolved hard sources identify different accounts, if live durable referenced-file pins identify different accounts, or if a request has partial live durable file-pin coverage, the service MUST fail closed before upstream dispatch. A request for which no referenced file has a live durable pin MUST preserve opaque `file_id` compatibility and proceed without inventing ownership evidence. If the owner account/session is unavailable or saturated and neither verified replay nor automatic client-history switching applies, the service MUST fail closed with an explicit retryable continuity/local overload reason instead of flooding the owner queue indefinitely.

Every HTTP, compact, direct WebSocket, and HTTP-bridge transport MUST resolve explicit turn state against both live and durable bridge aliases. Live, durable, previous-response, file, and explicit turn-state evidence MUST be compared independently; source ordering MUST NOT choose the first match when distinct sessions or accounts resolve. A reused direct WebSocket MUST repeat nonblank `conversation` ownership validation for each response-create frame because the existing socket account proves only the current route. Single-account routing MUST constrain effective routing without narrowing the ownership-candidate pool used by that validation.

When an HTTP-bridge owner is on another replica, the origin MUST forward its resolved durable file owner in authenticated full-context metadata. The receiving owner MUST perform its own fresh shared-database lookup and MUST require that durable result to match the forwarded owner. A missing or conflicting receiver-side durable owner MUST fail closed before account selection or upstream invocation. A retired direct WebSocket's upstream turn-state token MUST NOT be sent to a different account selected for a later movable bare-session request.

A nonblank `conversation` without a dedicated resolved owner MUST proceed only when an explicit hard Codex mapping proves ownership or exactly one account remains in the model/API-key/security-scoped selection pool before transient additional-quota availability, retry exclusions, runtime health, budget, or account-cap filtering. A temporarily quota-filtered, excluded, unhealthy, or capped candidate MUST remain part of this ambiguity check because it may be the actual owner. A bare process-session mapping MUST NOT prove conversation ownership.

#### Scenario: Previous-response owner queue is saturated

- **WHEN** a `/v1/responses` follow-up requires a previous-response owner
- **AND** the owner session queue or account cap is saturated
- **THEN** the service fails closed with `hard_affinity_saturated`, `previous_response_owner_unavailable`, or the applicable stable `account_stream_cap` / `account_response_create_cap` code
- **AND** it does not route to an unrelated account that lacks continuity state

#### Scenario: File-pinned request owner is capped

- **WHEN** a `/v1/responses` request references an `input_file.file_id` pinned to an owner account
- **AND** the owner account is at its account stream or response-create cap
- **THEN** the service returns a local account-cap overload for the owner
- **AND** it does not route the file reference to another account

#### Scenario: File-pinned request owner overrides process-session locality

- **GIVEN** a request carries a bare process-session header mapped to account A
- **AND** its `input_file.file_id` is durably pinned to account B
- **WHEN** the request is routed
- **THEN** account B is treated as the required owner
- **AND** the process-session mapping is neither consulted as an owner nor rewritten

#### Scenario: File-pinned request owner overrides thread locality

- **GIVEN** a request carries a `thread-id` whose bounded mapping points to account A
- **AND** its `input_file.file_id` is durably pinned to account B
- **WHEN** the request is routed
- **THEN** account B is treated as the required owner
- **AND** the thread mapping is neither consulted as an owner nor rewritten

#### Scenario: Conflicting hard owners fail closed

- **GIVEN** a turn state, previous response, bridge, or input file resolves to account A
- **AND** another hard source on the same request resolves to account B
- **WHEN** the request is routed
- **THEN** the service fails with `continuity_owner_conflict` before upstream dispatch
- **AND** source ordering does not choose either owner

#### Scenario: Partial or cross-account file pins fail closed

- **GIVEN** a request references multiple account-scoped input files
- **AND** at least one file has a live durable owner pin
- **AND** another file has no live durable owner pin or the live pins resolve to different accounts
- **WHEN** the request is routed
- **THEN** the service fails with `file_owner_unavailable` or `continuity_owner_conflict`
- **AND** it does not route the files using a soft affinity account

#### Scenario: Opaque file IDs with no live durable pins preserve compatibility

- **GIVEN** a request references one or more `input_file.file_id` values
- **AND** none of those IDs has a live durable owner pin
- **WHEN** the request is routed
- **THEN** the service forwards the opaque file references under ordinary unpinned routing
- **AND** it does not invent a hard owner or fail solely because durable pin metadata is absent

#### Scenario: Ambiguous conversation fails closed

- **GIVEN** a request carries nonblank `conversation` continuity and only bare process-session affinity
- **AND** more than one account is eligible
- **WHEN** no dedicated or hard-mapping owner can be resolved
- **THEN** the request fails with a stable owner-unavailable error before upstream dispatch

#### Scenario: Account-cap pressure does not manufacture a conversation owner

- **GIVEN** two accounts remain in the model/API-key/security-scoped selection pool
- **AND** one account is temporarily at its local account cap
- **WHEN** a request carries nonblank `conversation` continuity without a dedicated or hard-mapping owner
- **THEN** the request still fails with a stable owner-unavailable error
- **AND** the uncapped account is not treated as the unique owner

#### Scenario: Retry or additional-quota filtering does not manufacture a conversation owner

- **GIVEN** two accounts remain in the model/API-key/security-scoped selection pool
- **AND** retry exclusion or transient additional-quota availability removes one from the effective routing pool
- **WHEN** a request carries nonblank `conversation` continuity without a dedicated or hard-mapping owner
- **THEN** the request still fails with a stable owner-unavailable error
- **AND** the remaining effective account is not treated as the unique owner

#### Scenario: Account status does not manufacture a conversation owner

- **GIVEN** two accounts are in the model/API-key/security ownership pool
- **AND** one account is paused, requires reauthentication, deactivated, or otherwise unavailable for routing
- **WHEN** a request carries nonblank `conversation` continuity without a dedicated or hard-mapping owner
- **THEN** the request still fails with a stable owner-unavailable error
- **AND** the active account is not treated as the unique owner

#### Scenario: Preferred file owner does not manufacture a conversation owner

- **GIVEN** a request carries nonblank `conversation` continuity and a file durably pinned to account B
- **AND** another account remains in the model/API-key/security ownership pool
- **WHEN** no dedicated conversation owner can be resolved
- **THEN** file ownership does not narrow the conversation ambiguity check to account B
- **AND** the request fails closed before upstream dispatch

#### Scenario: Bridge turn state is owner-bound across transports

- **GIVEN** an HTTP bridge registered a turn-state alias for account A
- **WHEN** the alias is reused through compact, plain HTTP streaming, or direct WebSocket transport
- **THEN** each transport treats account A as the required owner
- **AND** it does not fall back to unrelated sticky affinity

#### Scenario: Independent bridge aliases conflict

- **GIVEN** a live or durable turn-state alias resolves to one bridge session
- **AND** a previous-response alias on the same request resolves to a distinct session or account
- **WHEN** the request is routed
- **THEN** the service fails with `continuity_owner_conflict`
- **AND** alias lookup order does not select either session

#### Scenario: Reused WebSocket revalidates conversation ownership

- **GIVEN** a direct upstream WebSocket is already open on account A
- **AND** a later response-create frame carries nonblank `conversation`
- **WHEN** more than one account remains in the ownership-candidate pool
- **THEN** the later frame fails with a stable owner-unavailable error before upstream send
- **AND** the existing socket account is not treated as ownership proof

#### Scenario: Single-account routing does not manufacture conversation ownership

- **GIVEN** single-account routing selects account A
- **AND** multiple accounts remain in the model/API-key/security ownership pool
- **WHEN** a request carries nonblank `conversation` without dedicated owner evidence
- **THEN** the request remains ambiguous and fails closed
- **AND** only the effective routing states are constrained to account A

#### Scenario: Remote bridge owner revalidates forwarded file ownership

- **GIVEN** origin replica A durably resolves an input file to account A
- **AND** the request's HTTP bridge owner runs on replica B
- **WHEN** replica A forwards the request to replica B with authenticated file-owner metadata
- **THEN** replica B MUST freshly resolve the shared durable pin
- **AND** it MUST accept the forwarded owner only when both owner values match
- **AND** a missing, conflicting, tampered, or legacy-unbound proof MUST be rejected before upstream invocation

#### Scenario: Retired WebSocket turn state does not cross accounts

- **GIVEN** a closed upstream WebSocket on account A supplied an account-scoped turn-state token
- **AND** a later movable bare-session frame or marked self-contained goal restart selects account B
- **WHEN** the proxy opens the replacement WebSocket
- **THEN** it removes account A's stale turn-state token before connect
- **AND** account B never receives that token

### Requirement: Required continuity-owner selection failures are explicit

Account selection MUST distinguish a proven request continuity owner from an ordinary preferred account or configured routing restriction. Durable continuity provenance, including a soft prompt-cache follow-up whose durable record contains a latest turn state, MUST make the preferred account mandatory for local reuse and fresh selection. When a required continuity owner cannot be returned because that owner no longer exists or is unavailable after supported selection reloads, selection MUST return `continuity_owner_unavailable`. When the owner exists but is outside the effective model, API-key, security, authorization, or routing policy, selection MUST return `continuity_owner_policy_conflict` or the more specific existing policy code. Stable local capacity codes MUST remain unchanged. The HTTP bridge MUST translate only a typed `continuity_owner_unavailable` selection result for its required owner to `previous_response_owner_unavailable`.

#### Scenario: Required owner is unavailable while another account is healthy

- **GIVEN** a follow-up has proven account A as its continuity owner
- **AND** account B remains available for unrelated traffic
- **WHEN** account A cannot be selected after supported selection reloads
- **THEN** selection returns `continuity_owner_unavailable`
- **AND** the HTTP bridge returns `previous_response_owner_unavailable` unless verified replay or automatic client-history switching applies
- **AND** it does not select account B as the unchanged continuation owner

#### Scenario: Required owner conflicts with selection policy

- **GIVEN** a follow-up has proven account A as its continuity owner
- **WHEN** account A is outside the request's model, API-key, security, authorization, or routing policy
- **THEN** selection returns `continuity_owner_policy_conflict` or the existing more-specific policy code
- **AND** the bridge does not convert that result into replay permission

#### Scenario: Soft prompt-cache follow-up has durable continuity provenance

- **GIVEN** a soft prompt-cache follow-up resolves durable account A and a latest turn state
- **AND** a stale local lane for the same prompt-cache key uses account B
- **WHEN** the bridge reuses or creates the follow-up lane
- **THEN** it rejects the stale account-B lane and requires account A
- **AND** account selection cannot switch to B before verified replay proof or automatic client-history switching applies

#### Scenario: Soft prompt-cache first turn changes model

- **GIVEN** a first-turn request reuses a soft prompt-cache key whose durable row was written for another model
- **AND** the request carries no previous-response, turn-state, or session-header continuation
- **WHEN** the bridge isolates the incompatible durable lane
- **THEN** it does not make the stale durable account a required continuity owner
- **AND** ordinary first-turn account selection remains available

#### Scenario: Required owner reaches a local capacity cap

- **WHEN** a required owner reaches `account_stream_cap` or `account_response_create_cap`
- **THEN** selection preserves that code and its `429` classification
- **AND** bounded local-cap recovery remains available

#### Scenario: Failure occurs after the owner was selected

- **GIVEN** the required continuity owner was selected successfully
- **WHEN** token refresh, authentication, connection, timeout, or another transport step fails
- **THEN** the failure retains its ordinary authentication or upstream classification
- **AND** it is not rewritten to `previous_response_owner_unavailable`
