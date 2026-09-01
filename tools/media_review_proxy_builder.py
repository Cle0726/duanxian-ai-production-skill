#!/usr/bin/env python3
"""Inventory visual files, then build bounded review proxies and contact sheets.

The script deliberately separates the metadata pass from the render pass. It never
changes source assets and records absolute source/proxy paths plus SHA-256 lineage.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont, ImageOps


SUPPORTED = {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff", ".bmp"}


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def collect_files(inputs: Iterable[Path], output_dir: Path) -> list[Path]:
    output_resolved = output_dir.resolve()
    files: set[Path] = set()
    for item in inputs:
        item = item.resolve()
        if item.is_file() and item.suffix.lower() in SUPPORTED:
            files.add(item)
        elif item.is_dir():
            for path in item.rglob("*"):
                if not path.is_file() or path.suffix.lower() not in SUPPORTED:
                    continue
                try:
                    path.resolve().relative_to(output_resolved)
                    continue
                except ValueError:
                    files.add(path.resolve())
    return sorted(files, key=lambda p: str(p).casefold())


def inspect_file(path: Path) -> dict:
    stat = path.stat()
    with Image.open(path) as image:
        width, height = image.size
        detected_format = image.format or path.suffix.lstrip(".").upper()
        mode = image.mode
    return {
        "source_path": str(path.resolve()),
        "relative_display_path": path.name,
        "extension": path.suffix.lower(),
        "detected_format": detected_format,
        "width": width,
        "height": height,
        "long_edge": max(width, height),
        "mode": mode,
        "bytes": stat.st_size,
        "modified_at": stat.st_mtime,
        "sha256": sha256_file(path),
    }


def write_inventory(records: list[dict], output_dir: Path, roots: list[Path]) -> None:
    payload = {
        "protocol": "MEDIA_REVIEW_PROXY_FIRST_V1",
        "phase": "METADATA_INVENTORY_COMPLETE_BEFORE_PROXY_RENDER",
        "roots": [str(p.resolve()) for p in roots],
        "count": len(records),
        "files": records,
    }
    (output_dir / "inventory.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    with (output_dir / "inventory.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        fields = [
            "source_path", "detected_format", "width", "height", "long_edge",
            "mode", "bytes", "sha256", "modified_at",
        ]
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)
    tree_lines = [f"ROOT {p.resolve()}" for p in roots]
    tree_lines.extend(f"FILE {r['source_path']}" for r in records)
    (output_dir / "directory_tree.txt").write_text("\n".join(tree_lines) + "\n", encoding="utf-8")


def flatten_for_rgb(image: Image.Image) -> Image.Image:
    image = ImageOps.exif_transpose(image)
    if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
        rgba = image.convert("RGBA")
        background = Image.new("RGBA", rgba.size, "white")
        return Image.alpha_composite(background, rgba).convert("RGB")
    return image.convert("RGB")


def proxy_name(record: dict, output_format: str) -> str:
    safe_stem = Path(record["source_path"]).stem
    return f"{safe_stem}__{record['sha256'][:12]}__review.{output_format}"


def build_proxy(record: dict, proxy_dir: Path, max_edge: int, output_format: str, quality: int) -> dict:
    source = Path(record["source_path"])
    destination = (proxy_dir / proxy_name(record, output_format)).resolve()
    with Image.open(source) as image:
        image = flatten_for_rgb(image)
        scale = min(1.0, max_edge / max(image.size))
        size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
        if size != image.size:
            image = image.resize(size, Image.Resampling.LANCZOS)
        save_format = "JPEG" if output_format in {"jpg", "jpeg"} else "WEBP"
        image.save(destination, format=save_format, quality=quality, optimize=True)
    record.update({
        "proxy_path": str(destination),
        "proxy_width": size[0],
        "proxy_height": size[1],
        "proxy_long_edge": max(size),
        "proxy_format": output_format.upper(),
        "proxy_sha256": sha256_file(destination),
    })
    return record


def fit_text(draw: ImageDraw.ImageDraw, text_value: str, width: int, font: ImageFont.ImageFont) -> str:
    text_value = text_value.replace("\n", " ")
    if draw.textlength(text_value, font=font) <= width:
        return text_value
    suffix = "..."
    while text_value and draw.textlength(text_value + suffix, font=font) > width:
        text_value = text_value[:-1]
    return text_value + suffix


def build_contact_sheets(records: list[dict], output_dir: Path, max_edge: int, per_sheet: int, columns: int) -> list[dict]:
    sheets: list[dict] = []
    font = ImageFont.load_default()
    for page_index in range(math.ceil(len(records) / per_sheet)):
        page_records = records[page_index * per_sheet:(page_index + 1) * per_sheet]
        cols = min(columns, len(page_records))
        rows = math.ceil(len(page_records) / cols)
        cell_w, cell_h, label_h, gutter = 360, 250, 38, 10
        canvas = Image.new("RGB", (cols * cell_w, rows * (cell_h + label_h)), "#202124")
        draw = ImageDraw.Draw(canvas)
        item_refs = []
        for idx, record in enumerate(page_records):
            col, row = idx % cols, idx // cols
            x, y = col * cell_w, row * (cell_h + label_h)
            with Image.open(record["proxy_path"]) as proxy:
                tile = proxy.convert("RGB")
                tile.thumbnail((cell_w - 2 * gutter, cell_h - 2 * gutter), Image.Resampling.LANCZOS)
                px = x + (cell_w - tile.width) // 2
                py = y + (cell_h - tile.height) // 2
                canvas.paste(tile, (px, py))
            label = f"{page_index * per_sheet + idx + 1:02d} {Path(record['source_path']).name}"
            draw.text((x + gutter, y + cell_h + 5), fit_text(draw, label, cell_w - 2 * gutter, font), fill="white", font=font)
            item_refs.append({"index": page_index * per_sheet + idx + 1, "source_path": record["source_path"], "proxy_path": record["proxy_path"]})
        scale = min(1.0, max_edge / max(canvas.size))
        if scale < 1.0:
            canvas = canvas.resize((round(canvas.width * scale), round(canvas.height * scale)), Image.Resampling.LANCZOS)
        sheet_path = (output_dir / f"contact_sheet_{page_index + 1:02d}.jpg").resolve()
        canvas.save(sheet_path, "JPEG", quality=90, optimize=True)
        sheets.append({
            "sheet_path": str(sheet_path),
            "width": canvas.width,
            "height": canvas.height,
            "long_edge": max(canvas.size),
            "sha256": sha256_file(sheet_path),
            "items": item_refs,
        })
    return sheets


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path, help="Image files or directories to inventory recursively")
    parser.add_argument("--output", required=True, type=Path, help="Review package output directory")
    parser.add_argument("--max-edge", type=int, default=1600)
    parser.add_argument("--format", choices=("jpg", "webp"), default="jpg")
    parser.add_argument("--quality", type=int, default=90)
    parser.add_argument("--per-sheet", type=int, default=12)
    parser.add_argument("--columns", type=int, default=4)
    args = parser.parse_args()
    if not 1 <= args.max_edge <= 1600:
        parser.error("--max-edge must be between 1 and 1600")
    if args.per_sheet < 1 or args.columns < 1:
        parser.error("--per-sheet and --columns must be positive")

    output_dir = args.output.resolve()
    proxy_dir = output_dir / "proxies"
    proxy_dir.mkdir(parents=True, exist_ok=True)
    files = collect_files(args.inputs, output_dir)
    if not files:
        parser.error("no supported image files found")

    # Phase 1 must complete and persist before any proxy pixels are rendered.
    records = [inspect_file(path) for path in files]
    write_inventory(records, output_dir, args.inputs)

    # Phase 2 renders bounded derivatives only; originals remain unchanged.
    records = [build_proxy(r, proxy_dir, args.max_edge, args.format, args.quality) for r in records]
    sheets = build_contact_sheets(records, output_dir, args.max_edge, args.per_sheet, args.columns)
    manifest = {
        "protocol": "MEDIA_REVIEW_PROXY_FIRST_V1",
        "source_count": len(records),
        "max_review_long_edge": args.max_edge,
        "sources_immutable": True,
        "contact_sheet_role": "TRIAGE_ONLY_NOT_FINAL_ASSET_ACCEPTANCE",
        "individual_asset_acceptance_requires": "OPEN_THE_SELECTED_INDIVIDUAL_PROXY",
        "files": records,
        "contact_sheets": sheets,
    }
    manifest_path = output_dir / "review_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "inventory": str((output_dir / "inventory.json").resolve()),
        "review_manifest": str(manifest_path.resolve()),
        "contact_sheets": [s["sheet_path"] for s in sheets],
        "source_count": len(records),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
