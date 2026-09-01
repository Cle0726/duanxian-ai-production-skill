#!/usr/bin/env python3
"""Hard QC for whether the actual Video Take executed protected pressure beats and active creature behavior."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

PASS='PASS'; NA='NOT_APPLICABLE'
INSPECTORS={'MULTIMODAL_MODEL','HUMAN','MIXED'}

def load(p):
    text=Path(p).read_text(encoding='utf-8')
    try: return json.loads(text)
    except Exception: return yaml.safe_load(text)

def add(issues,t,**kw): issues.append({'type':t,**kw})

def video_scope(video):
    s=(video or {}).get('scope') or {}
    scene=s.get('scene_id')
    shots=set(s.get('shot_ids') or [])
    if s.get('shot_id'): shots.add(s.get('shot_id'))
    return scene,shots

def relevant_beats(experience, scene, shots):
    if experience.get('genre_pressure_applicable') is not True or experience.get('status')=='NOT_REQUIRED': return []
    if scene and experience.get('scene_id') not in {None,scene}: return []
    beats=experience.get('pressure_beats') or []
    if shots:
        return [b for b in beats if shots.intersection(b.get('shot_ids') or [])]
    # Scene-scoped Video Runtime may omit shot ids; in that case all scene beats remain in scope.
    return list(beats) if scene and experience.get('scene_id')==scene else []

def active_creatures(creature, beat_ids):
    if not creature or creature.get('active_threat_present') is not True or creature.get('status')=='NOT_REQUIRED': return []
    out=[]
    for c in creature.get('creatures') or []:
        if c.get('threat_status')!='ACTIVE_THREAT': continue
        if beat_ids.intersection(c.get('threat_coverage_beat_ids') or []): out.append(c)
    return out

def lint(experience, creature, video, qc):
    issues=[]
    fp=(video or {}).get('video_take_fingerprint')
    scene,shots=video_scope(video)
    beats=relevant_beats(experience,scene,shots)
    protected=[b for b in beats if b.get('protected_from_cost_compression') is True]
    beat_ids={b.get('beat_id') for b in beats if b.get('beat_id')}
    creatures=active_creatures(creature,beat_ids)
    exp_applicable=bool(beats)
    creature_applicable=bool(creatures)

    if not exp_applicable:
        if (qc or {}).get('experience_execution_readiness') not in {NA,PASS,None}:
            add(issues,'VIDEO_EXPERIENCE_NOT_APPLICABLE_READINESS_CONFLICT',readiness=(qc or {}).get('experience_execution_readiness'))
        if not creature_applicable and (qc or {}).get('creature_performance_readiness') not in {NA,PASS,None}:
            add(issues,'VIDEO_CREATURE_NOT_APPLICABLE_READINESS_CONFLICT',readiness=(qc or {}).get('creature_performance_readiness'))
        return {'pass':not issues,'experience_gate':'VIDEO_EXPERIENCE_EXECUTION_QC_PASS','creature_gate':'VIDEO_CREATURE_PERFORMANCE_QC_PASS','experience_gate_pass':not issues,'creature_gate_pass':not issues,'experience_applicable':False,'creature_applicable':False,'issues':issues}

    if not fp: add(issues,'VIDEO_EXPERIENCE_TAKE_FINGERPRINT_MISSING')
    if not scene and not shots: add(issues,'VIDEO_EXPERIENCE_SCOPE_MISSING')
    ev=(qc or {}).get('video_experience_evidence') or {}
    if ev.get('evidence_status')!='CURRENT': add(issues,'VIDEO_EXPERIENCE_EVIDENCE_NOT_CURRENT',evidence_status=ev.get('evidence_status'))
    if fp and ev.get('video_take_fingerprint')!=fp: add(issues,'VIDEO_EXPERIENCE_EVIDENCE_STALE',expected_fingerprint=fp,evidence_fingerprint=ev.get('video_take_fingerprint'))
    if ev.get('inspector_mode') not in INSPECTORS: add(issues,'VIDEO_EXPERIENCE_INSPECTOR_INVALID',inspector_mode=ev.get('inspector_mode'))

    pv={x.get('beat_id'):x for x in ev.get('protected_beat_verdicts') or [] if isinstance(x,dict) and x.get('beat_id')}
    for b in protected:
        bid=b.get('beat_id'); row=pv.get(bid)
        if not row:
            add(issues,'VIDEO_PROTECTED_EXPERIENCE_BEAT_UNPROVEN',beat_id=bid); continue
        for field,code in [('execution_verdict','VIDEO_PROTECTED_EXPERIENCE_BEAT_EXECUTION_FAIL'),('landing_verdict','VIDEO_EXPERIENCE_LANDING_UNPROVEN'),('pressure_state_change_verdict','VIDEO_EXPERIENCE_STATE_CHANGE_UNPROVEN')]:
            if row.get(field)!=PASS: add(issues,code,beat_id=bid,observed=row.get(field))

    cv={x.get('creature_id'):x for x in ev.get('creature_verdicts') or [] if isinstance(x,dict) and x.get('creature_id')}
    role_by_beat={b.get('beat_id'):b.get('role') for b in beats}
    for c in creatures:
        cid=c.get('creature_id'); row=cv.get(cid)
        if not row:
            add(issues,'VIDEO_CREATURE_PERFORMANCE_UNPROVEN',creature_id=cid); continue
        required_beat_ids=beat_ids.intersection(c.get('threat_coverage_beat_ids') or [])
        observed=set(row.get('beat_ids_observed') or [])
        if required_beat_ids-observed:
            add(issues,'VIDEO_CREATURE_BEAT_COVERAGE_GAP',creature_id=cid,beat_ids=sorted(required_beat_ids-observed))
        for field,code in [
          ('perception_tracking','VIDEO_CREATURE_PERCEPTION_TRACKING_FAIL'),
          ('locomotion_body_coordination','VIDEO_CREATURE_LOCOMOTION_BODY_FAIL'),
          ('weight_environment_coupling','VIDEO_CREATURE_WEIGHT_ENVIRONMENT_FAIL'),
          ('approach_pause_behavior','VIDEO_CREATURE_APPROACH_PAUSE_FAIL')]:
            if row.get(field)!=PASS: add(issues,code,creature_id=cid,observed=row.get(field))
        needs_commit=any(role_by_beat.get(bid) in {'COMMITMENT','PAYOFF'} for bid in required_beat_ids)
        if needs_commit and row.get('attack_preparation_commitment')!=PASS:
            add(issues,'VIDEO_CREATURE_ATTACK_COMMITMENT_FAIL',creature_id=cid,observed=row.get('attack_preparation_commitment'))
        if (c.get('stillness') or {}).get('mode')=='PREDATORY_STILLNESS' and row.get('predatory_stillness_function')!=PASS:
            add(issues,'VIDEO_CREATURE_PREDATORY_STILLNESS_FAIL',creature_id=cid,observed=row.get('predatory_stillness_function'))
        if row.get('overall_verdict')!=PASS: add(issues,'VIDEO_CREATURE_OVERALL_NOT_PASS',creature_id=cid,observed=row.get('overall_verdict'))

    if ev.get('overall_verdict')!=PASS: add(issues,'VIDEO_EXPERIENCE_OVERALL_NOT_PASS',observed=ev.get('overall_verdict'))
    if ev.get('issue_codes'): add(issues,'VIDEO_EXPERIENCE_OPEN_ISSUES',issue_codes=ev.get('issue_codes'))
    if (qc or {}).get('experience_execution_readiness')!=PASS: add(issues,'VIDEO_EXPERIENCE_QC_RUNTIME_NOT_PASS',readiness=(qc or {}).get('experience_execution_readiness'))
    if creature_applicable and (qc or {}).get('creature_performance_readiness')!=PASS: add(issues,'VIDEO_CREATURE_QC_RUNTIME_NOT_PASS',readiness=(qc or {}).get('creature_performance_readiness'))
    if not creature_applicable and (qc or {}).get('creature_performance_readiness') not in {NA,PASS,None}: add(issues,'VIDEO_CREATURE_NOT_APPLICABLE_READINESS_CONFLICT',readiness=(qc or {}).get('creature_performance_readiness'))

    creature_issue_prefixes=('VIDEO_CREATURE_',)
    exp_issues=[i for i in issues if not i['type'].startswith(creature_issue_prefixes)]
    creature_issues=[i for i in issues if i['type'].startswith(creature_issue_prefixes)]
    return {
      'pass':not issues,
      'experience_gate':'VIDEO_EXPERIENCE_EXECUTION_QC_PASS',
      'creature_gate':'VIDEO_CREATURE_PERFORMANCE_QC_PASS',
      'experience_gate_pass':not exp_issues,
      'creature_gate_pass':not creature_issues,
      'experience_applicable':True,
      'creature_applicable':creature_applicable,
      'protected_beat_ids':[b.get('beat_id') for b in protected],
      'active_creature_ids':[c.get('creature_id') for c in creatures],
      'issues':issues,
    }

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--experience-plan',required=True); ap.add_argument('--creature-plan',required=True); ap.add_argument('--video-runtime',required=True); ap.add_argument('--qc-runtime',required=True); a=ap.parse_args()
    out=lint(load(a.experience_plan),load(a.creature_plan),load(a.video_runtime),load(a.qc_runtime)); print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
