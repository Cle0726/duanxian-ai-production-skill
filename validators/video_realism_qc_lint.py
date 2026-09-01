#!/usr/bin/env python3
"""Validate that an actual video take has current multimodal/human Everyday Realism evidence.

A text-only controller may consume this evidence but may not create the PASS. The evidence
must fingerprint-match the current video take. Scoped exceptions remain category-local.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
import yaml

CATEGORIES=[
 'ENVIRONMENT_FUNCTIONAL_REALISM','ARCHITECTURAL_REALISM','VEHICLE_REALISM','HUMAN_ERGONOMICS',
 'OBJECT_AFFORDANCE','SOCIAL_SPATIAL_PLAUSIBILITY','MUNDANE_PHYSICS','MUNDANE_CONTINUITY'
]
DEFAULTS={
 'GENERAL': {'ENVIRONMENT_FUNCTIONAL_REALISM','HUMAN_ERGONOMICS','OBJECT_AFFORDANCE','SOCIAL_SPATIAL_PLAUSIBILITY','MUNDANE_PHYSICS','MUNDANE_CONTINUITY'},
 'INTERIOR': {'ENVIRONMENT_FUNCTIONAL_REALISM','ARCHITECTURAL_REALISM','HUMAN_ERGONOMICS','OBJECT_AFFORDANCE','SOCIAL_SPATIAL_PLAUSIBILITY','MUNDANE_PHYSICS','MUNDANE_CONTINUITY'},
 'BUILDING': {'ENVIRONMENT_FUNCTIONAL_REALISM','ARCHITECTURAL_REALISM','HUMAN_ERGONOMICS','OBJECT_AFFORDANCE','SOCIAL_SPATIAL_PLAUSIBILITY','MUNDANE_PHYSICS','MUNDANE_CONTINUITY'},
 'RESTAURANT': {'ENVIRONMENT_FUNCTIONAL_REALISM','ARCHITECTURAL_REALISM','HUMAN_ERGONOMICS','OBJECT_AFFORDANCE','SOCIAL_SPATIAL_PLAUSIBILITY','MUNDANE_PHYSICS','MUNDANE_CONTINUITY'},
 'RESIDENTIAL': {'ENVIRONMENT_FUNCTIONAL_REALISM','ARCHITECTURAL_REALISM','HUMAN_ERGONOMICS','OBJECT_AFFORDANCE','SOCIAL_SPATIAL_PLAUSIBILITY','MUNDANE_PHYSICS','MUNDANE_CONTINUITY'},
 'WORKPLACE': {'ENVIRONMENT_FUNCTIONAL_REALISM','ARCHITECTURAL_REALISM','HUMAN_ERGONOMICS','OBJECT_AFFORDANCE','SOCIAL_SPATIAL_PLAUSIBILITY','MUNDANE_PHYSICS','MUNDANE_CONTINUITY'},
 'VEHICLE': {'ENVIRONMENT_FUNCTIONAL_REALISM','VEHICLE_REALISM','HUMAN_ERGONOMICS','OBJECT_AFFORDANCE','SOCIAL_SPATIAL_PLAUSIBILITY','MUNDANE_PHYSICS','MUNDANE_CONTINUITY'},
 'EXTERIOR': {'ENVIRONMENT_FUNCTIONAL_REALISM','HUMAN_ERGONOMICS','OBJECT_AFFORDANCE','SOCIAL_SPATIAL_PLAUSIBILITY','MUNDANE_PHYSICS','MUNDANE_CONTINUITY'},
 'STREET': {'ENVIRONMENT_FUNCTIONAL_REALISM','HUMAN_ERGONOMICS','OBJECT_AFFORDANCE','SOCIAL_SPATIAL_PLAUSIBILITY','MUNDANE_PHYSICS','MUNDANE_CONTINUITY'},
 'OTHER': {'ENVIRONMENT_FUNCTIONAL_REALISM','HUMAN_ERGONOMICS','OBJECT_AFFORDANCE','MUNDANE_PHYSICS','MUNDANE_CONTINUITY'},
}


def load(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))
def add(issues,t,**kw): issues.append({'type':t,**kw})

def scope_ids(video):
    s=(video or {}).get('scope') or {}
    shots=set(s.get('shot_ids') or [])
    if s.get('shot_id'): shots.add(s.get('shot_id'))
    scene=s.get('scene_id')
    return scene,shots

def contract_matches(c,scene,shots):
    if scene and c.get('scene_id')==scene: return True
    if shots & set(c.get('shot_ids') or []): return True
    return False

def category_waived(c,cat,scene,shots):
    for ex in c.get('exception_scopes') or []:
        if cat not in set(ex.get('allowed_categories') or []): continue
        if scene and scene in set(ex.get('scene_ids') or []): return True
        if shots & set(ex.get('shot_ids') or []): return True
    return False

def lint(realism,video,qc):
    issues=[]
    fp=(video or {}).get('video_take_fingerprint')
    if not fp: add(issues,'VIDEO_TAKE_FINGERPRINT_MISSING')
    ev=(qc or {}).get('video_realism_evidence') or {}
    if ev.get('evidence_status')!='CURRENT': add(issues,'VIDEO_REALISM_EVIDENCE_NOT_CURRENT',evidence_status=ev.get('evidence_status'))
    if fp and ev.get('video_take_fingerprint')!=fp: add(issues,'VIDEO_REALISM_EVIDENCE_STALE',expected_fingerprint=fp,evidence_fingerprint=ev.get('video_take_fingerprint'))
    if ev.get('inspector_mode') not in {'MULTIMODAL_MODEL','HUMAN','MIXED'}: add(issues,'VIDEO_REALISM_INSPECTOR_INVALID',inspector_mode=ev.get('inspector_mode'))
    scene,shots=scope_ids(video)
    if not scene and not shots: add(issues,'VIDEO_REALISM_SCOPE_MISSING')
    contracts=[c for c in (realism or {}).get('contracts') or [] if contract_matches(c,scene,shots)]
    if not contracts: add(issues,'VIDEO_REALISM_CONTRACT_SCOPE_MISSING',scene_id=scene,shot_ids=sorted(shots))
    required=set()
    for c in contracts:
        cats=set(c.get('required_categories') or []) or set(DEFAULTS.get(c.get('profile') or 'GENERAL',DEFAULTS['GENERAL']))
        for cat in cats:
            if not category_waived(c,cat,scene,shots): required.add(cat)
    verdicts=ev.get('category_verdicts') or {}
    for cat in sorted(required):
        v=verdicts.get(cat,'UNKNOWN')
        if v=='FAIL': add(issues,'VIDEO_REALISM_CATEGORY_FAIL',category=cat)
        elif v not in {'PASS','NOT_APPLICABLE'}: add(issues,'VIDEO_REALISM_CATEGORY_UNPROVEN',category=cat,observed=v)
    if ev.get('overall_verdict')!='PASS': add(issues,'VIDEO_REALISM_OVERALL_NOT_PASS',overall_verdict=ev.get('overall_verdict'))
    if ev.get('issue_codes'):
        add(issues,'VIDEO_REALISM_OPEN_ISSUES',issue_codes=ev.get('issue_codes'))
    if (qc or {}).get('realism_readiness')!='PASS': add(issues,'VIDEO_REALISM_QC_RUNTIME_NOT_PASS',realism_readiness=(qc or {}).get('realism_readiness'))
    return {'pass':not issues,'required_categories':sorted(required),'issues':issues}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--realism-contract',required=True); ap.add_argument('--video-runtime',required=True); ap.add_argument('--qc-runtime',required=True); a=ap.parse_args()
    out=lint(load(a.realism_contract),load(a.video_runtime),load(a.qc_runtime)); print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
