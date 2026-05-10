# Development Log

## Expo Runtime Stabilization

- Investigated Expo blue-screen crash after networking changes.
- Confirmed Metro could bundle the Android app.
- Hardened environment/API configuration.
- Added root error boundary.
- Added startup diagnostics.
- Added API request logging.
- Added upload and share error logging.

## Networking Stabilization

- Replaced phone-invalid localhost assumptions with LAN API URL.
- Backend configured for `0.0.0.0:8001`.
- Verified health, CORS, and multipart upload behavior over LAN.

## Documentation

- Added crash debugging notes.
- Added networking fix notes.
- Added mobile architecture and API flow explanations.
- Added viva common issues and solutions.
