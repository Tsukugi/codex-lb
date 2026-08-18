## 1. Design validation

- [ ] 1.1 Confirm the client has access to the visible transcript and current task state.
- [ ] 1.2 Define the handoff size budget and user approval UX.
- [ ] 1.3 Define the first-release portability rules for text, files, and tools.

## 2. Implementation

- [ ] 2.1 Add typed handling for the owner-unavailable response in the client.
- [ ] 2.2 Generate the client-owned handoff document after user approval.
- [ ] 2.3 Start a new conversation without `previous_response_id` on an available account.

## 3. Verification

- [ ] 3.1 Test plain-text recovery without proxy transcript storage.
- [ ] 3.2 Test refusal or explicit re-upload guidance for file and tool state.
- [ ] 3.3 Test that normal owner-bound continuations remain unchanged.
