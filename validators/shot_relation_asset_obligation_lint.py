#!/usr/bin/env python3
"""V4.5.2 closure validator for SHOT_RELATION_GRAPH + VISUAL_ASSET_OBLIGATION.

Mechanically checks planning completeness, spatial proof references, due asset evidence,
and A_EXIT↔B_ENTRY pair binding. A textual PASS label is never treated as evidence by itself.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

PHASE_ORDER={'planning':0,'spatial':1,'freeze':2,'storyboard':3,'conditioning':4}
FULFILL_ORDER={'STAGE_03_FREEZE':2,'STAGE_04_STORYBOARD_QC':3,'STAGE_04_VIDEO_CONDITIONING_QC':4}
PROOF_REQUIRED={'CLUE_REVEAL_CUT','LOOK_POV_REVEAL','MATCH_CUT','CONTINUITY_CUT','ACTION_CONSEQUENCE'}
CLUE_SOURCE_TYPES={'SCENE_CLUE_VIEW','LOCATION_VISIBILITY_VIEW'}
IDENTITY_TYPES={'LOCATION_IDENTITY_VIEW'}
BOUNDARY_EXIT={'VIDEO_CUT_EXIT_FRAME','VIDEO_LAST_FRAME'}
BOUNDARY_ENTRY={'VIDEO_CUT_ENTRY_FRAME','VIDEO_FIRST_FRAME'}
LEGACY_COVERAGE_OBLIGATION_TYPES={'SCENE_CLUE_VIEW','LOCATION_VISIBILITY_VIEW','LOCATION_IDENTITY_VIEW'}
LEGACY_COVERAGE_ASSET_TYPES={'SCENE_CLUE_VIEW','LOCATION_VISIBILITY_VIEW','LOCATION_IDENTITY_VIEW','EVENT_NODE_VIEW','RECIPROCAL_COVERAGE_VIEW','PREDICTIVE_COVERAGE_VIEW','DERIVED_COVERAGE_VIEW'}
NON_WAIVABLE_TYPES=LEGACY_COVERAGE_OBLIGATION_TYPES|{'EMPTY_ENVIRONMENT_MASTER','FUNCTIONAL_MINOR_HUMAN_MASTER'}
APPROVED={'APPROVED','APPROVED_SUPPORT','APPROVED_ASSEMBLY','APPROVED_VIDEO_CONDITIONING'}

def coverage_reasons(ob):
    return set((ob or {}).get('coverage_reason_codes') or [])

def is_clue_source_obligation(ob):
    typ=(ob or {}).get('obligation_type')
    return typ in CLUE_SOURCE_TYPES or (typ=='ENVIRONMENT_COVERAGE' and bool(coverage_reasons(ob) & {'CLUE_REVEAL','LOCATION_VISIBILITY'}))

def is_identity_obligation(ob):
    typ=(ob or {}).get('obligation_type')
    return typ in IDENTITY_TYPES or (typ=='ENVIRONMENT_COVERAGE' and 'LOCATION_IDENTITY' in coverage_reasons(ob))

def is_non_waivable_obligation(ob):
    typ=(ob or {}).get('obligation_type')
    return typ in NON_WAIVABLE_TYPES or (typ=='ENVIRONMENT_COVERAGE' and bool(coverage_reasons(ob) & {'CLUE_REVEAL','LOCATION_VISIBILITY','LOCATION_IDENTITY'}))

def load(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))
def duplicates(vals):
    s=set(); d=set()
    for v in vals:
        if v in s: d.add(v)
        s.add(v)
    return sorted(d)

def asset_index(reg): return {a.get('asset_id'):a for a in ((reg or {}).get('assets') or [])}
def obligation_assets(ob,assets): return [assets.get(aid) for aid in (ob.get('fulfillment_asset_ids') or []) if aid in assets]

def lint(graph, obligations, phase, spatial=None, registry=None, conditioning=None):
    issues=[]; rels=graph.get('relations') or []; obs=obligations.get('obligations') or []
    if str((obligations or {}).get('skill_version') or '') in {'4.5.7','4.5.11'}:
        for o in obs:
            if o.get('obligation_type') in LEGACY_COVERAGE_OBLIGATION_TYPES:
                issues.append({'type':'LEGACY_COVERAGE_OBLIGATION_REQUIRES_MIGRATION','obligation_id':o.get('obligation_id'),'obligation_type':o.get('obligation_type'),'required_current_type':'ENVIRONMENT_COVERAGE'})
    if str((registry or {}).get('skill_version') or '') in {'4.5.7','4.5.11'}:
        for a in (registry or {}).get('assets') or []:
            if a.get('asset_type') in LEGACY_COVERAGE_ASSET_TYPES:
                issues.append({'type':'LEGACY_COVERAGE_ASSET_REQUIRES_MIGRATION','asset_id':a.get('asset_id'),'asset_type':a.get('asset_type'),'required_current_type':'ENVIRONMENT_COVERAGE'})
    for d in duplicates(graph.get('shot_order') or []): issues.append({'type':'DUPLICATE_SHOT_ORDER_ID','shot_id':d})
    for d in duplicates([r.get('relation_id') for r in rels]): issues.append({'type':'DUPLICATE_RELATION_ID','relation_id':d})
    for d in duplicates([o.get('obligation_id') for o in obs]): issues.append({'type':'DUPLICATE_OBLIGATION_ID','obligation_id':d})
    rel_by={r.get('relation_id'):r for r in rels}; ob_by={o.get('obligation_id'):o for o in obs}; assets=asset_index(registry)
    shot_order=graph.get('shot_order') or []
    adjacent={(shot_order[i],shot_order[i+1]) for i in range(len(shot_order)-1)}
    covered={(r.get('from_shot_id'),r.get('to_shot_id')) for r in rels}
    for pair in sorted(adjacent-covered): issues.append({'type':'SHOT_RELATION_GRAPH_GAP','from_shot_id':pair[0],'to_shot_id':pair[1]})
    for r in rels:
        rid=r.get('relation_id'); rt=r.get('relation_type')
        if (r.get('from_shot_id'),r.get('to_shot_id')) not in adjacent:
            issues.append({'type':'NON_ADJACENT_SHOT_RELATION','relation_id':rid,'from':r.get('from_shot_id'),'to':r.get('to_shot_id')})
        if not r.get('cut_motivation'): issues.append({'type':'CUT_MOTIVATION_UNBOUND','relation_id':rid})
        if rt in {'CLUE_REVEAL_CUT','LOOK_POV_REVEAL'} and not r.get('narrative_attention_target'): issues.append({'type':'NARRATIVE_ATTENTION_TARGET_AMBIGUOUS','relation_id':rid})
        if rt in PROOF_REQUIRED:
            if not r.get('source_visual_fact'): issues.append({'type':'SOURCE_VISUAL_FACT_MISSING','relation_id':rid})
            if not r.get('destination_visual_fact'): issues.append({'type':'DESTINATION_VISUAL_FACT_MISSING','relation_id':rid})
        ids=r.get('asset_obligation_ids') or []
        for oid in [x for x in ids if x not in ob_by]: issues.append({'type':'RELATION_ASSET_OBLIGATION_REF_MISSING','relation_id':rid,'obligation_id':oid})
        relation_obs=[ob_by[x] for x in ids if x in ob_by]
        if rt in PROOF_REQUIRED and not relation_obs: issues.append({'type':'RELATION_ASSET_OBLIGATION_GAP','relation_id':rid,'relation_type':rt})
        if rt=='CLUE_REVEAL_CUT':
            req=set(r.get('bridge_requirements') or [])
            for x in {'SOURCE_CLUE_VISIBLE','DESTINATION_IDENTITY_PROVEN'}-req: issues.append({'type':'CLUE_REVEAL_BRIDGE_REQUIREMENT_MISSING','relation_id':rid,'requirement':x})
            if not any(is_clue_source_obligation(o) for o in relation_obs): issues.append({'type':'CLUE_VIEW_OR_VISIBILITY_PROOF_MISSING','relation_id':rid})
            if not any(is_identity_obligation(o) for o in relation_obs): issues.append({'type':'DESTINATION_IDENTITY_ASSET_OBLIGATION_MISSING','relation_id':rid})
            wr={x.get('relation_kind') for x in (r.get('world_relations') or [])}
            if 'VISIBLE_FROM' not in wr: issues.append({'type':'CLUE_REVEAL_WORLD_VISIBILITY_MISSING','relation_id':rid})
            if not ({'EXTERIOR_INTERIOR_SAME_ENTITY','SAME_LOCATION_DIFFERENT_LAYER'} & wr): issues.append({'type':'CLUE_REVEAL_LOCATION_IDENTITY_RELATION_MISSING','relation_id':rid})
        # From spatial phase onward, graph must point to locked spatial proof for claims that require it.
        if PHASE_ORDER[phase]>=PHASE_ORDER['spatial'] and rt in PROOF_REQUIRED:
            if r.get('spatial_proof_status')!='PASS': issues.append({'type':'SHOT_RELATION_SPATIAL_PROOF_NOT_PASS','relation_id':rid,'status':r.get('spatial_proof_status')})
            if not (r.get('spatial_relation_ids') or []): issues.append({'type':'SHOT_RELATION_SPATIAL_PROOF_REF_MISSING','relation_id':rid})
            if spatial:
                sids={x.get('spatial_relation_id') for x in (spatial.get('relations') or []) if x.get('status')=='LOCKED'}
                for sid in r.get('spatial_relation_ids') or []:
                    if sid not in sids: issues.append({'type':'SHOT_RELATION_SPATIAL_PROOF_REF_MISSING','relation_id':rid,'spatial_relation_id':sid})
        # Conditioning: require actual corresponding exit/entry obligation assets and actual registry records.
        if phase=='conditioning' and rt in PROOF_REQUIRED:
            exits=[o for o in relation_obs if o.get('obligation_type') in BOUNDARY_EXIT]
            entries=[o for o in relation_obs if o.get('obligation_type') in BOUNDARY_ENTRY]
            if not exits or not entries: issues.append({'type':'CUT_PAIR_ASSET_OBLIGATION_GAP','relation_id':rid})
            pairs=[p for p in ((conditioning or {}).get('boundary_pairs') or []) if p.get('relation_id')==rid]
            if not pairs: issues.append({'type':'CUT_PAIR_RUNTIME_MISSING','relation_id':rid})
            for pair in pairs:
                ea=pair.get('exit_asset_id'); ia=pair.get('entry_asset_id')
                if pair.get('alignment_status')!='PASS': issues.append({'type':'CUT_PAIR_ALIGNMENT_FAIL','relation_id':rid,'status':pair.get('alignment_status')})
                if not ea or not ia: issues.append({'type':'CUT_PAIR_BOUNDARY_ASSET_MISSING','relation_id':rid}); continue
                exit_allowed={x for o in exits for x in (o.get('fulfillment_asset_ids') or [])}; entry_allowed={x for o in entries for x in (o.get('fulfillment_asset_ids') or [])}
                if ea not in exit_allowed: issues.append({'type':'CUT_PAIR_EXIT_NOT_BOUND_TO_OBLIGATION','relation_id':rid,'asset_id':ea})
                if ia not in entry_allowed: issues.append({'type':'CUT_PAIR_ENTRY_NOT_BOUND_TO_OBLIGATION','relation_id':rid,'asset_id':ia})
                if registry:
                    for aid,expected in [(ea,{'VIDEO_CUT_EXIT_FRAME','VIDEO_LAST_FRAME'}),(ia,{'VIDEO_CUT_ENTRY_FRAME','VIDEO_FIRST_FRAME'})]:
                        a=assets.get(aid)
                        if not a: issues.append({'type':'CUT_PAIR_ASSET_NOT_IN_REGISTRY','relation_id':rid,'asset_id':aid}); continue
                        if a.get('status') not in APPROVED: issues.append({'type':'CUT_PAIR_ASSET_NOT_APPROVED','relation_id':rid,'asset_id':aid,'status':a.get('status')})
                        if a.get('asset_type') not in expected: issues.append({'type':'CUT_PAIR_ASSET_TYPE_MISMATCH','relation_id':rid,'asset_id':aid,'asset_type':a.get('asset_type')})
                        if rid not in (a.get('relation_ids') or []): issues.append({'type':'CUT_PAIR_ASSET_RELATION_BINDING_MISSING','relation_id':rid,'asset_id':aid})
    pord=PHASE_ORDER[phase]
    for o in obs:
        oid=o.get('obligation_id'); due=FULFILL_ORDER.get(o.get('fulfill_by'),99); typ=o.get('obligation_type')
        if o.get('status')=='WAIVED':
            pol=o.get('waiver_policy') or ('NON_WAIVABLE' if is_non_waivable_obligation(o) else 'USER_APPROVAL_REQUIRED')
            if pol=='NON_WAIVABLE': issues.append({'type':'NON_WAIVABLE_RELATION_ASSET_WAIVED','obligation_id':oid,'obligation_type':typ})
            if not o.get('waiver_reason'): issues.append({'type':'WAIVER_WITHOUT_REASON','obligation_id':oid})
        if due<=pord and o.get('status') not in {'FULFILLED','WAIVED'}: issues.append({'type':'RELATION_ASSET_OBLIGATION_UNFULFILLED','obligation_id':oid,'fulfill_by':o.get('fulfill_by'),'status':o.get('status')})
        if o.get('status')=='FULFILLED':
            ids=o.get('fulfillment_asset_ids') or []
            if not ids: issues.append({'type':'FULFILLED_OBLIGATION_WITHOUT_ASSET','obligation_id':oid})
            if due<=pord and o.get('proof_status')!='PASS': issues.append({'type':'FULFILLED_OBLIGATION_PROOF_NOT_PASS','obligation_id':oid,'proof_status':o.get('proof_status')})
            if registry:
                for aid in ids:
                    a=assets.get(aid)
                    if not a: issues.append({'type':'FULFILLMENT_ASSET_NOT_IN_REGISTRY','obligation_id':oid,'asset_id':aid}); continue
                    if a.get('status') not in APPROVED: issues.append({'type':'FULFILLMENT_ASSET_NOT_APPROVED','obligation_id':oid,'asset_id':aid,'status':a.get('status')})
                    if oid not in (a.get('obligation_ids') or []): issues.append({'type':'FULFILLMENT_ASSET_OBLIGATION_BINDING_MISSING','obligation_id':oid,'asset_id':aid})
        rid=o.get('relation_id')
        if rid and rid not in rel_by: issues.append({'type':'OBLIGATION_UNKNOWN_RELATION','obligation_id':oid,'relation_id':rid})
    if graph.get('status')!='LOCKED': issues.append({'type':'SHOT_RELATION_GRAPH_NOT_LOCKED','status':graph.get('status')})
    return {'pass':not issues,'phase':phase,'relation_count':len(rels),'obligation_count':len(obs),'issues':issues}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--graph',required=True); ap.add_argument('--obligations',required=True); ap.add_argument('--phase',required=True,choices=list(PHASE_ORDER)); ap.add_argument('--spatial-canon'); ap.add_argument('--asset-registry'); ap.add_argument('--conditioning-runtime'); a=ap.parse_args()
    out=lint(load(a.graph),load(a.obligations),a.phase,load(a.spatial_canon) if a.spatial_canon else None,load(a.asset_registry) if a.asset_registry else None,load(a.conditioning_runtime) if a.conditioning_runtime else None)
    print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
