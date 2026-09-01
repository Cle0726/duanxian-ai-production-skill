#!/usr/bin/env python3
from pathlib import Path
import copy, json, subprocess, sys, tempfile, yaml
ROOT=Path(__file__).resolve().parents[1]
PY=sys.executable
REG=ROOT/'tests/fixtures/v457/asset_registry.lineage_color.valid.yaml'

def run(args,expect=0):
    cp=subprocess.run(args,cwd=ROOT,text=True,capture_output=True)
    if cp.returncode!=expect:
        print(cp.stdout); print(cp.stderr,file=sys.stderr)
        raise SystemExit(f'expected {expect}, got {cp.returncode}: {args}')
    return cp

def ywrite(p,d): p.write_text(yaml.safe_dump(d,allow_unicode=True,sort_keys=False),encoding='utf-8')

def issue_types(cp):
    try: return {x['type'] for x in json.loads(cp.stdout).get('issues',[])}
    except Exception: return set()

base={
 'schema_version':1,'skill_version':'4.5.7','generation_job_id':'JOB-VID-BUDGET','media_kind':'VIDEO',
 'target_asset_id':'VID-017-TAKE','target_asset_type':'VIDEO_TAKE','route':'STAGE_05_VIDEO',
 'scene_id':'SCENE-BAR','location_entity_id':'LOC-BAR','look_domain':'INTERIOR','shot_id':'SH017','video_unit_id':'VU017',
 'attempt_no':1,'status':'PLANNED','host_profile':'NAMED_ASSET_PLATFORM',
 'prompt_ref':'/tmp/prompt.txt','prompt_fingerprint':'a'*64,'execution_plan_ref':'/tmp/plan.yaml','execution_plan_fingerprint':'b'*64,
 'prompt_artifact_ref':'/tmp/artifact.yaml',
 'required_bindings':[{'asset_id':'VIDEO-SH017-FIRST','role':'PRIMARY_VISUAL_CONDITIONING','binding_mode':'PRIMARY_VIEW','native_token':'@SH017视频首帧','asset_display_name':'SH017视频首帧','time_scope':'t0'}],
 'color_binding':{'required':False,'authority_level':'SCENE_COLOR_CARD','color_asset_id':'COLOR-SCENE-01','scene_scope':'SCENE-BAR:INTERIOR','binding_status':'NOT_REQUIRED','projection_mode':'LINEAGE_ONLY','reference_reason_code':'PRIMARY_VISUAL_INHERITS_COLOR'},
 'lineage':{'parent_asset_ids':['VIDEO-SH017-FIRST'],'derivation_kind':'VIDEO_FROM_SHOT_EXECUTION','source_generation_job_ids':['JOB-SH017-FRAME']},
 'result_handles':[],'selected_candidate_id':None,'approval_ref':None,'failure_code':None
}

with tempfile.TemporaryDirectory() as td:
    td=Path(td)
    # 1. Default video: one direct @ primary visual, color stays lineage-only.
    job=td/'lineage.yaml'; ywrite(job,base)
    run([PY,'validators/state_schema_lint.py','state/generation_job.schema.yaml',str(job),'--json'])
    cp=run([PY,'validators/generation_job_binding_lint.py','--job',str(job),'--registry',str(REG),'--named-mention-mode','--json'])
    assert json.loads(cp.stdout)['pass'] is True

    # 2. LINEAGE_ONLY may not secretly occupy the color-card slot.
    bad=copy.deepcopy(base)
    bad['required_bindings'].append({'asset_id':'COLOR-SCENE-01','role':'COLOR_AUTHORITY','binding_mode':'COLOR_AUTHORITY','native_token':'@酒吧场景色卡','asset_display_name':'酒吧场景色卡'})
    p=td/'lineage_with_color_ref.yaml'; ywrite(p,bad)
    cp=run([PY,'validators/generation_job_binding_lint.py','--job',str(p),'--registry',str(REG),'--named-mention-mode','--json'],expect=1)
    assert 'VIDEO_COLOR_REFERENCE_MODE_CONFLICT' in issue_types(cp)

    # 3. Direct color reference is legal only with an explicit trigger.
    direct=copy.deepcopy(base)
    direct['color_binding'].update({'required':True,'binding_status':'BOUND','projection_mode':'DIRECT_COLOR_REFERENCE','reference_reason_code':'COLOR_NARRATIVE_CRITICAL','native_token':'@酒吧场景色卡'})
    direct['required_bindings'].append({'asset_id':'COLOR-SCENE-01','role':'COLOR_AUTHORITY','binding_mode':'COLOR_AUTHORITY','native_token':'@酒吧场景色卡','asset_display_name':'酒吧场景色卡'})
    p=td/'direct.yaml'; ywrite(p,direct)
    run([PY,'validators/generation_job_binding_lint.py','--job',str(p),'--registry',str(REG),'--named-mention-mode','--json'])

    no_reason=copy.deepcopy(direct); no_reason['color_binding']['reference_reason_code']='NONE'
    p=td/'direct_no_reason.yaml'; ywrite(p,no_reason)
    cp=run([PY,'validators/generation_job_binding_lint.py','--job',str(p),'--registry',str(REG),'--named-mention-mode','--json'],expect=1)
    assert 'VIDEO_COLOR_DIRECT_REFERENCE_TRIGGER_MISSING' in issue_types(cp)

    # 4. Conditioning runtime: authority is mandatory, direct color ref is not.
    rt=yaml.safe_load((ROOT/'tests/fixtures/v457/video_conditioning.color.valid.yaml').read_text(encoding='utf-8'))
    p=td/'rt.yaml'; ywrite(p,rt)
    run([PY,'validators/scene_color_binding_lint.py','--registry',str(REG),'--conditioning-runtime',str(p),'--named-mention-mode','--json'])

    # 5. If mode says LINEAGE_ONLY but a direct color ref is still selected, fail.
    rt_bad=copy.deepcopy(rt)
    u=rt_bad['video_units'][0]
    u['required_reference_bindings'].append({'asset_id':'COLOR-SCENE-01','role':'COLOR_AUTHORITY','native_token':'@酒吧场景色卡','binding_status':'BOUND'})
    u['reference_budget']['selected_direct_reference_ids'].append('COLOR-SCENE-01')
    p=td/'rt_bad.yaml'; ywrite(p,rt_bad)
    cp=run([PY,'validators/scene_color_binding_lint.py','--registry',str(REG),'--conditioning-runtime',str(p),'--named-mention-mode','--json'],expect=1)
    its=issue_types(cp)
    assert 'VIDEO_COLOR_REFERENCE_MODE_CONFLICT' in its and 'VIDEO_COLOR_REFERENCE_BUDGET_CONFLICT' in its

    # 6. Authority lineage itself remains hard: mismatch primary visual must fail.
    reg=yaml.safe_load(REG.read_text(encoding='utf-8'))
    for a in reg['assets']:
        if a.get('asset_id')=='VIDEO-SH017-FIRST': a['scene_color_authority_id']='COLOR-GLOBAL-01'
    rp=td/'reg_bad.yaml'; ywrite(rp,reg)
    cp=run([PY,'validators/scene_color_binding_lint.py','--registry',str(rp),'--conditioning-runtime',str(p if False else td/'rt.yaml'),'--json'],expect=1)
    assert 'VIDEO_PRIMARY_COLOR_LINEAGE_MISMATCH' in issue_types(cp)

video=(ROOT/'templates/video_prompt_template.md').read_text(encoding='utf-8')
resolver=(ROOT/'templates/reference_resolver.md').read_text(encoding='utf-8')
assert 'Scene Color Card只在`DIRECT_REFERENCE`模式下额外@' in video
assert 'MINIMUM_SUFFICIENT_REFERENCE_SET' in resolver
assert 'Scene Color Card默认不预占P2槽' in resolver
print(json.dumps({'pass':True,'checks':['default_one_direct_reference','lineage_only_no_color_slot','direct_color_requires_trigger','conditioning_lineage_authority','budget_conflict_blocked','primary_color_lineage_hard']},ensure_ascii=False,indent=2))
