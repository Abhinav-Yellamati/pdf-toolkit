# Production Overview

PDF Toolkit is prepared for a split production deployment:

- React web frontend on Vercel.
- FastAPI backend on Render.
- Expo mobile app built with EAS.

Production URLs must be connected through environment variables:

- Web: `REACT_APP_API_BASE=https://your-render-api.onrender.com/api/pdf`
- Backend: `CORS_ORIGINS=https://your-vercel-app.vercel.app,https://your-custom-domain.com`
- Mobile: `EXPO_PUBLIC_API_BASE_URL=https://your-render-api.onrender.com/api/pdf`

The repository includes deployment configuration but live deployment still requires authenticated Vercel, Render, and Expo accounts.
