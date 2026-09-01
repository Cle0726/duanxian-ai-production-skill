#!/usr/bin/env python3
"""Validate YAML/JSON instance against a V4.3 YAML JSON-Schema."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator

def load(path: Path):
    text=path.read_text(encoding="utf-8")
    return json.loads(text) if path.suffix.lower()==".json" else yaml.safe_load(text)

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("schema",type=Path); ap.add_argument("instance",type=Path); ap.add_argument("--json",action="store_true",dest="as_json")
    a=ap.parse_args(); schema=load(a.schema); instance=load(a.instance)
    errors=sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda e:list(e.path))
    out={"valid":not errors,"errors":[{"path":"/"+"/".join(map(str,e.path)),"message":e.message} for e in errors]}
    print(json.dumps(out,ensure_ascii=False,indent=2) if a.as_json else out)
    return 0 if not errors else 1
if __name__=="__main__": raise SystemExit(main())
