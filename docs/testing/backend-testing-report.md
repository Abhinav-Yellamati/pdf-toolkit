# Backend Testing Report

## Scope

FastAPI endpoints were tested with generated realistic PDFs through the application router using FastAPI `TestClient`.

## Endpoint Results

| Endpoint | Result | Notes |
| --- | --- | --- |
| `GET /health` | Passed | HTTP 200 |
| `POST /api/pdf/compress` | Passed | 15 quality/asset combinations |
| `POST /api/pdf/merge` | Passed | 2-PDF, multi-PDF, and large mixed merge |
| `POST /api/pdf/split` | Passed | range, single-page, and large split cases |
| `POST /api/pdf/rearrange` | Passed | Reverse-order and mixed-selection cases |
| `POST /api/pdf/pdf-to-word` | Passed | `.docx` generated |
| `POST /api/pdf/pdf-to-image` | Passed | zip with page images generated |
| `POST /api/pdf/image-to-pdf` | Passed | 2-page PDF generated |
| `POST /api/pdf/watermark` | Passed | text watermark at 3 opacity levels |
| `POST /api/pdf/protect` | Passed | encrypted PDF rejects invalid password and opens with valid password |
| Invalid upload | Passed | HTTP 400 with clear message |
| CORS preflight | Passed | HTTP 200 with allow-origin header |
| Concurrent uploads | Passed | 8/8 compression requests returned HTTP 200 |

## Merge Validation

| Case | Expected Pages | Actual Pages | Output |
| --- | ---: | ---: | --- |
| merge-2-pdfs.pdf | 14 | 14 | 1.879 MB |
| merge-multi-pdfs.pdf | 36 | 36 | 7.489 MB |
| merge-large-mixed.pdf | 8 | 8 | 63.755 MB |

## Split Validation

| Case | Ranges | Zip Entries | Output |
| --- | --- | ---: | --- |
| split-ranges | `1-3,5,7-8` | 3 | 0.015 MB |
| split-single-pages | single pages | 8 | 0.031 MB |
| split-large | `1-2,3-4` | 2 | 14.431 MB |

## Rearrange Validation

| Case | Order | Expected Pages | Actual Pages | Output |
| --- | --- | ---: | ---: | --- |
| rearrange-reverse-text-small.pdf | `8,7,6,5,4,3,2,1` | 8 | 8 | 0.067 MB |
| rearrange-mixed-selection.pdf | `2,4,6,1` | 4 | 4 | 1.810 MB |

## Notes

- No unhandled backend exception occurred in automated testing.
- The invalid upload path correctly returned a handled HTTP 400.
- Image watermarking is not implemented by the current API and should be documented as future scope.
- Rearrange is now covered by direct API execution and output page-count validation.
