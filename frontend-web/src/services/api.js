import { apiRequest } from "./apiClient";

function apiErrorMessage(error) {
  if (error.name === "AbortError") {
    return "The request timed out. Please try again with a smaller file or check the backend service.";
  }
  if (/Failed to fetch|NetworkError|Load failed/i.test(error.message || "")) {
    return "Could not reach the PDF backend. Please refresh and try again; if it continues, the Render backend may still be starting.";
  }
  return error.message || "The server could not process this file.";
}

export async function runPdfTool(tool, files, fields, onProgress) {
  const formData = new FormData();
  files.forEach((file) => formData.append(tool.multiple ? "files" : "file", file));
  Object.entries(fields).forEach(([key, value]) => {
    if (value !== undefined && value !== null) formData.append(key, value);
  });

  const timer = window.setInterval(() => {
    onProgress((current) => Math.min(92, current + 7));
  }, 250);

  try {
    const response = await apiRequest(tool.endpoint, {
      method: "POST",
      body: formData,
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
  }
}
