const PRODUCTION_API_ORIGIN = "https://pdf-toolkit-api-v2.onrender.com";
const PRODUCTION_API_BASE = `${PRODUCTION_API_ORIGIN}/api/pdf`;
const LOCAL_API_BASE = "http://127.0.0.1:8001/api/pdf";
const API_PREFIX_CANDIDATES = ["/api/pdf", "/pdf", "/api"];

function env(name) {
  if (typeof process === "undefined" || !process.env) return "";
  return process.env[name] || "";
}

function trimTrailingSlash(value) {
  return String(value || "").replace(/\/+$/, "");
}

function isPlaceholder(value) {
  return /your-|example\.com/i.test(value);
}

function normalizeBaseUrl(value) {
  const base = trimTrailingSlash(value);
  if (!base || isPlaceholder(base)) return "";
  return base;
}

function isLocalApiUrl(value) {
  try {
    const { hostname } = new URL(value);
    return hostname === "localhost" || hostname === "127.0.0.1" || hostname === "::1";
  } catch {
    return false;
  }
}

function productionSafeBase(value, isProduction) {
  if (!value) return "";
  return isProduction && isLocalApiUrl(value) ? "" : value;
}

export function resolveConfiguredBase(envVars = {}) {
  const isProduction = envVars.NODE_ENV === "production";

  const explicitBase = productionSafeBase(normalizeBaseUrl(envVars.REACT_APP_API_BASE), isProduction);
  if (explicitBase) return explicitBase;

  const explicitOrigin = productionSafeBase(normalizeBaseUrl(envVars.REACT_APP_API_ORIGIN), isProduction);
  if (explicitOrigin) return `${explicitOrigin}/api/pdf`;

  const legacyExplicitOrigin = productionSafeBase(normalizeBaseUrl(envVars.REACT_APP_API_URL), isProduction);
  if (legacyExplicitOrigin) return `${legacyExplicitOrigin}/api/pdf`;

  if (isProduction) return PRODUCTION_API_BASE;

  return LOCAL_API_BASE;
}

export const CONFIGURED_API_BASE = resolveConfiguredBase({
  NODE_ENV: env("NODE_ENV"),
  REACT_APP_API_BASE: env("REACT_APP_API_BASE"),
  REACT_APP_API_ORIGIN: env("REACT_APP_API_ORIGIN"),
  REACT_APP_API_URL: env("REACT_APP_API_URL"),
});
export const API_TIMEOUT_MS = Number(env("REACT_APP_API_TIMEOUT_MS") || 120000);
export const ROUTE_PREFIX_CANDIDATES = API_PREFIX_CANDIDATES;
export const PRODUCTION_BACKEND_ORIGIN = PRODUCTION_API_ORIGIN;
