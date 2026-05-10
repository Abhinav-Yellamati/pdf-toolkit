# Production README

## Services

| Component | Platform | Directory | Build |
| --- | --- | --- | --- |
| Backend API | Render | `backend/` | `pip install -r requirements.txt` |
| Web App | Vercel | `frontend-web/` | `npm run build` |
| Mobile App | EAS | `frontend-mobile/` | `eas build` |

## Production Environment Variables

Backend:

```text
ENVIRONMENT=production
LOG_LEVEL=INFO
ENABLE_DOCS=1
MAX_FILE_MB=100
CORS_ORIGINS=https://your-vercel-app.vercel.app
```

Web:

```text
REACT_APP_API_BASE=https://your-render-api.onrender.com/api/pdf
REACT_APP_API_TIMEOUT_MS=120000
```

Mobile:

```text
EXPO_PUBLIC_API_BASE_URL=https://your-render-api.onrender.com/api/pdf
EXPO_PUBLIC_API_TIMEOUT_MS=120000
```

## Verification

1. Open backend `/health`.
2. Open backend `/docs`.
3. Open web app and run compress, merge, split, watermark, and protect flows.
4. Install mobile build and repeat upload/download checks.
