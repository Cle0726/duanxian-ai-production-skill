#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,hashlib
from pathlib import Path
import yaml

def load(p):
    text=Path(p).read_text(encoding='utf-8'); return json.loads(text) if Path(p).suffix.lower()=='.json' else yaml.safe_load(text)
def add(issues,t,**kw): d={'type':t}; d.update(kw); issues.append(d)

def lint(plan,handoff):
    issues=[]
    _h=dict(handoff); _actual=_h.pop('handoff_fingerprint',None); _expected=hashlib.sha256(yaml.safe_dump(_h,sort_keys=True,allow_unicode=True).encode('utf-8')).hexdigest()
    if not _actual or _actual!=_expected: add(issues,'VOICE_TTS_HANDOFF_FINGERPRINT_INVALID',expected=_expected,actual=_actual)
    if handoff.get('voice_direction_plan_id')!=plan.get('voice_direction_plan_id'): add(issues,'VOICE_TTS_PLAN_ID_MISMATCH')
    hlines=handoff.get('lines') or []
    hids=[x.get('line_id') for x in hlines]
    if len(hids)!=len(set(hids)): add(issues,'VOICE_TTS_DUPLICATE_LINE_ID')
    if plan.get('dialogue_required') is False:
        if handoff.get('dialogue_required') is not False: add(issues,'VOICE_TTS_DIALOGUE_REQUIRED_MISMATCH',expected=False,actual=handoff.get('dialogue_required'))
        if handoff.get('status')!='NOT_REQUIRED': add(issues,'VOICE_TTS_NOT_REQUIRED_STATUS_FAIL',status=handoff.get('status'))
        if hlines: add(issues,'VOICE_TTS_NOT_REQUIRED_LINES_PRESENT',line_count=len(hlines))
        return {'pass':not issues,'dialogue_required':False,'issues':issues}
    if handoff.get('dialogue_required') is not True: add(issues,'VOICE_TTS_DIALOGUE_REQUIRED_MISMATCH',expected=True,actual=handoff.get('dialogue_required'))
    if handoff.get('status')!='READY_FOR_TTS': add(issues,'VOICE_TTS_HANDOFF_NOT_READY',status=handoff.get('status'))
    if not str(handoff.get('picture_lock_fingerprint') or '').strip(): add(issues,'VOICE_TTS_PICTURE_LOCK_FINGERPRINT_REQUIRED')
    pby={x.get('line_id'):x for x in plan.get('lines') or []}; hby={x.get('line_id'):x for x in hlines}
    required=[x.get('line_id') for x in plan.get('lines') or []]
    miss=sorted(set(required)-set(hids)); extra=sorted(set(hids)-set(required))
    if miss: add(issues,'VOICE_TTS_LINE_COVERAGE_GAP',line_ids=miss)
    if extra: add(issues,'VOICE_TTS_UNKNOWN_LINE_ID',line_ids=extra)
    for lid,h in hby.items():
        p=pby.get(lid)
        if not p: continue
        if h.get('final_spoken_text')!=p.get('spoken_text'): add(issues,'VOICE_TTS_TEXT_DRIFT',line_id=lid)
        if h.get('end_sec',0)<=h.get('start_sec',0): add(issues,'VOICE_TTS_TIMING_INVALID',line_id=lid,start_sec=h.get('start_sec'),end_sec=h.get('end_sec'))
        if h.get('speaker_entity_id')!=p.get('speaker_entity_id'): add(issues,'VOICE_TTS_SPEAKER_MISMATCH',line_id=lid)
        if h.get('voice_identity_asset_id')!=p.get('voice_identity_asset_id'): add(issues,'VOICE_IDENTITY_DRIFT',line_id=lid,expected=p.get('voice_identity_asset_id'),actual=h.get('voice_identity_asset_id'))
        d=p.get('delivery') or {}; pc=d.get('pace_curve') or {}; hc=h.get('pace_control') or {}
        if h.get('performance_loudness')!=d.get('performance_loudness'): add(issues,'VOICE_TTS_INTENT_DRIFT',line_id=lid,field='performance_loudness')
        if h.get('terminal_intonation')!=d.get('terminal_intonation'): add(issues,'VOICE_TTS_INTENT_DRIFT',line_id=lid,field='terminal_intonation')
        if h.get('pitch_energy_contour')!=d.get('pitch_energy_contour'): add(issues,'VOICE_TTS_INTENT_DRIFT',line_id=lid,field='pitch_energy_contour')
        if any(hc.get(k)!=pc.get(k) for k in ('entry','mid','terminal')): add(issues,'VOICE_TTS_INTENT_DRIFT',line_id=lid,field='pace_control')
        p_pause={(z.get('position'),z.get('pause_type')) for z in d.get('pause_map') or []}; h_pause={(z.get('position'),z.get('pause_type')) for z in h.get('pauses') or []}
        if not p_pause.issubset(h_pause): add(issues,'VOICE_TTS_REQUIRED_PAUSE_DROPPED',line_id=lid,missing=sorted(p_pause-h_pause))
        p_stress={(z.get('text_span'),z.get('stress_level')) for z in d.get('stress_map') or []}; h_stress={(z.get('text_span'),z.get('stress_level')) for z in h.get('stress_map') or []}
        if not p_stress.issubset(h_stress): add(issues,'VOICE_TTS_REQUIRED_STRESS_DROPPED',line_id=lid,missing=sorted(p_stress-h_stress))
        p_texture=[z.get('adjustment') for z in d.get('texture_adjustments') or []]
        if (h.get('texture_adjustments') or [])!=p_texture: add(issues,'VOICE_TTS_TEXTURE_DRIFT',line_id=lid,expected=p_texture,actual=h.get('texture_adjustments') or [])
        if h.get('preserved_intent') is not True: add(issues,'VOICE_TTS_INTENT_NOT_PRESERVED',line_id=lid)
    seq=sorted(hlines,key=lambda z:z.get('start_sec',0))
    for a,b in zip(seq,seq[1:]):
        if b.get('start_sec',0)<a.get('end_sec',0):
            pa=pby.get(a.get('line_id')) or {}; pb=pby.get(b.get('line_id')) or {}; modes={(pa.get('interaction') or {}).get('mode'),(pb.get('interaction') or {}).get('mode')}
            if not modes.intersection({'OVERLAP','INTERRUPT'}): add(issues,'VOICE_TTS_UNAUTHORIZED_OVERLAP',line_ids=[a.get('line_id'),b.get('line_id')])
    return {'pass':not issues,'dialogue_required':True,'line_count':len(hlines),'issues':issues}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--plan',required=True); ap.add_argument('--handoff',required=True); a=ap.parse_args(); out=lint(load(a.plan),load(a.handoff)); print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
