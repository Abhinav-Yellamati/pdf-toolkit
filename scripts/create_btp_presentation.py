from __future__ import annotations

import html
import re
import zipfile
from pathlib import Path


OUT = Path("docs/presentation/PDF_Toolkit_BTP_Presentation.pptx")
GUIDE = Path("docs/presentation/PDF_Toolkit_BTP_Presenter_Guide.md")

SLIDE_W = 13_333_333
SLIDE_H = 7_500_000
NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
}


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def emu(inches: float) -> int:
    return int(inches * 914400)


def clean_notes(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def run_text(text: str, size: int = 20, color: str = "263238", bold: bool = False) -> str:
    b = ' b="1"' if bold else ""
    return (
        f'<a:r><a:rPr lang="en-US" sz="{size * 100}"{b}>'
        f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill></a:rPr>'
        f"<a:t>{esc(text)}</a:t></a:r>"
    )


def paragraph(text: str, size: int = 20, color: str = "263238", bold: bool = False, bullet: bool = False) -> str:
    mar = ' marL="285750" indent="-171450"' if bullet else ""
    bu = '<a:buChar char="•"/>' if bullet else ""
    return f"<a:p><a:pPr{mar}>{bu}</a:pPr>{run_text(text, size, color, bold)}<a:endParaRPr lang=\"en-US\" sz=\"{size * 100}\"/></a:p>"


def textbox(
    sid: int,
    name: str,
    x: float,
    y: float,
    w: float,
    h: float,
    lines: list[str],
    size: int = 20,
    color: str = "263238",
    bold_first: bool = False,
    bullet: bool = False,
    fill: str | None = None,
    line: str | None = None,
    radius: bool = False,
    align: str = "l",
) -> str:
    geom = "roundRect" if radius else "rect"
    fill_xml = "<a:noFill/>" if fill is None else f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>'
    line_xml = "<a:ln><a:noFill/></a:ln>" if line is None else f'<a:ln w="9525"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill></a:ln>'
    paras = []
    for i, line_text in enumerate(lines):
        paras.append(paragraph(line_text, size=size, color=color, bold=(bold_first and i == 0), bullet=bullet and i > 0))
    anchor = "mid" if align == "c" else "t"
    return f"""
    <p:sp>
      <p:nvSpPr><p:cNvPr id="{sid}" name="{esc(name)}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
      <p:spPr>
        <a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>
        <a:prstGeom prst="{geom}"><a:avLst/></a:prstGeom>{fill_xml}{line_xml}
      </p:spPr>
      <p:txBody><a:bodyPr wrap="square" anchor="{anchor}" lIns="137160" tIns="91440" rIns="137160" bIns="91440"/><a:lstStyle/>
        {''.join(paras)}
      </p:txBody>
    </p:sp>"""


def rect(sid: int, name: str, x: float, y: float, w: float, h: float, fill: str, line: str = "FFFFFF", radius: bool = False, alpha: int | None = None) -> str:
    geom = "roundRect" if radius else "rect"
    alpha_xml = f'<a:alpha val="{alpha}"/>' if alpha else ""
    return f"""
    <p:sp>
      <p:nvSpPr><p:cNvPr id="{sid}" name="{esc(name)}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
      <p:spPr><a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>
      <a:prstGeom prst="{geom}"><a:avLst/></a:prstGeom>
      <a:solidFill><a:srgbClr val="{fill}">{alpha_xml}</a:srgbClr></a:solidFill>
      <a:ln w="9525"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill></a:ln></p:spPr>
    </p:sp>"""


def line(sid: int, name: str, x1: float, y1: float, x2: float, y2: float, color: str = "1976D2", arrow: bool = True) -> str:
    head = '<a:headEnd type="triangle"/>' if arrow else ""
    return f"""
    <p:cxnSp>
      <p:nvCxnSpPr><p:cNvPr id="{sid}" name="{esc(name)}"/><p:cNvCxnSpPr/><p:nvPr/></p:nvCxnSpPr>
      <p:spPr><a:xfrm><a:off x="{emu(min(x1,x2))}" y="{emu(min(y1,y2))}"/><a:ext cx="{emu(abs(x2-x1))}" cy="{emu(abs(y2-y1))}"/></a:xfrm>
      <a:prstGeom prst="straightConnector1"><a:avLst/></a:prstGeom>
      <a:ln w="25400"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill>{head}</a:ln></p:spPr>
    </p:cxnSp>"""


def title_band(title: str, subtitle: str = "") -> list[str]:
    shapes = [rect(2, "Top blue band", 0, 0, 13.333, 0.62, "0B5CAD", "0B5CAD")]
    shapes.append(textbox(3, "Slide title", 0.45, 0.08, 9.5, 0.45, [title], 21, "FFFFFF", True))
    if subtitle:
        shapes.append(textbox(4, "Slide subtitle", 9.9, 0.12, 2.8, 0.36, [subtitle], 10, "EAF3FF", False, align="c"))
    return shapes


def placeholder(sid: int, label: str, x: float, y: float, w: float, h: float) -> str:
    return rect(sid, f"{label} placeholder", x, y, w, h, "F4F9FF", "8BBCE8", True) + textbox(
        sid + 1, label, x + 0.25, y + h / 2 - 0.3, w - 0.5, 0.6, [label, "Replace with actual screenshot"], 15, "0B5CAD", True, align="c"
    )


slides = [
    {
        "title": "PDF Toolkit",
        "subtitle": "A Web-Based PDF Processing Platform",
        "bullets": ["BTP Presentation", "React/Vite frontend + FastAPI backend", "Deployed with Vercel and Render"],
        "visual": "title",
        "notes": "Good morning respected faculty members. My BTP is PDF Toolkit, a web-based platform for common PDF operations. I will cover the problem, implementation, deployment, debugging journey, results, and future scope.",
    },
    {
        "title": "Introduction",
        "bullets": ["Browser-based toolkit for document processing", "Covers compression, conversion, merging, splitting, protection and watermarking", "Designed as a full-stack production-style project"],
        "notes": "Start by explaining that PDF operations are common in academic and office work. The project combines a user-friendly interface with a backend that performs the heavier PDF processing reliably.",
    },
    {
        "title": "Problem Statement",
        "bullets": ["Users rely on multiple third-party tools for simple PDF tasks", "Online tools may create privacy, size, and reliability concerns", "A single academic project should demonstrate complete frontend, backend and deployment flow"],
        "notes": "Explain that the problem is not only editing PDFs, but building a complete platform where upload, processing, download, API routing, validation, deployment and verification all work together.",
    },
    {
        "title": "Project Objectives",
        "bullets": ["Provide nine practical PDF utilities from one interface", "Use REST APIs for clean frontend-backend separation", "Deploy frontend and backend publicly", "Handle CORS, routing, file validation, and production checks"],
        "notes": "Mention measurable goals: working tools, documented APIs, public deployment, production environment variables, and verification scripts to prove the service is healthy after deployment.",
    },
    {
        "title": "Features Implemented",
        "bullets": ["Compress, merge, split, and rearrange pages", "Convert PDF to Word and PDF to images", "Convert images to PDF", "Watermark and password-protect PDF files"],
        "visual": "feature_grid",
        "notes": "Briefly describe each feature category. Keep the pace fast here because detailed implementation appears later in backend and API slides.",
    },
    {
        "title": "Technology Stack",
        "bullets": ["Frontend: React.js with Vite", "Backend: FastAPI, Uvicorn, Python", "PDF libraries: PyMuPDF and pypdf", "Deployment: Vercel for frontend, Render for backend"],
        "visual": "stack",
        "notes": "Explain why these technologies were selected: React for reusable UI, FastAPI for typed APIs and automatic docs, PyMuPDF/pypdf for PDF processing, Vercel/Render for public deployment.",
    },
    {
        "title": "System Architecture",
        "bullets": ["User selects a tool and uploads files in React", "React sends multipart REST requests to FastAPI", "FastAPI validates files and calls PDF service functions", "Generated file is returned as a downloadable response"],
        "visual": "architecture",
        "notes": "Walk left to right: browser UI, REST call, FastAPI router, processing service, file response. Emphasize that heavy processing stays on the server.",
    },
    {
        "title": "Frontend Design",
        "bullets": ["Tool-based UI with upload controls and parameters", "Uses production API base URL from environment configuration", "Handles loading, errors, and returned file downloads", "Designed for simple demo flow during presentation"],
        "visual": "frontend",
        "notes": "Explain that the frontend is intentionally simple for users: select a tool, upload a file, submit, and download the result. Environment variables avoid hardcoding localhost in production.",
    },
    {
        "title": "Backend Design",
        "bullets": ["FastAPI app exposes public routes and PDF routes under /api/pdf", "APIRouter groups all PDF endpoints", "Threadpool execution keeps async API responsive", "Temporary workspaces are cleaned after download"],
        "visual": "backend",
        "notes": "Explain FastAPI routing clearly. The main app mounts the PDF router with prefix /api/pdf, so /compress becomes /api/pdf/compress. Uploaded files are validated, saved temporarily, processed, returned, and then cleaned.",
    },
    {
        "title": "Deployment Architecture",
        "bullets": ["Vercel builds and hosts the React frontend", "Render builds Python backend and runs Uvicorn", "Frontend uses Render API URL as production API base", "CORS allows the Vercel origin to call Render safely"],
        "visual": "deployment",
        "notes": "Explain that frontend and backend are separate deployments. The browser loads React from Vercel, then calls the Render API over HTTPS. CORS is required because these are different origins.",
    },
    {
        "title": "Major Obstacles Faced",
        "bullets": ["Render service initially used the wrong backend assumptions", "Accidental Node/Express files conflicted with the Python backend", "Cannot GET /health and /docs indicated routing/startup mismatch", "Production variables and CORS needed exact configuration"],
        "notes": "Describe obstacles factually. The most important learning was that deployment platforms only run what is configured, so build/start commands, root directory and app import path must match the real backend.",
    },
    {
        "title": "Debugging & Solutions",
        "bullets": ["Removed Node/Express backend conflict and kept FastAPI as the only backend", "Configured Render rootDir as backend", "Configured startup: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT", "Added /health, /ready, /api/meta, /docs and startup route validation"],
        "visual": "debug",
        "notes": "Explain the Node/Express conflict: Render can detect Node if package files exist or if the wrong root is selected. Then /health may hit an Express/default service or no matching route. The fix was to remove the conflicting backend path and explicitly configure Python FastAPI with Uvicorn.",
    },
    {
        "title": "Results Obtained",
        "bullets": ["All major PDF workflows implemented through REST endpoints", "Frontend connects to deployed backend successfully", "Swagger/OpenAPI documentation available at /docs", "Deployment verification checks health, docs, metadata and tool endpoints"],
        "notes": "Mention practical outcomes: public web interface, deployed API, functioning PDF outputs, and smoke tests that validate production after deployment.",
    },
    {
        "title": "What I Learned",
        "bullets": ["Designing REST APIs for file upload and download workflows", "Handling CORS between two production domains", "Deploying Python APIs with Uvicorn on Render", "Debugging real production issues using logs, route maps, and verification scripts"],
        "notes": "Use this slide to show engineering maturity: not just building features, but diagnosing platform errors, validating routes, and separating frontend/backend responsibilities.",
    },
    {
        "title": "Future Improvements",
        "bullets": ["User accounts and document history", "Queue-based processing for large PDFs", "Cloud object storage for temporary files", "Batch processing and progress tracking", "More conversion formats and OCR support"],
        "notes": "Frame these as realistic next steps. Explain that current implementation is suitable for BTP scope, while larger-scale production would need queues, storage, authentication, and monitoring.",
    },
    {
        "title": "Conclusion",
        "bullets": ["PDF Toolkit demonstrates a complete full-stack PDF platform", "React handles the user experience; FastAPI handles processing", "Vercel and Render provide public deployment", "Debugging work strengthened the final production reliability"],
        "notes": "Conclude that the project satisfies both functionality and engineering objectives: usable tools, clean architecture, deployed services, API documentation and production verification.",
    },
    {
        "title": "Demo Workflow",
        "bullets": ["Open deployed frontend", "Choose a PDF operation such as Compress or Merge", "Upload input file and submit", "Frontend sends REST request to Render API", "Download and verify the processed output"],
        "visual": "demo",
        "notes": "During the demo, keep one reliable sample PDF ready. Show one fast feature first, such as compress or watermark, then show Swagger docs if time allows.",
    },
    {
        "title": "Live Demo Screenshots",
        "bullets": ["Frontend home/tools screen", "File upload and processing state", "Downloaded output result", "Backend health endpoint response"],
        "visual": "screens",
        "notes": "Replace the placeholders with actual screenshots from your deployed frontend and Render backend before final submission. Use this slide if internet is slow during the live demo.",
    },
    {
        "title": "API Documentation",
        "bullets": ["Swagger UI generated automatically by FastAPI", "OpenAPI schema confirms available routes and request formats", "Important routes: /health, /ready, /api/meta, /api/pdf/*", "Useful for testing and viva explanation"],
        "visual": "api",
        "notes": "Explain that FastAPI automatically generates /docs from route definitions and type hints. This makes backend validation transparent and helps test endpoints without manually writing a client.",
    },
    {
        "title": "Thank You",
        "bullets": ["Questions?", "PDF Toolkit - A Web-Based PDF Processing Platform"],
        "visual": "thanks",
        "notes": "Thank the panel and invite questions. Be ready to discuss CORS, deployment debugging, FastAPI routing, file uploads, and why backend processing was selected.",
    },
]


def visual_shapes(kind: str, start_id: int = 40) -> str:
    s: list[str] = []
    if kind == "title":
        s += [rect(start_id, "Hero block", 7.9, 1.15, 4.4, 4.6, "EAF3FF", "B9D8F5", True)]
        for i, label in enumerate(["PDF", "API", "UI"]):
            s.append(textbox(start_id + 1 + i, f"Icon {label}", 8.45 + i * 1.15, 2.45, 0.9, 0.9, [label], 18, "FFFFFF", True, fill="0B5CAD", line="0B5CAD", radius=True, align="c"))
        s.append(textbox(start_id + 5, "Hero caption", 8.35, 3.75, 3.5, 0.7, ["Web PDF processing", "from upload to download"], 16, "0B5CAD", True, align="c"))
    elif kind == "feature_grid":
        labels = ["Compress", "Merge", "Split", "Rearrange", "PDF->Word", "PDF->Image", "Image->PDF", "Watermark", "Protect"]
        for i, label in enumerate(labels):
            x = 6.8 + (i % 3) * 1.75
            y = 1.25 + (i // 3) * 1.28
            s.append(textbox(start_id + i, label, x, y, 1.45, 0.72, [label], 12, "0B5CAD", True, fill="F4F9FF", line="8BBCE8", radius=True, align="c"))
    elif kind == "stack":
        labels = [("React/Vite", "Frontend"), ("FastAPI", "Backend"), ("PyMuPDF + pypdf", "PDF Engine"), ("Vercel + Render", "Deployment")]
        for i, (a, b) in enumerate(labels):
            s.append(textbox(start_id + i, a, 6.7, 1.1 + i * 1.05, 4.7, 0.75, [a, b], 14, "FFFFFF" if i == 1 else "0B5CAD", True, fill="0B5CAD" if i == 1 else "EAF3FF", line="0B5CAD", radius=True, align="c"))
    elif kind == "architecture":
        boxes = [("React UI", 0.95), ("REST API", 3.15), ("FastAPI Router", 5.35), ("PDF Service", 7.8), ("Download", 10.1)]
        for i, (label, x) in enumerate(boxes):
            s.append(textbox(start_id + i, label, x, 2.6, 1.55, 0.75, [label], 13, "0B5CAD", True, fill="F4F9FF", line="0B5CAD", radius=True, align="c"))
            if i < len(boxes) - 1:
                s.append(line(start_id + 20 + i, f"Arrow {i}", x + 1.55, 2.98, boxes[i + 1][1], 2.98))
    elif kind == "frontend":
        s.append(placeholder(start_id, "Frontend UI screenshot", 6.3, 1.12, 5.7, 4.75))
    elif kind == "backend":
        boxes = [("main.py", 6.6, 1.15), ("APIRouter /api/pdf", 8.7, 1.15), ("validation", 6.6, 2.55), ("service function", 8.7, 2.55), ("FileResponse + cleanup", 7.45, 3.95)]
        for i, (label, x, y) in enumerate(boxes):
            s.append(textbox(start_id + i, label, x, y, 1.75, 0.62, [label], 11, "0B5CAD", True, fill="F4F9FF", line="8BBCE8", radius=True, align="c"))
    elif kind == "deployment":
        boxes = [("GitHub", 1.1, 2.7), ("Vercel\nReact", 3.6, 1.75), ("Browser", 6.0, 2.7), ("Render\nFastAPI", 8.5, 1.75), ("PDF Output", 10.9, 2.7)]
        for i, (label, x, y) in enumerate(boxes):
            s.append(textbox(start_id + i, label.replace("\n", " "), x, y, 1.55, 0.8, label.split("\n"), 12, "0B5CAD", True, fill="F4F9FF", line="0B5CAD", radius=True, align="c"))
            if i < len(boxes) - 1:
                s.append(line(start_id + 20 + i, f"Deploy arrow {i}", x + 1.55, y + 0.4, boxes[i + 1][1], boxes[i + 1][2] + 0.4))
    elif kind == "debug":
        rows = [("Symptom", "Cannot GET /health / /docs"), ("Cause", "Wrong backend/runtime path"), ("Fix", "FastAPI + Uvicorn + route checks"), ("Verify", "health, docs, OpenAPI, smoke tests")]
        for i, (a, b) in enumerate(rows):
            s.append(textbox(start_id + i, a, 6.4, 1.18 + i * 0.95, 1.35, 0.55, [a], 11, "FFFFFF", True, fill="0B5CAD", line="0B5CAD", radius=True, align="c"))
            s.append(textbox(start_id + 10 + i, b, 7.95, 1.18 + i * 0.95, 3.65, 0.55, [b], 11, "263238", False, fill="F4F9FF", line="B9D8F5", radius=True, align="c"))
    elif kind == "demo":
        steps = ["Open", "Choose", "Upload", "Process", "Download"]
        for i, label in enumerate(steps):
            s.append(textbox(start_id + i, label, 1.1 + i * 2.2, 3.15, 1.35, 0.75, [label], 12, "FFFFFF", True, fill="0B5CAD", line="0B5CAD", radius=True, align="c"))
            if i < 4:
                s.append(line(start_id + 20 + i, f"Demo arrow {i}", 2.45 + i * 2.2, 3.52, 3.3 + i * 2.2, 3.52))
    elif kind == "screens":
        s.append(placeholder(start_id, "Frontend screenshot", 6.15, 1.08, 2.65, 2.05))
        s.append(placeholder(start_id + 5, "Processing screenshot", 9.05, 1.08, 2.65, 2.05))
        s.append(placeholder(start_id + 10, "Swagger /docs screenshot", 6.15, 3.55, 5.55, 2.05))
    elif kind == "api":
        s.append(placeholder(start_id, "Swagger UI screenshot", 6.25, 1.05, 5.65, 4.8))
    elif kind == "thanks":
        s.append(textbox(start_id, "Q", 5.35, 2.05, 2.4, 2.4, ["Q&A"], 34, "FFFFFF", True, fill="0B5CAD", line="0B5CAD", radius=True, align="c"))
    return "".join(s)


def slide_xml(idx: int, slide: dict) -> str:
    shapes = [rect(1, "Background", 0, 0, 13.333, 7.5, "FFFFFF", "FFFFFF")]
    if idx == 1:
        shapes.append(rect(2, "Title left", 0, 0, 6.35, 7.5, "0B5CAD", "0B5CAD"))
        shapes.append(textbox(3, "Project title", 0.6, 1.25, 5.2, 1.25, [slide["title"], slide["subtitle"]], 29, "FFFFFF", True))
        shapes.append(textbox(4, "Title bullets", 0.75, 3.05, 4.9, 1.9, slide["bullets"], 17, "EAF3FF", False, bullet=True))
        shapes.append(visual_shapes("title"))
    else:
        shapes.extend(title_band(slide["title"], "PDF Toolkit BTP"))
        shapes.append(textbox(10, "Bullets", 0.65, 1.2, 5.3 if slide.get("visual") else 11.8, 4.9, ["Key Points"] + slide["bullets"], 17, "263238", True, bullet=True))
        if slide.get("visual"):
            shapes.append(visual_shapes(slide["visual"]))
    shapes.append(textbox(900, "Footer", 0.5, 7.03, 12.3, 0.28, [f"{idx:02d}  |  PDF Toolkit - BTP Presentation"], 8, "6B7A90", False, align="c"))
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="{NS['a']}" xmlns:r="{NS['r']}" xmlns:p="{NS['p']}">
  <p:cSld><p:spTree>
    <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
    <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
    {''.join(shapes)}
  </p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>"""


def notes_xml(idx: int, notes: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:notes xmlns:a="{NS['a']}" xmlns:r="{NS['r']}" xmlns:p="{NS['p']}">
  <p:cSld><p:spTree>
    <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
    <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
    {textbox(2, "Speaker Notes", 0.65, 5.35, 6.0, 2.0, ["Presenter notes", clean_notes(notes)], 12, "263238", True)}
  </p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:notes>"""


def rels_xml(targets: list[tuple[str, str]]) -> str:
    rels = []
    for i, (typ, target) in enumerate(targets, 1):
        rels.append(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/{typ}" Target="{target}"/>')
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + "".join(rels) + "</Relationships>"


def write_deck() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    overrides = [
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
        '<Default Extension="xml" ContentType="application/xml"/>',
        '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>',
        '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>',
        '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>',
        '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>',
        '<Override PartName="/ppt/notesMasters/notesMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesMaster+xml"/>',
    ]
    for i in range(1, len(slides) + 1):
        overrides.append(f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>')
        overrides.append(f'<Override PartName="/ppt/notesSlides/notesSlide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml"/>')

    slide_ids = "".join(f'<p:sldId id="{255+i}" r:id="rId{i+1}"/>' for i in range(1, len(slides) + 1))
    pres_rels = [("slideMaster", "slideMasters/slideMaster1.xml")] + [("slide", f"slides/slide{i}.xml") for i in range(1, len(slides) + 1)] + [("notesMaster", "notesMasters/notesMaster1.xml"), ("theme", "theme/theme1.xml")]

    slide_master = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldMaster xmlns:a="{NS['a']}" xmlns:r="{NS['r']}" xmlns:p="{NS['p']}"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld><p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/><p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst><p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles></p:sldMaster>"""
    slide_layout = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldLayout xmlns:a="{NS['a']}" xmlns:r="{NS['r']}" xmlns:p="{NS['p']}" type="blank" preserve="1"><p:cSld name="Blank"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>"""
    notes_master = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:notesMaster xmlns:a="{NS['a']}" xmlns:r="{NS['r']}" xmlns:p="{NS['p']}"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld><p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/></p:notesMaster>"""
    theme = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="PDF Toolkit"><a:themeElements><a:clrScheme name="Blue White"><a:dk1><a:srgbClr val="263238"/></a:dk1><a:lt1><a:srgbClr val="FFFFFF"/></a:lt1><a:dk2><a:srgbClr val="0B5CAD"/></a:dk2><a:lt2><a:srgbClr val="EAF3FF"/></a:lt2><a:accent1><a:srgbClr val="0B5CAD"/></a:accent1><a:accent2><a:srgbClr val="1976D2"/></a:accent2><a:accent3><a:srgbClr val="8BBCE8"/></a:accent3><a:accent4><a:srgbClr val="43A047"/></a:accent4><a:accent5><a:srgbClr val="F9A825"/></a:accent5><a:accent6><a:srgbClr val="546E7A"/></a:accent6><a:hlink><a:srgbClr val="0B5CAD"/></a:hlink><a:folHlink><a:srgbClr val="546E7A"/></a:folHlink></a:clrScheme><a:fontScheme name="Aptos"><a:majorFont><a:latin typeface="Aptos Display"/></a:majorFont><a:minorFont><a:latin typeface="Aptos"/></a:minorFont></a:fontScheme><a:fmtScheme name="Clean"><a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst><a:lnStyleLst><a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst><a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst><a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst></a:fmtScheme></a:themeElements></a:theme>"""

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">' + "".join(overrides) + "</Types>")
        z.writestr("_rels/.rels", rels_xml([("officeDocument", "ppt/presentation.xml")]))
        z.writestr("ppt/presentation.xml", f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:presentation xmlns:a="{NS['a']}" xmlns:r="{NS['r']}" xmlns:p="{NS['p']}"><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst><p:sldIdLst>{slide_ids}</p:sldIdLst><p:sldSz cx="{SLIDE_W}" cy="{SLIDE_H}" type="wide"/><p:notesSz cx="6858000" cy="9144000"/></p:presentation>""")
        z.writestr("ppt/_rels/presentation.xml.rels", rels_xml(pres_rels))
        z.writestr("ppt/slideMasters/slideMaster1.xml", slide_master)
        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", rels_xml([("slideLayout", "../slideLayouts/slideLayout1.xml"), ("theme", "../theme/theme1.xml")]))
        z.writestr("ppt/slideLayouts/slideLayout1.xml", slide_layout)
        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", rels_xml([("slideMaster", "../slideMasters/slideMaster1.xml")]))
        z.writestr("ppt/notesMasters/notesMaster1.xml", notes_master)
        z.writestr("ppt/notesMasters/_rels/notesMaster1.xml.rels", rels_xml([("theme", "../theme/theme1.xml")]))
        z.writestr("ppt/theme/theme1.xml", theme)
        for i, slide in enumerate(slides, 1):
            z.writestr(f"ppt/slides/slide{i}.xml", slide_xml(i, slide))
            z.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", rels_xml([("slideLayout", "../slideLayouts/slideLayout1.xml"), ("notesSlide", f"../notesSlides/notesSlide{i}.xml")]))
            z.writestr(f"ppt/notesSlides/notesSlide{i}.xml", notes_xml(i, slide["notes"]))
            z.writestr(f"ppt/notesSlides/_rels/notesSlide{i}.xml.rels", rels_xml([("slide", f"../slides/slide{i}.xml"), ("notesMaster", "../notesMasters/notesMaster1.xml")]))


def write_guide() -> None:
    qas = [
        ("Why did you use FastAPI?", "FastAPI gives typed request handling, automatic Swagger documentation, clean routing with APIRouter, file upload support through UploadFile, and easy deployment with Uvicorn."),
        ("How does React communicate with FastAPI?", "React creates multipart/form-data requests using the production API base URL. The request goes to Render, FastAPI validates uploads, processes the PDF, and returns a FileResponse that the browser downloads."),
        ("What is CORS and why was it needed?", "CORS is the browser security rule that controls whether one origin can call another. Since Vercel and Render have different domains, FastAPI must allow the Vercel origin and expose download headers like Content-Disposition."),
        ("Explain FastAPI routing in your project.", "The main app creates a FastAPI instance and includes the PDF router with prefix /api/pdf. Therefore router paths like /compress become public routes like /api/pdf/compress."),
        ("Why did the Node/Express conflict happen?", "Earlier deployment files or assumptions pointed the platform toward a Node/Express backend. That caused endpoints such as /health or /docs to be unavailable because the running service was not the intended FastAPI app."),
        ("How was the Express/Node issue fixed?", "The backend was standardized as Python FastAPI only. Render was configured with rootDir backend, Python build command, and Uvicorn startup command targeting app.main:app."),
        ("What does Cannot GET /health mean?", "It usually means the request reached a server, but that server did not have a GET route for /health. In this project, that indicated the wrong runtime/app or missing route registration."),
        ("How did you verify production deployment?", "I added health, ready, metadata, docs and OpenAPI checks, plus smoke tests that call each PDF endpoint with sample files and write a verification log."),
        ("Why not process PDFs only in React?", "Browser-only processing is limited for heavy PDFs and complex libraries. Backend processing gives better library support, centralized validation, and one implementation for all clients."),
        ("How are temporary files handled?", "Each request gets a temporary workspace. The processed output is returned as a download, and background cleanup removes the workspace after the response."),
    ]
    lines = ["# PDF Toolkit BTP Presenter Guide", "", "## 15-Minute Delivery Plan", ""]
    timing = [
        "0:00-1:00 Title and introduction",
        "1:00-3:00 Problem, objectives, and features",
        "3:00-6:00 Technology stack and system architecture",
        "6:00-9:30 Frontend, backend, routing, CORS, and API communication",
        "9:30-12:00 Deployment architecture and debugging story",
        "12:00-14:00 Results, learning, future scope, and demo workflow",
        "14:00-15:00 Conclusion and transition to viva questions",
    ]
    lines += [f"- {x}" for x in timing]
    lines += ["", "## Slide-Wise Speaker Notes", ""]
    for i, slide in enumerate(slides, 1):
        lines += [f"### {i}. {slide['title']}", clean_notes(slide["notes"]), ""]
    lines += ["## Deployment Debugging Explanation", ""]
    lines += [
        "The main deployment issue was runtime mismatch. The project needed a Python FastAPI backend, but accidental Node/Express backend assumptions caused routes like `/health` and `/docs` to fail. `Cannot GET /health` means a server responded, but the running app did not define that route.",
        "",
        "The fix was to make the backend unambiguous: Render uses `rootDir: backend`, installs `requirements.txt`, and starts `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`. The FastAPI app also defines `/health`, `/ready`, `/api/meta`, `/docs`, and validates expected routes during startup.",
        "",
        "Production validation then checks the Render origin, Swagger docs, OpenAPI JSON, metadata, and every PDF endpoint using sample files. This proves both routing and real document processing work after deployment.",
        "",
        "## Viva Questions and Strong Answers",
        "",
    ]
    for q, a in qas:
        lines += [f"**Q: {q}**", "", f"A: {a}", ""]
    lines += [
        "## Confident Delivery Tips",
        "",
        "- Keep the architecture explanation left-to-right: React, REST, FastAPI, PDF service, download.",
        "- When discussing bugs, state symptom, root cause, fix, and verification.",
        "- Do not memorize code. Memorize the flow and the reason behind each design choice.",
        "- Keep one sample PDF ready and demo one fast operation first.",
    ]
    GUIDE.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    write_deck()
    write_guide()
    print(f"Wrote {OUT}")
    print(f"Wrote {GUIDE}")
