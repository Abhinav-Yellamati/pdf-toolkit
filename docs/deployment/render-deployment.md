# Render Deployment

## Required Current Render Settings

Use these exact values for the production backend service:

```text
Service Type: Web Service
Runtime: Python
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
Health Check Path: /health
```

Required environment variables:

```text
ENVIRONMENT=production
LOG_LEVEL=INFO
ENABLE_DOCS=1
MAX_FILE_MB=100
CORS_ORIGINS=https://pdf-toolkit-black-ten.vercel.app
CORS_ORIGIN_REGEX=https://.*\.vercel\.app
```

The single recommended production startup path is `app.main:app` with Render Root Directory set to `backend`.

If Render is configured with repository root instead of `backend`, the compatible fallback is:

```text
Build Command: pip install -r requirements.txt
Start Command: python -m uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
```

Do not use gunicorn, Flask, `main:app`, or `backend.main:app` for this deployment.

## Purpose

Deploy `backend` as the public FastAPI API service.

## Generic Render Settings

- Service type: Web Service
- Runtime: Python
- Root directory: `backend`
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Health check path: `/health`

The repository also includes root-level `render.yaml` for blueprint deployment. Its authoritative settings match the required settings above.

## Environment Variables

```text
ENVIRONMENT=production
LOG_LEVEL=INFO
ENABLE_DOCS=1
MAX_FILE_MB=100
CORS_ORIGINS=https://your-vercel-app.vercel.app,https://your-custom-domain.com
```

## Production Endpoints

- `/health`
- `/ready`
- `/docs`
- `/api/pdf/compress`
- `/api/pdf/merge`
- `/api/pdf/split`
- `/api/pdf/rearrange`
- `/api/pdf/pdf-to-word`
- `/api/pdf/pdf-to-image`
- `/api/pdf/image-to-pdf`
- `/api/pdf/watermark`
- `/api/pdf/protect`

## Verification

1. Open `https://your-render-api.onrender.com/health`.
2. Open `https://your-render-api.onrender.com/docs`.
3. Use the Swagger UI or frontend app to upload sample files.
4. Confirm response files download correctly.
5. Check Render logs for handled errors and timing lines.

Run the local structure audit before pushing:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/verify-backend-structure.ps1
```

Run the public deployment verifier after Render redeploys:

```powershell
$env:RENDER_API_ORIGIN="https://pdf-toolkit-backend.onrender.com"
powershell -ExecutionPolicy Bypass -File scripts/verify-deployment.ps1
```
## Live 404 Diagnosis

If `https://pdf-toolkit-backend.onrender.com/health`, `/docs`, and `/openapi.json` return 404, Render is not running the current FastAPI app. The current source exposes those routes locally and startup validation now fails loudly if they are absent.

After redeploy, Render logs must include:

```text
PDF Toolkit FastAPI app started successfully
Docs enabled: True
Registered routers: PDF router mounted at /api/pdf
Registered PDF routes: [...]
Registered public routes: [...]
```

If these lines do not appear, check the service branch, root directory, build command, start command, and whether the service is connected to the correct repository. If all values are correct and 404s continue after "Clear build cache and deploy", delete the Render service and create a new one.
