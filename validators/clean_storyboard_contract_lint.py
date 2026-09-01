#!/usr/bin/env python3
"""Validate V4.5.2 storyboard pixel contract from Asset Registry metadata.
Visual QC supplies the cleanliness booleans; this validator prevents annotated panels from being approved as formal storyboard visual evidence.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
import yaml

def load(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))
def lint(registry):
    issues=[]; count=0
    for a in registry.get('assets') or []:
        if a.get('asset_type') not in {'STORYBOARD_CLEAN_PANEL','STORYBOARD_CLEAN_SEQUENCE_BOARD'}: continue
        count+=1; aid=a.get('asset_id')
        if a.get('asset_type')=='STORYBOARD_CLEAN_PANEL' and a.get('layout_type') not in {'CLEAN_PANEL','SINGLE_FRAME'}:
            issues.append({'type':'STORYBOARD_PANEL_LAYOUT_NOT_CLEAN_SINGLE_FRAME','asset_id':aid,'layout_type':a.get('layout_type')})
        if a.get('storyboard_render_mode') != 'WHITE_LINE_STORYBOARD_ONLY':
            issues.append({'type':'STORYBOARD_NOT_WHITE_LINE_BASELINE','asset_id':aid,'storyboard_render_mode':a.get('storyboard_render_mode')})
        cl=a.get('storyboard_cleanliness')
        if not isinstance(cl,dict):
            issues.append({'type':'STORYBOARD_CLEANLINESS_QC_MISSING','asset_id':aid}); continue
        dirty=[k for k,v in cl.items() if v is True]
        # Identity-specific human detail flags are handled separately by storyboard_anonymity_lint,
        # but if they appear in cleanliness we still treat them as pixel contamination signals.
        if dirty: issues.append({'type':'STORYBOARD_PIXEL_ANNOTATION_FAIL','asset_id':aid,'present':dirty})
        if a.get('status') in {'APPROVED','APPROVED_VIDEO_CONDITIONING'} and dirty:
            issues.append({'type':'ANNOTATED_STORYBOARD_CANNOT_BE_APPROVED_CLEAN','asset_id':aid})
    return {'pass':not issues,'storyboard_asset_count':count,'issues':issues}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--registry',required=True); a=ap.parse_args(); out=lint(load(a.registry)); print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
