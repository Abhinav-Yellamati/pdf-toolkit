# Backend Boot Flow

## Production Boot Path

The production Render service should use:

```text
Root Directory: backend
Start Command: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

With `backend` as the working directory, Python imports `backend/app/main.py` as `app.main`.

## FastAPI Startup Sequence

1. Render installs `backend/requirements.txt`.
2. Render runs uvicorn with `app.main:app`.
3. `backend/app/main.py` creates the FastAPI app with `/docs` and `/openapi.json` enabled.
4. CORS middleware is configured for the production Vercel app and preview deployments.
5. Core routes are registered: `/`, `/health`, `/ready`, and `/api/meta`.
6. The PDF router is mounted at `/api/pdf`.
7. Startup validation checks every required public route.
8. Startup logs print app identity, environment, docs state, CORS settings, router prefix, PDF routes, and public route paths.

## Route Validation

The backend fails startup if any of these required paths is missing:

```text
/
/health
/ready
/docs
/openapi.json
/api/meta
/api/pdf/compress
/api/pdf/merge
/api/pdf/split
/api/pdf/rearrange
/api/pdf/pdf-to-word
/api/pdf/pdf-to-image
/api/pdf/image-to-pdf
/api/pdf/watermark
/api/pdf/protect
```

## Interpreting Render Logs

Correct logs include:

```text
PDF Toolkit FastAPI app started successfully
App object: backend.app.main:app or app.main:app
Docs enabled: True
Registered routers: PDF router mounted at /api/pdf
Registered PDF routes: [...]
Registered public routes: [...]
```

If Render logs instead mention `gunicorn`, Flask, `main:app`, or do not contain these startup lines, the service is running the wrong deployment configuration.
