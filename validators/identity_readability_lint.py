#!/usr/bin/env python3
"""Hard gate for named/readable humans at platform-effective Primary Visual scale."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

APPROVED={'APPROVED','APPROVED_SUPPORT','APPROVED_ASSEMBLY','APPROVED_SCOPED_FIGURE','APPROVED_VIDEO_CONDITIONING'}
VALID_BASIS={'PLATFORM_ACTUAL_SCALE','PLATFORM_PROFILE_SIMULATION'}
IDENTITY_ROLES={'CHARACTER_IDENTITY','SCOPED_CHARACTER_APPEARANCE','IDENTITY_AUTHORITY','CHARACTER_CURRENT_LOOK'}


def load(p):
    txt=Path(p).read_text(encoding='utf-8')
    return json.loads(txt) if Path(p).suffix.lower()=='.json' else yaml.safe_load(txt)

def add(arr,t,**kw):
    d={'type':t}; d.update(kw); arr.append(d)

def identity_asset_ok(a, entity_id=None):
    if not a or a.get('status') not in APPROVED:
        return False
    role=str(a.get('authority_role') or '')
    typ=str(a.get('asset_type') or '')
    if role not in IDENTITY_ROLES and not any(x in typ for x in ('CHARACTER_MASTER','CHARACTER_VIEW','FUNCTIONAL_MINOR_HUMAN','MINOR_HUMAN')):
        return False
    # Identity fallback must be bound to the exact entity. Missing subject is not proof.
    subject=a.get('subject_entity_id') or a.get('entity_id')
    if entity_id and subject!=entity_id:
        return False
    return True

def slot_requires_identity(slot):
    if not slot or slot.get('slot_kind')!='HUMAN':
        return False
    pol=slot.get('identity_readability_policy','AUTO')
    if pol=='REQUIRED': return True
    if pol=='NOT_REQUIRED': return False
    # AUTO: CRITICAL and SUPPORT humans are identity-readability candidates.
    # AMBIENT humans are excluded unless explicitly REQUIRED.
    return slot.get('criticality') in {'CRITICAL','SUPPORT'}

def required_entities(binding_map, shot_id):
    slots={s.get('slot_id'):s for s in (binding_map or {}).get('slots',[]) if s.get('slot_id')}
    used=[]
    for ps in (binding_map or {}).get('panel_states',[]):
        if ps.get('shot_id')!=shot_id: continue
        for st in ps.get('entity_states') or []:
            s=slots.get(st.get('slot_id'))
            if not slot_requires_identity(s): continue
            eid=s.get('entity_id')
            if eid and eid not in used: used.append(eid)
    return used

def runtime_unit(runtime, uid):
    for u in (runtime or {}).get('video_units',[]):
        if u.get('video_unit_id')==uid: return u
    return None

def pass_evidence_ok(c, scale, issues):
    eid=c.get('entity_id')
    basis=scale.get('evaluation_basis')
    # A declared PASS must carry real scale evidence, not only a verdict string.
    if basis=='PLATFORM_PROFILE_SIMULATION' and not scale.get('preview_manifest_ref'):
        add(issues,'IDENTITY_READABILITY_SCALE_EVIDENCE_MISSING',entity_id=eid,required='preview_manifest_ref')
    if basis=='PLATFORM_ACTUAL_SCALE' and not (scale.get('scale_evidence_ref') or scale.get('preview_manifest_ref')):
        add(issues,'IDENTITY_READABILITY_SCALE_EVIDENCE_MISSING',entity_id=eid,required='scale_evidence_ref_or_preview_manifest_ref')
    conf=c.get('identity_match_confidence')
    if conf not in {'HIGH','MEDIUM'}:
        add(issues,'IDENTITY_READABILITY_PASS_CONFIDENCE_TOO_LOW',entity_id=eid,confidence=conf)
    vis=c.get('visibility_status')
    if vis in {'NOT_VISIBLE','UNKNOWN'}:
        add(issues,'IDENTITY_READABILITY_PASS_VISIBILITY_INVALID',entity_id=eid,visibility_status=vis)
    # When the face is visibly presented, record the face extent at effective scale.
    if vis in {'VISIBLE','PARTIALLY_OCCLUDED'} and not c.get('face_box_at_effective_scale_px'):
        add(issues,'IDENTITY_READABILITY_PASS_FACE_EVIDENCE_MISSING',entity_id=eid,visibility_status=vis)

def lint(assessment, binding_map, runtime, registry):
    issues=[]; diagnostics=[]
    shot=assessment.get('shot_id'); uid=assessment.get('video_unit_id'); primary=assessment.get('primary_visual_asset_id')
    scale=assessment.get('platform_scale') or {}; basis=scale.get('evaluation_basis')
    if basis not in VALID_BASIS:
        add(issues,'IDENTITY_READABILITY_EVIDENCE_BASIS_FAIL',evaluation_basis=basis,reason='original resolution/file size cannot prove platform-scale identity readability')
    assets={a.get('asset_id'):a for a in (registry or {}).get('assets',[]) if a.get('asset_id')}
    u=runtime_unit(runtime,uid)
    stale=False
    if not u:
        add(issues,'IDENTITY_READABILITY_VIDEO_UNIT_MISSING',video_unit_id=uid)
    else:
        prim_ids={x.get('asset_id') for x in u.get('primary_assets') or []}
        if primary not in prim_ids:
            stale=True; add(issues,'IDENTITY_READABILITY_PRIMARY_VISUAL_STALE',assessment_primary_visual_asset_id=primary,current_primary_asset_ids=sorted(x for x in prim_ids if x))
    if primary not in assets:
        add(issues,'IDENTITY_READABILITY_PRIMARY_VISUAL_NOT_IN_REGISTRY',asset_id=primary)
    elif assessment.get('source_primary_visual_fingerprint') and assets[primary].get('fingerprint') and assessment.get('source_primary_visual_fingerprint')!=assets[primary].get('fingerprint'):
        stale=True; add(issues,'IDENTITY_READABILITY_PRIMARY_FINGERPRINT_STALE',asset_id=primary)

    req=required_entities(binding_map,shot)
    chars={c.get('entity_id'):c for c in assessment.get('characters') or [] if c.get('entity_id')}
    if not req:
        if assessment.get('status') not in {'NOT_APPLICABLE','PASS'}:
            add(issues,'IDENTITY_READABILITY_STATUS_MISMATCH',expected='NOT_APPLICABLE',actual=assessment.get('status'))
        return {'pass':not issues,'gate':'IDENTITY_READABILITY_PASS' if not issues else 'IDENTITY_READABILITY_FAIL','shot_id':shot,'video_unit_id':uid,'primary_visual_asset_id':primary,'identity_authority_mode':'NOT_APPLICABLE','diagnostics':diagnostics,'issues':issues}

    had_nonpass=False; all_nonpass_supported=True
    for eid in req:
        c=chars.get(eid)
        if not c:
            had_nonpass=True; all_nonpass_supported=False
            add(issues,'IDENTITY_READABILITY_ASSESSMENT_MISSING',shot_id=shot,entity_id=eid); continue
        if c.get('required_for_identity') is not True:
            had_nonpass=True; all_nonpass_supported=False
            add(issues,'IDENTITY_READABILITY_REQUIRED_ENTITY_MARKED_OPTIONAL',shot_id=shot,entity_id=eid); continue
        verdict=c.get('identity_readability_verdict')
        if verdict=='PASS':
            pass_evidence_ok(c,scale,issues)
            diagnostics.append({'type':'IDENTITY_READABILITY_PRIMARY_PASS','entity_id':eid})
            continue
        had_nonpass=True
        if verdict not in {'FAIL','UNKNOWN'}:
            all_nonpass_supported=False
            add(issues,'IDENTITY_READABILITY_REQUIRED_ENTITY_NO_VERDICT',entity_id=eid,verdict=verdict); continue
        diagnostics.append({'type':'IDENTITY_READABILITY_FAIL','entity_id':eid,'verdict':verdict,'reason':c.get('reason')})
        fallback=c.get('direct_identity_authority_asset_id')
        if not fallback:
            all_nonpass_supported=False
            add(issues,'IDENTITY_READABILITY_FAIL',shot_id=shot,entity_id=eid,verdict=verdict,required_action='DIRECT_CHARACTER_IDENTITY_AUTHORITY_OR_REGENERATE_READABLE_PRIMARY')
            continue
        fa=assets.get(fallback)
        if not identity_asset_ok(fa,eid):
            all_nonpass_supported=False
            add(issues,'IDENTITY_AUTHORITY_ENTITY_OR_ROLE_MISMATCH',entity_id=eid,asset_id=fallback,asset_type=(fa or {}).get('asset_type'),authority_role=(fa or {}).get('authority_role'),subject_entity_id=(fa or {}).get('subject_entity_id'))
            continue
        if u:
            bound=False
            for b in u.get('required_reference_bindings') or []:
                if b.get('asset_id')==fallback and b.get('binding_status')=='BOUND' and str(b.get('role') or '') in IDENTITY_ROLES:
                    bound=True; break
            selected=set((u.get('reference_budget') or {}).get('selected_direct_reference_ids') or [])
            if not bound or (selected and fallback not in selected):
                all_nonpass_supported=False
                add(issues,'IDENTITY_DIRECT_AUTHORITY_NOT_BOUND',entity_id=eid,asset_id=fallback,bound_record=bound,selected_direct=(fallback in selected if selected else None))
            else:
                diagnostics.append({'type':'IDENTITY_READABILITY_SUPPORTED_BY_DIRECT_AUTHORITY','entity_id':eid,'asset_id':fallback})

    if stale:
        expected='STALE'
    elif not had_nonpass:
        expected='PASS'
    elif all_nonpass_supported:
        expected='NEEDS_DIRECT_IDENTITY_SUPPORT'
    else:
        expected='BLOCKED'
    if assessment.get('status')!=expected:
        add(issues,'IDENTITY_READABILITY_STATUS_MISMATCH',expected=expected,actual=assessment.get('status'))

    mode='PRIMARY_VISUAL_SUFFICIENT'
    if had_nonpass: mode='PRIMARY_PLUS_DIRECT_IDENTITY'
    return {'pass':not issues,'gate':'IDENTITY_READABILITY_PASS' if not issues else 'IDENTITY_READABILITY_FAIL','shot_id':shot,'video_unit_id':uid,'primary_visual_asset_id':primary,'identity_authority_mode':mode,'diagnostics':diagnostics,'issues':issues}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--assessment',required=True); ap.add_argument('--binding-map',required=True); ap.add_argument('--runtime',required=True); ap.add_argument('--registry',required=True)
    a=ap.parse_args(); out=lint(load(a.assessment),load(a.binding_map),load(a.runtime),load(a.registry))
    print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
