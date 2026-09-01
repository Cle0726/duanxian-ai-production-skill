#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

REQUIRED_MEDIA={'TEXT','IMAGE','AUDIO'}
FORBIDDEN_MEDIA={'VIDEO'}

def load(p):
    return yaml.safe_load(Path(p).read_text(encoding='utf-8'))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--host-profiles',default='adapters/generation/host_profiles.yaml')
    ap.add_argument('--platform-profile',default='adapters/generation/platform_profile.yaml')
    ap.add_argument('--json',action='store_true')
    a=ap.parse_args()
    hp=load(a.host_profiles); pp=load(a.platform_profile); issues=[]
    default=hp.get('default_target_profile')
    if default!='MULTIMODAL_ALL_ROUND_REFERENCE':
        issues.append({'type':'DEFAULT_VIDEO_REFERENCE_CAPABILITY_PROFILE_MISMATCH','actual':default})
    prof=(hp.get('profiles') or {}).get('MULTIMODAL_ALL_ROUND_REFERENCE') or {}
    for pname,pdata in (hp.get('profiles') or {}).items():
        pmedia=set((pdata or {}).get('supported_reference_media') or [])
        if 'VIDEO' in pmedia:
            issues.append({'type':'PROFILE_REFERENCE_VIDEO_POLICY_VIOLATION','profile':pname})
    if prof.get('reference_capability_class')!='MULTIMODAL_ALL_ROUND_REFERENCE':
        issues.append({'type':'ALL_ROUND_REFERENCE_CAPABILITY_CLASS_MISSING'})
    media=set(prof.get('supported_reference_media') or [])
    if not REQUIRED_MEDIA.issubset(media):
        issues.append({'type':'ALL_ROUND_REFERENCE_MEDIA_GAP','missing':sorted(REQUIRED_MEDIA-media)})
    if FORBIDDEN_MEDIA & media:
        issues.append({'type':'REFERENCE_VIDEO_POLICY_VIOLATION','present':sorted(FORBIDDEN_MEDIA & media)})
    if prof.get('reference_video_policy')!='FORBIDDEN_QUOTA_COST':
        issues.append({'type':'REFERENCE_VIDEO_HARD_POLICY_MISSING'})
    if prof.get('supports_motion_or_camera_video_reference') is not False:
        issues.append({'type':'REFERENCE_VIDEO_CAPABILITY_MUST_BE_DISABLED_AT_PROJECT_LAYER'})
    if prof.get('audio_asset_manifest_required_for_audio_reference') is not True:
        issues.append({'type':'AUDIO_MANIFEST_REFERENCE_POLICY_MISSING'})
    if prof.get('combined_multimodal_reference_job') is not True:
        issues.append({'type':'ALL_ROUND_REFERENCE_COMBINED_JOB_DISABLED'})
    if prof.get('role_aware_reference_assignment') is not True:
        issues.append({'type':'ALL_ROUND_REFERENCE_ROLE_ASSIGNMENT_DISABLED'})
    if prof.get('minimum_sufficient_reference_selection_required') is not True:
        issues.append({'type':'ALL_ROUND_REFERENCE_MINIMUM_SUFFICIENT_POLICY_MISSING'})
    if prof.get('provider_profile_required_for_exact_material_limits') is not True:
        issues.append({'type':'ALL_ROUND_REFERENCE_PROVIDER_LIMIT_POLICY_MISSING'})
    cap=pp.get('default_video_reference_capability') or {}
    if cap.get('class')!='MULTIMODAL_ALL_ROUND_REFERENCE':
        issues.append({'type':'PLATFORM_DEFAULT_REFERENCE_CAPABILITY_MISMATCH','actual':cap.get('class')})
    cap_media=set(cap.get('supported_reference_media') or [])
    if not REQUIRED_MEDIA.issubset(cap_media):
        issues.append({'type':'PLATFORM_ALL_ROUND_REFERENCE_MEDIA_GAP'})
    if 'VIDEO' in cap_media:
        issues.append({'type':'PLATFORM_REFERENCE_VIDEO_POLICY_VIOLATION'})
    if cap.get('reference_video_policy')!='FORBIDDEN_QUOTA_COST':
        issues.append({'type':'PLATFORM_REFERENCE_VIDEO_HARD_POLICY_MISSING'})
    vap=pp.get('visual_asset_policy') or {}
    if vap.get('video_reference_selection_policy') not in {'MINIMUM_SUFFICIENT_REFERENCE_SET','FIELD_AUTHORITY_PROVIDER_ROUTED_MINIMUM_SUFFICIENT_SET'}:
        issues.append({'type':'ALL_ROUND_REFERENCE_RESOLVER_POLICY_REGRESSION','actual':vap.get('video_reference_selection_policy')})
    if vap.get('asset_library_size_does_not_imply_job_reference_count') is not True:
        issues.append({'type':'ASSET_LIBRARY_REFERENCE_COUNT_SEPARATION_MISSING'})
    out={'pass':not issues,'default_target_profile':default,'issues':issues}
    print(json.dumps(out,ensure_ascii=False,indent=2) if a.json else out)
    raise SystemExit(0 if out['pass'] else 2)

if __name__=='__main__': main()
