import React from "react";
import { ArrowDownToLine, CheckCircle2, FileCheck2 } from "lucide-react";

export default function DownloadCard({ download, toolTitle }) {
  if (!download) return null;

  return (
    <section className="download-card" aria-live="polite">
      <span className="download-status">
        <CheckCircle2 size={18} />
        Ready
      </span>
      <div className="download-copy">
        <FileCheck2 size={28} />
        <div>
          <strong>{download.filename}</strong>
          <small>{toolTitle} finished successfully.</small>
        </div>
      </div>
      <a className="download-button" href={download.url} download={download.filename}>
        <ArrowDownToLine size={18} />
        Download file
      </a>
    </section>
  );
}

