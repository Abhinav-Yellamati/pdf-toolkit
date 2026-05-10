# Common Issues and Solutions

## Why did Expo Go show `Something went wrong`?

The crash happened after runtime configuration changes. Metro could bundle the app, so the problem was likely runtime module evaluation or an unsupported runtime value. The API config was hardened and an error boundary was added.

## Why does mobile need a LAN IP?

On a physical phone, `127.0.0.1` means the phone itself. The backend runs on the laptop, so the app must use the laptop LAN IP.

## Why not process PDFs on the phone?

PDF processing is CPU and memory intensive. Keeping it on the backend improves mobile performance and keeps native dependencies simple.

## How are upload failures handled?

The mobile service wraps requests with timeout handling, logs request context, and shows actionable messages that include backend reachability guidance.

## How is architecture preserved?

The fixes only add safety, logging, and documentation. The existing UI, APIs, backend routes, and feature set remain unchanged.
