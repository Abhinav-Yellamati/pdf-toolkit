# Architecture Diagram Explanation

Use this explanation when presenting the architecture diagram.

```text
+------------------+       multipart/form-data       +------------------+
| React Web App    | ------------------------------> | FastAPI Backend  |
+------------------+                                 +------------------+
                                                           |
+------------------+       multipart/form-data             |
| Expo Mobile App  | ------------------------------>       |
+------------------+                                      v
                                                   +------------------+
                                                   | PDF Services     |
                                                   | PyMuPDF + pypdf  |
                                                   +------------------+
                                                           |
                                                           v
                                                   +------------------+
                                                   | FileResponse     |
                                                   | PDF/DOCX/ZIP     |
                                                   +------------------+
```

## Explanation

Both the web and mobile apps are thin clients. They collect files, validate basic inputs, show progress, and call the same backend endpoints. The backend owns the processing logic. This keeps the business logic consistent and avoids duplicating PDF algorithms across clients.

## Why This Architecture Works

- Web and mobile stay consistent because they use the same API contract.
- FastAPI keeps endpoint definitions clear and testable.
- PyMuPDF and pypdf are isolated behind service functions.
- Temporary backend workspaces prevent long-term file buildup.
