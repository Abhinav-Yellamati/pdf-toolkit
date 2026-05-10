# Domain And HTTPS

## Frontend Domain

Vercel provides HTTPS automatically for both the generated Vercel URL and custom domains. Add custom domains in Vercel Project Settings -> Domains.

## Backend HTTPS

Render provides HTTPS automatically for `onrender.com` service URLs. If using a custom backend domain, configure it in Render and update DNS according to Render instructions.

## CORS Update

Every public frontend origin must be listed in the backend environment variable:

```text
CORS_ORIGINS=https://your-vercel-app.vercel.app,https://your-custom-domain.com
```

## Mobile URLs

Mobile builds must point directly to the HTTPS backend API:

```text
EXPO_PUBLIC_API_BASE_URL=https://your-render-api.onrender.com/api/pdf
```

