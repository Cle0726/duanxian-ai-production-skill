#!/usr/bin/env python3
import argparse, hashlib, json, pathlib, yaml, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'validators'))
from temporal_integrity import load, validate_snapshot_path

def canonical_fp(d):
    x=dict(d); x.pop('execution_plan_fingerprint',None)
    return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--job',required=True); ap.add_argument('--prompt-artifact',required=True); ap.add_argument('--execution-plan',required=True); a=ap.parse_args(); j=load(a.job); pa=load(a.prompt_artifact); ep=load(a.execution_plan); issues=[]
    if j.get('media_kind')!='VIDEO': print(json.dumps({'pass':True,'skipped':True},ensure_ascii=False,indent=2)); return 0
    for k in ['prompt_ref','prompt_fingerprint','execution_plan_ref','execution_plan_fingerprint','video_unit_id']:
        if not j.get(k): issues.append({'type':'VIDEO_JOB_REQUIRED_PROMPT_BINDING_MISSING','field':k})
    if pa.get('status')!='VALID': issues.append({'type':'VIDEO_PROMPT_ARTIFACT_NOT_VALID','status':pa.get('status')})
    if pa.get('voice_handoff_pass') is not True: issues.append({'type':'VIDEO_PROMPT_VOICE_HANDOFF_NOT_VALID','actual':pa.get('voice_handoff_pass')})
    for vk in ('voice_direction_plan_id','voice_prompt_handoff_id','voice_prompt_handoff_fingerprint'):
        if not pa.get(vk): issues.append({'type':'VIDEO_PROMPT_VOICE_BINDING_MISSING','field':vk})
    if ep.get('status')!='FROZEN_FOR_COMPILE' or ep.get('video_execution_plan_pass') is not True: issues.append({'type':'VIDEO_EXECUTION_PLAN_NOT_CURRENT'})
    pairs=[('prompt_ref',j.get('prompt_ref'),pa.get('prompt_ref')),('prompt_fingerprint',j.get('prompt_fingerprint'),pa.get('prompt_fingerprint')),('execution_plan_ref',j.get('execution_plan_ref'),pa.get('execution_plan_ref')),('execution_plan_fingerprint',j.get('execution_plan_fingerprint'),pa.get('execution_plan_fingerprint')),('video_unit_id',j.get('video_unit_id'),pa.get('video_unit_id'))]
    for name,a1,a2 in pairs:
        if a1 and a2 and a1!=a2: issues.append({'type':'VIDEO_JOB_PROMPT_BINDING_MISMATCH','field':name,'job':a1,'artifact':a2})
    if pa.get('execution_plan_fingerprint') and ep.get('execution_plan_fingerprint') and pa['execution_plan_fingerprint']!=ep['execution_plan_fingerprint']: issues.append({'type':'VIDEO_PROMPT_EXECUTION_PLAN_STALE'})
    temporal=ep.get('temporal_visual_isolation') or {}; same=temporal.get('entry_mode') in {'SEAMLESS_EXTEND','GUIDED_CONTINUATION'}
    if same:
        # Freezer-managed Temporal plans must retain their canonical self-hash; legacy hand-authored fixtures are not retroactively reinterpreted.
        if ep.get('temporal_visual_isolation') and canonical_fp(ep)!=ep.get('execution_plan_fingerprint'): issues.append({'type':'TEMPORAL_EXECUTION_PLAN_FINGERPRINT_INVALID'})
        tb=j.get('temporal_binding') or {}
        for k in ('entry_mode','prompt_profile','temporal_entry_plan_fingerprint','temporal_t0_sufficiency_fingerprint','continuity_snapshot_fingerprint'):
            expected=temporal.get(k)
            if tb.get(k)!=expected: issues.append({'type':'TEMPORAL_JOB_BINDING_FINGERPRINT_MISMATCH','field':k,'job':tb.get(k),'execution_plan':expected})
            if pa.get(k) != expected and k in {'prompt_profile','temporal_entry_plan_fingerprint','temporal_t0_sufficiency_fingerprint','continuity_snapshot_fingerprint'}: issues.append({'type':'TEMPORAL_PROMPT_BINDING_FINGERPRINT_MISMATCH','field':k})
        sr=temporal.get('continuity_snapshot_ref'); vr=validate_snapshot_path(sr)
        if not vr['pass'] or vr.get('snapshot',{}).get('snapshot_fingerprint')!=temporal.get('continuity_snapshot_fingerprint'): issues.append({'type':'TEMPORAL_CONTINUITY_SNAPSHOT_STALE','detail':vr['issues']})
        if any(b.get('binding_mode')=='PRIMARY_VIEW' for b in j.get('required_bindings') or []): issues.append({'type':'TEMPORAL_T0_MULTIPLE_PRIMARY_VISUAL_CONFLICT'})
        if any(b.get('resolution_mode')=='DIRECT_REFERENCE' for b in (ep.get('entity_binding_handoff') or {}).get('bindings') or []): issues.append({'type':'TEMPORAL_CONTINUITY_AUXILIARY_VISUAL_REFERENCE_CONFLICT'})
    try: dur=float(ep.get('duration_sec'))
    except Exception: dur=None
    if dur is not None and dur>15:
        q=ep.get('long_video_quota_confirmation') or {}
        if not (q.get('question_asked') is True and q.get('user_response')=='HAS_QUOTA' and q.get('confirmed_by')=='USER' and q.get('confirmation_ref')): issues.append({'type':'VIDEO_JOB_LONG_DURATION_QUOTA_UNCONFIRMED','duration_sec':dur,'threshold_sec':15.0})
    if ep.get('generation_envelope_id') or ep.get('format_mode'):
        for k in ['generation_envelope_id','format_mode']:
            if not j.get(k): issues.append({'type':'VIDEO_JOB_REQUIRED_ENVELOPE_BINDING_MISSING','field':k})
            if j.get(k) and ep.get(k) and j.get(k)!=ep.get(k): issues.append({'type':'VIDEO_JOB_ENVELOPE_BINDING_MISMATCH','field':k,'job':j.get(k),'execution_plan':ep.get(k)})
            if pa.get(k) and ep.get(k) and pa.get(k)!=ep.get(k): issues.append({'type':'VIDEO_PROMPT_ENVELOPE_BINDING_MISMATCH','field':k})
    hand=ep.get('entity_binding_handoff') or {}; job_bindings=j.get('required_bindings') or []; job_ids={b.get('asset_id') for b in job_bindings if b.get('asset_id')}; direct=[b for b in hand.get('bindings') or [] if b.get('resolution_mode')=='DIRECT_REFERENCE']
    for b in direct:
        aid=b.get('resolved_asset_id'); tok=b.get('native_token'); sid=b.get('slot_id')
        if not aid or aid not in job_ids: issues.append({'type':'VIDEO_JOB_ENTITY_DIRECT_BINDING_MISSING','slot_id':sid,'asset_id':aid})
        else:
            matches=[x for x in job_bindings if x.get('asset_id')==aid]
            if tok and not any(x.get('native_token')==tok or (x.get('native_token') is None and x.get('asset_display_name') and tok=='@'+x.get('asset_display_name')) for x in matches): issues.append({'type':'VIDEO_JOB_ENTITY_NATIVE_TOKEN_MISMATCH','slot_id':sid,'asset_id':aid,'expected_token':tok})
    pref=pa.get('prompt_ref')
    if pref and pathlib.Path(pref).is_file():
        text=pathlib.Path(pref).read_text(encoding='utf-8'); actual=hashlib.sha256(text.encode('utf-8')).hexdigest()
        if actual!=pa.get('prompt_fingerprint'): issues.append({'type':'VIDEO_PROMPT_FILE_FINGERPRINT_MISMATCH'})
        for b in direct:
            if b.get('native_token') and b.get('native_token') not in text: issues.append({'type':'VIDEO_PROMPT_ENTITY_NATIVE_TOKEN_MISSING','slot_id':b.get('slot_id'),'native_token':b.get('native_token')})
    out={'pass':not issues,'issues':issues}; print(json.dumps(out,ensure_ascii=False,indent=2)); return 0 if not issues else 2
if __name__=='__main__': raise SystemExit(main())
