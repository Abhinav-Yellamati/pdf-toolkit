# Changelog

All notable changes to this project will be documented in this file.

The format follows Keep a Changelog style. Dates use `YYYY-MM-DD`.

## [Unreleased]

### Added
- Added Python runtime pinning for Render through `backend/runtime.txt` and `PYTHON_VERSION=3.12.8` in `render.yaml`.
- Added `scripts/verify-backend-structure.ps1` to audit deployment files, package declarations, startup commands, and required FastAPI routes.
- Added FastAPI startup diagnostics that log the app object, environment, docs state, CORS configuration, mounted routers, and registered routes.
- Added startup route validation so the backend fails loudly if `/health`, `/docs`, `/openapi.json`, `/api/meta`, or any `/api/pdf/*` route is missing.
- Added root-level Render-compatible FastAPI entrypoint and requirements forwarding for deployment-root ambiguity.
- Added public deployment debugging logs, route map, and API test reports.
- Added `scripts/verify-deployment.ps1` to detect deployed FastAPI route prefixes and validate all 9 PDF endpoints.
- Added `logs/deployment-verification.md` with endpoint verification results.
- Added `docs/deployment/production-api-routing.md` documenting Render/Vercel API routing configuration.
- Created a complete project documentation and traceability system with `/logs`, `/docs`, `/changelog`, and `/history`.
- Added required append-only logs for development, build, dependency, testing, and test-result history.
- Added presentation-ready documentation for BTP review, viva preparation, demo flow, challenges, solutions, and future scope.
- Added architecture documentation for backend, frontend, API flow, folder structure, and PDF processing lifecycle.
- Added session history and debugging timeline files for future maintenance continuity.
- Added full-system QA assets, automated backend test runner, visual comparison artifacts, and testing reports under `docs/testing/`.
- Added Render, Vercel, and EAS deployment configuration files.
- Added production deployment, domain, HTTPS, GitHub, and verification documentation.
- Added Expo app icon, adaptive icon, and splash assets.

### Changed
- Updated `scripts/verify-deployment.ps1` to validate `/health`, `/docs`, `/openapi.json`, `/api/meta`, and all 9 PDF tool endpoints.
- Added explicit `pydantic` dependency to `backend/requirements.txt`.
- Updated Render and Vercel production configuration to use the real public URLs.
- Converted backend imports to package-relative imports so both root and backend uvicorn module paths work.
- Updated web and backend environment examples for `REACT_APP_API_ORIGIN`, `REACT_APP_API_BASE`, and `CORS_ORIGIN_REGEX`.
- Consolidated project maintenance expectations into a formal logging policy under `changelog/README.md`.
- Updated the web frontend smoke test to assert the current PDF Toolkit app shell instead of the default Create React App placeholder.
- Changed backend runtime defaults toward production-safe behavior, including disabled reload by default and restricted CORS defaults.
- Changed web and mobile API configuration examples from LAN/local-only values to production-ready URL placeholders.

### Fixed
- Removed stray backend Node deployment markers (`backend/package.json` and `backend/package-lock.json`) that could cause Render to run the backend as Node/Express.
- Updated production API origin from `https://pdf-toolkit-backend.onrender.com` to `https://pdf-toolkit-api.onrender.com`.
- Changed `/health` to return `{"status":"ok"}` for the public Render health check contract.
- Fixed the root `Procfile` to use Render's provided `$PORT` directly with the root-compatible FastAPI ASGI target.
- Fixed production frontend fallback so Vercel builds without API env vars still call `https://pdf-toolkit-api.onrender.com/api/pdf`.
- Fixed compatibility with the deployed Vercel `REACT_APP_API_URL` environment variable.
- Fixed Render deployment ambiguity by supporting both `backend.app.main:app` and `app.main:app` startup paths.
- Removed localhost fallbacks from production-loaded web/backend runtime defaults.
- Fixed production web API routing by introducing a centralized frontend API client with FastAPI route-prefix discovery.
- Replaced direct hardcoded frontend upload URLs with environment-aware API base resolution.
- Added backend `/api/meta` route metadata for deployment clients and verification tooling.
- Updated backend CORS to support explicit Vercel origins and Vercel preview deployment origins through `CORS_ORIGIN_REGEX`.
- Filled missing required documentation paths so future work has a consistent place to record fixes and observations.
- Fixed stale frontend test expectation that looked for `learn react`.
- Removed a hardcoded mobile LAN fallback from production path.

### Improved
- Improved project traceability by linking logs, changelog entries, testing reports, and presentation documents.
- Validated generated large, medium, small, scanned-style, text-heavy, image-heavy, and mixed-content PDF workflows with measurable outputs.
- Improved backend security headers, request timing logs, readiness endpoint, and upload limit configurability.
- Improved web API timeout handling and production metadata.

### Refactored
- No source-code refactor in this documentation-system setup.

### Security
- Documented that upload validation, password-protected PDF handling, and temporary workspace cleanup should be tracked during future security-relevant changes.

### Mobile
- Added mobile documentation notes for Expo, Metro, LAN networking, and runtime crash debugging.
- Verified Expo Android export into `frontend-mobile/dist-qa`.
- Added EAS preview and production build profiles.

### Backend
- Added backend architecture documentation describing FastAPI routing and PDF processing services.
- Added Render blueprint configuration and Procfile-compatible startup.

### Frontend
- Added frontend architecture documentation describing web/mobile API communication patterns.
- Verified React production build and Jest smoke test.
- Added Vercel deployment configuration and production env examples.

### Documentation
- Created the required professional documentation set for project review and historical traceability.
- Added full-system, compression, performance, mobile, frontend, and backend QA reports.
- Added deployment and production-readiness guides.

