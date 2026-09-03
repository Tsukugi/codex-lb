# Accept multipart Codex-base image edits

## Why

OpenAI SDK clients configured with Codex LB's native base URL send multipart
image-edit requests to `/backend-api/codex/images/edits`. That alias currently
accepts only Codex's JSON data-URL transport and rejects the SDK request before
the shared image-edit pipeline runs.

## What Changes

- Accept the canonical OpenAI multipart image-edit request shape on the
  Codex-base alias.
- Reuse the existing bounded multipart parser and shared edit pipeline.
- Preserve the alias's existing JSON data-URL transport.

## Impact

- Affected capability: `images-api-compat`
- Affected route: `POST /backend-api/codex/images/edits`
