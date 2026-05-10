# Changelog And Logging Policy

This directory explains how project history must be maintained.

Every meaningful change must update:

- `CHANGELOG.md` for user-visible and project-level changes.
- A relevant file in `logs/` for engineering detail.
- `history/session-history.md` for session-level memory.
- A relevant document under `docs/` when architecture, APIs, UI behavior, setup, testing, or presentation material changes.

Log entries are append-only. Do not remove older entries unless the project owner explicitly asks for archival cleanup.

Each log entry should include timestamp, affected files, issue description, root cause, fix implemented, result after fix, commands executed, and important observations.

