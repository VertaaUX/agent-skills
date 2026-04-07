#!/usr/bin/env python3

from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "compatibility"
SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)

LOGOS = [
    "codex-text.svg",
    "claudecode-text.svg",
    "cursor-text.svg",
    "githubcopilot-text.svg",
    "geminicli-text.svg",
    "windsurf-text.svg",
    "cline-text.svg",
]


def parse_view_box(value: str) -> tuple[float, float, float, float]:
    parts = [float(x) for x in value.replace(",", " ").split()]
    return parts[0], parts[1], parts[2], parts[3]


def layout_positions(canvas_width: int, row1: int, row2: int, cell_width: int, gap: int, top_y: int, bottom_y: int):
    row1_width = row1 * cell_width + (row1 - 1) * gap
    row2_width = row2 * cell_width + (row2 - 1) * gap
    row1_start = (canvas_width - row1_width) / 2
    row2_start = (canvas_width - row2_width) / 2

    positions = []
    for index in range(row1):
        positions.append((row1_start + index * (cell_width + gap), top_y))
    for index in range(row2):
        positions.append((row2_start + index * (cell_width + gap), bottom_y))
    return positions


def build_svg(output_svg: Path, output_png: Path, color: str) -> None:
    canvas_width = 1600
    canvas_height = 320
    cell_width = 320
    cell_height = 78
    gap = 42
    positions = layout_positions(canvas_width, 4, 3, cell_width, gap, 44, 186)

    svg = ET.Element(
        f"{{{SVG_NS}}}svg",
        {
            "width": str(canvas_width),
            "height": str(canvas_height),
            "viewBox": f"0 0 {canvas_width} {canvas_height}",
            "fill": "none",
            "role": "img",
            "aria-labelledby": "title desc",
        },
    )
    ET.SubElement(svg, f"{{{SVG_NS}}}title", {"id": "title"}).text = "Compatibility hosts"
    ET.SubElement(svg, f"{{{SVG_NS}}}desc", {"id": "desc"}).text = "Large compatibility wordmarks for supported coding hosts."

    for (x, y), file_name in zip(positions, LOGOS):
        source = ET.parse(ASSETS / file_name).getroot()
        min_x, min_y, view_w, view_h = parse_view_box(source.attrib["viewBox"])

        scale = min(cell_width / view_w, cell_height / view_h)
        tx = x + (cell_width - view_w * scale) / 2 - min_x * scale
        ty = y + (cell_height - view_h * scale) / 2 - min_y * scale

        wrapper = ET.SubElement(
            svg,
            f"{{{SVG_NS}}}g",
            {
                "transform": f"translate({tx:.3f} {ty:.3f}) scale({scale:.6f})",
                "color": color,
                "fill": color,
                "stroke": color,
            },
        )

        for child in list(source):
            if child.tag in {f"{{{SVG_NS}}}title", f"{{{SVG_NS}}}desc"}:
                continue
            wrapper.append(child)

    ET.ElementTree(svg).write(output_svg, encoding="utf-8", xml_declaration=True)

    subprocess.run(
        [
            "inkscape",
            str(output_svg),
            "--export-type=png",
            f"--export-filename={output_png}",
            "--export-background-opacity=0",
        ],
        check=True,
    )


def main() -> None:
    build_svg(ASSETS / "compatibility-board-light.svg", ASSETS / "compatibility-board-light.png", "#111111")
    build_svg(ASSETS / "compatibility-board-dark.svg", ASSETS / "compatibility-board-dark.png", "#FFFFFF")


if __name__ == "__main__":
    main()
