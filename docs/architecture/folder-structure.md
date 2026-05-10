# Folder Structure

```text
pdf-project/
  backend/
    app/
      main.py
      routes/
      services/
      utils/
    main.py
    requirements.txt
  frontend-web/
    public/
    src/
      components/
      config/
      services/
      utils/
  frontend-mobile/
    src/
      components/
      config/
      services/
      utils/
    App.js
    app.json
  shared/
    api-contract.md
  docs/
    architecture/
    api/
    frontend/
    mobile/
    backend/
    debugging/
    deployment/
    screenshots/
    logs/
```

## Backend

The backend contains FastAPI app setup, route handlers, validation utilities, file utilities, and PDF processing services.

## Web Frontend

The web frontend contains reusable UI components, tool configuration, upload validation, and browser download handling.

## Mobile Frontend

The mobile frontend contains React Native components, Expo document picking, LAN-aware API configuration, mobile upload handling, and native sharing.

## Docs

The docs folder is organized by audience: architecture reviewers, API users, frontend/mobile/backend developers, debugging sessions, deployment steps, and viva preparation.

## History And Logs

```text
logs/                 Append-only engineering logs
changelog/            Changelog maintenance policy
history/              Session-level project memory
CHANGELOG.md          Keep-a-Changelog project history
```

Generated dependency/build/runtime folders such as `node_modules`, `venv`, `.expo`, `build`, `dist`, `__pycache__`, and generated backend output PDFs should be treated as generated artifacts unless the project owner intentionally wants to preserve them.
