# Public Deployment Fixes

## User-Facing Problem

The Vercel website opened correctly, but PDF tools failed with `Failed to fetch` for public users.

## Investigation

Frontend:

- `https://pdf-toolkit-black-ten.vercel.app` is publicly reachable.
- The deployed JavaScript bundle includes `https://pdf-toolkit-backend.onrender.com`.
- Therefore the browser is attempting to use the Render backend.

Backend:

- `https://pdf-toolkit-backend.onrender.com/docs` returned 404.
- `https://pdf-toolkit-backend.onrender.com/openapi.json` returned 404.
- `https://pdf-toolkit-backend.onrender.com/api/pdf/compress` returned 404 or connection reset.
- Response headers indicated a Gunicorn origin and Flask-style 404 page, not the current FastAPI app.

## Root Cause

Render is not launching the current FastAPI ASGI app from this repository. The current source works locally and exposes the required routes, but the deployed service is stale or configured with the wrong start command/root directory.

## Fixes Implemented

- Added root-level `main.py` that exposes `backend.app.main:app`.
- Added root-level `requirements.txt`.
- Added `backend/__init__.py`.
- Converted backend imports to package-relative imports.
- Updated `Procfile` for root-level deployment.
- Updated `render.yaml` for backend-root deployment.
- Updated CORS defaults for the production Vercel domain and Vercel previews.
- Updated frontend API config to fall back to the Render backend in production.
- Added support for `REACT_APP_API_URL`.
- Removed production-loaded localhost fallbacks.

## Required Redeploy

Render must be redeployed from this updated repository. Until that happens, public users will still hit the stale backend.
