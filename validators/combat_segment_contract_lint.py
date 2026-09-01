#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

ROLES={
'FULL_EXCHANGE','ORIENTATION','THREAT_REVEAL','SPATIAL_READ','APPROACH','PROBE','COMMITMENT','CONTACT','CONTROL','REVERSAL','CONSEQUENCE','REACTION','PURSUIT','ESCAPE','PROJECTILE_RELEASE','PROJECTILE_TRAVEL','INTERCEPT','SCALE_REVEAL','RESET','PAYOFF'}

def load(p):
    text=Path(p).read_text(encoding='utf-8')
    return json.loads(text) if Path(p).suffix.lower()=='.json' else yaml.safe_load(text)

def get(d,path):
    cur=d
    for k in path.split('.'):
        if not isinstance(cur,dict): return None
        cur=cur.get(k)
    return cur

def need(issues,d,*paths):
    for p in paths:
        v=get(d,p)
        if v is None or v=='' or v==[]:
            issues.append({'type':'COMBAT_SEGMENT_ROLE_FIELD_MISSING','field':p,'segment_role':d.get('segment_role')})

def lint(d):
    issues=[]; role=d.get('segment_role')
    if role not in ROLES: issues.append({'type':'COMBAT_SEGMENT_ROLE_INVALID','actual':role})
    need(issues,d,'combat_segment_id','combat_objective','entry_combat_state','exit_combat_state','generation_risk.level','generation_risk.primary_contact_count')
    # Role-aware contracts: no CONTACT/Recoil requirements on reveal/orientation/reaction shots.
    if role=='FULL_EXCHANGE':
        need(issues,d,'engagement_distance.entry','engagement_distance.exit','read_decision.read','read_decision.decision','attack_defense_exchange.attacker','attack_defense_exchange.defender','attack_defense_exchange.attack_action','attack_defense_exchange.defense_response','lanes.attack_lane','lanes.escape_lane','contact.contact_type','contact.contact_point','contact.force_direction','recoil_recovery.recoil','recoil_recovery.recovery','initiative_shift','camera_read.contact_read')
    elif role in {'ORIENTATION','SPATIAL_READ'}:
        need(issues,d,'camera_read.function','camera_read.attention_landing')
    elif role in {'THREAT_REVEAL','SCALE_REVEAL'}:
        need(issues,d,'reveal.threat_source','reveal.audience_knowledge_out','camera_read.attention_landing')
        if role=='SCALE_REVEAL': need(issues,d,'reveal.scale_subject','reveal.human_scale_anchor','reveal.environment_scale_anchor','reveal.reveal_progression')
    elif role in {'APPROACH','PROBE','COMMITMENT'}:
        need(issues,d,'engagement_distance.entry','engagement_distance.exit','read_decision.read','read_decision.decision','camera_read.function')
        if role=='COMMITMENT': need(issues,d,'lanes.attack_lane')
    elif role=='CONTACT':
        need(issues,d,'engagement_distance.entry','engagement_distance.exit','attack_defense_exchange.attacker','attack_defense_exchange.defender','attack_defense_exchange.attack_action','attack_defense_exchange.defense_response','contact.contact_type','contact.contact_point','contact.force_direction','recoil_recovery.recoil','recoil_recovery.recovery','camera_read.contact_read')
        if get(d,'contact.contact_type')=='NONE': issues.append({'type':'COMBAT_CONTACT_ROLE_WITHOUT_CONTACT'})
    elif role in {'CONTROL','REVERSAL'}:
        need(issues,d,'attack_defense_exchange.attacker','attack_defense_exchange.defender','initiative_shift','consequence.tactical_result','camera_read.function')
    elif role in {'CONSEQUENCE','PAYOFF'}:
        need(issues,d,'consequence.tactical_result','camera_read.attention_landing')
        if not (get(d,'consequence.environment_proof') or get(d,'consequence.body_state_change')):
            issues.append({'type':'COMBAT_CONSEQUENCE_PROOF_MISSING','segment_role':role})
    elif role=='REACTION':
        need(issues,d,'camera_read.attention_landing','consequence.tactical_result')
    elif role in {'PURSUIT','ESCAPE'}:
        need(issues,d,'pursuit.route','pursuit.motion_vector','pursuit.relative_distance_change','pursuit.camera_subject_coupling','pursuit.momentum_landing')
    elif role in {'PROJECTILE_RELEASE','PROJECTILE_TRAVEL','INTERCEPT'}:
        need(issues,d,'projectile.entity_id','projectile.source','projectile.trajectory','projectile.target','projectile.state_in','projectile.state_out','camera_read.function')
    elif role=='RESET':
        need(issues,d,'engagement_distance.exit','camera_read.attention_landing')
    vfx_level=get(d,'vfx_coverage.effect_level')
    if vfx_level in {'STRUCTURAL','NARRATIVE'}:
        for field in ('vfx_coverage.source_read','vfx_coverage.geometry_read','vfx_coverage.scale_proof','vfx_coverage.aftermath_read'):
            if not get(d,field): issues.append({'type':'COMBAT_VFX_COVERAGE_GAP','field':field,'effect_level':vfx_level})

    risk=get(d,'generation_risk.level'); contacts=get(d,'generation_risk.primary_contact_count')
    if risk in {'L7','L8'} and isinstance(contacts,int) and contacts>1:
        issues.append({'type':'COMBAT_GENERATION_RISK_OVERLOAD','risk_level':risk,'primary_contact_count':contacts,'recommendation':'split at contact / initiative shift'})
    bridge=get(d,'generation_risk.bridge_mode')
    if bridge and bridge!='NONE' and not get(d,'generation_risk.bridge_reason'):
        issues.append({'type':'COMBAT_GENERATIVE_BRIDGE_REASON_MISSING','bridge_mode':bridge})
    return {'pass':not issues,'issues':issues,'segment_role':role,'generation_risk_level':risk}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('contract'); a=ap.parse_args(); out=lint(load(a.contract)); print(json.dumps(out,ensure_ascii=False,indent=2)); return 0 if out['pass'] else 2
if __name__=='__main__': raise SystemExit(main())
