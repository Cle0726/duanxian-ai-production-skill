#!/usr/bin/env python3
"""Prove that protected threat/genre-pressure beats survive into the final video prompt."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
import yaml
CORE_PATTERNS={
 'THREAT_ROLE':[r'Threat\s*Coverage\s*Role',r'威胁覆盖角色',r'威胁镜头角色'],
 'PRESSURE_STATE':[r'Pressure\s*(?:State|IN)',r'压力状态',r'Pressure\s*IN.*(?:→|->)',r'威胁压力'],
 'EXPERIENCE_GAIN':[r'Experience\s*Gain',r'体验增益',r'观众体验增益'],
}
CREATURE_PATTERNS={
 'CREATURE_BEHAVIOR':[r'Creature\s*Behavior',r'怪物行为',r'威胁行为'],
 'PERCEPTION_TRACKING':[r'Perception',r'Target\s*Tracking',r'感知',r'目标跟踪',r'锁定目标'],
 'BODY_MOTION':[r'Locomotion',r'Body\s*Coordination',r'移动方式',r'身体协调',r'肢体协调'],
 'WEIGHT_ENVIRONMENT':[r'Weight',r'Environment\s*Coupling',r'重量',r'惯性',r'环境耦合',r'地面.*(?:承重|震动|响应)'],
 'APPROACH_PAUSE':[r'Approach',r'Pause',r'Predatory\s*Stillness',r'逼近',r'停顿',r'捕猎静止',r'蓄势静止'],
}
COMMIT_PATTERNS=[r'Attack\s*Prep',r'Commitment',r'攻击准备',r'攻击前兆',r'真正发动',r'承诺动作']

def load(p):
    text=Path(p).read_text(encoding='utf-8')
    return json.loads(text) if Path(p).suffix.lower()=='.json' else yaml.safe_load(text)
def has(text,pats): return any(re.search(p,text,re.I) for p in pats)
def prompt_text(p):
    q=Path(p); return q.read_text(encoding='utf-8') if q.is_file() else str(p)

def lint(text, execution_plan, experience, creature):
    issues=[]; shot_id=execution_plan.get('shot_id')
    if experience.get('genre_pressure_applicable') is not True or experience.get('status')=='NOT_REQUIRED':
        return {'pass':True,'gate':'EXPERIENCE_VIDEO_PROMPT_HANDOFF_PASS','applicable':False,'issues':[]}
    beats=[b for b in (experience.get('pressure_beats') or []) if shot_id and shot_id in (b.get('shot_ids') or [])]
    if not beats:
        return {'pass':True,'gate':'EXPERIENCE_VIDEO_PROMPT_HANDOFF_PASS','applicable':False,'shot_id':shot_id,'issues':[]}
    if not any(b.get('protected_from_cost_compression') is True for b in beats):
        issues.append({'type':'EXPERIENCE_VIDEO_PROMPT_PROTECTED_BEAT_MISSING','shot_id':shot_id})
    for name,pats in CORE_PATTERNS.items():
        if not has(text,pats): issues.append({'type':'EXPERIENCE_VIDEO_PROMPT_CONCEPT_MISSING','shot_id':shot_id,'concept':name})
    roles={str(b.get('role')) for b in beats}; gains=sorted({str(g) for b in beats for g in (b.get('experience_gain') or [])})
    role_patterns=[]
    if roles & {'OMEN','OFFSCREEN_THREAT','TRACE'}: role_patterns=[r'画外',r'异常',r'痕迹',r'声响',r'未见',r'offscreen',r'omen',r'trace']
    elif 'NEGATIVE_SPACE_HOLD' in roles: role_patterns=[r'负空间',r'空镜',r'等待',r'停留',r'negative\s*space']
    elif 'PARTIAL_REVEAL' in roles: role_patterns=[r'局部',r'轮廓',r'影子',r'只露',r'partial\s*reveal']
    elif 'SCALE_REVEAL' in roles: role_patterns=[r'尺度',r'人物参照',r'建筑参照',r'scale']
    elif roles & {'ENCROACHMENT','ESCAPE_DENIAL'}: role_patterns=[r'逼近',r'距离缩短',r'退路',r'出口',r'封锁',r'encroach',r'escape']
    elif roles & {'CONSEQUENCE','AFTERMATH'}: role_patterns=[r'后果',r'余波',r'残留',r'结果',r'consequence',r'aftermath']
    if role_patterns and not has(text,role_patterns):
        issues.append({'type':'EXPERIENCE_VIDEO_PROMPT_ROLE_READ_MISSING','shot_id':shot_id,'roles':sorted(roles)})
    beat_ids={b.get('beat_id') for b in beats}; active=[]
    if creature and creature.get('active_threat_present') is True:
        for c in creature.get('creatures') or []:
            if c.get('threat_status')=='ACTIVE_THREAT' and beat_ids.intersection(c.get('threat_coverage_beat_ids') or []): active.append(c)
    for c in active:
        cid=c.get('creature_id')
        for name,pats in CREATURE_PATTERNS.items():
            if not has(text,pats): issues.append({'type':'CREATURE_VIDEO_PROMPT_CONCEPT_MISSING','shot_id':shot_id,'creature_id':cid,'concept':name})
        if roles & {'COMMITMENT','PAYOFF'} and not has(text,COMMIT_PATTERNS):
            issues.append({'type':'CREATURE_VIDEO_PROMPT_COMMITMENT_GAP','shot_id':shot_id,'creature_id':cid})
        if (c.get('stillness') or {}).get('mode')=='PREDATORY_STILLNESS' and not has(text,[r'Predatory\s*Stillness',r'捕猎静止',r'蓄势静止',r'静止.*(?:压力|威胁|等待)']):
            issues.append({'type':'CREATURE_VIDEO_PROMPT_STILLNESS_FUNCTION_MISSING','shot_id':shot_id,'creature_id':cid})
    return {'pass':not issues,'gate':'EXPERIENCE_VIDEO_PROMPT_HANDOFF_PASS','applicable':True,'shot_id':shot_id,'beat_ids':sorted(x for x in beat_ids if x),'roles':sorted(roles),'experience_gains':gains,'active_creatures':[c.get('creature_id') for c in active],'issues':issues}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--prompt',required=True); ap.add_argument('--execution-plan',required=True); ap.add_argument('--experience-plan',required=True); ap.add_argument('--creature-plan',required=True); a=ap.parse_args()
    out=lint(prompt_text(a.prompt),load(a.execution_plan),load(a.experience_plan),load(a.creature_plan)); print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
