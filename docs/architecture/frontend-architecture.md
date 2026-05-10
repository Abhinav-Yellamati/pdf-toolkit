# Frontend Architecture

The web frontend lives in `frontend-web`.

The web app presents available PDF tools, collects files and form values, sends multipart requests to the FastAPI backend, and downloads the returned file.

The API base URL can be configured with `REACT_APP_API_BASE`. During local development, it should point to the backend `/api/pdf` prefix.

Important frontend responsibilities:

- Present clear tool options.
- Validate obvious input before upload where possible.
- Send correct multipart field names.
- Show request progress and errors.
- Download PDF, zip, image, or Word results returned by the backend.

