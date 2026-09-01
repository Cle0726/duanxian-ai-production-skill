#!/usr/bin/env python3
from __future__ import annotations
import copy, subprocess, sys, tempfile
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parent.parent
PY=sys.executable

def run(cmd, expect=0):
    cp=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
    print(cp.stdout)
    if cp.stderr: print(cp.stderr)
    if cp.returncode!=expect: raise AssertionError(f'expected {expect}, got {cp.returncode}: {cmd}')
    return cp

def base(duration):
    return {'schema_version':1,'skill_version':'4.5.7','execution_plan_id':'EP1','video_unit_id':'VU1','status':'FROZEN_FOR_COMPILE','video_execution_plan_pass':True,'duration_sec':duration,
    'source_fingerprints':{'director':'d','storyboard':'s','shot_execution':'x','scene_color':'c','world_state':'w'},'execution_plan_fingerprint':'f'*16,
    'reference_integrity':{'conflict_count':0,'conflicts':[]},'spatial_blocking':{'conflict_count':0,'conflicts':[]},'body_prop_occupancy':{'conflict_count':0,'conflicts':[]},'timing':{'fits':True},
    'windows':[{'id':'W1','start':0,'end':duration,'primary_action':'continuous action','performance_required':False,'dominant_camera_moves':1,'camera':{'landing':'stable'}}],
    'ending_state':{'landing':'stable end'},'assembly_order':'CHRONOLOGICAL_CAUSAL','storyboard_handoff':{'source_storyboard_asset_ids':['SB1'],'items':[]}}

with tempfile.TemporaryDirectory() as td:
    td=Path(td)
    # <=15: no question required
    p=base(15.0); f=td/'15.yaml'; f.write_text(yaml.safe_dump(p,sort_keys=False),encoding='utf-8')
    run([PY,'validators/video_quota_confirmation_lint.py','--execution-plan',str(f)],0)
    # >15: missing confirmation must fail
    p=base(15.1); f2=td/'15_1_missing.yaml'; f2.write_text(yaml.safe_dump(p,sort_keys=False),encoding='utf-8')
    run([PY,'validators/video_quota_confirmation_lint.py','--execution-plan',str(f2)],2)
    # >15: explicit user HAS_QUOTA passes
    p['long_video_quota_confirmation']={'threshold_sec':15,'question_asked':True,'user_response':'HAS_QUOTA','confirmed_by':'USER','confirmation_ref':'USER_CONFIRM_001'}
    f3=td/'15_1_yes.yaml'; f3.write_text(yaml.safe_dump(p,sort_keys=False),encoding='utf-8')
    run([PY,'validators/video_quota_confirmation_lint.py','--execution-plan',str(f3)],0)
    # arbitrary longer duration also passes when confirmed: proves 15s is not a ceiling.
    p=base(60.0); p['long_video_quota_confirmation']={'threshold_sec':15,'question_asked':True,'user_response':'HAS_QUOTA','confirmed_by':'USER','confirmation_ref':'USER_CONFIRM_060'}
    f4=td/'60_yes.yaml'; f4.write_text(yaml.safe_dump(p,sort_keys=False),encoding='utf-8')
    run([PY,'validators/video_quota_confirmation_lint.py','--execution-plan',str(f4)],0)

    # Final Generation Job anti-bypass: >15s without confirmation must fail even if prompt/job bindings are otherwise current.
    prompt_file=td/'prompt.txt'; prompt_file.write_text('镜头目标 起始状态 时间轴 结尾状态',encoding='utf-8')
    import hashlib
    pf=hashlib.sha256(prompt_file.read_text(encoding='utf-8').encode('utf-8')).hexdigest()
    ep=base(16.0); epf=td/'ep16.yaml'; epf.write_text(yaml.safe_dump(ep,sort_keys=False),encoding='utf-8')
    pa={'status':'VALID','prompt_ref':str(prompt_file),'prompt_fingerprint':pf,'execution_plan_ref':str(epf),'execution_plan_fingerprint':ep['execution_plan_fingerprint'],'video_unit_id':'VU1','voice_handoff_pass':True,'voice_direction_plan_id':'VDP_NOT_REQUIRED','voice_prompt_handoff_id':'VPH_NOT_REQUIRED','voice_prompt_handoff_fingerprint':'n'*64}
    job={'media_kind':'VIDEO','prompt_ref':str(prompt_file),'prompt_fingerprint':pf,'execution_plan_ref':str(epf),'execution_plan_fingerprint':ep['execution_plan_fingerprint'],'video_unit_id':'VU1','required_bindings':[]}
    paf=td/'pa.yaml'; jf=td/'job.yaml'; paf.write_text(yaml.safe_dump(pa,sort_keys=False),encoding='utf-8'); jf.write_text(yaml.safe_dump(job,sort_keys=False),encoding='utf-8')
    run([PY,'validators/video_generation_job_prompt_lint.py','--job',str(jf),'--prompt-artifact',str(paf),'--execution-plan',str(epf)],2)
    ep['long_video_quota_confirmation']={'threshold_sec':15,'question_asked':True,'user_response':'HAS_QUOTA','confirmed_by':'USER','confirmation_ref':'USER_CONFIRM_016'}
    epf.write_text(yaml.safe_dump(ep,sort_keys=False),encoding='utf-8')
    run([PY,'validators/video_generation_job_prompt_lint.py','--job',str(jf),'--prompt-artifact',str(paf),'--execution-plan',str(epf)],0)

# A very long Source Master Prompt must not fail merely for exceeding the historical 3000-char range.
import importlib.util
spec=importlib.util.spec_from_file_location('vpd',ROOT/'validators/video_prompt_detail_lint.py'); vpd=importlib.util.module_from_spec(spec); spec.loader.exec_module(vpd)
base_prompt='''镜头目标。起始状态t=0。人物外观与服装。场景空间前景中景后景入口出口Anchor。道具Holder。构图。中景景别。摄影机Camera。0–20s时间轴。逐段动作启动减速停稳。表演微表情眉眼嘴角。视线看向。左手右手肢体占用承重。物理反馈重心惯性。环境动态风雨灯。光影综合色主光环境光。声音Foley。对白与呼吸停顿。结尾状态Landing。必要限制保持。@镜头执行图。'''
long_prompt=base_prompt + ('动作、空间、摄影机、物理和声音继续按既定时间轴保持因果一致。'*220)
r=vpd.lint(long_prompt,segment_type='NON_COMBAT')
assert r['pass'] and r['content_char_count']>5000 and r['prompt_length_ceiling'] is None, r

# Prompt authority must explicitly be unbounded and old target range must be gone from active authorities.
for fn in ['SKILL.md','README.md','templates/video_prompt_template.md','templates/prompt_compiler.md','templates/prompt_semantic_deduplication_engine.md']:
    text=(ROOT/fn).read_text(encoding='utf-8')
    assert 'PROMPT_LENGTH_CEILING = NONE' in text, fn
    assert '2500–3000' not in text, fn
print('PROMPT UNBOUNDED + LONG VIDEO QUOTA TESTS PASS')
