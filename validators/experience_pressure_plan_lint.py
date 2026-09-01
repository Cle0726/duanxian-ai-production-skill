#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

PRE_REVEAL={'OMEN','OFFSCREEN_THREAT','TRACE','NEGATIVE_SPACE_HOLD','PARTIAL_REVEAL','FALSE_CLEAR','REACTION_WITHHOLD','SCALE_REVEAL','ENCROACHMENT','ESCAPE_DENIAL'}

def load(p):
    text=Path(p).read_text(encoding='utf-8')
    return json.loads(text) if Path(p).suffix.lower()=='.json' else yaml.safe_load(text)

def meaningful(v): return bool(str(v or '').strip())

def lint(d):
    issues=[]
    def add(t,**kw): issues.append({'type':t,**kw})
    status=d.get('status'); applicable=d.get('genre_pressure_applicable') is True
    policy=d.get('episode_runtime_policy') or {}
    profile=d.get('production_priority_profile')
    if profile!='QUALITY_FIRST' and not meaningful(d.get('user_priority_override_ref')):
        add('QUALITY_FIRST_PROFILE_MISSING',actual=profile)
    if policy.get('mode')=='PREFERRED_AROUND_20':
        if policy.get('hard_cap_minutes') is not None: add('EXPERIENCE_RUNTIME_HARD_CAP_FORBIDDEN',hard_cap_minutes=policy.get('hard_cap_minutes'))
        if policy.get('over_band_policy')!='REVIEW_NOT_COMPRESS': add('EXPERIENCE_RUNTIME_FORCED_COMPRESSION_POLICY',actual=policy.get('over_band_policy'))
        pref=policy.get('preferred_minutes')
        if not isinstance(pref,(int,float)) or not (18 <= float(pref) <= 22): add('EPISODE_RUNTIME_PREFERENCE_INVALID',preferred_minutes=pref)
        band=policy.get('soft_review_band_minutes') or []
        if len(band)!=2 or not (band[0] <= pref <= band[1]): add('EPISODE_RUNTIME_REVIEW_BAND_INVALID',band=band,preferred_minutes=pref)
    if not applicable:
        if status!='NOT_REQUIRED': add('EXPERIENCE_PRESSURE_NOT_REQUIRED_STATUS_INVALID',status=status)
        if d.get('pressure_beats'): add('EXPERIENCE_PRESSURE_NOT_REQUIRED_HAS_BEATS')
        return {'pass':not issues,'issues':issues,'applicable':False}
    if status!='LOCKED': add('THREAT_PRESSURE_PLAN_NOT_LOCKED',status=status)
    if not (d.get('source_story_facts') or []): add('THREAT_PRESSURE_SOURCE_FACT_GAP')
    beats=d.get('pressure_beats') or []
    importance=d.get('threat_importance') or 'MINOR'
    if len(beats)<2: add('THREAT_PRESSURE_PLAN_GAP',reason='TOO_FEW_BEATS',beat_count=len(beats))
    if importance in {'MAJOR','HERO'} and len(beats)<4: add('THREAT_PRESSURE_PLAN_GAP',reason='MAJOR_THREAT_UNDERDEVELOPED',beat_count=len(beats))
    ids=set(); full_idx=None; pre_before=False
    for i,b in enumerate(beats):
        bid=b.get('beat_id')
        if bid in ids: add('THREAT_PRESSURE_DUPLICATE_BEAT_ID',beat_id=bid)
        ids.add(bid)
        if b.get('origin')=='SCREEN_EXPERIENCE_ELABORATION':
            if b.get('canon_delta')!='NONE' or b.get('story_state_delta')!='NONE':
                add('SCREEN_EXPERIENCE_CANON_OVERREACH',beat_id=bid,canon_delta=b.get('canon_delta'),story_state_delta=b.get('story_state_delta'))
        if not (b.get('experience_gain') or []): add('SCREEN_EXPERIENCE_PADDING_FAIL',beat_id=bid)
        if b.get('protected_from_cost_compression') is not True:
            add('QUALITY_FIRST_COST_BACKDRIVE_FAIL',beat_id=bid,reason='PROTECTED_BEAT_NOT_LOCKED')
        if not (b.get('shot_ids') or []): add('EXPERIENCE_BEAT_SHOT_MAPPING_GAP',beat_id=bid)
        role=b.get('role')
        if role in PRE_REVEAL and full_idx is None: pre_before=True
        if role in {'FULL_REVEAL','COMMITMENT'} and full_idx is None: full_idx=i
    if importance in {'MAJOR','HERO'} and full_idx is not None and not pre_before and not meaningful(d.get('immediate_reveal_justification')):
        add('THREAT_REVEAL_TOO_IMMEDIATE',importance=importance,first_full_reveal_index=full_idx)
    cp=d.get('cost_policy') or {}
    if cp.get('content_budget_separate_from_take_budget') is not True or cp.get('protected_beats_may_be_removed_for_cost') is not False or cp.get('extra_segments_allowed_for_experience') is not True:
        add('QUALITY_FIRST_COST_BACKDRIVE_FAIL',reason='COST_POLICY_NOT_QUALITY_FIRST',cost_policy=cp)
    return {'pass':not issues,'issues':issues,'applicable':True,'beat_count':len(beats),'threat_importance':importance}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('plan'); a=ap.parse_args(); out=lint(load(a.plan)); print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
