#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, pathlib, subprocess, yaml, datetime, shutil, sys, tempfile
ROOT=pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'validators'))
from temporal_integrity import validate_snapshot_path, fingerprint, sha_file

def load_state(p):
    if not p: return {}
    t=pathlib.Path(p).read_text(encoding='utf-8'); return json.loads(t) if pathlib.Path(p).suffix.lower()=='.json' else yaml.safe_load(t)
def sharpness(path):
    try:
        from PIL import Image, ImageFilter, ImageStat
        im=Image.open(path).convert('L'); edges=im.filter(ImageFilter.FIND_EDGES); return float(ImageStat.Stat(edges).var[0])
    except Exception: return 0.0
def extract_best(video,out,tail_window=0.32):
    if not shutil.which('ffmpeg') or not shutil.which('ffprobe'): raise RuntimeError('FFMPEG_UNAVAILABLE')
    cp=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',video],capture_output=True,text=True)
    if cp.returncode: raise RuntimeError('FFPROBE_FAILED')
    dur=float(cp.stdout.strip()); times=[max(0,dur-x) for x in (0.04,0.08,0.14,0.22,tail_window)]
    best=None
    with tempfile.TemporaryDirectory() as td:
        for i,t in enumerate(times):
            p=pathlib.Path(td)/f'f{i}.png'; c=subprocess.run(['ffmpeg','-y','-ss',f'{t:.3f}','-i',video,'-frames:v','1',str(p)],capture_output=True,text=True)
            if c.returncode or not p.is_file(): continue
            # proximity dominates, sharpness breaks bad-last-frame ties.
            sc=sharpness(p); score=(-abs(dur-t), sc)
            if best is None or score>best[0]: best=(score,p,t,sc)
        if not best: raise RuntimeError('ENDING_FRAME_EXTRACTION_FAILED')
        shutil.copyfile(best[1],out); return {'selected_timestamp_sec':best[2],'source_duration_sec':dur,'sharpness_score':best[3]}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--video-path'); ap.add_argument('--ending-frame-path'); ap.add_argument('--output-frame',required=True); ap.add_argument('--snapshot-output',required=True); ap.add_argument('--episode-id',required=True); ap.add_argument('--video-ref',required=True); ap.add_argument('--snapshot-id',required=True); ap.add_argument('--scene-id'); ap.add_argument('--segment-id'); ap.add_argument('--shot-id'); ap.add_argument('--exit-state'); ap.add_argument('--source-video-fingerprint'); ap.add_argument('--extraction-proof-ref'); ap.add_argument('--previous-snapshot'); ap.add_argument('--tail-window-sec',type=float,default=0.32); a=ap.parse_args()
    if bool(a.video_path)==bool(a.ending_frame_path):
        print(json.dumps({'pass':False,'error':'PROVIDE_EXACTLY_ONE_OF_VIDEO_OR_ENDING_FRAME'},ensure_ascii=False)); return 2
    out=pathlib.Path(a.output_frame); out.parent.mkdir(parents=True,exist_ok=True); selection={}
    try:
        if a.video_path:
            selection=extract_best(a.video_path,str(out),a.tail_window_sec); video_fp=sha_file(a.video_path); provenance='LOCAL_DECODED_VIDEO'; proof=None
        else:
            src=pathlib.Path(a.ending_frame_path)
            if not src.is_file(): raise RuntimeError('ENDING_FRAME_SOURCE_MISSING')
            if not a.source_video_fingerprint or len(a.source_video_fingerprint)!=64: raise RuntimeError('PLATFORM_EXTRACTED_SOURCE_VIDEO_FINGERPRINT_REQUIRED')
            if not a.extraction_proof_ref: raise RuntimeError('PLATFORM_EXTRACTED_PROOF_REQUIRED')
            shutil.copyfile(src,out); video_fp=a.source_video_fingerprint; provenance='PLATFORM_EXTRACTED_VERIFIED'; proof=a.extraction_proof_ref
    except Exception as e:
        print(json.dumps({'pass':False,'error':str(e)},ensure_ascii=False)); return 2
    prev_ref=prev_fp=None; depth=1
    if a.previous_snapshot:
        vr=validate_snapshot_path(a.previous_snapshot)
        if not vr['pass']:
            print(json.dumps({'pass':False,'error':'PREVIOUS_CONTINUITY_SNAPSHOT_INVALID','issues':vr['issues']},ensure_ascii=False,indent=2)); return 2
        prev_ref=str(pathlib.Path(a.previous_snapshot).resolve()); prev_fp=vr['snapshot']['snapshot_fingerprint']; depth=int(vr['snapshot']['pixel_lineage_depth'])+1
    state=load_state(a.exit_state)
    debt=state.get('degradation_debt') or {}
    debt={'sharpness_debt':float(debt.get('sharpness_debt',0.0)),'chroma_gamma_drift_debt':float(debt.get('chroma_gamma_drift_debt',0.0)),'noise_debt':float(debt.get('noise_debt',0.0)),'identity_debt':float(debt.get('identity_debt',0.0)),'generation_depth':depth}
    snap={'schema_version':1,'skill_version':'4.5.11','snapshot_id':a.snapshot_id,'episode_id':a.episode_id,'scene_id':a.scene_id,'segment_id':a.segment_id,'shot_id':a.shot_id,'source_approved_video_ref':a.video_ref,'source_video_fingerprint':video_fp,'provenance_mode':provenance,'extraction_proof_ref':proof,'ending_frame_ref':str(out.resolve()),'ending_frame_file_sha256':sha_file(out),'previous_continuity_snapshot_ref':prev_ref,'previous_continuity_snapshot_fingerprint':prev_fp,'pixel_lineage_depth':depth,'lineage_evidence_mode':'RECURSIVE_SNAPSHOT' if prev_ref else 'ROOT_GENERATED_VIDEO','degradation_debt':debt,'continuity_motion_capsule':state.get('continuity_motion_capsule') or {'ongoing_action_state':state.get('ongoing_action_state',{}),'screen_direction_state':state.get('screen_direction_state',{})},'actor_state':state.get('actor_state',{}),'wardrobe_state':state.get('wardrobe_state',{}),'injury_state':state.get('injury_state',{}),'prop_state':state.get('prop_state',{}),'environment_state':state.get('environment_state',{}),'ongoing_action_state':state.get('ongoing_action_state',{}),'screen_direction_state':state.get('screen_direction_state',{}),'ending_anchor_selection':selection,'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    snap['snapshot_fingerprint']=fingerprint(snap,'snapshot_fingerprint')
    pathlib.Path(a.snapshot_output).write_text(yaml.safe_dump(snap,sort_keys=False,allow_unicode=True),encoding='utf-8')
    vr=validate_snapshot_path(a.snapshot_output)
    if not vr['pass']:
        print(json.dumps({'pass':False,'error':'CONTINUITY_SNAPSHOT_POSTWRITE_INVALID','issues':vr['issues']},ensure_ascii=False,indent=2)); return 2
    print(json.dumps({'pass':True,'ending_frame_ref':snap['ending_frame_ref'],'ending_frame_file_sha256':snap['ending_frame_file_sha256'],'continuity_snapshot_ref':str(pathlib.Path(a.snapshot_output).resolve()),'snapshot_fingerprint':snap['snapshot_fingerprint'],'pixel_lineage_depth':depth},ensure_ascii=False,indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
