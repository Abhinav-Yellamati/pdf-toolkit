from fastapi import HTTPException, UploadFile

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_FILES = 20


def validate_pdf_file(file: UploadFile) -> None:
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")


def validate_pdf_files(files: list[UploadFile], min_count: int = 1) -> None:
    if len(files) < min_count:
        raise HTTPException(status_code=400, detail=f"Upload at least {min_count} PDF files.")
    if len(files) > MAX_FILES:
        raise HTTPException(status_code=400, detail=f"Upload up to {MAX_FILES} files at once.")
    for file in files:
        validate_pdf_file(file)


def validate_image_files(files: list[UploadFile]) -> None:
    if not files:
        raise HTTPException(status_code=400, detail="Upload at least one image.")
    if len(files) > MAX_FILES:
        raise HTTPException(status_code=400, detail=f"Upload up to {MAX_FILES} files at once.")
    for file in files:
        if file.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(status_code=400, detail="Only JPG, PNG and WebP images are supported.")

