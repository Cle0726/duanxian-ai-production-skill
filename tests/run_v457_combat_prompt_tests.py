#!/usr/bin/env python3
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'validators'/'video_prompt_detail_lint.py'
spec=importlib.util.spec_from_file_location('vpd',P)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

BASE='''镜头目标。起始状态。人物外观与服装。场景空间前景中景后景。道具Holder。构图。中景景别。摄影机Camera。0–3s时间轴。逐段动作启动减速。表演微表情眉眼嘴角。视线看向。左手右手肢体占用承重。物理反馈重心惯性。环境动态风雨灯。光影综合色主光环境光。声音Foley。对白与呼吸停顿。结尾状态Landing。必要限制保持。@镜头执行图 @场景色卡。'''
COMBAT='''战斗目标是保护同伴并逼迫对手退出门口。交战距离从中距进入威胁距离，再到Weapon Reach和接触距离，结束时重新拉开距离。她先读取攻击来势并完成战术判断，再Decision侧移。攻击与防御形成攻防交换：对手刺击，她闪避并拨挡后反击。Attack Lane沿门框左侧，Escape Lane沿桌边侧移。Contact Point在剑脊与对方腕部护具，Near Miss从肩外掠过。Force Direction由右前向左后，冲击沿手腕传到肩和躯干重心。Recoil后双方回弹，攻击者收招，防御者出现短暂Recovery暴露窗口。Initiative Shift由对手压制转为她取得主动权。战斗镜头保持关键接触可读，摄影机不遮挡攻击线和接触点。战斗结束状态是双方重新拉开距离，她保持先手，进入下一轮攻防。'''

def pad(s):
    # Length is not the purpose of these unit checks; satisfy density without introducing new concepts.
    filler='动作与表演按照既定时间轴连续执行，人物保持自然重量、空间站位和镜头连续性。'
    while len(m.normalize(s)) < 2500:
        s += filler
    return s

normal=pad(BASE)
r=m.lint(normal,segment_type='NON_COMBAT')
assert r['pass'], r
assert not r['combat_contract_active']

bad_combat=pad(BASE+' 战斗目标。攻击与格挡。')
r=m.lint(bad_combat,segment_type='COMBAT')
assert not r['pass'], r
assert r['combat_contract_active']
assert 'ENGAGEMENT_DISTANCE' in r['missing_combat_concepts']
assert 'FORCE_DIRECTION' in r['missing_combat_concepts']

full=pad(BASE+COMBAT)
r=m.lint(full,segment_type='COMBAT')
assert r['pass'], r
assert not r['missing_combat_concepts'], r

auto=pad(BASE+COMBAT)
r=m.lint(auto,segment_type='AUTO')
assert r['combat_contract_active'], r
assert r['pass'], r

# One isolated prohibition must not accidentally convert a normal shot into combat.
no_false=pad(BASE+'必要限制：不要出现无依据攻击行为。')
r=m.lint(no_false,segment_type='AUTO')
assert not r['combat_contract_active'], r
print('V4.5.7 combat prompt conditional tests: PASS')
