# Architecture Overview

PDF Toolkit uses a three-client-layer architecture:

```text
React Web App       Expo Mobile App
      \                  /
       \                /
        FastAPI Backend
              |
       PDF Processing Layer
              |
    Temporary files and outputs
```

## Main Components

- `frontend-web`: Browser-based React interface for desktop workflows.
- `frontend-mobile`: Expo React Native app for physical phone workflows.
- `backend`: FastAPI service that validates uploads, calls PDF processors, and returns downloadable files.
- `shared`: Shared notes and API contract documentation.
- `docs`: Presentation, viva, debugging, and architecture documentation.

## Data Flow

1. User selects a tool in web or mobile.
2. UI validates files and required fields.
3. Client sends `multipart/form-data` to FastAPI.
4. Backend validates file type, size, and request fields.
5. Backend creates a temporary workspace.
6. PDF service processes the document with PyMuPDF or pypdf.
7. Backend returns a generated file as `FileResponse`.
8. Client presents a download/share result card.

## Design Goals

- Keep API behavior shared across web and mobile.
- Keep PDF processing isolated in service functions.
- Use temporary workspaces so generated files can be cleaned up.
- Keep each tool's configuration declarative in frontend tool config files.
