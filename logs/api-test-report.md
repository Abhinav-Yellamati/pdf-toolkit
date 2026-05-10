# API Test Report

Date: 2026-05-11

## Current Source Test

The FastAPI app was imported from `backend.app.main:app` and tested with FastAPI TestClient.

| Check | Status |
| --- | --- |
| `/health` | 200 |
| `/docs` | 200 |
| `/openapi.json` | 200 |
| `/api/meta` | 200 |
| compress | 200 |
| merge | 200 |
| split | 200 |
| rearrange | 200 |
| pdf-to-word | 200 |
| pdf-to-image | 200 |
| image-to-pdf | 200 |
| watermark | 200 |
| protect | 200 |

## Public Render Test Before Redeploy

| Check | Observed |
| --- | --- |
| `/docs` | 404 |
| `/openapi.json` | 404 |
| `/api/pdf/compress` | 404 or connection reset |
| Response server style | Gunicorn / Flask-style 404 |

Conclusion: public Render must be redeployed with the corrected FastAPI app and start command.
