#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

IMPORTANT={'IMPORTANT','CRITICAL'}
APPROVED_AUDIO={'APPROVED'}
APPROVED_REGISTRY={'APPROVED','APPROVED_SUPPORT','APPROVED_ASSEMBLY','APPROVED_SCOPED_FIGURE','APPROVED_VIDEO_CONDITIONING'}


def load(p):
    if not p: return None
    text=Path(p).read_text(encoding='utf-8')
    return json.loads(text) if Path(p).suffix.lower()=='.json' else yaml.safe_load(text)

def add(issues,t,**kw):
    d={'type':t}; d.update(kw); issues.append(d)

def lint(plan, phase='planning', audio_manifest=None, registry=None):
    issues=[]
    lines=plan.get('lines') or []
    declared=set((plan.get('coverage') or {}).get('declared_dialogue_line_ids') or [])
    important=set((plan.get('coverage') or {}).get('important_line_ids') or [])
    excluded_entries=((plan.get('coverage') or {}).get('excluded_lines') or [])
    excluded={x.get('line_id') for x in excluded_entries if x.get('line_id')}
    ids=[]
    for x in lines:
        lid=x.get('line_id'); ids.append(lid)
    if len(ids)!=len(set(ids)): add(issues,'VOICE_DIRECTION_DUPLICATE_LINE_ID')
    planned=set(ids)
    if plan.get('dialogue_required') is False:
        if lines: add(issues,'VOICE_DIRECTION_NOT_REQUIRED_BUT_LINES_PRESENT',line_count=len(lines))
        if declared or important: add(issues,'VOICE_DIRECTION_FALSE_NOT_REQUIRED_WITH_DECLARED_DIALOGUE',declared_line_ids=sorted(declared),important_line_ids=sorted(important))
        if plan.get('status')!='NOT_REQUIRED': add(issues,'VOICE_DIRECTION_NOT_REQUIRED_STATUS_FAIL',status=plan.get('status'))
        return {'pass':not issues,'phase':phase,'dialogue_required':False,'line_count':len(lines),'issues':issues}
    if not lines: add(issues,'VOICE_DIRECTION_LINES_MISSING')
    if plan.get('status') not in {'READY_FOR_COMPILE','APPROVED'}: add(issues,'VOICE_DIRECTION_PLAN_NOT_READY',status=plan.get('status'))
    undeclared=sorted(planned-declared)
    if undeclared: add(issues,'VOICE_DIRECTION_UNDECLARED_LINE',line_ids=undeclared)
    excluded_not_declared=sorted(excluded-declared)
    if excluded_not_declared: add(issues,'VOICE_DIRECTION_EXCLUDED_LINE_NOT_DECLARED',line_ids=excluded_not_declared)
    excluded_but_planned=sorted(excluded & planned)
    if excluded_but_planned: add(issues,'VOICE_DIRECTION_EXCLUDED_LINE_PLANNED',line_ids=excluded_but_planned)
    important_not_declared=sorted(important-declared)
    if important_not_declared: add(issues,'VOICE_DIRECTION_IMPORTANT_LINE_NOT_DECLARED',line_ids=important_not_declared)
    important_excluded=sorted(important & excluded)
    if important_excluded: add(issues,'VOICE_DIRECTION_IMPORTANT_LINE_EXCLUDED',line_ids=important_excluded)
    uncovered=sorted((declared-excluded)-planned)
    if uncovered: add(issues,'VOICE_DIRECTION_DIALOGUE_COVERAGE_GAP',line_ids=uncovered)
    missing_important=sorted(important-planned)
    if missing_important: add(issues,'VOICE_DIRECTION_IMPORTANT_LINE_COVERAGE_GAP',line_ids=missing_important)
    declared_importance={x.get('line_id') for x in lines if x.get('importance') in IMPORTANT and x.get('line_id')}
    if declared_importance != important:
        add(issues,'VOICE_DIRECTION_IMPORTANCE_INDEX_MISMATCH',expected=sorted(declared_importance),actual=sorted(important))

    line_by={x.get('line_id'):x for x in lines if x.get('line_id')}
    for x in lines:
        lid=x.get('line_id'); imp=x.get('importance'); ec=x.get('emotional_causality') or {}; d=x.get('delivery') or {}; inter=x.get('interaction') or {}; coupling=x.get('body_voice_coupling') or {}
        line_status=x.get('status')
        allowed_line_status={'APPROVED'} if plan.get('status')=='APPROVED' else {'READY_FOR_COMPILE','APPROVED'}
        if line_status not in allowed_line_status:
            add(issues,'VOICE_DIRECTION_LINE_NOT_READY',line_id=lid,status=line_status,plan_status=plan.get('status'))
        if phase in {'pre_video','stage06'} and not (x.get('shot_id') or x.get('video_unit_id')):
            add(issues,'VOICE_DIRECTION_VIDEO_SCOPE_MISSING',line_id=lid)
        if imp in IMPORTANT:
            for f in ('trigger_event','meaning_appraisal','objective','tactic','subtext','affect_label'):
                if not str(ec.get(f) or '').strip(): add(issues,'VOICE_EMOTIONAL_CAUSALITY_GAP',line_id=lid,field=f)
            pace=d.get('pace_curve') or {}
            if not all(pace.get(k) for k in ('entry','mid','terminal','reason')):
                add(issues,'VOICE_PROSODY_UNDERDIRECTED',line_id=lid,missing='PACE_CURVE')
            if not d.get('terminal_intonation') or not str(d.get('terminal_reason') or '').strip():
                add(issues,'TERMINAL_INTONATION_FAIL',line_id=lid,reason='missing terminal contour or reason')
            executable_extra=bool(d.get('pause_map') or d.get('stress_map') or (d.get('pitch_energy_contour') not in {None,'LEVEL'}) or d.get('texture_adjustments') or inter.get('mode') not in {None,'NONE'})
            if not executable_extra:
                add(issues,'VOICE_PROSODY_UNDERDIRECTED',line_id=lid,missing='PAUSE_OR_STRESS_OR_CONTOUR_OR_INTERACTION')
            if coupling.get('same_trigger_required') is not True or not str(coupling.get('visual_behavior_anchor') or '').strip():
                add(issues,'VOICE_BODY_PERFORMANCE_CAUSALITY_GAP',line_id=lid)
        for p in d.get('pause_map') or []:
            if not str(p.get('reason') or '').strip(): add(issues,'PAUSE_DECORATION_FAIL',line_id=lid,position=p.get('position'))
        for st in d.get('stress_map') or []:
            span=st.get('text_span') or ''
            if span and span not in (x.get('spoken_text') or ''):
                add(issues,'VOICE_STRESS_TEXT_SPAN_NOT_IN_DIALOGUE',line_id=lid,text_span=span)
            if not str(st.get('reason') or '').strip(): add(issues,'VOICE_STRESS_REASON_MISSING',line_id=lid,text_span=span)
        if inter.get('mode') in {'INTERRUPT','OVERLAP','QUICK_PICKUP','LISTENING_DELAY'}:
            tgt=inter.get('target_line_id')
            if not tgt or tgt not in line_by: add(issues,'VOICE_INTERACTION_TARGET_MISSING',line_id=lid,target_line_id=tgt)
            if not str(inter.get('reason') or '').strip(): add(issues,'DIALOGUE_TURN_TAKING_MECHANICAL',line_id=lid)
        if x.get('voice_identity_required') and not x.get('voice_identity_asset_id'):
            add(issues,'VOICE_IDENTITY_ASSET_REQUIRED',line_id=lid,speaker_entity_id=x.get('speaker_entity_id'))

    if phase in {'pre_video','stage06'}:
        aud={a.get('asset_id'):a for a in ((audio_manifest or {}).get('audio_assets') or []) if a.get('asset_id')}
        assets={a.get('asset_id'):a for a in ((registry or {}).get('assets') or []) if a.get('asset_id')}
        if (audio_manifest or {}).get('status') not in {'READY','APPROVED'} and plan.get('dialogue_required'):
            add(issues,'VOICE_AUDIO_MANIFEST_NOT_READY',status=(audio_manifest or {}).get('status'))
        for x in lines:
            if not x.get('voice_identity_required'): continue
            lid=x.get('line_id'); aid=x.get('voice_identity_asset_id'); speaker=x.get('speaker_entity_id'); m=aud.get(aid); a=assets.get(aid)
            if not m: add(issues,'VOICE_IDENTITY_ASSET_NOT_IN_AUDIO_MANIFEST',line_id=lid,asset_id=aid); continue
            if m.get('audio_type')!='VOICE_IDENTITY' or m.get('authority_role')!='VOICE_IDENTITY': add(issues,'VOICE_IDENTITY_ASSET_ROLE_FAIL',line_id=lid,asset_id=aid)
            if m.get('subject_entity_id')!=speaker: add(issues,'VOICE_IDENTITY_SUBJECT_MISMATCH',line_id=lid,asset_id=aid,expected=speaker,actual=m.get('subject_entity_id'))
            if m.get('status') not in APPROVED_AUDIO: add(issues,'VOICE_IDENTITY_ASSET_NOT_APPROVED',line_id=lid,asset_id=aid,status=m.get('status'))
            if not a: add(issues,'VOICE_IDENTITY_REGISTRY_ASSET_MISSING',line_id=lid,asset_id=aid); continue
            if a.get('media_kind')!='AUDIO': add(issues,'VOICE_IDENTITY_REGISTRY_MEDIA_KIND_FAIL',line_id=lid,asset_id=aid,actual=a.get('media_kind'))
            if a.get('status') not in APPROVED_REGISTRY: add(issues,'VOICE_IDENTITY_REGISTRY_NOT_APPROVED',line_id=lid,asset_id=aid,status=a.get('status'))
            if a.get('subject_entity_id') and a.get('subject_entity_id')!=speaker: add(issues,'VOICE_IDENTITY_REGISTRY_SUBJECT_MISMATCH',line_id=lid,asset_id=aid,expected=speaker,actual=a.get('subject_entity_id'))
    return {'pass':not issues,'phase':phase,'dialogue_required':plan.get('dialogue_required'),'line_count':len(lines),'important_line_count':sum(1 for x in lines if x.get('importance') in IMPORTANT),'issues':issues}


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--plan',required=True); ap.add_argument('--phase',choices=['planning','pre_video','stage06'],default='planning'); ap.add_argument('--audio-manifest'); ap.add_argument('--registry'); a=ap.parse_args()
    out=lint(load(a.plan),a.phase,load(a.audio_manifest),load(a.registry)); print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
