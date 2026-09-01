#!/usr/bin/env python3
from pathlib import Path
import copy, importlib.util, json, subprocess, sys, tempfile, yaml, os, time
ROOT=Path(__file__).resolve().parents[1]; PY=sys.executable

def run(args,expect=0):
    t=time.monotonic(); p=subprocess.run(args,cwd=ROOT,text=True,capture_output=True,timeout=20)
    if os.environ.get('V457_TEST_TIMING'): print(f'{time.monotonic()-t:.2f}s :: {args[1] if len(args)>1 else args[0]}', flush=True)
    if p.returncode!=expect:
        print('$',' '.join(map(str,args))); print(p.stdout); print(p.stderr,file=sys.stderr); raise SystemExit(f'expected {expect}, got {p.returncode}')
    return p.stdout

def ywrite(p,d): Path(p).write_text(yaml.safe_dump(d,sort_keys=False,allow_unicode=True),encoding='utf-8')
def yload(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))

print('SECTION_1', flush=True)
# 1. Architecture, YAML and schemas.
run([PY,'validators/v457_architecture_lint.py','--root',str(ROOT),'--json'])
run([PY,'validators/yaml_duplicate_key_lint.py','controller/route_registry.yaml','controller/workflow_state_machine.yaml','controller/authority_registry.yaml','state/generation_job.schema.yaml','state/asset_registry.schema.yaml','runtime/generation_runtime.schema.yaml','adapters/generation/host_profiles.yaml','adapters/generation/platform_profile.yaml'])
run([PY,'validators/state_schema_lint.py','state/generation_job.schema.yaml','tests/fixtures/v457/generation_job.character.valid.yaml','--json'])

# Workflow authority must define initial states for every mode and episode-state enum must match the workflow.
wf=yload(ROOT/'controller/workflow_state_machine.yaml'); eps=yload(ROOT/'state/episode_state.schema.yaml')
assert wf['initial_state_by_mode']=={'PRODUCTION':'SOURCE_NARRATIVE_PENDING','DEMO':'SOURCE_NARRATIVE_PENDING','MIGRATION':'MIGRATION_REQUIRED'}
assert set(eps['properties']['workflow_state']['enum'])==set(wf['states'])
# REALISM_CONTRACT structured owner is explicit and unique.
ar=yload(ROOT/'controller/authority_registry.yaml'); owners=[k for k,v in ar['authorities'].items() if isinstance(v,dict) and v.get('structured_schema')=='state/realism_contract.schema.yaml']
assert owners==['realism_contract'] and ar['authorities']['everyday_realism_plausibility']['consumes_authority']=='realism_contract'

print('SECTION_2', flush=True)
# 2. V4.5.7 must inherit V4.5.6 strict Reality behavior.
spec=importlib.util.spec_from_file_location('er',ROOT/'validators/everyday_realism_lint.py'); er=importlib.util.module_from_spec(spec); spec.loader.exec_module(er)
assert er.is_v456_or_newer({'skill_version':'4.5.7'},None,None) is True
assert er.is_v456_or_newer({'skill_version':'4.5.5'},None,None) is False

print('SECTION_3', flush=True)
# 3. Required View must treat ENVIRONMENT_COVERAGE as the physical current coverage type in 4.5.7.
with tempfile.TemporaryDirectory() as td:
    sp=Path(td)/'sp.yaml'; rg=Path(td)/'rg.yaml'
    s=yload(ROOT/'tests/fixtures/spatial_canon.required_views.valid.yaml'); s['skill_version']='4.5.7'; ywrite(sp,s)
    r=yload(ROOT/'tests/fixtures/asset_registry.required_views.valid.yaml'); r['skill_version']='4.5.7'
    for x in r['assets']:
        if x.get('asset_type')=='DERIVED_COVERAGE_VIEW': x['asset_type']='ENVIRONMENT_COVERAGE'
    ywrite(rg,r)
    run([PY,'validators/required_view_realization_lint.py','--spatial-canon',str(sp),'--asset-registry',str(rg),'--phase','build'])

print('SECTION_4', flush=True)
# 4. Color cards are scope-owned, APPROVED, and required before generation.
registry=ROOT/'tests/fixtures/v457/asset_registry.lineage_color.valid.yaml'
run([PY,'validators/scene_color_binding_lint.py','--registry',str(registry),'--conditioning-runtime','tests/fixtures/v457/video_conditioning.color.valid.yaml','--named-mention-mode','--json'])
run([PY,'validators/generation_job_binding_lint.py','--job','tests/fixtures/v457/generation_job.character.valid.yaml','--registry',str(registry),'--named-mention-mode','--json'])
with tempfile.TemporaryDirectory() as td:
    bad=Path(td)/'bad.yaml'; d=yload(registry)
    for x in d['assets']:
        if x['asset_id']=='COLOR-SCENE-01': x['status']='QC_PASS_WAITING_APPROVAL'
    ywrite(bad,d); run([PY,'validators/scene_color_binding_lint.py','--registry',str(bad),'--json'],expect=1)
    bad2=Path(td)/'bad2.yaml'; d=yload(registry)
    for x in d['assets']:
        if x['asset_id']=='COLOR-SCENE-01': x['scene_id']='SCENE-WRONG'
    ywrite(bad2,d); run([PY,'validators/scene_color_binding_lint.py','--registry',str(bad2),'--json'],expect=1)

print('SECTION_5', flush=True)
# 5. Existing approved scene card is reused/synced; only truly missing card is derived.
with tempfile.TemporaryDirectory() as td:
    rt=Path(td)/'gr.yaml'; st=Path(td)/'st.yaml'
    ywrite(rt,{'runtime_type':'GENERATION_RUNTIME','schema_version':1,'skill_version':'4.5.7','status':'VALID','host_capability':{'resolved_profile':'NAMED_ASSET_PLATFORM','image_generation':'AVAILABLE','video_generation':'AVAILABLE','reference_transport':'NAMED_ASSET_MENTION'},'base_color_asset_id':'COLOR-GLOBAL-01','active_job_id':None,'queue':[],'completed_job_ids':[],'blocked_job_ids':[],'scene_color_authority_map':{},'runtime_fingerprint':'x'})
    ywrite(st,{'schema_version':1,'skill_version':'4.5.7','episode_id':'EP','mode':'PRODUCTION','workflow_state':'EPISODE_ASSET_BUILD','current_scene_id':'SCENE-BAR','current_look_domain':'INTERIOR'})
    out=json.loads(run([PY,'tools/controller_engine.py','--state',str(st),'--generation-runtime',str(rt),'--registry',str(registry),'--json']))
    assert out['next_action']=='SYNC_EXISTING_SCENE_COLOR_AUTHORITY'
    synced=Path(td)/'gr2.yaml'; run([PY,'tools/generation_runtime_manager.py','--runtime',str(rt),'--action','REGISTER_COLOR','--registry',str(registry),'--asset-id','COLOR-SCENE-01','--scene-id','SCENE-BAR','--look-domain','INTERIOR','--output',str(synced)])
    assert yload(synced)['scene_color_authority_map']['SCENE-BAR:INTERIOR']=='COLOR-SCENE-01'
    onlybase=Path(td)/'onlybase.yaml'; rd=yload(registry); rd['assets']=[x for x in rd['assets'] if x['asset_id']=='COLOR-GLOBAL-01']; ywrite(onlybase,rd)
    out=json.loads(run([PY,'tools/controller_engine.py','--state',str(st),'--generation-runtime',str(rt),'--registry',str(onlybase),'--json']))
    assert out['next_action']=='DERIVE_SCENE_COLOR_AUTHORITY'

print('SECTION_6', flush=True)
# 6. Retry isolation: old candidate cannot be selected on a new attempt.
with tempfile.TemporaryDirectory() as td:
    job=Path(td)/'job.yaml'; job.write_text((ROOT/'tests/fixtures/v457/generation_job.character.valid.yaml').read_text(encoding='utf-8'),encoding='utf-8')
    def step(*a,expect=0): return run([PY,'tools/generation_job_manager.py',str(job),*a,'--write',str(job),'--json'],expect=expect)
    step('--to','READY'); step('--to','RUNNING'); step('--to','RESULT_AVAILABLE'); step('--candidate-id','C1','--tool-result-handle','native://1'); step('--to','RETRY_REQUIRED'); step('--to','READY')
    assert yload(job)['attempt_no']==2
    step('--select-candidate','C1',expect=2)

print('SECTION_7', flush=True)
# 7. Image Promotion really closes into Asset Registry, then Generation Runtime completes.
with tempfile.TemporaryDirectory() as td:
    job=Path(td)/'job.yaml'; job.write_text((ROOT/'tests/fixtures/v457/generation_job.character.valid.yaml').read_text(encoding='utf-8'),encoding='utf-8')
    def step(*a,expect=0): return run([PY,'tools/generation_job_manager.py',str(job),*a,'--write',str(job),'--json'],expect=expect)
    step('--to','READY'); step('--to','RUNNING'); step('--to','RESULT_AVAILABLE'); step('--candidate-id','C1','--tool-result-handle','native://1','--file-path','generated/candidates/JOB-CHR-A-001/01.png'); step('--to','QC_PASS_WAITING_APPROVAL'); step('--select-candidate','C1','--approval-ref','APR-1'); step('--to','APPROVED_PROMOTED')
    rd=yload(registry); rd['assets'].append({'asset_id':'CHR-A','asset_type':'CHARACTER_MASTER','status':'DRAFT','authority_role':'CHARACTER','media_kind':'IMAGE','video_usage':{'direct_input_allowed':True,'primary_visual_eligible':False}})
    rin=Path(td)/'registry.yaml'; rout=Path(td)/'registry2.yaml'; ywrite(rin,rd)
    run([PY,'tools/asset_promoter.py','--job',str(job),'--registry',str(rin),'--output',str(rout)])
    promoted=next(x for x in yload(rout)['assets'] if x['asset_id']=='CHR-A'); assert promoted['status']=='APPROVED' and promoted['generation_job_id']=='JOB-CHR-A-001' and promoted['color_authority_id']=='COLOR-GLOBAL-01'
    chainreg=Path(td)/'chain_registry.yaml'; cr=yload(rout); cr['assets']=[x for x in cr['assets'] if x['asset_id']=='CHR-A']; ywrite(chainreg,cr)
    run([PY,'validators/generation_chain_lint.py','--registry',str(chainreg),'--jobs',str(job),'--json'])
    gr=Path(td)/'gr.yaml'; gro=Path(td)/'gro.yaml'; ywrite(gr,{'runtime_type':'GENERATION_RUNTIME','schema_version':1,'skill_version':'4.5.7','status':'VALID','host_capability':{'resolved_profile':'NAMED_ASSET_PLATFORM','image_generation':'AVAILABLE','video_generation':'AVAILABLE','reference_transport':'NAMED_ASSET_MENTION'},'base_color_asset_id':'COLOR-GLOBAL-01','active_job_id':'JOB-CHR-A-001','queue':['JOB-CHR-A-001'],'completed_job_ids':[],'blocked_job_ids':[],'scene_color_authority_map':{'SCENE-BAR:INTERIOR':'COLOR-SCENE-01'},'runtime_fingerprint':'x'})
    run([PY,'tools/generation_runtime_manager.py','--runtime',str(gr),'--job',str(job),'--action','COMPLETE','--registry',str(rout),'--output',str(gro)])
    assert 'JOB-CHR-A-001' in yload(gro)['completed_job_ids'] and not yload(gro)['queue']

print('SECTION_8', flush=True)
# 8. Video Job: default direct pack uses @Shot Execution only; Scene Color remains lineage authority; job terminates at VIDEO_TAKE_CAPTURED.
with tempfile.TemporaryDirectory() as td:
    vj=Path(td)/'video.yaml'
    ywrite(vj,{'schema_version':1,'skill_version':'4.5.7','generation_job_id':'JOB-VID-017','media_kind':'VIDEO','target_asset_id':'VID-017-TAKE','target_asset_type':'VIDEO_TAKE','route':'STAGE_05_VIDEO','scene_id':'SCENE-BAR','location_entity_id':'LOC-BAR','look_domain':'INTERIOR','shot_id':'SH017','video_unit_id':'VU017','attempt_no':1,'status':'PLANNED','host_profile':'NAMED_ASSET_PLATFORM','prompt_ref':'/tmp/seedance_vu017.txt','prompt_fingerprint':'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','execution_plan_ref':'/tmp/vu017_plan.yaml','execution_plan_fingerprint':'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb','prompt_artifact_ref':'/tmp/vu017_prompt_artifact.yaml','required_bindings':[{'asset_id':'VIDEO-SH017-FIRST','role':'PRIMARY_VISUAL_CONDITIONING','binding_mode':'PRIMARY_VIEW','native_token':'@SH017视频首帧','asset_display_name':'SH017视频首帧','time_scope':'t0'}],'color_binding':{'required':False,'authority_level':'SCENE_COLOR_CARD','color_asset_id':'COLOR-SCENE-01','scene_scope':'SCENE-BAR:INTERIOR','binding_status':'NOT_REQUIRED','projection_mode':'LINEAGE_ONLY','reference_reason_code':'PRIMARY_VISUAL_INHERITS_COLOR'},'lineage':{'parent_asset_ids':['VIDEO-SH017-FIRST'],'derivation_kind':'VIDEO_FROM_SHOT_EXECUTION','source_generation_job_ids':['JOB-SH017-FRAME']},'result_handles':[],'selected_candidate_id':None,'approval_ref':None,'failure_code':None})
    run([PY,'validators/state_schema_lint.py','state/generation_job.schema.yaml',str(vj),'--json'])
    run([PY,'validators/generation_job_binding_lint.py','--job',str(vj),'--registry',str(registry),'--named-mention-mode','--json'])
    def vstep(*a,expect=0): return run([PY,'tools/generation_job_manager.py',str(vj),*a,'--write',str(vj),'--json'],expect=expect)
    vstep('--to','READY'); vstep('--to','RUNNING'); vstep('--to','RESULT_AVAILABLE'); vstep('--candidate-id','TAKE-1','--tool-result-handle','native://video/1')
    vstep('--to','QC_PASS_WAITING_APPROVAL',expect=2)
    vstep('--to','VIDEO_TAKE_CAPTURED')
    run([PY,'tools/asset_promoter.py','--job',str(vj),'--registry',str(registry),'--output',str(Path(td)/'x.yaml')],expect=2)
    gr=Path(td)/'gr.yaml'; gro=Path(td)/'gro.yaml'; ywrite(gr,{'runtime_type':'GENERATION_RUNTIME','schema_version':1,'skill_version':'4.5.7','status':'VALID','host_capability':{'resolved_profile':'NAMED_ASSET_PLATFORM','image_generation':'AVAILABLE','video_generation':'AVAILABLE','reference_transport':'NAMED_ASSET_MENTION'},'base_color_asset_id':'COLOR-GLOBAL-01','active_job_id':'JOB-VID-017','queue':['JOB-VID-017'],'completed_job_ids':[],'blocked_job_ids':[],'scene_color_authority_map':{'SCENE-BAR:INTERIOR':'COLOR-SCENE-01'},'runtime_fingerprint':'x'})
    run([PY,'tools/generation_runtime_manager.py','--runtime',str(gr),'--job',str(vj),'--action','COMPLETE','--output',str(gro)])
    assert yload(gro)['completed_job_ids']==['JOB-VID-017']

print('SECTION_9', flush=True)
# 9. Runtime compiler cannot write a fake VALID runtime that fails its own schema.
with tempfile.TemporaryDirectory() as td:
    out=Path(td)/'gen.yaml'; run([PY,'tools/runtime_compiler.py','--runtime-type','GENERATION_RUNTIME','--output',str(out)])
    run([PY,'validators/state_schema_lint.py','runtime/generation_runtime.schema.yaml',str(out),'--json'])
    out2=Path(td)/'vc.yaml'; run([PY,'tools/runtime_compiler.py','--runtime-type','VIDEO_CONDITIONING_RUNTIME','--output',str(out2)],expect=2)
    run([PY,'tools/runtime_compiler.py','--runtime-type','VIDEO_CONDITIONING_RUNTIME','--projection','tests/fixtures/v457/video_conditioning.color.valid.yaml','--output',str(out2)])

print('SECTION_10', flush=True)
# 10. Color Authority is a prompt-surface hard binding in named-asset mode.
with tempfile.TemporaryDirectory() as td:
    rt=Path(td)/'ref.yaml'; pr=Path(td)/'p.txt'
    ywrite(rt,{'bindings':[{'asset_id':'COLOR-SCENE-01','asset_display_name':'酒吧场景色卡','native_token':'@酒吧场景色卡','binding_mode':'COLOR_AUTHORITY','emit_on_prompt':True}]})
    pr.write_text('酒吧夜景。',encoding='utf-8'); run([PY,'validators/asset_mention_lint.py','--prompt',str(pr),'--runtime',str(rt)],expect=2)
    pr.write_text('@酒吧场景色卡 保持综合色一致。',encoding='utf-8'); run([PY,'validators/asset_mention_lint.py','--prompt',str(pr),'--runtime',str(rt)])

print(json.dumps({'pass':True,'version':'4.5.7','checks':['strict_reality_inheritance','environment_coverage_current_type','scene_color_scope_approval','generation_preflight_color','existing_scene_color_reuse','retry_attempt_isolation','image_promotion_registry_closure','generation_runtime_completion','stage05_video_lifecycle','video_primary_plus_color','runtime_schema_closure','color_prompt_surface_hard_binding','legacy_active_template_cleanup']},ensure_ascii=False,indent=2))
