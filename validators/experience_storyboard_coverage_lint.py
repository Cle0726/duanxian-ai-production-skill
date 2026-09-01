#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

def load(p):
    text=Path(p).read_text(encoding='utf-8')
    return json.loads(text) if Path(p).suffix.lower()=='.json' else yaml.safe_load(text)

def lint(plan, shot_states):
    issues=[]
    if plan.get('status')=='NOT_REQUIRED' and plan.get('genre_pressure_applicable') is not True:
        return {'pass':True,'issues':[],'required_shots':[]}
    by={s.get('shot_id'):s for s in shot_states if s.get('shot_id')}
    required=[]; panel_to_beats={}
    by_beat={b.get('beat_id'):b for b in (plan.get('pressure_beats') or []) if b.get('beat_id')}
    for b in plan.get('pressure_beats') or []:
        if b.get('protected_from_cost_compression') is not True: continue
        for sid in b.get('shot_ids') or []:
            required.append(sid); st=by.get(sid)
            if not st:
                issues.append({'type':'EXPERIENCE_STORYBOARD_COVERAGE_GAP','beat_id':b.get('beat_id'),'shot_id':sid,'reason':'SHOT_STATE_MISSING'}); continue
            sb=st.get('storyboard') or {}
            panels=sb.get('mandatory_panel_asset_ids') or []
            if sb.get('mandatory_coverage_planned') is not True or not panels:
                issues.append({'type':'EXPERIENCE_STORYBOARD_COVERAGE_GAP','beat_id':b.get('beat_id'),'shot_id':sid,'reason':'MANDATORY_PANEL_NOT_PLANNED'})
            for panel in panels:
                panel_to_beats.setdefault(panel,[]).append(b.get('beat_id'))
    for panel,bids in panel_to_beats.items():
        ub=sorted(set(x for x in bids if x))
        if len(ub)<=1: continue
        justified=True
        for bid in ub:
            comp=(by_beat.get(bid,{}).get('compression') or {})
            if comp.get('action')!='MERGE' or not (set(ub)-{bid}).issubset(set(comp.get('target_beat_ids') or [])) or not str(comp.get('experience_equivalence_evidence') or '').strip():
                justified=False; break
        if not justified:
            issues.append({'type':'EXPERIENCE_STORYBOARD_PANEL_COLLAPSE','panel_asset_id':panel,'beat_ids':ub})
    return {'pass':not issues,'issues':issues,'required_shots':sorted(set(required))}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--experience-plan',required=True); ap.add_argument('--shot-state',action='append',default=[]); a=ap.parse_args(); out=lint(load(a.experience_plan),[load(x) for x in a.shot_state]); print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
