# Mobile Crash Debugging

## Symptom

Expo Go showed the blue `Something went wrong` screen during runtime startup.

## What Was Checked

- Metro server logs.
- Expo startup logs.
- Android bundle generation.
- Mobile API configuration.
- Imports added during networking fixes.
- Runtime paths that execute during module import.

## Root Cause Class

The crash happened after environment/API configuration changes. Metro could build the bundle, which means the issue was not a syntax error. The most likely startup-risk area was direct access to `process.env` and runtime configuration values during module evaluation.

## Fixes Implemented

- Hardened `frontend-mobile/src/config/api.js` with safe environment access.
- Added fallback API values if environment variables are missing.
- Added startup diagnostics with resolved API base URL.
- Added `ErrorBoundary` to prevent the app from falling straight to the Expo blue crash screen for render errors.
- Added logging for upload, API request, runtime, and share failures.
- Wrapped Expo document picker with error handling.
- Guarded selected tool resolution with fallback to the first configured tool.

## Debugging Methodology

1. Confirm Metro can bundle.
2. Check Expo logs for stack traces.
3. Identify modules imported at startup.
4. Harden any import-time code.
5. Add runtime boundary and logs.
6. Restart Expo with cache clear.
7. Test on physical phone.

## Expected Startup Logs

The app should log:

```text
[PDFToolkit:config] API configuration resolved
[PDFToolkit:startup] Mobile app mounted
[PDFToolkit:api] Checking backend health
```
