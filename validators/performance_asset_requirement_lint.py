#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

APPROVED={'APPROVED','APPROVED_SUPPORT','APPROVED_SCOPED_FIGURE','APPROVED_ASSEMBLY'}
TYPE_MAP={
 'EXPRESSION_SUPPORT': {'PERFORMANCE_EXPRESSION_SUPPORT'},
 'ACTION_POSE_SUPPORT': {'PERFORMANCE_ACTION_POSE_SUPPORT'},
 'CONTACT_POSE_SUPPORT': {'PERFORMANCE_CONTACT_POSE_SUPPORT'},
}
PACK_TYPES={'PERFORMANCE_EXPRESSION_SUPPORT','PERFORMANCE_ACTION_POSE_SUPPORT','PERFORMANCE_CONTACT_POSE_SUPPORT'}

def load(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))
def add(issues,t,**kw): d={'type':t}; d.update(kw); issues.append(d)

def lint(reqset, registry, phase='freeze'):
    issues=[]
    assets={a.get('asset_id'):a for a in (registry.get('assets') or []) if a.get('asset_id')}
    seen=set()
    counts={'NONE':0,'EXPRESSION_SUPPORT':0,'ACTION_POSE_SUPPORT':0,'CONTACT_POSE_SUPPORT':0,'PERFORMANCE_SUPPORT_PACK':0}
    for r in reqset.get('requirements') or []:
        rid=r.get('requirement_id'); typ=r.get('requirement_type'); eid=r.get('entity_id'); status=r.get('status')
        if rid in seen: add(issues,'PERFORMANCE_REQUIREMENT_DUPLICATE_ID',requirement_id=rid)
        seen.add(rid); counts[typ]=counts.get(typ,0)+1
        aids=r.get('support_asset_ids') or []
        if typ=='NONE':
            if status!='NOT_REQUIRED': add(issues,'PERFORMANCE_NONE_STATUS_INVALID',requirement_id=rid,status=status)
            if aids: add(issues,'PERFORMANCE_NONE_HAS_SUPPORT_ASSET',requirement_id=rid,asset_ids=aids)
            continue
        if not (r.get('trigger_codes') or []): add(issues,'PERFORMANCE_REQUIREMENT_TRIGGER_MISSING',requirement_id=rid)
        if (typ=='CONTACT_POSE_SUPPORT' or (typ=='PERFORMANCE_SUPPORT_PACK' and 'CONTACT_RELATION' in (r.get('trigger_codes') or []))) and not (r.get('interaction_entity_ids') or []):
            add(issues,'PERFORMANCE_CONTACT_ENTITY_MISSING',requirement_id=rid)
        if phase=='freeze':
            if status!='APPROVED': add(issues,'PERFORMANCE_REQUIREMENT_NOT_APPROVED',requirement_id=rid,status=status)
            if not aids: add(issues,'PERFORMANCE_SUPPORT_REQUIRED_MISSING',requirement_id=rid,entity_id=eid)
        if not aids: continue
        found_types=[]
        for aid in aids:
            a=assets.get(aid)
            if not a:
                add(issues,'PERFORMANCE_SUPPORT_ASSET_MISSING',requirement_id=rid,asset_id=aid); continue
            found_types.append(a.get('asset_type'))
            if phase=='freeze' and a.get('status') not in APPROVED:
                add(issues,'PERFORMANCE_SUPPORT_NOT_APPROVED',requirement_id=rid,asset_id=aid,status=a.get('status'))
            if a.get('subject_entity_id')!=eid:
                add(issues,'PERFORMANCE_SUPPORT_ENTITY_MISMATCH',requirement_id=rid,asset_id=aid,expected=eid,actual=a.get('subject_entity_id'))
            if a.get('media_kind')!='IMAGE':
                add(issues,'PERFORMANCE_SUPPORT_MEDIA_KIND_FAIL',requirement_id=rid,asset_id=aid,actual=a.get('media_kind'))
            if a.get('authority_role')!='PERFORMANCE_SUPPORT_AUTHORITY':
                add(issues,'PERFORMANCE_SUPPORT_AUTHORITY_ROLE_FAIL',requirement_id=rid,asset_id=aid,actual=a.get('authority_role'))
            if (a.get('video_usage') or {}).get('primary_visual_eligible') is True:
                add(issues,'PERFORMANCE_SUPPORT_PRIMARY_VISUAL_FORBIDDEN',requirement_id=rid,asset_id=aid)
            if a.get('layout_type')=='MULTI_PANEL' and (a.get('video_usage') or {}).get('direct_input_allowed') is True:
                add(issues,'PERFORMANCE_MULTIPANEL_DIRECT_REFERENCE_FORBIDDEN',requirement_id=rid,asset_id=aid)
            if a.get('performance_requirement_id')!=rid:
                add(issues,'PERFORMANCE_REQUIREMENT_ASSET_REF_MISMATCH',requirement_id=rid,asset_id=aid,expected=rid,actual=a.get('performance_requirement_id'))
            if a.get('asset_type')=='PERFORMANCE_CONTACT_POSE_SUPPORT':
                required_interactions=set(r.get('interaction_entity_ids') or [])
                actual_interactions=set(a.get('performance_interaction_entity_ids') or [])
                if not actual_interactions:
                    add(issues,'PERFORMANCE_CONTACT_SUPPORT_INTERACTION_BINDING_MISSING',requirement_id=rid,asset_id=aid,required_interaction_entity_ids=sorted(required_interactions))
                wrong=sorted(actual_interactions-required_interactions)
                if wrong:
                    add(issues,'PERFORMANCE_CONTACT_SUPPORT_WRONG_INTERACTION_ENTITY',requirement_id=rid,asset_id=aid,unexpected_interaction_entity_ids=wrong,required_interaction_entity_ids=sorted(required_interactions))
        if typ in {'CONTACT_POSE_SUPPORT','PERFORMANCE_SUPPORT_PACK'} and (r.get('interaction_entity_ids') or []):
            required_interactions=set(r.get('interaction_entity_ids') or [])
            covered_interactions=set()
            for aid in aids:
                a=assets.get(aid) or {}
                if a.get('asset_type')=='PERFORMANCE_CONTACT_POSE_SUPPORT':
                    covered_interactions.update(a.get('performance_interaction_entity_ids') or [])
            missing_interactions=sorted(required_interactions-covered_interactions)
            if missing_interactions:
                add(issues,'PERFORMANCE_CONTACT_SUPPORT_INTERACTION_COVERAGE_GAP',requirement_id=rid,missing_interaction_entity_ids=missing_interactions,covered_interaction_entity_ids=sorted(covered_interactions))
        if typ in TYPE_MAP:
            allowed=TYPE_MAP[typ]
            if not any(t in allowed for t in found_types):
                add(issues,'PERFORMANCE_SUPPORT_TYPE_MISMATCH',requirement_id=rid,required_type=typ,found_types=found_types)
        elif typ=='PERFORMANCE_SUPPORT_PACK':
            ft=set(found_types)
            if 'PERFORMANCE_EXPRESSION_SUPPORT' not in ft or not (ft & {'PERFORMANCE_ACTION_POSE_SUPPORT','PERFORMANCE_CONTACT_POSE_SUPPORT'}):
                add(issues,'PERFORMANCE_SUPPORT_PACK_INCOMPLETE',requirement_id=rid,found_types=found_types)
            for t in ft:
                if t not in PACK_TYPES: add(issues,'PERFORMANCE_SUPPORT_TYPE_MISMATCH',requirement_id=rid,required_type=typ,found_type=t)
    if phase=='freeze' and reqset.get('status')!='FROZEN':
        add(issues,'PERFORMANCE_ASSET_REQUIREMENT_SET_NOT_FROZEN',status=reqset.get('status'))
    return {'pass':not issues,'phase':phase,'counts':counts,'issues':issues}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--requirements',required=True); ap.add_argument('--asset-registry',required=True); ap.add_argument('--phase',choices=['planning','build','freeze'],default='freeze'); a=ap.parse_args()
    out=lint(load(a.requirements),load(a.asset_registry),a.phase); print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
