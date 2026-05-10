# Viva Questions

## What problem does this project solve?

It provides a single toolkit for common PDF operations through web and mobile interfaces.

## Why use FastAPI?

FastAPI provides a clean way to build typed HTTP APIs, validate requests, return files, and document endpoints.

## Why use PyMuPDF and pypdf?

PyMuPDF is useful for rendering, compression, image extraction, and watermarking. pypdf is suitable for structural PDF operations such as merging, splitting, rearranging, and encryption.

## Why is the backend needed?

PDF processing can be heavy and requires reliable file-system and library support. Keeping it on the backend avoids duplicating complex logic in web and mobile clients.

## How does mobile communicate with backend?

The Expo app sends HTTP requests to the backend LAN URL. A physical phone must use the computer IP address instead of `localhost`.

## How are errors handled?

The backend validates file type, count, page ranges, password length, and encrypted PDFs. It returns clear HTTP errors for invalid input and a generic message for unexpected failures.

