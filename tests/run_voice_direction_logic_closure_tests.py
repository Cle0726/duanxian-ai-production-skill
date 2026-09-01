#!/usr/bin/env python3
from __future__ import annotations
import copy, json, subprocess, sys, tempfile
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
PYEX=sys.executable

def run(args,expect=0):
    cp=subprocess.run(args,cwd=ROOT,text=True,capture_output=True)
    print('$',' '.join(map(str,args)))
    if cp.stdout: print(cp.stdout)
    if cp.stderr: print(cp.stderr,file=sys.stderr)
    if cp.returncode!=expect: raise AssertionError(f'expected {expect}, got {cp.returncode}')
    return cp

def ywrite(p,d): Path(p).write_text(yaml.safe_dump(d,sort_keys=False,allow_unicode=True),encoding='utf-8')
def yload(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))

def plan_doc():
    return {
      'schema_version':1,'skill_version':'4.5.7','voice_direction_plan_id':'VDP-EP1-SC1','episode_id':'EP_TEST','sequence_id':'SEQ1','scene_id':'SC1','source_performance_ref':'PERF1','source_screenplay_ref':'SCRIPT1','dialogue_required':True,
      'coverage':{'declared_dialogue_line_ids':['L1'],'important_line_ids':['L1'],'excluded_lines':[]},
      'lines':[{
        'line_id':'L1','sequence_id':'SEQ1','scene_id':'SC1','shot_id':'SH1','speaker_entity_id':'FATHER','speaker_prompt_label':'父亲','importance':'IMPORTANT','spoken_text':'我没事，你先进去。','transcript_ref':'SCRIPT1:L1','voice_identity_required':True,'voice_identity_asset_id':'VOICE_FATHER',
        'emotional_causality':{'trigger_event':'他刚意识到自己受伤但不想让家人担心','meaning_appraisal':'如果对方继续追问，他的伪装会被看穿','objective':'让对方先离开并停止追问','tactic':'用简短肯定句结束交流','subtext':'不要看出我正在撑着','affect_label':'压住疼痛后的克制泄露','arousal':'MEDIUM','control':'LEAKING'},
        'delivery':{'performance_loudness':'SOFT','pace_curve':{'entry':'QUICK','mid':'BASELINE','terminal':'CLIPPED','reason':'先抢答掩饰，随后恢复控制，句尾主动关闭交流'},'speech_phrases':[{'phrase_id':'P1','text_span':'我没事','speech_action':'先让对方停止担心','breath_required':False},{'phrase_id':'P2','text_span':'你先进去','speech_action':'把对方推离当前话题','breath_required':False}], 'pause_map':[{'position':'我没事之后','pause_type':'THOUGHT_PAUSE','duration_class':'SHORT','reason':'确认对方是否接受这个说法再给出下一步指令'}], 'stress_map':[{'text_span':'先','stress_level':'PRIMARY_STRESS','reason':'把注意力从自己身上转移到对方行动'}], 'pitch_energy_contour':'SPIKE_THEN_CONTROL','terminal_intonation':'CLIPPED','terminal_reason':'明确关闭继续追问的空间','texture_adjustments':[{'adjustment':'TEMPORARY_INSTABILITY','reason':'疼痛在第一句末短暂泄露后压回'}],'landing_carryover':'说完保持视线短暂回避，把未解决压力带入下一镜'},
        'interaction':{'mode':'NONE','target_line_id':None,'reason':'当前句不是抢话或重叠','listening_response':'先确认对方没有立刻反驳'},
        'body_voice_coupling':{'same_trigger_required':True,'visual_behavior_anchor':'第一句结束时下颌轻微收紧，视线短暂移开，与声音短暂失稳来自同一疼痛触发','coupling_note':'声音与身体都只泄露一次，不升级成明显崩溃'},
        'status':'READY_FOR_COMPILE'
      }],
      'status':'READY_FOR_COMPILE','plan_fingerprint':None
    }

def audio_manifest():
    return {'schema_version':1,'skill_version':'4.5.7','audio_asset_manifest_id':'AUD1','episode_id':'EP_TEST','status':'APPROVED','manifest_fingerprint':None,'audio_assets':[{'asset_id':'VOICE_FATHER','asset_display_name':'父亲声音身份','native_token':None,'audio_type':'VOICE_IDENTITY','authority_role':'VOICE_IDENTITY','scope':'CHARACTER','subject_entity_id':'FATHER','episode_id':'EP_TEST','sequence_id':None,'scene_id':None,'shot_id':None,'language':'zh-CN','transcript_ref':None,'reuse_key':'VOICE:FATHER','version':1,'duration_sec':8.0,'fingerprint':'voicefatherfp123456','status':'APPROVED','reference_policy':'STAGE06_ONLY','binding_status':'READY','direct_reference_eligible':False,'intended_use':['VOICE_CANON','STAGE06_EDIT']}]}

with tempfile.TemporaryDirectory() as td0:
    td=Path(td0); plan=td/'plan.yaml'; aud=td/'audio.yaml'; registry=ROOT/'tests/fixtures/asset_registry.virtual_set.valid.yaml'
    ywrite(plan,plan_doc()); ywrite(aud,audio_manifest())
    print('SECTION_1_SCHEMA_AND_PLAN')
    run([PYEX,'validators/state_schema_lint.py','state/voice_direction_plan.schema.yaml',str(plan),'--json'])
    run([PYEX,'validators/voice_direction_plan_lint.py','--plan',str(plan),'--phase','planning'])
    run([PYEX,'validators/voice_direction_plan_lint.py','--plan',str(plan),'--phase','pre_video','--audio-manifest',str(aud),'--registry',str(registry)])

    print('SECTION_2_UNDERDIRECTED_EXPECTED_FAIL')
    bad=plan_doc(); bad['lines'][0]['delivery']['pause_map']=[]; bad['lines'][0]['delivery']['stress_map']=[]; bad['lines'][0]['delivery']['pitch_energy_contour']='LEVEL'; bad['lines'][0]['delivery']['texture_adjustments']=[]
    badp=td/'bad_plan.yaml'; ywrite(badp,bad)
    cp=run([PYEX,'validators/voice_direction_plan_lint.py','--plan',str(badp),'--phase','planning'],expect=2)
    assert 'VOICE_PROSODY_UNDERDIRECTED' in cp.stdout

    print('SECTION_3_IDENTITY_MISMATCH_EXPECTED_FAIL')
    badid=plan_doc(); badid['lines'][0]['speaker_entity_id']='OTHER'; badidp=td/'bad_identity.yaml'; ywrite(badidp,badid)
    cp=run([PYEX,'validators/voice_direction_plan_lint.py','--plan',str(badidp),'--phase','pre_video','--audio-manifest',str(aud),'--registry',str(registry)],expect=2)
    assert 'VOICE_IDENTITY_SUBJECT_MISMATCH' in cp.stdout

    print('SECTION_4_COMPILE_PROMPT_HANDOFF')
    hand=td/'handoff.yaml'; voice_text=td/'voice.txt'
    run([PYEX,'tools/voice_direction_prompt_compiler.py','--plan',str(plan),'--video-unit-id','VU1','--shot-id','SH1','--output',str(hand),'--text-output',str(voice_text),'--handoff-id','VPH1'])
    run([PYEX,'validators/state_schema_lint.py','state/voice_prompt_handoff.schema.yaml',str(hand),'--json'])
    run([PYEX,'validators/prompt_surface_lint.py',str(voice_text)])
    run([PYEX,'validators/voice_prompt_handoff_lint.py','--plan',str(plan),'--handoff',str(hand),'--prompt',str(voice_text)])
    text=voice_text.read_text(encoding='utf-8'); assert '父亲说' in text and '句尾突然收断' in text and '我没事，你先进去。' in text

    print('SECTION_5_TERMINAL_ANCHOR_DROP_EXPECTED_FAIL')
    broken=td/'broken_voice.txt'; broken.write_text(text.replace('句尾突然收断',''),encoding='utf-8')
    cp=run([PYEX,'validators/voice_prompt_handoff_lint.py','--plan',str(plan),'--handoff',str(hand),'--prompt',str(broken)],expect=2)
    assert 'VOICE_PROMPT_TERMINAL_ANCHOR_MISSING' in cp.stdout

    print('SECTION_6_TTS_HANDOFF')
    timing=td/'timing.yaml'; ywrite(timing,{'lines':[{'line_id':'L1','start_sec':1.2,'end_sec':4.6}]})
    tts=td/'tts.yaml'
    run([PYEX,'tools/voice_tts_handoff_builder.py','--plan',str(plan),'--timings',str(timing),'--picture-lock-ref','MASTER_EDIT_V1','--picture-lock-fingerprint','picturelock1234567890','--output',str(tts),'--handoff-id','VTTS1'])
    run([PYEX,'validators/state_schema_lint.py','state/voice_tts_handoff.schema.yaml',str(tts),'--json'])
    run([PYEX,'validators/voice_tts_handoff_lint.py','--plan',str(plan),'--handoff',str(tts)])

    print('SECTION_7_TTS_INTENT_DRIFT_EXPECTED_FAIL')
    badtts=yload(tts); badtts['lines'][0]['terminal_intonation']='RISE'; badttsp=td/'bad_tts.yaml'; ywrite(badttsp,badtts)
    cp=run([PYEX,'validators/voice_tts_handoff_lint.py','--plan',str(plan),'--handoff',str(badttsp)],expect=2)
    assert 'VOICE_TTS_INTENT_DRIFT' in cp.stdout

    print('SECTION_8_NO_DIALOGUE_VIDEO_UNIT_PASS')
    hand2=td/'handoff_no_dialogue.yaml'; text2=td/'voice_none.txt'
    run([PYEX,'tools/voice_direction_prompt_compiler.py','--plan',str(plan),'--video-unit-id','VU2','--shot-id','SH_NO_DIALOGUE','--output',str(hand2),'--text-output',str(text2),'--handoff-id','VPH2'])
    run([PYEX,'validators/voice_prompt_handoff_lint.py','--plan',str(plan),'--handoff',str(hand2),'--prompt',str(text2)])

print('SECTION_9_CONTROLLER_WIRING')
route=yaml.safe_load((ROOT/'controller/route_registry.yaml').read_text(encoding='utf-8')); wf=yaml.safe_load((ROOT/'controller/workflow_state_machine.yaml').read_text(encoding='utf-8')); gates=yaml.safe_load((ROOT/'controller/gate_producer_registry.yaml').read_text(encoding='utf-8')); auth=yaml.safe_load((ROOT/'controller/authority_registry.yaml').read_text(encoding='utf-8'))
r2=route['routes']['STAGE_02C_PRODUCTION_TRANSLATION']; r3f=route['routes']['EPISODE_ASSET_FREEZE']; r5=route['routes']['STAGE_05_VIDEO']; r6=route['routes']['STAGE_06_POST']
assert 'VOICE_DIRECTION_PLAN' in r2['produces_structured_artifacts']
assert 'VOICE_DIRECTION_PLAN' in r3f['structured_inputs']
assert any(x.get('validator')=='validators/voice_direction_plan_lint.py' and x.get('produces_gate')=='REQUIRED_VOICE_IDENTITY_ASSETS_RESOLVED' for x in r3f['validator_invocations'])
assert 'VOICE_DIRECTION_PLAN' in r5['structured_inputs']
assert 'tools/voice_direction_prompt_compiler.py' in r5['deterministic_tools']
assert 'validators/voice_prompt_handoff_lint.py' in r5['validators']
assert 'VOICE_DIRECTION_PLAN' in r6['structured_inputs']
assert 'tools/voice_tts_handoff_builder.py' in r6['deterministic_tools']
assert 'validators/voice_tts_handoff_lint.py' in r6['validators']
t09=next(x for x in wf['transitions'] if x['id']=='T09_BREAKDOWN_READY'); t12=next(x for x in wf['transitions'] if x['id']=='T12_SPATIAL_RECONCILE'); t23=next(x for x in wf['transitions'] if x['id']=='T23B_VIDEO_READY'); t29=next(x for x in wf['transitions'] if x['id']=='T29_MASTER')
assert 'VOICE_DIRECTION_PLAN_DERIVED' in t09['requires']
assert 'REQUIRED_VOICE_IDENTITY_ASSETS_RESOLVED' in t12['requires']
assert 'VOICE_DIRECTION_PLAN_PASS' in t23['requires'] and 'VOICE_DIRECTION_PROMPT_HANDOFF_PASS' in t23['requires']
assert 'VOICE_TTS_HANDOFF_PASS' in t29['requires']
for g in ['VOICE_DIRECTION_PLAN_DERIVED','REQUIRED_VOICE_IDENTITY_ASSETS_RESOLVED','VOICE_DIRECTION_PLAN_PASS','VOICE_DIRECTION_PROMPT_HANDOFF_PASS','VOICE_TTS_HANDOFF_PASS']:
    assert g in gates['producers']
for a in ['voice_direction_plan','voice_prompt_handoff','voice_tts_handoff']:
    assert a in auth['authorities']
print('VOICE DIRECTION LOGIC CLOSURE TESTS PASSED')
