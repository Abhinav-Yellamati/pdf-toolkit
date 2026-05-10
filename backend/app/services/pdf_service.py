import re
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

import fitz
from fastapi import HTTPException
from pypdf import PdfReader, PdfWriter


def compress_pdf(input_path: Path, output_path: Path, quality: int = 55) -> None:
    quality = max(20, min(85, int(quality)))
    doc = fitz.open(input_path)
    if doc.needs_pass:
        doc.close()
        raise HTTPException(status_code=400, detail="Password protected PDFs cannot be compressed.")
    try:
        doc.set_metadata({})
        for page in doc:
            for image in page.get_images(full=True):
                xref = image[0]
                pix = None
                temp = None
                try:
                    pix = fitz.Pixmap(doc, xref)
                    if pix.alpha or pix.n > 3:
                        pix = fitz.Pixmap(fitz.csRGB, pix)
                    if pix.width > 1600 or pix.height > 1600:
                        factor = min(1600 / pix.width, 1600 / pix.height)
                        matrix = fitz.Matrix(factor, factor)
                        rect = fitz.Rect(0, 0, pix.width, pix.height)
                        temp = fitz.open()
                        page_img = temp.new_page(width=pix.width, height=pix.height)
                        page_img.insert_image(rect, pixmap=pix)
                        pix = page_img.get_pixmap(matrix=matrix, alpha=False)
                    doc.update_stream(xref, pix.tobytes("jpeg", jpg_quality=quality))
                except Exception:
                    continue
                finally:
                    if temp is not None:
                        temp.close()
                    if pix is not None:
                        pix = None
        doc.save(output_path, garbage=4, deflate=True, clean=True)
    finally:
        doc.close()


def merge_pdfs(input_paths: list[Path], output_path: Path) -> None:
    writer = PdfWriter()
    for path in input_paths:
        reader = PdfReader(str(path))
        if reader.is_encrypted:
            raise HTTPException(status_code=400, detail=f"{path.name} is password protected.")
        for page in reader.pages:
            writer.add_page(page)
    with output_path.open("wb") as output:
        writer.write(output)


def split_pdf(input_path: Path, zip_path: Path, ranges: str = "") -> None:
    reader = PdfReader(str(input_path))
    if reader.is_encrypted:
        raise HTTPException(status_code=400, detail="Password protected PDFs cannot be split.")
    page_groups = _parse_ranges(ranges, len(reader.pages)) if ranges.strip() else [[i] for i in range(len(reader.pages))]
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for index, group in enumerate(page_groups, start=1):
            writer = PdfWriter()
            for page_index in group:
                writer.add_page(reader.pages[page_index])
            page_path = zip_path.parent / f"split_{index}.pdf"
            with page_path.open("wb") as output:
                writer.write(output)
            archive.write(page_path, arcname=page_path.name)


def rearrange_pdf(input_path: Path, output_path: Path, order: str) -> None:
    reader = PdfReader(str(input_path))
    if reader.is_encrypted:
        raise HTTPException(status_code=400, detail="Password protected PDFs cannot be rearranged.")
    indexes = _parse_order(order, len(reader.pages))
    writer = PdfWriter()
    for page_index in indexes:
        writer.add_page(reader.pages[page_index])
    with output_path.open("wb") as output:
        writer.write(output)


def convert_pdf_to_word(input_path: Path, output_path: Path) -> None:
    doc = fitz.open(input_path)
    try:
        paragraphs = []
        for page_index, page in enumerate(doc, start=1):
            text = page.get_text("text").strip()
            paragraphs.append(f"Page {page_index}")
            paragraphs.extend(line.strip() for line in text.splitlines() if line.strip())
        _write_docx(output_path, paragraphs or ["No extractable text found."])
    finally:
        doc.close()


def convert_pdf_to_images(input_path: Path, zip_path: Path, dpi: int = 160) -> None:
    dpi = max(72, min(300, int(dpi)))
    matrix = fitz.Matrix(dpi / 72, dpi / 72)
    doc = fitz.open(input_path)
    try:
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for index, page in enumerate(doc, start=1):
                pix = page.get_pixmap(matrix=matrix, alpha=False)
                image_path = zip_path.parent / f"page_{index}.png"
                pix.save(image_path)
                archive.write(image_path, arcname=image_path.name)
    finally:
        doc.close()


def convert_images_to_pdf(input_paths: list[Path], output_path: Path) -> None:
    doc = fitz.open()
    try:
        for image_path in input_paths:
            image_doc = fitz.open(image_path)
            rect = image_doc[0].rect
            page = doc.new_page(width=rect.width, height=rect.height)
            page.insert_image(rect, filename=str(image_path))
            image_doc.close()
        doc.save(output_path, garbage=4, deflate=True)
    finally:
        doc.close()


def add_watermark(input_path: Path, output_path: Path, text: str, opacity: float = 0.18) -> None:
    if not text.strip():
        raise HTTPException(status_code=400, detail="Watermark text is required.")
    opacity = max(0.05, min(0.75, float(opacity)))
    doc = fitz.open(input_path)
    try:
        for page in doc:
            rect = page.rect
            font_size = max(28, min(72, rect.width / max(len(text), 8) * 1.4))
            page.insert_textbox(
                rect,
                text,
                fontsize=font_size,
                fontname="helv",
                color=(0.85, 0.1, 0.1),
                align=fitz.TEXT_ALIGN_CENTER,
                fill_opacity=opacity,
                overlay=True,
            )
        doc.save(output_path, garbage=4, deflate=True, clean=True)
    finally:
        doc.close()


def protect_pdf(input_path: Path, output_path: Path, password: str) -> None:
    if len(password) < 4:
        raise HTTPException(status_code=400, detail="Password must be at least 4 characters.")
    reader = PdfReader(str(input_path))
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.encrypt(user_password=password, owner_password=password, use_128bit=True)
    with output_path.open("wb") as output:
        writer.write(output)


def _parse_order(order: str, page_count: int) -> list[int]:
    try:
        indexes = [int(item.strip()) - 1 for item in order.split(",") if item.strip()]
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Page order must be comma-separated numbers.") from exc
    if not indexes or any(index < 0 or index >= page_count for index in indexes):
        raise HTTPException(status_code=400, detail=f"Page order must use numbers from 1 to {page_count}.")
    return indexes


def _parse_ranges(ranges: str, page_count: int) -> list[list[int]]:
    groups = []
    for part in re.split(r"[,;]", ranges):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_text, end_text = part.split("-", 1)
            start, end = int(start_text), int(end_text)
            if start > end:
                start, end = end, start
            group = list(range(start - 1, end))
        else:
            group = [int(part) - 1]
        if any(index < 0 or index >= page_count for index in group):
            raise HTTPException(status_code=400, detail=f"Ranges must use pages from 1 to {page_count}.")
        groups.append(group)
    if not groups:
        raise HTTPException(status_code=400, detail="No valid split ranges were provided.")
    return groups


def _write_docx(output_path: Path, paragraphs: list[str]) -> None:
    document_xml = "".join(
        f"<w:p><w:r><w:t>{escape(paragraph)}</w:t></w:r></w:p>" for paragraph in paragraphs
    )
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>"""
    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>"""
    document = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>{document_xml}<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr></w:body></w:document>"""
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as docx:
        docx.writestr("[Content_Types].xml", content_types)
        docx.writestr("_rels/.rels", rels)
        docx.writestr("word/document.xml", document)
