# Testing Report

## Current Baseline - 2026-05-10

### APIs Tested
- `GET /health`: existing logs report HTTP 200 over LAN.
- `POST /api/pdf/compress`: existing logs report HTTP 200 and successful output generation.
- CORS preflight: existing backend log reports verification for mobile-origin style requests.

### Mobile Tests
- Existing mobile runtime logs report clean Android bundle generation.
- Existing Expo logs report a fresh LAN server on port `8087`.
- Existing mobile runtime logs report Android bundle served by Metro with HTTP 200.

### Frontend Tests
- Existing frontend logs report API default alignment for the web client.
- No fresh web test was executed during this documentation-only setup.

### Failed Tests
- No new test failures occurred during this documentation-only setup.
- `git status --short` could not run because `git` is unavailable in the current shell environment.

### Fixes After Failed Tests
- No code fixes were made in this setup session.

### Performance Observations
- PDF processing uses temporary workspaces and background cleanup, which should be monitored for large files and repeated mobile uploads.
- Compression quality and image DPI are bounded in the backend service to reduce extreme resource usage.

### Next Validation Checklist
- Start backend and verify `/health`.
- Run one upload/download test for each PDF tool.
- Start web frontend and verify file selection, progress, result download, and error states.
- Start Expo with LAN host and verify physical-device upload/download.
- Record all command outputs in `logs/test-results.log`.

## Full QA Pass - 2026-05-10

- Generated `test-assets/` with realistic PDFs, result folders, screenshots, and CSV/JSON reports.
- Backend API testing passed for compression, merge, rearrange, split, PDF-to-Word, PDF-to-image, image-to-PDF, text watermark, password protection, invalid upload handling, CORS, health, and concurrent upload checks.
- Web production build passed.
- Web Jest smoke test initially failed due to a stale Create React App assertion and passed after updating the test to match the current PDF Toolkit UI.
- Expo Android export passed.
- Physical mobile-device testing and browser screenshot automation were not executed because no device/browser automation was available in this environment.
