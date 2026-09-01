#!/usr/bin/env python3
"""Fail on duplicate YAML mapping keys; PyYAML otherwise silently overwrites them."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml
class UniqueKeyLoader(yaml.SafeLoader): pass
def construct_mapping(loader,node,deep=False):
    mapping={}
    for key_node,value_node in node.value:
        key=loader.construct_object(key_node,deep=deep)
        if key in mapping: raise ValueError(f'duplicate key {key!r} at line {key_node.start_mark.line+1}')
        mapping[key]=loader.construct_object(value_node,deep=deep)
    return mapping
UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,construct_mapping)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('paths',nargs='+'); a=ap.parse_args(); issues=[]
    for raw in a.paths:
        p=Path(raw)
        files=list(p.rglob('*.yaml'))+list(p.rglob('*.yml')) if p.is_dir() else [p]
        for f in files:
            try: yaml.load(f.read_text(encoding='utf-8'),Loader=UniqueKeyLoader)
            except Exception as e: issues.append({'file':str(f),'error':str(e)})
    out={'pass':not issues,'issues':issues}; print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
