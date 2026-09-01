#!/usr/bin/env python3
"""Deterministic lint for sequence-level editorial intent.

Errors block the sequence. Warnings flag likely visual/editorial monotony but do not force cuts.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml


def load(path):
    return yaml.safe_load(Path(path).read_text(encoding='utf-8'))


def lint(plan, relation_graph=None):
    findings=[]
    def add(kind, severity='ERROR', **data):
        findings.append({'type':kind,'severity':severity,**data})

    if plan.get('status') != 'LOCKED':
        add('EDITORIAL_PLAN_NOT_LOCKED', status=plan.get('status'))

    order=plan.get('shot_order') or []
    if len(order) != len(set(order)):
        add('EDITORIAL_DUPLICATE_SHOT_ORDER')

    shot_rows=plan.get('shots') or []
    by_shot={s.get('shot_id'):s for s in shot_rows if s.get('shot_id')}
    for sid in order:
        if sid not in by_shot:
            add('EDITORIAL_SHOT_VIEWPOINT_GAP', shot_id=sid)
    for sid in by_shot:
        if sid not in set(order):
            add('EDITORIAL_UNKNOWN_SHOT', shot_id=sid)

    # Information-state and hold/breathing contracts belong to Editorial Authority.
    seq_strategy=plan.get('sequence_strategy') or {}
    seq_logic=seq_strategy.get('sequence_logic')
    if seq_logic not in {'CAUSAL','ASSOCIATIVE','MONTAGE'}:
        add('SEQUENCE_LOGIC_GAP', actual=seq_logic)
    for sid in order:
        row=by_shot.get(sid,{})
        if row.get('editorial_weight') not in {'TRANSIENT','NORMAL','EMPHASIS','HOLD'}:
            add('EDITORIAL_WEIGHT_GAP', shot_id=sid, actual=row.get('editorial_weight'))
        bf=row.get('breathing_function')
        if bf not in {'NONE','DECOMPRESSION','ANTICIPATION','SPATIAL_REORIENTATION','EMOTIONAL_DELAY','TEMPORAL_REALISM'}:
            add('BREATHING_FUNCTION_GAP', shot_id=sid, actual=bf)
        # Breathing shots may intentionally reveal very little, but still need explicit audience in/out states.
        needed=['information_state_in','information_state_out']
        if bf in {None,'NONE'}:
            needed += ['information_revealed','information_withheld']
        missing=[k for k in needed if not str(row.get(k) or '').strip()]
        if missing:
            add('SHOT_INFORMATION_STATE_GAP', shot_id=sid, missing=missing)

    shuffle=plan.get('shuffle_test') or {}
    if len(order) > 1 and seq_logic == 'CAUSAL':
        if shuffle.get('status') != 'PASS':
            add('SEQUENCE_SHUFFLE_TEST_GAP', status=shuffle.get('status'))
        if shuffle.get('counterfactual_swap_breaks_sequence') is not True:
            add('SEQUENCE_SHUFFLE_TEST_FAIL', counterfactual_swap_breaks_sequence=shuffle.get('counterfactual_swap_breaks_sequence'))
        if not (shuffle.get('dependency_reasons') or []):
            add('SEQUENCE_SHUFFLE_TEST_GAP', field='dependency_reasons')
    elif len(order) > 1 and seq_logic in {'ASSOCIATIVE','MONTAGE'}:
        if shuffle.get('status') not in {'PASS','NOT_REQUIRED'}:
            add('SEQUENCE_SHUFFLE_TEST_GAP', status=shuffle.get('status'), sequence_logic=seq_logic)
        if not str(shuffle.get('rationale') or '').strip():
            add('SEQUENCE_SHUFFLE_TEST_GAP', field='rationale', sequence_logic=seq_logic)

    edits=plan.get('edits') or []
    edit_by_pair={}
    for e in edits:
        pair=(e.get('from_shot_id'), e.get('to_shot_id'))
        if pair in edit_by_pair:
            add('EDITORIAL_DUPLICATE_EDIT_PAIR', from_shot_id=pair[0], to_shot_id=pair[1])
        edit_by_pair[pair]=e
        if e.get('status') != 'LOCKED':
            add('EDITORIAL_EDIT_NOT_LOCKED', edit_id=e.get('edit_id'), status=e.get('status'))
        if not e.get('cut_trigger'):
            add('CUT_TRIGGER_MISSING', edit_id=e.get('edit_id'))
        if not e.get('cut_timing'):
            add('CUT_TIMING_MISSING', edit_id=e.get('edit_id'))
        if not e.get('edit_function'):
            add('CUT_INFORMATION_FUNCTION_GAP', edit_id=e.get('edit_id'))
        if not e.get('information_delta') and not e.get('rhythm_function'):
            add('CUT_INFORMATION_FUNCTION_GAP', edit_id=e.get('edit_id'))
        cs=set(e.get('continuity_strategy') or [])
        if not cs:
            add('EDIT_CONTINUITY_STRATEGY_MISSING', edit_id=e.get('edit_id'))
        if 'INTENTIONAL_DISCONTINUITY' in cs and not e.get('audience_effect'):
            add('INTENTIONAL_DISCONTINUITY_EFFECT_MISSING', edit_id=e.get('edit_id'))

    adjacent=[(order[i],order[i+1]) for i in range(len(order)-1)]
    for a,b in adjacent:
        if (a,b) not in edit_by_pair:
            add('EDITORIAL_EDIT_POINT_GAP', from_shot_id=a, to_shot_id=b)
    for a,b in edit_by_pair:
        if (a,b) not in set(adjacent):
            add('EDITORIAL_NON_ADJACENT_EDIT', from_shot_id=a, to_shot_id=b)

    if relation_graph:
        rels={(r.get('from_shot_id'),r.get('to_shot_id')):r for r in (relation_graph.get('relations') or [])}
        for pair,e in edit_by_pair.items():
            r=rels.get(pair)
            if not r:
                add('EDIT_RELATION_MISMATCH', edit_id=e.get('edit_id'), from_shot_id=pair[0], to_shot_id=pair[1])
                continue
            rid=e.get('relation_id')
            if rid and rid != r.get('relation_id'):
                add('EDIT_RELATION_MISMATCH', edit_id=e.get('edit_id'), relation_id=rid, expected_relation_id=r.get('relation_id'))

    # Monotony warnings: do not force extra cuts.
    sustained=((plan.get('sequence_strategy') or {}).get('sustained_strategy') or '').strip()
    if not sustained and len(order) >= 3:
        for i in range(len(order)-2):
            trio=[by_shot.get(x,{}) for x in order[i:i+3]]
            sig=[(x.get('viewpoint_role'),x.get('shot_size_family'),x.get('subject_view')) for x in trio]
            if sig[0] == sig[1] == sig[2] and all(sig[0]):
                add('VIEWPOINT_STAGNATION_RISK','WARN', shot_ids=order[i:i+3], signature=sig[0])

    # Repeated A/B relational coverage is not automatically wrong, but flag if no changing function.
    if len(order) >= 4:
        roles=[by_shot.get(s,{}).get('viewpoint_role') for s in order]
        for i in range(len(roles)-3):
            if roles[i] and roles[i]==roles[i+2] and roles[i+1] and roles[i+1]==roles[i+3] and roles[i]!=roles[i+1]:
                funcs=[edit_by_pair.get((order[j],order[j+1]),{}).get('edit_function') for j in range(i,i+3)]
                if len(set(funcs)) <= 1:
                    add('MECHANICAL_REVERSE_SHOT_RISK','WARN', shot_ids=order[i:i+4])

    # Sequence-local scale bias is advisory; do not force a wider shot if the close-up is justified.
    close_tokens={'CU','ECU','CLOSEUP','CLOSE_UP','EXTREME_CLOSEUP','EXTREME_CLOSE_UP','DETAIL','INSERT'}
    scale_vals=[str(by_shot.get(s,{}).get('shot_size_family') or '').upper().replace('-','_').replace(' ','_') for s in order]
    if len(scale_vals) >= 4:
        close_count=sum(1 for x in scale_vals if x in close_tokens or 'CLOSE' in x)
        if close_count/len(scale_vals) > 0.5:
            add('SEQUENCE_CLOSEUP_BIAS_RISK','WARN', closeup_count=close_count, shot_count=len(scale_vals))

    errors=[x for x in findings if x['severity']=='ERROR']
    warnings=[x for x in findings if x['severity']=='WARN']
    return {'pass':not errors,'error_count':len(errors),'warning_count':len(warnings),'findings':findings}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--plan',required=True)
    ap.add_argument('--relation-graph')
    a=ap.parse_args()
    out=lint(load(a.plan), load(a.relation_graph) if a.relation_graph else None)
    print(json.dumps(out,ensure_ascii=False,indent=2))
    raise SystemExit(0 if out['pass'] else 2)

if __name__=='__main__':
    main()
