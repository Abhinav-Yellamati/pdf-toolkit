# Compression Analysis

## Method

Compression was tested through `POST /api/pdf/compress` using quality levels `35`, `55`, and `75`. Each output was reopened and page-count verified.

## Results

| Input | Quality | Original MB | Compressed MB | Reduction | Pages | Time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| text-small.pdf | 35 | 0.027 | 0.005 | 81.03% | 8 | 0.540s |
| text-small.pdf | 55 | 0.027 | 0.005 | 81.03% | 8 | 0.111s |
| text-small.pdf | 75 | 0.027 | 0.005 | 81.03% | 8 | 0.105s |
| image-heavy-small.pdf | 35 | 1.807 | 0.053 | 97.06% | 2 | 0.430s |
| image-heavy-small.pdf | 55 | 1.807 | 0.109 | 93.96% | 2 | 0.475s |
| image-heavy-small.pdf | 75 | 1.807 | 0.226 | 87.49% | 2 | 0.621s |
| image-heavy-medium.pdf | 35 | 7.215 | 0.007 | 99.90% | 4 | 1.782s |
| image-heavy-medium.pdf | 55 | 7.215 | 0.011 | 99.84% | 4 | 2.133s |
| image-heavy-medium.pdf | 75 | 7.215 | 0.033 | 99.55% | 4 | 2.480s |
| image-heavy-large.pdf | 35 | 56.540 | 1.826 | 96.77% | 4 | 3.667s |
| image-heavy-large.pdf | 55 | 56.540 | 2.653 | 95.31% | 4 | 3.912s |
| image-heavy-large.pdf | 75 | 56.540 | 4.404 | 92.21% | 4 | 4.748s |
| mixed-content.pdf | 35 | 1.812 | 0.008 | 99.56% | 6 | 0.709s |
| mixed-content.pdf | 55 | 1.812 | 0.010 | 99.45% | 6 | 0.813s |
| mixed-content.pdf | 75 | 1.812 | 0.020 | 98.92% | 6 | 1.003s |

## Quality Observations

- All compressed outputs reopened successfully and preserved page counts.
- Lower quality levels produced stronger size reduction.
- Image-heavy PDFs showed the largest optimization gains.
- Text-only PDFs were already small, but still reduced without corruption.
- First-page comparison screenshots were generated for each compressed result.

## Visual Evidence

- `test-assets/screenshots/compression-size-comparison.svg`
- `test-assets/screenshots/original-*.png`
- `test-assets/screenshots/compressed-*.png`
