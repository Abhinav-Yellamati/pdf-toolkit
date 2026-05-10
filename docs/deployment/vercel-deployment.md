# Vercel Deployment

## Purpose

Deploy `frontend-web` as the public PDF Toolkit website.

## Required Backend URL

Deploy the Render backend first, then use its public URL:

```text
https://your-render-api.onrender.com/api/pdf
```

## Vercel Project Settings

- Framework: Create React App
- Root directory: `frontend-web`
- Build command: `npm run build`
- Output directory: `build`
- Install command: `npm install`

## Environment Variables

```text
REACT_APP_API_BASE=https://your-render-api.onrender.com/api/pdf
REACT_APP_API_TIMEOUT_MS=120000
```

## Files Added

- `frontend-web/vercel.json`
- `frontend-web/.env.example`
- `frontend-web/.env.production.example`

## Verification

1. Run `npm.cmd run build` locally.
2. Deploy the Vercel project.
3. Open the Vercel URL.
4. Upload a sample PDF and test compression.
5. Confirm download works and browser console has no API URL errors.

## Custom Domain

In Vercel, add the domain under Project Settings -> Domains. After the domain is active, add it to backend `CORS_ORIGINS` on Render.

