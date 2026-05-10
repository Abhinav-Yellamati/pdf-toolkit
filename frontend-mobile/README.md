# PDF Toolkit Mobile

Expo React Native mobile app for PDF Toolkit.

## Responsibilities

- Pick PDFs and images from a phone.
- Upload files to the FastAPI backend.
- Show progress and toast feedback.
- Save returned files to Expo cache.
- Share or save generated files through native sharing.

## Setup

```powershell
npm install
```

## Run

```powershell
npx expo start --host lan
```

## API Configuration

The app reads:

```text
EXPO_PUBLIC_API_BASE_URL=http://10.196.40.171:8001/api/pdf
```

For a physical phone, this must use the computer LAN IP, not `localhost` or `127.0.0.1`.

## Important Files

- `App.js`
- `src/config/api.js`
- `src/config/tools.js`
- `src/services/api.js`
- `src/components/UploadBox.js`
- `src/components/ToolCard.js`
- `src/components/Toast.js`
