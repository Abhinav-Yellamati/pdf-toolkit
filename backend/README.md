# PDF Toolkit Backend

FastAPI backend for the PDF Toolkit project.

## Responsibilities

- Accept PDF and image uploads.
- Validate file types and form fields.
- Process documents with PyMuPDF and pypdf.
- Return generated files as downloads.
- Serve both web and mobile clients.

## Setup

```powershell
python -m pip install -r requirements.txt
```

## Run

```powershell
python main.py
```

Default host and port:

```text
0.0.0.0:8001
```

## Health Check

```powershell
Invoke-WebRequest http://127.0.0.1:8001/health
```

## API Routes

All PDF routes are under:

```text
/api/pdf
```

See `docs/api/api-reference.md` for the full API contract.
