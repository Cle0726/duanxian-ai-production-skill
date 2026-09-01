#!/usr/bin/env python3
"""Invalidate a frozen execution plan when any authoritative source fingerprint changes."""
import argparse, json, pathlib, yaml

def load(p):
    text=pathlib.Path(p).read_text(encoding='utf-8')
    return json.loads(text) if pathlib.Path(p).suffix.lower()=='.json' else yaml.safe_load(text)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--plan',required=True); ap.add_argument('--current',required=True); a=ap.parse_args()
    p=load(a.plan); cur=load(a.current); issues=[]
    if p.get('status')!='FROZEN_FOR_COMPILE' or p.get('video_execution_plan_pass') is not True: issues.append({'type':'EXECUTION_PLAN_NOT_FROZEN'})
    sf=p.get('source_fingerprints') or {}
    for k in ['director','storyboard','shot_execution','scene_color','world_state']:
        if not sf.get(k): issues.append({'type':'EXECUTION_PLAN_SOURCE_FINGERPRINT_MISSING','source':k})
        elif cur.get(k)!=sf.get(k): issues.append({'type':'EXECUTION_PLAN_STALE','source':k,'planned':sf.get(k),'current':cur.get(k)})
    out={'pass':not issues,'status':'VALID' if not issues else 'STALE','issues':issues}
    print(json.dumps(out,ensure_ascii=False,indent=2)); return 0 if not issues else 2
if __name__=='__main__': raise SystemExit(main())
