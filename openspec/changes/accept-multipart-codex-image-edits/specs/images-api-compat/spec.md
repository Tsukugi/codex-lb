## ADDED Requirements

### Requirement: Codex-base image edits accept both supported transports

`POST /backend-api/codex/images/edits` SHALL accept both the Codex JSON
data-URL request shape and the canonical OpenAI multipart image-edit request
shape. Multipart handling MUST use the same authorization order, bounded parser,
form validation, image-byte ordering, shared edit pipeline, observability, and
error-envelope behavior as `POST /v1/images/edits`.

#### Scenario: OpenAI SDK multipart edit uses the Codex-base alias

- **WHEN** an OpenAI SDK client posts a valid multipart image edit to
  `POST /backend-api/codex/images/edits`
- **THEN** the service forwards each image part as `input_image` content through
  the shared edit pipeline
- **AND** returns the same OpenAI Images response envelope as the canonical
  `/v1/images/edits` endpoint

#### Scenario: Codex JSON data-URL edits remain supported

- **WHEN** a Codex client posts its existing JSON `images[].image_url` data URLs
  to `POST /backend-api/codex/images/edits`
- **THEN** the service retains the existing shared edit-pipeline behavior
