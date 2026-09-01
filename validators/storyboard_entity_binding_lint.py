#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re
from pathlib import Path
import yaml

PREFIX={'HUMAN':'H_','PROP':'P_','ENVIRONMENT':'E_','CROWD':'C_','VEHICLE':'V_'}
ENTITY_KIND={'CHARACTER':'HUMAN','MINOR_HUMAN':'HUMAN','PROP':'PROP','ENVIRONMENT':'ENVIRONMENT','CROWD_ARCHETYPE':'CROWD','VEHICLE':'VEHICLE'}
FORBIDDEN_IDENTITY_KEYS={
    'face','facial_features','recognizable_face','hair','hairstyle','hair_style','costume','wardrobe','clothing_detail',
    'identity_feature','identity_specific_feature','eye_color','makeup','signature_adornment','uniform_pattern'
}
STATIC_ACTIONS={'STATIC_HOLD','IDLE_HOLD','STANDING_HOLD','SEATED_HOLD','NONE_INTENTIONAL'}

def load(p):
    return yaml.safe_load(Path(p).read_text(encoding='utf-8'))

def issue(issues,t,**kw):
    d={'type':t}; d.update(kw); issues.append(d)

def scan_forbidden(obj,path='$'):
    hits=[]
    if isinstance(obj,dict):
        for k,v in obj.items():
            kl=str(k).lower()
            if kl in FORBIDDEN_IDENTITY_KEYS:
                hits.append({'path':f'{path}.{k}','key':k})
            hits.extend(scan_forbidden(v,f'{path}.{k}'))
    elif isinstance(obj,list):
        for i,v in enumerate(obj): hits.extend(scan_forbidden(v,f'{path}[{i}]'))
    return hits

def lint(doc):
    issues=[]
    if doc.get('status')!='LOCKED':
        issue(issues,'STORYBOARD_ENTITY_BINDING_NOT_LOCKED',status=doc.get('status'))
    if doc.get('frame_projection_derived_from_camera') is not True:
        issue(issues,'STORYBOARD_FRAME_PROJECTION_AUTHORITY_INVALID')
    slots=doc.get('slots') or []
    by_slot={}; by_entity={}
    for s in slots:
        sid=s.get('slot_id'); eid=s.get('entity_id'); kind=s.get('slot_kind'); et=s.get('entity_type')
        if not sid:
            issue(issues,'STORYBOARD_SLOT_ID_MISSING'); continue
        if sid in by_slot:
            issue(issues,'STORYBOARD_SLOT_DUPLICATE',slot_id=sid)
        by_slot[sid]=s
        if eid in by_entity and by_entity[eid]!=sid:
            issue(issues,'STORYBOARD_ENTITY_MULTI_SLOT_ALIAS',entity_id=eid,slot_ids=[by_entity[eid],sid])
        else:
            by_entity[eid]=sid
        expected=PREFIX.get(kind)
        if expected and not sid.startswith(expected):
            issue(issues,'STORYBOARD_SLOT_PREFIX_KIND_MISMATCH',slot_id=sid,slot_kind=kind)
        expected_kind=ENTITY_KIND.get(et)
        if expected_kind and expected_kind!=kind:
            issue(issues,'STORYBOARD_SLOT_ENTITY_TYPE_MISMATCH',slot_id=sid,slot_kind=kind,entity_type=et)
        assets=s.get('approved_asset_ids') or []
        preferred=s.get('preferred_asset_id')
        if preferred and preferred not in assets:
            issue(issues,'STORYBOARD_PREFERRED_ASSET_NOT_IN_AUTHORITY_SET',slot_id=sid,preferred_asset_id=preferred)
        if s.get('criticality')=='CRITICAL' and s.get('visual_owner')!='PRIMARY_VISUAL_BAKED' and not assets:
            issue(issues,'STORYBOARD_CRITICAL_ENTITY_VISUAL_AUTHORITY_GAP',slot_id=sid,entity_id=eid)
    for p in doc.get('panel_states') or []:
        seen=set()
        for st in p.get('entity_states') or []:
            sid=st.get('slot_id')
            if sid in seen: issue(issues,'STORYBOARD_PANEL_SLOT_DUPLICATE',panel_asset_id=p.get('panel_asset_id'),slot_id=sid)
            seen.add(sid)
            slot=by_slot.get(sid)
            if not slot:
                issue(issues,'STORYBOARD_PANEL_UNKNOWN_SLOT',panel_asset_id=p.get('panel_asset_id'),slot_id=sid); continue
            for rel_key in ('gaze_target_slot','contact_target_slot'):
                target=st.get(rel_key)
                if target and target not in by_slot:
                    issue(issues,'STORYBOARD_RELATION_TARGET_UNKNOWN',panel_asset_id=p.get('panel_asset_id'),slot_id=sid,field=rel_key,target=target)
            for ps in st.get('held_prop_slots') or []:
                if ps not in by_slot or by_slot[ps].get('slot_kind')!='PROP':
                    issue(issues,'STORYBOARD_HELD_PROP_SLOT_INVALID',panel_asset_id=p.get('panel_asset_id'),slot_id=sid,prop_slot=ps)
            if slot.get('slot_kind')=='HUMAN':
                required=('world_zone','frame_region','depth_region','body_orientation','pose_state','action_state','action_phase')
                for k in required:
                    if not str(st.get(k) or '').strip():
                        issue(issues,'STORYBOARD_HUMAN_BLOCKING_UNDERSPECIFIED',panel_asset_id=p.get('panel_asset_id'),slot_id=sid,field=k)
                action=str(st.get('action_state') or '').strip()
                if action and action not in STATIC_ACTIONS and not str(st.get('motion_vector') or '').strip() and not str(st.get('contact_target_slot') or '').strip():
                    # A non-static action must at least expose a motion vector or interaction target.
                    issue(issues,'STORYBOARD_HUMAN_ACTION_DIRECTION_GAP',panel_asset_id=p.get('panel_asset_id'),slot_id=sid,action_state=action)
    for hit in scan_forbidden(doc.get('panel_states') or []):
        issue(issues,'STORYBOARD_IDENTITY_DETAIL_IN_METADATA_FAIL',**hit)
    return {'pass':not issues,'slot_count':len(slots),'panel_state_count':len(doc.get('panel_states') or []),'issues':issues}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--binding-map',required=True); a=ap.parse_args()
    out=lint(load(a.binding_map)); print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
