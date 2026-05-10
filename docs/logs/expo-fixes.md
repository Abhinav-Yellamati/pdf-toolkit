# Expo Fixes Log

## Issues

- PowerShell blocked `npx.ps1`.
- Expo web mode required web dependencies.
- Expo Go needed a native-compatible mobile bundle.
- Physical phone networking required LAN URLs.

## Fixes

- Used `npx.cmd` instead of `npx.ps1`.
- Removed web-only dependencies from the mobile app after mobile testing.
- Added `expo-constants` for runtime host awareness.
- Verified the Android bundle through Metro.
- Started Expo in LAN mode for phone testing.
