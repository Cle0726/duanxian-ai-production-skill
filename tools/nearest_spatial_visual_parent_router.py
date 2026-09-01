#!/usr/bin/env python3
"""Select nearest approved visual parent(s) by circular camera/view yaw distance."""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import yaml

APPROVED={'APPROVED','APPROVED_SUPPORT','APPROVED_ASSEMBLY','APPROVED_SCOPED_FIGURE','APPROVED_VIDEO_CONDITIONING'}

def load(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))
def circ(a,b):
    return abs((float(a)-float(b)+180.0)%360.0-180.0)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--request',required=True); ap.add_argument('--registry'); ap.add_argument('--max-primary-distance',type=float,default=100.0); ap.add_argument('--json',action='store_true'); a=ap.parse_args()
    req=load(a.request); target=req.get('target_yaw_deg'); issues=[]
    try: target=float(target)
    except Exception:
        out={'pass':False,'issues':[{'type':'VISUAL_PARENT_TARGET_YAW_INVALID','actual':target}]}; print(json.dumps(out,ensure_ascii=False,indent=2)); return 2
    assets={}
    if a.registry:
        reg=load(a.registry); assets={x.get('asset_id'):x for x in reg.get('assets') or [] if x.get('asset_id')}
    ranked=[]
    for c in req.get('candidate_views') or []:
        aid=c.get('asset_id'); yaw=c.get('yaw_deg')
        if not aid or yaw is None: continue
        if assets:
            ax=assets.get(aid)
            if not ax or ax.get('status') not in APPROVED: continue
        try: d=circ(target,float(yaw))
        except Exception: continue
        ranked.append((d,aid,c))
    ranked.sort(key=lambda x:(x[0],x[1]))
    if not ranked:
        out={'pass':False,'issues':[{'type':'NEAREST_VISUAL_PARENT_NOT_FOUND'}]}; print(json.dumps(out,ensure_ascii=False,indent=2)); return 2
    primary=ranked[0]
    if primary[0]>a.max_primary_distance:
        out={'pass':False,'issues':[{'type':'NEAREST_VISUAL_PARENT_TOO_FAR','asset_id':primary[1],'distance_deg':primary[0],'max_deg':a.max_primary_distance}]}; print(json.dumps(out,ensure_ascii=False,indent=2)); return 2
    secondary=ranked[1] if len(ranked)>1 else None
    out={'pass':True,'target_yaw_deg':target,'primary':{'asset_id':primary[1],'distance_deg':round(primary[0],3),'authority_kind':primary[2].get('authority_kind')},'secondary':None if secondary is None else {'asset_id':secondary[1],'distance_deg':round(secondary[0],3),'authority_kind':secondary[2].get('authority_kind')}}
    print(json.dumps(out,ensure_ascii=False,indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
