#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

def load(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))

def issue(issues,t,**k): d={'type':t}; d.update(k); issues.append(d)

def lint_prop(doc):
    issues=[]
    if doc.get('closure_status')=='CLOSED':
        for s in doc.get('surface_inventory') or []:
            if s.get('criticality')=='CRITICAL' and not (s.get('covered_by_view_ids') or []):
                issue(issues,'CRITICAL_PROP_SURFACE_UNCOVERED',surface_id=s.get('surface_id'))
    return {'pass': not issues, 'issues': issues}

def lint_env(doc):
    issues=[]
    if doc.get('closure_status') in {'PARTIAL','CLOSED'} and not (doc.get('anchors') or []):
        issue(issues,'ENV_ANCHOR_SET_EMPTY')
    for a in doc.get('anchors') or []:
        if not a.get('must_see_anchors'):
            issue(issues,'ENV_ANCHOR_MUST_SEE_MISSING',anchor_id=a.get('anchor_id'))
    return {'pass': not issues, 'issues': issues}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--prop'); ap.add_argument('--env'); a=ap.parse_args()
    if a.prop: out=lint_prop(load(a.prop))
    elif a.env: out=lint_env(load(a.env))
    else: out={'pass':False,'issues':[{'type':'ARGS_REQUIRED'}]}
    print(json.dumps(out, ensure_ascii=False, indent=2)); raise SystemExit(0 if out['pass'] else 2)

if __name__=='__main__': main()
