# GitHub Deployment Guide

## Repository Preparation

Before pushing:

1. Confirm `.gitignore` excludes `node_modules`, `venv`, `.env`, build outputs, uploads, storage, and heavy generated test assets.
2. Keep source, docs, deployment configs, and lightweight reports.
3. Do not commit production secrets.

## Suggested Repository Structure

```text
backend/
frontend-web/
frontend-mobile/
docs/
logs/
history/
changelog/
render.yaml
Procfile
CHANGELOG.md
README.md
```

## Deployment Flow

1. Push repository to GitHub.
2. Connect Render to the GitHub repository and deploy the backend.
3. Copy the Render API URL.
4. Connect Vercel to the same repository and deploy `frontend-web`.
5. Set Vercel `REACT_APP_API_BASE` to the Render `/api/pdf` URL.
6. Update Render `CORS_ORIGINS` with the Vercel URL.
7. Configure EAS with the same backend API URL.

