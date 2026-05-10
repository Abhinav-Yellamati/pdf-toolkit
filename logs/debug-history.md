# Debug History

## Mobile Startup Crash

Symptom: Expo Go displayed the blue `Something went wrong` screen after networking and environment configuration changes.

Investigation:

- Metro logs showed the JavaScript bundle was produced successfully.
- No device-side stack trace was present in the captured Metro log.
- The likely crash zone was startup module evaluation, especially API config imports.

Fixes:

- Hardened `src/config/api.js` against missing `process.env`.
- Added safe API fallback values.
- Added `ErrorBoundary` around the mobile app root.
- Added startup diagnostics and API request logging.
- Added upload, runtime, and sharing error logs.

Verification Plan:

- Run clean Android bundle.
- Restart Expo with cache clear.
- Open in Expo Go.
- Verify backend health and compress upload.

Verification Completed:

- Clean Android bundle: passed.
- Fresh Expo LAN server: `http://localhost:8087`.
- Android bundle served by Metro: HTTP 200.
- Backend health over LAN: HTTP 200.
- Compress upload over LAN: HTTP 200.

Physical Device Note:

- This environment does not have `adb`, so direct device log extraction is unavailable.
- Expo logs should now print startup diagnostics and component stack traces when the app is opened in Expo Go.

## 2026-05-10 11:34 IST - Documentation Traceability Baseline

- Affected files: `logs/`, `docs/`, `CHANGELOG.md`, `changelog/`, `history/`
- Issue description: Required complete debugging and engineering history system was incomplete.
- Root cause: Existing debugging notes were useful but did not include every required log, changelog, testing, history, and presentation file.
- Fix implemented: Added the missing append-only documentation files and created a baseline session entry.
- Result after fix: Future issues can be tracked chronologically with symptoms, investigation, root cause, solution, validation, and lessons learned.
- Commands executed: `Get-ChildItem`, `rg --files`, `Get-Content`, `New-Item`
- Important observations: Existing logs already captured Expo, LAN, API, and CORS stabilization work from 2026-05-10.

## 2026-05-10 12:05 IST - QA Runner And Frontend Test Stabilization

- Affected files: `test-assets/reports/run_full_qa.py`, `frontend-web/src/App.test.js`
- Issue description: QA automation initially failed during asset generation and frontend Jest testing.
- Root cause: PyMuPDF Pixmap constructor usage differed in the installed Python version; frontend test still expected the default Create React App `learn react` text; repeated image streams did not produce a true 50 MB PDF.
- Fix implemented: Updated the Pixmap constructor to use `fitz.IRect`, changed the frontend smoke test to assert current PDF Toolkit UI text, and generated unique large page images for the 56.54 MB PDF.
- Result after fix: Full backend QA runner passed, frontend Jest test passed, web build passed, and Expo Android export passed.
- Commands executed: `python .\test-assets\reports\run_full_qa.py`; `npm.cmd test -- --watchAll=false`; `npm.cmd run build`; `npx.cmd expo export --platform android --output-dir dist-qa`
- Important observations: Image watermarking is unsupported by the current API and should be handled as future scope unless the product requirements change.
