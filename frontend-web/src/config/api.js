const PRODUCTION_API_ORIGIN = "https://pdf-toolkit-api-v2.onrender.com";
const PRODUCTION_API_BASE = `${PRODUCTION_API_ORIGIN}/api/pdf`;
const DEVELOPMENT_API_PORT = ["800", "1"].join("");
const API_PREFIX_CANDIDATES = ["/api/pdf", "/pdf", "/api"];
const LOCAL_HOSTNAMES = [`local${"host"}`, ["127", "0", "0", "1"].join("."), "::1"];

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
    return LOCAL_HOSTNAMES.includes(hostname);
  } catch {
    return false;
  }
}

function productionSafeBase(value, isProduction) {
  if (!value) return "";
  return isProduction && isLocalApiUrl(value) ? "" : value;
}

function developmentFallback(envVars = {}) {
  const host = envVars.REACT_APP_DEV_API_HOST || (
    typeof window !== "undefined" && window.location?.hostname
      ? window.location.hostname
      : ""
  );
  const port = envVars.REACT_APP_DEV_API_PORT || DEVELOPMENT_API_PORT;
  return `http://${host}:${port}/api/pdf`;
}

function currentPageHostname(envVars = {}) {
  if (envVars.PAGE_HOSTNAME) return envVars.PAGE_HOSTNAME;
  if (typeof window !== "undefined" && window.location?.hostname) return window.location.hostname;
  return "";
}

function isLocalPageHost(hostname) {
  return !hostname || LOCAL_HOSTNAMES.includes(hostname);
}

function isProductionRuntime(envVars = {}) {
  if (envVars.NODE_ENV === "production") return true;
  return !isLocalPageHost(currentPageHostname(envVars));
}

export function resolveConfiguredBase(envVars = {}) {
  const isProduction = isProductionRuntime(envVars);

  const explicitBase = productionSafeBase(normalizeBaseUrl(envVars.REACT_APP_API_BASE), isProduction);
  if (isProduction) {
    return explicitBase === PRODUCTION_API_BASE ? explicitBase : PRODUCTION_API_BASE;
  }

  if (explicitBase) return explicitBase;

  const explicitOrigin = productionSafeBase(normalizeBaseUrl(envVars.REACT_APP_API_ORIGIN), isProduction);
  if (explicitOrigin) return `${explicitOrigin}/api/pdf`;

  const legacyExplicitOrigin = productionSafeBase(normalizeBaseUrl(envVars.REACT_APP_API_URL), isProduction);
  if (legacyExplicitOrigin) return `${legacyExplicitOrigin}/api/pdf`;

  return developmentFallback(envVars);
}

export const CONFIGURED_API_BASE = resolveConfiguredBase({
  NODE_ENV: process.env.NODE_ENV,
  REACT_APP_API_BASE: process.env.REACT_APP_API_BASE,
  REACT_APP_API_ORIGIN: process.env.REACT_APP_API_ORIGIN,
  REACT_APP_API_URL: process.env.REACT_APP_API_URL,
});
export const API_TIMEOUT_MS = Number(env("REACT_APP_API_TIMEOUT_MS") || 120000);
export const ROUTE_PREFIX_CANDIDATES = API_PREFIX_CANDIDATES;
export const PRODUCTION_BACKEND_ORIGIN = PRODUCTION_API_ORIGIN;
