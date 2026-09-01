#!/usr/bin/env python3
"""Deterministically bind Execution Plan, Prompt, Take and Continuity evidence into VIDEO_RUNTIME."""
import argparse, json, pathlib, yaml, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'validators'))
from temporal_integrity import validate_snapshot_path

def load(p):
    text=pathlib.Path(p).read_text(encoding='utf-8')
    return json.loads(text) if pathlib.Path(p).suffix.lower()=='.json' else yaml.safe_load(text)
def dump(d,p): pathlib.Path(p).write_text(yaml.safe_dump(d,sort_keys=False,allow_unicode=True),encoding='utf-8')
def fail(code,**kw): print(json.dumps({'pass':False,'error':code,**kw},ensure_ascii=False,indent=2)); return 2

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--runtime',required=True); ap.add_argument('--action',required=True,choices=['BIND_PLAN','BIND_PROMPT','CAPTURE_TAKE','BIND_CONTINUITY']); ap.add_argument('--artifact',required=True); ap.add_argument('--output',required=True); a=ap.parse_args()
    rt=load(a.runtime); x=load(a.artifact)
    if rt.get('runtime_type')!='VIDEO_RUNTIME': return fail('NOT_VIDEO_RUNTIME')
    if a.action=='BIND_PLAN':
        if x.get('status')!='FROZEN_FOR_COMPILE' or x.get('video_execution_plan_pass') is not True: return fail('EXECUTION_PLAN_NOT_FROZEN')
        rt['video_unit_id']=x.get('video_unit_id'); rt['execution_plan_ref']=str(pathlib.Path(a.artifact).resolve()); rt['execution_plan_fingerprint']=x.get('execution_plan_fingerprint'); rt['execution_plan_source_fingerprints']=x.get('source_fingerprints') or {}; rt['status']='VALID'
        # any new plan invalidates downstream prompt/take
        rt['prompt_artifact_ref']=None; rt['prompt_ref']=None; rt['prompt_fingerprint']=None; rt['video_take_id']=None; rt['video_take_fingerprint']=None
    elif a.action=='BIND_PROMPT':
        if x.get('status')!='VALID': return fail('PROMPT_ARTIFACT_NOT_VALID')
        if rt.get('execution_plan_fingerprint')!=x.get('execution_plan_fingerprint'): return fail('PROMPT_EXECUTION_PLAN_FINGERPRINT_MISMATCH')
        if rt.get('video_unit_id')!=x.get('video_unit_id'): return fail('PROMPT_VIDEO_UNIT_MISMATCH')
        rt['prompt_artifact_ref']=str(pathlib.Path(a.artifact).resolve()); rt['prompt_ref']=x.get('prompt_ref'); rt['prompt_fingerprint']=x.get('prompt_fingerprint'); rt['status']='VALID'
    elif a.action=='CAPTURE_TAKE':
        if not rt.get('prompt_fingerprint') or not rt.get('execution_plan_fingerprint'): return fail('VIDEO_TAKE_REQUIRES_BOUND_PLAN_AND_PROMPT')
        if x.get('media_kind')!='VIDEO' or x.get('status')!='VIDEO_TAKE_CAPTURED': return fail('VIDEO_JOB_NOT_CAPTURED')
        if x.get('prompt_fingerprint')!=rt.get('prompt_fingerprint') or x.get('execution_plan_fingerprint')!=rt.get('execution_plan_fingerprint'): return fail('VIDEO_TAKE_SOURCE_BINDING_MISMATCH')
        rt['video_take_id']=x.get('generation_job_id'); handles=x.get('result_handles') or []; rt['video_take_fingerprint']=(handles[-1].get('fingerprint') if handles else None); rt['status']='VALID'
    elif a.action=='BIND_CONTINUITY':
        vr=validate_snapshot_path(a.artifact)
        if not vr['pass']: return fail('CONTINUITY_SNAPSHOT_INVALID',issues=vr['issues'])
        if not x.get('ending_frame_ref') or not x.get('ending_frame_file_sha256'): return fail('CONTINUITY_REAL_ENDING_FRAME_MISSING')
        rt['continuity_snapshot_ref']=str(pathlib.Path(a.artifact).resolve()); rt['ending_frame_ref']=x.get('ending_frame_ref'); rt['status']='VALID'
    dump(rt,a.output); print(json.dumps({'pass':True,'action':a.action,'video_unit_id':rt.get('video_unit_id'),'execution_plan_fingerprint':rt.get('execution_plan_fingerprint'),'prompt_fingerprint':rt.get('prompt_fingerprint'),'video_take_id':rt.get('video_take_id'),'ending_frame_ref':rt.get('ending_frame_ref')},ensure_ascii=False,indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
