# Networking Fixes Log

## Issue

Expo Go showed `Network request failed` when calling the backend.

## Root Cause

The mobile app used localhost-style URLs. On a phone, `localhost` and `127.0.0.1` refer to the phone, not the development computer.

## Fixes

- Created `frontend-mobile/src/config/api.js`.
- Added `EXPO_PUBLIC_API_BASE_URL`.
- Set the mobile API URL to `http://10.196.40.171:8001/api/pdf`.
- Updated backend entrypoint to bind to `0.0.0.0`.
- Verified health, CORS, and multipart uploads over LAN.

## Remaining Environment Note

Windows Firewall may require an Administrator rule for inbound TCP port `8001`.
