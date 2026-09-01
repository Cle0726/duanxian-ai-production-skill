#!/usr/bin/env python3
import argparse, hashlib, json, pathlib, yaml, copy, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'validators'))
from video_execution_plan_lint import lint
from temporal_integrity import load as tload, validate_snapshot_path
from temporal_entry_plan_lint import lint as lint_temporal_plan
from temporal_t0_sufficiency_lint import lint as lint_t0

def load(p):
    text=pathlib.Path(p).read_text(encoding='utf-8'); return json.loads(text) if pathlib.Path(p).suffix.lower()=='.json' else yaml.safe_load(text)
def canonical(d): return json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def dump(d,p): pathlib.Path(p).write_text(yaml.safe_dump(d,sort_keys=False,allow_unicode=True),encoding='utf-8')
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--plan',required=True); ap.add_argument('--output',required=True); ap.add_argument('--execution-plan-id',required=True); ap.add_argument('--video-unit-id',required=True); ap.add_argument('--shot-id'); ap.add_argument('--scene-id')
    for k in ['director','storyboard','shot-execution','scene-color','world-state']: ap.add_argument('--'+k+'-fp',required=True)
    ap.add_argument('--generation-envelope-id'); ap.add_argument('--generation-envelope-fp'); ap.add_argument('--format-mode',choices=['ONER','SEQUENTIAL_MULTISHOT','TIMED_MULTISHOT','FREESTYLE_BROLL']); ap.add_argument('--shot-id-list'); ap.add_argument('--temporal-entry-plan'); ap.add_argument('--temporal-t0-assessment'); a=ap.parse_args()
    d=load(a.plan); result=lint(d)
    if not result['pass']: print(json.dumps({'pass':False,'error':'VIDEO_EXECUTION_PLAN_LINT_FAIL','issues':result['issues']},ensure_ascii=False,indent=2)); return 2
    d=copy.deepcopy(d); d.update({'schema_version':1,'skill_version':'4.5.11','execution_plan_id':a.execution_plan_id,'video_unit_id':a.video_unit_id,'shot_id':a.shot_id,'scene_id':a.scene_id,'status':'FROZEN_FOR_COMPILE','video_execution_plan_pass':True})
    d['source_fingerprints']={'director':a.director_fp,'storyboard':a.storyboard_fp,'shot_execution':a.shot_execution_fp,'scene_color':a.scene_color_fp,'world_state':a.world_state_fp}
    if a.generation_envelope_id or a.generation_envelope_fp or a.format_mode:
        if not (a.generation_envelope_id and a.generation_envelope_fp and a.format_mode): print(json.dumps({'pass':False,'error':'GENERATION_ENVELOPE_FREEZE_ARGS_INCOMPLETE'})); return 2
        d['generation_envelope_id']=a.generation_envelope_id; d['format_mode']=a.format_mode; d['source_fingerprints']['generation_envelope']=a.generation_envelope_fp
        if a.shot_id_list: d['shot_ids']=[x.strip() for x in a.shot_id_list.split(',') if x.strip()]
    if a.temporal_entry_plan:
        tp=tload(a.temporal_entry_plan); lr=lint_temporal_plan(tp,a.temporal_entry_plan)
        if not lr['pass']: print(json.dumps({'pass':False,'error':'TEMPORAL_ENTRY_PLAN_INVALID','issues':lr['issues']},ensure_ascii=False,indent=2)); return 2
        same=tp.get('entry_mode') in {'SEAMLESS_EXTEND','GUIDED_CONTINUATION'}; ta=None
        if same:
            if not a.temporal_t0_assessment: print(json.dumps({'pass':False,'error':'TEMPORAL_T0_ASSESSMENT_REQUIRED'})); return 2
            ta=tload(a.temporal_t0_assessment); ar=lint_t0(ta,a.temporal_t0_assessment)
            if not ar['pass'] or ta.get('overall_verdict')!='SUFFICIENT': print(json.dumps({'pass':False,'error':'TEMPORAL_RESET_REQUIRED','issues':ar['issues']},ensure_ascii=False,indent=2)); return 2
            if ta.get('temporal_entry_plan_fingerprint')!=tp.get('temporal_entry_plan_fingerprint'): print(json.dumps({'pass':False,'error':'TEMPORAL_T0_ENTRY_PLAN_FINGERPRINT_MISMATCH'})); return 2
            sr=tp.get('continuity_snapshot_ref'); vr=validate_snapshot_path(sr)
            if not vr['pass'] or vr['snapshot'].get('snapshot_fingerprint')!=tp.get('continuity_snapshot_fingerprint'): print(json.dumps({'pass':False,'error':'TEMPORAL_CONTINUITY_SNAPSHOT_INVALID','issues':vr['issues']},ensure_ascii=False,indent=2)); return 2
        d['temporal_visual_isolation']={'entry_mode':tp.get('entry_mode'),'internal_conditioning_primary':tp.get('internal_conditioning_primary') or (d.get('reference_integrity') or {}).get('primary_visual'),'model_t0_owner':tp.get('model_t0_owner'),'prompt_profile':tp.get('prompt_profile'),'temporal_entry_plan_ref':str(pathlib.Path(a.temporal_entry_plan).resolve()),'temporal_entry_plan_fingerprint':tp.get('temporal_entry_plan_fingerprint'),'temporal_t0_sufficiency_ref':str(pathlib.Path(a.temporal_t0_assessment).resolve()) if a.temporal_t0_assessment else None,'temporal_t0_sufficiency_fingerprint':(ta or {}).get('assessment_fingerprint'),'continuity_snapshot_ref':tp.get('continuity_snapshot_ref'),'continuity_snapshot_fingerprint':tp.get('continuity_snapshot_fingerprint'),'target_frame_ref':tp.get('target_frame_ref'),'target_frame_fingerprint':tp.get('target_frame_fingerprint'),'provider_transport':tp.get('provider_transport') or {},'visual_isolation_pass':True}
        eh=d.get('entity_binding_handoff') or {}
        if same:
            eh['temporal_entry_plan_fingerprint']=tp.get('temporal_entry_plan_fingerprint'); eh['temporal_t0_sufficiency_fingerprint']=(ta or {}).get('assessment_fingerprint'); eh['continuity_snapshot_fingerprint']=tp.get('continuity_snapshot_fingerprint'); d['entity_binding_handoff']=eh
    post=lint(d)
    if not post['pass']: print(json.dumps({'pass':False,'error':'VIDEO_EXECUTION_PLAN_POST_BIND_LINT_FAIL','issues':post['issues']},ensure_ascii=False,indent=2)); return 2
    d.pop('execution_plan_fingerprint',None); d['execution_plan_fingerprint']=hashlib.sha256(canonical(d)).hexdigest(); dump(d,a.output)
    print(json.dumps({'pass':True,'execution_plan_ref':str(pathlib.Path(a.output)),'execution_plan_fingerprint':d['execution_plan_fingerprint']},ensure_ascii=False,indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
