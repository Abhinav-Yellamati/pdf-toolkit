# Mobile Testing Report

## Scope

The Expo React Native mobile app was validated through static configuration inspection and Android export generation.

## Results

| Test | Result | Evidence |
| --- | --- | --- |
| Expo env loading | Passed | Export printed `EXPO_PUBLIC_API_BASE_URL` and timeout variables |
| Android bundle export | Passed | `dist-qa` generated with 21 files |
| Bundle size | Passed | Exported files total approximately 5.88 MB |
| API base configuration | Passed | `.env` points to `http://10.196.40.171:8001/api/pdf` |
| Physical-device upload/download | Not executed | No connected Expo Go device or `adb` available in this environment |

## Commands

```powershell
npx.cmd expo export --platform android --output-dir dist-qa
```

## Observations

- Metro bundled the Android entry successfully.
- The app can be exported for Android without JavaScript syntax or dependency errors.
- Physical mobile validation should be completed on the same Wi-Fi network using the configured LAN API URL.

## Recommended Device Checklist

- Open Expo Go on a physical Android device.
- Confirm app loads without red screen.
- Upload `test-assets/sample-pdfs/text-small.pdf`.
- Run compress, split, watermark, and password workflows.
- Confirm result sharing/download works.
- Record Expo console logs in `logs/mobile-runtime.log`.

