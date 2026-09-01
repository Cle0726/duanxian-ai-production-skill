#!/usr/bin/env python3
import argparse, hashlib, json, pathlib, yaml, datetime, sys, re
ROOT=pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'validators'))
from video_prompt_detail_lint import lint as prompt_lint
from storyboard_to_video_prompt_handoff_lint import lint as storyboard_handoff_lint
from voice_prompt_handoff_lint import lint as voice_handoff_lint
from temporal_integrity import validate_snapshot_path, load

def sha_text(text): return hashlib.sha256(text.encode('utf-8')).hexdigest()
def temporal_prompt_lint(text,profile):
    issues=[]; norm=re.sub(r'\s+','',text)
    if len(norm)<20: issues.append({'type':'TEMPORAL_PROMPT_TOO_THIN'})
    if profile=='DELTA_CONTINUATION_PROMPT' and len(norm)>1800: issues.append({'type':'TEMPORAL_DELTA_PROMPT_OVEREXPANDED','char_count':len(norm)})
    return {'pass':not issues,'issues':issues,'content_char_count':len(norm)}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--prompt',required=True); ap.add_argument('--execution-plan',required=True); ap.add_argument('--output',required=True); ap.add_argument('--prompt-id',required=True); ap.add_argument('--video-unit-id',required=True); ap.add_argument('--shot-id'); ap.add_argument('--segment-type',choices=['AUTO','COMBAT','NON_COMBAT'],default='AUTO'); ap.add_argument('--voice-plan',required=True); ap.add_argument('--voice-handoff',required=True); a=ap.parse_args()
    text=pathlib.Path(a.prompt).read_text(encoding='utf-8'); plan=load(a.execution_plan)
    if plan.get('status')!='FROZEN_FOR_COMPILE' or plan.get('video_execution_plan_pass') is not True or not plan.get('execution_plan_fingerprint'): print(json.dumps({'pass':False,'error':'PROMPT_REQUIRES_FROZEN_EXECUTION_PLAN'},ensure_ascii=False)); return 2
    if plan.get('video_unit_id')!=a.video_unit_id: print(json.dumps({'pass':False,'error':'PROMPT_VIDEO_UNIT_PLAN_MISMATCH'},ensure_ascii=False)); return 2
    temporal=plan.get('temporal_visual_isolation') or {}; profile=temporal.get('prompt_profile') or 'FULL_SHOT_PROMPT'
    if profile=='FULL_SHOT_PROMPT': pl=prompt_lint(text,segment_type=a.segment_type)
    else: pl=temporal_prompt_lint(text,profile)
    if not pl['pass']: print(json.dumps({'pass':False,'error':'VIDEO_PROMPT_DETAIL_LINT_FAIL','detail':pl},ensure_ascii=False,indent=2)); return 2
    if temporal.get('entry_mode') in {'SEAMLESS_EXTEND','GUIDED_CONTINUATION'}:
        vr=validate_snapshot_path(temporal.get('continuity_snapshot_ref'))
        if not vr['pass'] or vr['snapshot'].get('snapshot_fingerprint')!=temporal.get('continuity_snapshot_fingerprint'): print(json.dumps({'pass':False,'error':'TEMPORAL_CONTINUITY_SNAPSHOT_INVALID_OR_STALE','issues':vr['issues']},ensure_ascii=False,indent=2)); return 2
    hl=storyboard_handoff_lint(plan,text)
    if not hl['pass']: print(json.dumps({'pass':False,'error':'STORYBOARD_TO_VIDEO_PROMPT_HANDOFF_GAP','detail':hl},ensure_ascii=False,indent=2)); return 2
    voice_plan=load(a.voice_plan); voice_handoff=load(a.voice_handoff); vl=voice_handoff_lint(voice_plan,voice_handoff,text,plan)
    if not vl['pass']: print(json.dumps({'pass':False,'error':'VOICE_DIRECTION_PROMPT_HANDOFF_FAIL','detail':vl},ensure_ascii=False,indent=2)); return 2
    vhfp=voice_handoff.get('handoff_fingerprint')
    if not vhfp: print(json.dumps({'pass':False,'error':'VOICE_PROMPT_HANDOFF_FINGERPRINT_MISSING'},ensure_ascii=False)); return 2
    out={'schema_version':1,'skill_version':'4.5.11','prompt_id':a.prompt_id,'video_unit_id':a.video_unit_id,'shot_id':a.shot_id,'generation_envelope_id':plan.get('generation_envelope_id'),'format_mode':plan.get('format_mode'),'shot_ids':plan.get('shot_ids') or ([a.shot_id] if a.shot_id else []),'status':'VALID','prompt_ref':str(pathlib.Path(a.prompt).resolve()),'prompt_fingerprint':sha_text(text),'content_char_count':pl['content_char_count'],'execution_plan_ref':str(pathlib.Path(a.execution_plan).resolve()),'execution_plan_fingerprint':plan['execution_plan_fingerprint'],'source_fingerprints':plan.get('source_fingerprints') or {},'storyboard_handoff_pass':True,'voice_handoff_pass':True,'voice_direction_plan_id':voice_plan.get('voice_direction_plan_id'),'voice_prompt_handoff_id':voice_handoff.get('voice_prompt_handoff_id'),'voice_prompt_handoff_fingerprint':vhfp,'segment_type':a.segment_type,'prompt_profile':profile,'temporal_entry_plan_fingerprint':temporal.get('temporal_entry_plan_fingerprint'),'temporal_t0_sufficiency_fingerprint':temporal.get('temporal_t0_sufficiency_fingerprint'),'continuity_snapshot_fingerprint':temporal.get('continuity_snapshot_fingerprint'),'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    pathlib.Path(a.output).write_text(yaml.safe_dump(out,sort_keys=False,allow_unicode=True),encoding='utf-8'); print(json.dumps({'pass':True,'prompt_ref':out['prompt_ref'],'prompt_fingerprint':out['prompt_fingerprint'],'content_char_count':out['content_char_count'],'prompt_profile':profile},ensure_ascii=False,indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
