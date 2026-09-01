#!/usr/bin/env python3
"""Deterministically prove Storyboard off-image direction survives into Final Video Prompt."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
import yaml

FIELDS=('CAMERA_MOTION','TIMING','CUT_NOCUT','ACTION_BEAT','PERFORMANCE','EYELINE','SHOT_RELATION','LANDING')
ALWAYS_REQUIRED={'CAMERA_MOTION','TIMING','CUT_NOCUT','ACTION_BEAT','LANDING'}


def load(path):
    p=Path(path); text=p.read_text(encoding='utf-8')
    return json.loads(text) if p.suffix.lower()=='.json' else yaml.safe_load(text)


def norm(s):
    s=str(s or '').lower()
    s=re.sub(r'[\s\u3000]+','',s)
    s=re.sub(r'[，。！？；：、“”‘’（）()\[\]【】<>《》,.;:!?\-—_~]+','',s)
    return s


def lint_structure(plan):
    issues=[]; h=plan.get('storyboard_handoff')
    if not isinstance(h,dict):
        return {'pass':False,'issues':[{'type':'STORYBOARD_HANDOFF_CONTRACT_MISSING'}]}
    src=h.get('source_storyboard_asset_ids') or []
    if not src: issues.append({'type':'STORYBOARD_HANDOFF_SOURCE_ASSETS_MISSING'})
    items=h.get('items') or []
    by={}
    for it in items:
        f=it.get('field')
        if f not in FIELDS:
            issues.append({'type':'STORYBOARD_HANDOFF_FIELD_UNKNOWN','field':f}); continue
        if f in by:
            issues.append({'type':'STORYBOARD_HANDOFF_FIELD_DUPLICATE','field':f}); continue
        by[f]=it
    for f in FIELDS:
        it=by.get(f)
        if not it:
            issues.append({'type':'STORYBOARD_HANDOFF_FIELD_MISSING','field':f}); continue
        app=it.get('applicability')
        if f in ALWAYS_REQUIRED and app!='REQUIRED':
            issues.append({'type':'STORYBOARD_HANDOFF_ALWAYS_REQUIRED_FIELD_WAIVED','field':f,'applicability':app})
        if app=='REQUIRED':
            if not str(it.get('source_text') or '').strip(): issues.append({'type':'STORYBOARD_HANDOFF_SOURCE_TEXT_MISSING','field':f})
            anchor=str(it.get('prompt_anchor') or '').strip()
            if len(norm(anchor))<6: issues.append({'type':'STORYBOARD_HANDOFF_PROMPT_ANCHOR_TOO_WEAK','field':f})
        elif app=='NOT_APPLICABLE':
            if not str(it.get('reason') or '').strip(): issues.append({'type':'STORYBOARD_HANDOFF_NA_REASON_MISSING','field':f})
        else:
            issues.append({'type':'STORYBOARD_HANDOFF_APPLICABILITY_INVALID','field':f,'applicability':app})
    return {'pass':not issues,'issues':issues}


def lint(plan,prompt_text):
    base=lint_structure(plan); issues=list(base['issues'])
    if base['pass']:
        pnorm=norm(prompt_text); h=plan['storyboard_handoff']
        for it in h.get('items') or []:
            if it.get('applicability')!='REQUIRED': continue
            anchor=norm(it.get('prompt_anchor'))
            if anchor not in pnorm:
                issues.append({'type':'STORYBOARD_TO_VIDEO_PROMPT_HANDOFF_GAP','field':it.get('field'),'prompt_anchor':it.get('prompt_anchor')})
    return {'pass':not issues,'error_code':None if not issues else 'STORYBOARD_TO_VIDEO_PROMPT_HANDOFF_GAP','issues':issues}


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--execution-plan',required=True); ap.add_argument('--prompt',required=True); a=ap.parse_args()
    out=lint(load(a.execution_plan),Path(a.prompt).read_text(encoding='utf-8'))
    print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)

if __name__=='__main__': main()
