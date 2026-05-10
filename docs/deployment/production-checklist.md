# Production Checklist

## Backend

- [ ] Render service created.
- [ ] `ENVIRONMENT=production` set.
- [ ] `CORS_ORIGINS` includes Vercel and custom domains.
- [ ] `/health` returns 200.
- [ ] `/ready` returns 200.
- [ ] `/docs` opens.
- [ ] Upload/download APIs work with sample PDFs.

## Web

- [ ] Vercel project root set to `frontend-web`.
- [ ] `REACT_APP_API_BASE` points to Render `/api/pdf`.
- [ ] `npm run build` passes.
- [ ] Public site loads over HTTPS.
- [ ] Compress, merge, split, watermark, and protect flows work.

## Mobile

- [ ] Expo project configured.
- [ ] `frontend-mobile/eas.json` uses Render API URL.
- [ ] Preview APK builds.
- [ ] Production AAB builds.
- [ ] Physical device upload/download flows pass.

## GitHub

- [ ] `.gitignore` excludes dependencies, build outputs, local env files, storage, uploads, and generated heavy test assets.
- [ ] README includes production deployment notes.
- [ ] Deployment docs are committed.
- [ ] Logs and changelog include deployment-prep history.

## Domain

- [ ] Custom frontend domain added in Vercel.
- [ ] Custom API domain or Render URL confirmed.
- [ ] Backend CORS updated with final domains.
- [ ] HTTPS verified on frontend and backend.

