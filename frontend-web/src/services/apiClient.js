import { API_TIMEOUT_MS, CONFIGURED_API_BASE, PRODUCTION_BACKEND_ORIGIN, ROUTE_PREFIX_CANDIDATES } from "../config/api";

let resolvedApiBasePromise;

function trimTrailingSlash(value) {
  return String(value || "").replace(/\/+$/, "");
}

function splitBase(base) {
  const url = new URL(base);
  return {
    origin: url.origin,
    pathname: trimTrailingSlash(url.pathname),
  };
}

function endpointUrl(base, endpoint) {
  return `${trimTrailingSlash(base)}${endpoint}`;
}

async function fetchJson(url) {
  const response = await fetch(url, { headers: { Accept: "application/json" } });
  if (!response.ok) throw new Error(`Route discovery failed at ${url} (${response.status})`);
  return response.json();
}

async function fetchWithDiagnostics(url, options = {}) {
  try {
    return await fetch(url, options);
  } catch (error) {
    console.error("[PDFToolkit:web-api] network failure", {
      url,
      message: error.message,
      configuredApiBase: CONFIGURED_API_BASE,
      productionBackendOrigin: PRODUCTION_BACKEND_ORIGIN,
      online: typeof navigator === "undefined" ? undefined : navigator.onLine,
      pageOrigin: typeof window === "undefined" ? undefined : window.location.origin,
    });
    throw error;
  }
}

function prefixFromOpenApi(openApi, endpoint) {
  const paths = Object.keys(openApi?.paths || {});
  const matchedPath = paths.find((path) => path.endsWith(endpoint));
  return matchedPath ? matchedPath.slice(0, matchedPath.length - endpoint.length) : "";
}

async function discoverPrefixFromOpenApi(origin, endpoint) {
  try {
    const openApi = await fetchJson(`${origin}/openapi.json`);
    return prefixFromOpenApi(openApi, endpoint);
  } catch (error) {
    console.warn("[PDFToolkit:web-api] OpenAPI route discovery failed", error);
    return "";
  }
}

async function probePrefix(origin, endpoint) {
  for (const prefix of ROUTE_PREFIX_CANDIDATES) {
    try {
      const response = await fetchWithDiagnostics(`${origin}${prefix}${endpoint}`, { method: "OPTIONS" });
      if (response.ok || response.status === 405) return prefix;
    } catch (error) {
      console.warn("[PDFToolkit:web-api] Route prefix probe failed", { prefix, message: error.message });
    }
  }

  return "";
}

async function resolveApiBase(endpoint = "/compress") {
  const configured = trimTrailingSlash(CONFIGURED_API_BASE);
  const { origin, pathname } = splitBase(configured);

  if (pathname && pathname !== "/") {
    return configured;
  }

  const openApiPrefix = await discoverPrefixFromOpenApi(origin, endpoint);
  if (openApiPrefix) return `${origin}${openApiPrefix}`;

  const probedPrefix = await probePrefix(origin, endpoint);
  if (probedPrefix) return `${origin}${probedPrefix}`;

  throw new Error(`Could not detect FastAPI PDF route prefix for ${origin}. Set REACT_APP_API_BASE to the full deployed API base, for example https://your-service.onrender.com/api/pdf.`);
}

async function apiBase(endpoint) {
  if (!resolvedApiBasePromise) {
    resolvedApiBasePromise = resolveApiBase(endpoint);
  }

  return resolvedApiBasePromise;
}

export async function apiRequest(endpoint, options = {}) {
  const base = await apiBase(endpoint);
  const controller = new AbortController();
  const timeout = window.setTimeout(() => controller.abort(), API_TIMEOUT_MS);
  const url = endpointUrl(base, endpoint);

  try {
    console.info("[PDFToolkit:web-api] request", { url, method: options.method || "GET" });
    const response = await fetchWithDiagnostics(url, {
      ...options,
      signal: controller.signal,
    });
    console.info("[PDFToolkit:web-api] response", { url, status: response.status });
    return response;
  } finally {
    window.clearTimeout(timeout);
  }
}

export async function getResolvedApiBase() {
  return apiBase("/compress");
}

export async function checkBackendHealth() {
  const base = await getResolvedApiBase();
  const origin = new URL(base).origin;
  const response = await fetchWithDiagnostics(`${origin}/health`, {
    headers: { Accept: "application/json" },
  });

  if (!response.ok) {
    throw new Error(`Backend health check failed (${response.status})`);
  }

  return response.json();
}
