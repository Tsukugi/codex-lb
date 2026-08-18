# Client conversation handoff recovery design

## Purpose

Recover a conversation when its required upstream owner account is unavailable.
The recovery moves to an available account as a new conversation. It does not
pretend that a foreign account can resume the old `previous_response_id`.

The client owns the handoff. The proxy keeps its current account-ownership
rule. This avoids retaining every transcript in the proxy.

## Scope

The recovery starts only for the typed owner-unavailable error. It applies when
the client has enough visible context to start a useful new conversation.

It does not migrate the upstream response object. It does not change a normal
continuation. It does not make an account-scoped file, tool session, or hidden
reasoning state portable.

## User flow

1. The client receives `previous_response_owner_unavailable`.
2. The client stops retrying the same `previous_response_id`.
3. The client builds a handoff document from its local conversation state.
4. The client starts a new conversation without `previous_response_id`.
5. The client sends the handoff as the initial context to an available account.
6. The client tells the user that this is a recovered conversation.

The client should offer a clear action such as **Continue in new conversation**.
It must not recover silently.

## Handoff document

The handoff is a bounded Markdown document. It is created only when recovery
is requested. It is not a background transcript archive.

```md
# Conversation handoff

## Goal
<The current user goal.>

## Conversation summary
<A concise summary of decisions and progress.>

## Recent transcript
<The most relevant recent user and assistant messages.>

## Completed work
<Files changed, commands run, and important results.>

## Constraints
<Rules that the new conversation must preserve.>

## Tool and file state
<Portable tool results and files that must be re-uploaded.>

## Continue from here
<The next concrete user request.>
```

The client should prefer a concise summary plus recent turns. It should include
older turns only when they are needed to preserve a decision or constraint.

## Portable and non-portable state

Portable state includes visible text, user instructions, local file paths when
the new account can access them, completed tool results, and explicit decisions.

Non-portable state includes `previous_response_id`, hidden reasoning,
account-owned uploaded files, remote tool sessions, server-side cursors, and
cached prompt state. The handoff must list non-portable items plainly so the new
conversation can re-create or re-upload them.

## Failure modes

If the client has no local transcript, it must not attempt recovery. It should
show the owner-unavailable error and offer a new empty conversation.

If the conversation uses files or tools, the handoff must list the missing
items. The new conversation must not claim that those resources were moved.

If generating the handoff fails, the client must preserve the original error.
It must not send a partial handoff as though it were complete.

## Privacy and cost

The handoff remains in client memory or client-controlled storage. The proxy
does not persist it. The client creates it only after an owner-unavailable
failure and only sends it to the newly selected account after user approval.

The handoff has a size budget. The client should summarize old turns before it
adds them. If it exceeds the budget, it should ask the user to choose what to
retain rather than silently dropping constraints.

## Observability

Record a client recovery event with a non-sensitive outcome:

- `offered`
- `accepted`
- `declined`
- `not_portable`
- `handoff_generation_failed`
- `new_conversation_started`

Do not record transcript text, file names, response IDs, or tool arguments in
these events.

## Example

The old account is rate-limited. The client receives
`previous_response_owner_unavailable` for a coding conversation. It offers a
handoff. The user accepts. The client creates a document with the goal, the
last decisions, changed files, test results, and the next requested change.
It starts a new request on the available account with no
`previous_response_id`. The new account continues from the handoff and asks to
re-upload any account-owned file that is needed.

## Rollout

Start behind a client feature flag. Enable it for plain-text conversations
first. Add tool and file support only after the client can describe and
re-create their state without hiding gaps. Keep the proxy error unchanged.

## /grill me

### Does this hide a broken continuation?

No. The user must approve a new conversation, and the UI must call it a
recovery. The old continuation remains unavailable until its owner recovers.

### Does it add proxy storage overhead?

No. The proxy stores no new transcript data. The client creates the handoff
only after this specific failure.

### Can a summary lose important context?

Yes. The design keeps recent turns and explicit constraints, and it asks the
user to choose when the size budget would drop needed context.

### Can it migrate files and tools safely?

Not in the first version. It lists them as missing work that must be re-created
or re-uploaded. Claiming automatic migration would be unsafe.

### Why not reroute `previous_response_id` directly?

The ID is owned by the original upstream account. The new account cannot read
or resume it. Direct rerouting produces an invalid continuation.
