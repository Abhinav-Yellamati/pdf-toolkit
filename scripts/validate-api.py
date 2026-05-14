import sys
from pathlib import Path

import fitz
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app.main import app


def make_pdf(text="PDF Toolkit smoke test"):
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), text)
    data = doc.tobytes()
    doc.close()
    return data


def make_png():
    pix = fitz.Pixmap(fitz.csRGB, (0, 0, 16, 16), 0)
    pix.clear_with(0x336699)
    return pix.tobytes("png")


def assert_response(name, response, expected_type):
    content_type = response.headers.get("content-type", "")
    if response.status_code != 200 or expected_type not in content_type or not response.content:
        raise AssertionError(
            f"{name} failed: status={response.status_code} content_type={content_type} body={response.text[:200]!r}"
        )
    print(f"{name}: status={response.status_code} content_type={content_type} bytes={len(response.content)}")


def main():
    client = TestClient(app)
    pdf_a = make_pdf("first")
    pdf_b = make_pdf("second")
    png = make_png()

    json_checks = {
        "/health": client.get("/health"),
        "/openapi.json": client.get("/openapi.json"),
        "/api/meta": client.get("/api/meta"),
    }
    for path, response in json_checks.items():
        assert_response(path, response, "application/json")

    assert_response("/docs", client.get("/docs"), "text/html")

    checks = [
        (
            "compress",
            client.post(
                "/api/pdf/compress",
                files={"file": ("a.pdf", pdf_a, "application/pdf")},
                data={"quality": "55"},
            ),
            "application/pdf",
        ),
        (
            "merge",
            client.post(
                "/api/pdf/merge",
                files=[
                    ("files", ("a.pdf", pdf_a, "application/pdf")),
                    ("files", ("b.pdf", pdf_b, "application/pdf")),
                ],
            ),
            "application/pdf",
        ),
        (
            "split",
            client.post(
                "/api/pdf/split",
                files={"file": ("a.pdf", pdf_a, "application/pdf")},
                data={"ranges": "1"},
            ),
            "application/zip",
        ),
        (
            "rearrange",
            client.post(
                "/api/pdf/rearrange",
                files={"file": ("a.pdf", pdf_a, "application/pdf")},
                data={"order": "1"},
            ),
            "application/pdf",
        ),
        (
            "pdf-to-word",
            client.post("/api/pdf/pdf-to-word", files={"file": ("a.pdf", pdf_a, "application/pdf")}),
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ),
        (
            "pdf-to-image",
            client.post(
                "/api/pdf/pdf-to-image",
                files={"file": ("a.pdf", pdf_a, "application/pdf")},
                data={"dpi": "100"},
            ),
            "application/zip",
        ),
        (
            "image-to-pdf",
            client.post("/api/pdf/image-to-pdf", files=[("files", ("pixel.png", png, "image/png"))]),
            "application/pdf",
        ),
        (
            "watermark",
            client.post(
                "/api/pdf/watermark",
                files={"file": ("a.pdf", pdf_a, "application/pdf")},
                data={"text": "TEST", "opacity": "0.2"},
            ),
            "application/pdf",
        ),
        (
            "protect",
            client.post(
                "/api/pdf/protect",
                files={"file": ("a.pdf", pdf_a, "application/pdf")},
                data={"password": "test1234"},
            ),
            "application/pdf",
        ),
    ]

    for name, response, expected_type in checks:
        assert_response(name, response, expected_type)

    for origin in (
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://pdf-toolkit-black-ten.vercel.app",
        "https://preview.vercel.app",
    ):
        response = client.options(
            "/api/pdf/compress",
            headers={
                "Origin": origin,
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type",
            },
        )
        allowed_origin = response.headers.get("access-control-allow-origin")
        if response.status_code != 200 or allowed_origin != origin:
            raise AssertionError(f"CORS preflight failed for {origin}: {response.status_code} {allowed_origin}")
        print(f"cors:{origin}: status={response.status_code} allow_origin={allowed_origin}")

    print("API validation passed.")


if __name__ == "__main__":
    main()
