#!/usr/bin/env python3
"""Deterministic Required View coverage matrix / minimal generation queue (V4.5.4)."""
from __future__ import annotations
import argparse,json
from pathlib import Path
import yaml

ACTIVE={'DRAFT','QC_PASS_WAITING_APPROVAL','APPROVED','APPROVED_SUPPORT','APPROVED_ASSEMBLY','APPROVED_SCOPED_FIGURE','APPROVED_VIDEO_CONDITIONING'}

def load(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--spatial-canon',required=True); ap.add_argument('--asset-registry',required=True); ap.add_argument('--output')
    a=ap.parse_args(); sp=load(a.spatial_canon); reg=load(a.asset_registry)
    reqs=[r for r in sp.get('view_requirements',[]) if r.get('status') in {'REQUIRED','FULFILLED'}]
    assets=reg.get('assets',[])
    rows=[]; queue=[]
    for r in reqs:
        rid=r.get('view_requirement_id')
        cands=[]
        for asset in assets:
            if asset.get('status') not in ACTIVE: continue
            if rid in ((asset.get('derivation') or {}).get('view_requirement_ids') or []): cands.append(asset.get('asset_id'))
        selected=r.get('selected_fulfillment_asset_id')
        selected_valid=bool(selected and selected in cands)
        state='FULFILLED_SELECTED' if selected_valid else ('HAS_CANDIDATE' if cands else 'MISSING')
        row={
            'view_requirement_id':rid,'priority':r.get('priority','P1'),'scene_id':r.get('scene_id'),
            'location_entity_id':r.get('location_entity_id'),'view_role':r.get('view_role'),
            'camera_origin_zone_id':r.get('camera_origin_zone_id'),'camera_origin_anchor_id':r.get('camera_origin_anchor_id'),
            'view_target_entity_id':r.get('view_target_entity_id'),'view_target_anchor_id':r.get('view_target_anchor_id'),
            'view_direction_code':r.get('view_direction_code'),'required_visible_anchor_ids':r.get('required_visible_anchor_ids',[]),
            'candidate_asset_ids':cands,'selected_fulfillment_asset_id':selected,'coverage_state':state
        }
        rows.append(row)
        if state=='MISSING': queue.append(row)
    rank={'P0':0,'P1':1,'P2':2,'P3':3}
    queue.sort(key=lambda x:(rank.get(x.get('priority'),9),str(x.get('scene_id')),str(x.get('view_requirement_id'))))
    out={'coverage_matrix':rows,'generation_queue':queue,'missing_count':len(queue),'rule':'Generate only missing view requirements; P0/P1 missing views precede extra candidates for already-covered directions.'}
    text=json.dumps(out,ensure_ascii=False,indent=2)
    if a.output: Path(a.output).write_text(text+'\n',encoding='utf-8')
    else: print(text)

if __name__=='__main__': main()
