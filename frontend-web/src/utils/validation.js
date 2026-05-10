import { MAX_FILE_COUNT, MAX_FILE_SIZE_MB } from "../config/tools";

export function validateFilesForTool(tool, files) {
  if (!files.length) return "Choose at least one file.";
  if (!tool.multiple && files.length > 1) return "This tool accepts one file.";
  if (tool.minFiles && files.length < tool.minFiles) return `Upload at least ${tool.minFiles} files.`;
  if (files.length > MAX_FILE_COUNT) return `Upload up to ${MAX_FILE_COUNT} files at once.`;

  const tooLarge = files.find((file) => file.size > MAX_FILE_SIZE_MB * 1024 * 1024);
  if (tooLarge) return `${tooLarge.name} is larger than ${MAX_FILE_SIZE_MB}MB.`;

  const wrongType = files.find((file) => {
    const lowerName = file.name.toLowerCase();
    return !tool.allowedExtensions?.some((extension) => lowerName.endsWith(extension));
  });
  if (wrongType) return `${wrongType.name} is not supported for ${tool.title}.`;

  return "";
}

export function validateRequiredFields(tool, fields) {
  const missingField = (tool.fields || []).find((field) => field.required && !String(fields[field.name] || "").trim());
  return missingField ? `${missingField.label} is required.` : "";
}

