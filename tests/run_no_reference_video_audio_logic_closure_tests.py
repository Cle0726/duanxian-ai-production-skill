#!/usr/bin/env python3
from __future__ import annotations
import subprocess, sys, tempfile
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parent.parent; PY=sys.executable

def run(cmd,expect=0):
    cp=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
    print('$',' '.join(map(str,cmd))); print(cp.stdout)
    if cp.stderr: print(cp.stderr)
    if cp.returncode!=expect: raise AssertionError((cmd,cp.returncode,expect))
    return cp

def yw(p,d): Path(p).write_text(yaml.safe_dump(d,sort_keys=False,allow_unicode=True),encoding='utf-8')

def base_registry():
    return {'schema_version':7,'skill_version':'4.5.7','assets':[
      {'asset_id':'SHOT_EXEC','asset_display_name':'执行帧','native_token':'@执行帧','asset_type':'VIDEO_SHOT_EXECUTION_FRAME','media_kind':'IMAGE','status':'APPROVED_VIDEO_CONDITIONING','authority_role':'PRIMARY_VISUAL_CONDITIONING','scene_color_authority_id':'COLOR','video_usage':{'direct_input_allowed':True,'primary_visual_eligible':True}},
      {'asset_id':'COLOR','asset_display_name':'色卡','native_token':'@色卡','asset_type':'SCENE_COLOR_CARD','media_kind':'IMAGE','status':'APPROVED','authority_role':'COLOR_AUTHORITY','scene_id':'SC1','video_usage':{'direct_input_allowed':True,'primary_visual_eligible':False}},
      {'asset_id':'AUD','asset_display_name':'角色声线','native_token':'@角色声线','asset_type':'VOICE_IDENTITY_ASSET','media_kind':'AUDIO','status':'APPROVED','authority_role':'VOICE_IDENTITY','subject_entity_id':'CHAR_A','fingerprint':'b'*64,'video_usage':{'direct_input_allowed':True,'primary_visual_eligible':False}},
      {'asset_id':'IMG','asset_display_name':'人物图','native_token':'@人物图','asset_type':'CHARACTER_MASTER','media_kind':'IMAGE','status':'APPROVED','authority_role':'CHARACTER_IDENTITY','subject_entity_id':'CHAR_A','video_usage':{'direct_input_allowed':True,'primary_visual_eligible':False}},
      {'asset_id':'VID','asset_display_name':'动作视频','native_token':'@动作视频','asset_type':'MOTION_REFERENCE_VIDEO','media_kind':'VIDEO','status':'APPROVED','authority_role':'MOTION_REFERENCE','video_usage':{'direct_input_allowed':True,'primary_visual_eligible':False}},
    ]}

def manifest(status='READY',subject='CHAR_A',scope='CHARACTER'):
    return {'schema_version':1,'skill_version':'4.5.7','audio_asset_manifest_id':'AM','episode_id':'EP1','status':status,'manifest_fingerprint':'f'*64,'audio_assets':[
      {'asset_id':'AUD','asset_display_name':'角色声线','native_token':'@角色声线','audio_type':'VOICE_IDENTITY','authority_role':'VOICE_IDENTITY','scope':scope,'subject_entity_id':subject,'episode_id':'EP1','reuse_key':'VOICE:CHAR_A','version':1,'fingerprint':'b'*64,'status':'APPROVED','reference_policy':'VIDEO_REFERENCE_ALLOWED','binding_status':'READY','direct_reference_eligible':True,'intended_use':['VIDEO_REFERENCE','VOICE_CANON']}
    ]}

def job(extra=None):
    binds=[{'asset_id':'SHOT_EXEC','role':'PRIMARY_VISUAL_CONDITIONING','binding_mode':'PRIMARY_VIEW','native_token':'@执行帧'}]
    if extra: binds+=extra
    return {'schema_version':1,'skill_version':'4.5.7','generation_job_id':'VJ','media_kind':'VIDEO','target_asset_id':'OUT','target_asset_type':'VIDEO_TAKE','route':'STAGE_05_VIDEO','episode_id':'EP1','sequence_id':'SEQ1','scene_id':'SC1','shot_id':'SH1','video_unit_id':'VU1','attempt_no':1,'status':'READY','host_profile':'MULTIMODAL_ALL_ROUND_REFERENCE','prompt_ref':'p.txt','prompt_fingerprint':'p'*64,'execution_plan_ref':'e.yaml','execution_plan_fingerprint':'e'*64,'prompt_artifact_ref':'a.yaml','required_bindings':binds,'color_binding':{'required':False,'authority_level':'SCENE_COLOR_CARD','color_asset_id':'COLOR','scene_scope':'SC1','binding_status':'NOT_REQUIRED','projection_mode':'LINEAGE_ONLY','reference_reason_code':'PRIMARY_VISUAL_INHERITS_COLOR'},'lineage':{'parent_asset_ids':['SHOT_EXEC'],'derivation_kind':'VIDEO_FROM_SHOT_EXECUTION','source_generation_job_ids':[]},'result_handles':[]}

with tempfile.TemporaryDirectory() as td:
    td=Path(td); reg=td/'r.yaml'; mf=td/'m.yaml'; yw(reg,base_registry()); yw(mf,manifest())
    # valid audio
    good=td/'good.yaml'; yw(good,job([{'asset_id':'AUD','role':'VOICE_AUTHORITY','binding_mode':'VOICE_AUTHORITY','native_token':'@角色声线'}]))
    run([PY,'validators/audio_reference_binding_lint.py','--job',str(good),'--registry',str(reg),'--manifest',str(mf)])
    run([PY,'validators/generation_job_binding_lint.py','--job',str(good),'--registry',str(reg),'--named-mention-mode','--json'])
    # unknown reference must fail
    u=td/'unknown.yaml'; yw(u,job([{'asset_id':'VID_UNKNOWN','role':'MOTION_REFERENCE','binding_mode':'DIRECT_BIND','native_token':'@未知视频'}]))
    run([PY,'validators/generation_job_binding_lint.py','--job',str(u),'--registry',str(reg),'--json'],expect=1)
    run([PY,'validators/audio_reference_binding_lint.py','--job',str(u),'--registry',str(reg),'--manifest',str(mf)],expect=2)
    # real video must fail
    v=td/'video.yaml'; yw(v,job([{'asset_id':'VID','role':'MOTION_REFERENCE','binding_mode':'DIRECT_BIND','native_token':'@动作视频'}]))
    run([PY,'validators/generation_job_binding_lint.py','--job',str(v),'--registry',str(reg),'--json'],expect=1)
    # image masquerading as audio must fail
    ia=td/'imageaudio.yaml'; yw(ia,job([{'asset_id':'IMG','role':'VOICE_AUTHORITY','binding_mode':'VOICE_AUTHORITY','native_token':'@人物图'}]))
    run([PY,'validators/generation_job_binding_lint.py','--job',str(ia),'--registry',str(reg),'--json'],expect=1)
    run([PY,'validators/audio_reference_binding_lint.py','--job',str(ia),'--registry',str(reg),'--manifest',str(mf)],expect=2)
    # missing job token must fail even if manifest has token
    nt=td/'notoken.yaml'; yw(nt,job([{'asset_id':'AUD','role':'VOICE_AUTHORITY','binding_mode':'VOICE_AUTHORITY'}]))
    run([PY,'validators/audio_reference_binding_lint.py','--job',str(nt),'--registry',str(reg),'--manifest',str(mf)],expect=2)
    # draft manifest must fail at job use
    dm=td/'draftmanifest.yaml'; yw(dm,manifest(status='DRAFT'))
    run([PY,'validators/audio_reference_binding_lint.py','--job',str(good),'--registry',str(reg),'--manifest',str(dm)],expect=2)
    # wrong voice subject must fail manifest lint
    sm=td/'subject.yaml'; yw(sm,manifest(subject='CHAR_B'))
    run([PY,'validators/audio_asset_manifest_lint.py','--manifest',str(sm),'--registry',str(reg)],expect=2)
    # scope owner must be present (SCENE but no scene_id)
    badscope=manifest(); badscope['audio_assets'][0]['scope']='SCENE'; badscope['audio_assets'][0]['scene_id']=None
    sf=td/'scope.yaml'; yw(sf,badscope)
    run([PY,'validators/audio_asset_manifest_lint.py','--manifest',str(sf),'--registry',str(reg)],expect=2)
print('NO REFERENCE VIDEO + AUDIO LOGIC CLOSURE TESTS PASS')
