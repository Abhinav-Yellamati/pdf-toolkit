# Backend

The backend is a FastAPI application that exposes all PDF processing operations as HTTP endpoints.

## Responsibilities

- Accept multipart uploads.
- Validate file extensions, file types, and required fields.
- Create isolated temporary workspaces.
- Run PDF processing services.
- Return generated files with `FileResponse`.
- Clean up temporary workspaces after responses are sent.

## Important Files

- `main.py`: Development entrypoint, defaults to `0.0.0.0:8001`.
- `app/main.py`: FastAPI app, CORS, health endpoints, exception handlers.
- `app/routes/pdf.py`: API route handlers.
- `app/services/pdf_service.py`: PDF algorithms.
- `app/utils/validation.py`: Upload validation.
- `app/utils/files.py`: Temporary workspace and file save helpers.

## PDF Libraries

- PyMuPDF handles compression, rendering pages to images, image-to-PDF conversion, text extraction, and watermarking.
- pypdf handles merging, splitting, rearranging, and encryption.

## Run

```powershell
cd backend
python -m pip install -r requirements.txt
python main.py
```

The backend should show:

```text
Uvicorn running on http://0.0.0.0:8001
```
