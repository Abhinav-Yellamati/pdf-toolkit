export function logInfo(scope, message, details) {
  write("info", scope, message, details);
}

export function logWarn(scope, message, details) {
  write("warn", scope, message, details);
}

export function logError(scope, message, error) {
  write("error", scope, message, serializeError(error));
}

function write(level, scope, message, details) {
  const payload = {
    time: new Date().toISOString(),
    level,
    scope,
    message,
    details,
  };

  const line = `[PDFToolkit:${scope}] ${message}`;

  if (level === "error") {
    console.error(line, payload);
    return;
  }

  if (level === "warn") {
    console.warn(line, payload);
    return;
  }

  console.log(line, payload);
}

function serializeError(error) {
  if (!error) return null;

  return {
    name: error.name,
    message: error.message || String(error),
    stack: error.stack,
  };
}
