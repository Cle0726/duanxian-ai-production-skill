#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,re,hashlib
from pathlib import Path
import yaml
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.voice_direction_prompt_compiler import compile_line

def load(p):
    text=Path(p).read_text(encoding='utf-8'); return json.loads(text) if Path(p).suffix.lower()=='.json' else yaml.safe_load(text)
def norm(s):
    s=str(s or '').replace('“','').replace('”','').replace('‘','').replace('’','').replace('：',':').replace('；',';').replace('，',',').replace('。','')
    return re.sub(r'\s+','',s).lower()
def add(issues,t,**kw): d={'type':t}; d.update(kw); issues.append(d)

def lint(plan,handoff,prompt,execution_plan=None):
    issues=[]
    _h=dict(handoff); _actual=_h.pop('handoff_fingerprint',None); _expected=hashlib.sha256(yaml.safe_dump(_h,sort_keys=True,allow_unicode=True).encode('utf-8')).hexdigest()
    if not _actual or _actual!=_expected: add(issues,'VOICE_PROMPT_HANDOFF_FINGERPRINT_INVALID',expected=_expected,actual=_actual)
    if handoff.get('voice_direction_plan_id')!=plan.get('voice_direction_plan_id'): add(issues,'VOICE_PROMPT_PLAN_ID_MISMATCH')
    if execution_plan and handoff.get('video_unit_id')!=execution_plan.get('video_unit_id'): add(issues,'VOICE_PROMPT_VIDEO_UNIT_MISMATCH',expected=execution_plan.get('video_unit_id'),actual=handoff.get('video_unit_id'))
    hlines=handoff.get('lines') or []
    hids=[x.get('line_id') for x in hlines]
    if len(hids)!=len(set(hids)): add(issues,'VOICE_PROMPT_DUPLICATE_LINE_ID')
    if plan.get('dialogue_required') is False:
        if handoff.get('dialogue_required') is not False: add(issues,'VOICE_PROMPT_UNEXPECTED_DIALOGUE_HANDOFF',reason='dialogue_required flag must be false')
        if handoff.get('status')!='NOT_REQUIRED': add(issues,'VOICE_PROMPT_UNEXPECTED_DIALOGUE_HANDOFF',reason='status must be NOT_REQUIRED',status=handoff.get('status'))
        if hlines: add(issues,'VOICE_PROMPT_UNEXPECTED_DIALOGUE_HANDOFF',reason='NOT_REQUIRED handoff must have zero lines',line_count=len(hlines))
        return {'pass':not issues,'dialogue_required':False,'issues':issues}
    current_shots=set(handoff.get('shot_ids') or [])
    current_vu=handoff.get('video_unit_id')
    expected_current=[]
    for x in plan.get('lines') or []:
        if x.get('video_unit_id'):
            if x.get('video_unit_id')==current_vu: expected_current.append(x)
        elif current_shots:
            if x.get('shot_id') in current_shots: expected_current.append(x)
        else:
            expected_current.append(x)
    expected_ids=[x.get('line_id') for x in expected_current]
    expected_required=bool(expected_current)
    if handoff.get('dialogue_required') != expected_required:
        add(issues,'VOICE_PROMPT_DIALOGUE_REQUIRED_MISMATCH',expected=expected_required,actual=handoff.get('dialogue_required'),expected_line_ids=expected_ids)
    if not expected_required:
        if handoff.get('status')!='NOT_REQUIRED' or hlines:
            add(issues,'VOICE_PROMPT_NOT_REQUIRED_STATE_CONFLICT',status=handoff.get('status'),line_count=len(hlines))
        return {'pass':not issues,'dialogue_required':False,'issues':issues}
    if handoff.get('status')!='READY': add(issues,'VOICE_PROMPT_HANDOFF_NOT_READY',status=handoff.get('status'))
    missing=sorted(set(expected_ids)-set(hids)); extra=sorted(set(hids)-set(expected_ids))
    if missing: add(issues,'VOICE_PROMPT_LINE_COVERAGE_GAP',line_ids=missing)
    if extra: add(issues,'VOICE_PROMPT_UNEXPECTED_LINE',line_ids=extra)
    hp=norm(prompt)
    plan_by={x.get('line_id'):x for x in plan.get('lines') or []}
    for h in hlines:
        lid=h.get('line_id'); p=plan_by.get(lid)
        if not p: add(issues,'VOICE_PROMPT_UNKNOWN_LINE_ID',line_id=lid); continue
        if p.get('video_unit_id') and p.get('video_unit_id')!=current_vu:
            add(issues,'VOICE_PROMPT_LINE_OUT_OF_VIDEO_UNIT',line_id=lid,video_unit_id=p.get('video_unit_id'))
        elif current_shots and not p.get('video_unit_id') and p.get('shot_id') not in current_shots:
            add(issues,'VOICE_PROMPT_LINE_OUT_OF_VIDEO_UNIT',line_id=lid,shot_id=p.get('shot_id'))
        if h.get('speaker_entity_id')!=p.get('speaker_entity_id') or h.get('spoken_text')!=p.get('spoken_text') or h.get('shot_id')!=p.get('shot_id'):
            add(issues,'VOICE_PROMPT_LINE_IDENTITY_MISMATCH',line_id=lid)
        expected_compiled,expected_terms=compile_line(p)
        if h.get('compiled_direction')!=expected_compiled or (h.get('required_surface_terms') or [])!=expected_terms:
            add(issues,'VOICE_PROMPT_HANDOFF_COMPILER_DRIFT',line_id=lid)
        if norm(p.get('spoken_text')) not in hp: add(issues,'VOICE_PROMPT_DIALOGUE_TEXT_MISSING',line_id=lid)
        if norm(h.get('speaker_surface')) not in hp: add(issues,'VOICE_PROMPT_SPEAKER_ANCHOR_MISSING',line_id=lid,speaker=h.get('speaker_surface'))
        terms=expected_terms
        missing_terms=[t for t in terms if norm(t) not in hp]
        if missing_terms:
            termcat=(p.get('delivery') or {}).get('terminal_intonation')
            terminal_surface=terms[terms.index(next(t for t in terms if t in {'句尾明确落下','句尾真正上扬','句尾先落后回升并保留含义','句尾保持悬而未决','句尾突然收断','句尾随气息释放','句尾故意不完成落点'}))] if any(t in {'句尾明确落下','句尾真正上扬','句尾先落后回升并保留含义','句尾保持悬而未决','句尾突然收断','句尾随气息释放','句尾故意不完成落点'} for t in terms) else None
            if terminal_surface and terminal_surface in missing_terms: add(issues,'VOICE_PROMPT_TERMINAL_ANCHOR_MISSING',line_id=lid,terminal=termcat)
            add(issues,'VOICE_PROMPT_DELIVERY_ANCHOR_MISSING',line_id=lid,missing=missing_terms)
        if p.get('importance') in {'IMPORTANT','CRITICAL'} and len(terms)<4:
            add(issues,'VOICE_PROSODY_UNDERDIRECTED',line_id=lid,reason='handoff has too few executable surface terms')
    return {'pass':not issues,'dialogue_required':True,'line_count':len(hlines),'issues':issues}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--plan',required=True); ap.add_argument('--handoff',required=True); ap.add_argument('--prompt',required=True); ap.add_argument('--execution-plan'); a=ap.parse_args()
    out=lint(load(a.plan),load(a.handoff),Path(a.prompt).read_text(encoding='utf-8'),load(a.execution_plan) if a.execution_plan else None); print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
