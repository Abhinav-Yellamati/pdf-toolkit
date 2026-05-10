import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "test-assets" / "reports"
SCREENSHOTS = ROOT / "test-assets" / "screenshots"
SCREENSHOTS.mkdir(parents=True, exist_ok=True)


def read_csv(name):
    with (REPORTS / name).open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def bar_svg(title, rows, label_key, value_keys, colors, path):
    width = 1100
    row_h = 44
    left = 250
    top = 70
    max_val = max(float(row[key]) for row in rows for key in value_keys)
    height = top + len(rows) * row_h + 70
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="30" y="38" font-family="Arial" font-size="24" font-weight="700" fill="#111827">{title}</text>',
    ]
    for i, row in enumerate(rows):
        y = top + i * row_h
        parts.append(f'<text x="30" y="{y + 21}" font-family="Arial" font-size="13" fill="#374151">{row[label_key]}</text>')
        for j, key in enumerate(value_keys):
            value = float(row[key])
            bar_w = 760 * (value / max_val) if max_val else 0
            bar_y = y + 4 + j * 17
            parts.append(f'<rect x="{left}" y="{bar_y}" width="{bar_w:.1f}" height="14" rx="3" fill="{colors[j]}"/>')
            parts.append(f'<text x="{left + bar_w + 8:.1f}" y="{bar_y + 11}" font-family="Arial" font-size="11" fill="#111827">{value:.2f} MB</text>')
    legend_y = height - 30
    for j, key in enumerate(value_keys):
        x = 30 + j * 170
        parts.append(f'<rect x="{x}" y="{legend_y - 12}" width="16" height="12" fill="{colors[j]}"/>')
        parts.append(f'<text x="{x + 24}" y="{legend_y - 2}" font-family="Arial" font-size="12" fill="#374151">{key}</text>')
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def summary_svg(path):
    cards = [
        ("Backend feature cases", "30", "#2563eb"),
        ("Backend API failures", "0", "#16a34a"),
        ("Largest generated PDF", "56.54 MB", "#9333ea"),
        ("Concurrent uploads", "8/8 pass", "#ea580c"),
        ("Web build", "Pass", "#16a34a"),
        ("Expo Android export", "Pass", "#16a34a"),
    ]
    width = 1000
    height = 360
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#f8fafc"/>',
        '<text x="32" y="44" font-family="Arial" font-size="26" font-weight="700" fill="#111827">PDF Toolkit QA Result Summary</text>',
    ]
    for i, (label, value, color) in enumerate(cards):
        col = i % 3
        row = i // 3
        x = 32 + col * 312
        y = 78 + row * 120
        parts.append(f'<rect x="{x}" y="{y}" width="280" height="92" rx="8" fill="#ffffff" stroke="#d1d5db"/>')
        parts.append(f'<text x="{x + 18}" y="{y + 36}" font-family="Arial" font-size="26" font-weight="700" fill="{color}">{value}</text>')
        parts.append(f'<text x="{x + 18}" y="{y + 66}" font-family="Arial" font-size="14" fill="#374151">{label}</text>')
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def main():
    compression = read_csv("compression-results.csv")
    selected = [row for row in compression if row["quality"] == "55"]
    bar_svg(
        "Original vs Compressed Size at Quality 55",
        selected,
        "input",
        ["original_mb", "compressed_mb"],
        ["#94a3b8", "#2563eb"],
        SCREENSHOTS / "compression-size-comparison.svg",
    )
    merge = read_csv("merge-results.csv")
    bar_svg(
        "Merge Output Size Comparison",
        merge,
        "case",
        ["output_mb"],
        ["#7c3aed"],
        SCREENSHOTS / "merge-output-size-comparison.svg",
    )
    summary_svg(SCREENSHOTS / "qa-result-summary.svg")


if __name__ == "__main__":
    main()
