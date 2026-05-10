# Performance Report

## Summary

| Metric | Result |
| --- | ---: |
| Total automated QA runtime | 39.918s |
| Largest generated PDF | 56.54 MB |
| Compression cases | 15 |
| Concurrent upload requests | 8 |
| Concurrent upload total time | 0.553s |
| Web production build | Passed |
| Expo Android export | Passed |

## Backend Timing Highlights

| Operation | Representative Case | Time |
| --- | --- | ---: |
| Compress | 56.54 MB PDF at quality 75 | 4.748s |
| Merge | 63.755 MB merged output | 1.807s |
| Rearrange | reverse 8-page text PDF | 0.111s |
| Split | image-heavy medium split | 1.749s |
| PDF to Image | 6-page mixed PDF | 3.743s |
| Image to PDF | 2 PNG files | 1.272s |
| Watermark | 25-page text watermark | 0.221s to 0.238s |
| Password Protect | 8-page text PDF | 0.339s |

## Concurrent Uploads

Eight parallel compression requests returned HTTP 200. Individual responses were approximately `0.243s` to `0.276s`, with latest total concurrent time `0.623s`.

## Bottlenecks

- PDF-to-image conversion and large image-heavy compression are the slowest workflows because they render or recompress raster content.
- Very large PDFs should use visible progress indicators in the frontend/mobile clients.
- Physical mobile upload speed depends on LAN quality and still needs device validation.

## Improvements Confirmed

- Threadpool execution prevents PDF processing functions from blocking the FastAPI async route handler directly.
- Temporary workspace cleanup runs after file responses.
- Compression settings cap quality values to avoid extreme processing configurations.
