import React, { useMemo, useState } from "react";
import { Activity, FileText, Moon, RotateCcw, Sparkles, Sun, UploadCloud } from "lucide-react";
import "./App.css";
import DownloadCard from "./components/DownloadCard";
import ToastStack from "./components/ToastStack";
import ToolCard from "./components/ToolCard";
import UploadPanel from "./components/UploadPanel";
import { initialFields, tools } from "./config/tools";
import { runPdfTool } from "./services/api";
import { checkBackendHealth, getResolvedApiBase } from "./services/apiClient";
import { validateFilesForTool, validateRequiredFields } from "./utils/validation";

export default function App() {
  const [activeId, setActiveId] = useState("compress");
  const [theme, setTheme] = useState("light");
  const [files, setFiles] = useState([]);
  const [fields, setFields] = useState(initialFields(tools[0]));
  const [progress, setProgress] = useState(0);
  const [isWorking, setIsWorking] = useState(false);
  const [download, setDownload] = useState(null);
  const [toasts, setToasts] = useState([]);

  const activeTool = useMemo(() => tools.find((tool) => tool.id === activeId), [activeId]);

  React.useEffect(() => {
    getResolvedApiBase()
      .then((apiBase) => console.info("[PDFToolkit:web-api] resolved API base", apiBase))
      .then(() => checkBackendHealth())
      .then((health) => console.info("[PDFToolkit:web-api] backend health", health))
      .catch((error) => console.error("[PDFToolkit:web-api] startup diagnostics failed", error));
  }, []);

  function showToast(message, tone = "info") {
    const id = Date.now();
    setToasts((items) => [...items, { id, message, tone }]);
    window.setTimeout(() => setToasts((items) => items.filter((item) => item.id !== id)), 3600);
  }

  function selectTool(tool) {
    setActiveId(tool.id);
    setFiles([]);
    setFields(initialFields(tool));
    setDownload(null);
    setProgress(0);
  }

  function handleFiles(nextFiles) {
    const selected = Array.from(nextFiles);
    const error = validateFilesForTool(activeTool, selected);
    if (error) {
      showToast(error, "error");
      return;
    }
    setFiles(selected);
    setDownload(null);
    setProgress(0);
    showToast(`${selected.length} file${selected.length > 1 ? "s" : ""} ready.`);
  }

  async function submitTool(event) {
    event.preventDefault();
    const fileError = validateFilesForTool(activeTool, files);
    if (fileError) {
      showToast(fileError, "error");
      return;
    }

    const fieldError = validateRequiredFields(activeTool, fields);
    if (fieldError) {
      showToast(fieldError, "error");
      return;
    }

    setIsWorking(true);
    setProgress(8);
    setDownload(null);
    try {
      const result = await runPdfTool(activeTool, files, fields, setProgress);
      setDownload(result);
      setProgress(100);
      showToast(`${activeTool.title} completed.`, "success");
    } catch (error) {
      showToast(error.message || "Processing failed.", "error");
      setProgress(0);
    } finally {
      setIsWorking(false);
    }
  }

  const ActiveIcon = activeTool.icon;

  return (
    <main className={`app-shell ${theme}`}>
      <ToastStack toasts={toasts} />
      <nav className="topbar">
        <button className="brand" onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}>
          <span className="brand-mark"><FileText size={22} /></span>
          <span>
            <strong>PDF Toolkit</strong>
            <small>FastAPI document studio</small>
          </span>
        </button>
        <div className="nav-actions">
          <a href="#workspace" className="nav-link">Workspace</a>
          <a href="#tools" className="nav-link">Tools</a>
          <span className="api-pill">9 tools live</span>
          <button className="icon-button" onClick={() => setTheme(theme === "light" ? "dark" : "light")} aria-label="Toggle theme">
            {theme === "light" ? <Moon size={18} /> : <Sun size={18} />}
          </button>
        </div>
      </nav>

      <section className="hero">
        <div className="hero-copy">
          <span className="eyebrow"><Sparkles size={17} /> Production PDF workflow suite</span>
          <h1>Compress, convert, organize and secure PDFs in one polished workspace.</h1>
          <p>
            A full-stack React and FastAPI toolkit with validated uploads, reliable downloads,
            real PDF processing, and a presentation-ready interface.
          </p>
          <div className="hero-stats">
            <span><strong>100MB</strong> upload limit</span>
            <span><strong>ZIP</strong> batch exports</span>
            <span><strong>Clean</strong> temporary files</span>
          </div>
          <div className="platform-strip" aria-label="Platform capabilities">
            <span><Activity size={16} /> Live API health</span>
            <span>Web + mobile ready</span>
            <span>FastAPI + PyMuPDF</span>
          </div>
        </div>

        <form className="workspace" id="workspace" onSubmit={submitTool}>
          <div className="workspace-head">
            <div className="tool-badge">
              <ActiveIcon size={24} />
            </div>
            <div>
              <h2>{activeTool.title}</h2>
              <p>{activeTool.description}</p>
            </div>
          </div>

          <UploadPanel tool={activeTool} files={files} onFiles={handleFiles} onClear={() => setFiles([])} />

          {!!activeTool.fields?.length && (
            <div className="field-grid">
              {activeTool.fields.map((field) => (
                <label key={field.name} className="field">
                  <span>{field.label}</span>
                  <input
                    type={field.type || "text"}
                    min={field.min}
                    max={field.max}
                    step={field.step}
                    placeholder={field.placeholder}
                    value={fields[field.name] ?? ""}
                    onChange={(event) => setFields((current) => ({ ...current, [field.name]: event.target.value }))}
                  />
                </label>
              ))}
            </div>
          )}

          <div className="progress-wrap">
            <span style={{ width: `${progress}%` }} />
          </div>

          <div className="action-row">
            <button className="primary-button" disabled={isWorking}>
              {isWorking ? <RotateCcw className="spin" size={18} /> : <UploadCloud size={18} />}
              {isWorking ? "Processing..." : `Run ${activeTool.title}`}
            </button>
          </div>

          <DownloadCard download={download} toolTitle={activeTool.title} />
        </form>
      </section>

      <section className="tools-section" id="tools">
        <div className="section-head">
          <span>Dashboard</span>
          <h2>Choose a PDF tool</h2>
        </div>
        <div className="tool-grid">
          {tools.map((tool) => (
            <ToolCard key={tool.id} tool={tool} active={tool.id === activeId} onClick={() => selectTool(tool)} />
          ))}
        </div>
      </section>
    </main>
  );
}
