#!/usr/bin/env python3
"""Validate V4.5.2 Script-Grounded Virtual Set architecture invariants."""
from __future__ import annotations
import argparse,json
from pathlib import Path
import yaml

def load(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]); ap.add_argument('--json',action='store_true'); a=ap.parse_args(); root=a.root.resolve(); errors=[]; warnings=[]
    rr=load(root/'controller/route_registry.yaml'); wf=load(root/'controller/workflow_state_machine.yaml'); ar=load(root/'controller/authority_registry.yaml')
    for name,obj in [('route_registry',rr),('workflow',wf),('authority_registry',ar)]:
        if obj.get('skill_version') not in {'4.5.2','4.5.3','4.5.4','4.5.5','4.5.6','4.5.7','4.5.8','4.5.9','4.5.10','4.5.11'}: errors.append(f'{name} unsupported skill_version {obj.get("skill_version")}')
    auth=ar.get('authorities') or {}
    for k in ['character_event_route','spatial_planning_diagram','reciprocal_predictive_coverage','coverage_derivation_parentage','asset_justification','cascade_asset_approval','scene_look_domain','voice_identity_asset']:
        if k not in auth: errors.append(f'missing authority {k}')
    routes=rr.get('routes') or {}
    for rn in ['STAGE_03_SPATIAL_CANON_BUILD','STAGE_03_SPATIAL_CANON_QC','EPISODE_ASSET_BUILD','EPISODE_ASSET_FREEZE']:
        if rn not in routes: errors.append(f'missing route {rn}')
    for rn in ['STAGE_03_SPATIAL_CANON_QC','EPISODE_ASSET_BUILD','EPISODE_ASSET_FREEZE']:
        if 'validators/virtual_set_asset_lint.py' not in (routes.get(rn,{}).get('validators') or []): errors.append(f'{rn}: virtual_set_asset_lint missing')
    if 'tools/spatial_diagram_renderer.py' not in (routes.get('STAGE_03_SPATIAL_CANON_BUILD',{}).get('deterministic_tools') or []): errors.append('Spatial Canon build missing deterministic planning diagram renderer')
    tids={t.get('id'):t for t in wf.get('transitions') or []}
    req=lambda tid:set(tids.get(tid,{}).get('requires') or [])
    if not {'SPATIAL_PLANNING_DIAGRAMS_QC_PASS','CHARACTER_EVENT_ROUTES_VALIDATED'} <= req('T10B_SPATIAL_CANON_QC'): errors.append('Spatial QC missing route/diagram validation')
    if 'USER_APPROVED_REQUIRED_SPATIAL_DIAGRAMS' not in req('T10C_SPATIAL_CANON_APPROVE'): errors.append('Spatial approval missing diagram approval')
    if not {'JUSTIFIED_ASSET_QUEUE_READY','CASCADE_ASSET_BUILD_PLAN_READY'} <= req('T10D_ASSET_BUILD'): errors.append('Asset build missing justified/cascade plan')
    for x in ['JUSTIFIED_ASSET_GENERATION_PASS','PREDICTIVE_COVERAGE_COMPLETE','LOOK_DOMAIN_FREEZE_PASS','REQUIRED_VOICE_IDENTITY_ASSETS_RESOLVED']:
        if x not in req('T12_SPATIAL_RECONCILE'): errors.append(f'Freeze path missing {x}')
    # schemas
    sc=load(root/'state/spatial_canon.schema.yaml'); reg=load(root/'state/asset_registry.schema.yaml'); obl=load(root/'state/visual_asset_obligation.schema.yaml')
    if sc.get('properties',{}).get('schema_version',{}).get('const')!=2: errors.append('spatial canon schema not v2')
    for p in ['character_routes','planning_diagrams']:
        if p not in (sc.get('properties') or {}): errors.append(f'spatial canon missing {p}')
    sv=reg.get('properties',{}).get('schema_version',{}); vals=set(sv.get('enum',[])); const=sv.get('const');
    if not ((const==5) or (5 in vals and 6 in vals)): errors.append('asset registry schema does not retain v5/v6 compatibility')
    aprops=reg['properties']['assets']['items']['properties']
    for p in ['justification','derivation','cascade_stage','look_domain','media_kind']:
        if p not in aprops: errors.append(f'asset registry missing {p}')
    types=set(obl['properties']['obligations']['items']['properties']['obligation_type']['enum'])
    for t in ['EVENT_NODE_VIEW','RECIPROCAL_COVERAGE_VIEW','PREDICTIVE_COVERAGE_VIEW','OUTDOOR_TOPOLOGY_DIAGRAM','BUILDING_FLOOR_PLAN_DIAGRAM','SCENE_LOOK_CARD']:
        if t not in types: errors.append(f'obligation type missing {t}')
    # active docs tokens
    checks={
        'templates/environment_asset_standard.md':['Character Event Route','Reciprocal / Predictive Set Coverage','双Parent派生','Outdoor Topology Diagram'],
        'templates/episode_asset_pack_first.md':['Justified Asset Generation','Cascade Approval','Required Voice Identity Asset'],
        'templates/shot_coverage_asset_derivation.md':['Predictive Coverage','双Parent Contract'],
        'templates/voice_identity_audio_status.md':['Stage 03 Voice Asset Requirement'],
        'templates/color_script_derivation_engine.md':['Interior / Exterior Look Domain']
    }
    for rel,toks in checks.items():
        txt=(root/rel).read_text(encoding='utf-8')
        for tok in toks:
            if tok not in txt: errors.append(f'{rel} missing {tok}')
    out={'errors':errors,'warnings':warnings,'route_count':len(routes),'state_count':len(wf.get('states') or {}),'transition_count':len(wf.get('transitions') or [])}
    print(json.dumps(out,ensure_ascii=False,indent=2) if a.json else out); return 1 if errors else 0
if __name__=='__main__': raise SystemExit(main())
