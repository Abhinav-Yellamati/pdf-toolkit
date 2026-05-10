# Debugging Timeline

## 2026-05-10 - Documentation And Traceability Setup

### Symptoms
The project had useful documentation and some runtime logs, but the required complete historical system was incomplete. Several required log files, changelog files, testing records, presentation documents, and architecture documents were missing.

### Investigation Process
The project directory was located under `C:\Users\abhin\Downloads\pdf-project`. The top-level README, backend FastAPI entry point, PDF routes, PDF service layer, frontend/mobile folders, and existing logs were inspected. Existing logs showed prior work on Expo runtime stabilization, LAN backend access, API upload checks, and CORS/mobile networking.

### Why The Issue Occurred
Documentation had grown organically around individual fixes and presentation needs. There was no single enforced project rule that every change must update logs, changelog, session history, testing notes, and relevant architecture or presentation documents.

### Solution
Created the missing documentation and logging files, added a root changelog, added a logging policy, and recorded this session as the baseline for future chronological maintenance.

### Lessons Learned
Professional project history should be updated at the same time as code changes. Debugging notes are most useful when they preserve symptoms, investigation steps, root cause, solution, and validation result.

## Known Debugging Areas To Track

- Expo and Metro startup failures.
- LAN, WSL, ngrok, and tunnel connectivity problems.
- FastAPI validation errors and uncaught backend exceptions.
- React web upload/download issues.
- Mobile runtime crashes and Expo Go compatibility issues.
- PDF upload, processing, download, and cleanup failures.

