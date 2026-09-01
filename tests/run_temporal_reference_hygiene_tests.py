#!/usr/bin/env python3
from __future__ import annotations
import base64, copy, hashlib, json, subprocess, sys, tempfile
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]; PY=sys.executable
FIX=ROOT/'tests'/'fixtures'/'v457'/'entity_binding'

def run(args,expect=0,timeout=45):
    p=subprocess.run(args,cwd=ROOT,text=True,capture_output=True,timeout=timeout)
    if p.returncode!=expect:
        print(p.stdout); print(p.stderr,file=sys.stderr); raise AssertionError(f'expected {expect}, got {p.returncode}: {args}')
    return p.stdout

def load(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))
def write(p,d): Path(p).write_text(yaml.safe_dump(d,sort_keys=False,allow_unicode=True),encoding='utf-8')
def canon_fp(d,key):
    x=copy.deepcopy(d); x.pop(key,None)
    return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def main():
  with tempfile.TemporaryDirectory() as td0:
    td=Path(td0); frame=td/'tail.png'
    frame.write_bytes(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9Y9Z9ZsAAAAASUVORK5CYII='))
    exitst=td/'exit.yaml'; write(exitst,{'ongoing_action_state':{'phase':'REACH_70'},'continuity_motion_capsule':{'body_momentum':'FORWARD','camera_velocity':'STABLE'}})

    print('SECTION_1_ENDING_ANCHOR_PROVENANCE')
    bad=run([PY,'tools/ending_frame_capture.py','--ending-frame-path',str(frame),'--output-frame',str(td/'bad.png'),'--snapshot-output',str(td/'bad.yaml'),'--episode-id','EP','--video-ref','VID','--snapshot-id','BAD'],expect=2)
    assert 'PLATFORM_EXTRACTED_SOURCE_VIDEO_FINGERPRINT_REQUIRED' in bad
    s1=td/'s1.yaml'; c1=td/'c1.png'
    run([PY,'tools/ending_frame_capture.py','--ending-frame-path',str(frame),'--source-video-fingerprint','1'*64,'--extraction-proof-ref','PROOF_1','--output-frame',str(c1),'--snapshot-output',str(s1),'--episode-id','EP','--video-ref','VID1','--snapshot-id','S1','--scene-id','SC','--segment-id','VU1','--shot-id','SH','--exit-state',str(exitst)])
    run([PY,'validators/continuity_snapshot_lint.py',str(s1)])
    assert load(s1)['pixel_lineage_depth']==1

    print('SECTION_2_RECURSIVE_PIXEL_LINEAGE')
    s2=td/'s2.yaml'; c2=td/'c2.png'
    run([PY,'tools/ending_frame_capture.py','--ending-frame-path',str(frame),'--source-video-fingerprint','2'*64,'--extraction-proof-ref','PROOF_2','--previous-snapshot',str(s1),'--output-frame',str(c2),'--snapshot-output',str(s2),'--episode-id','EP','--video-ref','VID2','--snapshot-id','S2'])
    assert load(s2)['pixel_lineage_depth']==2
    run([PY,'validators/continuity_snapshot_lint.py',str(s2)])
    tam=load(s1); tam['degradation_debt']['identity_debt']=0.5; tam['snapshot_fingerprint']=canon_fp(tam,'snapshot_fingerprint'); write(s1,tam)
    out=json.loads(run([PY,'validators/continuity_snapshot_lint.py',str(s2)],expect=2))
    assert any(x['type']=='TEMPORAL_PREVIOUS_SNAPSHOT_FINGERPRINT_MISMATCH' for x in out['issues'])
    # restore a valid root and child
    run([PY,'tools/ending_frame_capture.py','--ending-frame-path',str(frame),'--source-video-fingerprint','1'*64,'--extraction-proof-ref','PROOF_1','--output-frame',str(c1),'--snapshot-output',str(s1),'--episode-id','EP','--video-ref','VID1','--snapshot-id','S1'])
    run([PY,'tools/ending_frame_capture.py','--ending-frame-path',str(frame),'--source-video-fingerprint','2'*64,'--extraction-proof-ref','PROOF_2','--previous-snapshot',str(s1),'--output-frame',str(c2),'--snapshot-output',str(s2),'--episode-id','EP','--video-ref','VID2','--snapshot-id','S2'])

    print('SECTION_3_PROVIDER_T0_TRANSPORT')
    badp=run([PY,'tools/temporal_entry_planner.py','--output',str(td/'badplan.yaml'),'--plan-id','TP_BAD','--video-unit-id','VU2','--mode','SEAMLESS_EXTEND','--snapshot',str(s2),'--internal-conditioning-primary','SHOT_EXEC_01','--transport-type','GENERIC_REFERENCE'],expect=2)
    assert 'TEMPORAL_PROVIDER_T0_TRANSPORT_UNVERIFIED' in badp
    tp=td/'tp.yaml'
    run([PY,'tools/temporal_entry_planner.py','--output',str(tp),'--plan-id','TP1','--video-unit-id','VU2','--mode','SEAMLESS_EXTEND','--snapshot',str(s2),'--internal-conditioning-primary','SHOT_EXEC_01','--transport-type','FIRST_FRAME_INPUT','--t0-semantics-verified','--capability-evidence-ref','PROVIDER_DOC_FIRST_FRAME'])
    run([PY,'validators/state_schema_lint.py','state/temporal_entry_plan.schema.yaml',str(tp),'--json'])
    run([PY,'validators/temporal_entry_plan_lint.py',str(tp)])

    print('SECTION_4_T0_SUFFICIENCY_AND_ENTITY_BINDING')
    req=td/'t0req.yaml'; write(req,{'entities':[{'slot_id':'H_A','entity_id':'CHAR_A','verdict':'SUFFICIENT','evidence_ref':'TAIL_FACE_READABLE'},{'slot_id':'H_B','entity_id':'CHAR_B','verdict':'SUFFICIENT','evidence_ref':'TAIL_FACE_B_READABLE'},{'slot_id':'P_A','entity_id':'PROP_SCORE','verdict':'SUFFICIENT','evidence_ref':'TAIL_PROP_BACK_READABLE'}]})
    ta=td/'t0.yaml'; run([PY,'tools/temporal_t0_sufficiency_builder.py','--entry-plan',str(tp),'--request',str(req),'--output',str(ta),'--assessment-id','T0A1'])
    run([PY,'validators/state_schema_lint.py','state/temporal_t0_sufficiency_assessment.schema.yaml',str(ta),'--json'])
    resolution=td/'resolution.yaml'
    run([PY,'tools/entity_binding_reference_resolver.py','--binding-map',str(FIX/'binding_map.valid.yaml'),'--registry',str(FIX/'registry.yaml'),'--request',str(FIX/'resolution_request.yaml'),'--identity-readability',str(FIX/'identity_readability.pass.yaml'),'--temporal-entry-plan',str(tp),'--temporal-t0-assessment',str(ta),'--direct-budget','2','--output',str(resolution)])
    r=load(resolution); by={x['slot_id']:x for x in r['bindings']}; assert by['H_A']['resolution_mode']=='TEMPORAL_T0_BAKED' and by['P_A']['resolution_mode']=='TEMPORAL_T0_BAKED'; assert r['direct_reference_ids']==[]
    assert not by['H_A']['resolved_asset_id'] and not by['H_A']['native_token']
    run([PY,'validators/state_schema_lint.py','state/entity_binding_resolution.schema.yaml',str(resolution),'--json'])
    reqbad=td/'t0badreq.yaml'; write(reqbad,{'entities':[{'slot_id':'H_A','entity_id':'CHAR_A','verdict':'INSUFFICIENT','reason':'face soft'}]}); tabad=td/'t0bad.yaml'; run([PY,'tools/temporal_t0_sufficiency_builder.py','--entry-plan',str(tp),'--request',str(reqbad),'--output',str(tabad),'--assessment-id','T0BAD'])
    out=json.loads(run([PY,'tools/entity_binding_reference_resolver.py','--binding-map',str(FIX/'binding_map.valid.yaml'),'--registry',str(FIX/'registry.yaml'),'--request',str(FIX/'resolution_request.yaml'),'--identity-readability',str(FIX/'identity_readability.pass.yaml'),'--temporal-entry-plan',str(tp),'--temporal-t0-assessment',str(tabad),'--direct-budget','2'],expect=2))
    assert any(x['type']=='TEMPORAL_RESET_REQUIRED' for x in out['issues'])

    print('SECTION_5_INTERNAL_PRIMARY_VS_MODEL_T0')
    fields=[('CAMERA_MOTION','摄影机保持稳定反打关系'),('TIMING','动作在六秒内完成递交'),('CUT_NOCUT','本视频单元保持单镜头连续'),('ACTION_BEAT','谱盒从角色A向角色B继续递交'),('PERFORMANCE','角色B先观察再抬手回应'),('EYELINE','两人视线保持相互对齐'),('SHOT_RELATION','反打只改变画面左右不改变世界站位'),('LANDING','结尾停在角色B即将接到谱盒的状态')]
    base={'schema_version':1,'skill_version':'4.5.7','execution_plan_id':'TEMP_PLAN','video_unit_id':'VU2','shot_id':'SH01','scene_id':'SC01','status':'FROZEN_FOR_COMPILE','video_execution_plan_pass':True,'duration_sec':6.0,'scene_bound':True,'source_fingerprints':{'director':'d'*16,'storyboard':'s'*16,'shot_execution':'x'*16,'scene_color':'c'*16,'world_state':'w'*16},'reference_integrity':{'primary_visual':'SHOT_EXEC_01','scene_color_authority':'COLOR_SCENE_01','scene_color_reference_mode':'LINEAGE_ONLY','scene_color_reference_reason':'PRIMARY_VISUAL_INHERITS_COLOR','direct_reference_ids':[],'conflict_count':0,'conflicts':[]},'spatial_blocking':{'conflict_count':0,'conflicts':[],'subjects':[{'id':'CHAR_A','critical':True,'start':'CONTROL_LEFT','end':'CONTROL_LEFT','moves':False}]},'body_prop_occupancy':{'conflict_count':0,'conflicts':[],'subjects':[{'id':'CHAR_A','critical':True,'human':True,'occupancy_clear':True}]},'timing':{'fits':True},'conflicts':[],'windows':[{'id':'W1','start':0,'end':6,'primary_action':'继续递交谱盒','dominant_camera_moves':1,'camera_previs_proven':True,'camera':{'landing':'稳定落点'}}],'ending_state':{'landing':'角色B即将接到谱盒'},'assembly_order':'CHRONOLOGICAL','storyboard_handoff':{'source_storyboard_asset_ids':['SB_SH01'],'items':[{'field':f,'applicability':'REQUIRED','source_text':x,'prompt_anchor':x} for f,x in fields]},'storyboard_entity_binding_map_id':'BMAP_SEQ_01','entity_binding_handoff':{'source_binding_map_id':r['source_binding_map_id'],'primary_visual_asset_id':r['primary_visual_asset_id'],'bindings':r['bindings'],'temporal_entry_plan_fingerprint':r['temporal_entry_plan_fingerprint'],'temporal_t0_sufficiency_fingerprint':r['temporal_t0_sufficiency_fingerprint'],'continuity_snapshot_fingerprint':r['continuity_snapshot_fingerprint']}}
    tpd=load(tp); tad=load(ta)
    base['temporal_visual_isolation']={'entry_mode':'SEAMLESS_EXTEND','internal_conditioning_primary':'SHOT_EXEC_01','model_t0_owner':'PREVIOUS_ENDING_ANCHOR','prompt_profile':'DELTA_CONTINUATION_PROMPT','temporal_entry_plan_ref':str(tp.resolve()),'temporal_entry_plan_fingerprint':tpd['temporal_entry_plan_fingerprint'],'temporal_t0_sufficiency_ref':str(ta.resolve()),'temporal_t0_sufficiency_fingerprint':tad['assessment_fingerprint'],'continuity_snapshot_ref':tpd['continuity_snapshot_ref'],'continuity_snapshot_fingerprint':tpd['continuity_snapshot_fingerprint'],'target_frame_ref':None,'target_frame_fingerprint':None,'provider_transport':tpd['provider_transport'],'visual_isolation_pass':True}
    base['execution_plan_fingerprint']=canon_fp(base,'execution_plan_fingerprint'); plan=td/'plan.yaml'; write(plan,base)
    run([PY,'validators/state_schema_lint.py','state/video_execution_plan.schema.yaml',str(plan),'--json']); run([PY,'validators/video_execution_plan_lint.py',str(plan)])

    print('SECTION_6_PLAN_PROMPT_JOB_FINGERPRINT_CHAIN')
    prompt=td/'delta.txt'; text='摄影机保持稳定反打关系。动作在六秒内完成递交。本视频单元保持单镜头连续。谱盒从角色A向角色B继续递交。角色B先观察再抬手回应。两人视线保持相互对齐。反打只改变画面左右不改变世界站位。结尾停在角色B即将接到谱盒的状态。'; prompt.write_text(text,encoding='utf-8'); pf=hashlib.sha256(text.encode()).hexdigest()
    art={'schema_version':1,'skill_version':'4.5.7','prompt_id':'PA1','video_unit_id':'VU2','shot_id':'SH01','status':'VALID','prompt_ref':str(prompt),'prompt_fingerprint':pf,'content_char_count':len(text),'execution_plan_ref':str(plan),'execution_plan_fingerprint':base['execution_plan_fingerprint'],'source_fingerprints':base['source_fingerprints'],'storyboard_handoff_pass':True,'voice_handoff_pass':True,'voice_direction_plan_id':'VDP_NONE','voice_prompt_handoff_id':'VPH_NONE','voice_prompt_handoff_fingerprint':'v'*64,'prompt_profile':'DELTA_CONTINUATION_PROMPT','temporal_entry_plan_fingerprint':tpd['temporal_entry_plan_fingerprint'],'temporal_t0_sufficiency_fingerprint':tad['assessment_fingerprint'],'continuity_snapshot_fingerprint':tpd['continuity_snapshot_fingerprint']}
    artp=td/'art.yaml'; write(artp,art); run([PY,'validators/state_schema_lint.py','state/video_prompt_artifact.schema.yaml',str(artp),'--json'])
    job={'schema_version':1,'skill_version':'4.5.7','generation_job_id':'J1','media_kind':'VIDEO','target_asset_id':'TAKE','target_asset_type':'VIDEO_TAKE','route':'STAGE_05_VIDEO','scene_id':'SC01','shot_id':'SH01','video_unit_id':'VU2','attempt_no':1,'status':'PLANNED','host_profile':'MULTIMODAL_ALL_ROUND_REFERENCE','prompt_ref':str(prompt),'prompt_fingerprint':pf,'execution_plan_ref':str(plan),'execution_plan_fingerprint':base['execution_plan_fingerprint'],'prompt_artifact_ref':str(artp),'required_bindings':[],'color_binding':{'required':False,'authority_level':'SCENE_COLOR_CARD','color_asset_id':'COLOR_SCENE_01','scene_scope':'SC01:INTERIOR','binding_status':'NOT_REQUIRED','projection_mode':'LINEAGE_ONLY','reference_reason_code':'PRIMARY_VISUAL_INHERITS_COLOR'},'lineage':{'parent_asset_ids':['SHOT_EXEC_01'],'derivation_kind':'VIDEO_FROM_SHOT_EXECUTION','source_generation_job_ids':[]},'result_handles':[],'selected_candidate_id':None,'approval_ref':None,'failure_code':None,'temporal_binding':{'entry_mode':'SEAMLESS_EXTEND','prompt_profile':'DELTA_CONTINUATION_PROMPT','temporal_entry_plan_ref':str(tp),'temporal_entry_plan_fingerprint':tpd['temporal_entry_plan_fingerprint'],'temporal_t0_sufficiency_ref':str(ta),'temporal_t0_sufficiency_fingerprint':tad['assessment_fingerprint'],'continuity_snapshot_ref':tpd['continuity_snapshot_ref'],'continuity_snapshot_fingerprint':tpd['continuity_snapshot_fingerprint'],'target_frame_ref':None,'target_frame_fingerprint':None,'provider_transport':tpd['provider_transport']}}
    jp=td/'job.yaml'; write(jp,job); run([PY,'validators/state_schema_lint.py','state/generation_job.schema.yaml',str(jp),'--json']); run([PY,'validators/generation_job_binding_lint.py','--job',str(jp),'--registry',str(FIX/'registry.yaml'),'--json']); run([PY,'validators/video_generation_job_prompt_lint.py','--job',str(jp),'--prompt-artifact',str(artp),'--execution-plan',str(plan)])

    print('SECTION_7_SECOND_PRIMARY_AND_AUX_STATIC_FORBIDDEN')
    badjob=copy.deepcopy(job); badjob['required_bindings']=[{'asset_id':'SHOT_EXEC_01','role':'PRIMARY_VISUAL_CONDITIONING','binding_mode':'PRIMARY_VIEW','native_token':'@SH01执行帧','asset_display_name':'SH01执行帧','time_scope':'t0'}]; bp=td/'badjob.yaml'; write(bp,badjob)
    out=json.loads(run([PY,'validators/generation_job_binding_lint.py','--job',str(bp),'--registry',str(FIX/'registry.yaml'),'--json'],expect=1)); assert any(x['type']=='TEMPORAL_T0_MULTIPLE_PRIMARY_VISUAL_CONFLICT' for x in out['issues'])

    print('SECTION_8_GATE_AFTER_SNAPSHOT_REPLACEMENT')
    # Replace a previously valid snapshot in place and prove the downstream job gate reopens it.
    s2d=load(s2); s2d['degradation_debt']['noise_debt']=0.7; s2d['snapshot_fingerprint']=canon_fp(s2d,'snapshot_fingerprint'); write(s2,s2d)
    out=json.loads(run([PY,'validators/video_generation_job_prompt_lint.py','--job',str(jp),'--prompt-artifact',str(artp),'--execution-plan',str(plan)],expect=2)); assert any(x['type']=='TEMPORAL_CONTINUITY_SNAPSHOT_STALE' for x in out['issues'])

    print('SECTION_9_CONTROLLER_AND_FAILURE_ROUTER')
    wf=load(ROOT/'controller/workflow_state_machine.yaml'); t=next(x for x in wf['transitions'] if x['id']=='T23B_VIDEO_READY'); assert t['conditional_requires']['TEMPORAL_SAME_TAKE']==['CONTINUITY_SNAPSHOT_PASS','TEMPORAL_ENTRY_PLAN_PASS','TEMPORAL_T0_SUFFICIENCY_PASS']
    gates=load(ROOT/'controller/gate_producer_registry.yaml')['producers']; assert gates['CONTINUITY_SNAPSHOT_PASS']['owner']=='validators/continuity_snapshot_lint.py'; assert gates['TEMPORAL_ENTRY_PLAN_PASS']['owner']=='validators/temporal_entry_plan_lint.py'
    fr=load(ROOT/'controller/failure_router.yaml'); required=['TEMPORAL_T0_MULTIPLE_PRIMARY_VISUAL_CONFLICT','TEMPORAL_CONTINUITY_AUXILIARY_VISUAL_REFERENCE_CONFLICT','TEMPORAL_CONTINUITY_DIRECT_COLOR_REFERENCE_CONFLICT','TEMPORAL_PROVIDER_T0_TRANSPORT_UNVERIFIED','CONTINUITY_SNAPSHOT_FINGERPRINT_INVALID','TEMPORAL_RESET_REQUIRED']
    for code in required: assert code in fr['code_aliases'],code

    print('SECTION_10_PROVIDER_GENERIC_REFERENCE_NOT_T0')
    hp=load(ROOT/'adapters/generation/host_profiles.yaml'); assert hp['profiles']['MULTIMODAL_ALL_ROUND_REFERENCE']['temporal_transport']['generic_reference_implies_t0_semantics'] is False
    assert hp['profiles']['MULTIMODAL_ALL_ROUND_REFERENCE']['temporal_transport']['t0_semantics_verified'] is False
    print('TEMPORAL REFERENCE HYGIENE TESTS: PASS')
if __name__=='__main__': main()
