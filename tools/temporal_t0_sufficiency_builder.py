#!/usr/bin/env python3
import argparse, json, pathlib, yaml, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'validators'))
from temporal_integrity import load, fingerprint
from temporal_entry_plan_lint import lint as lint_plan
from temporal_t0_sufficiency_lint import lint

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--entry-plan',required=True); ap.add_argument('--request',required=True); ap.add_argument('--output',required=True); ap.add_argument('--assessment-id',required=True); a=ap.parse_args()
    p=load(a.entry_plan); pr=lint_plan(p,a.entry_plan)
    if not pr['pass']: print(json.dumps({'pass':False,'error':'TEMPORAL_ENTRY_PLAN_INVALID','issues':pr['issues']},ensure_ascii=False,indent=2)); return 2
    r=load(a.request) or {}; same=p.get('entry_mode') in {'SEAMLESS_EXTEND','GUIDED_CONTINUATION'}; entities=[]
    for e in r.get('entities') or []:
        verdict=str(e.get('verdict') or 'INSUFFICIENT').upper() if same else 'NOT_APPLICABLE'
        if verdict not in {'SUFFICIENT','INSUFFICIENT','NOT_APPLICABLE'}: verdict='INSUFFICIENT'
        entities.append({'slot_id':e.get('slot_id'),'entity_id':e.get('entity_id'),'verdict':verdict,'evidence_ref':e.get('evidence_ref'),'reason':e.get('reason')})
    overall='NOT_APPLICABLE' if not same else ('RESET_REQUIRED' if any(e['verdict']!='SUFFICIENT' for e in entities) else 'SUFFICIENT')
    d={'schema_version':1,'skill_version':'4.5.11','assessment_id':a.assessment_id,'video_unit_id':p.get('video_unit_id'),'temporal_entry_plan_ref':str(pathlib.Path(a.entry_plan).resolve()),'temporal_entry_plan_fingerprint':p.get('temporal_entry_plan_fingerprint'),'continuity_snapshot_ref':p.get('continuity_snapshot_ref'),'continuity_snapshot_fingerprint':p.get('continuity_snapshot_fingerprint'),'overall_verdict':overall,'entities':entities}
    d['assessment_fingerprint']=fingerprint(d,'assessment_fingerprint'); pathlib.Path(a.output).write_text(yaml.safe_dump(d,sort_keys=False,allow_unicode=True),encoding='utf-8')
    o=lint(d,a.output)
    if not o['pass']: print(json.dumps({'pass':False,'error':'TEMPORAL_T0_SUFFICIENCY_LINT_FAIL','issues':o['issues']},ensure_ascii=False,indent=2)); return 2
    print(json.dumps({'pass':True,'assessment_ref':str(pathlib.Path(a.output).resolve()),'assessment_fingerprint':d['assessment_fingerprint'],'overall_verdict':overall},ensure_ascii=False,indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
