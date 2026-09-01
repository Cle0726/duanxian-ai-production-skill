#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

VALID_MODES={'DIRECT_CONTINUITY','MATCH_ON_ACTION','CUT_REFRAME','REACTION_CUT','ELLIPSIS','SPATIAL_REORIENTATION','SCENE_CHANGE'}
VALID_DISTANCE={'LOW','MEDIUM','HIGH','SCENE_BOUNDARY'}
VALID_PRECISION={'PIXEL_EXACT_T0','WORLD_STATE_STRICT','STORYBOARD_BLOCKING_APPROXIMATE','SCENE_RESET'}
VALID_ENDING_ROUTE={'DIRECT_T0_ANCHOR','LINEAGE_ONLY','STAGE06_EDIT_REFERENCE_ONLY','NOT_APPLICABLE'}
CUT_TRANSITIONS={'MATCH_ON_ACTION','CUT_REFRAME','REACTION_CUT','SPATIAL_REORIENTATION','J_CUT','L_CUT','SOUND_BRIDGE','SHAPE_OR_DIRECTION_MATCH'}

def load(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))

def issue(issues,t,**k): d={'type':t}; d.update(k); issues.append(d)

def lint_contract(doc):
    issues=[]
    if doc.get('inheritance_mode') not in VALID_MODES:
        issue(issues,'BOUNDARY_INHERITANCE_MODE_INVALID',actual=doc.get('inheritance_mode'))
    if doc.get('continuity_distance') not in VALID_DISTANCE:
        issue(issues,'BOUNDARY_CONTINUITY_DISTANCE_INVALID',actual=doc.get('continuity_distance'))
    if doc.get('inheritance_mode')=='DIRECT_CONTINUITY' and not doc.get('required_invariants'):
        issue(issues,'DIRECT_CONTINUITY_INVARIANTS_MISSING')
    precision=doc.get('continuity_precision')
    route=doc.get('ending_frame_provider_route')
    if precision is not None and precision not in VALID_PRECISION:
        issue(issues,'BOUNDARY_CONTINUITY_PRECISION_INVALID',actual=precision)
    if route is not None and route not in VALID_ENDING_ROUTE:
        issue(issues,'BOUNDARY_ENDING_FRAME_ROUTE_INVALID',actual=route)
    if precision=='STORYBOARD_BLOCKING_APPROXIMATE':
        bridge=doc.get('storyboard_bridge') or {}
        if doc.get('inheritance_mode')=='DIRECT_CONTINUITY':
            issue(issues,'APPROXIMATE_STORYBOARD_BRIDGE_FORBIDDEN_FOR_DIRECT_CONTINUITY')
        if route not in {'LINEAGE_ONLY','STAGE06_EDIT_REFERENCE_ONLY'}:
            issue(issues,'APPROXIMATE_STORYBOARD_BRIDGE_ENDING_FRAME_ROUTE_INVALID',actual=route)
        for k in ('storyboard_exit_panel_ref','storyboard_entry_panel_ref'):
            if not bridge.get(k): issue(issues,'APPROXIMATE_STORYBOARD_BRIDGE_REF_MISSING',field=k)
        if bridge.get('approximate_spatial_match_allowed') is not True:
            issue(issues,'APPROXIMATE_STORYBOARD_BRIDGE_FLAG_MISSING')
        if bridge.get('transition_language') not in CUT_TRANSITIONS:
            issue(issues,'APPROXIMATE_STORYBOARD_BRIDGE_TRANSITION_INVALID',actual=bridge.get('transition_language'))
        if not bridge.get('required_invariants'):
            issue(issues,'APPROXIMATE_STORYBOARD_BRIDGE_INVARIANTS_MISSING')
    if precision=='PIXEL_EXACT_T0' and route!='DIRECT_T0_ANCHOR':
        issue(issues,'PIXEL_EXACT_T0_REQUIRES_ENDING_ANCHOR',actual=route)
    return {'pass': not issues, 'issues': issues}

def compare_states(contract, before, after):
    issues=[]
    mode=contract.get('inheritance_mode')
    strict_world=mode in {'DIRECT_CONTINUITY','CUT_REFRAME','REACTION_CUT'}
    moderate=mode=='MATCH_ON_ACTION'
    b={x.get('entity_id'):x for x in before.get('entity_states') or [] if x.get('entity_id')}
    a={x.get('entity_id'):x for x in after.get('entity_states') or [] if x.get('entity_id')}
    shared=set(b)&set(a)
    for eid in sorted(shared):
        x,y=b[eid],a[eid]
        bx=x.get('world_position') or {}; ay=y.get('world_position') or {}
        if strict_world or moderate:
            if bx.get('zone_id')!=ay.get('zone_id'):
                issue(issues,'BOUNDARY_WORLD_ZONE_JUMP',entity_id=eid,before=bx.get('zone_id'),after=ay.get('zone_id'),inheritance_mode=mode)
        if strict_world:
            for k in ('anchor_id','relation'):
                if bx.get(k) is not None and ay.get(k) is not None and bx.get(k)!=ay.get(k):
                    issue(issues,'BOUNDARY_WORLD_ANCHOR_RELATION_JUMP',entity_id=eid,field=k,before=bx.get(k),after=ay.get(k),inheritance_mode=mode)
            if x.get('body_orientation') and y.get('body_orientation') and x.get('body_orientation')!=y.get('body_orientation'):
                issue(issues,'BOUNDARY_BODY_ORIENTATION_JUMP',entity_id=eid,before=x.get('body_orientation'),after=y.get('body_orientation'),inheritance_mode=mode)
            if x.get('contact_state') is not None and y.get('contact_state') is not None and x.get('contact_state')!=y.get('contact_state'):
                issue(issues,'BOUNDARY_CONTACT_STATE_JUMP',entity_id=eid,before=x.get('contact_state'),after=y.get('contact_state'),inheritance_mode=mode)
        # Held props are continuity facts for direct/reframe/reaction and match-on-action.
        if strict_world or moderate:
            if sorted(x.get('held_prop_ids') or [])!=sorted(y.get('held_prop_ids') or []):
                issue(issues,'BOUNDARY_HELD_PROP_JUMP',entity_id=eid,before=x.get('held_prop_ids') or [],after=y.get('held_prop_ids') or [],inheritance_mode=mode)
        # Deliberately DO NOT compare frame_projection LEFT/RIGHT: it is camera-derived.
    if strict_world and set(b)!=set(a):
        issue(issues,'BOUNDARY_TRACKED_ENTITY_SET_CHANGED',before=sorted(b),after=sorted(a),inheritance_mode=mode)
    return {'pass':not issues,'issues':issues}

def lint_envelope(doc):
    issues=[]
    for cut in doc.get('cut_contracts') or []:
        mode=((cut.get('structured_continuity') or {}).get('inheritance_mode'))
        dist=cut.get('continuity_distance')
        cid=cut.get('cut_id')
        if mode and mode not in VALID_MODES:
            issue(issues,'CUT_BOUNDARY_INHERITANCE_MODE_INVALID',cut_id=cid,actual=mode)
        if dist is not None and dist not in VALID_DISTANCE:
            issue(issues,'CUT_BOUNDARY_DISTANCE_INVALID',cut_id=cid,actual=dist)
        if dist=='HIGH' and doc.get('format_mode')=='TIMED_MULTISHOT' and not cut.get('boundary_contract_ref'):
            issue(issues,'HIGH_CONTINUITY_DISTANCE_WITHOUT_CONTRACT_REF',cut_id=cid)
    return {'pass': not issues, 'issues': issues}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--contract'); ap.add_argument('--envelope'); ap.add_argument('--from-state'); ap.add_argument('--to-state'); a=ap.parse_args()
    if a.contract and a.from_state and a.to_state:
        base=lint_contract(load(a.contract)); trans=compare_states(load(a.contract),load(a.from_state),load(a.to_state)); out={'pass':base['pass'] and trans['pass'],'issues':base['issues']+trans['issues']}
    elif a.contract: out=lint_contract(load(a.contract))
    elif a.envelope: out=lint_envelope(load(a.envelope))
    else: out={'pass':False,'issues':[{'type':'ARGS_REQUIRED'}]}
    print(json.dumps(out, ensure_ascii=False, indent=2)); raise SystemExit(0 if out['pass'] else 2)

if __name__=='__main__': main()
