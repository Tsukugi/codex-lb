## 1. Implementation

- [x] 1.1 Route multipart requests on the Codex-base image-edit alias through the existing bounded multipart parsing path.
- [x] 1.2 Preserve JSON data-URL behavior and the shared validation, authorization, observability, and edit pipeline.

## 2. Coverage

- [x] 2.1 Add a route-level regression proving an OpenAI SDK-style multipart request succeeds on the Codex-base alias and forwards the image as `input_image` content.

## 3. Verification

- [ ] 3.1 Run the focused image-route regression test.
- [ ] 3.2 Validate this OpenSpec change and the main specs.
