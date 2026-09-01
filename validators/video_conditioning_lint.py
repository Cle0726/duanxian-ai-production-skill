#!/usr/bin/env python3
"""Validate V4.5.2 primary visual conditioning coverage and strategy-specific frame sets."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml
APPROVED={'APPROVED','APPROVED_VIDEO_CONDITIONING'}
STRATEGY_REQUIRED={
 'FIRST_FRAME':[{'VIDEO_FIRST_FRAME','VIDEO_SHOT_EXECUTION_FRAME'}],
 'FIRST_TARGET':[{'VIDEO_FIRST_FRAME','VIDEO_SHOT_EXECUTION_FRAME'},{'VIDEO_TARGET_FRAME'}],
 'FIRST_LAST':[{'VIDEO_FIRST_FRAME','VIDEO_SHOT_EXECUTION_FRAME'},{'VIDEO_LAST_FRAME'}],
 'CONTACT_CHAIN':[{'VIDEO_FIRST_FRAME','VIDEO_SHOT_EXECUTION_FRAME'},{'VIDEO_CONTACT_FRAME'}],
 'TRANSFORMATION_CHAIN':[{'VIDEO_FIRST_FRAME','VIDEO_SHOT_EXECUTION_FRAME'},{'VIDEO_KEY_POSE'},{'VIDEO_LAST_FRAME','VIDEO_TARGET_FRAME'}],
 'CUT_PAIR':[{'VIDEO_CUT_EXIT_FRAME','VIDEO_CUT_ENTRY_FRAME','VIDEO_FIRST_FRAME','VIDEO_LAST_FRAME'}],
}

def load(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))
def lint(runtime,registry=None):
    issues=[]; assets={a.get('asset_id'):a for a in ((registry or {}).get('assets') or [])}; units=runtime.get('video_units') or []
    if not units: issues.append({'type':'VIDEO_CONDITIONING_PLAN_MISSING'})
    for u in units:
        uid=u.get('video_unit_id'); prim=u.get('primary_assets') or []; roles={x.get('role') for x in prim}
        if not prim: issues.append({'type':'PRIMARY_VISUAL_CONDITIONING_GAP','video_unit_id':uid}); continue
        strat=u.get('conditioning_strategy')
        if strat=='KEY_POSE_CHAIN':
            if not ({'VIDEO_FIRST_FRAME','VIDEO_SHOT_EXECUTION_FRAME'} & roles): issues.append({'type':'CONDITIONING_STRATEGY_FRAME_GAP','video_unit_id':uid,'strategy':strat,'required':'FIRST'})
            if 'VIDEO_KEY_POSE' not in roles: issues.append({'type':'CONDITIONING_STRATEGY_FRAME_GAP','video_unit_id':uid,'strategy':strat,'required':'KEY_POSE'})
        else:
            for idx,allowed in enumerate(STRATEGY_REQUIRED.get(strat,[])):
                if not (roles & allowed): issues.append({'type':'CONDITIONING_STRATEGY_FRAME_GAP','video_unit_id':uid,'strategy':strat,'required_any_of':sorted(allowed),'slot':idx})
        if u.get('qc_status')!='PASS': issues.append({'type':'VIDEO_CONDITIONING_QC_NOT_PASS','video_unit_id':uid,'status':u.get('qc_status')})
        for pa in prim:
            aid=pa.get('asset_id')
            if not pa.get('direct_video_eligible'): issues.append({'type':'DIRECT_VIDEO_ELIGIBILITY_FAIL','video_unit_id':uid,'asset_id':aid})
            if pa.get('approval_status') not in APPROVED: issues.append({'type':'PRIMARY_VISUAL_NOT_APPROVED','video_unit_id':uid,'asset_id':aid})
            if registry:
                a=assets.get(aid)
                if not a: issues.append({'type':'PRIMARY_VISUAL_ASSET_NOT_IN_REGISTRY','video_unit_id':uid,'asset_id':aid}); continue
                vu=a.get('video_usage') or {}
                if not vu.get('primary_visual_eligible'): issues.append({'type':'ASSET_ROLE_ESCALATION_FAIL','video_unit_id':uid,'asset_id':aid,'asset_type':a.get('asset_type')})
                if not vu.get('direct_input_allowed'): issues.append({'type':'DIRECT_VIDEO_ELIGIBILITY_FAIL','video_unit_id':uid,'asset_id':aid,'registry':True})
                if a.get('layout_type') in {'MULTI_PANEL','COLOR_SWATCH','CONTACT_SHEET','MAP','PLANNING_DIAGRAM'}: issues.append({'type':'NON_SINGLE_FRAME_PRIMARY_VISUAL_FAIL','video_unit_id':uid,'asset_id':aid,'layout_type':a.get('layout_type')})
    if runtime.get('readiness')!='PASS': issues.append({'type':'VIDEO_CONDITIONING_RUNTIME_NOT_READY','status':runtime.get('readiness')})
    return {'pass':not issues,'video_unit_count':len(units),'issues':issues}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--runtime',required=True); ap.add_argument('--registry'); a=ap.parse_args(); out=lint(load(a.runtime),load(a.registry) if a.registry else None); print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
