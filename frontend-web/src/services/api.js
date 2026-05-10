const DEFAULT_API_BASE = "http://127.0.0.1:8001/api/pdf";
const API_BASE = (process.env.REACT_APP_API_BASE || DEFAULT_API_BASE).replace(/\/+$/, "");
const API_TIMEOUT_MS = Number(process.env.REACT_APP_API_TIMEOUT_MS || 120000);

function apiErrorMessage(error) {
  if (error.name === "AbortError") {
    return "The request timed out. Please try again with a smaller file or check the backend service.";
  }
  return error.message || "The server could not process this file.";
}

export async function runPdfTool(tool, files, fields, onProgress) {
  const formData = new FormData();
  files.forEach((file) => formData.append(tool.multiple ? "files" : "file", file));
  Object.entries(fields).forEach(([key, value]) => {
    if (value !== undefined && value !== null) formData.append(key, value);
  });

  const controller = new AbortController();
  const timeout = window.setTimeout(() => controller.abort(), API_TIMEOUT_MS);
  const timer = window.setInterval(() => {
    onProgress((current) => Math.min(92, current + 7));
  }, 250);

  try {
    const response = await fetch(`${API_BASE}${tool.endpoint}`, {
      method: "POST",
      body: formData,
      signal: controller.signal,
    });
    if (!response.ok) {
      let message = "The server could not process this file.";
      try {
        const payload = await response.json();
        message = payload.detail || message;
      } catch {
        message = await response.text();
      }
      throw new Error(message);
    }
    const blob = await response.blob();
    return {
      url: URL.createObjectURL(blob),
      filename: tool.output,
    };
  } catch (error) {
    throw new Error(apiErrorMessage(error));
  } finally {
    window.clearInterval(timer);
    window.clearTimeout(timeout);
  }
}
