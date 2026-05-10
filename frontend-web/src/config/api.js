const PRODUCTION_API_ORIGIN = "https://pdf-toolkit-backend.onrender.com";
const PRODUCTION_API_BASE = `${PRODUCTION_API_ORIGIN}/api/pdf`;
const LOCAL_API_BASE = PRODUCTION_API_BASE;
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

function productionFallback() {
  return PRODUCTION_API_BASE;
}

function resolveConfiguredBase() {
  const explicitBase = normalizeBaseUrl(env("REACT_APP_API_BASE"));
  if (explicitBase) return explicitBase;

  const explicitOrigin = normalizeBaseUrl(env("REACT_APP_API_ORIGIN"));
  if (explicitOrigin) return `${explicitOrigin}/api/pdf`;

  const legacyExplicitOrigin = normalizeBaseUrl(env("REACT_APP_API_URL"));
  if (legacyExplicitOrigin) return `${legacyExplicitOrigin}/api/pdf`;

  if (env("NODE_ENV") === "production") {
    return productionFallback();
  }

  return LOCAL_API_BASE;
}

export const CONFIGURED_API_BASE = resolveConfiguredBase();
export const API_TIMEOUT_MS = Number(env("REACT_APP_API_TIMEOUT_MS") || 120000);
export const ROUTE_PREFIX_CANDIDATES = API_PREFIX_CANDIDATES;
export const PRODUCTION_BACKEND_ORIGIN = PRODUCTION_API_ORIGIN;
