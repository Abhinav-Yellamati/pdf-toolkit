# Public User Testing

## Public URLs

Frontend:

```text
https://pdf-toolkit-black-ten.vercel.app
```

Backend:

```text
https://pdf-toolkit-api.onrender.com
```

API base:

```text
https://pdf-toolkit-api.onrender.com/api/pdf
```

## Tests To Run After Render Redeploy

1. Open `/health`.
2. Open `/docs`.
3. Open `/openapi.json`.
4. Open the Vercel website from a different network.
5. Upload a PDF to Compress PDF.
6. Upload two PDFs to Merge PDFs.
7. Run Split PDF with range `1`.
8. Run Rearrange Pages with order `1`.
9. Run PDF to Word.
10. Run PDF to Image.
11. Upload an image to Image to PDF.
12. Run Watermark.
13. Run Protect PDF.

## Expected Result

- Browser console should show API requests to `https://pdf-toolkit-api.onrender.com/api/pdf/...`.
- No request should go to `localhost`.
- OPTIONS preflight should succeed.
- POST upload should return 200.
- Browser should receive a downloadable PDF, DOCX, or ZIP.

## Current Status

Current source passes all backend route tests. Public Render must be redeployed before public users can pass the same tests.

## Verification Commands

After redeploy:

```powershell
$env:RENDER_API_BASE="https://pdf-toolkit-api.onrender.com/api/pdf"
powershell -ExecutionPolicy Bypass -File scripts\verify-deployment.ps1
```

