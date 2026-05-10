# PDF Toolkit API Contract

Base URL: `http://127.0.0.1:8001/api/pdf`

Web override: `REACT_APP_API_BASE`

Mobile override: `EXPO_PUBLIC_API_BASE_URL`

All tool endpoints accept `multipart/form-data` and return a downloadable file.

| Tool | Endpoint | File fields | Extra fields | Output |
| --- | --- | --- | --- | --- |
| Compress PDF | `/compress` | `file` | `quality` | PDF |
| Merge PDFs | `/merge` | `files[]` | - | PDF |
| Split PDF | `/split` | `file` | `ranges` optional | ZIP |
| Rearrange pages | `/rearrange` | `file` | `order` required | PDF |
| PDF to Word | `/pdf-to-word` | `file` | - | DOCX |
| PDF to Image | `/pdf-to-image` | `file` | `dpi` | ZIP |
| Image to PDF | `/image-to-pdf` | `files[]` | - | PDF |
| Watermark | `/watermark` | `file` | `text`, `opacity` | PDF |
| Protect PDF | `/protect` | `file` | `password` | PDF |
