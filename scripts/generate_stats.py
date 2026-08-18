#!/usr/bin/env python3
"""Generate compact, accurate profile stats SVGs from owned original repos."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATS = ROOT / "stats"

# Snapshot taken 2026-08-18 from GitHub API (owned original repos, including private).
STATS_DATA = {
    "public_repos": 58,
    "private_originals": 46,
    "original_repos": 55,
    "stars": 4,
    "followers": 2,
    "years": 14,
}

# Language bytes aggregated from repos/bpzhang/*/languages (originals only, forks excluded).
LANG_BYTES = [
    ("Java", 68761270, "#b07219"),
    ("JavaScript", 9767559, "#f1e05a"),
    ("TSQL", 4174851, "#e38c00"),
    ("TypeScript", 3869043, "#3178c6"),
    ("Python", 2563402, "#3572a5"),
    ("CSS", 1397437, "#563d7c"),
    ("Vue", 1319149, "#41b883"),
    ("Go", 1033715, "#00add8"),
]
LANG_TOTAL = 94486924
LANG_LIMIT = 8

TITLE = "#2E9EF7"
TEXT = "#434d58"
MUTED = "#8b949e"
BG = "#fffefe"
BORDER = "#e4e2e2"
BAR_BG = "#eaeaea"


def esc(s):
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def stats_svg():
    rows = [
        ("Public Repos", STATS_DATA["public_repos"]),
        ("Private Originals", STATS_DATA["private_originals"]),
        ("Original Repos", STATS_DATA["original_repos"]),
        ("Stars", STATS_DATA["stars"]),
        ("Followers", STATS_DATA["followers"]),
        ("Years on GitHub", STATS_DATA["years"]),
    ]
    width, height = 420, 155
    items = []
    for i, (label, value) in enumerate(rows):
        col, row = i % 2, i // 2
        x = 24 + col * 200
        y = 62 + row * 34
        items.append(
            f'<text x="{x}" y="{y}" fill="{TEXT}" font-size="13">{esc(label)}</text>'
            f'<text x="{x + 168}" y="{y}" fill="{TEXT}" font-size="13" font-weight="700" text-anchor="end">{esc(value)}</text>'
        )
    body = "\n  ".join(items)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="GitHub stats">
  <style>
    text {{ font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif; }}
  </style>
  <rect width="{width}" height="{height}" rx="8" fill="{BG}" stroke="{BORDER}"/>
  <text x="24" y="32" fill="{TITLE}" font-size="16" font-weight="700">GitHub Stats</text>
  <text x="396" y="32" fill="{MUTED}" font-size="10" text-anchor="end">includes private originals</text>
  {body}
</svg>
'''


def languages_svg():
    top = LANG_BYTES[:LANG_LIMIT]
    width, row_h, header = 420, 22, 48
    height = header + len(top) * row_h + 20
    lines = []
    for i, (name, n, color) in enumerate(top):
        pct = 100.0 * n / LANG_TOTAL
        y = header + i * row_h
        bar_w = min(220, max(4, round(220 * n / top[0][1])))
        lines.append(
            f'<text x="24" y="{y + 12}" fill="{TEXT}" font-size="12">{esc(name)}</text>'
            f'<rect x="130" y="{y + 2}" width="220" height="10" rx="5" fill="{BAR_BG}"/>'
            f'<rect x="130" y="{y + 2}" width="{bar_w}" height="10" rx="5" fill="{color}"/>'
            f'<text x="396" y="{y + 12}" fill="{TEXT}" font-size="12" text-anchor="end">{pct:.1f}%</text>'
        )
    body = "\n  ".join(lines)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Top languages">
  <style>
    text {{ font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif; }}
  </style>
  <rect width="{width}" height="{height}" rx="8" fill="{BG}" stroke="{BORDER}"/>
  <text x="24" y="32" fill="{TITLE}" font-size="16" font-weight="700">Top Languages</text>
  <text x="396" y="32" fill="{MUTED}" font-size="10" text-anchor="end">by bytes, includes private</text>
  {body}
</svg>
'''


def main():
    STATS.mkdir(exist_ok=True)
    (STATS / "github-stats.svg").write_text(stats_svg(), encoding="utf-8")
    (STATS / "languages.svg").write_text(languages_svg(), encoding="utf-8")
    print("wrote", STATS / "github-stats.svg")
    print("wrote", STATS / "languages.svg")


if __name__ == "__main__":
    main()
