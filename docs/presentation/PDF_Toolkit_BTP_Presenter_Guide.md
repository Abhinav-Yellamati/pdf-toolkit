# PDF Toolkit BTP Presenter Guide

## 15-Minute Delivery Plan

- 0:00-1:00 Title and introduction
- 1:00-3:00 Problem, objectives, and features
- 3:00-6:00 Technology stack and system architecture
- 6:00-9:30 Frontend, backend, routing, CORS, and API communication
- 9:30-12:00 Deployment architecture and debugging story
- 12:00-14:00 Results, learning, future scope, and demo workflow
- 14:00-15:00 Conclusion and transition to viva questions

## Slide-Wise Speaker Notes

### 1. PDF Toolkit
Good morning respected faculty members. My BTP is PDF Toolkit, a web-based platform for common PDF operations. I will cover the problem, implementation, deployment, debugging journey, results, and future scope.

### 2. Introduction
Start by explaining that PDF operations are common in academic and office work. The project combines a user-friendly interface with a backend that performs the heavier PDF processing reliably.

### 3. Problem Statement
Explain that the problem is not only editing PDFs, but building a complete platform where upload, processing, download, API routing, validation, deployment and verification all work together.

### 4. Project Objectives
Mention measurable goals: working tools, documented APIs, public deployment, production environment variables, and verification scripts to prove the service is healthy after deployment.

### 5. Features Implemented
Briefly describe each feature category. Keep the pace fast here because detailed implementation appears later in backend and API slides.

### 6. Technology Stack
Explain why these technologies were selected: React for reusable UI, FastAPI for typed APIs and automatic docs, PyMuPDF/pypdf for PDF processing, Vercel/Render for public deployment.

### 7. System Architecture
Walk left to right: browser UI, REST call, FastAPI router, processing service, file response. Emphasize that heavy processing stays on the server.

### 8. Frontend Design
Explain that the frontend is intentionally simple for users: select a tool, upload a file, submit, and download the result. Environment variables avoid hardcoding localhost in production.

### 9. Backend Design
Explain FastAPI routing clearly. The main app mounts the PDF router with prefix /api/pdf, so /compress becomes /api/pdf/compress. Uploaded files are validated, saved temporarily, processed, returned, and then cleaned.

### 10. Deployment Architecture
Explain that frontend and backend are separate deployments. The browser loads React from Vercel, then calls the Render API over HTTPS. CORS is required because these are different origins.

### 11. Major Obstacles Faced
Describe obstacles factually. The most important learning was that deployment platforms only run what is configured, so build/start commands, root directory and app import path must match the real backend.

### 12. Debugging & Solutions
Explain the Node/Express conflict: Render can detect Node if package files exist or if the wrong root is selected. Then /health may hit an Express/default service or no matching route. The fix was to remove the conflicting backend path and explicitly configure Python FastAPI with Uvicorn.

### 13. Results Obtained
Mention practical outcomes: public web interface, deployed API, functioning PDF outputs, and smoke tests that validate production after deployment.

### 14. What I Learned
Use this slide to show engineering maturity: not just building features, but diagnosing platform errors, validating routes, and separating frontend/backend responsibilities.

### 15. Future Improvements
Frame these as realistic next steps. Explain that current implementation is suitable for BTP scope, while larger-scale production would need queues, storage, authentication, and monitoring.

### 16. Conclusion
Conclude that the project satisfies both functionality and engineering objectives: usable tools, clean architecture, deployed services, API documentation and production verification.

### 17. Demo Workflow
During the demo, keep one reliable sample PDF ready. Show one fast feature first, such as compress or watermark, then show Swagger docs if time allows.

### 18. Live Demo Screenshots
Replace the placeholders with actual screenshots from your deployed frontend and Render backend before final submission. Use this slide if internet is slow during the live demo.

### 19. API Documentation
Explain that FastAPI automatically generates /docs from route definitions and type hints. This makes backend validation transparent and helps test endpoints without manually writing a client.

### 20. Thank You
Thank the panel and invite questions. Be ready to discuss CORS, deployment debugging, FastAPI routing, file uploads, and why backend processing was selected.

## Deployment Debugging Explanation

The main deployment issue was runtime mismatch. The project needed a Python FastAPI backend, but accidental Node/Express backend assumptions caused routes like `/health` and `/docs` to fail. `Cannot GET /health` means a server responded, but the running app did not define that route.

The fix was to make the backend unambiguous: Render uses `rootDir: backend`, installs `requirements.txt`, and starts `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`. The FastAPI app also defines `/health`, `/ready`, `/api/meta`, `/docs`, and validates expected routes during startup.

Production validation then checks the Render origin, Swagger docs, OpenAPI JSON, metadata, and every PDF endpoint using sample files. This proves both routing and real document processing work after deployment.

## Viva Questions and Strong Answers

**Q: Why did you use FastAPI?**

A: FastAPI gives typed request handling, automatic Swagger documentation, clean routing with APIRouter, file upload support through UploadFile, and easy deployment with Uvicorn.

**Q: How does React communicate with FastAPI?**

A: React creates multipart/form-data requests using the production API base URL. The request goes to Render, FastAPI validates uploads, processes the PDF, and returns a FileResponse that the browser downloads.

**Q: What is CORS and why was it needed?**

A: CORS is the browser security rule that controls whether one origin can call another. Since Vercel and Render have different domains, FastAPI must allow the Vercel origin and expose download headers like Content-Disposition.

**Q: Explain FastAPI routing in your project.**

A: The main app creates a FastAPI instance and includes the PDF router with prefix /api/pdf. Therefore router paths like /compress become public routes like /api/pdf/compress.

**Q: Why did the Node/Express conflict happen?**

A: Earlier deployment files or assumptions pointed the platform toward a Node/Express backend. That caused endpoints such as /health or /docs to be unavailable because the running service was not the intended FastAPI app.

**Q: How was the Express/Node issue fixed?**

A: The backend was standardized as Python FastAPI only. Render was configured with rootDir backend, Python build command, and Uvicorn startup command targeting app.main:app.

**Q: What does Cannot GET /health mean?**

A: It usually means the request reached a server, but that server did not have a GET route for /health. In this project, that indicated the wrong runtime/app or missing route registration.

**Q: How did you verify production deployment?**

A: I added health, ready, metadata, docs and OpenAPI checks, plus smoke tests that call each PDF endpoint with sample files and write a verification log.

**Q: Why not process PDFs only in React?**

A: Browser-only processing is limited for heavy PDFs and complex libraries. Backend processing gives better library support, centralized validation, and one implementation for all clients.

**Q: How are temporary files handled?**

A: Each request gets a temporary workspace. The processed output is returned as a download, and background cleanup removes the workspace after the response.

## Confident Delivery Tips

- Keep the architecture explanation left-to-right: React, REST, FastAPI, PDF service, download.
- When discussing bugs, state symptom, root cause, fix, and verification.
- Do not memorize code. Memorize the flow and the reason behind each design choice.
- Keep one sample PDF ready and demo one fast operation first.