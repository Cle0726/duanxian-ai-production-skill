#!/usr/bin/env python3
"""Gate for user quota confirmation on video plans longer than 15 seconds.

This is NOT a duration ceiling. <=15s passes automatically. >15s requires an
explicit USER confirmation that sufficient video-generation quota is available.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

THRESHOLD_SEC = 15.0

def load(path):
    text=Path(path).read_text(encoding='utf-8')
    return json.loads(text) if Path(path).suffix.lower()=='.json' else yaml.safe_load(text)

def lint(plan):
    issues=[]
    try:
        duration=float(plan.get('duration_sec'))
    except Exception:
        return {'pass':False,'gate':'LONG_VIDEO_QUOTA_CONFIRMATION_PASS','issues':[{'type':'INVALID_DIRECTOR_DURATION'}]}
    q=plan.get('long_video_quota_confirmation') or {}
    if duration <= THRESHOLD_SEC:
        return {'pass':True,'gate':'LONG_VIDEO_QUOTA_CONFIRMATION_PASS','required':False,'duration_sec':duration,'threshold_sec':THRESHOLD_SEC,'issues':[]}
    if q.get('threshold_sec') != THRESHOLD_SEC:
        issues.append({'type':'LONG_VIDEO_QUOTA_CONFIRMATION_REQUIRED','duration_sec':duration,'threshold_sec':THRESHOLD_SEC,'reason':'threshold_or_record_missing'})
    if q.get('question_asked') is not True:
        issues.append({'type':'LONG_VIDEO_QUOTA_QUESTION_NOT_ASKED','duration_sec':duration,'threshold_sec':THRESHOLD_SEC})
    response=q.get('user_response')
    if response == 'NO_QUOTA':
        issues.append({'type':'LONG_VIDEO_QUOTA_NOT_AVAILABLE','duration_sec':duration})
    elif response != 'HAS_QUOTA':
        issues.append({'type':'LONG_VIDEO_QUOTA_CONFIRMATION_REQUIRED','duration_sec':duration,'threshold_sec':THRESHOLD_SEC,'reason':'user_confirmation_pending'})
    if response == 'HAS_QUOTA':
        if q.get('confirmed_by')!='USER':
            issues.append({'type':'LONG_VIDEO_QUOTA_CONFIRMATION_NOT_USER_AUTHORED'})
        if not q.get('confirmation_ref'):
            issues.append({'type':'LONG_VIDEO_QUOTA_CONFIRMATION_REF_MISSING'})
    return {'pass':not issues,'gate':'LONG_VIDEO_QUOTA_CONFIRMATION_PASS','required':True,'duration_sec':duration,'threshold_sec':THRESHOLD_SEC,'issues':issues}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--execution-plan',required=True); a=ap.parse_args()
    out=lint(load(a.execution_plan)); print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
