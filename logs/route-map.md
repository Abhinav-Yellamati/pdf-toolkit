# Backend Route Map

Expected public backend origin:

```text
https://pdf-toolkit-backend.onrender.com
```

Expected public API base:

```text
https://pdf-toolkit-backend.onrender.com/api/pdf
```

Required routes:

| Route | Method | Purpose |
| --- | --- | --- |
| `/` | GET | API root status |
| `/health` | GET | Render health check |
| `/ready` | GET | Readiness and environment status |
| `/docs` | GET | FastAPI Swagger UI |
| `/openapi.json` | GET | OpenAPI route map |
| `/api/meta` | GET | Lightweight route metadata |
| `/api/pdf/compress` | POST, OPTIONS | Compress PDF |
| `/api/pdf/merge` | POST, OPTIONS | Merge PDFs |
| `/api/pdf/split` | POST, OPTIONS | Split PDF |
| `/api/pdf/rearrange` | POST, OPTIONS | Rearrange PDF |
| `/api/pdf/pdf-to-word` | POST, OPTIONS | Convert PDF to DOCX |
| `/api/pdf/pdf-to-image` | POST, OPTIONS | Convert PDF to PNG ZIP |
| `/api/pdf/image-to-pdf` | POST, OPTIONS | Convert images to PDF |
| `/api/pdf/watermark` | POST, OPTIONS | Add watermark |
| `/api/pdf/protect` | POST, OPTIONS | Password protect PDF |

Startup validation now requires every route above. If any of these paths is missing when the FastAPI process starts, the app raises `RuntimeError` and Render logs will show the missing route list.
