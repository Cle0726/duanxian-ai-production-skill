#!/usr/bin/env python3
"""Validate V4.5.4 Required View Realization architecture invariants."""
from __future__ import annotations
import argparse,json
from pathlib import Path
import yaml

def load(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]); ap.add_argument('--json',action='store_true')
    a=ap.parse_args(); root=a.root.resolve(); errors=[]
    rr=load(root/'controller/route_registry.yaml'); wf=load(root/'controller/workflow_state_machine.yaml'); ar=load(root/'controller/authority_registry.yaml')
    for name,obj in [('route_registry',rr),('workflow',wf),('authority_registry',ar)]:
        if obj.get('skill_version') not in {'4.5.4','4.5.5','4.5.6','4.5.7','4.5.8','4.5.9','4.5.10','4.5.11'}: errors.append(f'{name} unsupported skill_version {obj.get("skill_version")}')
    auth=ar.get('authorities') or {}
    for k in ['required_view_specification','required_view_realization_gate','required_view_visual_proof']:
        if k not in auth: errors.append(f'missing authority {k}')
    for rel in ['validators/required_view_realization_lint.py','tools/view_coverage_planner.py']:
        if not (root/rel).exists(): errors.append(f'missing {rel}')
    routes=rr.get('routes') or {}
    checks=[('STAGE_03_SPATIAL_CANON_QC','planning'),('EPISODE_ASSET_BUILD','build'),('EPISODE_ASSET_FREEZE','freeze')]
    for rn,phase in checks:
        r=routes.get(rn,{})
        if 'validators/required_view_realization_lint.py' not in (r.get('validators') or []): errors.append(f'{rn}: required_view_realization_lint missing')
        inv=[x for x in (r.get('validator_invocations') or []) if x.get('validator')=='validators/required_view_realization_lint.py' and x.get('phase')==phase]
        if not inv: errors.append(f'{rn}: required view invocation phase={phase} missing')
    if 'VISUAL_EVIDENCE' not in (routes.get('EPISODE_ASSET_FREEZE',{}).get('structured_inputs') or []): errors.append('freeze route missing VISUAL_EVIDENCE input')
    if 'tools/view_coverage_planner.py' not in (routes.get('EPISODE_ASSET_BUILD',{}).get('deterministic_tools') or []): errors.append('asset build missing view coverage planner')
    sc=load(root/'state/spatial_canon.schema.yaml'); reg=load(root/'state/asset_registry.schema.yaml'); ve=load(root/'state/visual_evidence.schema.yaml'); sr=load(root/'runtime/spatial_canon_runtime.schema.yaml')
    if 'view_requirements' not in (sc.get('properties') or {}): errors.append('spatial canon missing view_requirements')
    der=reg['properties']['assets']['items']['properties']['derivation']['properties']
    for f in ['view_requirement_ids','view_role','camera_origin_zone_id','camera_origin_anchor_id','view_target_entity_id','view_target_anchor_id','view_direction_code','forbidden_visible_anchor_ids']:
        if f not in der: errors.append(f'asset derivation missing {f}')
    vesp=ve['properties']['records']['items']['properties']['observed']['properties']['spatial']['properties']
    for f in ['view_roles','camera_origin_zone_id','camera_origin_anchor_id','view_target_entity_id','view_target_anchor_id','view_direction_code']:
        if f not in vesp: errors.append(f'visual evidence spatial missing {f}')
    if 'view_requirements' not in (sr.get('properties') or {}): errors.append('spatial runtime missing view_requirements')
    tids={t.get('id'):t for t in wf.get('transitions') or []}
    req=lambda tid:set(tids.get(tid,{}).get('requires') or [])
    if 'REQUIRED_VIEW_SPEC_VALIDATED' not in req('T10B_SPATIAL_CANON_QC'): errors.append('Spatial QC missing required view spec validation')
    for x in ['REQUIRED_VIEW_ASSET_COVERAGE_COMPLETE','REQUIRED_VIEW_VISUAL_REALIZATION_PASS']:
        if x not in req('T12_SPATIAL_RECONCILE'): errors.append(f'T12 missing {x}')
        if x not in req('T13_FREEZE'): errors.append(f'T13 missing {x}')
    checks_txt={
      'SKILL.md':['Required View Realization','Camera Origin','Optical Axis','Must See'],
      'templates/shot_coverage_asset_derivation.md':['REQUIRED_VIEW_REALIZATION_GATE','VIEW_ROLE_COVERAGE_MATRIX','COVERAGE_BUDGET_STARVES_REQUIRED_VIEW'],
      'templates/asset_master_prompt_template.md':['COVERAGE CAMERA PROOF BLOCK'],
      'templates/image_candidate_strategy.md':['Coverage Debt First'],
      'templates/visual_evidence_handoff.md':['Observed View Role'],
      'checklists/qc_checklists.md':['Required View Realization QC']
    }
    for rel,toks in checks_txt.items():
        txt=(root/rel).read_text(encoding='utf-8')
        for tok in toks:
            if tok not in txt: errors.append(f'{rel} missing {tok}')
    out={'errors':errors,'route_count':len(routes),'state_count':len(wf.get('states') or {}),'transition_count':len(wf.get('transitions') or [])}
    print(json.dumps(out,ensure_ascii=False,indent=2) if a.json else out)
    return 1 if errors else 0
if __name__=='__main__': raise SystemExit(main())
