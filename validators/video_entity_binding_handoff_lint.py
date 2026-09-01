#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re
from pathlib import Path
import yaml

APPROVED={'APPROVED','APPROVED_SUPPORT','APPROVED_ASSEMBLY','APPROVED_SCOPED_FIGURE','APPROVED_VIDEO_CONDITIONING'}
IDENTITY_ROLES={'CHARACTER_IDENTITY','SCOPED_CHARACTER_APPEARANCE','IDENTITY_AUTHORITY','CHARACTER_CURRENT_LOOK'}

def slot_requires_identity(slot):
    if not slot or slot.get('slot_kind')!='HUMAN': return False
    pol=slot.get('identity_readability_policy','AUTO')
    if pol=='REQUIRED': return True
    if pol=='NOT_REQUIRED': return False
    return slot.get('criticality') in {'CRITICAL','SUPPORT'}

def identity_asset_ok(a, entity_id):
    if not a or a.get('status') not in APPROVED: return False
    role=str(a.get('authority_role') or '')
    typ=str(a.get('asset_type') or '')
    if role not in IDENTITY_ROLES and not any(x in typ for x in ('CHARACTER_MASTER','CHARACTER_VIEW','FUNCTIONAL_MINOR_HUMAN','MINOR_HUMAN')): return False
    subject=a.get('subject_entity_id') or a.get('entity_id')
    return subject==entity_id

def load(p):
    txt=Path(p).read_text(encoding='utf-8')
    return json.loads(txt) if Path(p).suffix.lower()=='.json' else yaml.safe_load(txt)
def norm(s):
    s=str(s or '').lower(); s=re.sub(r'[\s\u3000]+','',s); s=re.sub(r'[，。！？；：、“”‘’（）()\[\]【】<>《》,.;:!?\-—_~]+','',s); return s
def issue(arr,t,**kw): d={'type':t}; d.update(kw); arr.append(d)

def lint(binding_map, plan, prompt, registry=None, identity_readability=None, temporal_t0_assessment=None):
    issues=[]
    slots={s.get('slot_id'):s for s in binding_map.get('slots') or [] if s.get('slot_id')}
    used=set()
    for p in binding_map.get('panel_states') or []:
        for st in p.get('entity_states') or []:
            if st.get('slot_id'): used.add(st['slot_id'])
    hand=plan.get('entity_binding_handoff') or {}
    if hand.get('source_binding_map_id')!=binding_map.get('binding_map_id'):
        issue(issues,'VIDEO_ENTITY_BINDING_MAP_MISMATCH',expected=binding_map.get('binding_map_id'),actual=hand.get('source_binding_map_id'))
    binds={b.get('slot_id'):b for b in hand.get('bindings') or [] if b.get('slot_id')}
    if len(binds)!=len(hand.get('bindings') or []): issue(issues,'VIDEO_ENTITY_BINDING_DUPLICATE_SLOT')
    direct_ids=set((plan.get('reference_integrity') or {}).get('direct_reference_ids') or [])
    pnorm=norm(prompt)
    assets={a.get('asset_id'):a for a in (registry or {}).get('assets',[]) if a.get('asset_id')}
    readability_by_entity={c.get('entity_id'):c for c in (identity_readability or {}).get('characters',[]) if c.get('entity_id')}
    temporal=(plan.get('temporal_visual_isolation') or {})
    temporal_same=temporal.get('entry_mode') in {'SEAMLESS_EXTEND','GUIDED_CONTINUATION'}
    t0_by_slot={e.get('slot_id'):e for e in (temporal_t0_assessment or {}).get('entities',[]) if e.get('slot_id')}
    if temporal_same:
        if not temporal_t0_assessment or temporal_t0_assessment.get('assessment_fingerprint')!=temporal.get('temporal_t0_sufficiency_fingerprint'):
            issue(issues,'TEMPORAL_T0_ASSESSMENT_REQUIRED_OR_STALE')
        elif temporal_t0_assessment.get('temporal_entry_plan_fingerprint')!=temporal.get('temporal_entry_plan_fingerprint'):
            issue(issues,'TEMPORAL_T0_ENTRY_PLAN_FINGERPRINT_MISMATCH')
    if identity_readability:
        assessed_primary=identity_readability.get('primary_visual_asset_id')
        plan_primary=(plan.get('reference_integrity') or {}).get('primary_visual')
        if assessed_primary and plan_primary and assessed_primary!=plan_primary:
            issue(issues,'VIDEO_IDENTITY_READABILITY_PRIMARY_STALE',assessment_primary_visual_asset_id=assessed_primary,plan_primary_visual_asset_id=plan_primary)
    # Internal slot labels must never leak into model-facing prompt.
    for sid in used:
        if sid.lower() in prompt.lower(): issue(issues,'STORYBOARD_SLOT_LEAK_TO_VIDEO_PROMPT',slot_id=sid)
        s=slots.get(sid); b=binds.get(sid)
        if not s:
            issue(issues,'VIDEO_ENTITY_UNKNOWN_STORYBOARD_SLOT',slot_id=sid); continue
        if not b:
            issue(issues,'VIDEO_ENTITY_BINDING_HANDOFF_GAP',slot_id=sid,entity_id=s.get('entity_id')); continue
        if b.get('entity_id')!=s.get('entity_id'):
            issue(issues,'VIDEO_ENTITY_SLOT_ENTITY_MISMATCH',slot_id=sid,expected=s.get('entity_id'),actual=b.get('entity_id'))
        mode=b.get('resolution_mode')
        if slot_requires_identity(s):
            if not identity_readability and mode=='PRIMARY_VISUAL_BAKED':
                issue(issues,'VIDEO_IDENTITY_READABILITY_ASSESSMENT_REQUIRED',slot_id=sid,entity_id=s.get('entity_id'))
            elif identity_readability:
                rc=readability_by_entity.get(s.get('entity_id'))
                verdict=(rc or {}).get('identity_readability_verdict')
                if verdict in {'FAIL','UNKNOWN'}:
                    if mode=='TEMPORAL_T0_BAKED':
                        te=t0_by_slot.get(sid)
                        if not te or te.get('entity_id')!=s.get('entity_id') or te.get('verdict')!='SUFFICIENT' or not te.get('evidence_ref'):
                            issue(issues,'TEMPORAL_RESET_REQUIRED',slot_id=sid,entity_id=s.get('entity_id'))
                    elif mode!='DIRECT_REFERENCE':
                        issue(issues,'VIDEO_UNREADABLE_IDENTITY_NOT_DIRECT_BOUND',slot_id=sid,entity_id=s.get('entity_id'),verdict=verdict,resolution_mode=mode)
                    elif registry is not None:
                        aid=b.get('resolved_asset_id'); a=assets.get(aid)
                        if not identity_asset_ok(a,s.get('entity_id')):
                            issue(issues,'VIDEO_IDENTITY_DIRECT_ASSET_ENTITY_OR_ROLE_MISMATCH',slot_id=sid,entity_id=s.get('entity_id'),asset_id=aid,authority_role=(a or {}).get('authority_role'),subject_entity_id=(a or {}).get('subject_entity_id'))
                elif verdict!='PASS':
                    issue(issues,'VIDEO_IDENTITY_READABILITY_VERDICT_MISSING',slot_id=sid,entity_id=s.get('entity_id'),verdict=verdict or 'MISSING')
        if s.get('criticality')=='CRITICAL' and mode=='OMITTED':
            issue(issues,'VIDEO_CRITICAL_ENTITY_REFERENCE_CLOSURE_GAP',slot_id=sid)
        if s.get('slot_kind')=='HUMAN' and s.get('criticality')=='CRITICAL' and mode=='TEXT_CONTROL':
            issue(issues,'VIDEO_CRITICAL_HUMAN_TEXT_ONLY_FORBIDDEN',slot_id=sid)
        for field in ('prompt_identity_anchor','blocking_anchor','action_anchor'):
            val=b.get(field)
            if s.get('slot_kind')=='HUMAN' and (not val or len(norm(val))<6):
                issue(issues,'VIDEO_HUMAN_PROMPT_RECOVERABILITY_GAP',slot_id=sid,field=field)
            elif val and norm(val) not in pnorm:
                issue(issues,'VIDEO_ENTITY_PROMPT_ANCHOR_MISSING',slot_id=sid,field=field,anchor=val)
        if mode=='DIRECT_REFERENCE':
            aid=b.get('resolved_asset_id'); token=b.get('native_token')
            if not aid or aid not in (s.get('approved_asset_ids') or []):
                issue(issues,'VIDEO_ENTITY_DIRECT_ASSET_NOT_AUTHORIZED',slot_id=sid,asset_id=aid)
            if aid and aid not in direct_ids:
                issue(issues,'VIDEO_ENTITY_DIRECT_ASSET_NOT_IN_REFERENCE_PACK',slot_id=sid,asset_id=aid)
            if not token or token not in prompt:
                issue(issues,'VIDEO_ENTITY_DIRECT_TOKEN_MISSING_FROM_PROMPT',slot_id=sid,asset_id=aid,native_token=token)
            if registry is not None and aid:
                a=assets.get(aid)
                if not a or a.get('status') not in APPROVED:
                    issue(issues,'VIDEO_ENTITY_DIRECT_ASSET_NOT_APPROVED',slot_id=sid,asset_id=aid)
                elif token and a.get('native_token') and token!=a.get('native_token'):
                    issue(issues,'VIDEO_ENTITY_NATIVE_TOKEN_MISMATCH',slot_id=sid,asset_id=aid,expected=a.get('native_token'),actual=token)
        if mode=='TEMPORAL_T0_BAKED':
            te=t0_by_slot.get(sid)
            if not temporal_same or not te or te.get('entity_id')!=s.get('entity_id') or te.get('verdict')!='SUFFICIENT' or not te.get('evidence_ref'):
                issue(issues,'TEMPORAL_RESET_REQUIRED',slot_id=sid,entity_id=s.get('entity_id'))
            if b.get('resolved_asset_id') or b.get('native_token'):
                issue(issues,'TEMPORAL_CONTINUITY_AUXILIARY_VISUAL_REFERENCE_CONFLICT',slot_id=sid)
        if mode=='PRIMARY_VISUAL_BAKED':
            if not (plan.get('reference_integrity') or {}).get('primary_visual'):
                issue(issues,'VIDEO_ENTITY_BAKED_WITHOUT_PRIMARY_VISUAL',slot_id=sid)
            if s.get('criticality')=='CRITICAL' and not b.get('coverage_evidence_ref'):
                issue(issues,'VIDEO_CRITICAL_BAKED_EVIDENCE_MISSING',slot_id=sid)
    return {'pass':not issues,'used_slot_count':len(used),'issues':issues}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--binding-map',required=True); ap.add_argument('--execution-plan',required=True); ap.add_argument('--prompt',required=True); ap.add_argument('--registry'); ap.add_argument('--identity-readability'); ap.add_argument('--temporal-t0-assessment'); a=ap.parse_args()
    out=lint(load(a.binding_map),load(a.execution_plan),Path(a.prompt).read_text(encoding='utf-8'),load(a.registry) if a.registry else None,load(a.identity_readability) if a.identity_readability else None,load(a.temporal_t0_assessment) if a.temporal_t0_assessment else None)
    print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
