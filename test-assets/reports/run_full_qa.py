import csv
import io
import json
import math
import os
import random
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import fitz
from fastapi.testclient import TestClient
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
ASSETS = ROOT / "test-assets"
SAMPLE = ASSETS / "sample-pdfs"
COMPRESSED = ASSETS / "compressed-results"
MERGE = ASSETS / "merge-results"
REARRANGE = ASSETS / "rearrange-results"
SPLIT = ASSETS / "split-results"
CONVERSION = ASSETS / "conversion-results"
WATERMARK = ASSETS / "watermark-results"
PASSWORD = ASSETS / "password-results"
SCREENSHOTS = ASSETS / "screenshots"
REPORTS = ASSETS / "reports"

for path in [SAMPLE, COMPRESSED, MERGE, REARRANGE, SPLIT, CONVERSION, WATERMARK, PASSWORD, SCREENSHOTS, REPORTS]:
    path.mkdir(parents=True, exist_ok=True)

os.chdir(BACKEND)
import sys

sys.path.insert(0, str(BACKEND))
from app.main import app


client = TestClient(app)


def size_mb(path: Path) -> float:
    return path.stat().st_size / (1024 * 1024)


def pdf_page_count(path: Path) -> int:
    return len(PdfReader(str(path)).pages)


def make_noise_png(path: Path, width: int, height: int, seed: int) -> None:
    random.seed(seed)
    pix = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, width, height), False)
    data = bytearray(width * height * 3)
    for y in range(height):
        for x in range(width):
            i = (y * width + x) * 3
            base = (x * 3 + y * 5 + seed) % 256
            data[i] = (base + random.randint(0, 90)) % 256
            data[i + 1] = (base * 2 + random.randint(0, 90)) % 256
            data[i + 2] = (base * 3 + random.randint(0, 90)) % 256
    pix.samples_mv[:] = data
    pix.save(path)


def make_text_pdf(path: Path, pages: int, title: str) -> None:
    doc = fitz.open()
    for i in range(1, pages + 1):
        page = doc.new_page(width=595, height=842)
        page.insert_text((72, 72), title, fontsize=22, fontname="helv", color=(0.1, 0.1, 0.1))
        body = [
            f"PDF Toolkit QA text sample - page {i}",
            "This page contains searchable text for conversion and readability validation.",
            "The document is generated automatically for repeatable backend testing.",
        ]
        y = 120
        for _ in range(12):
            for line in body:
                page.insert_text((72, y), line, fontsize=11, fontname="helv")
                y += 18
            y += 8
    doc.save(path, garbage=4, deflate=True)
    doc.close()


def make_image_pdf(path: Path, pages: int, image: Path, title: str) -> None:
    doc = fitz.open()
    for i in range(1, pages + 1):
        page = doc.new_page(width=595, height=842)
        page.insert_text((40, 35), f"{title} - page {i}", fontsize=16, fontname="helv")
        page.insert_image(fitz.Rect(35, 70, 560, 795), filename=str(image))
    doc.save(path, garbage=1, deflate=False)
    doc.close()


def make_mixed_pdf(path: Path, pages: int, image: Path) -> None:
    doc = fitz.open()
    for i in range(1, pages + 1):
        page = doc.new_page(width=595, height=842)
        page.insert_text((50, 50), f"Mixed content document - page {i}", fontsize=18, fontname="helv")
        page.insert_text((50, 88), "Text, raster image, and simple drawing elements are combined.", fontsize=11)
        page.draw_rect(fitz.Rect(50, 125, 545, 180), color=(0.2, 0.4, 0.7), fill=(0.9, 0.95, 1))
        page.insert_text((65, 155), f"Metric block {i}: generated for QA comparison", fontsize=12)
        page.insert_image(fitz.Rect(70, 220, 525, 720), filename=str(image))
    doc.save(path, garbage=1, deflate=False)
    doc.close()


def make_unique_large_image_pdf(path: Path, pages: int) -> None:
    doc = fitz.open()
    temp_images = []
    try:
        for i in range(1, pages + 1):
            image_path = SAMPLE / f"qa-large-page-{i}.png"
            if not image_path.exists():
                make_noise_png(image_path, 2600, 1900, 100 + i)
            temp_images.append(image_path)
            page = doc.new_page(width=595, height=842)
            page.insert_text((40, 35), f"Large image-heavy PDF - unique page {i}", fontsize=16, fontname="helv")
            page.insert_image(fitz.Rect(35, 70, 560, 795), filename=str(image_path))
        doc.save(path, garbage=1, deflate=False)
    finally:
        doc.close()


def ensure_assets():
    image_small = SAMPLE / "qa-image-small.png"
    image_medium = SAMPLE / "qa-image-medium.png"
    image_large = SAMPLE / "qa-image-large.png"
    if not image_small.exists():
        make_noise_png(image_small, 900, 700, 11)
    if not image_medium.exists():
        make_noise_png(image_medium, 1800, 1400, 22)
    if not image_large.exists():
        make_noise_png(image_large, 2600, 1900, 33)

    targets = {
        "text-small.pdf": lambda p: make_text_pdf(p, 8, "Small Text PDF"),
        "text-medium.pdf": lambda p: make_text_pdf(p, 55, "Medium Text PDF"),
        "image-heavy-small.pdf": lambda p: make_image_pdf(p, 2, image_small, "Image Heavy Small PDF"),
        "image-heavy-medium.pdf": lambda p: make_image_pdf(p, 4, image_medium, "Image Heavy Medium PDF"),
        "image-heavy-large.pdf": lambda p: make_unique_large_image_pdf(p, 4),
        "scanned-sample.pdf": lambda p: make_image_pdf(p, 3, image_medium, "Scanned Style PDF"),
        "mixed-content.pdf": lambda p: make_mixed_pdf(p, 6, image_small),
        "multi-page.pdf": lambda p: make_text_pdf(p, 25, "Multi Page PDF"),
    }
    for name, factory in targets.items():
        path = SAMPLE / name
        if name == "image-heavy-large.pdf" and path.exists() and size_mb(path) < 50:
            path.unlink()
        if not path.exists():
            factory(path)


def render_first_page(pdf_path: Path, out_path: Path) -> None:
    doc = fitz.open(pdf_path)
    page = doc[0]
    pix = page.get_pixmap(matrix=fitz.Matrix(0.5, 0.5), alpha=False)
    pix.save(out_path)
    doc.close()


def post_file(endpoint: str, file_path: Path, field: str = "file", data=None):
    with file_path.open("rb") as fh:
        files = {field: (file_path.name, fh, "application/pdf")}
        start = time.perf_counter()
        response = client.post(endpoint, files=files, data=data or {})
        elapsed = time.perf_counter() - start
    return response, elapsed


def write_bytes(path: Path, content: bytes) -> None:
    path.write_bytes(content)


def test_compression():
    rows = []
    for pdf in [
        SAMPLE / "text-small.pdf",
        SAMPLE / "image-heavy-small.pdf",
        SAMPLE / "image-heavy-medium.pdf",
        SAMPLE / "image-heavy-large.pdf",
        SAMPLE / "mixed-content.pdf",
    ]:
        for quality in [35, 55, 75]:
            response, elapsed = post_file("/api/pdf/compress", pdf, data={"quality": str(quality)})
            out = COMPRESSED / f"{pdf.stem}-q{quality}.pdf"
            ok = response.status_code == 200
            if ok:
                write_bytes(out, response.content)
                pages = pdf_page_count(out)
                render_first_page(out, SCREENSHOTS / f"compressed-{pdf.stem}-q{quality}.png")
                compressed_size = size_mb(out)
            else:
                pages = 0
                compressed_size = 0
            original = size_mb(pdf)
            reduction = (1 - compressed_size / original) * 100 if compressed_size else 0
            rows.append(
                {
                    "input": pdf.name,
                    "quality": quality,
                    "status": response.status_code,
                    "original_mb": round(original, 3),
                    "compressed_mb": round(compressed_size, 3),
                    "reduction_percent": round(reduction, 2),
                    "pages": pages,
                    "seconds": round(elapsed, 3),
                    "readable": ok and pages == pdf_page_count(pdf),
                    "notes": "Readable output" if ok else response.text[:120],
                }
            )
    return rows


def test_merge():
    cases = [
        ("merge-2-pdfs.pdf", [SAMPLE / "text-small.pdf", SAMPLE / "mixed-content.pdf"]),
        ("merge-multi-pdfs.pdf", [SAMPLE / "text-small.pdf", SAMPLE / "multi-page.pdf", SAMPLE / "scanned-sample.pdf"]),
        ("merge-large-mixed.pdf", [SAMPLE / "image-heavy-medium.pdf", SAMPLE / "image-heavy-large.pdf"]),
    ]
    rows = []
    for name, pdfs in cases:
        files = [("files", (p.name, p.open("rb"), "application/pdf")) for p in pdfs]
        start = time.perf_counter()
        response = client.post("/api/pdf/merge", files=files)
        elapsed = time.perf_counter() - start
        for _, file_tuple in files:
            file_tuple[1].close()
        out = MERGE / name
        expected_pages = sum(pdf_page_count(p) for p in pdfs)
        if response.status_code == 200:
            write_bytes(out, response.content)
            actual_pages = pdf_page_count(out)
            render_first_page(out, SCREENSHOTS / f"{Path(name).stem}.png")
        else:
            actual_pages = 0
        rows.append(
            {
                "case": name,
                "inputs": ", ".join(p.name for p in pdfs),
                "status": response.status_code,
                "expected_pages": expected_pages,
                "actual_pages": actual_pages,
                "page_order_valid": expected_pages == actual_pages,
                "output_mb": round(size_mb(out), 3) if out.exists() else 0,
                "seconds": round(elapsed, 3),
            }
        )
    return rows


def test_rearrange():
    cases = [
        ("rearrange-reverse-text-small.pdf", SAMPLE / "text-small.pdf", "8,7,6,5,4,3,2,1"),
        ("rearrange-mixed-selection.pdf", SAMPLE / "mixed-content.pdf", "2,4,6,1"),
    ]
    rows = []
    for name, pdf, order in cases:
        response, elapsed = post_file("/api/pdf/rearrange", pdf, data={"order": order})
        out = REARRANGE / name
        expected_pages = len([part for part in order.split(",") if part.strip()])
        if response.status_code == 200:
            write_bytes(out, response.content)
            actual_pages = pdf_page_count(out)
            render_first_page(out, SCREENSHOTS / f"{Path(name).stem}.png")
        else:
            actual_pages = 0
        rows.append(
            {
                "case": name,
                "input": pdf.name,
                "order": order,
                "status": response.status_code,
                "expected_pages": expected_pages,
                "actual_pages": actual_pages,
                "output_mb": round(size_mb(out), 3) if out.exists() else 0,
                "seconds": round(elapsed, 3),
                "valid": response.status_code == 200 and expected_pages == actual_pages,
            }
        )
    return rows


def test_split():
    cases = [
        ("split-ranges", SAMPLE / "multi-page.pdf", "1-3,5,7-8"),
        ("split-single-pages", SAMPLE / "text-small.pdf", ""),
        ("split-large", SAMPLE / "image-heavy-medium.pdf", "1-2,3-4"),
    ]
    rows = []
    for case, pdf, ranges in cases:
        response, elapsed = post_file("/api/pdf/split", pdf, data={"ranges": ranges})
        out = SPLIT / f"{case}.zip"
        if response.status_code == 200:
            write_bytes(out, response.content)
            with zipfile.ZipFile(out) as archive:
                names = archive.namelist()
                extracted_dir = SPLIT / case
                extracted_dir.mkdir(exist_ok=True)
                archive.extractall(extracted_dir)
            first_pdf = next((SPLIT / case).glob("*.pdf"), None)
            if first_pdf:
                render_first_page(first_pdf, SCREENSHOTS / f"{case}.png")
        else:
            names = []
        rows.append(
            {
                "case": case,
                "input": pdf.name,
                "ranges": ranges or "single pages",
                "status": response.status_code,
                "zip_entries": len(names),
                "output_mb": round(size_mb(out), 3) if out.exists() else 0,
                "seconds": round(elapsed, 3),
                "entries": ", ".join(names[:8]),
            }
        )
    return rows


def test_conversions():
    rows = []
    pdf = SAMPLE / "mixed-content.pdf"
    for endpoint, filename, media in [
        ("/api/pdf/pdf-to-word", "mixed-content.docx", "application/pdf"),
        ("/api/pdf/pdf-to-image", "mixed-content-images.zip", "application/pdf"),
    ]:
        response, elapsed = post_file(endpoint, pdf)
        out = CONVERSION / filename
        if response.status_code == 200:
            write_bytes(out, response.content)
        entries = ""
        if out.suffix == ".zip" and out.exists():
            with zipfile.ZipFile(out) as archive:
                entries = ", ".join(archive.namelist()[:6])
        rows.append(
            {
                "case": endpoint,
                "status": response.status_code,
                "output": filename,
                "output_mb": round(size_mb(out), 3) if out.exists() else 0,
                "seconds": round(elapsed, 3),
                "observations": entries or "File generated",
            }
        )

    image_files = []
    for p in [SAMPLE / "qa-image-small.png", SAMPLE / "qa-image-medium.png"]:
        image_files.append(("files", (p.name, p.open("rb"), "image/png")))
    start = time.perf_counter()
    response = client.post("/api/pdf/image-to-pdf", files=image_files)
    elapsed = time.perf_counter() - start
    for _, file_tuple in image_files:
        file_tuple[1].close()
    out = CONVERSION / "images-to-pdf.pdf"
    if response.status_code == 200:
        write_bytes(out, response.content)
        render_first_page(out, SCREENSHOTS / "images-to-pdf.png")
    rows.append(
        {
            "case": "/api/pdf/image-to-pdf",
            "status": response.status_code,
            "output": out.name,
            "output_mb": round(size_mb(out), 3) if out.exists() else 0,
            "seconds": round(elapsed, 3),
            "observations": f"pages={pdf_page_count(out)}" if out.exists() else response.text[:120],
        }
    )
    return rows


def test_watermark():
    rows = []
    for opacity in [0.1, 0.35, 0.7]:
        pdf = SAMPLE / "multi-page.pdf"
        response, elapsed = post_file(
            "/api/pdf/watermark",
            pdf,
            data={"text": f"PDF TOOLKIT QA {opacity}", "opacity": str(opacity)},
        )
        out = WATERMARK / f"watermark-opacity-{opacity}.pdf"
        if response.status_code == 200:
            write_bytes(out, response.content)
            render_first_page(out, SCREENSHOTS / f"watermark-opacity-{opacity}.png")
        rows.append(
            {
                "case": f"text opacity {opacity}",
                "status": response.status_code,
                "pages": pdf_page_count(out) if out.exists() else 0,
                "output_mb": round(size_mb(out), 3) if out.exists() else 0,
                "seconds": round(elapsed, 3),
                "observations": "Text watermark applied" if response.status_code == 200 else response.text[:120],
            }
        )
    rows.append(
        {
            "case": "image watermark",
            "status": "not implemented",
            "pages": 0,
            "output_mb": 0,
            "seconds": 0,
            "observations": "Current API supports text watermark only; image watermark endpoint is not present.",
        }
    )
    return rows


def test_password():
    pdf = SAMPLE / "text-small.pdf"
    response, elapsed = post_file("/api/pdf/protect", pdf, data={"password": "qa-pass-2026"})
    out = PASSWORD / "protected-text-small.pdf"
    if response.status_code == 200:
        write_bytes(out, response.content)
        reader = PdfReader(str(out))
        encrypted = reader.is_encrypted
        invalid_result = reader.decrypt("wrong-password")
        valid_result = reader.decrypt("qa-pass-2026")
        pages = len(reader.pages) if valid_result else 0
    else:
        encrypted = False
        invalid_result = 0
        valid_result = 0
        pages = 0
    return [
        {
            "case": "add password",
            "status": response.status_code,
            "encrypted": encrypted,
            "invalid_password_result": invalid_result,
            "valid_password_result": valid_result,
            "pages_after_unlock": pages,
            "output_mb": round(size_mb(out), 3) if out.exists() else 0,
            "seconds": round(elapsed, 3),
        }
    ]


def test_invalid_and_cors():
    bad = io.BytesIO(b"not a pdf")
    start = time.perf_counter()
    invalid_response = client.post("/api/pdf/compress", files={"file": ("bad.txt", bad, "text/plain")})
    invalid_elapsed = time.perf_counter() - start
    cors_response = client.options(
        "/api/pdf/compress",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
        },
    )
    health_start = time.perf_counter()
    health = client.get("/health")
    health_elapsed = time.perf_counter() - health_start
    return [
        {
            "case": "invalid upload",
            "status": invalid_response.status_code,
            "seconds": round(invalid_elapsed, 3),
            "observations": invalid_response.text[:160],
        },
        {
            "case": "cors preflight",
            "status": cors_response.status_code,
            "seconds": 0,
            "observations": str(dict(cors_response.headers)),
        },
        {
            "case": "health",
            "status": health.status_code,
            "seconds": round(health_elapsed, 3),
            "observations": health.text,
        },
    ]


def test_concurrent_uploads():
    pdf = SAMPLE / "text-small.pdf"

    def one(index):
        response, elapsed = post_file("/api/pdf/compress", pdf, data={"quality": "55"})
        return {"request": index, "status": response.status_code, "seconds": round(elapsed, 3), "bytes": len(response.content)}

    rows = []
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(one, i) for i in range(1, 9)]
        for future in as_completed(futures):
            rows.append(future.result())
    total = time.perf_counter() - start
    return rows, round(total, 3)


def write_csv(name: str, rows):
    if not rows:
        return
    path = REPORTS / name
    keys = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows):
    if not rows:
        return ""
    keys = list(rows[0].keys())
    lines = ["| " + " | ".join(keys) + " |", "| " + " | ".join(["---"] * len(keys)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(k, "")).replace("|", "/") for k in keys) + " |")
    return "\n".join(lines)


def main():
    started = time.perf_counter()
    ensure_assets()
    for pdf in SAMPLE.glob("*.pdf"):
        render_first_page(pdf, SCREENSHOTS / f"original-{pdf.stem}.png")

    asset_rows = [
        {"file": p.name, "size_mb": round(size_mb(p), 3), "pages": pdf_page_count(p)}
        for p in sorted(SAMPLE.glob("*.pdf"))
    ]
    compression = test_compression()
    merge = test_merge()
    rearrange = test_rearrange()
    split = test_split()
    conversions = test_conversions()
    watermark = test_watermark()
    password = test_password()
    backend = test_invalid_and_cors()
    concurrent, concurrent_total = test_concurrent_uploads()

    for name, rows in [
        ("asset-inventory.csv", asset_rows),
        ("compression-results.csv", compression),
        ("merge-results.csv", merge),
        ("rearrange-results.csv", rearrange),
        ("split-results.csv", split),
        ("conversion-results.csv", conversions),
        ("watermark-results.csv", watermark),
        ("password-results.csv", password),
        ("backend-results.csv", backend),
        ("concurrent-results.csv", concurrent),
    ]:
        write_csv(name, rows)

    summary = {
        "asset_count": len(asset_rows),
        "largest_asset_mb": max(row["size_mb"] for row in asset_rows),
        "compression_cases": len(compression),
        "compression_success": sum(1 for row in compression if row["status"] == 200),
        "merge_success": sum(1 for row in merge if row["status"] == 200),
        "rearrange_success": sum(1 for row in rearrange if row["status"] == 200),
        "split_success": sum(1 for row in split if row["status"] == 200),
        "conversion_success": sum(1 for row in conversions if row["status"] == 200),
        "watermark_text_success": sum(1 for row in watermark if row["status"] == 200),
        "password_success": sum(1 for row in password if row["status"] == 200 and row["encrypted"]),
        "concurrent_total_seconds": concurrent_total,
        "total_seconds": round(time.perf_counter() - started, 3),
    }
    (REPORTS / "qa-summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (REPORTS / "qa-summary.md").write_text(
        "# QA Summary\n\n"
        "## Test Assets\n\n"
        + markdown_table(asset_rows)
        + "\n\n## Compression\n\n"
        + markdown_table(compression)
        + "\n\n## Merge\n\n"
        + markdown_table(merge)
        + "\n\n## Rearrange\n\n"
        + markdown_table(rearrange)
        + "\n\n## Split\n\n"
        + markdown_table(split)
        + "\n\n## Conversions\n\n"
        + markdown_table(conversions)
        + "\n\n## Watermark\n\n"
        + markdown_table(watermark)
        + "\n\n## Password\n\n"
        + markdown_table(password)
        + "\n\n## Backend\n\n"
        + markdown_table(backend)
        + "\n\n## Concurrent Uploads\n\n"
        + markdown_table(concurrent)
        + f"\n\nConcurrent total seconds: {concurrent_total}\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
