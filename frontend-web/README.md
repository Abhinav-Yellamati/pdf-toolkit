# PDF Toolkit Web

React web frontend for PDF Toolkit.

## Responsibilities

- Provide a browser-based PDF processing workspace.
- Validate uploads before API calls.
- Send multipart requests to the FastAPI backend.
- Show processing progress.
- Present generated files through download cards.
- Display toast feedback for success and errors.

## Setup

```powershell
npm install
```

## Run

```powershell
npm start
```

## API Configuration

For production, set the deployed backend base URL with:

```text
REACT_APP_API_BASE=https://pdf-toolkit-api-v2.onrender.com/api/pdf
```

For local development, leave `REACT_APP_API_BASE` unset and optionally set:

```text
REACT_APP_DEV_API_HOST=127.0.0.1
REACT_APP_DEV_API_PORT=8001
```

Production builds never fall back to the local development backend.

## Important Files

- `src/App.js`
- `src/config/tools.js`
- `src/services/api.js`
- `src/components/UploadPanel.js`
- `src/components/DownloadCard.js`
- `src/components/ToolCard.js`
- `src/components/ToastStack.js`
