import * as FileSystem from "expo-file-system";
import * as Sharing from "expo-sharing";
import * as Base64 from "base-64";
import { API_BASE, API_TIMEOUT_MS, apiUrl, networkHelpMessage } from "../config/api";
import { logError, logInfo } from "../utils/logger";

const MIME_TYPES = {
  ".pdf": "application/pdf",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
};

function extensionFor(name = "") {
  const dotIndex = name.lastIndexOf(".");
  return dotIndex >= 0 ? name.slice(dotIndex).toLowerCase() : "";
}

function mimeTypeFor(file) {
  return file.mimeType || file.type || MIME_TYPES[extensionFor(file.name)] || "application/octet-stream";
}

function filePayload(file) {
  return {
    uri: file.uri,
    name: file.name || `upload${extensionFor(file.uri) || ".pdf"}`,
    type: mimeTypeFor(file),
  };
}

function arrayBufferToBase64(buffer) {
  const bytes = new Uint8Array(buffer);
  const chunkSize = 0x8000;
  let binary = "";

  for (let index = 0; index < bytes.length; index += chunkSize) {
    const chunk = bytes.subarray(index, index + chunkSize);
    binary += String.fromCharCode.apply(null, chunk);
  }

  return Base64.encode(binary);
}

async function fetchWithTimeout(url, options) {
  const canAbort = typeof AbortController !== "undefined";
  const controller = canAbort ? new AbortController() : null;
  const timeout = canAbort ? setTimeout(() => controller.abort(), API_TIMEOUT_MS) : null;

  try {
    return await fetch(url, { ...options, signal: controller?.signal });
  } catch (error) {
    if (error.name === "AbortError") {
      throw new Error(`The backend did not respond within ${Math.round(API_TIMEOUT_MS / 1000)} seconds.`);
    }

    logError("api", `Network request failed for ${url}`, error);
    throw new Error(networkHelpMessage());
  } finally {
    if (timeout) clearTimeout(timeout);
  }
}

async function responseErrorMessage(response) {
  let message = "The server could not process this file.";

  try {
    const payload = await response.json();
    message = payload.detail || message;
  } catch {
    const text = await response.text();
    message = text || message;
  }

  return `${message} (${response.status})`;
}

export async function runTool(tool, files, fields, onProgress) {
  const formData = new FormData();
  const fileField = tool.multiple ? "files" : "file";
  files.forEach((file) => formData.append(fileField, filePayload(file)));
  Object.entries(fields).forEach(([key, value]) => formData.append(key, String(value ?? "")));
  const url = apiUrl(tool.endpoint);

  logInfo("api", "Starting PDF tool request", {
    apiBase: API_BASE,
    endpoint: tool.endpoint,
    fileField,
    fileCount: files.length,
    fields: Object.keys(fields),
  });

  const timer = setInterval(() => onProgress((current) => Math.min(92, current + 6)), 240);
  try {
    const response = await fetchWithTimeout(url, {
      method: "POST",
      body: formData,
      headers: { Accept: "*/*" },
    });

    if (!response.ok) {
      const message = await responseErrorMessage(response);
      logError("api", `PDF tool request failed with HTTP ${response.status}`, new Error(message));
      throw new Error(message);
    }

    const buffer = await response.arrayBuffer();
    const base64 = arrayBufferToBase64(buffer);
    const uri = `${FileSystem.cacheDirectory}${Date.now()}-${tool.output}`;
    await FileSystem.writeAsStringAsync(uri, base64, { encoding: FileSystem.EncodingType.Base64 });
    onProgress(100);
    logInfo("api", "PDF tool request completed", { endpoint: tool.endpoint, outputUri: uri });
    return { uri, filename: tool.output };
  } finally {
    clearInterval(timer);
  }
}

export async function checkApiHealth() {
  const healthUrl = apiUrl("").replace("/api/pdf", "/health");
  logInfo("api", "Checking backend health", { healthUrl });
  const response = await fetchWithTimeout(healthUrl, {
    method: "GET",
    headers: { Accept: "application/json" },
  });

  if (!response.ok) {
    throw new Error(await responseErrorMessage(response));
  }

  return response.json();
}

export async function shareDownload(download) {
  if (!(await Sharing.isAvailableAsync())) {
    throw new Error("Sharing is not available on this device.");
  }
  await Sharing.shareAsync(download.uri, {
    dialogTitle: download.filename,
    mimeType: "application/octet-stream",
  });
}
