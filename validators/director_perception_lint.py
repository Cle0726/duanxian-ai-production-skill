#!/usr/bin/env python3
"""Validate director-perception contracts and report anti-pattern drift.

Hard errors cover missing/weak creative causality needed to lock the Director Core.
Cross-shot repetition is advisory only: warnings never force gratuitous variation.
"""
from __future__ import annotations
import argparse, json
from collections import Counter
from pathlib import Path
import yaml

CAMERA_ETHICS={
    'NEUTRAL_WITNESS','INVOLVED_PARTICIPANT','FORBIDDEN_WITNESS','DISTANT_OBSERVER',
    'SURVEILLANCE_OBSERVER','TRAPPED_OBSERVER','CHARACTER_ALIGNED','MISINFORMED_OBSERVER','OTHER'
}
CLOSEUP_TOKENS={'CU','ECU','CLOSE_UP','CLOSEUP','EXTREME_CLOSE_UP','EXTREME_CLOSEUP','DETAIL','INSERT','MACRO'}
GENERIC_JUSTIFICATIONS={
    'emotion','more emotion','emotional','more emotional','cinematic','dramatic','intense','intensity',
    '情绪','情绪更强','更有情绪','更电影','电影感','更紧张','更有张力','好看','高级感','强化情绪'
}

def load(path):
    return yaml.safe_load(Path(path).read_text(encoding='utf-8'))

def text(v):
    return str(v or '').strip()

def meaningful(v):
    return bool(text(v))

def add(findings, typ, severity='ERROR', **kw):
    findings.append({'type':typ,'severity':severity,**kw})

def is_closeup(v):
    s=text(v).upper().replace('-','_').replace(' ','_')
    return s in CLOSEUP_TOKENS or 'CLOSE' in s or s in {'DETAIL_EVIDENCE','INSERT'}

def weak_justification(v):
    s=text(v).lower().replace('。','').replace('.','')
    if not s:
        return True
    return s in GENERIC_JUSTIFICATIONS or len(s) < 6

def lint(runtime, editorial=None):
    findings=[]
    if runtime.get('runtime_type')!='DIRECTOR_RUNTIME':
        add(findings,'DIRECTOR_RUNTIME_TYPE_FAIL',actual=runtime.get('runtime_type'))
    if runtime.get('status') not in {None,'VALID'}:
        add(findings,'DIRECTOR_RUNTIME_NOT_VALID',status=runtime.get('status'))

    pc=runtime.get('perception_context') or {}
    unresolved=pc.get('unresolved_state') or {}
    connective_exception=meaningful(unresolved.get('connective_exception_reason'))
    if not connective_exception:
        missing=[k for k in ('what_character_wants','what_prevents_resolution','why_not_resolvable_now','what_can_change_state') if not meaningful(unresolved.get(k))]
        if missing: add(findings,'UNRESOLVED_STATE_GAP',missing=missing)

    pressure=pc.get('relational_pressure') or {}
    p_missing=[k for k in ('pressure_source','pressure_target','knowledge_asymmetry','power_asymmetry') if not meaningful(pressure.get(k))]
    if not (meaningful(pressure.get('spatial_constraint')) or meaningful(pressure.get('social_constraint'))):
        p_missing.append('spatial_constraint_or_social_constraint')
    if p_missing: add(findings,'RELATIONAL_PRESSURE_GAP',missing=p_missing)

    contracts=runtime.get('shot_perception_contracts') or {}
    order=(editorial or {}).get('shot_order') or list(contracts.keys())
    editorial_rows={x.get('shot_id'):x for x in ((editorial or {}).get('shots') or []) if x.get('shot_id')}

    current_signatures=[]
    for sid in order:
        c=contracts.get(sid)
        if not isinstance(c,dict):
            add(findings,'SHOT_PERCEPTION_CONTRACT_GAP',shot_id=sid); continue
        ethics=c.get('camera_ethics')
        if ethics not in CAMERA_ETHICS:
            add(findings,'CAMERA_ETHICS_GAP',shot_id=sid,actual=ethics)

        af=c.get('attention_flow') or {}
        af_missing=[k for k in ('entry','resistance','decisive_landing','residual_information','exit') if not meaningful(af.get(k))]
        if af_missing: add(findings,'ATTENTION_FLOW_GAP',shot_id=sid,missing=af_missing)

        place=c.get('camera_placement_justification') or {}
        place_missing=[k for k in ('physical','narrative') if not meaningful(place.get(k))]
        if place_missing: add(findings,'CAMERA_PLACEMENT_JUSTIFICATION_GAP',shot_id=sid,missing=place_missing)

        scale=c.get('shot_scale_justification') or {}
        sf=scale.get('shot_size_family')
        scale_missing=[k for k in ('shot_size_family','required_information','narrative_gain') if not meaningful(scale.get(k))]
        if scale_missing: add(findings,'SHOT_SCALE_JUSTIFICATION_GAP',shot_id=sid,missing=scale_missing)
        erow=editorial_rows.get(sid) or {}
        esf=erow.get('shot_size_family')
        if meaningful(esf) and meaningful(sf) and text(esf).upper()!=text(sf).upper():
            add(findings,'SHOT_SCALE_CONTRACT_MISMATCH',shot_id=sid,director_runtime=sf,editorial_plan=esf)
        if is_closeup(sf or esf):
            if weak_justification(scale.get('why_wider_fails')) or weak_justification(scale.get('narrative_gain')):
                add(findings,'CLOSEUP_JUSTIFICATION_WEAK',shot_id=sid,why_wider_fails=scale.get('why_wider_fails'),narrative_gain=scale.get('narrative_gain'))
            if not meaningful(scale.get('spatial_information_sacrificed')):
                add(findings,'CLOSEUP_SPATIAL_COST_GAP',shot_id=sid)

        vf=c.get('visual_force_stack') or {}
        if not meaningful(vf.get('primary_force')):
            add(findings,'VISUAL_FORCE_STACK_GAP',shot_id=sid)
        supports=vf.get('supporting_forces') or []
        if len(supports)>2:
            add(findings,'VISUAL_FORCE_STACK_OVERLOAD',shot_id=sid,supporting_count=len(supports))

        sal=c.get('visual_salience_budget') or {}
        sal_missing=[k for k in ('primary_salience','ambient_information','suppressed_information','allowed_mundane_area') if not meaningful(sal.get(k))]
        if sal_missing: add(findings,'VISUAL_SALIENCE_BUDGET_GAP',shot_id=sid,missing=sal_missing)

        comp=(c.get('composition_mechanism') or {}).get('primary')
        current_signatures.append((sid,text(sf or esf),text(erow.get('viewpoint_role')),text(ethics),text(comp),text(af.get('entry')),text(af.get('decisive_landing'))))

    # Current-sequence anti-template warnings. These never hard-fail.
    if len(current_signatures)>=3:
        for i in range(len(current_signatures)-2):
            tri=current_signatures[i:i+3]
            # same attention path wording = likely copied template
            flows=[(x[5],x[6]) for x in tri]
            if flows[0]==flows[1]==flows[2] and all(flows[0]):
                add(findings,'ATTENTION_FLOW_TEMPLATE_REPEAT','WARN',shot_ids=[x[0] for x in tri],signature=flows[0])

    # Historical creative drift telemetry: advisory only.
    history=runtime.get('shot_grammar_history') or []
    window=(runtime.get('creative_drift_telemetry') or {}).get('window_size') or 24
    hist=history[-int(window):] if history else []
    if len(hist)>=8:
        close_count=sum(1 for h in hist if is_closeup(h.get('shot_size_family')))
        ratio=close_count/len(hist)
        if ratio>0.45:
            add(findings,'SHOT_SCALE_BIAS','WARN',window=len(hist),closeup_count=close_count,closeup_ratio=round(ratio,3))
        for field,code,threshold in [
            ('camera_ethics','CAMERA_ETHICS_BIAS',0.65),
            ('composition_mechanism','COMPOSITION_PATTERN_COLLAPSE',0.55),
            ('viewpoint_role','VIEWPOINT_ROLE_BIAS',0.65),
            ('camera_character','CAMERA_CHARACTER_BIAS',0.60),
        ]:
            vals=[text(h.get(field)) for h in hist if meaningful(h.get(field))]
            if len(vals)>=8:
                val,count=Counter(vals).most_common(1)[0]
                r=count/len(vals)
                if r>threshold:
                    add(findings,code,'WARN',field=field,value=val,count=count,window=len(vals),ratio=round(r,3))
        # exact 3-shot grammar recurring at least twice
        sig=[(text(h.get('shot_size_family')),text(h.get('viewpoint_role')),text(h.get('composition_mechanism'))) for h in hist]
        triples=Counter(tuple(sig[i:i+3]) for i in range(max(0,len(sig)-2)))
        if triples:
            pattern,count=triples.most_common(1)[0]
            if count>=2 and all(any(x) for x in pattern):
                add(findings,'EDITORIAL_PATTERN_COLLAPSE','WARN',pattern=pattern,occurrences=count)

    errors=[x for x in findings if x['severity']=='ERROR']
    warnings=[x for x in findings if x['severity']=='WARN']
    return {'pass':not errors,'error_count':len(errors),'warning_count':len(warnings),'findings':findings}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--director-runtime',required=True)
    ap.add_argument('--editorial-plan')
    a=ap.parse_args()
    out=lint(load(a.director_runtime),load(a.editorial_plan) if a.editorial_plan else None)
    print(json.dumps(out,ensure_ascii=False,indent=2))
    raise SystemExit(0 if out['pass'] else 2)

if __name__=='__main__': main()
