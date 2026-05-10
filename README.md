# PDF Toolkit

PDF Toolkit is a full-stack document processing project with a React web app, an Expo React Native mobile app, and a FastAPI backend. It provides production-style PDF workflows for compression, merging, splitting, page rearrangement, conversion, watermarking, and password protection.

## Project Structure

```text
backend/           FastAPI application and PDF processing services
frontend-web/      React web interface
frontend-mobile/   Expo React Native mobile interface
shared/            Shared API contract notes
docs/              Presentation, architecture, debugging, and viva documentation
```

## Technology Stack

- React for the browser UI.
- Expo React Native for the mobile app.
- FastAPI for typed, async HTTP APIs.
- PyMuPDF for PDF rendering, compression, image extraction, image-to-PDF, and watermarking.
- pypdf for merge, split, rearrange, and password protection.

## Core Features

- Compress PDF
- Merge PDFs
- Split PDF
- Rearrange pages
- PDF to Word
- PDF to Image
- Image to PDF
- Add watermark
- Protect PDF with password

## Run Backend

```powershell
cd backend
python -m pip install -r requirements.txt
python main.py
```

The backend defaults to `0.0.0.0:8001` for LAN access.

## Run Web

```powershell
cd frontend-web
npm install
npm start
```

Set `REACT_APP_API_BASE` if the backend URL is different.

## Run Mobile

```powershell
cd frontend-mobile
npm install
npx expo start --host lan
```

The mobile app reads `EXPO_PUBLIC_API_BASE_URL` from `.env`. For a physical phone, use the computer LAN IP, for example:

```text
EXPO_PUBLIC_API_BASE_URL=http://10.196.40.171:8001/api/pdf
```

## Documentation

Start with [docs/README.md](docs/README.md). Presentation and viva files are included under `docs/`.

## Production Deployment

The project is prepared for production deployment:

- Backend API: Render using `render.yaml` or `backend` web-service settings.
- Web app: Vercel using `frontend-web/vercel.json`.
- Mobile app: EAS Build using `frontend-mobile/eas.json`.

Deployment guides are available in:

- `docs/deployment/render-deployment.md`
- `docs/deployment/vercel-deployment.md`
- `docs/deployment/mobile-deployment.md`
- `docs/deployment/production-checklist.md`

Set production API URLs before deploying:

```text
REACT_APP_API_BASE=https://your-render-api.onrender.com/api/pdf
EXPO_PUBLIC_API_BASE_URL=https://your-render-api.onrender.com/api/pdf
CORS_ORIGINS=https://your-vercel-app.vercel.app
```
