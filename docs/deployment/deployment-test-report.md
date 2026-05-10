# Deployment Test Report

## 2026-05-10 Local Production-Readiness Validation

| Area | Result | Notes |
| --- | --- | --- |
| Backend production config | Prepared | `render.yaml`, `Procfile`, env examples, security headers, `/ready` |
| Web production config | Prepared | `vercel.json`, production env examples, metadata updates |
| Mobile production config | Prepared | `eas.json`, production env example, icon/splash assets |
| Backend QA runner | Passed | 15 compression, 3 merge, 2 rearrange, 3 split, 3 conversion, 3 watermark, 1 password case |
| Backend health/docs | Passed | `/health`, `/ready`, and `/docs` returned HTTP 200 through TestClient |
| Web production build | Passed | `npm.cmd run build` compiled successfully with production-style API env |
| Web smoke test | Passed | `npm.cmd test -- --watchAll=false` passed |
| Expo Android export | Passed | `npx.cmd expo export --platform android --output-dir dist-qa` passed |
| Public deployment | Pending credentials | Requires authenticated Vercel, Render, and Expo accounts |

Final live URL verification must be completed after the services are deployed.
