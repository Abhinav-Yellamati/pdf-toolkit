# Backend Architecture

The backend is a FastAPI application in `backend/app`.

## Entry Point

`backend/app/main.py` creates the FastAPI app, configures CORS, defines health endpoints, installs exception handlers, and mounts the PDF router at `/api/pdf`.

## Routing Layer

`backend/app/routes/pdf.py` contains one route per PDF tool. Each route validates uploaded files, creates a temporary workspace, saves uploads, calls a service function, and returns a `FileResponse`.

## Service Layer

`backend/app/services/pdf_service.py` contains the PDF processing implementation. It uses PyMuPDF and pypdf depending on the operation.

## Utilities

`backend/app/utils/files.py` handles file saving, workspace creation, and cleanup. `backend/app/utils/validation.py` validates upload types and request constraints.

## Error Handling

Expected validation failures use `HTTPException`. Unexpected exceptions are logged and converted into a generic 500 response.

