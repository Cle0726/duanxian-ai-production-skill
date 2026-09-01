#!/usr/bin/env python3
import argparse, json
from temporal_integrity import load, fingerprint, resolve_ref, validate_snapshot_path
from temporal_entry_plan_lint import lint as lint_plan

def lint(d,path=None):
    issues=[]; pref=d.get('temporal_entry_plan_ref')
    if not pref: issues.append({'type':'TEMPORAL_T0_ENTRY_PLAN_REQUIRED'})
    elif path:
        try:
            pp=resolve_ref(path,pref); p=load(pp); r=lint_plan(p,pp); issues.extend(r['issues'])
            if d.get('temporal_entry_plan_fingerprint')!=p.get('temporal_entry_plan_fingerprint'): issues.append({'type':'TEMPORAL_T0_ENTRY_PLAN_FINGERPRINT_MISMATCH'})
            same=p.get('entry_mode') in {'SEAMLESS_EXTEND','GUIDED_CONTINUATION'}
            if same:
                if d.get('overall_verdict') not in {'SUFFICIENT','RESET_REQUIRED'}: issues.append({'type':'TEMPORAL_T0_VERDICT_INVALID_FOR_SAME_TAKE'})
                if d.get('continuity_snapshot_fingerprint')!=p.get('continuity_snapshot_fingerprint'): issues.append({'type':'TEMPORAL_T0_SNAPSHOT_FINGERPRINT_MISMATCH'})
                sr=d.get('continuity_snapshot_ref')
                if not sr: issues.append({'type':'TEMPORAL_T0_SNAPSHOT_REQUIRED'})
                else:
                    vr=validate_snapshot_path(resolve_ref(path,sr)); issues.extend(vr['issues'])
                    if vr.get('snapshot') and d.get('continuity_snapshot_fingerprint')!=vr['snapshot'].get('snapshot_fingerprint'): issues.append({'type':'TEMPORAL_T0_SNAPSHOT_FINGERPRINT_MISMATCH'})
            elif d.get('overall_verdict')!='NOT_APPLICABLE': issues.append({'type':'TEMPORAL_T0_NON_SAME_TAKE_MUST_BE_NOT_APPLICABLE'})
        except Exception as e: issues.append({'type':'TEMPORAL_T0_ENTRY_PLAN_UNREADABLE','detail':str(e)})
    seen=set(); insufficient=False
    for e in d.get('entities') or []:
        sid=e.get('slot_id')
        if sid in seen: issues.append({'type':'TEMPORAL_T0_DUPLICATE_SLOT','slot_id':sid})
        seen.add(sid)
        if e.get('verdict')=='SUFFICIENT' and not e.get('evidence_ref'): issues.append({'type':'TEMPORAL_T0_SUFFICIENT_EVIDENCE_MISSING','slot_id':sid})
        if e.get('verdict')=='INSUFFICIENT': insufficient=True
    if insufficient and d.get('overall_verdict')!='RESET_REQUIRED': issues.append({'type':'TEMPORAL_RESET_REQUIRED'})
    actual=fingerprint(d,'assessment_fingerprint')
    if d.get('assessment_fingerprint')!=actual: issues.append({'type':'TEMPORAL_T0_ASSESSMENT_FINGERPRINT_INVALID','expected':actual,'actual':d.get('assessment_fingerprint')})
    return {'pass':not issues,'issues':issues,'fingerprint':actual}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('assessment'); a=ap.parse_args(); d=load(a.assessment); out=lint(d,a.assessment); print(json.dumps(out,ensure_ascii=False,indent=2)); return 0 if out['pass'] else 2
if __name__=='__main__': raise SystemExit(main())
