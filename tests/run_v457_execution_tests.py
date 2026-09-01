#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, sys, tempfile, yaml
ROOT=Path(__file__).resolve().parents[1]
PY=sys.executable

def run(args, expect=0):
    p=subprocess.run(args,cwd=ROOT,text=True,capture_output=True)
    if p.returncode!=expect:
        print('$',' '.join(map(str,args))); print(p.stdout); print(p.stderr,file=sys.stderr); raise SystemExit(f'expected {expect}, got {p.returncode}')
    return p.stdout

# Architecture + schema
run([PY,'validators/v457_architecture_lint.py','--root',str(ROOT),'--json'])
run([PY,'validators/state_schema_lint.py','state/generation_job.schema.yaml','tests/fixtures/v457/generation_job.character.valid.yaml','--json'])
run([PY,'validators/state_schema_lint.py','state/asset_registry.schema.yaml','tests/fixtures/v457/asset_registry.lineage_color.valid.yaml','--json'])
run([PY,'validators/state_schema_lint.py','runtime/video_conditioning_runtime.schema.yaml','tests/fixtures/v457/video_conditioning.color.valid.yaml','--json'])
# Deterministic route dispatch
assert json.loads(run([PY,'tools/asset_route_dispatcher.py','ENVIRONMENT_COVERAGE','--json']))['route']=='ENVIRONMENT_MASTER_COVERAGE'
assert json.loads(run([PY,'tools/asset_route_dispatcher.py','SCENE_COLOR_EXTENSION_CARD','--json']))['route']=='SCENE_COLOR_CARD_DERIVATION'
assert json.loads(run([PY,'tools/asset_route_dispatcher.py','VIDEO_SHOT_EXECUTION_FRAME','--json']))['route']=='STAGE_04_VIDEO_CONDITIONING_BUILD'
assert json.loads(run([PY,'tools/asset_route_dispatcher.py','VIDEO_TAKE','--json']))['route']=='STAGE_05_VIDEO'
# Scene change automatically produces a color-card job seed from base card
with tempfile.TemporaryDirectory() as td:
    reg=Path(td)/'registry.yaml'
    rd=yaml.safe_load((ROOT/'tests/fixtures/v457/asset_registry.lineage_color.valid.yaml').read_text(encoding='utf-8'))
    rd['assets']=[x for x in rd['assets'] if x['asset_id']=='COLOR-GLOBAL-01']
    reg.write_text(yaml.safe_dump(rd,sort_keys=False,allow_unicode=True),encoding='utf-8')
    color=json.loads(run([PY,'tools/scene_color_router.py','--registry',str(reg),'--base-color-asset-id','COLOR-GLOBAL-01','--scene-id','SCENE-BAR','--look-domain','INTERIOR','--json']))
    assert color['required'] is True and color['derivation_kind']=='SCENE_COLOR_FROM_BASE' and color['parent_asset_ids']==['COLOR-GLOBAL-01']
# Controller detects a new scene/look domain and routes color first.
with tempfile.TemporaryDirectory() as td:
    st=Path(td)/'state.yaml'; gr=Path(td)/'gr.yaml'
    st.write_text(yaml.safe_dump({'schema_version':1,'skill_version':'4.5.7','episode_id':'EP01','mode':'PRODUCTION','workflow_state':'EPISODE_ASSET_BUILD','current_scene_id':'SCENE-BAR','current_look_domain':'INTERIOR'}),encoding='utf-8')
    gr.write_text(yaml.safe_dump({'runtime_type':'GENERATION_RUNTIME','schema_version':1,'skill_version':'4.5.7','status':'VALID','host_capability':{'resolved_profile':'NAMED_ASSET_PLATFORM','image_generation':'AVAILABLE','video_generation':'AVAILABLE','reference_transport':'NAMED_ASSET_MENTION'},'base_color_asset_id':'COLOR-GLOBAL-01','active_job_id':None,'queue':[],'completed_job_ids':[],'blocked_job_ids':[],'scene_color_authority_map':{},'runtime_fingerprint':'x'}),encoding='utf-8')
    reg=Path(td)/'registry.yaml'; rd=yaml.safe_load((ROOT/'tests/fixtures/v457/asset_registry.lineage_color.valid.yaml').read_text(encoding='utf-8')); rd['assets']=[x for x in rd['assets'] if x['asset_id']=='COLOR-GLOBAL-01']; reg.write_text(yaml.safe_dump(rd,sort_keys=False,allow_unicode=True),encoding='utf-8')
    nxt=json.loads(run([PY,'tools/controller_engine.py','--state',str(st),'--workflow','controller/workflow_state_machine.yaml','--generation-runtime',str(gr),'--registry',str(reg),'--json']))
    assert nxt['next_action']=='DERIVE_SCENE_COLOR_AUTHORITY' and nxt['route']=='SCENE_COLOR_CARD_DERIVATION'
# Job lifecycle: result capture is before approval/promotion
with tempfile.TemporaryDirectory() as td:
    job=Path(td)/'job.yaml'; job.write_text((ROOT/'tests/fixtures/v457/generation_job.character.valid.yaml').read_text(encoding='utf-8'),encoding='utf-8')
    def step(*args): run([PY,'tools/generation_job_manager.py',str(job),*args,'--write',str(job),'--json'])
    step('--to','READY'); step('--to','RUNNING'); step('--to','RESULT_AVAILABLE')
    step('--candidate-id','CAND-CHR-A-01','--tool-result-handle','native://img/1','--file-path','generated/candidates/JOB-CHR-A-001/01.png')
    j=yaml.safe_load(job.read_text(encoding='utf-8')); assert j['status']=='CANDIDATE_CAPTURED' and j['approval_ref'] is None
    step('--to','QC_PASS_WAITING_APPROVAL')
    # Promotion without selected candidate/approval must fail.
    run([PY,'tools/generation_job_manager.py',str(job),'--to','APPROVED_PROMOTED','--json'],expect=2)
    step('--select-candidate','CAND-CHR-A-01','--approval-ref','APR-CHR-A')
    step('--to','APPROVED_PROMOTED')
    j=yaml.safe_load(job.read_text(encoding='utf-8')); assert j['status']=='APPROVED_PROMOTED' and j['selected_candidate_id']=='CAND-CHR-A-01'
# Lineage + scene color binding including Video
run([PY,'validators/generation_chain_lint.py','--registry','tests/fixtures/v457/asset_registry.lineage_color.valid.yaml','--json'])
run([PY,'validators/scene_color_binding_lint.py','--registry','tests/fixtures/v457/asset_registry.lineage_color.valid.yaml','--conditioning-runtime','tests/fixtures/v457/video_conditioning.color.valid.yaml','--named-mention-mode','--json'])
# Adversarial: a scene-bound image without Scene Color Authority must fail.
with tempfile.TemporaryDirectory() as td:
    bad=Path(td)/'bad.yaml'
    data=yaml.safe_load((ROOT/'tests/fixtures/v457/asset_registry.lineage_color.valid.yaml').read_text(encoding='utf-8'))
    for x in data['assets']:
        if x['asset_id']=='ENV-BAR-MASTER': x['scene_color_authority_id']=None
    bad.write_text(yaml.safe_dump(data,sort_keys=False,allow_unicode=True),encoding='utf-8')
    run([PY,'validators/scene_color_binding_lint.py','--registry',str(bad),'--json'],expect=1)
# Adversarial: Video Unit cannot silently drop Scene Color Authority lineage even when direct color reference is omitted.
with tempfile.TemporaryDirectory() as td:
    bad=Path(td)/'badrt.yaml'
    data=yaml.safe_load((ROOT/'tests/fixtures/v457/video_conditioning.color.valid.yaml').read_text(encoding='utf-8'))
    data['video_units'][0]['scene_color_authority_id']=None
    bad.write_text(yaml.safe_dump(data,sort_keys=False,allow_unicode=True),encoding='utf-8')
    run([PY,'validators/scene_color_binding_lint.py','--registry','tests/fixtures/v457/asset_registry.lineage_color.valid.yaml','--conditioning-runtime',str(bad),'--json'],expect=1)
print(json.dumps({'pass':True,'version':'4.5.7','checks':['route_dispatch','scene_color_auto_derivation','generation_job_lifecycle','candidate_vs_approval','asset_lineage','video_color_authority_lineage','controller_scene_color_priority','negative_color_drop_blocked']},ensure_ascii=False,indent=2))
