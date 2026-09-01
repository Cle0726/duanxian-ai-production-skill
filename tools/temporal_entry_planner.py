#!/usr/bin/env python3
import argparse, json, pathlib, yaml, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'validators'))
from temporal_integrity import load, validate_snapshot_path, fingerprint, sha_file
from temporal_entry_plan_lint import lint

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True); ap.add_argument('--plan-id',required=True); ap.add_argument('--video-unit-id',required=True); ap.add_argument('--mode',required=True,choices=['SEAMLESS_EXTEND','GUIDED_CONTINUATION','CUT_REPROJECT','SCENE_REBASE']); ap.add_argument('--scene-id'); ap.add_argument('--shot-id'); ap.add_argument('--internal-conditioning-primary'); ap.add_argument('--snapshot'); ap.add_argument('--target-frame'); ap.add_argument('--transport-type',default='GENERIC_REFERENCE'); ap.add_argument('--t0-semantics-verified',action='store_true'); ap.add_argument('--capability-evidence-ref'); ap.add_argument('--endpoint-semantics-verified',action='store_true'); ap.add_argument('--endpoint-evidence-ref'); ap.add_argument('--camera-topology'); ap.add_argument('--grace-window-sec',type=float,default=0.35); ap.add_argument('--overlap-sec',type=float,default=0.0); a=ap.parse_args()
    same=a.mode in {'SEAMLESS_EXTEND','GUIDED_CONTINUATION'}; snapref=snapfp=None
    if a.snapshot:
        vr=validate_snapshot_path(a.snapshot)
        if not vr['pass']:
            print(json.dumps({'pass':False,'error':'TEMPORAL_SNAPSHOT_INVALID','issues':vr['issues']},ensure_ascii=False,indent=2)); return 2
        snapref=str(pathlib.Path(a.snapshot).resolve()); snapfp=vr['snapshot']['snapshot_fingerprint']
    targetref=targetfp=None
    if a.target_frame:
        p=pathlib.Path(a.target_frame)
        if not p.is_file(): print(json.dumps({'pass':False,'error':'TEMPORAL_TARGET_FRAME_MISSING'},ensure_ascii=False)); return 2
        targetref=str(p.resolve()); targetfp=sha_file(p)
    cam=load(a.camera_topology) if a.camera_topology else None
    profile={'SEAMLESS_EXTEND':'DELTA_CONTINUATION_PROMPT','GUIDED_CONTINUATION':'TRANSITION_PROMPT','CUT_REPROJECT':'FULL_SHOT_PROMPT','SCENE_REBASE':'FULL_SHOT_PROMPT'}[a.mode]
    owner='PREVIOUS_ENDING_ANCHOR' if same else ('CANON_DERIVED_EXECUTION_FRAME' if a.mode=='SCENE_REBASE' else 'SHOT_EXECUTION_FRAME')
    d={'schema_version':1,'skill_version':'4.5.11','temporal_entry_plan_id':a.plan_id,'video_unit_id':a.video_unit_id,'scene_id':a.scene_id,'shot_id':a.shot_id,'entry_mode':a.mode,'model_t0_owner':owner,'internal_conditioning_primary':a.internal_conditioning_primary,'prompt_profile':profile,'continuity_snapshot_ref':snapref,'continuity_snapshot_fingerprint':snapfp,'target_frame_ref':targetref,'target_frame_fingerprint':targetfp,'provider_transport':{'transport_type':a.transport_type,'t0_semantics_verified':bool(a.t0_semantics_verified),'capability_evidence_ref':a.capability_evidence_ref,'endpoint_semantics_verified':bool(a.endpoint_semantics_verified),'endpoint_evidence_ref':a.endpoint_evidence_ref},'camera_topology':cam,'continuity_grace_window_sec':a.grace_window_sec,'generation_overlap_handle':{'enabled':a.overlap_sec>0,'overlap_sec':a.overlap_sec}}
    d['temporal_entry_plan_fingerprint']=fingerprint(d,'temporal_entry_plan_fingerprint')
    out=lint(d,a.output)
    # lint path needs file for relative refs, but refs emitted absolute; persist temp before lint.
    pathlib.Path(a.output).write_text(yaml.safe_dump(d,sort_keys=False,allow_unicode=True),encoding='utf-8'); out=lint(d,a.output)
    if not out['pass']:
        pathlib.Path(a.output).unlink(missing_ok=True); print(json.dumps({'pass':False,'error':'TEMPORAL_ENTRY_PLAN_LINT_FAIL','issues':out['issues']},ensure_ascii=False,indent=2)); return 2
    print(json.dumps({'pass':True,'temporal_entry_plan_ref':str(pathlib.Path(a.output).resolve()),'temporal_entry_plan_fingerprint':d['temporal_entry_plan_fingerprint'],'entry_mode':a.mode,'prompt_profile':profile},ensure_ascii=False,indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
