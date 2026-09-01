#!/usr/bin/env python3
"""Append approved shot-grammar signatures to DIRECTOR_RUNTIME history.

This tool never invents creative authority. It only projects already-locked
EDITORIAL_PLAN + DIRECTOR_RUNTIME contracts into a compact anti-pattern history.
"""
from __future__ import annotations
import argparse, datetime
from pathlib import Path
import yaml

def load(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))
def save(p,d): Path(p).write_text(yaml.safe_dump(d,allow_unicode=True,sort_keys=False,width=120),encoding='utf-8')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--director-runtime',required=True)
    ap.add_argument('--editorial-plan',required=True)
    ap.add_argument('--output',required=True)
    ap.add_argument('--status',default='STORYBOARD_APPROVED',choices=['STORYBOARD_APPROVED','VIDEO_APPROVED','DIRECTOR_LOCKED'])
    ap.add_argument('--max-history',type=int,default=120)
    ap.add_argument('--replace-existing',action='store_true')
    a=ap.parse_args()
    rt=load(a.director_runtime); ed=load(a.editorial_plan)
    contracts=rt.get('shot_perception_contracts') or {}
    rows={x.get('shot_id'):x for x in (ed.get('shots') or []) if x.get('shot_id')}
    edits=ed.get('edits') or []
    cut_by_from={e.get('from_shot_id'):e.get('transition_type') for e in edits}
    history=list(rt.get('shot_grammar_history') or [])
    existing={x.get('shot_id') for x in history}
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    for sid in ed.get('shot_order') or []:
        if sid in existing and not a.replace_existing: continue
        if sid in existing and a.replace_existing:
            history=[x for x in history if x.get('shot_id')!=sid]
        c=contracts.get(sid) or {}; r=rows.get(sid) or {}; comp=c.get('composition_mechanism') or {}; af=c.get('attention_flow') or {}; scale=c.get('shot_scale_justification') or {}
        history.append({
            'shot_id':sid,'sequence_id':ed.get('sequence_id'),'status':a.status,
            'shot_size_family':scale.get('shot_size_family') or r.get('shot_size_family'),
            'viewpoint_role':r.get('viewpoint_role'),'camera_ethics':c.get('camera_ethics'),
            'composition_mechanism':comp.get('primary'),'camera_character':c.get('camera_character'),
            'lens_family':c.get('lens_family'),'foreground_strategy':c.get('foreground_strategy'),
            'attention_entry_type':af.get('entry'),'attention_landing_type':af.get('decisive_landing'),
            'cut_type':cut_by_from.get(sid),'optical_exception':c.get('optical_exception'),
            'breathing_or_peak':r.get('breathing_function') if r.get('breathing_function') not in {None,'NONE'} else r.get('editorial_weight'),
            'recorded_at':now,
        })
    rt['shot_grammar_history']=history[-max(1,a.max_history):]
    save(a.output,rt)
    print(f"SHOT_GRAMMAR_HISTORY_UPDATED count={len(rt['shot_grammar_history'])}")
if __name__=='__main__': main()
