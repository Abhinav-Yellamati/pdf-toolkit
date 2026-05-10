# QA Summary

## Test Assets

| file | size_mb | pages |
| --- | --- | --- |
| image-heavy-large.pdf | 56.54 | 4 |
| image-heavy-medium.pdf | 7.215 | 4 |
| image-heavy-small.pdf | 1.807 | 2 |
| mixed-content.pdf | 1.812 | 6 |
| multi-page.pdf | 0.072 | 25 |
| scanned-sample.pdf | 7.215 | 3 |
| text-medium.pdf | 0.151 | 55 |
| text-small.pdf | 0.027 | 8 |

## Compression

| input | quality | status | original_mb | compressed_mb | reduction_percent | pages | seconds | readable | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| text-small.pdf | 35 | 200 | 0.027 | 0.005 | 81.03 | 8 | 0.302 | True | Readable output |
| text-small.pdf | 55 | 200 | 0.027 | 0.005 | 81.03 | 8 | 0.083 | True | Readable output |
| text-small.pdf | 75 | 200 | 0.027 | 0.005 | 81.03 | 8 | 0.065 | True | Readable output |
| image-heavy-small.pdf | 35 | 200 | 1.807 | 0.053 | 97.06 | 2 | 0.25 | True | Readable output |
| image-heavy-small.pdf | 55 | 200 | 1.807 | 0.109 | 93.96 | 2 | 0.285 | True | Readable output |
| image-heavy-small.pdf | 75 | 200 | 1.807 | 0.226 | 87.49 | 2 | 0.38 | True | Readable output |
| image-heavy-medium.pdf | 35 | 200 | 7.215 | 0.007 | 99.9 | 4 | 1.34 | True | Readable output |
| image-heavy-medium.pdf | 55 | 200 | 7.215 | 0.011 | 99.84 | 4 | 1.338 | True | Readable output |
| image-heavy-medium.pdf | 75 | 200 | 7.215 | 0.033 | 99.55 | 4 | 1.573 | True | Readable output |
| image-heavy-large.pdf | 35 | 200 | 56.54 | 1.826 | 96.77 | 4 | 2.348 | True | Readable output |
| image-heavy-large.pdf | 55 | 200 | 56.54 | 2.653 | 95.31 | 4 | 2.587 | True | Readable output |
| image-heavy-large.pdf | 75 | 200 | 56.54 | 4.404 | 92.21 | 4 | 2.887 | True | Readable output |
| mixed-content.pdf | 35 | 200 | 1.812 | 0.008 | 99.56 | 6 | 0.41 | True | Readable output |
| mixed-content.pdf | 55 | 200 | 1.812 | 0.01 | 99.45 | 6 | 0.458 | True | Readable output |
| mixed-content.pdf | 75 | 200 | 1.812 | 0.02 | 98.92 | 6 | 0.583 | True | Readable output |

## Merge

| case | inputs | status | expected_pages | actual_pages | page_order_valid | output_mb | seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| merge-2-pdfs.pdf | text-small.pdf, mixed-content.pdf | 200 | 14 | 14 | True | 1.879 | 0.172 |
| merge-multi-pdfs.pdf | text-small.pdf, multi-page.pdf, scanned-sample.pdf | 200 | 36 | 36 | True | 7.489 | 0.365 |
| merge-large-mixed.pdf | image-heavy-medium.pdf, image-heavy-large.pdf | 200 | 8 | 8 | True | 63.755 | 1.645 |

## Rearrange

| case | input | order | status | expected_pages | actual_pages | output_mb | seconds | valid |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rearrange-reverse-text-small.pdf | text-small.pdf | 8,7,6,5,4,3,2,1 | 200 | 8 | 8 | 0.067 | 0.082 | True |
| rearrange-mixed-selection.pdf | mixed-content.pdf | 2,4,6,1 | 200 | 4 | 4 | 1.81 | 0.127 | True |

## Split

| case | input | ranges | status | zip_entries | output_mb | seconds | entries |
| --- | --- | --- | --- | --- | --- | --- | --- |
| split-ranges | multi-page.pdf | 1-3,5,7-8 | 200 | 3 | 0.015 | 0.242 | split_1.pdf, split_2.pdf, split_3.pdf |
| split-single-pages | text-small.pdf | single pages | 200 | 8 | 0.031 | 0.291 | split_1.pdf, split_2.pdf, split_3.pdf, split_4.pdf, split_5.pdf, split_6.pdf, split_7.pdf, split_8.pdf |
| split-large | image-heavy-medium.pdf | 1-2,3-4 | 200 | 2 | 14.431 | 1.236 | split_1.pdf, split_2.pdf |

## Conversions

| case | status | output | output_mb | seconds | observations |
| --- | --- | --- | --- | --- | --- |
| /api/pdf/pdf-to-word | 200 | mixed-content.docx | 0.001 | 0.079 | File generated |
| /api/pdf/pdf-to-image | 200 | mixed-content-images.zip | 13.716 | 1.911 | page_1.png, page_2.png, page_3.png, page_4.png, page_5.png, page_6.png |
| /api/pdf/image-to-pdf | 200 | images-to-pdf.pdf | 9.019 | 0.725 | pages=2 |

## Watermark

| case | status | pages | output_mb | seconds | observations |
| --- | --- | --- | --- | --- | --- |
| text opacity 0.1 | 200 | 25 | 0.017 | 0.134 | Text watermark applied |
| text opacity 0.35 | 200 | 25 | 0.017 | 0.125 | Text watermark applied |
| text opacity 0.7 | 200 | 25 | 0.017 | 0.132 | Text watermark applied |
| image watermark | not implemented | 0 | 0 | 0 | Current API supports text watermark only; image watermark endpoint is not present. |

## Password

| case | status | encrypted | invalid_password_result | valid_password_result | pages_after_unlock | output_mb | seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| add password | 200 | True | 0 | 2 | 8 | 0.067 | 0.182 |

## Backend

| case | status | seconds | observations |
| --- | --- | --- | --- |
| invalid upload | 400 | 0.006 | {"detail":"Please upload a PDF file."} |
| cors preflight | 200 | 0 | {'vary': 'Origin', 'access-control-allow-methods': 'DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT', 'access-control-max-age': '600', 'access-control-allow-credentials': 'true', 'access-control-allow-origin': 'http://localhost:3000', 'content-length': '2', 'content-type': 'text/plain; charset=utf-8', 'x-content-type-options': 'nosniff', 'x-frame-options': 'DENY', 'referrer-policy': 'strict-origin-when-cross-origin', 'permissions-policy': 'camera=(), microphone=(), geolocation=()'} |
| health | 200 | 0.006 | {"status":"healthy"} |

## Concurrent Uploads

| request | status | seconds | bytes |
| --- | --- | --- | --- |
| 1 | 200 | 0.338 | 5351 |
| 3 | 200 | 0.444 | 5351 |
| 2 | 200 | 0.445 | 5351 |
| 4 | 200 | 0.444 | 5351 |
| 5 | 200 | 0.268 | 5351 |
| 6 | 200 | 0.16 | 5351 |
| 7 | 200 | 0.196 | 5351 |
| 8 | 200 | 0.199 | 5351 |

Concurrent total seconds: 0.649
