import Constants from "expo-constants";
import { logInfo, logWarn } from "../utils/logger";

const DEFAULT_BACKEND_PORT = "8001";
const DEFAULT_LAN_HOST = "127.0.0.1";
const API_PATH = "/api/pdf";

function env(name) {
  if (typeof process === "undefined" || !process.env) {
    return "";
  }

  return process.env[name] || "";
}

function trimTrailingSlash(value) {
  return String(value || "").replace(/\/+$/, "");
}

function normalizeApiBase(value) {
  const base = trimTrailingSlash(value);
  if (!base) return "";
  return base.endsWith(API_PATH) ? base : `${base}${API_PATH}`;
}

function expoHostUri() {
  try {
    return (
      Constants.expoConfig?.hostUri ||
      Constants.manifest2?.extra?.expoClient?.hostUri ||
      Constants.manifest?.debuggerHost ||
      ""
    );
  } catch (error) {
    logWarn("config", "Unable to read Expo host URI", { message: error.message });
    return "";
  }
}

function hostFromExpo() {
  const hostUri = expoHostUri();
  const host = hostUri.split(":")[0];

  if (!host || host === "localhost" || host === "127.0.0.1") {
    return "";
  }

  return host;
}

function resolveApiBase() {
  const explicitBaseUrl = normalizeApiBase(env("EXPO_PUBLIC_API_BASE_URL"));
  if (explicitBaseUrl) {
    return explicitBaseUrl;
  }

  const explicitOrigin = normalizeApiBase(env("EXPO_PUBLIC_API_ORIGIN"));
  if (explicitOrigin) {
    return explicitOrigin;
  }

  const host = hostFromExpo() || env("EXPO_PUBLIC_BACKEND_HOST") || DEFAULT_LAN_HOST;
  const port = env("EXPO_PUBLIC_BACKEND_PORT") || DEFAULT_BACKEND_PORT;
  return `http://${host}:${port}${API_PATH}`;
}

export const API_BASE = resolveApiBase();
export const API_TIMEOUT_MS = Number(env("EXPO_PUBLIC_API_TIMEOUT_MS") || 120000);

logInfo("config", "API configuration resolved", {
  apiBase: API_BASE,
  timeoutMs: API_TIMEOUT_MS,
  expoHostUri: expoHostUri(),
});

export function apiUrl(path) {
  return `${API_BASE}${path}`;
}

export function networkHelpMessage() {
  return `Cannot reach the PDF backend at ${API_BASE}. For production, check EXPO_PUBLIC_API_BASE_URL. For local LAN testing, make sure your phone and computer are on the same Wi-Fi, the backend is running with --host 0.0.0.0, and Windows Firewall allows the backend port.`;
}
