# Viva Preparation Notes

## Why React?

React is suitable for this project because the UI is state-driven. Tool selection, upload state, progress, validation messages, and result cards are all naturally represented as React state.

## Why FastAPI?

FastAPI provides clear route definitions, async request handling, automatic validation support, and good performance for API services. It is simple to connect with Python PDF libraries.

## Why Expo?

Expo reduces React Native setup complexity and allows fast physical-phone testing through Expo Go. It also provides useful APIs such as document picking, file system access, and native sharing.

## Why PyMuPDF?

PyMuPDF is fast and capable for PDF rendering, image extraction, compression-related operations, watermarking, and conversion workflows.

## Why pypdf?

pypdf is useful for structural PDF operations such as merging, splitting, rearranging pages, and encryption.

## Compression Strategy

The compression tool removes metadata, recompresses images with controlled JPEG quality, optionally resizes large images, and saves the PDF with cleanup and deflate options.

## API Architecture

The API exposes one endpoint per tool. Each endpoint accepts multipart form data, validates input, calls one service function, and returns a generated file.

## Mobile and Web Integration

Both clients use the same API contract. The web client downloads blobs with browser APIs, while the mobile client writes returned binary data to Expo cache and shares it with native APIs.

## Key Explanation for Demo

The architecture separates interface, transport, and processing. This makes the project easier to maintain and explain.
