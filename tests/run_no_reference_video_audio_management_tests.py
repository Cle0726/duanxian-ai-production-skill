#!/usr/bin/env python3
from __future__ import annotations
import subprocess, sys, tempfile
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parent.parent; PY=sys.executable

def run(cmd,expect=0):
    cp=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
    print(cp.stdout)
    if cp.stderr: print(cp.stderr)
    if cp.returncode!=expect: raise AssertionError((cmd,cp.returncode,expect))
    return cp

def ywrite(p,d): Path(p).write_text(yaml.safe_dump(d,sort_keys=False,allow_unicode=True),encoding='utf-8')

print('SECTION_1_AUDIO_MANIFEST_SCHEMA_AND_LINT')
with tempfile.TemporaryDirectory() as td:
    td=Path(td)
    registry={'schema_version':7,'skill_version':'4.5.7','assets':[
      {'asset_id':'SHOT_EXEC','asset_display_name':'SH执行帧','native_token':'@SH执行帧','asset_type':'VIDEO_SHOT_EXECUTION_FRAME','media_kind':'IMAGE','status':'APPROVED_VIDEO_CONDITIONING','authority_role':'PRIMARY_VISUAL_CONDITIONING','scene_color_authority_id':'COLOR_SC','video_usage':{'direct_input_allowed':True,'primary_visual_eligible':True}},
      {'asset_id':'COLOR_SC','asset_display_name':'场景色卡','native_token':'@场景色卡','asset_type':'SCENE_COLOR_CARD','media_kind':'IMAGE','status':'APPROVED','authority_role':'COLOR_AUTHORITY','scene_id':'SC1','video_usage':{'direct_input_allowed':True,'primary_visual_eligible':False}},
      {'asset_id':'AUD_VOICE','asset_display_name':'艾琳声线母带','native_token':'@艾琳声线母带','asset_type':'VOICE_IDENTITY_ASSET','media_kind':'AUDIO','status':'APPROVED','authority_role':'VOICE_IDENTITY','subject_entity_id':'CHAR_ELIN','video_usage':{'direct_input_allowed':True,'primary_visual_eligible':False}},
      {'asset_id':'VID_MOTION','asset_display_name':'动作参考视频','native_token':'@动作参考视频','asset_type':'MOTION_REFERENCE_VIDEO','media_kind':'VIDEO','status':'APPROVED','authority_role':'MOTION_REFERENCE','video_usage':{'direct_input_allowed':True,'primary_visual_eligible':False}},
    ]}
    reg=td/'registry.yaml'; ywrite(reg,registry)
    manifest={'schema_version':1,'skill_version':'4.5.7','audio_asset_manifest_id':'AUD-M-1','episode_id':'EP1','status':'READY','manifest_fingerprint':None,'audio_assets':[
      {'asset_id':'AUD_VOICE','asset_display_name':'艾琳声线母带','native_token':'@艾琳声线母带','audio_type':'VOICE_IDENTITY','authority_role':'VOICE_IDENTITY','scope':'CHARACTER','subject_entity_id':'CHAR_ELIN','episode_id':'EP1','reuse_key':'VOICE:CHAR_ELIN','version':1,'fingerprint':'a'*64,'status':'APPROVED','reference_policy':'VIDEO_REFERENCE_ALLOWED','binding_status':'READY','direct_reference_eligible':True,'intended_use':['VIDEO_REFERENCE','VOICE_CANON']}
    ]}
    mf=td/'audio.yaml'; ywrite(mf,manifest)
    run([PY,'validators/state_schema_lint.py','state/audio_asset_manifest.schema.yaml',str(mf),'--json'])
    run([PY,'validators/audio_asset_manifest_lint.py','--manifest',str(mf),'--registry',str(reg)])

    job={'schema_version':1,'skill_version':'4.5.7','generation_job_id':'VJOB','media_kind':'VIDEO','target_asset_id':'VIDEO_OUT','target_asset_type':'VIDEO_TAKE','route':'STAGE_05_VIDEO','scene_id':'SC1','shot_id':'SH1','video_unit_id':'VU1','attempt_no':1,'status':'READY','host_profile':'MULTIMODAL_ALL_ROUND_REFERENCE','prompt_ref':'prompt.txt','prompt_fingerprint':'p'*64,'execution_plan_ref':'plan.yaml','execution_plan_fingerprint':'e'*64,'prompt_artifact_ref':'artifact.yaml','required_bindings':[
      {'asset_id':'SHOT_EXEC','role':'PRIMARY_VISUAL_CONDITIONING','binding_mode':'PRIMARY_VIEW','native_token':'@SH执行帧','asset_display_name':'SH执行帧','time_scope':None},
      {'asset_id':'AUD_VOICE','role':'VOICE_AUTHORITY','binding_mode':'VOICE_AUTHORITY','native_token':'@艾琳声线母带','asset_display_name':'艾琳声线母带','time_scope':None}],
      'color_binding':{'required':False,'authority_level':'SCENE_COLOR_CARD','color_asset_id':'COLOR_SC','scene_scope':'SC1','native_token':None,'binding_status':'NOT_REQUIRED','projection_mode':'LINEAGE_ONLY','reference_reason_code':'PRIMARY_VISUAL_INHERITS_COLOR'},
      'lineage':{'parent_asset_ids':['SHOT_EXEC'],'derivation_kind':'VIDEO_FROM_SHOT_EXECUTION','source_generation_job_ids':[]},'result_handles':[]}
    jf=td/'job.yaml'; ywrite(jf,job)
    run([PY,'validators/state_schema_lint.py','state/generation_job.schema.yaml',str(jf),'--json'])
    run([PY,'validators/audio_reference_binding_lint.py','--job',str(jf),'--registry',str(reg),'--manifest',str(mf)])
    run([PY,'validators/generation_job_binding_lint.py','--job',str(jf),'--registry',str(reg),'--named-mention-mode','--json'])

    print('SECTION_1B_AUDIO_NATIVE_MENTION_SURFACE')
    runtime={'bindings':[{'asset_id':'AUD_VOICE','asset_display_name':'艾琳声线母带','native_token':'@艾琳声线母带','binding_mode':'VOICE_AUTHORITY','emit_on_prompt':True}]}
    rtf=td/'rt.yaml'; ywrite(rtf,runtime)
    goodp=td/'good.txt'; goodp.write_text('声音参考 @艾琳声线母带；保持角色已批准声线身份。',encoding='utf-8')
    badp=td/'missing.txt'; badp.write_text('保持角色已批准声线身份。',encoding='utf-8')
    run([PY,'validators/asset_mention_lint.py','--prompt',str(goodp),'--runtime',str(rtf)])
    run([PY,'validators/asset_mention_lint.py','--prompt',str(badp),'--runtime',str(rtf)],expect=2)

    bad=dict(job); bad['required_bindings']=list(job['required_bindings'])+[
      {'asset_id':'VID_MOTION','role':'MOTION_REFERENCE','binding_mode':'DIRECT_BIND','native_token':'@动作参考视频','asset_display_name':'动作参考视频','time_scope':None}]
    bf=td/'badjob.yaml'; ywrite(bf,bad)
    run([PY,'validators/audio_reference_binding_lint.py','--job',str(bf),'--registry',str(reg),'--manifest',str(mf)],expect=2)
    run([PY,'validators/generation_job_binding_lint.py','--job',str(bf),'--registry',str(reg),'--named-mention-mode','--json'],expect=1)

print('SECTION_2_AUDIO_INDEX_BUILDER')
with tempfile.TemporaryDirectory() as td:
    td=Path(td)
    reg={'schema_version':7,'skill_version':'4.5.7','assets':[{'asset_id':'AUD1','asset_display_name':'雨声','native_token':'@雨声','asset_type':'AMBIENCE_AUDIO','media_kind':'AUDIO','status':'APPROVED','authority_role':'AMBIENCE','video_usage':{'direct_input_allowed':True,'primary_visual_eligible':False}}]}
    rf=td/'r.yaml'; of=td/'out.yaml'; ywrite(rf,reg)
    run([PY,'tools/audio_asset_index_builder.py','--registry',str(rf),'--output',str(of),'--episode-id','EP1'])
    out=yaml.safe_load(of.read_text(encoding='utf-8')); assert out['audio_assets'][0]['native_token']=='@雨声'
    assert out['audio_assets'][0]['audio_type']=='AMBIENCE'
print('NO REFERENCE VIDEO + AUDIO MANAGEMENT TESTS PASS')
