#!/usr/bin/env python3
"""Validate V4.5 relation-driven control-plane invariants."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import yaml

def load(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]); ap.add_argument('--json',action='store_true'); a=ap.parse_args(); root=a.root.resolve(); errors=[]; warnings=[]
    rr=load(root/'controller/route_registry.yaml'); wf=load(root/'controller/workflow_state_machine.yaml'); ar=load(root/'controller/authority_registry.yaml')
    for name,obj in [('route_registry',rr),('workflow',wf),('authority_registry',ar)]:
        if obj.get('skill_version') not in {'4.5.0','4.5.1','4.5.2','4.5.3','4.5.4','4.5.5','4.5.6','4.5.7','4.5.8','4.5.9','4.5.10','4.5.11'}: errors.append(f'{name} unsupported skill_version {obj.get("skill_version")}')
    sa=rr.get('structured_artifacts') or {}
    for key in ['SHOT_RELATION_GRAPH','VISUAL_ASSET_OBLIGATION']:
        rel=sa.get(key)
        if not rel or not (root/rel).exists(): errors.append(f'missing structured artifact {key}: {rel}')
    routes=rr.get('routes') or {}
    for rn in ['EPISODE_ASSET_BUILD','EPISODE_ASSET_FREEZE','STAGE_04_STORYBOARD','STAGE_04_VIDEO_CONDITIONING_BUILD','STAGE_04_VIDEO_CONDITIONING_QC','STAGE_05_VIDEO']:
        if rn not in routes: errors.append(f'missing route {rn}'); continue
        si=set(routes[rn].get('structured_inputs') or [])
        if not {'SHOT_RELATION_GRAPH','VISUAL_ASSET_OBLIGATION'}<=si: errors.append(f'{rn}: relation structured inputs missing')
    prod=set(routes['STAGE_02C_PRODUCTION_TRANSLATION'].get('produces_structured_artifacts') or [])
    if not {'SHOT_RELATION_GRAPH','VISUAL_ASSET_OBLIGATION'}<=prod: errors.append('STAGE_02C does not produce both relation artifacts')
    trans={t.get('id'):set(t.get('requires') or []) for t in wf.get('transitions') or []}
    must={
      'T09_BREAKDOWN_READY':{'SHOT_RELATION_GRAPH_LOCKED','RELATION_DRIVEN_ASSET_OBLIGATIONS_DERIVED'},
      'T13_FREEZE':{'LOCATION_RELATION_PROOF_PASS','RELATION_DRIVEN_STAGE03_ASSET_QC_COMPLETE'},
      'T19_STORYBOARD_QC':{'SHOT_RELATION_STORYBOARD_ALIGNMENT_PASS'},
      'T22_CONDITIONING_QC':{'SHOT_RELATION_CONDITIONING_ALIGNMENT_PASS'},
      'T23B_VIDEO_READY':{'RELATION_DRIVEN_VIDEO_CONDITIONING_PASS'},
    }
    for tid,req in must.items():
        if not req<=trans.get(tid,set()): errors.append(f'{tid}: missing requirements {sorted(req-trans.get(tid,set()))}')
    for auth in ['shot_relation_graph','relation_driven_visual_asset_obligation','location_relation_visual_proof','pairwise_video_boundary_alignment']:
        if auth not in (ar.get('authorities') or {}): errors.append(f'missing authority index {auth}')
    # no new markdown engine should be necessary for these two structures
    for fname in ['shot_relation_graph.md','visual_asset_obligation.md']:
        forbidden=Path('templates')/fname
        if (root/forbidden).exists(): warnings.append(f'unexpected extra markdown authority: {forbidden}')
    out={'errors':errors,'warnings':warnings,'route_count':len(routes),'state_count':len(wf.get('states') or {}),'transition_count':len(wf.get('transitions') or [])}
    print(json.dumps(out,ensure_ascii=False,indent=2) if a.json else out); return 1 if errors else 0
if __name__=='__main__': raise SystemExit(main())
