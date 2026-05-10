import shutil
import os
import uuid
from pathlib import Path
from typing import Iterable

from fastapi import HTTPException, UploadFile

BASE_DIR = Path(__file__).resolve().parents[2]
STORAGE_DIR = Path(os.getenv("STORAGE_DIR", BASE_DIR / "storage"))
MAX_FILE_BYTES = int(os.getenv("MAX_FILE_MB", "100")) * 1024 * 1024


def prepare_workspace() -> Path:
    workspace = STORAGE_DIR / uuid.uuid4().hex
    workspace.mkdir(parents=True, exist_ok=True)
    return workspace


async def save_upload(file: UploadFile, destination: Path) -> Path:
    size = 0
    with destination.open("wb") as output:
        while chunk := await file.read(1024 * 1024):
            size += len(chunk)
            if size > MAX_FILE_BYTES:
                raise HTTPException(status_code=413, detail="File exceeds the 100MB upload limit.")
            output.write(chunk)
    await file.close()
    return destination


async def save_uploads(files: Iterable[UploadFile], workspace: Path) -> list[Path]:
    paths = []
    for index, file in enumerate(files, start=1):
        suffix = Path(file.filename or "").suffix.lower()
        path = workspace / f"file_{index}{suffix}"
        paths.append(await save_upload(file, path))
    return paths


def cleanup_paths(paths: Iterable[Path]) -> None:
    for path in paths:
        try:
            if path.is_dir():
                shutil.rmtree(path)
            elif path.exists():
                path.unlink()
        except OSError:
            pass
