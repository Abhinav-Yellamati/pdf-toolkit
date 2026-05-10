# Challenges Faced and Solutions Implemented

## Physical Phone Networking

Challenge: Expo Go could not reach `127.0.0.1`.

Solution: Added LAN-aware mobile API config and moved the backend to `0.0.0.0:8001`.

## React Native File Handling

Challenge: Browser APIs such as `FileReader` are not reliable in React Native.

Solution: Replaced browser-only file conversion with `arrayBuffer()` and base64 file writing through Expo FileSystem.

## Mobile Upload Compatibility

Challenge: React Native multipart uploads require `{ uri, name, type }` objects.

Solution: Added mobile-specific file payload normalization and MIME type fallback.

## Consistent Web and Mobile Features

Challenge: The same PDF tools had to work from two different clients.

Solution: Both clients use declarative tool configuration and call the same FastAPI endpoints.

## Temporary File Management

Challenge: PDF processing creates intermediate files.

Solution: Backend creates isolated workspaces and cleans them after the response.
