#!/usr/bin/env python3
from __future__ import annotations
import copy, hashlib, json, subprocess, sys, tempfile
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parent.parent
FIX=ROOT/'tests'/'fixtures'/'v457'/'entity_binding'
PYEX=sys.executable

def run(args,expect=0):
    p=subprocess.run(args,cwd=ROOT,text=True,capture_output=True,timeout=30)
    print('$',' '.join(map(str,args)))
    if p.stdout: print(p.stdout)
    if p.stderr: print(p.stderr,file=sys.stderr)
    if p.returncode!=expect:
        raise AssertionError(f'expected {expect}, got {p.returncode}: {args}')
    return p.stdout

def load(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))
def write(p,d): Path(p).write_text(yaml.safe_dump(d,sort_keys=False,allow_unicode=True),encoding='utf-8')

def main():
    print('SECTION_1_SCHEMA_AND_BINDING_MAP')
    run([PYEX,'validators/state_schema_lint.py','state/storyboard_entity_binding_map.schema.yaml',str(FIX/'binding_map.valid.yaml'),'--json'])
    run([PYEX,'validators/storyboard_entity_binding_lint.py','--binding-map',str(FIX/'binding_map.valid.yaml')])
    run([PYEX,'validators/storyboard_entity_binding_lint.py','--binding-map',str(FIX/'binding_map.invalid.yaml')],expect=2)

    print('SECTION_2_NEAREST_VISUAL_PARENT')
    out=json.loads(run([PYEX,'tools/nearest_spatial_visual_parent_router.py','--request',str(FIX/'nearest_request.yaml'),'--registry',str(FIX/'registry.yaml'),'--json']))
    assert out['primary']['asset_id']=='ENV_90'
    assert out['secondary']['asset_id']=='ENV_45'

    print('SECTION_3_WORLD_CONTINUITY_REPROJECTION')
    run([PYEX,'validators/shot_boundary_continuity_lint.py','--contract',str(FIX/'boundary_contract.yaml'),'--from-state',str(FIX/'spatial_before.yaml'),'--to-state',str(FIX/'spatial_after_reverse.yaml')])
    bad=json.loads(run([PYEX,'validators/shot_boundary_continuity_lint.py','--contract',str(FIX/'boundary_contract.yaml'),'--from-state',str(FIX/'spatial_before.yaml'),'--to-state',str(FIX/'spatial_after_jump.yaml')],expect=2))
    assert any(x['type']=='BOUNDARY_WORLD_ZONE_JUMP' for x in bad['issues'])

    print('SECTION_4_BINDING_RESOLVE_TO_EXECUTION_PLAN')
    with tempfile.TemporaryDirectory() as td:
        td=Path(td)
        resolution=td/'resolution.yaml'
        run([PYEX,'tools/entity_binding_reference_resolver.py','--binding-map',str(FIX/'binding_map.valid.yaml'),'--registry',str(FIX/'registry.yaml'),'--request',str(FIX/'resolution_request.yaml'),'--identity-readability',str(FIX/'identity_readability.pass.yaml'),'--direct-budget','2','--output',str(resolution)])
        run([PYEX,'validators/state_schema_lint.py','state/entity_binding_resolution.schema.yaml',str(resolution),'--json'])
        r=load(resolution)
        assert r['direct_reference_ids']==['CHAR_A_3Q','PROP_SCORE_BACK']

        prompt='''@角色A保持角色A身份。@角色A站在控制台左侧中景，身体朝向角色B，右臂向前伸出，动作处于递交中段。角色B保持角色B身份。角色B位于角色A右侧半步，身体朝向角色A，角色B抬手准备接取，动作处于接取准备阶段。@关键谱盒保持其已批准背面结构。摄影机保持稳定反打关系。动作在六秒内完成递交。本视频单元保持单镜头连续。谱盒从角色A向角色B递交。角色B先观察再抬手回应。两人视线保持相互对齐。反打只改变画面左右不改变世界站位。结尾停在角色B即将接到谱盒的状态。'''
        prompt_path=td/'video_prompt.txt'; prompt_path.write_text(prompt,encoding='utf-8')

        fields=[
            ('CAMERA_MOTION','摄影机保持稳定反打关系'),('TIMING','动作在六秒内完成递交'),('CUT_NOCUT','本视频单元保持单镜头连续'),
            ('ACTION_BEAT','谱盒从角色A向角色B递交'),('PERFORMANCE','角色B先观察再抬手回应'),('EYELINE','两人视线保持相互对齐'),
            ('SHOT_RELATION','反打只改变画面左右不改变世界站位'),('LANDING','结尾停在角色B即将接到谱盒的状态')]
        plan={
            'schema_version':1,'skill_version':'4.5.7','execution_plan_id':'VEP_01','video_unit_id':'VU_01','shot_id':'SH01','scene_id':'SC01',
            'status':'FROZEN_FOR_COMPILE','video_execution_plan_pass':True,'duration_sec':6.0,'scene_bound':True,
            'source_fingerprints':{'director':'d'*16,'storyboard':'s'*16,'shot_execution':'x'*16,'scene_color':'c'*16,'world_state':'w'*16},
            'execution_plan_fingerprint':'e'*64,
            'reference_integrity':{'primary_visual':'SHOT_EXEC_01','scene_color_authority':'COLOR_SCENE_01','scene_color_reference_mode':'LINEAGE_ONLY','scene_color_reference_reason':'PRIMARY_VISUAL_INHERITS_COLOR','direct_reference_ids':r['direct_reference_ids'],'conflict_count':0,'conflicts':[]},
            'spatial_blocking':{'conflict_count':0,'conflicts':[],'subjects':[{'id':'CHAR_A','critical':True,'start':'CONTROL_LEFT','end':'CONTROL_LEFT','moves':False},{'id':'CHAR_B','critical':True,'start':'CONTROL_CENTER','end':'CONTROL_CENTER','moves':False}]},
            'body_prop_occupancy':{'conflict_count':0,'conflicts':[],'subjects':[{'id':'CHAR_A','critical':True,'human':True,'occupancy_clear':True},{'id':'CHAR_B','critical':True,'human':True,'occupancy_clear':True}]},
            'timing':{'fits':True},'conflicts':[],
            'windows':[{'id':'W1','start':0,'end':6,'primary_action':'递交谱盒','dominant_camera_moves':1,'camera_previs_proven':True,'camera':{'landing':'稳定反打落点'}}],
            'ending_state':{'landing':'角色B即将接到谱盒'},'assembly_order':'CHRONOLOGICAL',
            'storyboard_handoff':{'source_storyboard_asset_ids':['SB_SH01'],'items':[{'field':f,'applicability':'REQUIRED','source_text':a,'prompt_anchor':a} for f,a in fields]},
            'storyboard_entity_binding_map_id':'BMAP_SEQ_01',
            'entity_binding_handoff':{'source_binding_map_id':r['source_binding_map_id'],'primary_visual_asset_id':r['primary_visual_asset_id'],'bindings':r['bindings']}
        }
        plan_path=td/'plan.yaml'; write(plan_path,plan)
        run([PYEX,'validators/state_schema_lint.py','state/video_execution_plan.schema.yaml',str(plan_path),'--json'])
        run([PYEX,'validators/video_execution_plan_lint.py',str(plan_path)])
        run([PYEX,'validators/storyboard_to_video_prompt_handoff_lint.py','--execution-plan',str(plan_path),'--prompt',str(prompt_path)])
        run([PYEX,'validators/video_entity_binding_handoff_lint.py','--binding-map',str(FIX/'binding_map.valid.yaml'),'--execution-plan',str(plan_path),'--prompt',str(prompt_path),'--registry',str(FIX/'registry.yaml'),'--identity-readability',str(FIX/'identity_readability.pass.yaml')])

        print('SECTION_5_SLOT_LEAK_MUST_FAIL')
        leak=td/'leak.txt'; leak.write_text(prompt+' H_A继续动作。',encoding='utf-8')
        leakout=json.loads(run([PYEX,'validators/video_entity_binding_handoff_lint.py','--binding-map',str(FIX/'binding_map.valid.yaml'),'--execution-plan',str(plan_path),'--prompt',str(leak),'--registry',str(FIX/'registry.yaml'),'--identity-readability',str(FIX/'identity_readability.pass.yaml')],expect=2))
        assert any(x['type']=='STORYBOARD_SLOT_LEAK_TO_VIDEO_PROMPT' for x in leakout['issues'])

        print('SECTION_6_FINAL_PROMPT_TO_GENERATION_JOB')
        pf=hashlib.sha256(prompt.encode('utf-8')).hexdigest()
        artifact={
            'schema_version':1,'skill_version':'4.5.7','prompt_id':'VP_01','video_unit_id':'VU_01','shot_id':'SH01','status':'VALID',
            'prompt_ref':str(prompt_path),'prompt_fingerprint':pf,'content_char_count':len(prompt),'execution_plan_ref':str(plan_path),
            'execution_plan_fingerprint':plan['execution_plan_fingerprint'],'source_fingerprints':{'storyboard':'s'*16},'storyboard_handoff_pass':True,
            'voice_handoff_pass':True,'voice_direction_plan_id':'VDP_NONE','voice_prompt_handoff_id':'VPH_NONE','voice_prompt_handoff_fingerprint':'v'*64,'created_at':None
        }
        artifact_path=td/'artifact.yaml'; write(artifact_path,artifact)
        run([PYEX,'validators/state_schema_lint.py','state/video_prompt_artifact.schema.yaml',str(artifact_path),'--json'])
        job={
            'schema_version':1,'skill_version':'4.5.7','generation_job_id':'JOB_VIDEO_01','media_kind':'VIDEO','target_asset_id':'TAKE_01','target_asset_type':'VIDEO_TAKE',
            'route':'STAGE_05_VIDEO','scene_id':'SC01','shot_id':'SH01','video_unit_id':'VU_01','attempt_no':1,'status':'PLANNED','host_profile':'NAMED_ASSET_PLATFORM',
            'prompt_ref':str(prompt_path),'prompt_fingerprint':pf,'execution_plan_ref':str(plan_path),'execution_plan_fingerprint':plan['execution_plan_fingerprint'],'prompt_artifact_ref':str(artifact_path),
            'required_bindings':[
                {'asset_id':'SHOT_EXEC_01','role':'PRIMARY_VISUAL_CONDITIONING','binding_mode':'PRIMARY_VIEW','native_token':'@SH01执行帧','asset_display_name':'SH01执行帧','time_scope':'t0'},
                {'asset_id':'CHAR_A_3Q','role':'CHARACTER_IDENTITY','binding_mode':'MUST_BIND','native_token':'@角色A','asset_display_name':'角色A','time_scope':'all'},
                {'asset_id':'PROP_SCORE_BACK','role':'PROP_VIEW_AUTHORITY','binding_mode':'MUST_BIND','native_token':'@关键谱盒','asset_display_name':'关键谱盒','time_scope':'all'}],
            'color_binding':{'required':False,'authority_level':'SCENE_COLOR_CARD','color_asset_id':'COLOR_SCENE_01','scene_scope':'SC01:INTERIOR','binding_status':'NOT_REQUIRED','projection_mode':'LINEAGE_ONLY','reference_reason_code':'PRIMARY_VISUAL_INHERITS_COLOR'},
            'lineage':{'parent_asset_ids':['SHOT_EXEC_01','CHAR_A_3Q','PROP_SCORE_BACK'],'derivation_kind':'VIDEO_FROM_SHOT_EXECUTION','source_generation_job_ids':[]},
            'result_handles':[],'selected_candidate_id':None,'approval_ref':None,'failure_code':None
        }
        job_path=td/'job.yaml'; write(job_path,job)
        run([PYEX,'validators/state_schema_lint.py','state/generation_job.schema.yaml',str(job_path),'--json'])
        run([PYEX,'validators/generation_job_binding_lint.py','--job',str(job_path),'--registry',str(FIX/'registry.yaml'),'--named-mention-mode','--json'])
        run([PYEX,'validators/video_generation_job_prompt_lint.py','--job',str(job_path),'--prompt-artifact',str(artifact_path),'--execution-plan',str(plan_path)])

        badjob=copy.deepcopy(job); badjob['required_bindings']=[x for x in badjob['required_bindings'] if x['asset_id']!='PROP_SCORE_BACK']; badjob_path=td/'badjob.yaml'; write(badjob_path,badjob)
        badout=json.loads(run([PYEX,'validators/video_generation_job_prompt_lint.py','--job',str(badjob_path),'--prompt-artifact',str(artifact_path),'--execution-plan',str(plan_path)],expect=2))
        assert any(x['type']=='VIDEO_JOB_ENTITY_DIRECT_BINDING_MISSING' and x.get('asset_id')=='PROP_SCORE_BACK' for x in badout['issues'])

    print('SECTION_7_CONTROL_PLANE_WIRING')
    route=load(ROOT/'controller'/'route_registry.yaml'); wf=load(ROOT/'controller'/'workflow_state_machine.yaml'); gates=load(ROOT/'controller'/'gate_producer_registry.yaml'); auth=load(ROOT/'controller'/'authority_registry.yaml')
    assert route['structured_artifacts']['STORYBOARD_ENTITY_BINDING_MAP']=='state/storyboard_entity_binding_map.schema.yaml'
    assert 'STORYBOARD_ENTITY_BINDING_MAP' in route['routes']['STAGE_05_VIDEO']['structured_inputs']
    assert 'tools/entity_binding_reference_resolver.py' in route['routes']['STAGE_05_VIDEO']['deterministic_tools']
    assert 'tools/nearest_spatial_visual_parent_router.py' in route['routes']['STAGE_05_VIDEO']['deterministic_tools']
    t19=next(x for x in wf['transitions'] if x['id']=='T19_STORYBOARD_QC'); t23=next(x for x in wf['transitions'] if x['id']=='T23B_VIDEO_READY')
    assert 'STORYBOARD_ENTITY_BINDING_PASS' in t19['requires']
    assert 'VIDEO_ENTITY_BINDING_HANDOFF_PASS' in t23['requires']
    assert gates['producers']['STORYBOARD_ENTITY_BINDING_PASS']['owner']=='validators/storyboard_entity_binding_lint.py'
    assert gates['producers']['VIDEO_ENTITY_BINDING_HANDOFF_PASS']['owner']=='validators/video_entity_binding_handoff_lint.py'
    assert auth['authorities']['storyboard_entity_binding_map']['structured_schema']=='state/storyboard_entity_binding_map.schema.yaml'
    print('ALL ENTITY BINDING -> VIDEO CLOSURE TESTS PASSED')

if __name__=='__main__': main()
