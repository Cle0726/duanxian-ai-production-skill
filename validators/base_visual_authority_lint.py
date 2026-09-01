#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

APPROVED={'APPROVED','APPROVED_SCOPED_FIGURE','APPROVED_SUPPORT','APPROVED_ASSEMBLY'}
ENV_TYPES={'ENVIRONMENT_CLEAN_CANON','ENV_CANON_MASTER','EMPTY_ENVIRONMENT_MASTER'}
HUMAN_TYPES={'FUNCTIONAL_MINOR_HUMAN_ASSET','MINOR_HUMAN_MASTER'}

def load(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))
def add(issues,t,**kw): d={'type':t}; d.update(kw); issues.append(d)

def lint(manifest, spatial, obligations, registry, phase='freeze'):
    issues=[]
    assets={a.get('asset_id'):a for a in (registry.get('assets') or []) if a.get('asset_id')}
    obs={o.get('obligation_id'):o for o in (obligations.get('obligations') or []) if o.get('obligation_id')}
    envs=manifest.get('environments') or []
    humans=manifest.get('minor_humans') or []
    actor_index=manifest.get('actor_authority_index') or []

    # Management/dedup invariants.
    for label,items,idkey in [('environment',envs,'location_entity_id'),('minor_human',humans,'entity_id')]:
        seen_id={}; seen_reuse={}
        for item in items:
            eid=item.get(idkey); rk=item.get('reuse_key')
            if eid in seen_id: add(issues,'BASE_VISUAL_DUPLICATE_ENTITY_REQUIREMENT',kind=label,entity_id=eid)
            else: seen_id[eid]=item
            if rk in seen_reuse and seen_reuse[rk].get(idkey)!=eid:
                add(issues,'BASE_VISUAL_REUSE_KEY_COLLISION',kind=label,reuse_key=rk,entities=[seen_reuse[rk].get(idkey),eid])
            else: seen_reuse[rk]=item

    # Every actor referenced by formal event nodes must be classified, so a one-shot supporting actor cannot disappear from asset planning.
    event_actor_ids={aid for e in (spatial.get('event_nodes') or []) for aid in (e.get('actor_ids') or []) if aid}
    actor_seen={}
    for rec in actor_index:
        eid=rec.get('entity_id')
        if not eid: continue
        if eid in actor_seen:
            add(issues,'ACTOR_BASE_AUTHORITY_DUPLICATE_ENTITY',entity_id=eid,first_actor_class=actor_seen[eid].get('actor_class'),duplicate_actor_class=rec.get('actor_class'))
        else:
            actor_seen[eid]=rec
    actor_by=actor_seen
    for aid in sorted(event_actor_ids):
        if aid not in actor_by:
            add(issues,'ACTOR_BASE_AUTHORITY_CLASSIFICATION_MISSING',entity_id=aid)
    minor_by_req={x.get('requirement_id'):x for x in humans if x.get('requirement_id')}
    minor_by_entity={x.get('entity_id'):x for x in humans if x.get('entity_id')}
    for rec in actor_index:
        eid=rec.get('entity_id'); cls=rec.get('actor_class'); kind=rec.get('authority_kind'); read=rec.get('readability')
        if cls=='MINOR_HUMAN':
            if kind!='FMH_ASSET' and read!='DEEP_BACKGROUND': add(issues,'ACTOR_MINOR_HUMAN_AUTHORITY_KIND_INVALID',entity_id=eid,actual=kind)
            req=minor_by_entity.get(eid)
            if not req: add(issues,'ACTOR_MINOR_HUMAN_REQUIREMENT_MISSING',entity_id=eid)
            elif rec.get('minor_human_requirement_id') and rec.get('minor_human_requirement_id')!=req.get('requirement_id'):
                add(issues,'ACTOR_MINOR_HUMAN_REQUIREMENT_REF_MISMATCH',entity_id=eid,expected=req.get('requirement_id'),actual=rec.get('minor_human_requirement_id'))
        elif cls=='CHARACTER_CANON' and kind!='CHARACTER_AUTHORITY':
            add(issues,'ACTOR_CHARACTER_AUTHORITY_KIND_INVALID',entity_id=eid,actual=kind)
        elif cls=='CROWD_CLUSTER':
            if read=='DEEP_BACKGROUND' and kind not in {'TEXT_ONLY','CROWD_ARCHETYPE_SET'}: add(issues,'ACTOR_CROWD_AUTHORITY_KIND_INVALID',entity_id=eid,actual=kind)
            if read!='DEEP_BACKGROUND' and kind!='CROWD_ARCHETYPE_SET': add(issues,'ACTOR_CROWD_ARCHETYPE_REQUIRED',entity_id=eid,actual=kind)

    # Every formal visual location used by an event node requires an empty environment master.
    formal_locations={e.get('location_entity_id') for e in (spatial.get('event_nodes') or []) if e.get('location_entity_id')}
    env_by={e.get('location_entity_id'):e for e in envs}
    for lid in sorted(formal_locations):
        if lid not in env_by:
            add(issues,'EMPTY_ENVIRONMENT_MASTER_REQUIREMENT_MISSING',location_entity_id=lid)
    for req in envs:
        lid=req.get('location_entity_id'); aid=req.get('empty_master_asset_id'); oid=req.get('obligation_id')
        ob=obs.get(oid)
        if not ob: add(issues,'EMPTY_ENVIRONMENT_MASTER_OBLIGATION_MISSING',location_entity_id=lid,obligation_id=oid)
        else:
            if ob.get('obligation_type')!='EMPTY_ENVIRONMENT_MASTER': add(issues,'EMPTY_ENVIRONMENT_MASTER_OBLIGATION_TYPE_FAIL',location_entity_id=lid,actual=ob.get('obligation_type'))
            if ob.get('fulfill_by')!='STAGE_03_FREEZE': add(issues,'BASE_VISUAL_OBLIGATION_DUE_STAGE_INVALID',obligation_id=oid,actual=ob.get('fulfill_by'))
            if aid not in (ob.get('fulfillment_asset_ids') or []): add(issues,'EMPTY_ENVIRONMENT_MASTER_OBLIGATION_ASSET_MISMATCH',location_entity_id=lid,asset_id=aid)
            if phase=='freeze' and (ob.get('status')!='FULFILLED' or ob.get('proof_status')!='PASS'):
                add(issues,'EMPTY_ENVIRONMENT_MASTER_OBLIGATION_NOT_CLOSED',obligation_id=oid,status=ob.get('status'),proof_status=ob.get('proof_status'))
        a=assets.get(aid)
        if not a: add(issues,'EMPTY_ENVIRONMENT_MASTER_ASSET_MISSING',location_entity_id=lid,asset_id=aid); continue
        if a.get('status') not in APPROVED: add(issues,'EMPTY_ENVIRONMENT_MASTER_NOT_APPROVED',asset_id=aid,status=a.get('status'))
        if a.get('asset_type') not in ENV_TYPES: add(issues,'EMPTY_ENVIRONMENT_MASTER_TYPE_FAIL',asset_id=aid,actual=a.get('asset_type'))
        if a.get('location_entity_id')!=lid: add(issues,'EMPTY_ENVIRONMENT_MASTER_LOCATION_MISMATCH',asset_id=aid,expected=lid,actual=a.get('location_entity_id'))
        if a.get('transient_content_policy')!='CLEAN_CANON': add(issues,'EMPTY_ENVIRONMENT_MASTER_NOT_CLEAN_CANON',asset_id=aid)
        if a.get('population_policy')!='EMPTY_ENVIRONMENT_ONLY': add(issues,'EMPTY_ENVIRONMENT_MASTER_POPULATION_POLICY_FAIL',asset_id=aid,actual=a.get('population_policy'))
        if a.get('readable_human_count') != 0: add(issues,'EMPTY_ENVIRONMENT_MASTER_HUMAN_COUNT_NOT_EXPLICIT_ZERO',asset_id=aid,count=a.get('readable_human_count'))
        if (a.get('video_usage') or {}).get('primary_visual_eligible') is True: add(issues,'BASE_MASTER_PRIMARY_VISUAL_FORBIDDEN',asset_id=aid)

    # Every readable scoped/minor human must own a standalone human master before storyboard/video.
    for req in humans:
        eid=req.get('entity_id'); readable=req.get('readability')!='DEEP_BACKGROUND'
        if not readable:
            if req.get('visual_owner')!='TEXT_ONLY': add(issues,'DEEP_BACKGROUND_OWNER_INVALID',entity_id=eid,actual=req.get('visual_owner'))
            continue
        if req.get('visual_owner')!='FMH_ASSET': add(issues,'READABLE_MINOR_HUMAN_OWNER_MUST_BE_FMH_ASSET',entity_id=eid,actual=req.get('visual_owner'))
        aid=req.get('human_master_asset_id'); oid=req.get('obligation_id')
        if not aid: add(issues,'FUNCTIONAL_MINOR_HUMAN_MASTER_ID_MISSING',entity_id=eid); continue
        ob=obs.get(oid)
        if not ob: add(issues,'FUNCTIONAL_MINOR_HUMAN_MASTER_OBLIGATION_MISSING',entity_id=eid,obligation_id=oid)
        else:
            if ob.get('obligation_type')!='FUNCTIONAL_MINOR_HUMAN_MASTER': add(issues,'FUNCTIONAL_MINOR_HUMAN_MASTER_OBLIGATION_TYPE_FAIL',entity_id=eid,actual=ob.get('obligation_type'))
            if ob.get('fulfill_by')!='STAGE_03_FREEZE': add(issues,'BASE_VISUAL_OBLIGATION_DUE_STAGE_INVALID',obligation_id=oid,actual=ob.get('fulfill_by'))
            if aid not in (ob.get('fulfillment_asset_ids') or []): add(issues,'FUNCTIONAL_MINOR_HUMAN_MASTER_OBLIGATION_ASSET_MISMATCH',entity_id=eid,asset_id=aid)
            if phase=='freeze' and (ob.get('status')!='FULFILLED' or ob.get('proof_status')!='PASS'):
                add(issues,'FUNCTIONAL_MINOR_HUMAN_MASTER_OBLIGATION_NOT_CLOSED',obligation_id=oid,status=ob.get('status'),proof_status=ob.get('proof_status'))
        a=assets.get(aid)
        if not a: add(issues,'FUNCTIONAL_MINOR_HUMAN_MASTER_ASSET_MISSING',entity_id=eid,asset_id=aid); continue
        if a.get('status') not in APPROVED: add(issues,'FUNCTIONAL_MINOR_HUMAN_MASTER_NOT_APPROVED',entity_id=eid,asset_id=aid,status=a.get('status'))
        if a.get('asset_type') not in HUMAN_TYPES: add(issues,'FUNCTIONAL_MINOR_HUMAN_MASTER_TYPE_FAIL',entity_id=eid,asset_id=aid,actual=a.get('asset_type'))
        if a.get('subject_entity_id')!=eid: add(issues,'FUNCTIONAL_MINOR_HUMAN_MASTER_ENTITY_MISMATCH',asset_id=aid,expected=eid,actual=a.get('subject_entity_id'))
        if a.get('layout_type')!='SINGLE_FRAME': add(issues,'FUNCTIONAL_MINOR_HUMAN_MASTER_LAYOUT_FAIL',asset_id=aid,actual=a.get('layout_type'))
        if (a.get('video_usage') or {}).get('primary_visual_eligible') is True: add(issues,'BASE_MASTER_PRIMARY_VISUAL_FORBIDDEN',asset_id=aid)

    if phase=='freeze' and manifest.get('status')!='FROZEN': add(issues,'BASE_VISUAL_AUTHORITY_MANIFEST_NOT_FROZEN',status=manifest.get('status'))
    return {'pass':not issues,'phase':phase,'formal_location_count':len(formal_locations),'environment_requirement_count':len(envs),'minor_human_requirement_count':len(humans),'actor_authority_index_count':len(actor_index),'issues':issues}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--manifest',required=True); ap.add_argument('--spatial-canon',required=True); ap.add_argument('--obligations',required=True); ap.add_argument('--asset-registry',required=True); ap.add_argument('--phase',choices=['build','freeze'],default='freeze'); a=ap.parse_args()
    out=lint(load(a.manifest),load(a.spatial_canon),load(a.obligations),load(a.asset_registry),a.phase); print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
