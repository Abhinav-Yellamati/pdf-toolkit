# Mobile Deployment

## Purpose

Prepare the Expo React Native app for production builds using EAS.

## Files Added

- `frontend-mobile/eas.json`
- `frontend-mobile/.env.production.example`
- `frontend-mobile/assets/icon.png`
- `frontend-mobile/assets/adaptive-icon.png`
- `frontend-mobile/assets/splash.png`

## Environment Variables

```text
EXPO_PUBLIC_API_BASE_URL=https://your-render-api.onrender.com/api/pdf
EXPO_PUBLIC_API_TIMEOUT_MS=120000
```

## Build Commands

Preview APK:

```powershell
cd frontend-mobile
eas build --platform android --profile preview
```

Production Android App Bundle:

```powershell
cd frontend-mobile
eas build --platform android --profile production
```

Local export verification:

```powershell
npx.cmd expo export --platform android --output-dir dist-qa
```

## Physical Device Verification

1. Install the preview APK.
2. Open the app on a real Android device.
3. Run compress, merge, split, watermark, and protect workflows.
4. Confirm file sharing/download works.
5. Confirm API requests go to the Render URL, not a LAN IP.

