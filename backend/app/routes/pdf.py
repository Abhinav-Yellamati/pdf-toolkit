from typing import Callable, List

from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
from starlette.concurrency import run_in_threadpool

from ..services.pdf_service import (
    add_watermark,
    compress_pdf,
    convert_images_to_pdf,
    convert_pdf_to_images,
    convert_pdf_to_word,
    merge_pdfs,
    protect_pdf,
    rearrange_pdf,
    split_pdf,
)
from ..utils.files import cleanup_paths, prepare_workspace, save_upload, save_uploads
from ..utils.validation import validate_image_files, validate_pdf_file, validate_pdf_files

router = APIRouter()


def download_response(path, filename: str, media_type: str, cleanup):
    return FileResponse(
        path,
        filename=filename,
        media_type=media_type,
        background=BackgroundTask(cleanup_paths, cleanup),
    )


async def run_pdf_job(workspace, processor: Callable):
    try:
        return await run_in_threadpool(processor)
    except Exception:
        cleanup_paths([workspace])
        raise


async def save_upload_or_cleanup(workspace, file: UploadFile, path):
    try:
        return await save_upload(file, path)
    except Exception:
        cleanup_paths([workspace])
        raise


async def save_uploads_or_cleanup(workspace, files: List[UploadFile]):
    try:
        return await save_uploads(files, workspace)
    except Exception:
        cleanup_paths([workspace])
        raise


@router.post("/compress")
async def compress(file: UploadFile = File(...), quality: int = Form(55)):
    validate_pdf_file(file)
    workspace = prepare_workspace()
    input_path = await save_upload_or_cleanup(workspace, file, workspace / "input.pdf")
    output_path = workspace / "compressed.pdf"
    await run_pdf_job(workspace, lambda: compress_pdf(input_path, output_path, quality=quality))
    return download_response(output_path, "compressed.pdf", "application/pdf", [workspace])


@router.post("/merge")
async def merge(files: List[UploadFile] = File(...)):
    validate_pdf_files(files, min_count=2)
    workspace = prepare_workspace()
    input_paths = await save_uploads_or_cleanup(workspace, files)
    output_path = workspace / "merged.pdf"
    await run_pdf_job(workspace, lambda: merge_pdfs(input_paths, output_path))
    return download_response(output_path, "merged.pdf", "application/pdf", [workspace])


@router.post("/split")
async def split(file: UploadFile = File(...), ranges: str = Form("")):
    validate_pdf_file(file)
    workspace = prepare_workspace()
    input_path = await save_upload_or_cleanup(workspace, file, workspace / "input.pdf")
    output_path = workspace / "split-pages.zip"
    await run_pdf_job(workspace, lambda: split_pdf(input_path, output_path, ranges=ranges))
    return download_response(output_path, "split-pages.zip", "application/zip", [workspace])


@router.post("/rearrange")
async def rearrange(file: UploadFile = File(...), order: str = Form(...)):
    validate_pdf_file(file)
    workspace = prepare_workspace()
    input_path = await save_upload_or_cleanup(workspace, file, workspace / "input.pdf")
    output_path = workspace / "rearranged.pdf"
    await run_pdf_job(workspace, lambda: rearrange_pdf(input_path, output_path, order=order))
    return download_response(output_path, "rearranged.pdf", "application/pdf", [workspace])


@router.post("/pdf-to-word")
async def pdf_to_word(file: UploadFile = File(...)):
    validate_pdf_file(file)
    workspace = prepare_workspace()
    input_path = await save_upload_or_cleanup(workspace, file, workspace / "input.pdf")
    output_path = workspace / "converted.docx"
    await run_pdf_job(workspace, lambda: convert_pdf_to_word(input_path, output_path))
    return download_response(
        output_path,
        "converted.docx",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        [workspace],
    )


@router.post("/pdf-to-image")
async def pdf_to_image(file: UploadFile = File(...), dpi: int = Form(160)):
    validate_pdf_file(file)
    workspace = prepare_workspace()
    input_path = await save_upload_or_cleanup(workspace, file, workspace / "input.pdf")
    output_path = workspace / "pdf-images.zip"
    await run_pdf_job(workspace, lambda: convert_pdf_to_images(input_path, output_path, dpi=dpi))
    return download_response(output_path, "pdf-images.zip", "application/zip", [workspace])


@router.post("/image-to-pdf")
async def image_to_pdf(files: List[UploadFile] = File(...)):
    validate_image_files(files)
    workspace = prepare_workspace()
    input_paths = await save_uploads_or_cleanup(workspace, files)
    output_path = workspace / "images.pdf"
    await run_pdf_job(workspace, lambda: convert_images_to_pdf(input_paths, output_path))
    return download_response(output_path, "images.pdf", "application/pdf", [workspace])


@router.post("/watermark")
async def watermark(
    file: UploadFile = File(...),
    text: str = Form(...),
    opacity: float = Form(0.18),
):
    validate_pdf_file(file)
    workspace = prepare_workspace()
    input_path = await save_upload_or_cleanup(workspace, file, workspace / "input.pdf")
    output_path = workspace / "watermarked.pdf"
    await run_pdf_job(workspace, lambda: add_watermark(input_path, output_path, text=text, opacity=opacity))
    return download_response(output_path, "watermarked.pdf", "application/pdf", [workspace])


@router.post("/protect")
async def protect(file: UploadFile = File(...), password: str = Form(...)):
    validate_pdf_file(file)
    workspace = prepare_workspace()
    input_path = await save_upload_or_cleanup(workspace, file, workspace / "input.pdf")
    output_path = workspace / "protected.pdf"
    await run_pdf_job(workspace, lambda: protect_pdf(input_path, output_path, password=password))
    return download_response(output_path, "protected.pdf", "application/pdf", [workspace])
