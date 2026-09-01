#!/usr/bin/env python3
from __future__ import annotations
import copy, subprocess, sys, tempfile
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]; PYEX=sys.executable

def run(args,expect=0):
    cp=subprocess.run(args,cwd=ROOT,text=True,capture_output=True)
    if cp.returncode!=expect:
        print(cp.stdout); print(cp.stderr,file=sys.stderr)
        raise AssertionError(f'expected {expect}, got {cp.returncode}: {args}')
    return cp

def ywrite(p,d): Path(p).write_text(yaml.safe_dump(d,sort_keys=False,allow_unicode=True),encoding='utf-8')
def yload(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))

def line(lid='L1',shot='SH1',importance='IMPORTANT',text='我没事，你先进去。'):
    return {
      'line_id':lid,'sequence_id':'SEQ1','scene_id':'SC1','shot_id':shot,'speaker_entity_id':'FATHER','speaker_prompt_label':'父亲','importance':importance,'spoken_text':text,'transcript_ref':f'SCRIPT:{lid}','voice_identity_required':False,'voice_identity_asset_id':None,
      'emotional_causality':{'trigger_event':'对方继续追问','meaning_appraisal':'再解释会暴露真实状态','objective':'结束追问','tactic':'短句关闭交流','subtext':'不要看出来','affect_label':'克制泄露','arousal':'MEDIUM','control':'LEAKING'},
      'delivery':{'performance_loudness':'SOFT','pace_curve':{'entry':'QUICK','mid':'BASELINE','terminal':'CLIPPED','reason':'先抢答再收住'},'speech_phrases':[{'phrase_id':f'{lid}P1','text_span':'我没事','speech_action':'安抚','breath_required':False}], 'pause_map':[{'position':'我没事之后','pause_type':'THOUGHT_PAUSE','duration_class':'SHORT','reason':'确认对方反应'}], 'stress_map':[{'text_span':'先','stress_level':'PRIMARY_STRESS','reason':'转移注意力'}], 'pitch_energy_contour':'SPIKE_THEN_CONTROL','terminal_intonation':'CLIPPED','terminal_reason':'关闭追问空间','texture_adjustments':[{'adjustment':'TEMPORARY_INSTABILITY','reason':'疼痛短暂泄露'}],'landing_carryover':'保持回避，把压力带入下一镜'},
      'interaction':{'mode':'NONE','target_line_id':None,'reason':'单句直接回应','listening_response':'确认对方反应'},
      'body_voice_coupling':{'same_trigger_required':True,'visual_behavior_anchor':'下颌收紧并短暂移开视线','coupling_note':'与声音失稳同源'},
      'status':'READY_FOR_COMPILE'
    }

def plan(lines=None,declared=None,important=None,excluded=None,dialogue=True,status=None):
    lines=lines if lines is not None else [line()]
    return {'schema_version':1,'skill_version':'4.5.7','voice_direction_plan_id':'VDP-AUDIT','episode_id':'EP1','sequence_id':'SEQ1','scene_id':'SC1','source_performance_ref':'PERF','source_screenplay_ref':'SCRIPT','dialogue_required':dialogue,
      'coverage':{'declared_dialogue_line_ids':declared if declared is not None else [x['line_id'] for x in lines], 'important_line_ids':important if important is not None else [x['line_id'] for x in lines if x['importance'] in {'IMPORTANT','CRITICAL'}], 'excluded_lines':excluded or []},
      'lines':lines,'status':status or ('READY_FOR_COMPILE' if dialogue else 'NOT_REQUIRED'),'plan_fingerprint':None}

def assert_code(cp,code):
    assert code in cp.stdout, (code,cp.stdout)

with tempfile.TemporaryDirectory() as td0:
    td=Path(td0)
    print('SECTION_A_FALSE_NOT_REQUIRED_CANNOT_HIDE_DECLARED_DIALOGUE')
    p=td/'a.yaml'; ywrite(p,plan(lines=[],declared=['L1'],important=[],dialogue=False))
    cp=run([PYEX,'validators/voice_direction_plan_lint.py','--plan',str(p),'--phase','planning'],2); assert_code(cp,'VOICE_DIRECTION_FALSE_NOT_REQUIRED_WITH_DECLARED_DIALOGUE')

    print('SECTION_B_PLAN_COVERAGE_BIDIRECTIONAL')
    p=td/'b.yaml'; ywrite(p,plan(lines=[line('L1'),line('L2','SH2','NORMAL','你进去。')],declared=['L1'],important=['L1']))
    cp=run([PYEX,'validators/voice_direction_plan_lint.py','--plan',str(p),'--phase','planning'],2); assert_code(cp,'VOICE_DIRECTION_UNDECLARED_LINE')
    p=td/'b2.yaml'; ywrite(p,plan(excluded=[{'line_id':'L1','reason':'NO_VOICE_EXECUTION_REQUIRED','note':'bad overlap'}]))
    cp=run([PYEX,'validators/voice_direction_plan_lint.py','--plan',str(p),'--phase','planning'],2); assert_code(cp,'VOICE_DIRECTION_EXCLUDED_LINE_PLANNED')

    print('SECTION_C_READY_PLAN_CANNOT_CONTAIN_UNREADY_LINE')
    d=plan(); d['lines'][0]['status']='PLANNED'; p=td/'c.yaml'; ywrite(p,d)
    cp=run([PYEX,'validators/voice_direction_plan_lint.py','--plan',str(p),'--phase','planning'],2); assert_code(cp,'VOICE_DIRECTION_LINE_NOT_READY')

    print('SECTION_D_COMPILER_SURFACES_ALL_EXPLICIT_CONTROLS')
    d=plan(); x=d['lines'][0]
    x['delivery']['pause_map'].append({'position':'你先进去之前','pause_type':'HESITATION','duration_class':'MICRO','reason':'短暂压住疼痛'})
    x['delivery']['stress_map'].append({'text_span':'进去','stress_level':'SECONDARY_STRESS','reason':'把行动指令说清'})
    x['delivery']['texture_adjustments'].append({'adjustment':'ARTICULATION_CLEARER','reason':'恢复控制'})
    p=td/'d.yaml'; ywrite(p,d); h=td/'d_hand.yaml'; txt=td/'d.txt'
    run([PYEX,'tools/voice_direction_prompt_compiler.py','--plan',str(p),'--video-unit-id','VU1','--shot-id','SH1','--output',str(h),'--text-output',str(txt)])
    text=txt.read_text(encoding='utf-8')
    for term in ['我没事之后处思想转向处停顿','你先进去之前处犹豫处停顿','重读“先”','次重读“进去”','短暂失稳后恢复','咬字更清楚','声音变化与可见表演同源：下颌收紧并短暂移开视线','说完后的延续：保持回避，把压力带入下一镜']:
        assert term in text, term
    run([PYEX,'validators/voice_prompt_handoff_lint.py','--plan',str(p),'--handoff',str(h),'--prompt',str(txt)])

    print('SECTION_E_PROMPT_HANDOFF_CANNOT_DROP_EXPECTED_LINE')
    d=plan(lines=[line('L1'),line('L2','SH2','NORMAL','你先进去。')],declared=['L1','L2'],important=['L1'])
    p=td/'e.yaml'; ywrite(p,d); h=td/'e_hand.yaml'; txt=td/'e.txt'
    run([PYEX,'tools/voice_direction_prompt_compiler.py','--plan',str(p),'--video-unit-id','VUALL','--output',str(h),'--text-output',str(txt)])
    hd=yload(h); hd['lines']=hd['lines'][:1]; badh=td/'e_bad_hand.yaml'; ywrite(badh,hd)
    cp=run([PYEX,'validators/voice_prompt_handoff_lint.py','--plan',str(p),'--handoff',str(badh),'--prompt',str(txt)],2); assert_code(cp,'VOICE_PROMPT_LINE_COVERAGE_GAP')

    print('SECTION_F_NOT_REQUIRED_HANDOFF_MUST_BE_EMPTY')
    d=plan(lines=[],declared=[],important=[],dialogue=False); p=td/'f.yaml'; ywrite(p,d)
    bad={'schema_version':1,'skill_version':'4.5.7','voice_prompt_handoff_id':'H','voice_direction_plan_id':'VDP-AUDIT','video_unit_id':'VU','shot_ids':[],'dialogue_required':False,'lines':[{'line_id':'Lx','shot_id':'SH','speaker_entity_id':'X','speaker_surface':'X','spoken_text':'x','compiled_direction':'x','required_surface_terms':['x']}],'status':'NOT_REQUIRED','handoff_fingerprint':None}; h=td/'f_hand.yaml'; ywrite(h,bad); txt=td/'f.txt'; txt.write_text('x',encoding='utf-8')
    cp=run([PYEX,'validators/voice_prompt_handoff_lint.py','--plan',str(p),'--handoff',str(h),'--prompt',str(txt)],2); assert_code(cp,'VOICE_PROMPT_UNEXPECTED_DIALOGUE_HANDOFF')

    print('SECTION_G_TTS_EXACT_CONTENT_AND_PICTURE_LOCK')
    d=plan(); p=td/'g.yaml'; ywrite(p,d); timings=td/'times.yaml'; ywrite(timings,{'lines':[{'line_id':'L1','start_sec':1.0,'end_sec':4.0}]}); tts=td/'tts.yaml'
    run([PYEX,'tools/voice_tts_handoff_builder.py','--plan',str(p),'--timings',str(timings),'--picture-lock-ref','PL1','--picture-lock-fingerprint','1234567890abcdef','--output',str(tts)])
    run([PYEX,'validators/voice_tts_handoff_lint.py','--plan',str(p),'--handoff',str(tts)])
    td1=yload(tts); td1['lines'][0]['final_spoken_text']='被篡改'; bad=td/'tts_text.yaml'; ywrite(bad,td1)
    cp=run([PYEX,'validators/voice_tts_handoff_lint.py','--plan',str(p),'--handoff',str(bad)],2); assert_code(cp,'VOICE_TTS_TEXT_DRIFT')
    td2=yload(tts); td2['lines'][0]['texture_adjustments']=[]; bad=td/'tts_texture.yaml'; ywrite(bad,td2)
    cp=run([PYEX,'validators/voice_tts_handoff_lint.py','--plan',str(p),'--handoff',str(bad)],2); assert_code(cp,'VOICE_TTS_TEXTURE_DRIFT')
    td3=yload(tts); td3['picture_lock_fingerprint']=''; bad=td/'tts_fp.yaml'; ywrite(bad,td3)
    cp=run([PYEX,'validators/voice_tts_handoff_lint.py','--plan',str(p),'--handoff',str(bad)],2); assert_code(cp,'VOICE_TTS_PICTURE_LOCK_FINGERPRINT_REQUIRED')

    print('SECTION_H_BACKGROUND_PLANNED_LINE_IS_NOT_SILENTLY_DROPPED')
    bg=line('BG1','SHBG','BACKGROUND','后面有人喊了一声。'); bg['delivery']['pitch_energy_contour']='LEVEL'; bg['delivery']['texture_adjustments']=[]
    d=plan(lines=[bg],declared=['BG1'],important=[]); p=td/'h.yaml'; ywrite(p,d); timings=td/'h_times.yaml'; ywrite(timings,{'lines':[{'line_id':'BG1','start_sec':0.2,'end_sec':1.5}]}); tts=td/'h_tts.yaml'
    run([PYEX,'tools/voice_tts_handoff_builder.py','--plan',str(p),'--timings',str(timings),'--picture-lock-ref','PL2','--picture-lock-fingerprint','abcdef1234567890','--output',str(tts)])
    assert len(yload(tts)['lines'])==1
    run([PYEX,'validators/voice_tts_handoff_lint.py','--plan',str(p),'--handoff',str(tts)])


    print('SECTION_I_SEQUENCE_VO_CAN_BIND_VIDEO_UNIT_WITHOUT_FAKE_SHOT')
    vo=line('VO1',None,'IMPORTANT','夜色终于安静下来。'); vo['video_unit_id']='VU-VO'; vo['speaker_entity_id']='NARRATOR'; vo['speaker_prompt_label']='旁白'; vo['delivery']['stress_map']=[{'text_span':'终于','stress_level':'PRIMARY_STRESS','reason':'强调状态转折'}]
    d=plan(lines=[vo],declared=['VO1'],important=['VO1']); p=td/'i.yaml'; ywrite(p,d); h=td/'i_hand.yaml'; txt=td/'i.txt'
    run([PYEX,'tools/voice_direction_prompt_compiler.py','--plan',str(p),'--video-unit-id','VU-VO','--output',str(h),'--text-output',str(txt)])
    assert len(yload(h)['lines'])==1
    run([PYEX,'validators/voice_prompt_handoff_lint.py','--plan',str(p),'--handoff',str(h),'--prompt',str(txt)])
    h2=td/'i_other.yaml'; txt2=td/'i_other.txt'; run([PYEX,'tools/voice_direction_prompt_compiler.py','--plan',str(p),'--video-unit-id','VU-OTHER','--output',str(h2),'--text-output',str(txt2)])
    assert yload(h2)['status']=='NOT_REQUIRED' and not yload(h2)['lines']

print('VOICE DIRECTION ADVERSARIAL CLOSURE TESTS PASSED')
