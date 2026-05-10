import logging
import os
import time

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routes.pdf import router as pdf_router

logger = logging.getLogger("pdf_toolkit")
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

cors_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000",
    ).split(",")
    if origin.strip()
]
cors_origin_regex = os.getenv(
    "CORS_ORIGIN_REGEX",
    r"https://.*\.vercel\.app",
)
allow_all_origins = "*" in cors_origins
environment = os.getenv("ENVIRONMENT", "development").lower()
docs_enabled = os.getenv("ENABLE_DOCS", "1") == "1"

app = FastAPI(
    title="PDF Toolkit API",
    description="Production-ready PDF processing APIs powered by FastAPI, PyMuPDF and pypdf.",
    version="2.0.0",
    docs_url="/docs" if docs_enabled else None,
    redoc_url="/redoc" if docs_enabled else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if allow_all_origins else cors_origins,
    allow_origin_regex=None if allow_all_origins else cors_origin_regex,
    allow_credentials=not allow_all_origins,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition", "Content-Length", "Content-Type"],
)


@app.middleware("http")
async def production_headers_and_logging(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start) * 1000
    logger.info("%s %s -> %s %.2fms", request.method, request.url.path, response.status_code, elapsed_ms)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    if environment == "production":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled API error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Something went wrong while processing the document."},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.info("Handled API error on %s %s: %s", request.method, request.url.path, exc.detail)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.get("/")
async def root():
    return {"status": "ok", "message": "PDF Toolkit API is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/ready")
async def ready():
    return {
        "status": "ready",
        "environment": environment,
        "cors": "wildcard" if allow_all_origins else "restricted",
    }


@app.get("/api/meta")
async def api_meta():
    return {
        "status": "ok",
        "pdfPrefix": "/api/pdf",
        "healthPath": "/health",
        "openApiPath": "/openapi.json",
        "tools": [
            "/compress",
            "/merge",
            "/split",
            "/rearrange",
            "/pdf-to-word",
            "/pdf-to-image",
            "/image-to-pdf",
            "/watermark",
            "/protect",
        ],
    }


app.include_router(pdf_router, prefix="/api/pdf", tags=["PDF Tools"])
