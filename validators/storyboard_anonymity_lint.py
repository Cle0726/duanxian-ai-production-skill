#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

def load(p):
    return yaml.safe_load(Path(p).read_text(encoding='utf-8'))

def lint(registry):
    issues=[]; count=0
    for a in registry.get('assets') or []:
        if a.get('asset_type') not in {'STORYBOARD_CLEAN_PANEL','STORYBOARD_CLEAN_SEQUENCE_BOARD'}:
            continue
        count+=1; aid=a.get('asset_id')
        policy=a.get('storyboard_human_render_policy')
        if policy not in {None,'ANONYMOUS_GEOMETRIC_HUMAN_ONLY'}:
            issues.append({'type':'STORYBOARD_HUMAN_POLICY_INVALID','asset_id':aid,'actual':policy})
        cl=a.get('storyboard_cleanliness') or {}
        banned=[]
        for key in ('recognizable_face_present','recognizable_hair_present','recognizable_costume_detail_present','identity_specific_feature_present'):
            if cl.get(key) is True:
                banned.append(key)
        if banned:
            issues.append({'type':'STORYBOARD_IDENTITY_SPECIFIC_HUMAN_FAIL','asset_id':aid,'present':banned})
    return {'pass': not issues, 'storyboard_asset_count':count, 'issues':issues}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--registry', required=True); a=ap.parse_args(); out=lint(load(a.registry)); print(json.dumps(out, ensure_ascii=False, indent=2)); raise SystemExit(0 if out['pass'] else 2)

if __name__=='__main__':
    main()
