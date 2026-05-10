import React from "react";

export default function ToolCard({ tool, active, onClick }) {
  const Icon = tool.icon;
  return (
    <button className={`tool-card ${active ? "active" : ""}`} onClick={onClick}>
      <span className="tool-icon"><Icon size={24} /></span>
      <span className="tool-title">{tool.title}</span>
      <span className="tool-desc">{tool.description}</span>
    </button>
  );
}
