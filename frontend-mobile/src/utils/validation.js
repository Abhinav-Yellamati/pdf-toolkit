import { MAX_FILE_SIZE_MB } from "../config/tools";

export function validateFiles(tool, files) {
  if (!files.length) return "Select at least one file.";
  if (!tool.multiple && files.length > 1) return "This tool accepts one file.";
  if (tool.minFiles && files.length < tool.minFiles) return `Select at least ${tool.minFiles} files.`;

  const wrongType = files.find((file) => {
    const name = (file.name || "").toLowerCase();
    return !tool.allowedExtensions.some((extension) => name.endsWith(extension));
  });
  if (wrongType) return `${wrongType.name} is not supported for ${tool.title}.`;

  const tooLarge = files.find((file) => file.size && file.size > MAX_FILE_SIZE_MB * 1024 * 1024);
  if (tooLarge) return `${tooLarge.name} exceeds ${MAX_FILE_SIZE_MB}MB.`;

  return "";
}

export function validateFields(tool, fields) {
  const missing = (tool.fields || []).find((field) => field.required && !String(fields[field.name] || "").trim());
  return missing ? `${missing.label} is required.` : "";
}

