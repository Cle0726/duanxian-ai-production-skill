#!/usr/bin/env python3
import argparse, json, re, sys

REQUIRED_CONCEPTS = {
    'TARGET': [r'镜头目标|叙事目标|情绪目标'],
    'ENTRY_STATE': [r'起始状态|起始画面|t\s*=\s*0'],
    'HUMAN_WARDROBE': [r'人物.*(?:服装|外观)|服装|外观'],
    'SCENE_SPACE': [r'场景空间|前景|中景|后景|FG|MG|BG|入口|出口|Anchor'],
    'PROP_STATE': [r'道具|Holder|持有|手持|握住|放置'],
    'COMPOSITION': [r'构图|画面占比|前中后景'],
    'SHOT_SIZE': [r'景别|Shot Size|特写|近景|中景|全景'],
    'CAMERA': [r'摄影机|Camera|机位|焦点|Focus|焦段|镜头运动'],
    'TIMELINE': [r'\d+(?:\.\d+)?\s*[–\-~至]\s*\d+(?:\.\d+)?\s*s|时间轴'],
    'SEGMENTED_ACTION': [r'逐段动作|动作过程|启动|加速|减速|停稳|转身|抬手|迈步'],
    'PERFORMANCE': [r'表演|微表情|眉|眼睑|嘴角|下颌|吞咽|迟疑|情绪泄露'],
    'EYELINE': [r'视线|眼神|注视|看向|移开视线|Eyeline'],
    'LIMB_OCCUPANCY': [r'肢体占用|左手|右手|左脚|右脚|承重|支撑|换手'],
    'PHYSICAL_FEEDBACK': [r'物理反馈|重心|惯性|碰撞|接触|反作用|布料|头发|余摆'],
    'ENV_DYNAMICS': [r'环境动态|雨|风|烟|灯|背景生命|门窗|车辆'],
    'LIGHT_COLOR': [r'光影|综合色|冷暖|主光|辅光|环境光|明暗'],
    'SOUND': [r'声音|环境声|Foley|拟音|BGM|钟声|脚步声'],
    'DIALOGUE_BREATH': [r'对白|台词|呼吸|喘气|停顿|重音|语速'],
    'ENDING_STATE': [r'结尾状态|结束状态|落点|Landing|最后一刻'],
    'NECESSARY_RESTRICTION': [r'必要限制|禁止|不出现|避免|保持'],
    'ASSET_MENTION': [r'@[\w\u4e00-\u9fff\-]+'],
}

# Combat checks are conditional. They supplement the 20 universal Stage 05 controls;
# they never replace performance, camera, spatial, physics, color or audio requirements.
COMBAT_REQUIRED_CONCEPTS = {
    'COMBAT_OBJECTIVE': [r'战斗目标|战术目标|Combat\s*Objective|Micro[- ]?objective|胜利条件|拖延目标|撤离目标|保护目标'],
    'ENGAGEMENT_DISTANCE': [r'Engagement\s*Distance|交战距离|距离梯度|威胁距离|武器有效距离|Weapon\s*Reach|接触距离|脱离距离'],
    'READ_DECISION': [r'Read\s*(?:→|->).*Decision|读取(?:攻击|威胁)|判断(?:攻击|威胁|来势)|预判|战术判断|防御判断|决策'],
    'ATTACK_DEFENSE_EXCHANGE': [r'攻防|攻击.*(?:防御|格挡|闪避|拨挡|截击)|(?:格挡|闪避|拨挡|截击).*攻击|Attack.*Defense|Defense\s*Choice|反击|Counter'],
    'ATTACK_ESCAPE_LANE': [r'Attack\s*Lane|攻击线|进攻路径|Escape\s*Lane|撤离线|闪避路径|侧移路径'],
    'CONTACT_NEAR_MISS': [r'Contact\s*Point|接触点|命中点|Near\s*Miss|险些命中|擦过|掠过|格挡接触'],
    'FORCE_DIRECTION': [r'Force\s*Direction|受力方向|力的方向|冲击方向|传力方向'],
    'RECOIL_RECOVERY': [r'Recoil|反冲|回弹|Recovery|收招|回收动作|恢复窗口|暴露窗口|动作余势'],
    'INITIATIVE_SHIFT': [r'Initiative\s*Shift|主动权|节奏权|攻守转换|先手.*转换|压制权'],
    'COMBAT_CAMERA_READ': [r'Contact\s*Read|接触读镜头|战斗镜头|关键接触.*(?:看清|可读)|摄影机.*(?:攻击线|接触点|动作方向)|Camera.*(?:contact|attack\s*lane)'],
    'EXIT_COMBAT_STATE': [r'New\s*Combat\s*State|Exit\s*Combat\s*State|战斗结束状态|新的战斗状态|脱离(?:交战|距离)|收势|重新拉开距离|下一轮攻防'],
}

COMBAT_SIGNAL_GROUPS = [
    [r'战斗|Combat\b|Combat\s*Exchange'],
    [r'攻击|进攻|挥砍|挥剑|刺击|拳击|踢击|冲刺攻击|Attack\b|Threat\b'],
    [r'格挡|闪避|拨挡|截击|防御|反击|Defense\b|Evade\b|Counter\b'],
    [r'命中|接触点|Contact\s*Point|Near\s*Miss|险些命中|受击'],
    [r'主动权|Initiative|Attack\s*Lane|Weapon\s*Reach|武器有效距离'],
]

def normalize(text):
    # Count model-facing content, excluding code-fence marks and whitespace only.
    text=re.sub(r'```[^\n]*', '', text)
    text=text.replace('```','')
    return re.sub(r'\s+','',text)

def detect_combat(text):
    # Explicit combat labels are decisive. Otherwise require evidence from at least
    # two distinct combat signal groups to avoid triggering on a single negative word.
    if re.search(r'战斗执行控制|战斗目标|Combat\s*Objective|SEGMENT_TYPE\s*[:=]\s*COMBAT', text, re.I):
        return True
    groups=0
    for pats in COMBAT_SIGNAL_GROUPS:
        if any(re.search(p,text,re.I|re.M) for p in pats):
            groups += 1
    return groups >= 2

def _missing(text, concepts):
    missing=[]
    for name,pats in concepts.items():
        if not any(re.search(p,text,re.I|re.M) for p in pats):
            missing.append(name)
    return missing

def lint(text, min_chars=0, max_chars=None, segment_type='AUTO'):
    n=len(normalize(text))
    missing=_missing(text, REQUIRED_CONCEPTS)
    st=(segment_type or 'AUTO').upper()
    combat_active = st == 'COMBAT' or (st == 'AUTO' and detect_combat(text))
    combat_missing = _missing(text, COMBAT_REQUIRED_CONCEPTS) if combat_active else []
    return {
        'pass': not missing and not combat_missing,
        'content_char_count': n,
        'prompt_length_ceiling': None,
        'length_policy': 'COMPLETENESS_DRIVEN_NO_SKILL_CHAR_LIMIT',
        'segment_type_requested': st,
        'combat_contract_active': combat_active,
        'missing_concepts': missing,
        'missing_combat_concepts': combat_missing,
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('file', nargs='?')
    ap.add_argument('--min-chars', type=int, default=0, help='legacy compatibility only; Source Master Prompt length is not hard-gated by character count')
    ap.add_argument('--max-chars', type=int, default=None, help='legacy compatibility only; ignored for Source Master Prompt because PROMPT_LENGTH_CEILING = NONE')
    ap.add_argument('--segment-type', choices=['AUTO','COMBAT','NON_COMBAT'], default='AUTO')
    a=ap.parse_args()
    text=open(a.file,encoding='utf-8').read() if a.file else sys.stdin.read()
    out=lint(text,a.min_chars,a.max_chars,a.segment_type)
    print(json.dumps(out,ensure_ascii=False,indent=2))
    raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
