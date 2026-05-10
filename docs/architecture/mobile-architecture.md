# Mobile Architecture

The mobile app is an Expo React Native client for the same FastAPI backend used by the web app.

## Layers

```text
App.js
  components/
  config/
  services/
  utils/
```

## Responsibilities

- `App.js`: screen state, tool selection, progress, result state.
- `components/`: reusable mobile UI pieces.
- `config/api.js`: safe LAN-aware API configuration.
- `config/tools.js`: declarative tool definitions.
- `services/api.js`: upload, timeout, binary response handling, sharing.
- `utils/logger.js`: runtime diagnostics.
- `utils/validation.js`: client-side validation.

## Error Handling

The app has an `ErrorBoundary` at the root. API failures are handled as user-friendly toast messages. Runtime details are printed to the Expo console for debugging.

## Expo And Networking Notes

The mobile app must use a reachable backend URL. On a physical phone, `localhost` points to the phone itself, not the development computer. Use the computer LAN IP in `EXPO_PUBLIC_API_BASE_URL`, and record any LAN, WSL, ngrok, tunnel, Metro, or Expo runtime issue in `logs/mobile-runtime.log` and `docs/debugging/debugging-timeline.md`.
