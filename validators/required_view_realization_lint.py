#!/usr/bin/env python3
"""V4.5.4 Required View Realization Gate.

Closes the gap between declared scene/event coverage needs and actually generated,
visually verified assets. A required view is not complete merely because a prompt,
asset filename, or planning diagram says it exists.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

FORMAL_APPROVED={
    'APPROVED','APPROVED_SUPPORT','APPROVED_ASSEMBLY',
    'APPROVED_SCOPED_FIGURE','APPROVED_VIDEO_CONDITIONING'
}
ACTIVE_STATUSES=FORMAL_APPROVED|{'DRAFT','QC_PASS_WAITING_APPROVAL'}
LEGACY_COVERAGE_TYPES={
    'DERIVED_COVERAGE_VIEW','EVENT_NODE_VIEW','RECIPROCAL_COVERAGE_VIEW',
    'PREDICTIVE_COVERAGE_VIEW','SCENE_CLUE_VIEW','LOCATION_VISIBILITY_VIEW','LOCATION_IDENTITY_VIEW'
}
COVERAGE_TYPES=LEGACY_COVERAGE_TYPES|{'ENVIRONMENT_COVERAGE'}
DIRECTIONAL_ROLES={'FORWARD','REVERSE','ENTRY','EXIT','LOOK_BACK','LANDMARK','CLUE','DETAIL','OTHER'}


def load(path):
    if not path:
        return None
    return yaml.safe_load(Path(path).read_text(encoding='utf-8'))


def evidence_index(evidence):
    out={}
    for r in (evidence or {}).get('records') or []:
        aid=r.get('asset_id')
        if aid:
            out[aid]=r
    return out


def current_evidence(asset, record):
    if not record or record.get('evidence_status')!='CURRENT':
        return False
    return bool(asset.get('fingerprint') and record.get('source_fingerprint') and asset.get('fingerprint')==record.get('source_fingerprint'))


def requirement_index(spatial):
    reqs={}; dup=[]
    for r in (spatial or {}).get('view_requirements') or []:
        rid=r.get('view_requirement_id')
        if not rid:
            continue
        if rid in reqs:
            dup.append(rid)
        reqs[rid]=r
    return reqs,dup


def lint(spatial, registry, evidence=None, phase='planning'):
    issues=[]; warnings=[]
    assets=(registry or {}).get('assets') or []
    if str((registry or {}).get('skill_version') or '') in {'4.5.7','4.5.11'}:
        for a in assets:
            if a.get('asset_type') in LEGACY_COVERAGE_TYPES:
                issues.append({'type':'LEGACY_COVERAGE_ASSET_REQUIRES_MIGRATION','asset_id':a.get('asset_id'),'asset_type':a.get('asset_type'),'required_current_type':'ENVIRONMENT_COVERAGE'})
    asset_by={a.get('asset_id'):a for a in assets if a.get('asset_id')}
    events={x.get('event_node_id'):x for x in (spatial or {}).get('event_nodes') or [] if x.get('event_node_id')}
    locations={x.get('location_entity_id'):x for x in (spatial or {}).get('locations') or [] if x.get('location_entity_id')}
    anchors=set()
    for l in locations.values():
        for a in l.get('anchors') or []:
            if a.get('anchor_id'): anchors.add(a.get('anchor_id'))
    reqs,dup=requirement_index(spatial)
    evidence_by=evidence_index(evidence)
    for rid in dup:
        issues.append({'type':'DUPLICATE_VIEW_REQUIREMENT_ID','view_requirement_id':rid})

    skill=str((spatial or {}).get('skill_version') or '')
    if skill in {'4.5.4','4.5.5','4.5.6','4.5.7','4.5.11'} and not reqs:
        issues.append({'type':'REQUIRED_VIEW_SET_MISSING','message':'V4.5.4+ requires materialized view_requirements before Stage 03 asset generation.'})

    # Every event shorthand required_view_role must be materialized into a concrete requirement.
    for eid,e in events.items():
        for role in e.get('required_view_roles') or []:
            matches=[r for r in reqs.values() if role==r.get('view_role') and eid in (r.get('event_node_ids') or []) and r.get('status')!='WAIVED']
            if not matches:
                issues.append({'type':'EVENT_REQUIRED_VIEW_UNMATERIALIZED','event_node_id':eid,'view_role':role})

    # Requirement integrity.
    for rid,r in reqs.items():
        lid=r.get('location_entity_id')
        if lid not in locations:
            issues.append({'type':'VIEW_REQUIREMENT_UNKNOWN_LOCATION','view_requirement_id':rid,'location_entity_id':lid})
        for eid in r.get('event_node_ids') or []:
            if eid not in events:
                issues.append({'type':'VIEW_REQUIREMENT_UNKNOWN_EVENT_NODE','view_requirement_id':rid,'event_node_id':eid})
        for aid in [r.get('camera_origin_anchor_id'),r.get('view_target_anchor_id')]+list(r.get('required_visible_anchor_ids') or [])+list(r.get('forbidden_visible_anchor_ids') or []):
            if aid and aid not in anchors:
                issues.append({'type':'VIEW_REQUIREMENT_UNKNOWN_ANCHOR','view_requirement_id':rid,'anchor_id':aid})
        if r.get('status')=='WAIVED' and not r.get('waiver_ref'):
            issues.append({'type':'VIEW_REQUIREMENT_WAIVER_WITHOUT_AUTHORITY','view_requirement_id':rid})
        if r.get('status') in {'REQUIRED','FULFILLED'}:
            role=r.get('view_role')
            if role in DIRECTIONAL_ROLES:
                has_origin=bool(r.get('camera_origin_zone_id') or r.get('camera_origin_anchor_id'))
                has_target=bool(r.get('view_target_entity_id') or r.get('view_target_anchor_id') or r.get('view_direction_code') or r.get('required_visible_anchor_ids'))
                if not has_origin:
                    issues.append({'type':'VIEW_REQUIREMENT_CAMERA_ORIGIN_MISSING','view_requirement_id':rid,'view_role':role})
                if not has_target:
                    issues.append({'type':'VIEW_REQUIREMENT_OPTICAL_AXIS_UNDERSPECIFIED','view_requirement_id':rid,'view_role':role})

    # Candidate assets must be linked to a concrete view requirement rather than vague scene names.
    coverage_assets=[]
    for a in assets:
        if a.get('asset_type') not in COVERAGE_TYPES or a.get('status') not in ACTIVE_STATUSES:
            continue
        coverage_assets.append(a)
        linked=(a.get('derivation') or {}).get('view_requirement_ids') or []
        if skill in {'4.5.4','4.5.5','4.5.6','4.5.7','4.5.11'} and not linked:
            issues.append({'type':'COVERAGE_ASSET_UNLINKED_TO_VIEW_REQUIREMENT','asset_id':a.get('asset_id')})
        for rid in linked:
            if rid not in reqs:
                issues.append({'type':'COVERAGE_ASSET_UNKNOWN_VIEW_REQUIREMENT','asset_id':a.get('asset_id'),'view_requirement_id':rid})

    if phase in {'build','freeze'}:
        candidates={rid:[] for rid in reqs}
        for a in coverage_assets:
            for rid in (a.get('derivation') or {}).get('view_requirement_ids') or []:
                if rid in candidates:
                    candidates[rid].append(a)

        required=[r for r in reqs.values() if r.get('status') in {'REQUIRED','FULFILLED'}]
        missing=[]
        for r in required:
            rid=r['view_requirement_id']; cands=candidates.get(rid) or []
            if not cands:
                missing.append(rid)
                issues.append({'type':'REQUIRED_VIEW_ASSET_MISSING','view_requirement_id':rid,'location_entity_id':r.get('location_entity_id'),'view_role':r.get('view_role')})
                continue
            # planned metadata must match the requirement; image evidence is checked later.
            for a in cands:
                aid=a.get('asset_id'); der=a.get('derivation') or {}
                if a.get('location_entity_id')!=r.get('location_entity_id'):
                    issues.append({'type':'VIEW_ASSET_LOCATION_MISMATCH','view_requirement_id':rid,'asset_id':aid})
                # V4.5.5: a correct camera direction is not sufficient. The concrete view must inherit
                # every Everyday Realism Contract attached to the requirement so it cannot escape
                # cast/seat/vehicle/ergonomic plausibility checks by omitting the realism back-reference.
                expected_realism=set(r.get('realism_contract_ids') or [])
                actual_realism=set(a.get('realism_contract_ids') or [])
                missing_realism=expected_realism-actual_realism
                if missing_realism:
                    issues.append({'type':'VIEW_ASSET_REALISM_CONTRACT_GAP','view_requirement_id':rid,'asset_id':aid,'missing_realism_contract_ids':sorted(missing_realism)})
                if der.get('view_role') and der.get('view_role')!=r.get('view_role'):
                    issues.append({'type':'VIEW_ASSET_ROLE_METADATA_MISMATCH','view_requirement_id':rid,'asset_id':aid,'expected':r.get('view_role'),'actual':der.get('view_role')})
                for key in ['camera_origin_zone_id','camera_origin_anchor_id','view_target_entity_id','view_target_anchor_id','view_direction_code']:
                    expected=r.get(key); actual=der.get(key)
                    if expected and actual!=expected:
                        issues.append({'type':'VIEW_ASSET_AXIS_METADATA_MISMATCH','view_requirement_id':rid,'asset_id':aid,'field':key,'expected':expected,'actual':actual})
                reqanchors=set(r.get('required_visible_anchor_ids') or [])
                metaanchors=set(der.get('required_visible_anchor_ids') or [])
                if reqanchors-metaanchors:
                    issues.append({'type':'VIEW_ASSET_REQUIRED_ANCHOR_METADATA_GAP','view_requirement_id':rid,'asset_id':aid,'missing_anchor_ids':sorted(reqanchors-metaanchors)})
            # Budget starvation: don't spend many attempts on one direction while another required direction has zero candidates.
            budget=int(r.get('candidate_budget') or 4)
            if len(cands)>budget:
                warnings.append({'type':'VIEW_REQUIREMENT_CANDIDATE_BUDGET_EXCEEDED','view_requirement_id':rid,'candidate_count':len(cands),'candidate_budget':budget})

        if missing:
            for r in required:
                rid=r['view_requirement_id']; cands=candidates.get(rid) or []; budget=int(r.get('candidate_budget') or 4)
                if len(cands)>budget:
                    issues.append({'type':'COVERAGE_BUDGET_STARVES_REQUIRED_VIEW','view_requirement_id':rid,'candidate_count':len(cands),'candidate_budget':budget,'still_missing_view_requirement_ids':sorted(missing)})

    if phase=='freeze':
        for r in reqs.values():
            if r.get('status') not in {'REQUIRED','FULFILLED'}:
                continue
            rid=r['view_requirement_id']
            selected=r.get('selected_fulfillment_asset_id')
            if not selected:
                issues.append({'type':'REQUIRED_VIEW_FULFILLMENT_NOT_SELECTED','view_requirement_id':rid})
                continue
            a=asset_by.get(selected)
            if not a:
                issues.append({'type':'REQUIRED_VIEW_SELECTED_ASSET_MISSING','view_requirement_id':rid,'asset_id':selected}); continue
            if a.get('status') not in FORMAL_APPROVED:
                issues.append({'type':'REQUIRED_VIEW_SELECTED_ASSET_NOT_APPROVED','view_requirement_id':rid,'asset_id':selected,'status':a.get('status')})
            linked=(a.get('derivation') or {}).get('view_requirement_ids') or []
            if rid not in linked:
                issues.append({'type':'REQUIRED_VIEW_SELECTED_ASSET_NOT_LINKED','view_requirement_id':rid,'asset_id':selected})
            expected_realism=set(r.get('realism_contract_ids') or [])
            actual_realism=set(a.get('realism_contract_ids') or [])
            missing_realism=expected_realism-actual_realism
            if missing_realism:
                issues.append({'type':'REQUIRED_VIEW_REALISM_CONTRACT_GAP','view_requirement_id':rid,'asset_id':selected,'missing_realism_contract_ids':sorted(missing_realism)})
            if expected_realism and a.get('realism_qc_status')!='PASS':
                issues.append({'type':'REQUIRED_VIEW_REALISM_QC_NOT_PASS','view_requirement_id':rid,'asset_id':selected,'realism_qc_status':a.get('realism_qc_status')})
            rec=evidence_by.get(selected)
            if not current_evidence(a,rec):
                issues.append({'type':'REQUIRED_VIEW_VISUAL_EVIDENCE_MISSING_OR_STALE','view_requirement_id':rid,'asset_id':selected})
                continue
            obs=rec.get('observed') or {}; sp=obs.get('spatial') or {}
            roles=set(sp.get('view_roles') or ([] if not sp.get('view_role') else [sp.get('view_role')]))
            if r.get('view_role') not in roles:
                issues.append({'type':'REQUIRED_VIEW_ROLE_VISUALLY_UNPROVEN','view_requirement_id':rid,'asset_id':selected,'expected':r.get('view_role'),'observed':sorted(roles)})
            for key in ['camera_origin_zone_id','camera_origin_anchor_id','view_target_entity_id','view_target_anchor_id','view_direction_code']:
                expected=r.get(key)
                if expected:
                    actual=sp.get(key)
                    if actual!=expected:
                        issues.append({'type':'REQUIRED_VIEW_AXIS_VISUALLY_UNPROVEN','view_requirement_id':rid,'asset_id':selected,'field':key,'expected':expected,'observed':actual})
            visible=set(sp.get('visible_anchor_ids') or [])
            reqanchors=set(r.get('required_visible_anchor_ids') or [])
            miss=reqanchors-visible
            if miss:
                issues.append({'type':'REQUIRED_VIEW_VISIBLE_ANCHOR_GAP','view_requirement_id':rid,'asset_id':selected,'missing_anchor_ids':sorted(miss)})
            bad=visible & set(r.get('forbidden_visible_anchor_ids') or [])
            if bad:
                issues.append({'type':'REQUIRED_VIEW_FORBIDDEN_ANCHOR_VISIBLE','view_requirement_id':rid,'asset_id':selected,'anchor_ids':sorted(bad)})
            visible_entities=set(sp.get('visible_location_entity_ids') or [])
            if r.get('view_target_entity_id') and r.get('view_target_entity_id') not in visible_entities:
                issues.append({'type':'REQUIRED_VIEW_TARGET_ENTITY_NOT_VISUALLY_PROVEN','view_requirement_id':rid,'asset_id':selected,'target_entity_id':r.get('view_target_entity_id')})
            facts=set(obs.get('fact_codes') or []); issues_seen=set(obs.get('issue_codes') or [])
            missfacts=set(r.get('required_visual_fact_codes') or [])-facts
            if missfacts:
                issues.append({'type':'REQUIRED_VIEW_VISUAL_FACT_GAP','view_requirement_id':rid,'asset_id':selected,'missing_fact_codes':sorted(missfacts)})
            conflicts=(facts|issues_seen)&set(r.get('forbidden_visual_fact_codes') or [])
            if conflicts:
                issues.append({'type':'REQUIRED_VIEW_VISUAL_FACT_CONFLICT','view_requirement_id':rid,'asset_id':selected,'conflict_codes':sorted(conflicts)})

    return {
        'pass': not issues,
        'phase': phase,
        'view_requirement_count': len(reqs),
        'issues': issues,
        'warnings': warnings,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--spatial-canon',required=True)
    ap.add_argument('--asset-registry',required=True)
    ap.add_argument('--visual-evidence')
    ap.add_argument('--phase',choices=['planning','build','freeze'],default='planning')
    a=ap.parse_args()
    out=lint(load(a.spatial_canon),load(a.asset_registry),load(a.visual_evidence) if a.visual_evidence else None,a.phase)
    print(json.dumps(out,ensure_ascii=False,indent=2))
    raise SystemExit(0 if out['pass'] else 2)

if __name__=='__main__':
    main()
