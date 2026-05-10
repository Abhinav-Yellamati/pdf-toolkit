# API Flow

## Upload Flow

```text
User selects file
  -> React Native DocumentPicker returns asset
  -> app validates extension and size
  -> service creates FormData
  -> fetch sends multipart request
  -> FastAPI validates UploadFile
  -> PDF service processes output
  -> FastAPI returns FileResponse
  -> app writes file to Expo cache
  -> user shares or saves file
```

## Why Multipart

PDFs and images are binary files. `multipart/form-data` supports file fields plus extra form fields such as quality, ranges, order, watermark text, and password.

## Mobile Difference

The mobile client sends file objects with:

```js
{ uri, name, type }
```

This is required for React Native uploads.

## Backend Request Lifecycle

1. FastAPI receives the multipart request under `/api/pdf`.
2. The route validates file type, file count, and form fields.
3. A temporary workspace is created for the request.
4. Uploads are saved to the workspace.
5. The PDF service runs in a threadpool so the API event loop is not blocked by document processing.
6. The backend returns a `FileResponse` with the processed file.
7. A background cleanup task removes temporary files after the response is sent.

## Main Endpoints

- `POST /api/pdf/compress`
- `POST /api/pdf/merge`
- `POST /api/pdf/split`
- `POST /api/pdf/rearrange`
- `POST /api/pdf/pdf-to-word`
- `POST /api/pdf/pdf-to-image`
- `POST /api/pdf/image-to-pdf`
- `POST /api/pdf/watermark`
- `POST /api/pdf/protect`
