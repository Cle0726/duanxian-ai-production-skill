#!/usr/bin/env python3
"""Validate V4.5.5 Everyday Realism & Plausibility architecture invariants."""
from __future__ import annotations
import argparse,json
from pathlib import Path
import yaml

def load(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]); ap.add_argument('--json',action='store_true')
    a=ap.parse_args(); root=a.root.resolve(); errors=[]
    rr=load(root/'controller/route_registry.yaml'); wf=load(root/'controller/workflow_state_machine.yaml'); ar=load(root/'controller/authority_registry.yaml'); mm=load(root/'controller/module_manifest.yaml'); fr=load(root/'controller/failure_router.yaml')
    for name,obj in [('route_registry',rr),('workflow',wf),('authority_registry',ar),('module_manifest',mm)]:
        if obj.get('skill_version') not in {'4.5.5','4.5.6','4.5.7','4.5.8','4.5.9','4.5.10','4.5.11'}: errors.append(f'{name} unsupported skill_version {obj.get("skill_version")}')
    if 'everyday_realism_plausibility' not in (ar.get('authorities') or {}): errors.append('missing everyday_realism_plausibility authority')
    for rel in ['templates/everyday_realism_plausibility_gate.md','state/realism_contract.schema.yaml','runtime/realism_runtime.schema.yaml','validators/everyday_realism_lint.py']:
        if not (root/rel).exists(): errors.append(f'missing {rel}')
    if 'REALISM_RUNTIME' not in (rr.get('runtime_types') or []): errors.append('REALISM_RUNTIME missing from route registry')
    if (rr.get('structured_artifacts') or {}).get('REALISM_CONTRACT')!='state/realism_contract.schema.yaml': errors.append('REALISM_CONTRACT artifact mapping missing')
    routes=rr.get('routes') or {}
    for rn,phase in [('STAGE_03_SPATIAL_CANON_QC','planning'),('EPISODE_ASSET_BUILD','build'),('EPISODE_ASSET_FREEZE','freeze')]:
        r=routes.get(rn,{})
        if 'validators/everyday_realism_lint.py' not in (r.get('validators') or []): errors.append(f'{rn}: everyday_realism_lint missing')
        inv=[x for x in (r.get('validator_invocations') or []) if x.get('validator')=='validators/everyday_realism_lint.py' and x.get('phase')==phase]
        if not inv: errors.append(f'{rn}: realism invocation phase={phase} missing')
        if 'REALISM_RUNTIME' not in (r.get('runtime') or []): errors.append(f'{rn}: REALISM_RUNTIME missing')
    if 'EVERYDAY_REALISM_RECONCILIATION' not in routes: errors.append('missing EVERYDAY_REALISM_RECONCILIATION route')
    # Exact emitted failure codes must resolve to deterministic rollback routes.
    failure_routes=fr.get('routes') or {}
    for code in ['CAST_COUNT_MISMATCH','CHARACTER_ZONE_ASSIGNMENT_FAIL','CHARACTER_FUNCTIONAL_POSITION_FAIL','ERGONOMIC_SUPPORT_FAIL','HUMAN_ENVIRONMENT_INTERSECTION_FAIL','HUMAN_SCALE_IMPLAUSIBLE','SPACE_CAPACITY_EXCEEDED','OBJECT_AFFORDANCE_FAIL','SOCIAL_SPATIAL_IMPLAUSIBILITY','MUNDANE_PHYSICS_FAIL','MUNDANE_CONTINUITY_FAIL','VEHICLE_FUNCTIONAL_LAYOUT_DRIFT','REALISM_VISUAL_EVIDENCE_MISSING_OR_STALE','REALISM_CATEGORY_UNPROVEN','REQUIRED_VIEW_REALISM_CONTRACT_GAP','REQUIRED_VIEW_REALISM_QC_NOT_PASS']:
        if code not in failure_routes: errors.append(f'failure router missing exact realism code: {code}')
    rv=(root/'validators/required_view_realization_lint.py').read_text(encoding='utf-8')
    for tok in ['VIEW_ASSET_REALISM_CONTRACT_GAP','REQUIRED_VIEW_REALISM_CONTRACT_GAP','REQUIRED_VIEW_REALISM_QC_NOT_PASS']:
        if tok not in rv: errors.append(f'required-view realism bridge missing {tok}')
    # Schema hooks
    sc=load(root/'state/spatial_canon.schema.yaml'); ve=load(root/'state/visual_evidence.schema.yaml'); reg=load(root/'state/asset_registry.schema.yaml')
    loc=sc['properties']['locations']['items']['properties']
    if 'VEHICLE' not in loc['location_kind']['enum']: errors.append('spatial canon missing VEHICLE location kind')
    pdt=sc['properties']['planning_diagrams']['items']['properties']['diagram_type']['enum']
    if 'VEHICLE_LAYOUT' not in pdt: errors.append('spatial canon missing VEHICLE_LAYOUT diagram type')
    for f in ['functional_profile','specific_functional_type','realism_contract_ids']:
        if f not in loc: errors.append(f'spatial location missing {f}')
    ro=ve['properties']['records']['items']['properties']['observed']['properties'].get('realism',{}).get('properties',{})
    for f in ['human_count','characters','environment','object_affordances','character_relations','category_verdicts','overall_verdict']:
        if f not in ro: errors.append(f'visual evidence realism missing {f}')
    arp=reg['properties']['assets']['items']['properties']
    for f in ['realism_contract_ids','realism_qc_status','realism_exception_ids']:
        if f not in arp: errors.append(f'asset registry missing {f}')
    # Workflow gates
    tids={t.get('id'):t for t in wf.get('transitions') or []}
    def req(tid): return set(tids.get(tid,{}).get('requires') or [])
    for x in ['REALISM_CONTRACT_AVAILABLE','REALISM_CONTRACT_QC_PASS','VEHICLE_FUNCTIONAL_PROFILE_VALIDATED_IF_APPLICABLE']:
        if x not in req('T10B_SPATIAL_CANON_QC'): errors.append(f'T10B missing {x}')
    for tid in ['T12_SPATIAL_RECONCILE','T13_FREEZE']:
        for x in ['EVERYDAY_REALISM_PLAUSIBILITY_PASS','REALISM_RECONCILIATION_CLEAR']:
            if x not in req(tid): errors.append(f'{tid} missing {x}')
    if 'STORYBOARD_EVERYDAY_REALISM_PASS' not in req('T19_STORYBOARD_QC'): errors.append('T19 missing Storyboard realism pass')
    if 'VIDEO_CONDITIONING_EVERYDAY_REALISM_PASS' not in req('T22_CONDITIONING_QC'): errors.append('T22 missing conditioning realism pass')
    if 'VIDEO_EVERYDAY_REALISM_QC_PASS' not in req('T25_VIDEO_QC'): errors.append('T25 missing video realism QC pass')
    # Text owner propagation
    checks={
      'SKILL.md':['Everyday Realism & Plausibility','Reality by Default','VEHICLE','漂亮'],
      'templates/everyday_realism_plausibility_gate.md':['ENVIRONMENT_FUNCTIONAL_REALISM','VEHICLE_REALISM','HUMAN_ERGONOMICS','OBJECT_AFFORDANCE','SOCIAL_SPATIAL_PLAUSIBILITY','MUNDANE_PHYSICS','MUNDANE_CONTINUITY','Asset Logic Reconciliation Loop'],
      'templates/environment_asset_standard.md':['Functional Reality Before Visual Beauty','VEHICLE_LAYOUT'],
      'templates/asset_master_prompt_template.md':['EVERYDAY REALISM EXECUTION BLOCK'],
      'templates/visual_evidence_handoff.md':['Observed Everyday Realism'],
      'checklists/qc_checklists.md':['Everyday Realism & Plausibility QC']
    }
    for rel,toks in checks.items():
        txt=(root/rel).read_text(encoding='utf-8')
        for tok in toks:
            if tok not in txt: errors.append(f'{rel} missing {tok}')
    out={'errors':errors,'route_count':len(routes),'state_count':len(wf.get('states') or {}),'transition_count':len(wf.get('transitions') or [])}
    print(json.dumps(out,ensure_ascii=False,indent=2) if a.json else out)
    return 1 if errors else 0
if __name__=='__main__': raise SystemExit(main())
