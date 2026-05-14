import { resolveConfiguredBase } from "./api";

test("uses the Render v2 REACT_APP_API_BASE when configured in production", () => {
  expect(resolveConfiguredBase({
    NODE_ENV: "production",
    REACT_APP_API_BASE: "https://pdf-toolkit-api-v2.onrender.com/api/pdf/",
  })).toBe("https://pdf-toolkit-api-v2.onrender.com/api/pdf");
});

test("falls back to Render v2 backend in production when API base is missing", () => {
  expect(resolveConfiguredBase({ NODE_ENV: "production" })).toBe(
    "https://pdf-toolkit-api-v2.onrender.com/api/pdf",
  );
});

test("ignores non-v2 API base in production", () => {
  expect(resolveConfiguredBase({
    NODE_ENV: "production",
    REACT_APP_API_BASE: "https://api.company.test/api/pdf",
  })).toBe("https://pdf-toolkit-api-v2.onrender.com/api/pdf");
});

test("does not use localhost API base in production", () => {
  expect(resolveConfiguredBase({
    NODE_ENV: "production",
    REACT_APP_API_BASE: "http://127.0.0.1:8001/api/pdf",
  })).toBe("https://pdf-toolkit-api-v2.onrender.com/api/pdf");
});

test("treats Vercel host as production even if NODE_ENV is missing", () => {
  expect(resolveConfiguredBase({
    PAGE_HOSTNAME: "pdf-toolkit-web-v2.vercel.app",
    REACT_APP_API_BASE: "http://127.0.0.1:8001/api/pdf",
  })).toBe("https://pdf-toolkit-api-v2.onrender.com/api/pdf");
});

test("keeps localhost fallback for local development", () => {
  expect(resolveConfiguredBase({
    NODE_ENV: "development",
    PAGE_HOSTNAME: "127.0.0.1",
    REACT_APP_DEV_API_HOST: "127.0.0.1",
    REACT_APP_DEV_API_PORT: "8001",
  })).toBe("http://127.0.0.1:8001/api/pdf");
});
