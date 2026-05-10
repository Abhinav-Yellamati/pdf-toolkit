# Production API Routing

## Problem

The web frontend must call the deployed Render backend, not a local development URL.

## Solution

- Web API calls now go through `frontend-web/src/services/apiClient.js`.
- Environment handling lives in `frontend-web/src/config/api.js`.
- `REACT_APP_API_BASE` can point directly to the full deployed PDF API base.
- `REACT_APP_API_ORIGIN` can point to the Render origin; the client discovers the PDF prefix from `/openapi.json`.
- Backend exposes `/api/meta` with the current PDF prefix.
- Backend CORS supports explicit Vercel origins and Vercel preview deployments.

## Production Variables

Vercel:

```text
REACT_APP_API_BASE=https://your-render-service.onrender.com/api/pdf
REACT_APP_API_TIMEOUT_MS=120000
```

Render:

```text
CORS_ORIGINS=https://your-vercel-app.vercel.app,https://your-custom-domain.com
CORS_ORIGIN_REGEX=https://.*\.vercel\.app
```

## Verification

```powershell
$env:RENDER_API_BASE="https://your-render-service.onrender.com/api/pdf"
powershell -ExecutionPolicy Bypass -File scripts/verify-deployment.ps1
```
