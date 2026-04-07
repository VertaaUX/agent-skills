#!/usr/bin/env python3
"""Render banner.txt (ANSI Shadow ASCII art) to a flattened banner.svg.

Reads banner.txt from the repo root, converts every supported character
into SVG <rect> primitives on a 19.2 x 42.24 grid (matching the FIGlet
ANSI Shadow font cell), and writes banner.svg.

Supported characters:
  space  (empty)
  full block      "\u2588"
  upper half      "\u2580"
  lower half      "\u2584"
  double horiz    "\u2550"
  double vert     "\u2551"
  double corners  "\u2554" "\u2557" "\u255a" "\u255d"
"""
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "banner.txt"
OUT = REPO / "banner.svg"

CW = 19.2          # cell width
CH = 42.24         # cell height
HH = CH / 2        # half height
T = 3.2            # thin line thickness for double-line glyphs
OVERLAP = 0.3      # extend block rects to hide AA seams between adjacent cells

# Double-line stroke positions inside a cell (centered pairs)
VL_LEFT = 4.8      # ║ left line x
VL_RIGHT = 11.2    # ║ right line x
HL_TOP = 16.0      # ═ top line y
HL_BOTTOM = 23.04  # ═ bottom line y

# Background and foreground
BG = "#0D1117"
FG = "#12FFF7"

# Margins around the text block
PAD_X = 50
PAD_Y = 30


def glyph_rects(ch):
    """Return list of (x, y, w, h) rects for a character, relative to cell origin."""
    if ch == " ":
        return []
    if ch == "\u2588":  # █ full block
        return [(0, 0, CW + OVERLAP, CH + OVERLAP)]
    if ch == "\u2580":  # ▀ upper half
        return [(0, 0, CW + OVERLAP, HH + OVERLAP)]
    if ch == "\u2584":  # ▄ lower half
        return [(0, HH, CW + OVERLAP, HH + OVERLAP)]
    if ch == "\u2550":  # ═ double horizontal
        return [
            (0, HL_TOP, CW, T),
            (0, HL_BOTTOM, CW, T),
        ]
    if ch == "\u2551":  # ║ double vertical
        return [
            (VL_LEFT, 0, T, CH),
            (VL_RIGHT, 0, T, CH),
        ]
    if ch == "\u2554":  # ╔ top-left double corner
        return [
            # outer L (upper-left of the double pair)
            (VL_LEFT, HL_TOP, T, CH - HL_TOP),                 # vertical down
            (VL_LEFT, HL_TOP, CW - VL_LEFT, T),                # horizontal right
            # inner L (lower-right of the double pair)
            (VL_RIGHT, HL_BOTTOM, T, CH - HL_BOTTOM),
            (VL_RIGHT, HL_BOTTOM, CW - VL_RIGHT, T),
        ]
    if ch == "\u2557":  # ╗ top-right double corner
        return [
            (VL_RIGHT, HL_TOP, T, CH - HL_TOP),
            (0, HL_TOP, VL_RIGHT + T, T),
            (VL_LEFT, HL_BOTTOM, T, CH - HL_BOTTOM),
            (0, HL_BOTTOM, VL_LEFT + T, T),
        ]
    if ch == "\u255a":  # ╚ bottom-left double corner
        return [
            (VL_LEFT, 0, T, HL_BOTTOM + T),
            (VL_LEFT, HL_BOTTOM, CW - VL_LEFT, T),
            (VL_RIGHT, 0, T, HL_TOP + T),
            (VL_RIGHT, HL_TOP, CW - VL_RIGHT, T),
        ]
    if ch == "\u255d":  # ╝ bottom-right double corner
        return [
            (VL_RIGHT, 0, T, HL_BOTTOM + T),
            (0, HL_BOTTOM, VL_RIGHT + T, T),
            (VL_LEFT, 0, T, HL_TOP + T),
            (0, HL_TOP, VL_LEFT + T, T),
        ]
    raise ValueError(f"unsupported char: {ch!r}")


def render(text):
    lines = text.splitlines()
    cols = max((len(l) for l in lines), default=0)
    rows = len(lines)

    width = int(round(cols * CW + 2 * PAD_X))
    height = int(round(rows * CH + 2 * PAD_Y))

    rects = []
    for r, line in enumerate(lines):
        for c, ch in enumerate(line):
            ox = PAD_X + c * CW
            oy = PAD_Y + r * CH
            for x, y, w, h in glyph_rects(ch):
                rects.append((ox + x, oy + y, w, h))

    # Emit SVG
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        f'  <rect width="{width}" height="{height}" fill="{BG}"/>',
        f'  <g fill="{FG}">',
    ]
    for x, y, w, h in rects:
        parts.append(
            f'    <rect x="{x:.2f}" y="{y:.2f}" '
            f'width="{w:.2f}" height="{h:.2f}"/>'
        )
    parts.append("  </g>")
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main():
    text = SRC.read_text(encoding="utf-8")
    OUT.write_text(render(text), encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
