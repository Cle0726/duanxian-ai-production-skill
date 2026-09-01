#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import yaml

LOUD={'HUSHED':'压低声音','SOFT':'轻声','NEUTRAL':'自然音量','FIRM':'坚定但不喊','RAISED':'提高音量','SHOUT':'呼喊','CALL':'向远处喊话'}
PACE={'VERY_SLOW':'非常慢','SLOW':'慢','BASELINE':'自然','QUICK':'稍快','FAST':'快','CLIPPED':'句尾迅速收断'}
PITCH={'LEVEL':'能量保持克制平稳','RISING_PRESSURE':'能量逐步上升','FALLING_ENERGY':'能量逐渐退去','SPIKE_THEN_CONTROL':'短暂泄露后立即压回','SUSPENDED':'维持未解决张力','BREAK_CRACK':'短暂失稳后恢复'}
TERM={'FALL':'句尾明确落下','RISE':'句尾真正上扬','FALL_RISE':'句尾先落后回升并保留含义','LEVEL':'句尾保持悬而未决','CLIPPED':'句尾突然收断','BREATH_RELEASED':'句尾随气息释放','SUSPENDED':'句尾故意不完成落点'}
PAUSE={'PRE_LINE_PROCESSING':'开口前先处理信息','THOUGHT_PAUSE':'思想转向处停顿','HESITATION':'犹豫处停顿','LISTENING_PAUSE':'等待对方反应','IMPACT_PROCESSING':'受到信息冲击后停顿','BREATH_PAUSE':'真实换气停顿','INTERRUPTED':'在此处被打断','POST_LINE_HOLD':'说完后留白'}
STRESS={'PRIMARY_STRESS':'重读','SECONDARY_STRESS':'次重读','DE_EMPHASIS':'故意弱读'}
TEXTURE={'BREATHINESS_UP':'气声略增加','BREATHINESS_DOWN':'气声略减少','ARTICULATION_CLEARER':'咬字更清楚','ARTICULATION_SOFTENED':'咬字更柔和','CONSONANT_ATTACK_HARDER':'辅音起音更硬','CONSONANT_ATTACK_SOFTER':'辅音起音更软','RESONANCE_NARROWER':'共鸣暂时收窄','RESONANCE_OPENER':'共鸣略打开','DRYNESS':'出现有剧情依据的干涩','STRAIN':'出现有剧情依据的紧绷','TEMPORARY_INSTABILITY':'短暂失稳后恢复'}
INTERACTION={'INTERRUPT':'允许真实被打断，不等待完整句尾','OVERLAP':'允许与对方句尾短暂重叠','QUICK_PICKUP':'紧接对方句尾快速接话','LISTENING_DELAY':'先听完并处理后再回答'}

def load(p):
    text=Path(p).read_text(encoding='utf-8')
    return json.loads(text) if Path(p).suffix.lower()=='.json' else yaml.safe_load(text)
def fp(d): return hashlib.sha256(yaml.safe_dump(d,sort_keys=True,allow_unicode=True).encode('utf-8')).hexdigest()

def compile_line(x):
    d=x['delivery']; pace=d['pace_curve']; terms=[]; parts=[]
    def add_term(t):
        if t and t not in terms:
            terms.append(t); parts.append(t)
    add_term(LOUD[d['performance_loudness']])
    add_term(f"开口{PACE[pace['entry']]}，中段{PACE[pace['mid']]}，句尾{PACE[pace['terminal']]}")
    for p in d.get('pause_map') or []:
        add_term(f"{p['position']}处{PAUSE[p['pause_type']]}")
    for st in d.get('stress_map') or []:
        add_term(f"{STRESS[st['stress_level']]}“{st['text_span']}”")
    add_term(PITCH[d['pitch_energy_contour']])
    add_term(TERM[d['terminal_intonation']])
    for z in d.get('texture_adjustments') or []:
        add_term(TEXTURE[z['adjustment']])
    mode=(x.get('interaction') or {}).get('mode')
    if mode in INTERACTION:
        add_term(INTERACTION[mode])
    visual=(x.get('body_voice_coupling') or {}).get('visual_behavior_anchor')
    if visual:
        add_term(f"声音变化与可见表演同源：{visual}")
    landing=str(d.get('landing_carryover') or '').strip()
    if landing:
        add_term(f"说完后的延续：{landing}")
    text=f"{x['speaker_prompt_label']}说：“{x['spoken_text']}”。"+'；'.join(parts)+'。'
    return text,terms

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--plan',required=True); ap.add_argument('--video-unit-id',required=True); ap.add_argument('--shot-id',action='append',default=[]); ap.add_argument('--output',required=True); ap.add_argument('--text-output'); ap.add_argument('--handoff-id',default='VOICE_HANDOFF_AUTO'); a=ap.parse_args()
    plan=load(a.plan); shotset=set(a.shot_id)
    lines=[]; text_parts=[]
    if plan.get('dialogue_required'):
        for x in plan.get('lines') or []:
            explicit_vu=x.get('video_unit_id')
            if explicit_vu:
                if explicit_vu!=a.video_unit_id: continue
            elif shotset and x.get('shot_id') not in shotset:
                continue
            compiled,terms=compile_line(x); text_parts.append(compiled)
            lines.append({'line_id':x['line_id'],'shot_id':x.get('shot_id'),'speaker_entity_id':x['speaker_entity_id'],'speaker_surface':x['speaker_prompt_label'],'spoken_text':x['spoken_text'],'compiled_direction':compiled,'required_surface_terms':terms})
    out={'schema_version':1,'skill_version':'4.5.11','voice_prompt_handoff_id':a.handoff_id,'voice_direction_plan_id':plan['voice_direction_plan_id'],'video_unit_id':a.video_unit_id,'shot_ids':sorted(shotset),'dialogue_required':bool(lines) if shotset else bool(plan.get('dialogue_required')),'lines':lines,'status':'READY' if lines else 'NOT_REQUIRED'}
    out['handoff_fingerprint']=fp(out)
    Path(a.output).write_text(yaml.safe_dump(out,sort_keys=False,allow_unicode=True),encoding='utf-8')
    if a.text_output: Path(a.text_output).write_text('\n'.join(text_parts),encoding='utf-8')
    print(json.dumps({'pass':True,'line_count':len(lines),'handoff_fingerprint':out['handoff_fingerprint']},ensure_ascii=False,indent=2))
if __name__=='__main__': main()
