#!/usr/bin/env python3
"""V4.5.2 validator for Script-Grounded Virtual Set assets.

Checks asset justification, planning-diagram permissions, event/coverage parentage,
predictive/reciprocal coverage evidence, look-domain and required voice-identity freeze.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

def load(p):
    if not p: return None
    return yaml.safe_load(Path(p).read_text(encoding='utf-8'))

def lint(spatial, registry, obligations=None, phase='build'):
    issues=[]
    assets=(registry or {}).get('assets') or []
    asset_by={}
    for a in assets:
        aid=a.get('asset_id')
        if not aid: continue
        if aid in asset_by: issues.append({'type':'DUPLICATE_ASSET_ID','asset_id':aid})
        asset_by[aid]=a
    locs={x.get('location_entity_id'):x for x in (spatial or {}).get('locations') or []}
    diagrams={x.get('diagram_id'):x for x in (spatial or {}).get('planning_diagrams') or []}
    events={x.get('event_node_id'):x for x in (spatial or {}).get('event_nodes') or []}
    routes={x.get('route_id'):x for x in (spatial or {}).get('character_routes') or []}

    # Planning diagram evidence and permissions
    for did,d in diagrams.items():
        if d.get('status')=='APPROVED':
            aid=d.get('asset_id')
            if not aid or aid not in asset_by:
                issues.append({'type':'PLANNING_DIAGRAM_ASSET_MISSING','diagram_id':did,'asset_id':aid})
                continue
            a=asset_by[aid]
            if a.get('layout_type')!='PLANNING_DIAGRAM': issues.append({'type':'PLANNING_DIAGRAM_LAYOUT_TYPE_FAIL','asset_id':aid})
            vu=a.get('video_usage') or {}
            if vu.get('direct_input_allowed') or vu.get('primary_visual_eligible'):
                issues.append({'type':'PLANNING_DIAGRAM_VIDEO_AUTHORITY_FAIL','asset_id':aid})

    formal={'APPROVED','APPROVED_SUPPORT','APPROVED_ASSEMBLY','APPROVED_SCOPED_FIGURE','APPROVED_VIDEO_CONDITIONING'}
    exempt_types={'GLOBAL_COLOR_DNA','MIGRATION_RECORD','LEGACY_EXTERNAL_ASSET'}
    legacy_coverage_types={'DERIVED_COVERAGE_VIEW','EVENT_NODE_VIEW','RECIPROCAL_COVERAGE_VIEW','PREDICTIVE_COVERAGE_VIEW','SCENE_CLUE_VIEW','LOCATION_VISIBILITY_VIEW','LOCATION_IDENTITY_VIEW'}
    coverage_types={'ENVIRONMENT_COVERAGE'}|legacy_coverage_types
    if str((registry or {}).get('skill_version') or '') in {'4.5.7','4.5.11'}:
        for a in assets:
            if a.get('asset_type') in legacy_coverage_types:
                issues.append({'type':'LEGACY_COVERAGE_ASSET_REQUIRES_MIGRATION','asset_id':a.get('asset_id'),'asset_type':a.get('asset_type'),'required_current_type':'ENVIRONMENT_COVERAGE'})
    # Migration-safe scope: do not retroactively invalidate unrelated legacy Approved assets.
    # Current V4.5.2 assets are those referenced by this Spatial Canon/Obligation set or explicitly assigned a cascade_stage.
    current_asset_ids={d.get('asset_id') for d in diagrams.values() if d.get('asset_id')}
    for o in (obligations or {}).get('obligations') or []:
        current_asset_ids.update(o.get('fulfillment_asset_ids') or [])
    current_asset_ids.update(a.get('asset_id') for a in assets if a.get('cascade_stage') not in {None,'UNKNOWN'})
    voice_required=[]
    for a in assets:
        if a.get('status') not in formal: continue
        at=a.get('asset_type') or ''
        current=a.get('asset_id') in current_asset_ids
        # every current production asset should be justified; unrelated migrated assets are grandfathered until reused/rebuilt.
        if current and at not in exempt_types:
            j=a.get('justification') or {}
            if not (j.get('why_required') or '').strip(): issues.append({'type':'ASSET_WHY_REQUIRED_MISSING','asset_id':a.get('asset_id')})
            if not (j.get('required_by') or []): issues.append({'type':'ASSET_REQUIRED_BY_MISSING','asset_id':a.get('asset_id')})
            if not (j.get('downstream_use') or []): issues.append({'type':'ASSET_DOWNSTREAM_USE_MISSING','asset_id':a.get('asset_id')})
        # Coverage dual parentage
        if current and at in coverage_types:
            der=a.get('derivation') or {}
            if not der.get('spatial_parent_refs'): issues.append({'type':'COVERAGE_SPATIAL_PARENT_MISSING','asset_id':a.get('asset_id')})
            if not der.get('visual_parent_refs'): issues.append({'type':'COVERAGE_VISUAL_PARENT_MISSING','asset_id':a.get('asset_id')})
            reasons=set(der.get('coverage_reason_codes') or [])
            if (at=='EVENT_NODE_VIEW' or (at=='ENVIRONMENT_COVERAGE' and 'EVENT_NODE' in reasons)) and not der.get('event_node_ids'):
                issues.append({'type':'EVENT_VIEW_EVENT_NODE_MISSING','asset_id':a.get('asset_id')})
            if (at=='PREDICTIVE_COVERAGE_VIEW' or (at=='ENVIRONMENT_COVERAGE' and 'PREDICTIVE' in reasons)) and not der.get('predicted_shot_ids'):
                issues.append({'type':'PREDICTIVE_COVERAGE_NO_PREDICTED_USE','asset_id':a.get('asset_id')})
            if (at=='RECIPROCAL_COVERAGE_VIEW' or (at=='ENVIRONMENT_COVERAGE' and 'RECIPROCAL' in reasons)) and not der.get('reciprocal_relation_id'):
                issues.append({'type':'RECIPROCAL_COVERAGE_RELATION_MISSING','asset_id':a.get('asset_id')})
        # Look domain must be explicit for look cards
        if 'COLOR' in at or 'LOOK' in at:
            if a.get('cascade_stage')=='LOOK' and a.get('look_domain') in {None,'UNKNOWN'}:
                issues.append({'type':'LOOK_DOMAIN_MISSING','asset_id':a.get('asset_id')})
        # voice identities count only if approved and justified
        if at in {'VOICE_IDENTITY_ASSET','VOICE_MASTER','VOICE_REFERENCE'}:
            voice_required.append(a)

    # S/A spatial locations need approved planning evidence appropriate to kind
    if phase in {'spatial','freeze'}:
        approved_diagrams=list(diagrams.values())
        for lid,l in locs.items():
            if l.get('reuse_tier') not in {'S','A'}: continue
            kind=l.get('location_kind')
            acceptable={'OUTDOOR':{'OUTDOOR_TOPOLOGY','ROUTE_MAP'},'BUILDING':{'BUILDING_FLOOR_PLAN','ROOM_LAYOUT','ZONE_MAP'},'INTERIOR':{'BUILDING_FLOOR_PLAN','ROOM_LAYOUT','ZONE_MAP'},'VEHICLE':{'VEHICLE_LAYOUT','ZONE_MAP'},'MIXED':{'OUTDOOR_TOPOLOGY','BUILDING_FLOOR_PLAN','ROOM_LAYOUT','ZONE_MAP','ROUTE_MAP'}}.get(kind,set())
            ok=any(d.get('status')=='APPROVED' and lid in (d.get('scope_location_ids') or []) and d.get('diagram_type') in acceptable for d in approved_diagrams)
            if not ok: issues.append({'type':'REQUIRED_SPATIAL_PLANNING_DIAGRAM_MISSING','location_entity_id':lid,'reuse_tier':l.get('reuse_tier'),'location_kind':kind})
    # At freeze, all required voice obligations in registry must resolve; explicit exception assets can represent deferral.
    if phase=='freeze':
        # If a character voice requirement marker exists, it must be approved master/reference or explicit temp-sync exception.
        for a in assets:
            if a.get('asset_type')=='VOICE_REQUIREMENT':
                j=a.get('justification') or {}; status=a.get('status')
                mode=(a.get('voice_mode') or a.get('authority_role') or '')
                refs=a.get('parent_refs') or []
                if status not in formal:
                    issues.append({'type':'VOICE_REQUIREMENT_UNRESOLVED','asset_id':a.get('asset_id')})
                if 'TEMP_SYNC' not in mode and not refs:
                    issues.append({'type':'VOICE_IDENTITY_REFERENCE_MISSING','asset_id':a.get('asset_id')})
    return {'pass':not issues,'phase':phase,'asset_count':len(assets),'issues':issues}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--spatial-canon',required=True); ap.add_argument('--asset-registry',required=True); ap.add_argument('--obligations'); ap.add_argument('--phase',choices=['spatial','build','freeze'],default='build')
    a=ap.parse_args(); out=lint(load(a.spatial_canon),load(a.asset_registry),load(a.obligations),a.phase); print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
