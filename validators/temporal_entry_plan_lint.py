#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from temporal_integrity import load, fingerprint, validate_snapshot_path, sha_file, resolve_ref
SAME={'SEAMLESS_EXTEND','GUIDED_CONTINUATION'}
def lint(d,path=None):
    issues=[]; mode=d.get('entry_mode'); profile=d.get('prompt_profile'); owner=d.get('model_t0_owner'); tr=d.get('provider_transport') or {}
    exp={'SEAMLESS_EXTEND':'DELTA_CONTINUATION_PROMPT','GUIDED_CONTINUATION':'TRANSITION_PROMPT','CUT_REPROJECT':'FULL_SHOT_PROMPT','SCENE_REBASE':'FULL_SHOT_PROMPT'}.get(mode)
    if not exp: issues.append({'type':'TEMPORAL_ENTRY_MODE_INVALID','entry_mode':mode})
    elif profile!=exp: issues.append({'type':'TEMPORAL_PROMPT_PROFILE_MISMATCH','expected':exp,'actual':profile})
    if mode in SAME:
        if owner!='PREVIOUS_ENDING_ANCHOR': issues.append({'type':'TEMPORAL_T0_OWNER_INVALID','expected':'PREVIOUS_ENDING_ANCHOR','actual':owner})
        if tr.get('transport_type')=='GENERIC_REFERENCE' or tr.get('t0_semantics_verified') is not True or not tr.get('capability_evidence_ref'):
            issues.append({'type':'TEMPORAL_PROVIDER_T0_TRANSPORT_UNVERIFIED'})
        sr=d.get('continuity_snapshot_ref')
        if not sr: issues.append({'type':'TEMPORAL_CONTINUITY_SNAPSHOT_REQUIRED'})
        elif path:
            vr=validate_snapshot_path(resolve_ref(path,sr)); issues.extend(vr['issues'])
            if vr.get('snapshot') and d.get('continuity_snapshot_fingerprint')!=vr['snapshot'].get('snapshot_fingerprint'): issues.append({'type':'TEMPORAL_CONTINUITY_SNAPSHOT_FINGERPRINT_MISMATCH'})
        if mode=='GUIDED_CONTINUATION':
            if not d.get('target_frame_ref') or not d.get('target_frame_fingerprint'): issues.append({'type':'TEMPORAL_GUIDED_TARGET_REQUIRED'})
            if tr.get('endpoint_semantics_verified') is not True or not tr.get('endpoint_evidence_ref'): issues.append({'type':'TEMPORAL_PROVIDER_ENDPOINT_TRANSPORT_UNVERIFIED'})
    else:
        if owner not in {'SHOT_EXECUTION_FRAME','CANON_DERIVED_EXECUTION_FRAME'}: issues.append({'type':'TEMPORAL_T0_OWNER_INVALID','actual':owner})
        if not d.get('internal_conditioning_primary'): issues.append({'type':'TEMPORAL_INTERNAL_CONDITIONING_PRIMARY_REQUIRED'})
        if mode=='CUT_REPROJECT':
            cam=d.get('camera_topology') or {}
            for k in ('camera_zone','viewing_direction','axis_side','target_anchor'):
                if not cam.get(k): issues.append({'type':'TEMPORAL_CUT_CAMERA_TOPOLOGY_GAP','field':k})
    actual=fingerprint(d,'temporal_entry_plan_fingerprint')
    if d.get('temporal_entry_plan_fingerprint')!=actual: issues.append({'type':'TEMPORAL_ENTRY_PLAN_FINGERPRINT_INVALID','expected':actual,'actual':d.get('temporal_entry_plan_fingerprint')})
    return {'pass':not issues,'issues':issues,'fingerprint':actual}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('plan'); a=ap.parse_args(); d=load(a.plan); out=lint(d,a.plan); print(json.dumps(out,ensure_ascii=False,indent=2)); return 0 if out['pass'] else 2
if __name__=='__main__': raise SystemExit(main())
