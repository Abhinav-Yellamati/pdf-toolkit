# Challenges Faced

- Mobile devices cannot reliably call `localhost` on the development computer, so LAN IP configuration is required.
- Expo and Metro can cache stale JavaScript bundles, which makes runtime fixes appear incomplete until the cache is cleared.
- File upload APIs need careful multipart form handling for both browser and mobile clients.
- Large PDF files can increase processing time and memory usage.
- Some PDFs are password protected or malformed, so validation and clear error handling are necessary.
- Download behavior differs between web browsers and mobile environments.

