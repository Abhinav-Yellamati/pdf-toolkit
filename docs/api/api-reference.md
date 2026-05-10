# API Reference

## Base URLs

Local backend:

```text
http://127.0.0.1:8001/api/pdf
```

LAN backend for mobile:

```text
http://10.196.40.171:8001/api/pdf
```

## Health

```http
GET /health
```

Returns:

```json
{"status":"healthy"}
```

## PDF Tool Endpoints

All tool endpoints use `multipart/form-data` and return a downloadable file.

| Feature | Method | Endpoint | File fields | Extra fields | Output |
| --- | --- | --- | --- | --- | --- |
| Compress PDF | POST | `/compress` | `file` | `quality` | PDF |
| Merge PDFs | POST | `/merge` | `files` | none | PDF |
| Split PDF | POST | `/split` | `file` | `ranges` optional | ZIP |
| Rearrange Pages | POST | `/rearrange` | `file` | `order` required | PDF |
| PDF to Word | POST | `/pdf-to-word` | `file` | none | DOCX |
| PDF to Image | POST | `/pdf-to-image` | `file` | `dpi` | ZIP |
| Image to PDF | POST | `/image-to-pdf` | `files` | none | PDF |
| Add Watermark | POST | `/watermark` | `file` | `text`, `opacity` | PDF |
| Protect PDF | POST | `/protect` | `file` | `password` | PDF |

## Error Format

Errors are returned as JSON:

```json
{"detail":"Human readable error message"}
```

## Mobile Upload Notes

The mobile app sends React Native file payloads in this shape:

```js
{
  uri: file.uri,
  name: file.name,
  type: file.mimeType
}
```

The app does not manually set `Content-Type` for multipart uploads. React Native sets the boundary automatically.
