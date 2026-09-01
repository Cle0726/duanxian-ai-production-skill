#!/usr/bin/env python3
"""Anti-shortcut gate for genre-pressure / threat sequences.

This validator rejects formally complete but experientially underdeveloped plans.
It is intentionally structural: it does not impose a universal shot count or a
universal duration. It verifies that the director's own protected beats,
landing conditions and required experience dimensions survive into editorial
planning without cost-driven deletion/collapse.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
import yaml

COST_WORDS = re.compile(r"(?:cost|quota|token|budget|cheap|save\s*(?:time|money)|省钱|省成本|省额度|节省|便宜|少生成|少一段|压缩时长)", re.I)
HOLD_ROLES = {'NEGATIVE_SPACE_HOLD','REACTION_WITHHOLD','FALSE_CLEAR','FALSE_RELIEF','AFTERMATH'}
HOLD_FUNCTIONS = {'NEGATIVE_SPACE','EMOTIONAL_DELAY','THREAT_PRESSURE','FALSE_RELIEF','PREDATORY_WAIT','AFTERMATH_HOLD','ANTICIPATION'}
ROLE_DIMENSION_HINTS = {
    'OFFSCREEN_THREAT': {'THREAT_PRESENCE','UNCERTAINTY','ANTICIPATION','CHARACTER_PERCEPTION'},
    'TRACE': {'THREAT_PRESENCE','CHARACTER_PERCEPTION','UNCERTAINTY'},
    'PARTIAL_REVEAL': {'THREAT_PRESENCE','CHARACTER_PERCEPTION','UNCERTAINTY'},
    'SCALE_REVEAL': {'SCALE','THREAT_PROXIMITY'},
    'ENCROACHMENT': {'THREAT_PROXIMITY'},
    'ESCAPE_DENIAL': {'ESCAPE_SPACE'},
    'FULL_REVEAL': {'THREAT_PRESENCE','ESCAPE_SPACE'},
    'COMMITMENT': {'CREATURE_INTENT','THREAT_PROXIMITY','CONSEQUENCE'},
    'CONSEQUENCE': {'CONSEQUENCE'},
    'AFTERMATH': {'AFTERMATH','CONSEQUENCE'},
}
GAIN_TO_DIM = {
    'PRESSURE':'THREAT_PRESENCE', 'UNCERTAINTY':'UNCERTAINTY', 'PROXIMITY':'THREAT_PROXIMITY',
    'ESCAPE_DENIAL':'ESCAPE_SPACE','PERCEPTION':'CHARACTER_PERCEPTION','SCALE':'SCALE',
    'ANTICIPATION':'ANTICIPATION','CONSEQUENCE':'CONSEQUENCE','SPATIAL_ORIENTATION':'SPATIAL_ORIENTATION',
    'FALSE_RELIEF':'UNCERTAINTY',
}
VISIBLE_ROLES = {'PARTIAL_REVEAL','SCALE_REVEAL','ENCROACHMENT','ESCAPE_DENIAL','FULL_REVEAL','COMMITMENT','CONSEQUENCE','AFTERMATH','PAYOFF'}


def load(p):
    text=Path(p).read_text(encoding='utf-8')
    return json.loads(text) if Path(p).suffix.lower()=='.json' else yaml.safe_load(text)

def meaningful(v): return bool(str(v or '').strip())
def norm(v): return re.sub(r"\s+", "", str(v or '')).lower()

def lint(exp, editorial, creature=None):
    issues=[]
    def add(t, **kw): issues.append({'type':t, **kw})
    if exp.get('genre_pressure_applicable') is not True or exp.get('status')=='NOT_REQUIRED':
        return {'pass':True,'gate':'EXPERIENCE_COMPLETENESS_PASS','applicable':False,'issues':[]}

    beats=exp.get('pressure_beats') or []
    by_id={b.get('beat_id'):b for b in beats if b.get('beat_id')}
    protected=[b for b in beats if b.get('protected_from_cost_compression') is True]
    anti=exp.get('anti_shortcut_policy') or {}
    if anti.get('protected_beat_delete_policy')!='FORBID': add('ANTI_SHORTCUT_POLICY_WEAKENED',field='protected_beat_delete_policy')
    if anti.get('protected_beat_merge_policy')!='FORBID_UNLESS_PROVEN_EQUIVALENT': add('ANTI_SHORTCUT_POLICY_WEAKENED',field='protected_beat_merge_policy')
    if anti.get('protected_beat_shorten_policy')!='REQUIRE_LANDING_EVIDENCE': add('ANTI_SHORTCUT_POLICY_WEAKENED',field='protected_beat_shorten_policy')
    if anti.get('experience_debt_must_be_zero_at_lock') is not True: add('ANTI_SHORTCUT_POLICY_WEAKENED',field='experience_debt_must_be_zero_at_lock')
    if anti.get('cost_is_not_compression_justification') is not True: add('ANTI_SHORTCUT_POLICY_WEAKENED',field='cost_is_not_compression_justification')

    # Director's own declared duration need cannot be silently under-budgeted.
    needed=sum(float(b.get('duration_need_seconds') or 0) for b in protected if (b.get('compression') or {}).get('action')=='KEEP')
    planned=exp.get('planned_scene_duration_seconds')
    if isinstance(planned,(int,float)) and planned + 1e-9 < needed:
        add('EXPERIENCE_DURATION_BUDGET_UNDERRUN',planned_scene_duration_seconds=planned,protected_keep_duration_need_seconds=needed)

    # Coverage debt is explicit and cross-checked against actual beat owners/gains/roles.
    covered_dims=set()
    for b in beats:
        for g in b.get('experience_gain') or []:
            if g in GAIN_TO_DIM: covered_dims.add(GAIN_TO_DIM[g])
        covered_dims |= ROLE_DIMENSION_HINTS.get(b.get('role'), set())
    for row in exp.get('experience_coverage_contract') or []:
        dim=row.get('dimension'); app=row.get('applicability'); owners=row.get('owner_beat_ids') or []
        if app=='REQUIRED':
            if not owners: add('EXPERIENCE_COVERAGE_DEBT',dimension=dim,reason='NO_OWNER_BEAT')
            unknown=sorted(set(owners)-set(by_id))
            if unknown: add('EXPERIENCE_COVERAGE_DEBT',dimension=dim,reason='UNKNOWN_OWNER_BEAT',beat_ids=unknown)
            if dim not in covered_dims: add('EXPERIENCE_COVERAGE_DEBT',dimension=dim,reason='NO_SEMANTIC_COVERAGE')
        elif app=='NOT_APPLICABLE' and not meaningful(row.get('not_applicable_reason')):
            add('EXPERIENCE_COVERAGE_NOT_APPLICABLE_UNJUSTIFIED',dimension=dim)

    # Beat landing + compression closure.
    shot_to_beats={}
    for b in protected:
        bid=b.get('beat_id'); land=b.get('landing_contract') or {}; comp=b.get('compression') or {}
        if land.get('required') is not True or not meaningful(land.get('landing_condition')) or land.get('exit_before_landing_forbidden') is not True:
            add('EXPERIENCE_LANDING_CONTRACT_GAP',beat_id=bid)
        action=comp.get('action')
        if action=='DELETE': add('PROTECTED_EXPERIENCE_BEAT_DELETE_FORBIDDEN',beat_id=bid)
        if action in {'MERGE','SHORTEN'}:
            j=comp.get('justification'); ev=comp.get('experience_equivalence_evidence')
            if not meaningful(j) or not meaningful(ev): add('EXPERIENCE_COMPRESSION_JUSTIFICATION_GAP',beat_id=bid,action=action)
            if meaningful(j) and COST_WORDS.search(str(j)): add('COST_DRIVEN_EXPERIENCE_COMPRESSION_FORBIDDEN',beat_id=bid,action=action)
            if action=='MERGE' and not (comp.get('target_beat_ids') or []): add('EXPERIENCE_COMPRESSION_TARGET_GAP',beat_id=bid,action=action)
        elif action=='KEEP':
            if comp.get('target_beat_ids'): add('EXPERIENCE_KEEP_HAS_MERGE_TARGETS',beat_id=bid)
        for sid in b.get('shot_ids') or []:
            shot_to_beats.setdefault(sid,[]).append(bid)

    # Multiple protected beats in the same shot are legal only with explicit MERGE evidence.
    for sid,bids in shot_to_beats.items():
        if len(bids)<=1: continue
        for bid in bids:
            comp=(by_id[bid].get('compression') or {})
            targets=set(comp.get('target_beat_ids') or [])
            others=set(bids)-{bid}
            if comp.get('action')!='MERGE' or not others.issubset(targets) or not meaningful(comp.get('experience_equivalence_evidence')):
                add('PROTECTED_BEAT_COLLAPSE_UNJUSTIFIED',shot_id=sid,beat_ids=sorted(bids))
                break

    # Editorial must carry each protected beat as experience, not merely retain the shot id.
    edshots={s.get('shot_id'):s for s in (editorial.get('shots') or []) if s.get('shot_id')}
    for b in protected:
        bid=b.get('beat_id'); mapped=[]
        for sid in b.get('shot_ids') or []:
            s=edshots.get(sid)
            if not s: continue
            if s.get('experience_beat_id')==bid:
                mapped.append(s)
        if not mapped:
            add('EXPERIENCE_EDITORIAL_BEAT_MAPPING_GAP',beat_id=bid,shot_ids=b.get('shot_ids') or [])
            continue
        for s in mapped:
            sid=s.get('shot_id')
            if s.get('protected_experience_beat') is not True:
                add('EXPERIENCE_EDITORIAL_PROTECTION_GAP',beat_id=bid,shot_id=sid)
            if not (meaningful(s.get('experience_state_in')) and meaningful(s.get('experience_delta')) and meaningful(s.get('experience_state_out'))):
                add('EXPERIENCE_EDITORIAL_STATE_GAP',beat_id=bid,shot_id=sid)
            elif norm(s.get('experience_state_in'))==norm(s.get('experience_state_out')):
                add('EXPERIENCE_EDITORIAL_NO_EFFECT',beat_id=bid,shot_id=sid)
        if b.get('role') in HOLD_ROLES:
            if not any(s.get('editorial_weight') in {'HOLD','EMPHASIS'} and s.get('breathing_function') in HOLD_FUNCTIONS for s in mapped):
                add('EXPERIENCE_HOLD_FUNCTION_UNDERDEVELOPED',beat_id=bid,role=b.get('role'))

    # Active visible creature beats need specific per-beat behavior, not one generic paragraph reused everywhere.
    if creature and creature.get('active_threat_present') is True:
        exp_role={b.get('beat_id'):b.get('role') for b in beats}
        for c in creature.get('creatures') or []:
            if c.get('threat_status')!='ACTIVE_THREAT': continue
            cid=c.get('creature_id'); rows=c.get('behavior_beat_map') or []; rb={r.get('beat_id'):r for r in rows if r.get('beat_id')}
            visible=[bid for bid in c.get('threat_coverage_beat_ids') or [] if exp_role.get(bid) in VISIBLE_ROLES]
            for bid in visible:
                row=rb.get(bid)
                if not row:
                    add('CREATURE_BEHAVIOR_BEAT_COVERAGE_GAP',creature_id=cid,beat_id=bid); continue
                missing=[f for f in ['perception_action','body_action','target_tracking_change','environment_response','pressure_function','exit_trigger'] if not meaningful(row.get(f))]
                if missing: add('CREATURE_BEHAVIOR_BEAT_FIELD_GAP',creature_id=cid,beat_id=bid,missing=missing)
            # Reusing essentially identical body/perception text across most visible beats is a wooden-monster shortcut.
            vals=[]
            for bid in visible:
                row=rb.get(bid) or {}
                vals.append(norm(str(row.get('perception_action',''))+'|'+str(row.get('body_action',''))+'|'+str(row.get('environment_response',''))))
            vals=[v for v in vals if v]
            if len(vals)>=3 and len(set(vals)) <= max(1, len(vals)//2):
                add('CREATURE_BEHAVIOR_TEMPLATE_REPETITION',creature_id=cid,visible_beat_count=len(vals),unique_behavior_count=len(set(vals)))

    return {
        'pass':not issues,'gate':'EXPERIENCE_COMPLETENESS_PASS','applicable':True,
        'protected_beat_count':len(protected),'declared_keep_duration_need_seconds':needed,
        'planned_scene_duration_seconds':planned,'issues':issues,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--experience-plan',required=True)
    ap.add_argument('--editorial-plan',required=True)
    ap.add_argument('--creature-plan')
    a=ap.parse_args()
    out=lint(load(a.experience_plan),load(a.editorial_plan),load(a.creature_plan) if a.creature_plan else None)
    print(json.dumps(out,ensure_ascii=False,indent=2))
    raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
