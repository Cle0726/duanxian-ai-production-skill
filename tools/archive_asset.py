#!/usr/bin/env python3
"""Copy-first asset archive with filesystem and SHA-256 postconditions."""
from __future__ import annotations
import argparse, hashlib, json, shutil
from pathlib import Path


def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def within(root: Path, path: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve()); return True
    except ValueError:
        return False

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("source", type=Path)
    ap.add_argument("target", type=Path)
    ap.add_argument("--project-root", type=Path, required=True)
    ap.add_argument("--json", action="store_true")
    a=ap.parse_args()
    src=a.source.resolve(); dst=a.target.resolve(); root=a.project_root.resolve()
    result={"status":"ARCHIVE_PENDING","source":str(src),"target":str(dst),"project_root":str(root)}
    if not src.exists() or not src.is_file() or src.stat().st_size <= 0:
        result["reason"]="SOURCE_PREFLIGHT_FAIL"
    elif not within(root,dst):
        result["reason"]="TARGET_OUTSIDE_PROJECT_ROOT"
    elif dst.exists():
        result["reason"]="TARGET_ALREADY_EXISTS"
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src,dst)
        ss,ts=src.stat().st_size,dst.stat().st_size
        sh,th=sha256_file(src),sha256_file(dst)
        result.update({"source_size":ss,"target_size":ts,"source_sha256":sh,"target_sha256":th})
        if dst.exists() and dst.is_file() and ss==ts and sh==th:
            result["status"]="ARCHIVED"; result["sha256_verification"]="PASS"
        else:
            result["reason"]="POSTCONDITION_FAIL"; result["sha256_verification"]="FAILED"
    print(json.dumps(result, ensure_ascii=False, indent=2) if a.json else result)
    return 0 if result["status"]=="ARCHIVED" else 2
if __name__ == "__main__": raise SystemExit(main())
