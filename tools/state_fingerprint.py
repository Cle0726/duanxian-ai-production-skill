#!/usr/bin/env python3
"""Compute a stable SHA-256 fingerprint for YAML/JSON structured state.

This fingerprint proves structured-content identity. It is NOT a media-file SHA-256.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import yaml


def load_data(path: Path):
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    return yaml.safe_load(text)


def canonical_bytes(data) -> bytes:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def fingerprint(path: Path) -> str:
    return hashlib.sha256(canonical_bytes(load_data(path))).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path", type=Path)
    ap.add_argument("--json", action="store_true", dest="as_json")
    args = ap.parse_args()
    digest = fingerprint(args.path)
    if args.as_json:
        print(json.dumps({"path": str(args.path), "fingerprint_type": "STRUCTURED_SHA256", "sha256": digest}, ensure_ascii=False))
    else:
        print(digest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
