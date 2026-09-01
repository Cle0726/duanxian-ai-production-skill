#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

APPROVED={'APPROVED','APPROVED_SUPPORT','APPROVED_ASSEMBLY','APPROVED_SCOPED_FIGURE','APPROVED_VIDEO_CONDITIONING'}
CURRENT_STAGE03_TYPES={
 'EMPTY_ENVIRONMENT_MASTER','FUNCTIONAL_MINOR_HUMAN_MASTER','DERIVED_COVERAGE','ENVIRONMENT_COVERAGE','PRODUCTION_SUPPORT_REFERENCE','SHOT_ASSEMBLY','SCENE_LOOK_CARD','PERFORMANCE_EXPRESSION_SUPPORT','PERFORMANCE_ACTION_POSE_SUPPORT','PERFORMANCE_CONTACT_POSE_SUPPORT','NARRATIVE_FX_REFERENCE'
}
LEGACY_COVERAGE_OBLIGATION_TYPES={
 'SCENE_CLUE_VIEW','LOCATION_VISIBILITY_VIEW','LOCATION_IDENTITY_VIEW','EVENT_NODE_VIEW','RECIPROCAL_COVERAGE_VIEW','PREDICTIVE_COVERAGE_VIEW'
}

def load(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))
def add(issues,t,**kw): d={'type':t}; d.update(kw); issues.append(d)

def lint(base, perf, fx, obligations, registry, phase='freeze'):
    issues=[]
    assets={a.get('asset_id'):a for a in (registry.get('assets') or []) if a.get('asset_id')}
    if phase=='freeze' and base.get('status')!='FROZEN': add(issues,'ASSET_LIBRARY_BASE_VISUAL_NOT_FROZEN',status=base.get('status'))
    if phase=='freeze' and perf.get('status')!='FROZEN': add(issues,'ASSET_LIBRARY_PERFORMANCE_SET_NOT_FROZEN',status=perf.get('status'))
    if phase=='freeze' and fx.get('status')!='FROZEN': add(issues,'ASSET_LIBRARY_NARRATIVE_FX_NOT_FROZEN',status=fx.get('status'))
    unresolved=[]; missing_assets=[]
    current_v457=str(obligations.get('skill_version') or '') in {'4.5.7','4.5.11'}
    for o in obligations.get('obligations') or []:
        otype=o.get('obligation_type')
        if current_v457 and otype in LEGACY_COVERAGE_OBLIGATION_TYPES:
            add(issues,'LEGACY_COVERAGE_OBLIGATION_REQUIRES_MIGRATION',obligation_id=o.get('obligation_id'),obligation_type=otype,required_current_type='ENVIRONMENT_COVERAGE')
            continue
        active_types=CURRENT_STAGE03_TYPES if current_v457 else (CURRENT_STAGE03_TYPES|LEGACY_COVERAGE_OBLIGATION_TYPES)
        if o.get('fulfill_by')!='STAGE_03_FREEZE' or otype not in active_types: continue
        if o.get('status')=='WAIVED':
            if o.get('waiver_policy')=='NON_WAIVABLE': add(issues,'ASSET_LIBRARY_NON_WAIVABLE_OBLIGATION_WAIVED',obligation_id=o.get('obligation_id'))
            continue
        if o.get('status')!='FULFILLED' or o.get('proof_status')!='PASS':
            unresolved.append(o.get('obligation_id')); continue
        for aid in o.get('fulfillment_asset_ids') or []:
            a=assets.get(aid)
            if not a: missing_assets.append(aid); continue
            if a.get('status') not in APPROVED: add(issues,'ASSET_LIBRARY_REFERENCED_ASSET_NOT_APPROVED',obligation_id=o.get('obligation_id'),asset_id=aid,status=a.get('status'))
    if unresolved: add(issues,'ASSET_LIBRARY_STAGE03_OBLIGATIONS_UNRESOLVED',obligation_ids=sorted(x for x in unresolved if x))
    if missing_assets: add(issues,'ASSET_LIBRARY_FULFILLMENT_ASSET_MISSING',asset_ids=sorted(set(missing_assets)))
    for r in perf.get('requirements') or []:
        if r.get('requirement_type')!='NONE' and r.get('status')!='APPROVED':
            add(issues,'ASSET_LIBRARY_PERFORMANCE_REQUIREMENT_OPEN',requirement_id=r.get('requirement_id'),status=r.get('status'))
    for e in fx.get('effects') or []:
        if e.get('authority_mode')=='NARRATIVE_FX_REFERENCE' and e.get('status')!='APPROVED':
            add(issues,'ASSET_LIBRARY_NARRATIVE_FX_REQUIREMENT_OPEN',narrative_fx_id=e.get('narrative_fx_id'),status=e.get('status'))
    return {'pass':not issues,'phase':phase,'policy':'RICH_CANON_LIBRARY__MINIMUM_EXECUTION_PACK','stage03_obligation_count':sum(1 for o in obligations.get('obligations') or [] if o.get('fulfill_by')=='STAGE_03_FREEZE'),'registry_asset_count':len(assets),'issues':issues}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--base-visual-manifest',required=True); ap.add_argument('--performance-requirements',required=True); ap.add_argument('--narrative-fx-manifest',required=True); ap.add_argument('--obligations',required=True); ap.add_argument('--asset-registry',required=True); ap.add_argument('--phase',choices=['build','freeze'],default='freeze'); a=ap.parse_args()
    out=lint(load(a.base_visual_manifest),load(a.performance_requirements),load(a.narrative_fx_manifest),load(a.obligations),load(a.asset_registry),a.phase); print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
