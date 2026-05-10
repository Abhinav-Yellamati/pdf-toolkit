# Web Frontend

The web frontend is a React application for desktop browser workflows.

## Responsibilities

- Render the main PDF Toolkit workspace.
- Let users select a PDF tool.
- Validate file count, extension, and required fields before submission.
- Send `multipart/form-data` requests to the FastAPI backend.
- Show progress while the backend processes the file.
- Create browser download links from returned blobs.
- Show success and error toast messages.

## Important Files

- `src/App.js`: Main application state and workflow.
- `src/config/tools.js`: Declarative tool definitions.
- `src/services/api.js`: API upload/download logic.
- `src/components/UploadPanel.js`: Upload UI.
- `src/components/ToolCard.js`: Tool selection card.
- `src/components/DownloadCard.js`: Result/download UI.
- `src/components/ToastStack.js`: Toast messages.

## Environment

Set the backend URL with:

```text
REACT_APP_API_BASE=http://127.0.0.1:8001/api/pdf
```

## Demo Talking Point

The web UI is configuration-driven. Adding a new tool generally requires a backend endpoint and a new entry in `tools.js`.
