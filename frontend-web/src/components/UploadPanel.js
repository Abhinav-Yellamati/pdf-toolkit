import React, { useState } from "react";
import { Trash2, UploadCloud } from "lucide-react";

function formatSize(bytes) {
  if (!bytes) return "0 KB";
  const units = ["B", "KB", "MB", "GB"];
  const index = Math.floor(Math.log(bytes) / Math.log(1024));
  return `${(bytes / Math.pow(1024, index)).toFixed(index ? 1 : 0)} ${units[index]}`;
}

export default function UploadPanel({ tool, files, onFiles, onClear }) {
  const [isDragging, setIsDragging] = useState(false);

  function handleDrop(event) {
    event.preventDefault();
    setIsDragging(false);
    onFiles(event.dataTransfer.files);
  }

  return (
    <div
      className={`upload-panel ${isDragging ? "dragging" : ""}`}
      onDragOver={(event) => {
        event.preventDefault();
        setIsDragging(true);
      }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={handleDrop}
    >
      <input
        id="file-upload"
        type="file"
        accept={tool.accept}
        multiple={tool.multiple}
        onChange={(event) => onFiles(event.target.files)}
      />
      <label htmlFor="file-upload" className="upload-target">
        <span className="upload-icon"><UploadCloud size={34} /></span>
        <strong>Drop files here or browse</strong>
        <small>{tool.multiple ? "Multiple files supported" : "Single file required"} up to 100MB each</small>
      </label>

      {!!files.length && (
        <div className="file-list">
          {files.map((file) => (
            <span key={`${file.name}-${file.size}`} className="file-chip">
              <span>{file.name}</span>
              <small>{formatSize(file.size)}</small>
            </span>
          ))}
          <button type="button" className="clear-button" onClick={onClear} aria-label="Clear files">
            <Trash2 size={16} />
          </button>
        </div>
      )}
    </div>
  );
}
