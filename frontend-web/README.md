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

Set the backend base URL with:

```text
REACT_APP_API_BASE=http://127.0.0.1:8001/api/pdf
```

If this variable is not set, the app uses the default in `src/services/api.js`.

## Important Files

- `src/App.js`
- `src/config/tools.js`
- `src/services/api.js`
- `src/components/UploadPanel.js`
- `src/components/DownloadCard.js`
- `src/components/ToolCard.js`
- `src/components/ToastStack.js`
