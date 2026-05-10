# Networking Fixes

## Problem

The mobile app could not call the FastAPI backend from a physical phone.

## Cause

`localhost` and `127.0.0.1` point to the phone itself in Expo Go, not the development computer.

## Solution

- Backend runs on `0.0.0.0:8001`.
- Mobile app uses `EXPO_PUBLIC_API_BASE_URL`.
- Current demo API URL:

```text
http://10.196.40.171:8001/api/pdf
```

## Verification

```powershell
Invoke-WebRequest http://10.196.40.171:8001/health
```

Expected:

```json
{"status":"healthy"}
```
