# Render Deployment

## Purpose

Deploy `backend` as the public FastAPI API service.

## Render Settings

- Service type: Web Service
- Runtime: Python
- Root directory: `backend`
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Health check path: `/health`

The repository also includes root-level `render.yaml` for blueprint deployment.

## Environment Variables

```text
ENVIRONMENT=production
LOG_LEVEL=INFO
ENABLE_DOCS=1
MAX_FILE_MB=100
CORS_ORIGINS=https://your-vercel-app.vercel.app,https://your-custom-domain.com
```

## Production Endpoints

- `/health`
- `/ready`
- `/docs`
- `/api/pdf/compress`
- `/api/pdf/merge`
- `/api/pdf/split`
- `/api/pdf/rearrange`
- `/api/pdf/pdf-to-word`
- `/api/pdf/pdf-to-image`
- `/api/pdf/image-to-pdf`
- `/api/pdf/watermark`
- `/api/pdf/protect`

## Verification

1. Open `https://your-render-api.onrender.com/health`.
2. Open `https://your-render-api.onrender.com/docs`.
3. Use the Swagger UI or frontend app to upload sample files.
4. Confirm response files download correctly.
5. Check Render logs for handled errors and timing lines.

