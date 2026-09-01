#!/usr/bin/env python3
import argparse, json, sys
from pathlib import Path
import yaml
from storyboard_to_video_prompt_handoff_lint import lint_structure as lint_storyboard_handoff_structure

MAX_GAP = 0.35

def load_doc(path):
    text=Path(path).read_text(encoding='utf-8')
    return json.loads(text) if Path(path).suffix.lower()=='.json' else yaml.safe_load(text)
EPS = 1e-6


def _list(x):
    return x if isinstance(x, list) else []


def lint(d):
    issues=[]
    status=str(d.get('status','')).upper()
    pass_flag=d.get('video_execution_plan_pass')
    if status not in ('FROZEN_FOR_COMPILE','PASS','FROZEN'):
        issues.append({'type':'EXECUTION_PLAN_NOT_FROZEN','status':status or None})
    if pass_flag not in (True,'YES','PASS',1):
        issues.append({'type':'VIDEO_EXECUTION_PLAN_NOT_PASS'})

    duration=d.get('duration_sec')
    try:
        duration=float(duration)
        if duration <= 0: raise ValueError
    except Exception:
        duration=None
        issues.append({'type':'EXECUTION_DURATION_INVALID'})

    refs=d.get('reference_integrity') or {}
    if int(refs.get('conflict_count', len(_list(refs.get('conflicts')))) or 0) > 0 or _list(refs.get('conflicts')):
        issues.append({'type':'REFERENCE_EXECUTION_CONFLICT'})
    if not refs.get('primary_visual'):
        issues.append({'type':'EXECUTION_PRIMARY_VISUAL_MISSING'})
    if d.get('scene_bound', True) and not refs.get('scene_color_authority'):
        issues.append({'type':'EXECUTION_SCENE_COLOR_MISSING'})
    color_mode=refs.get('scene_color_reference_mode')
    if color_mode is not None and color_mode not in ('LINEAGE_ONLY','TEXT_CONTROL','DIRECT_REFERENCE'):
        issues.append({'type':'VIDEO_COLOR_REFERENCE_MODE_INVALID','mode':color_mode})
    if color_mode=='DIRECT_REFERENCE' and not refs.get('scene_color_reference_reason'):
        issues.append({'type':'VIDEO_COLOR_REFERENCE_REASON_MISSING','mode':color_mode})
    direct_ids=set(_list(refs.get('direct_reference_ids')))
    color_id=refs.get('scene_color_authority')
    if color_mode in ('LINEAGE_ONLY','TEXT_CONTROL') and color_id and color_id in direct_ids:
        issues.append({'type':'VIDEO_COLOR_REFERENCE_MODE_CONFLICT','mode':color_mode,'color_asset_id':color_id})

    spatial=d.get('spatial_blocking') or {}
    if int(spatial.get('conflict_count', len(_list(spatial.get('conflicts')))) or 0) > 0 or _list(spatial.get('conflicts')):
        issues.append({'type':'EXECUTION_SPATIAL_PATH_CONFLICT'})
    for s in _list(spatial.get('subjects')):
        if s.get('critical',True):
            if not s.get('start') or not s.get('end'):
                issues.append({'type':'EXECUTION_SPATIAL_ENDPOINT_GAP','subject':s.get('id')})
            if s.get('moves',False) and not s.get('path_proven',False):
                issues.append({'type':'EXECUTION_MOTION_CORRIDOR_UNPROVEN','subject':s.get('id')})

    body=d.get('body_prop_occupancy') or {}
    if int(body.get('conflict_count', len(_list(body.get('conflicts')))) or 0) > 0 or _list(body.get('conflicts')):
        issues.append({'type':'EXECUTION_LIMB_OCCUPANCY_CONFLICT'})
    for s in _list(body.get('subjects')):
        if s.get('critical',True) and s.get('human',True) and not s.get('occupancy_clear',False):
            issues.append({'type':'EXECUTION_LIMB_OCCUPANCY_UNPROVEN','subject':s.get('id')})

    timing=d.get('timing') or {}
    if timing.get('fits') not in (True,'YES','PASS',1):
        issues.append({'type':'EXECUTION_TIMING_BUDGET_OVERFLOW'})

    conflicts=_list(d.get('conflicts'))
    if conflicts:
        issues.append({'type':'EXECUTION_PLAN_UNRESOLVED_CONFLICTS','count':len(conflicts)})

    # >15s is allowed, but explicit USER quota confirmation is mandatory before compile/generation.
    if duration is not None and duration > 15.0:
        q=d.get('long_video_quota_confirmation') or {}
        if q.get('question_asked') is not True:
            issues.append({'type':'LONG_VIDEO_QUOTA_QUESTION_NOT_ASKED','duration_sec':duration,'threshold_sec':15.0})
        response=q.get('user_response')
        if response == 'NO_QUOTA':
            issues.append({'type':'LONG_VIDEO_QUOTA_NOT_AVAILABLE','duration_sec':duration})
        elif response != 'HAS_QUOTA':
            issues.append({'type':'LONG_VIDEO_QUOTA_CONFIRMATION_REQUIRED','duration_sec':duration,'threshold_sec':15.0})
        if response == 'HAS_QUOTA' and (q.get('confirmed_by')!='USER' or not q.get('confirmation_ref')):
            issues.append({'type':'LONG_VIDEO_QUOTA_CONFIRMATION_EVIDENCE_MISSING','duration_sec':duration})

    windows=_list(d.get('windows'))
    if not windows:
        issues.append({'type':'EXECUTION_WINDOWS_MISSING'})
    parsed=[]
    for i,w in enumerate(windows):
        wid=w.get('id',f'W{i+1}')
        try:
            st=float(w.get('start')); en=float(w.get('end'))
            if en <= st: raise ValueError
            parsed.append((st,en,wid,w))
        except Exception:
            issues.append({'type':'EXECUTION_WINDOW_TIME_INVALID','window':wid})
            continue
        if int(w.get('dominant_camera_moves',1) or 0) > 1 and not w.get('camera_previs_proven',False):
            issues.append({'type':'EXECUTION_CAMERA_COMPETITION_CONFLICT','window':wid})
        if not w.get('primary_action') and not w.get('hold_state'):
            issues.append({'type':'EXECUTION_WINDOW_ACTION_GAP','window':wid})
        if w.get('performance_required',False):
            for key,code in [
                ('trigger','EXECUTION_PERFORMANCE_TRIGGER_GAP'),
                ('perception','EXECUTION_PERCEPTION_GAP'),
                ('micro_expression','EXECUTION_MICRO_EXPRESSION_GAP'),
                ('response','EXECUTION_CONTROLLED_RESPONSE_GAP')]:
                if not w.get(key): issues.append({'type':code,'window':wid})
        cam=w.get('camera') or {}
        if cam and not cam.get('landing'):
            issues.append({'type':'EXECUTION_CAMERA_LANDING_GAP','window':wid})

    if parsed and duration is not None:
        parsed.sort(key=lambda x:x[0])
        if parsed[0][0] > MAX_GAP:
            issues.append({'type':'EXECUTION_TIMELINE_ENTRY_GAP','gap':parsed[0][0]})
        prev_end=parsed[0][1]
        for st,en,wid,w in parsed[1:]:
            if st < prev_end - EPS:
                issues.append({'type':'EXECUTION_WINDOW_OVERLAP','window':wid})
            elif st-prev_end > MAX_GAP:
                issues.append({'type':'EXECUTION_TIMELINE_GAP','before_window':wid,'gap':round(st-prev_end,3)})
            prev_end=max(prev_end,en)
        if duration-prev_end > MAX_GAP:
            issues.append({'type':'EXECUTION_TIMELINE_EXIT_GAP','gap':round(duration-prev_end,3)})
        if prev_end-duration > MAX_GAP:
            issues.append({'type':'EXECUTION_TIMELINE_EXCEEDS_DURATION','overflow':round(prev_end-duration,3)})

    ending=d.get('ending_state') or {}
    if not ending or not ending.get('landing'):
        issues.append({'type':'EXECUTION_ENDING_STATE_GAP'})

    order=str(d.get('assembly_order','')).upper()
    if order not in ('CHRONOLOGICAL','TIME_CAUSAL','CHRONOLOGICAL_CAUSAL'):
        issues.append({'type':'EXECUTION_ASSEMBLY_ORDER_INVALID','value':order or None})

    # Generation Envelope closure. Backward compatible: only active when format/envelope fields are present.
    mode=d.get('format_mode')
    envelope_id=d.get('generation_envelope_id')
    shot_ids=_list(d.get('shot_ids'))
    if mode or envelope_id:
        if not envelope_id:
            issues.append({'type':'VIDEO_EXECUTION_PLAN_ENVELOPE_MISSING'})
        if mode not in ('ONER','SEQUENTIAL_MULTISHOT','TIMED_MULTISHOT','FREESTYLE_BROLL'):
            issues.append({'type':'VIDEO_EXECUTION_PLAN_FORMAT_INVALID','format_mode':mode})
        if not shot_ids:
            issues.append({'type':'VIDEO_EXECUTION_PLAN_SHOT_IDS_MISSING'})
        sh=d.get('storyboard_handoff') or {}
        cut_handoffs=_list(sh.get('cut_handoffs'))
        if mode=='ONER':
            if len(shot_ids)!=1:
                issues.append({'type':'VIDEO_EXECUTION_PLAN_ONER_SHOT_COUNT_FAIL','shot_count':len(shot_ids)})
            if cut_handoffs and len(cut_handoffs)!=1:
                issues.append({'type':'VIDEO_EXECUTION_PLAN_ONER_CUT_HANDOFF_FAIL','cut_count':len(cut_handoffs)})
        elif mode in ('SEQUENTIAL_MULTISHOT','TIMED_MULTISHOT','FREESTYLE_BROLL'):
            if len(shot_ids)<2:
                issues.append({'type':'VIDEO_EXECUTION_PLAN_MULTISHOT_SHOT_COUNT_FAIL','shot_count':len(shot_ids)})
            if len(cut_handoffs)!=len(shot_ids):
                issues.append({'type':'VIDEO_EXECUTION_PLAN_CUT_HANDOFF_COUNT_FAIL','shot_count':len(shot_ids),'cut_handoff_count':len(cut_handoffs)})
            if not sh.get('generation_envelope_storyboard_grid_asset_id') or not sh.get('generation_envelope_storyboard_grid_fingerprint'):
                issues.append({'type':'VIDEO_EXECUTION_PLAN_STORYBOARD_GRID_MISSING'})
            if mode=='TIMED_MULTISHOT':
                for c in cut_handoffs:
                    if c.get('start_sec') is None or c.get('end_sec') is None:
                        issues.append({'type':'VIDEO_EXECUTION_PLAN_TIMED_CUT_GAP','cut_id':c.get('cut_id')})
        sf=d.get('source_fingerprints') or {}
        if not sf.get('generation_envelope'):
            issues.append({'type':'VIDEO_EXECUTION_PLAN_ENVELOPE_FINGERPRINT_MISSING'})


    temporal=d.get('temporal_visual_isolation') or None
    if temporal:
        mode=temporal.get('entry_mode'); same=mode in {'SEAMLESS_EXTEND','GUIDED_CONTINUATION'}
        expected_profile={'SEAMLESS_EXTEND':'DELTA_CONTINUATION_PROMPT','GUIDED_CONTINUATION':'TRANSITION_PROMPT','CUT_REPROJECT':'FULL_SHOT_PROMPT','SCENE_REBASE':'FULL_SHOT_PROMPT'}.get(mode)
        if temporal.get('prompt_profile')!=expected_profile: issues.append({'type':'TEMPORAL_PROMPT_PROFILE_MISMATCH'})
        if temporal.get('visual_isolation_pass') is not True: issues.append({'type':'TEMPORAL_VISUAL_ISOLATION_NOT_PASS'})
        if same:
            if temporal.get('model_t0_owner')!='PREVIOUS_ENDING_ANCHOR': issues.append({'type':'TEMPORAL_T0_OWNER_INVALID'})
            for k in ('temporal_entry_plan_fingerprint','temporal_t0_sufficiency_fingerprint','continuity_snapshot_fingerprint'):
                if not temporal.get(k): issues.append({'type':'TEMPORAL_EXECUTION_BINDING_MISSING','field':k})
            tr=temporal.get('provider_transport') or {}
            if tr.get('t0_semantics_verified') is not True or tr.get('transport_type')=='GENERIC_REFERENCE' or not tr.get('capability_evidence_ref'):
                issues.append({'type':'TEMPORAL_PROVIDER_T0_TRANSPORT_UNVERIFIED'})
            if color_mode=='DIRECT_REFERENCE': issues.append({'type':'TEMPORAL_CONTINUITY_DIRECT_COLOR_REFERENCE_CONFLICT'})
        elif mode in {'CUT_REPROJECT','SCENE_REBASE'} and temporal.get('model_t0_owner') not in {'SHOT_EXECUTION_FRAME','CANON_DERIVED_EXECUTION_FRAME'}:
            issues.append({'type':'TEMPORAL_T0_OWNER_INVALID'})

    # Storyboard anonymous-slot -> real entity handoff closure.
    binding_map_id=d.get('storyboard_entity_binding_map_id')
    entity_handoff=d.get('entity_binding_handoff') or {}
    if binding_map_id:
        if entity_handoff.get('source_binding_map_id')!=binding_map_id:
            issues.append({'type':'VIDEO_ENTITY_BINDING_HANDOFF_MISSING_OR_MISMATCH','expected':binding_map_id,'actual':entity_handoff.get('source_binding_map_id')})
        eb=_list(entity_handoff.get('bindings'))
        if not eb:
            issues.append({'type':'VIDEO_ENTITY_BINDING_HANDOFF_MISSING'})
        seen=set()
        for b in eb:
            sid=b.get('slot_id')
            if not sid: issues.append({'type':'VIDEO_ENTITY_BINDING_SLOT_MISSING'})
            elif sid in seen: issues.append({'type':'VIDEO_ENTITY_BINDING_SLOT_DUPLICATE','slot_id':sid})
            seen.add(sid)
            if b.get('resolution_mode')=='TEMPORAL_T0_BAKED':
                if b.get('resolved_asset_id') or b.get('native_token'):
                    issues.append({'type':'TEMPORAL_CONTINUITY_AUXILIARY_VISUAL_REFERENCE_CONFLICT','slot_id':sid})
            if b.get('resolution_mode')=='DIRECT_REFERENCE':
                if not b.get('resolved_asset_id') or not b.get('native_token'):
                    issues.append({'type':'VIDEO_ENTITY_DIRECT_REFERENCE_INCOMPLETE','slot_id':sid})
                elif b.get('resolved_asset_id') not in direct_ids:
                    issues.append({'type':'VIDEO_ENTITY_DIRECT_REFERENCE_NOT_DECLARED','slot_id':sid,'asset_id':b.get('resolved_asset_id')})
    handoff=lint_storyboard_handoff_structure(d)
    issues.extend(handoff['issues'])

    return {'pass':not issues,'issues':issues,'window_count':len(windows)}


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('file',nargs='?'); a=ap.parse_args()
    d=load_doc(a.file) if a.file else json.load(sys.stdin)
    out=lint(d); print(json.dumps(out,ensure_ascii=False,indent=2))
    raise SystemExit(0 if out['pass'] else 2)

if __name__=='__main__': main()
