# Production Route Map

## Frontend

```text
https://pdf-toolkit-black-ten.vercel.app
```

## Backend

```text
https://pdf-toolkit-backend.onrender.com
```

## API Base

```text
https://pdf-toolkit-backend.onrender.com/api/pdf
```

## Required Backend Routes

- `GET /`
- `GET /health`
- `GET /ready`
- `GET /docs`
- `GET /openapi.json`
- `GET /api/meta`
- `POST /api/pdf/compress`
- `POST /api/pdf/merge`
- `POST /api/pdf/split`
- `POST /api/pdf/rearrange`
- `POST /api/pdf/pdf-to-word`
- `POST /api/pdf/pdf-to-image`
- `POST /api/pdf/image-to-pdf`
- `POST /api/pdf/watermark`
- `POST /api/pdf/protect`

Every `/api/pdf/*` route must also allow CORS preflight `OPTIONS`.
