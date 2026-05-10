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
REACT_APP_API_BASE=https://pdf-toolkit-api.onrender.com/api/pdf
REACT_APP_API_ORIGIN=https://pdf-toolkit-api.onrender.com
REACT_APP_API_URL=https://pdf-toolkit-api.onrender.com
REACT_APP_API_TIMEOUT_MS=120000
```

Render:

```text
ENVIRONMENT=production
PYTHON_VERSION=3.12.8
LOG_LEVEL=INFO
ENABLE_DOCS=1
MAX_FILE_MB=100
CORS_ORIGINS=https://pdf-toolkit-black-ten.vercel.app
CORS_ORIGIN_REGEX=https://.*\.vercel\.app
```

## Correct Render Boot Target

Use one deployment shape only:

```text
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
Health Check Path: /health
```

With this root directory, `app.main:app` resolves to `backend/app/main.py`. The repository-root target `backend.app.main:app` exists only as a compatibility fallback for services that cannot set Root Directory.

## Verification

```powershell
$env:RENDER_API_BASE="https://your-render-service.onrender.com/api/pdf"
powershell -ExecutionPolicy Bypass -File scripts/verify-deployment.ps1
```

