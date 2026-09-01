#!/usr/bin/env python3
"""Resolve Storyboard anonymous entity slots into Stage05 reference decisions.

Request format:
primary_visual_asset_id: SHOT_EXEC_01
slot_requests:
  - slot_id: H_A
    resolution_mode: PRIMARY_VISUAL_BAKED
    reason: already baked into approved shot execution frame
  - slot_id: P_A
    resolution_mode: DIRECT_REFERENCE
    asset_id: PROP_BACK
    reason: reverse face is not reliably visible in primary frame
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

APPROVED={'APPROVED','APPROVED_SUPPORT','APPROVED_ASSEMBLY','APPROVED_SCOPED_FIGURE','APPROVED_VIDEO_CONDITIONING'}
MODES={'PRIMARY_VISUAL_BAKED','DIRECT_REFERENCE','TEMPORAL_T0_BAKED','TEXT_CONTROL','OMITTED'}
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

def load(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))
def write(p,d): Path(p).write_text(yaml.safe_dump(d,sort_keys=False,allow_unicode=True),encoding='utf-8')
def fail(t,**kw): d={'pass':False,'error':t}; d.update(kw); return d

def resolve(binding_map, registry, request, budget, identity_readability=None, temporal_entry_plan=None, temporal_t0_assessment=None):
    slots={s['slot_id']:s for s in binding_map.get('slots') or []}
    assets={a.get('asset_id'):a for a in registry.get('assets') or [] if a.get('asset_id')}
    reqs={r.get('slot_id'):r for r in request.get('slot_requests') or [] if r.get('slot_id')}
    primary=request.get('primary_visual_asset_id')
    reference_policy=request.get('reference_policy') or 'LEGACY_ADAPTIVE'
    full_policy=reference_policy=='FULL_AUTHORITY_DIRECT_BINDING' or request.get('full_authority_direct_binding') is True
    provider_routed_policy=reference_policy=='FIELD_AUTHORITY_PROVIDER_ROUTED_BINDING'
    base_authority_direct=full_policy or provider_routed_policy
    if primary:
        pa=assets.get(primary)
        if not pa or pa.get('status') not in APPROVED:
            return fail('ENTITY_RESOLVER_PRIMARY_VISUAL_INVALID',asset_id=primary)
    out=[]; direct=[]; issues=[]
    readability_by_entity={}
    temporal_same=bool(temporal_entry_plan and temporal_entry_plan.get('entry_mode') in {'SEAMLESS_EXTEND','GUIDED_CONTINUATION'})
    t0_by_slot={e.get('slot_id'):e for e in (temporal_t0_assessment or {}).get('entities',[]) if e.get('slot_id')}
    if temporal_same:
        if not temporal_t0_assessment or temporal_t0_assessment.get('temporal_entry_plan_fingerprint')!=temporal_entry_plan.get('temporal_entry_plan_fingerprint'):
            issues.append({'type':'TEMPORAL_T0_ASSESSMENT_REQUIRED_OR_STALE'})
        elif temporal_t0_assessment.get('continuity_snapshot_fingerprint')!=temporal_entry_plan.get('continuity_snapshot_fingerprint'):
            issues.append({'type':'TEMPORAL_T0_SNAPSHOT_FINGERPRINT_MISMATCH'})
    if identity_readability:
        if identity_readability.get('primary_visual_asset_id') and primary and identity_readability.get('primary_visual_asset_id')!=primary:
            issues.append({'type':'IDENTITY_READABILITY_PRIMARY_VISUAL_STALE','assessment_primary_visual_asset_id':identity_readability.get('primary_visual_asset_id'),'current_primary_visual_asset_id':primary})
        readability_by_entity={c.get('entity_id'):c for c in identity_readability.get('characters') or [] if c.get('entity_id')}
    for sid,slot in slots.items():
        r=reqs.get(sid) or {}
        mode=r.get('resolution_mode')
        if base_authority_direct and slot.get('slot_kind') in {'HUMAN','ENVIRONMENT'}:
            if mode and mode!='DIRECT_REFERENCE':
                issues.append({'type':'BASE_AUTHORITY_DIRECT_BINDING_MODE_VIOLATION','slot_id':sid,'resolution_mode':mode,'reference_policy':reference_policy}); continue
            mode='DIRECT_REFERENCE'
        elif not mode:
            pol=slot.get('direct_reference_policy')
            mode='PRIMARY_VISUAL_BAKED' if primary and pol in {'AUTO_MINIMUM_SUFFICIENT','MUST_DIRECT_IF_NOT_BAKED'} else ('DIRECT_REFERENCE' if pol=='ALWAYS_DIRECT' else 'OMITTED')
        if mode not in MODES:
            issues.append({'type':'ENTITY_RESOLUTION_MODE_INVALID','slot_id':sid,'actual':mode}); continue
        pol=slot.get('direct_reference_policy')
        if pol=='ALWAYS_DIRECT' and mode!='DIRECT_REFERENCE':
            issues.append({'type':'ENTITY_ALWAYS_DIRECT_POLICY_VIOLATION','slot_id':sid,'resolution_mode':mode}); continue
        if pol=='NEVER_DIRECT' and mode=='DIRECT_REFERENCE':
            issues.append({'type':'ENTITY_NEVER_DIRECT_POLICY_VIOLATION','slot_id':sid}); continue
        reason=str(r.get('reason') or '').strip()
        if not reason:
            issues.append({'type':'ENTITY_RESOLUTION_REASON_MISSING','slot_id':sid}); continue
        resolved=None; token=None; evidence=r.get('coverage_evidence_ref')
        if temporal_same and mode=='DIRECT_REFERENCE':
            te=t0_by_slot.get(sid)
            if te and te.get('entity_id')==slot.get('entity_id') and te.get('verdict')=='SUFFICIENT' and te.get('evidence_ref'):
                mode='TEMPORAL_T0_BAKED'; evidence=te.get('evidence_ref'); reason=reason+' | T0 evidence sufficient'
            else:
                issues.append({'type':'TEMPORAL_RESET_REQUIRED','slot_id':sid,'entity_id':slot.get('entity_id'),'reason':'DIRECT_REFERENCE_WOULD_CONFLICT_WITH_SAME_TAKE_T0'}); continue
        if mode=='PRIMARY_VISUAL_BAKED':
            if not primary:
                issues.append({'type':'ENTITY_PRIMARY_VISUAL_BAKED_WITHOUT_PRIMARY','slot_id':sid})
            if slot.get('criticality')=='CRITICAL' and not evidence:
                issues.append({'type':'ENTITY_CRITICAL_BAKED_EVIDENCE_MISSING','slot_id':sid})
            if slot_requires_identity(slot):
                if not identity_readability:
                    issues.append({'type':'IDENTITY_READABILITY_ASSESSMENT_REQUIRED','slot_id':sid,'entity_id':slot.get('entity_id'),'required_action':'RUN_PLATFORM_SCALE_IDENTITY_ASSESSMENT'})
                else:
                    rc=readability_by_entity.get(slot.get('entity_id'))
                    verdict=(rc or {}).get('identity_readability_verdict')
                    if verdict!='PASS':
                        te=t0_by_slot.get(sid)
                        if temporal_same and te and te.get('entity_id')==slot.get('entity_id') and te.get('verdict')=='SUFFICIENT' and te.get('evidence_ref'):
                            mode='TEMPORAL_T0_BAKED'; evidence=te.get('evidence_ref'); reason=reason+' | T0 identity evidence sufficient'
                        else:
                            issues.append({'type':'TEMPORAL_RESET_REQUIRED' if temporal_same else 'IDENTITY_READABILITY_FAIL','slot_id':sid,'entity_id':slot.get('entity_id'),'verdict':verdict or 'MISSING','required_action':'LEGAL_TEMPORAL_RESET' if temporal_same else 'DIRECT_REFERENCE_OR_REGENERATE_READABLE_PRIMARY'})
        elif mode=='TEMPORAL_T0_BAKED':
            te=t0_by_slot.get(sid)
            if not temporal_same or not te or te.get('entity_id')!=slot.get('entity_id') or te.get('verdict')!='SUFFICIENT' or not te.get('evidence_ref'):
                issues.append({'type':'TEMPORAL_RESET_REQUIRED','slot_id':sid,'entity_id':slot.get('entity_id')}); continue
            evidence=te.get('evidence_ref')
        elif mode=='DIRECT_REFERENCE':
            aid=r.get('asset_id')
            if not aid and base_authority_direct and slot.get('slot_kind') in {'HUMAN','ENVIRONMENT'}:
                candidates=slot.get('approved_asset_ids') or []
                if slot.get('slot_kind')=='HUMAN':
                    accepted={'CHARACTER','CHARACTER_MASTER','FUNCTIONAL_MINOR_HUMAN_ASSET','MINOR_HUMAN_MASTER','MINOR_HUMAN_CANON_VIEW_SET'}
                    candidates=[x for x in candidates if (assets.get(x) or {}).get('asset_type') in accepted and x!=primary]
                else:
                    candidates=[x for x in candidates if (assets.get(x) or {}).get('asset_type') in {'EMPTY_ENVIRONMENT_MASTER','ENVIRONMENT_COVERAGE','RECIPROCAL_COVERAGE_VIEW'} and x!=primary]
                aid=candidates[0] if candidates else None
            if not aid:
                aid=slot.get('preferred_asset_id')
            if not aid:
                candidates=slot.get('approved_asset_ids') or []
                aid=candidates[0] if len(candidates)==1 else None
            if not aid or aid not in (slot.get('approved_asset_ids') or []):
                issues.append({'type':'ENTITY_DIRECT_ASSET_NOT_AUTHORIZED','slot_id':sid,'asset_id':aid}); continue
            a=assets.get(aid)
            if not a or a.get('status') not in APPROVED:
                issues.append({'type':'ENTITY_DIRECT_ASSET_NOT_APPROVED','slot_id':sid,'asset_id':aid}); continue
            if slot_requires_identity(slot) and identity_readability:
                rc=readability_by_entity.get(slot.get('entity_id'))
                verdict=(rc or {}).get('identity_readability_verdict')
                if verdict in {'FAIL','UNKNOWN'}:
                    if not identity_asset_ok(a,slot.get('entity_id')):
                        issues.append({'type':'IDENTITY_DIRECT_ASSET_ENTITY_OR_ROLE_MISMATCH','slot_id':sid,'entity_id':slot.get('entity_id'),'asset_id':aid,'authority_role':a.get('authority_role'),'subject_entity_id':a.get('subject_entity_id')}); continue
                    assessed=(rc or {}).get('direct_identity_authority_asset_id')
                    if assessed and assessed!=aid:
                        issues.append({'type':'IDENTITY_DIRECT_ASSET_ASSESSMENT_MISMATCH','slot_id':sid,'entity_id':slot.get('entity_id'),'assessment_asset_id':assessed,'resolved_asset_id':aid}); continue
            token=a.get('native_token') or (('@'+a.get('asset_display_name')) if a.get('asset_display_name') else None)
            if not token:
                issues.append({'type':'ENTITY_DIRECT_NATIVE_TOKEN_MISSING','slot_id':sid,'asset_id':aid}); continue
            resolved=aid; direct.append(aid)
        elif mode=='OMITTED' and slot.get('criticality')=='CRITICAL':
            issues.append({'type':'ENTITY_CRITICAL_SLOT_OMITTED','slot_id':sid})
        elif mode=='TEXT_CONTROL' and slot.get('slot_kind')=='HUMAN' and slot.get('criticality')=='CRITICAL':
            issues.append({'type':'ENTITY_CRITICAL_HUMAN_TEXT_ONLY_FORBIDDEN','slot_id':sid})
        out.append({
            'slot_id':sid,'entity_id':slot.get('entity_id'),'entity_type':slot.get('entity_type'),
            'prompt_entity_label':slot.get('prompt_entity_label'),'resolution_mode':mode,
            'resolved_asset_id':resolved,'native_token':token,'reason':reason,'coverage_evidence_ref':evidence,
            'prompt_identity_anchor':r.get('prompt_identity_anchor'),
            'blocking_anchor':r.get('blocking_anchor'),
            'action_anchor':r.get('action_anchor')
        })
    if len(direct)>budget:
        overflow_type='FULL_AUTHORITY_DIRECT_BINDING_BUDGET_INSUFFICIENT' if full_policy else ('PROVIDER_ROUTED_BINDING_BUDGET_OR_FIELD_CONFLICT' if provider_routed_policy else 'ENTITY_DIRECT_REFERENCE_BUDGET_OVERFLOW')
        issues.append({'type':overflow_type,'direct_count':len(direct),'budget':budget})
    if issues: return {'pass':False,'issues':issues}
    return {'pass':True,'schema_version':1,'skill_version':'4.5.10','reference_policy':reference_policy,'source_binding_map_id':binding_map.get('binding_map_id'),'primary_visual_asset_id':primary,'bindings':out,'direct_reference_ids':direct,'temporal_entry_plan_fingerprint':(temporal_entry_plan or {}).get('temporal_entry_plan_fingerprint'),'temporal_t0_sufficiency_fingerprint':(temporal_t0_assessment or {}).get('assessment_fingerprint'),'continuity_snapshot_fingerprint':(temporal_entry_plan or {}).get('continuity_snapshot_fingerprint')}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--binding-map',required=True); ap.add_argument('--registry',required=True); ap.add_argument('--request',required=True); ap.add_argument('--identity-readability'); ap.add_argument('--temporal-entry-plan'); ap.add_argument('--temporal-t0-assessment'); ap.add_argument('--direct-budget',type=int,default=4); ap.add_argument('--output'); a=ap.parse_args()
    out=resolve(load(a.binding_map),load(a.registry),load(a.request),a.direct_budget,load(a.identity_readability) if a.identity_readability else None,load(a.temporal_entry_plan) if a.temporal_entry_plan else None,load(a.temporal_t0_assessment) if a.temporal_t0_assessment else None)
    if a.output and out.get('pass'):
        clean={k:v for k,v in out.items() if k!='pass'}; write(a.output,clean)
    print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out.get('pass') else 2)
if __name__=='__main__': main()
