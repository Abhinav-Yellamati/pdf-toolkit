# Architecture Explanation

The system has three main parts:

- The web frontend provides a browser interface for selecting tools and uploading files.
- The mobile frontend provides the same toolkit experience through Expo React Native.
- The backend exposes FastAPI endpoints under `/api/pdf` and performs the actual PDF processing.

The user selects a PDF operation, the client sends files and form data to the backend, the backend validates the request, runs the PDF service, and returns a downloadable result file.

This separation keeps the frontend simple and keeps heavy document processing on the server, where libraries such as PyMuPDF and pypdf can run reliably.

