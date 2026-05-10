# Networking Debugging

## Problem

The mobile app showed `Network request failed` in Expo Go.

## Cause

The app used `127.0.0.1`, which points to the phone itself when running in Expo Go. The backend was also bound through a loopback-only listener, so the phone could not reach it.

## Fix

- Added centralized mobile API config in `frontend-mobile/src/config/api.js`.
- Set the mobile API base to the computer LAN IP.
- Updated backend startup to bind to `0.0.0.0:8001`.
- Added clearer mobile network error messages.
- Verified all API endpoints over LAN.

## Checks

```powershell
netstat -ano | Select-String ':8001'
Invoke-WebRequest http://10.196.40.171:8001/health
```

Expected:

```text
0.0.0.0:8001 LISTENING
{"status":"healthy"}
```

## Firewall

If a physical phone still cannot connect, allow inbound TCP traffic for port `8001` from an Administrator PowerShell:

```powershell
netsh advfirewall firewall add rule name="PDF Toolkit FastAPI 8001" dir=in action=allow protocol=TCP localport=8001
```
