#!/usr/bin/env python3
"""Re-seal a mutated Runtime Capsule: recompute runtime_fingerprint, then prove schema closure."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]

def load(p):
    p=Path(p); text=p.read_text(encoding='utf-8')
    try:return json.loads(text)
    except Exception:return yaml.safe_load(text)

def fp(d):
    x=dict(d); x.pop('runtime_fingerprint',None)
    return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),default=str).encode('utf-8')).hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--runtime',required=True); ap.add_argument('--output',required=True); a=ap.parse_args()
    d=load(a.runtime)
    if not isinstance(d,dict) or not d.get('runtime_type'):
        print(json.dumps({'pass':False,'error':'RUNTIME_TYPE_MISSING'},ensure_ascii=False,indent=2)); return 2
    sp=ROOT/'runtime'/(str(d['runtime_type']).lower()+'.schema.yaml')
    if not sp.exists():
        print(json.dumps({'pass':False,'error':'RUNTIME_SCHEMA_NOT_FOUND','runtime_type':d['runtime_type']},ensure_ascii=False,indent=2)); return 2
    d['runtime_fingerprint']=fp(d)
    schema=load(sp)
    errors=sorted(Draft202012Validator(schema).iter_errors(d),key=lambda e:list(e.absolute_path))
    if errors:
        print(json.dumps({'pass':False,'error':'RUNTIME_SCHEMA_CLOSURE_FAILED','issues':[{'path':'/'.join(map(str,e.absolute_path)) or '$','message':e.message} for e in errors[:30]]},ensure_ascii=False,indent=2)); return 2
    out=Path(a.output); out.write_text(yaml.safe_dump(d,sort_keys=False,allow_unicode=True),encoding='utf-8')
    print(json.dumps({'pass':True,'runtime_type':d['runtime_type'],'runtime_fingerprint':d['runtime_fingerprint'],'output':str(out)},ensure_ascii=False,indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
