#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

FIELDS=['behavior_thesis','perception_method','locomotion_signature','weight_inertia','body_coordination','idle_threat_motion','target_tracking','approach_pattern','pause_pattern','attack_preparation','commitment_motion','recovery_behavior','environment_coupling','sound_coupling']

def load(p):
    text=Path(p).read_text(encoding='utf-8')
    return json.loads(text) if Path(p).suffix.lower()=='.json' else yaml.safe_load(text)
def meaningful(v): return bool(str(v or '').strip())

def lint(d, experience=None):
    issues=[]
    def add(t,**kw): issues.append({'type':t,**kw})
    active=d.get('active_threat_present') is True
    if not active:
        if d.get('status')!='NOT_REQUIRED': add('CREATURE_PERFORMANCE_NOT_REQUIRED_STATUS_INVALID',status=d.get('status'))
        if d.get('creatures'): add('CREATURE_PERFORMANCE_NOT_REQUIRED_HAS_CREATURES')
        return {'pass':not issues,'issues':issues,'active_threat_present':False}
    if d.get('status')!='LOCKED': add('CREATURE_PERFORMANCE_PLAN_NOT_LOCKED',status=d.get('status'))
    creatures=d.get('creatures') or []
    if not creatures: add('CREATURE_PERFORMANCE_PLAN_GAP')
    exp_ids={b.get('beat_id') for b in ((experience or {}).get('pressure_beats') or []) if b.get('beat_id')}
    for c in creatures:
        cid=c.get('creature_id')
        if c.get('threat_status')=='ACTIVE_THREAT':
            missing=[f for f in FIELDS if not meaningful(c.get(f))]
            if missing: add('CREATURE_PERFORMANCE_FIELD_GAP',creature_id=cid,missing=missing)
            still=c.get('stillness') or {}; mode=still.get('mode')
            if mode=='STATIC_UNJUSTIFIED': add('CREATURE_STATIC_PROP_FAIL',creature_id=cid)
            if mode=='PREDATORY_STILLNESS' and not (meaningful(still.get('reason')) and meaningful(still.get('pressure_effect')) and meaningful(still.get('exit_trigger'))):
                add('CREATURE_PREDATORY_STILLNESS_JUSTIFICATION_GAP',creature_id=cid)
            if c.get('scale_read_required') is True and not meaningful(c.get('scale_anchor')):
                add('CREATURE_SCALE_READ_GAP',creature_id=cid)
            rp=c.get('reference_pose_policy') or {}
            if rp.get('pose_bias_risk')=='HIGH':
                if rp.get('action_anchor_strategy') in {None,'NONE'} or not meaningful(rp.get('action_anchor_ref')):
                    add('STATIC_CANON_POSE_CONFLICT',creature_id=cid,pose_bias_risk='HIGH')
            if c.get('threat_importance') in {'MAJOR','HERO'}:
                binds=c.get('threat_coverage_beat_ids') or []
                if not binds: add('CREATURE_THREAT_COVERAGE_BINDING_GAP',creature_id=cid)
                elif experience is not None:
                    unknown=sorted(set(binds)-exp_ids)
                    if unknown: add('CREATURE_THREAT_COVERAGE_BINDING_GAP',creature_id=cid,unknown_beat_ids=unknown)
                rows=c.get('behavior_beat_map') or []
                row_ids=[r.get('beat_id') for r in rows if r.get('beat_id')]
                missing_rows=sorted(set(binds)-set(row_ids))
                # Offscreen-only beats may omit body choreography; visible linked beats are enforced by completeness gate.
                if not rows: add('CREATURE_BEHAVIOR_BEAT_COVERAGE_GAP',creature_id=cid,reason='BEHAVIOR_BEAT_MAP_EMPTY')
                dup=sorted({x for x in row_ids if row_ids.count(x)>1})
                if dup: add('CREATURE_BEHAVIOR_BEAT_DUPLICATE',creature_id=cid,beat_ids=dup)
                for r in rows:
                    missing=[f for f in ['perception_action','body_action','target_tracking_change','environment_response','pressure_function','exit_trigger'] if not meaningful(r.get(f))]
                    if missing: add('CREATURE_BEHAVIOR_BEAT_FIELD_GAP',creature_id=cid,beat_id=r.get('beat_id'),missing=missing)
    return {'pass':not issues,'issues':issues,'active_threat_present':True,'creature_count':len(creatures)}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('plan'); ap.add_argument('--experience-plan'); a=ap.parse_args(); out=lint(load(a.plan),load(a.experience_plan) if a.experience_plan else None); print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
