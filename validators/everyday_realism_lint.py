#!/usr/bin/env python3
"""Validate REALISM_CONTRACT lifecycle, coverage, scoped exceptions and pixel-derived reality.

V4.5.6 closes four failure classes that are expensive in production:
1) an ordinary image cannot escape Reality-by-Default by omitting its contract binding;
2) an asset cannot borrow another shot/asset's scoped exception merely by naming its id;
3) planning QC validates a DRAFT contract before approval; LOCKED is required only downstream;
4) fine-grained observed FAIL facts dominate a coarse category PASS.

The validator never infers pixels from prompts, filenames or intended content.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

CATEGORIES = [
    'ENVIRONMENT_FUNCTIONAL_REALISM','ARCHITECTURAL_REALISM','VEHICLE_REALISM',
    'HUMAN_ERGONOMICS','OBJECT_AFFORDANCE','SOCIAL_SPATIAL_PLAUSIBILITY',
    'MUNDANE_PHYSICS','MUNDANE_CONTINUITY'
]
DEFAULTS = {
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
FORMAL_APPROVED={'APPROVED','APPROVED_SUPPORT','APPROVED_ASSEMBLY','APPROVED_SCOPED_FIGURE','APPROVED_VIDEO_CONDITIONING'}
ACTIVE_ASSET_STATUSES=FORMAL_APPROVED|{'DRAFT','QC_PASS_WAITING_APPROVAL','REVISE'}
LOCK_REQUIRED_PHASES={'build','freeze','storyboard','conditioning','pre_video'}
PIXEL_EVIDENCE_PHASES={'freeze','storyboard','conditioning','pre_video'}


def load(p):
    return yaml.safe_load(Path(p).read_text(encoding='utf-8')) if p else None


def add(issues, typ, severity='P0', root='UNKNOWN', **kw):
    issues.append({'type':typ,'severity':severity,'root_cause_hint':root,**kw})


def current_evidence(asset, rec):
    if not asset or not rec or rec.get('evidence_status')!='CURRENT': return False
    fp=asset.get('fingerprint'); rfp=rec.get('source_fingerprint')
    return bool(fp and rfp and fp==rfp)


def rel_key(a,b):
    return tuple(sorted((a,b)))


def execution_root(contract, default='GENERATED_ASSET_EXECUTION'):
    cls=(contract or {}).get('source_fact_class') or 'MIXED'
    if cls=='EXPLICIT_SOURCE_FACT': return default
    if cls=='DERIVED_REALISTIC_RESOLUTION': return 'REALISM_CONTRACT_OR_ASSET_EXECUTION'
    if cls=='OPEN_STORY_SIGNIFICANT': return 'SOURCE_REVIEW_REQUIRED'
    if cls=='MIXED': return 'REALISM_RECONCILIATION_REQUIRED'
    return default


def is_v456_or_newer(realism, registry, spatial):
    """V4.5.6 strictness is inherited by every later 4.5.x release."""
    versions={str((x or {}).get('skill_version') or '') for x in [realism,registry,spatial]}
    for v in versions:
        try:
            major, minor, patch = (int(x) for x in v.split('.'))
        except Exception:
            continue
        if (major, minor, patch) >= (4, 5, 6):
            return True
    return False


def asset_event_ids(asset):
    return set(((asset or {}).get('derivation') or {}).get('event_node_ids') or [])


def exception_scope_match(contract, asset, ex):
    aid=(asset or {}).get('asset_id'); shot=(asset or {}).get('shot_id')
    evs=asset_event_ids(asset)
    return bool(
        (aid and aid in set(ex.get('asset_ids') or [])) or
        (shot and shot in set(ex.get('shot_ids') or [])) or
        (evs & set(ex.get('event_node_ids') or [])) or
        (contract.get('scene_id') in set(ex.get('scene_ids') or []))
    )


def scoped_exception_applies(contract, asset, category):
    """An asset's explicit exception id is a selector, never an authority grant.

    The exception must exist in the governing contract, allow the exact category, AND
    the current asset/shot/event/scene must independently match that exception's scope.
    """
    explicit=set((asset or {}).get('realism_exception_ids') or [])
    for ex in contract.get('exception_scopes') or []:
        if category not in set(ex.get('allowed_categories') or []):
            continue
        if not exception_scope_match(contract, asset, ex):
            continue
        if explicit and ex.get('exception_id') not in explicit:
            continue
        return True
    return False


def asset_relevant_for_phase(asset, phase):
    if not asset or asset.get('status')=='DEPRECATED' or asset.get('media_kind')!='IMAGE':
        return False
    if asset.get('status') not in ACTIVE_ASSET_STATUSES:
        return False
    stage=asset.get('cascade_stage') or 'UNKNOWN'
    if phase=='planning': return False
    if phase=='build': return stage not in {'STORYBOARD','VIDEO_CONDITIONING'}
    if phase=='freeze': return asset.get('status') in FORMAL_APPROVED
    if phase=='storyboard': return stage=='STORYBOARD'
    if phase=='conditioning': return stage=='VIDEO_CONDITIONING'
    if phase=='pre_video':
        vu=asset.get('video_usage') or {}
        return asset.get('status') in FORMAL_APPROVED and (stage=='VIDEO_CONDITIONING' or bool(vu.get('direct_input_allowed')))
    return False


def validate_reality_basis(c, issues, strict):
    if not strict:
        return
    cid=c.get('contract_id'); basis=c.get('reality_basis')
    if not basis:
        add(issues,'REALITY_BASIS_MISSING',root='REALISM_CONTRACT',contract_id=cid)
        return
    req=basis.get('reference_requirement')
    status=basis.get('verification_status')
    refs=basis.get('reference_refs') or []
    btype=basis.get('basis_type')
    if req=='REFERENCE_REQUIRED':
        if status!='VERIFIED':
            add(issues,'REALITY_REFERENCE_NOT_VERIFIED',root='REALISM_CONTRACT',contract_id=cid,verification_status=status)
        if not refs:
            add(issues,'REALITY_REFERENCE_REQUIRED_BUT_MISSING',root='REALISM_CONTRACT',contract_id=cid)
    if btype in {'VERIFIED_REFERENCE','HISTORICAL_REFERENCE','TECHNICAL_REFERENCE','MIXED'} and not refs:
        add(issues,'REALITY_BASIS_REFERENCE_MISSING',root='REALISM_CONTRACT',contract_id=cid,basis_type=btype)
    if c.get('source_fact_class')=='DERIVED_REALISTIC_RESOLUTION' and btype=='OPEN':
        add(issues,'DERIVED_REALITY_BASIS_OPEN',root='REALISM_CONTRACT',contract_id=cid)


def validate_contract_structure(c, locs, events, anchors, path_by, assets, phase, issues, warnings, strict):
    cid=c.get('contract_id'); lid=c.get('location_entity_id'); profile=c.get('profile') or 'GENERAL'
    status=c.get('status')
    if phase=='planning':
        if status=='REVISE_REQUIRED':
            add(issues,'REALISM_CONTRACT_REVISE_REQUIRED',root='REALISM_CONTRACT',contract_id=cid,status=status)
        elif status not in {'DRAFT','QC_PASS_WAITING_APPROVAL','LOCKED'}:
            add(issues,'REALISM_CONTRACT_INVALID_PLANNING_STATUS',root='REALISM_CONTRACT',contract_id=cid,status=status)
    elif phase in LOCK_REQUIRED_PHASES and status!='LOCKED':
        add(issues,'REALISM_CONTRACT_NOT_LOCKED',root='REALISM_CONTRACT',contract_id=cid,status=status)

    if lid not in locs:
        add(issues,'REALISM_CONTRACT_UNKNOWN_LOCATION',root='SPATIAL_CANON',contract_id=cid,location_entity_id=lid)
        return
    for eid in c.get('event_node_ids') or []:
        if eid not in events:
            add(issues,'REALISM_CONTRACT_UNKNOWN_EVENT_NODE',root='SPATIAL_CANON',contract_id=cid,event_node_id=eid)
        elif events[eid].get('location_entity_id')!=lid:
            add(issues,'REALISM_EVENT_LOCATION_MISMATCH',root='SPATIAL_CANON',contract_id=cid,event_node_id=eid,expected_location=lid,actual_location=events[eid].get('location_entity_id'))

    validate_reality_basis(c,issues,strict)

    exids=[]
    for ex in c.get('exception_scopes') or []:
        eid=ex.get('exception_id')
        if eid in exids: add(issues,'DUPLICATE_REALISM_EXCEPTION_ID',root='REALISM_CONTRACT',contract_id=cid,exception_id=eid)
        exids.append(eid)
        scoped=any(ex.get(k) for k in ['scene_ids','event_node_ids','shot_ids','asset_ids'])
        if not scoped: add(issues,'REALISM_EXCEPTION_UNSCOPED',root='REALISM_CONTRACT',contract_id=cid,exception_id=eid)
        cats=set(ex.get('allowed_categories') or [])
        if not cats: add(issues,'REALISM_EXCEPTION_EMPTY',root='REALISM_CONTRACT',contract_id=cid,exception_id=eid)
        if len(cats)==len(CATEGORIES) and not ex.get('approval_ref'):
            add(issues,'REALISM_EXCEPTION_OVERBROAD_WITHOUT_APPROVAL',root='REALISM_CONTRACT',contract_id=cid,exception_id=eid)
    if c.get('baseline_mode')=='REALISM_EXCEPTION_SCOPED' and not c.get('exception_scopes'):
        add(issues,'REALISM_EXCEPTION_MODE_WITHOUT_SCOPE',root='REALISM_CONTRACT',contract_id=cid)

    env=c.get('environment_requirements') or {}
    loc=locs[lid]
    if profile=='VEHICLE':
        if loc.get('location_kind')!='VEHICLE':
            add(issues,'VEHICLE_PROFILE_LOCATION_KIND_MISMATCH',root='SPATIAL_CANON',contract_id=cid,location_entity_id=lid,location_kind=loc.get('location_kind'))
        veh=env.get('vehicle') or {}
        if not (veh.get('vehicle_type') or env.get('specific_type')): add(issues,'VEHICLE_TYPE_UNSPECIFIED',root='REALISM_CONTRACT',contract_id=cid)
        if not veh.get('driver_zone_id'): add(issues,'VEHICLE_DRIVER_ZONE_UNSPECIFIED',root='REALISM_CONTRACT',contract_id=cid)
        if not (veh.get('passenger_zone_ids') or []): add(issues,'VEHICLE_PASSENGER_ZONES_UNSPECIFIED',root='REALISM_CONTRACT',contract_id=cid)
        if not veh.get('front_direction_code'): add(issues,'VEHICLE_FRONT_DIRECTION_UNSPECIFIED',root='REALISM_CONTRACT',contract_id=cid)
        cap=veh.get('passenger_capacity')
        if cap is not None:
            expected_passengers=sum(int(x.get('expected_count') or 1) for x in c.get('expected_cast') or [] if x.get('functional_role')!='DRIVER')
            if expected_passengers>int(cap):
                add(issues,'VEHICLE_PASSENGER_CAPACITY_CONTRACT_FAIL',root='REALISM_CONTRACT_OR_ASSET_EXECUTION',contract_id=cid,passenger_capacity=cap,expected_passengers=expected_passengers)

    zones=set(loc.get('zones') or [])
    for zid in env.get('required_zone_ids') or []:
        if zid not in zones: add(issues,'REALISM_REQUIRED_ZONE_UNKNOWN',root='SPATIAL_CANON',contract_id=cid,zone_id=zid)
    for aid in env.get('required_anchor_ids') or []:
        if aid not in anchors: add(issues,'REALISM_REQUIRED_ANCHOR_UNKNOWN',root='SPATIAL_CANON',contract_id=cid,anchor_id=aid)
    for pid in env.get('required_access_path_ids') or []:
        if pid not in path_by or path_by[pid][0]!=lid:
            add(issues,'REALISM_REQUIRED_ACCESS_PATH_UNKNOWN',root='SPATIAL_CANON',contract_id=cid,access_path_id=pid)
    veh=env.get('vehicle') or {}
    for zid in [veh.get('driver_zone_id')]+list(veh.get('passenger_zone_ids') or []):
        if zid and zid not in zones: add(issues,'VEHICLE_ZONE_UNKNOWN',root='SPATIAL_CANON',contract_id=cid,zone_id=zid)
    for aid in veh.get('entry_anchor_ids') or []:
        if aid not in anchors: add(issues,'VEHICLE_ENTRY_ANCHOR_UNKNOWN',root='SPATIAL_CANON',contract_id=cid,anchor_id=aid)
    if env.get('ingress_egress_required'):
        has_entry=bool(veh.get('entry_anchor_ids')) or any(a.get('anchor_type') in {'ENTRY','EXIT','DOOR'} and owner==lid for _,(owner,a) in anchors.items())
        if not has_entry: add(issues,'INGRESS_EGRESS_STRUCTURE_MISSING',root='SPATIAL_CANON',contract_id=cid)
    if env.get('circulation_required') and strict and not (loc.get('access_paths') or []):
        add(issues,'CIRCULATION_PATH_STRUCTURE_MISSING',root='SPATIAL_CANON',contract_id=cid)

    for ec in c.get('expected_cast') or []:
        zid=ec.get('required_zone_id')
        if zid and zid not in zones: add(issues,'CHARACTER_REQUIRED_ZONE_UNKNOWN',root='SPATIAL_CANON',contract_id=cid,character_id=ec.get('character_id'),zone_id=zid)
        pos=ec.get('required_position_id')
        if pos and pos not in anchors: add(issues,'CHARACTER_FUNCTIONAL_POSITION_UNKNOWN',root='SPATIAL_CANON',contract_id=cid,character_id=ec.get('character_id'),functional_position_id=pos)
        surf=ec.get('required_support_surface_id')
        if surf and surf not in anchors: add(issues,'CHARACTER_SUPPORT_SURFACE_UNKNOWN',root='SPATIAL_CANON',contract_id=cid,character_id=ec.get('character_id'),support_surface_id=surf)

    cont=c.get('continuity_requirements') or {}
    if strict and any(bool(cont.get(k)) for k in ['no_unexplained_character_relocation','no_unexplained_prop_state_change','no_unexplained_environment_reset','no_unexplained_wetness_damage_reset','no_unexplained_task_drop']) and not cont.get('world_state_ref'):
        add(issues,'MUNDANE_CONTINUITY_WORLD_STATE_REF_MISSING',root='WORLD_STATE_OR_ASSET_EXECUTION',contract_id=cid)

    for aid in c.get('asset_ids') or []:
        if aid not in assets:
            add(issues,'REALISM_CONTRACT_ASSET_MISSING',root='ASSET_REGISTRY',contract_id=cid,asset_id=aid)
        elif strict and cid not in set((assets[aid] or {}).get('realism_contract_ids') or []):
            add(issues,'REALISM_CONTRACT_ASSET_BACKREF_MISSING',root='ASSET_REGISTRY',contract_id=cid,asset_id=aid)


def validate_asset_binding(asset, contract_by, phase, issues, strict):
    if not strict or not asset_relevant_for_phase(asset,phase):
        return
    aid=asset.get('asset_id'); app=asset.get('realism_applicability') or 'UNKNOWN'
    reason=asset.get('realism_applicability_reason')
    cids=set(asset.get('realism_contract_ids') or [])
    exids=set(asset.get('realism_exception_ids') or [])
    if app=='UNKNOWN':
        add(issues,'REALISM_APPLICABILITY_UNDECLARED',root='ASSET_REGISTRY',asset_id=aid,phase=phase)
        return
    if app=='NOT_APPLICABLE':
        if not reason: add(issues,'REALISM_NOT_APPLICABLE_WITHOUT_REASON',root='ASSET_REGISTRY',asset_id=aid)
        if asset.get('realism_qc_status')!='NOT_APPLICABLE': add(issues,'REALISM_NOT_APPLICABLE_STATUS_MISMATCH',root='ASSET_REGISTRY',asset_id=aid,realism_qc_status=asset.get('realism_qc_status'))
        if cids or exids: add(issues,'REALISM_NOT_APPLICABLE_HAS_ACTIVE_BINDING',root='ASSET_REGISTRY',asset_id=aid)
        return
    if app not in {'REQUIRED','SCOPED_EXCEPTION'}:
        add(issues,'REALISM_APPLICABILITY_INVALID',root='ASSET_REGISTRY',asset_id=aid,value=app)
        return
    if not cids:
        add(issues,'REALISM_ASSET_CONTRACT_BINDING_MISSING',root='ASSET_REGISTRY',asset_id=aid,phase=phase)
        return
    for cid in sorted(cids):
        if cid not in contract_by:
            add(issues,'REALISM_ASSET_UNKNOWN_CONTRACT',root='ASSET_REGISTRY',asset_id=aid,contract_id=cid)
    if app=='SCOPED_EXCEPTION' and not exids:
        add(issues,'REALISM_SCOPED_EXCEPTION_ID_MISSING',root='ASSET_REGISTRY',asset_id=aid)
    if app=='REQUIRED' and exids:
        add(issues,'REALISM_EXCEPTION_IDS_REQUIRE_SCOPED_APPLICABILITY',root='ASSET_REGISTRY',asset_id=aid,exception_ids=sorted(exids))
    for exid in sorted(exids):
        found=False; scoped=False
        for cid in cids:
            c=contract_by.get(cid)
            if not c: continue
            for ex in c.get('exception_scopes') or []:
                if ex.get('exception_id')==exid:
                    found=True
                    if exception_scope_match(c,asset,ex): scoped=True
        if not found:
            add(issues,'REALISM_EXCEPTION_UNKNOWN',root='REALISM_CONTRACT',asset_id=aid,exception_id=exid)
        elif not scoped:
            add(issues,'REALISM_EXCEPTION_SCOPE_MISMATCH',root='REALISM_CONTRACT',asset_id=aid,exception_id=exid)


def add_observed_failure(issues, fine_fail_categories, contract, asset, category, code, **kw):
    aid=asset.get('asset_id'); cid=contract.get('contract_id')
    if scoped_exception_applies(contract,asset,category):
        return
    fine_fail_categories.add(category)
    add(issues,code,root=execution_root(contract),contract_id=cid,asset_id=aid,**kw)


def validate_pixel_asset(asset, contract, rec, issues, strict):
    aid=asset.get('asset_id'); cid=contract.get('contract_id'); profile=contract.get('profile') or 'GENERAL'
    if not current_evidence(asset,rec):
        add(issues,'REALISM_VISUAL_EVIDENCE_MISSING_OR_STALE',root='VISUAL_EVIDENCE',contract_id=cid,asset_id=aid); return
    obs=rec.get('observed') or {}; ro=obs.get('realism') or {}
    if not ro:
        add(issues,'REALISM_VISUAL_EVIDENCE_FIELDS_MISSING',root='VISUAL_EVIDENCE',contract_id=cid,asset_id=aid); return
    if strict and asset.get('realism_qc_status')!='PASS':
        add(issues,'REALISM_ASSET_QC_STATUS_NOT_PASS',root='ASSET_REGISTRY',contract_id=cid,asset_id=aid,realism_qc_status=asset.get('realism_qc_status'))

    required=set(contract.get('required_categories') or []) or set(DEFAULTS.get(profile,DEFAULTS['GENERAL']))
    env=contract.get('environment_requirements') or {}
    fine_fail_categories=set()

    expected_cast=contract.get('expected_cast') or []; expected_total=sum(int(x.get('expected_count') or 0) for x in expected_cast)
    human_count=ro.get('human_count')
    if expected_cast:
        if human_count is None:
            add(issues,'REALISM_HUMAN_COUNT_UNPROVEN',root='VISUAL_EVIDENCE',contract_id=cid,asset_id=aid)
        elif human_count!=expected_total and not contract.get('unexpected_humans_allowed',False):
            add_observed_failure(issues,fine_fail_categories,contract,asset,'HUMAN_ERGONOMICS','CAST_COUNT_MISMATCH',expected=expected_total,observed=human_count)
    observed_chars={x.get('character_id'):x for x in ro.get('characters') or []}
    for ec in expected_cast:
        ch=ec.get('character_id'); oc=observed_chars.get(ch)
        if not oc:
            add(issues,'CHARACTER_VISUAL_PRESENCE_UNPROVEN',root='VISUAL_EVIDENCE',contract_id=cid,asset_id=aid,character_id=ch); continue
        if int(oc.get('count') or 0)!=int(ec.get('expected_count') or 1):
            add_observed_failure(issues,fine_fail_categories,contract,asset,'HUMAN_ERGONOMICS','CHARACTER_DUPLICATION_OR_COUNT_FAIL',character_id=ch,expected=ec.get('expected_count'),observed=oc.get('count'))
        if ec.get('required_zone_id') and oc.get('zone_id')!=ec.get('required_zone_id'):
            add_observed_failure(issues,fine_fail_categories,contract,asset,'HUMAN_ERGONOMICS','CHARACTER_ZONE_ASSIGNMENT_FAIL',character_id=ch,expected=ec.get('required_zone_id'),observed=oc.get('zone_id'))
        if ec.get('required_position_id') and oc.get('functional_position_id')!=ec.get('required_position_id'):
            add_observed_failure(issues,fine_fail_categories,contract,asset,'HUMAN_ERGONOMICS','CHARACTER_FUNCTIONAL_POSITION_FAIL',character_id=ch,expected=ec.get('required_position_id'),observed=oc.get('functional_position_id'))
        if ec.get('required_posture') not in {None,'NOT_FIXED','UNKNOWN'} and oc.get('posture')!=ec.get('required_posture'):
            add_observed_failure(issues,fine_fail_categories,contract,asset,'HUMAN_ERGONOMICS','CHARACTER_POSTURE_REALISM_FAIL',character_id=ch,expected=ec.get('required_posture'),observed=oc.get('posture'))
        if ec.get('required_support_surface_id') and oc.get('support_surface_id')!=ec.get('required_support_surface_id'):
            add_observed_failure(issues,fine_fail_categories,contract,asset,'HUMAN_ERGONOMICS','ERGONOMIC_SUPPORT_FAIL',character_id=ch,expected=ec.get('required_support_surface_id'),observed=oc.get('support_surface_id'))
        req_gaze=set(ec.get('required_eyeline_targets') or [])
        got_gaze=set(oc.get('gaze_target_ids') or [])
        if req_gaze-got_gaze:
            add_observed_failure(issues,fine_fail_categories,contract,asset,'SOCIAL_SPATIAL_PLAUSIBILITY','CHARACTER_REQUIRED_EYELINE_TARGET_GAP',character_id=ch,missing_target_ids=sorted(req_gaze-got_gaze))

    counts={}
    for oc in ro.get('characters') or []:
        z=oc.get('zone_id')
        if z: counts[z]=counts.get(z,0)+int(oc.get('count') or 1)
    for cap in env.get('capacity_constraints') or []:
        z=cap.get('zone_id'); n=counts.get(z,0)
        if n>int(cap.get('max_humans') or 0):
            add_observed_failure(issues,fine_fail_categories,contract,asset,'HUMAN_ERGONOMICS','SPACE_CAPACITY_EXCEEDED',zone_id=z,max=cap.get('max_humans'),observed=n)
        if n<int(cap.get('min_humans') or 0):
            add_observed_failure(issues,fine_fail_categories,contract,asset,'HUMAN_ERGONOMICS','SPACE_REQUIRED_OCCUPANCY_MISSING',zone_id=z,min=cap.get('min_humans'),observed=n)

    oe=ro.get('environment') or {}
    if env.get('environment_kind') not in {None,'UNKNOWN'} and oe.get('environment_kind') not in {env.get('environment_kind')}:
        add_observed_failure(issues,fine_fail_categories,contract,asset,'ENVIRONMENT_FUNCTIONAL_REALISM','ENVIRONMENT_KIND_VISUAL_MISMATCH',expected=env.get('environment_kind'),observed=oe.get('environment_kind'))
    expected_specific=env.get('specific_type')
    if expected_specific and oe.get('specific_type') and str(expected_specific).casefold()!=str(oe.get('specific_type')).casefold():
        add_observed_failure(issues,fine_fail_categories,contract,asset,'ENVIRONMENT_FUNCTIONAL_REALISM','ENVIRONMENT_FUNCTIONAL_TYPE_DRIFT',expected=expected_specific,observed=oe.get('specific_type'))

    # Fine-grained environment facts. Explicit FAIL always beats a coarse PASS.
    checks=[
        ('scale_plausibility_required','scale_plausibility','ENVIRONMENT_FUNCTIONAL_REALISM','ENVIRONMENT_SCALE_PLAUSIBILITY_FAIL'),
        ('functional_layout_required','functional_layout_plausibility','ENVIRONMENT_FUNCTIONAL_REALISM','ENVIRONMENT_FUNCTIONAL_LAYOUT_FAIL'),
        ('ingress_egress_required','ingress_egress_plausibility','ENVIRONMENT_FUNCTIONAL_REALISM','INGRESS_EGRESS_PLAUSIBILITY_FAIL'),
        ('circulation_required','circulation_plausibility','ENVIRONMENT_FUNCTIONAL_REALISM','CIRCULATION_PLAUSIBILITY_FAIL'),
    ]
    for reqkey,obskey,cat,code in checks:
        if env.get(reqkey) and oe.get(obskey)=='FAIL':
            add_observed_failure(issues,fine_fail_categories,contract,asset,cat,code)
    required_paths=set(env.get('required_access_path_ids') or [])
    observed_paths=set(oe.get('access_path_ids') or [])
    if required_paths and required_paths-observed_paths:
        add_observed_failure(issues,fine_fail_categories,contract,asset,'ENVIRONMENT_FUNCTIONAL_REALISM','REQUIRED_ACCESS_PATH_VISUAL_GAP',missing_access_path_ids=sorted(required_paths-observed_paths))

    if profile=='VEHICLE':
        v=env.get('vehicle') or {}; expected_vehicle=v.get('vehicle_type') or env.get('specific_type')
        observed_vehicle=oe.get('vehicle_type') or oe.get('specific_type')
        if expected_vehicle and not observed_vehicle:
            add(issues,'VEHICLE_TYPE_VISUALLY_UNPROVEN',root='VISUAL_EVIDENCE',contract_id=cid,asset_id=aid)
        elif expected_vehicle and str(expected_vehicle).casefold()!=str(observed_vehicle).casefold():
            add_observed_failure(issues,fine_fail_categories,contract,asset,'VEHICLE_REALISM','VEHICLE_FUNCTIONAL_LAYOUT_DRIFT',expected_vehicle_type=expected_vehicle,observed_vehicle_type=observed_vehicle)
        if v.get('driver_zone_id') and oe.get('driver_zone_id') and v.get('driver_zone_id')!=oe.get('driver_zone_id'):
            add_observed_failure(issues,fine_fail_categories,contract,asset,'VEHICLE_REALISM','VEHICLE_DRIVER_ZONE_DRIFT',expected=v.get('driver_zone_id'),observed=oe.get('driver_zone_id'))
        if v.get('front_direction_code') and oe.get('front_direction_code') and v.get('front_direction_code')!=oe.get('front_direction_code'):
            add_observed_failure(issues,fine_fail_categories,contract,asset,'VEHICLE_REALISM','VEHICLE_FRONT_DIRECTION_DRIFT',expected=v.get('front_direction_code'),observed=oe.get('front_direction_code'))
        if v.get('driver_forward_visibility_required') and oe.get('driver_forward_visibility')=='FAIL':
            add_observed_failure(issues,fine_fail_categories,contract,asset,'VEHICLE_REALISM','VEHICLE_DRIVER_FORWARD_VISIBILITY_FAIL')
        expected_entries=set(v.get('entry_anchor_ids') or [])
        observed_entries=set(oe.get('entry_anchor_ids') or [])
        if expected_entries and observed_entries and expected_entries-observed_entries:
            add_observed_failure(issues,fine_fail_categories,contract,asset,'VEHICLE_REALISM','VEHICLE_ENTRY_ANCHOR_VISUAL_GAP',missing_entry_anchor_ids=sorted(expected_entries-observed_entries))
        cap=v.get('passenger_capacity')
        observed_passengers=oe.get('passenger_count')
        if cap is not None and observed_passengers is not None and int(observed_passengers)>int(cap):
            add_observed_failure(issues,fine_fail_categories,contract,asset,'VEHICLE_REALISM','VEHICLE_PASSENGER_CAPACITY_EXCEEDED',passenger_capacity=cap,observed_passengers=observed_passengers)

    oo={x.get('object_id'):x for x in ro.get('object_affordances') or []}
    for req in contract.get('object_affordances') or []:
        ob=oo.get(req.get('object_id'))
        if not ob:
            add(issues,'OBJECT_AFFORDANCE_UNPROVEN',severity='P1',root='VISUAL_EVIDENCE',contract_id=cid,asset_id=aid,object_id=req.get('object_id')); continue
        if ob.get('verdict')=='FAIL' or (req.get('required_reachable',True) and ob.get('reachable')=='NO') or (req.get('required_supported',True) and ob.get('supported')=='NO') or (req.get('required_operable',True) and ob.get('operable')=='NO'):
            add_observed_failure(issues,fine_fail_categories,contract,asset,'OBJECT_AFFORDANCE','OBJECT_AFFORDANCE_FAIL',object_id=req.get('object_id'))

    observed_rel={rel_key(x.get('character_a'),x.get('character_b')):x for x in ro.get('character_relations') or []}
    acceptable={
        'CONTACT':{'CONTACT'},'NEAR':{'CONTACT','NEAR'},'CONVERSATIONAL':{'CONTACT','NEAR','CONVERSATIONAL'},
        'MEDIUM':{'CONVERSATIONAL','MEDIUM'},'FAR':{'FAR'},'SEPARATED':{'FAR','SEPARATED'},'NOT_FIXED':{'CONTACT','NEAR','CONVERSATIONAL','MEDIUM','FAR','SEPARATED','UNKNOWN'}
    }
    for sr in contract.get('social_spatial_constraints') or []:
        if sr.get('relation')=='NOT_FIXED': continue
        key=rel_key(sr.get('character_a'),sr.get('character_b')); got=observed_rel.get(key)
        if not got:
            add(issues,'SOCIAL_SPATIAL_RELATION_UNPROVEN',severity='P1',root='VISUAL_EVIDENCE',contract_id=cid,asset_id=aid,characters=list(key)); continue
        if got.get('relation') not in acceptable.get(sr.get('relation'),{sr.get('relation')}) and not sr.get('behavior_reason_ref'):
            add_observed_failure(issues,fine_fail_categories,contract,asset,'SOCIAL_SPATIAL_PLAUSIBILITY','SOCIAL_SPATIAL_IMPLAUSIBILITY',characters=list(key),expected=sr.get('relation'),observed=got.get('relation'))
        if sr.get('eyeline_access_required') and got.get('eyeline_access')!='YES':
            add_observed_failure(issues,fine_fail_categories,contract,asset,'SOCIAL_SPATIAL_PLAUSIBILITY','SOCIAL_EYELINE_ACCESS_FAIL',characters=list(key),observed=got.get('eyeline_access'))

    # Fine-grained mundane continuity, only for stateful shot/event imagery.
    if asset.get('cascade_stage') in {'EVENT_VIEW','COVERAGE','STORYBOARD','VIDEO_CONDITIONING'}:
        cont_req=contract.get('continuity_requirements') or {}; cont_obs=ro.get('continuity') or {}
        cont_map={
            'no_unexplained_character_relocation':('character_relocation','MUNDANE_CHARACTER_RELOCATION_FAIL'),
            'no_unexplained_prop_state_change':('prop_state','MUNDANE_PROP_STATE_CHANGE_FAIL'),
            'no_unexplained_environment_reset':('environment_reset','MUNDANE_ENVIRONMENT_RESET_FAIL'),
            'no_unexplained_wetness_damage_reset':('wetness_damage_reset','MUNDANE_WETNESS_DAMAGE_RESET_FAIL'),
            'no_unexplained_task_drop':('task_continuity','MUNDANE_TASK_CONTINUITY_FAIL'),
        }
        for reqkey,(obskey,code) in cont_map.items():
            if cont_req.get(reqkey) and cont_obs.get(obskey)=='FAIL':
                add_observed_failure(issues,fine_fail_categories,contract,asset,'MUNDANE_CONTINUITY',code)

    verdicts=ro.get('category_verdicts') or {}
    for cat in sorted(required):
        if scoped_exception_applies(contract,asset,cat): continue
        verdict=verdicts.get(cat,'UNKNOWN')
        if verdict=='FAIL':
            root='WORLD_STATE_OR_ASSET_EXECUTION' if cat=='MUNDANE_CONTINUITY' else execution_root(contract)
            add(issues,cat+'_FAIL',root=root,contract_id=cid,asset_id=aid)
        elif verdict not in {'PASS','NOT_APPLICABLE'}:
            add(issues,'REALISM_CATEGORY_UNPROVEN',severity='P1',root='VISUAL_EVIDENCE',contract_id=cid,asset_id=aid,category=cat,observed=verdict)
        elif verdict=='PASS' and cat in fine_fail_categories:
            add(issues,'REALISM_SUMMARY_CONTRADICTS_OBSERVATION',root='VISUAL_EVIDENCE',contract_id=cid,asset_id=aid,category=cat,summary_verdict='PASS')

    issue_codes=set(obs.get('issue_codes') or [])
    hard_map={
        'HUMAN_ENVIRONMENT_INTERSECTION_FAIL':'HUMAN_ERGONOMICS','HUMAN_SCALE_IMPLAUSIBLE':'HUMAN_ERGONOMICS','ERGONOMIC_SUPPORT_FAIL':'HUMAN_ERGONOMICS',
        'OBJECT_AFFORDANCE_FAIL':'OBJECT_AFFORDANCE','VEHICLE_FUNCTIONAL_LAYOUT_DRIFT':'VEHICLE_REALISM','VEHICLE_DRIVER_FORWARD_VISIBILITY_FAIL':'VEHICLE_REALISM',
        'ENVIRONMENT_FUNCTIONAL_REALISM_FAIL':'ENVIRONMENT_FUNCTIONAL_REALISM','ARCHITECTURAL_REALISM_FAIL':'ARCHITECTURAL_REALISM',
        'SOCIAL_SPATIAL_IMPLAUSIBILITY':'SOCIAL_SPATIAL_PLAUSIBILITY','MUNDANE_PHYSICS_FAIL':'MUNDANE_PHYSICS','MUNDANE_CONTINUITY_FAIL':'MUNDANE_CONTINUITY',
    }
    for code,cat in hard_map.items():
        if code in issue_codes and not scoped_exception_applies(contract,asset,cat):
            add(issues,code,root=execution_root(contract),contract_id=cid,asset_id=aid)


def lint(realism, spatial=None, registry=None, evidence=None, phase='planning'):
    issues=[]; warnings=[]
    realism=realism or {'contracts':[]}; spatial=spatial or {}; registry=registry or {'assets':[]}; evidence=evidence or {'records':[]}
    strict=is_v456_or_newer(realism,registry,spatial)
    contracts=realism.get('contracts') or []; assets_list=registry.get('assets') or []
    cids=[c.get('contract_id') for c in contracts]
    for cid in sorted({x for x in cids if x and cids.count(x)>1}): add(issues,'DUPLICATE_REALISM_CONTRACT_ID',root='REALISM_CONTRACT',contract_id=cid)
    contract_by={c.get('contract_id'):c for c in contracts if c.get('contract_id')}
    assets={a.get('asset_id'):a for a in assets_list if a.get('asset_id')}
    evidence_by={x.get('asset_id'):x for x in evidence.get('records') or [] if x.get('evidence_status')=='CURRENT'}
    locs={x.get('location_entity_id'):x for x in spatial.get('locations') or []}
    events={x.get('event_node_id'):x for x in spatial.get('event_nodes') or []}
    anchors={}; path_by={}
    for lid,l in locs.items():
        for a in l.get('anchors') or []: anchors[a.get('anchor_id')]=(lid,a)
        for p in l.get('access_paths') or []:
            pid=p.get('path_id')
            if pid in path_by: add(issues,'DUPLICATE_SPATIAL_ACCESS_PATH_ID',root='SPATIAL_CANON',access_path_id=pid)
            path_by[pid]=(lid,p)

    for c in contracts:
        validate_contract_structure(c,locs,events,anchors,path_by,assets,phase,issues,warnings,strict)

    # V4.5.6 reverse-coverage rule: ordinary IMAGE assets cannot silently omit Reality-by-Default metadata.
    for a in assets_list:
        validate_asset_binding(a,contract_by,phase,issues,strict)

    if phase=='freeze':
        for c in contracts:
            cid=c.get('contract_id')
            covered=[a for a in assets_list if a.get('status') in FORMAL_APPROVED and cid in set(a.get('realism_contract_ids') or []) and a.get('media_kind')=='IMAGE' and a.get('realism_applicability')!='NOT_APPLICABLE']
            if not covered:
                add(issues,'REALISM_CONTRACT_NO_FULFILLMENT_ASSET',root='ASSET_REGISTRY',contract_id=cid)

    if phase in PIXEL_EVIDENCE_PHASES:
        for a in assets_list:
            if not asset_relevant_for_phase(a,phase): continue
            app=a.get('realism_applicability') if strict else ('REQUIRED' if a.get('realism_contract_ids') else 'NOT_APPLICABLE')
            if app=='NOT_APPLICABLE': continue
            for cid in set(a.get('realism_contract_ids') or []):
                c=contract_by.get(cid)
                if not c: continue
                validate_pixel_asset(a,c,evidence_by.get(a.get('asset_id')),issues,strict)

    action_map={
        'SPATIAL_CANON':'PATCH_SPATIAL_CANON_THEN_REDERIVE_AFFECTED_ASSETS','REALISM_CONTRACT':'PATCH_OR_QC_REALISM_CONTRACT_BEFORE_DEPENDENT_IMAGE_GENERATION',
        'GENERATED_ASSET_EXECUTION':'REJECT_CANDIDATE_AND_REGENERATE_MINIMUM_AFFECTED_ASSET','REALISM_CONTRACT_OR_ASSET_EXECUTION':'COMPARE_DERIVED_CONTRACT_WITH_SOURCE_AND_REAL_WORLD_FUNCTION_THEN_PATCH_TRUE_OWNER_ONLY',
        'REALISM_RECONCILIATION_REQUIRED':'RECONCILE_MIXED_SOURCE_CONTRACT_SPATIAL_AND_RENDER_BEFORE_CONTINUING','SOURCE_REVIEW_REQUIRED':'RESOLVE_STORY_SIGNIFICANT_SOURCE_FACT_BEFORE_AUTOMATIC_PATCH',
        'VISUAL_EVIDENCE':'QUEUE_ONLY_BLOCKING_ASSET_FOR_MULTIMODAL_VISUAL_REVIEW','WORLD_STATE_OR_ASSET_EXECUTION':'RECONCILE_WORLD_STATE_SOURCE_THEN_PATCH_MINIMUM_OWNER',
        'ASSET_REGISTRY':'REPAIR_ASSET_BINDING_OR_APPLICABILITY_METADATA','UNKNOWN':'DIAGNOSE_OWNER_BEFORE_CONTINUING',
    }
    roots=[]
    for i in issues:
        r=i.get('root_cause_hint','UNKNOWN')
        if r not in roots: roots.append(r)
    actions=[{'root_cause':r,'action':action_map.get(r,action_map['UNKNOWN'])} for r in roots]
    return {'pass':not issues,'phase':phase,'contract_count':len(contracts),'strict_v456':strict,'issues':issues,'warnings':warnings,'reconciliation_actions':actions}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--realism-contract',required=True)
    ap.add_argument('--spatial-canon')
    ap.add_argument('--asset-registry')
    ap.add_argument('--visual-evidence')
    ap.add_argument('--phase',choices=['planning','build','freeze','storyboard','conditioning','pre_video'],default='planning')
    a=ap.parse_args()
    out=lint(load(a.realism_contract),load(a.spatial_canon),load(a.asset_registry),load(a.visual_evidence),a.phase)
    print(json.dumps(out,ensure_ascii=False,indent=2))
    raise SystemExit(0 if out['pass'] else 2)

if __name__=='__main__':
    main()
