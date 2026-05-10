# Changelog

All notable changes to this project will be documented in this file.

The format follows Keep a Changelog style. Dates use `YYYY-MM-DD`.

## [Unreleased]

### Added
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
- Updated web and backend environment examples for `REACT_APP_API_ORIGIN`, `REACT_APP_API_BASE`, and `CORS_ORIGIN_REGEX`.
- Consolidated project maintenance expectations into a formal logging policy under `changelog/README.md`.
- Updated the web frontend smoke test to assert the current PDF Toolkit app shell instead of the default Create React App placeholder.
- Changed backend runtime defaults toward production-safe behavior, including disabled reload by default and restricted CORS defaults.
- Changed web and mobile API configuration examples from LAN/local-only values to production-ready URL placeholders.

### Fixed
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
