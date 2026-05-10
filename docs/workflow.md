# Workflow Explanation

## User Workflow

1. User opens the web or mobile app.
2. User selects a PDF tool.
3. App updates required inputs for the selected tool.
4. User selects files.
5. App validates file type, count, and size.
6. User submits the job.
7. App sends files and fields to FastAPI as `multipart/form-data`.
8. Backend validates the request.
9. Backend processes the file.
10. Backend returns PDF, DOCX, or ZIP output.
11. Web shows a download card; mobile opens native share/save.

## Backend Workflow

1. Route receives upload.
2. Validation rejects unsupported inputs early.
3. Temporary workspace is created.
4. Uploaded files are saved.
5. PDF service function runs in a threadpool.
6. Output file is returned as `FileResponse`.
7. Temporary workspace is cleaned up by a background task.
