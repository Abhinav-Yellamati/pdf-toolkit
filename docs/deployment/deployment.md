# Deployment Notes

## Local Demo Deployment

Start the backend:

```powershell
cd backend
python main.py
```

Start the web frontend:

```powershell
cd frontend-web
npm start
```

Start the mobile app:

```powershell
cd frontend-mobile
npx expo start --host lan
```

## LAN Demo

Use the computer LAN IP in the mobile `.env` file:

```text
EXPO_PUBLIC_API_BASE_URL=http://10.196.40.171:8001/api/pdf
```

The phone and computer must be on the same network.

## Production Direction

- Deploy FastAPI behind HTTPS.
- Store generated files in temporary object storage if scaling beyond one server.
- Add authentication if the toolkit becomes user-specific.
- Add request size limits and rate limiting.
- Move environment values to deployment-specific config.
