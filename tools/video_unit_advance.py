#!/usr/bin/env python3
"""Advance an episode from an approved unit to the next Video Unit deterministically."""
import argparse, json, pathlib, yaml, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'validators'))
from temporal_integrity import validate_snapshot_path

def load(p):
    text=pathlib.Path(p).read_text(encoding='utf-8')
    return json.loads(text) if pathlib.Path(p).suffix.lower()=='.json' else yaml.safe_load(text)
def dump(d,p): pathlib.Path(p).write_text(yaml.safe_dump(d,sort_keys=False,allow_unicode=True),encoding='utf-8')
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--state',required=True); ap.add_argument('--snapshot',required=True); ap.add_argument('--output',required=True); a=ap.parse_args()
    vr=validate_snapshot_path(a.snapshot)
    if not vr['pass']:
        print(json.dumps({'pass':False,'error':'CONTINUITY_SNAPSHOT_INVALID','issues':vr['issues']},ensure_ascii=False,indent=2)); return 2
    st=load(a.state); snap=load(a.snapshot); vu=st.get('video_units') or {}; ordered=vu.get('ordered_ids') or []; current=vu.get('current_video_unit_id') or st.get('current_segment_id'); completed=list(vu.get('completed_ids') or [])
    if not current or current not in ordered:
        print(json.dumps({'pass':False,'error':'CURRENT_VIDEO_UNIT_NOT_IN_ORDER'},ensure_ascii=False)); return 2
    if current not in completed: completed.append(current)
    idx=ordered.index(current); next_id=ordered[idx+1] if idx+1<len(ordered) else None
    vu['completed_ids']=completed; vu['current_video_unit_id']=next_id; vu['next_video_unit_id']=ordered[idx+2] if next_id and idx+2<len(ordered) else None; vu['all_units_complete']=next_id is None; vu['next_video_unit_available']=next_id is not None; vu['current_video_unit_advanced']=True; vu['continuity_entry_written']=True; vu['required_segments_approved']=next_id is None and set(completed)==set(ordered); vu['no_remaining_video_units']=next_id is None
    st['video_units']=vu; st['previous_approved_ending_frame']={'artifact_id':snap.get('ending_frame_ref'),'status':'APPROVED','fingerprint_type':'FILE_SHA256','fingerprint':snap.get('ending_frame_file_sha256'),'source_refs':[snap.get('snapshot_id')]}
    if next_id:
        st['current_segment_id']=next_id; st['next_action']='BUILD_NEXT_UNIT_STORYBOARD'; st['waiting_reason']=None
    else:
        st['next_action']='ENTER_POST'; st['waiting_reason']=None
    dump(st,a.output)
    print(json.dumps({'pass':True,'completed_video_unit_id':current,'next_video_unit_id':next_id,'all_units_complete':next_id is None,'next_video_unit_available':next_id is not None,'current_video_unit_advanced':True,'continuity_entry_written':True,'required_segments_approved':next_id is None and set(completed)==set(ordered),'no_remaining_video_units':next_id is None},ensure_ascii=False,indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
