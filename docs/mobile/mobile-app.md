# Mobile App

The mobile app is built with Expo React Native and targets Expo Go for development and demo testing.

## Responsibilities

- Provide mobile access to the same PDF Toolkit API.
- Use `expo-document-picker` for selecting PDFs and images.
- Upload files using React Native `FormData`.
- Save returned files to Expo cache with `expo-file-system`.
- Share or save processed files with `expo-sharing`.
- Use LAN-aware API configuration for physical phone testing.

## Important Files

- `App.js`: Main mobile screen, tool switching, progress, and toasts.
- `src/config/api.js`: Central API URL resolution.
- `src/config/tools.js`: Mobile tool definitions.
- `src/services/api.js`: Upload, download, timeout, and sharing logic.
- `src/components/UploadBox.js`: Mobile upload panel.
- `src/components/ToolCard.js`: Mobile tool cards.
- `src/components/Toast.js`: Mobile toast message.

## Networking

Physical phones cannot use `127.0.0.1` to reach a computer backend. The mobile app uses:

```text
EXPO_PUBLIC_API_BASE_URL=http://10.196.40.171:8001/api/pdf
```

If the Expo LAN host is available, the app can also infer the computer IP from Expo's host URI.

## Performance Notes

- PDF processing stays on the backend, keeping the phone lightweight.
- The mobile app only handles upload, progress state, cached result writing, and native sharing.
- Timeouts produce actionable network messages instead of generic failures.
