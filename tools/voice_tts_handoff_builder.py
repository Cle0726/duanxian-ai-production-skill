#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
import yaml

def load(p):
    text=Path(p).read_text(encoding='utf-8'); return json.loads(text) if Path(p).suffix.lower()=='.json' else yaml.safe_load(text)
def fp(d): return hashlib.sha256(yaml.safe_dump(d,sort_keys=True,allow_unicode=True).encode('utf-8')).hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--plan',required=True); ap.add_argument('--timings',required=True); ap.add_argument('--picture-lock-ref',required=True); ap.add_argument('--picture-lock-fingerprint',required=True); ap.add_argument('--output',required=True); ap.add_argument('--handoff-id',default='VOICE_TTS_HANDOFF_AUTO'); ap.add_argument('--adapter-mode',choices=['DIRECT_TTS_CONTROL','SSML_WHEN_SUPPORTED','DIRECTOR_NOTE_ONLY'],default='SSML_WHEN_SUPPORTED'); a=ap.parse_args()
    plan=load(a.plan); t=load(a.timings); timing_lines=t.get('lines') or []; tids=[x.get('line_id') for x in timing_lines]
    if len(tids)!=len(set(tids)): raise SystemExit('VOICE_TTS_TIMING_DUPLICATE_LINE_ID')
    tm={x['line_id']:x for x in timing_lines}
    out_lines=[]
    for x in plan.get('lines') or []:
        ti=tm.get(x['line_id'])
        if not ti: raise SystemExit(f'VOICE_TTS_TIMING_MISSING:{x["line_id"]}')
        d=x['delivery']; out_lines.append({'line_id':x['line_id'],'speaker_entity_id':x['speaker_entity_id'],'final_spoken_text':x['spoken_text'],'start_sec':ti['start_sec'],'end_sec':ti['end_sec'],'voice_identity_asset_id':x.get('voice_identity_asset_id'),'performance_loudness':d['performance_loudness'],'pace_control':{'entry':d['pace_curve']['entry'],'mid':d['pace_curve']['mid'],'terminal':d['pace_curve']['terminal']},'pauses':[dict(p, duration_sec=None) for p in (d.get('pause_map') or [])],'stress_map':d.get('stress_map') or [],'pitch_energy_contour':d['pitch_energy_contour'],'terminal_intonation':d['terminal_intonation'],'texture_adjustments':[z['adjustment'] for z in (d.get('texture_adjustments') or [])],'tts_adapter_mode':a.adapter_mode,'preserved_intent':True,'override_reason':None})
    out={'schema_version':1,'skill_version':'4.5.11','voice_tts_handoff_id':a.handoff_id,'voice_direction_plan_id':plan['voice_direction_plan_id'],'episode_id':plan['episode_id'],'dialogue_required':bool(out_lines) if plan.get('dialogue_required') else False,'picture_lock_ref':a.picture_lock_ref,'picture_lock_fingerprint':a.picture_lock_fingerprint,'lines':out_lines,'status':'READY_FOR_TTS' if out_lines else 'NOT_REQUIRED'}
    out['handoff_fingerprint']=fp(out); Path(a.output).write_text(yaml.safe_dump(out,sort_keys=False,allow_unicode=True),encoding='utf-8'); print(json.dumps({'pass':True,'line_count':len(out_lines),'handoff_fingerprint':out['handoff_fingerprint']},ensure_ascii=False,indent=2))
if __name__=='__main__': main()
