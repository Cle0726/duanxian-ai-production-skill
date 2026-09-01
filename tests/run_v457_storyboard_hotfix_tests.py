#!/usr/bin/env python3
from pathlib import Path
import copy, hashlib, json, subprocess, sys, tempfile, yaml
ROOT=Path(__file__).resolve().parents[1]; PY=sys.executable

def run(args,expect=0):
    cp=subprocess.run(args,cwd=ROOT,capture_output=True,text=True,timeout=20)
    if cp.returncode!=expect:
        print('$',' '.join(map(str,args))); print(cp.stdout); print(cp.stderr,file=sys.stderr)
        raise SystemExit(f'expected {expect}, got {cp.returncode}')
    return cp

def ywrite(p,d): Path(p).write_text(yaml.safe_dump(d,sort_keys=False,allow_unicode=True),encoding='utf-8')
def jout(cp): return json.loads(cp.stdout)

print('HOTFIX_A_WORKFLOW_ORDER')
wf=yaml.safe_load((ROOT/'controller/workflow_state_machine.yaml').read_text(encoding='utf-8'))['transitions']
t19=next(x for x in wf if x['id']=='T19_STORYBOARD_QC'); t20=next(x for x in wf if x['id']=='T20_STORYBOARD_APPROVE')
assert 'STORYBOARD_GENERATION_JOBS_QC_READY' in t19['requires']
assert 'STORYBOARD_GENERATION_JOBS_PROMOTED' not in t19['requires']
assert 'USER_APPROVED_STORYBOARD' in t20['requires']
assert 'STORYBOARD_GENERATION_JOBS_PROMOTED' in t20['requires']
assert 'MANDATORY_STORYBOARD_APPROVED_COVERAGE_PASS' in t20['requires']

print('HOTFIX_B_COVERAGE_NEGATIVE_POSITIVE')
with tempfile.TemporaryDirectory() as td:
    td=Path(td); reg=td/'reg.yaml'; shot=td/'shot.yaml'; job=td/'job.yaml'; apr=td/'apr.yaml'; img=td/'p.png'; img.write_bytes(b'panel')
    shotd={'schema_version':3,'skill_version':'4.5.7','episode_id':'EP','scene_id':'SC','segment_id':'SEG','shot_id':'SH1','entry_mode':'SCENE_OPENING','storyboard':{'mandatory_coverage_planned':True,'required_panel_count':1,'mandatory_panel_asset_ids':['SB1'],'status':'IN_PROGRESS'}}
    ywrite(shot,shotd)
    ywrite(reg,{'schema_version':7,'skill_version':'4.5.7','assets':[]})
    cp=run([PY,'validators/storyboard_coverage_lint.py','--registry',str(reg),'--shot-state',str(shot),'--phase','qc'],expect=2)
    assert any(x['type']=='MANDATORY_STORYBOARD_PANEL_MISSING_FROM_REGISTRY' for x in jout(cp)['issues'])

    clean={'visible_text':False,'visible_numbers':False,'arrows_or_motion_lines':False,'timecode':False,'shot_or_panel_labels':False,'cut_or_camera_labels':False,'caption_boxes':False,'subtitle_or_logo':False}
    regd={'schema_version':7,'skill_version':'4.5.7','assets':[
        {'asset_id':'COLOR','asset_type':'SCENE_COLOR_CARD','scene_id':'SC','look_domain':'INTERIOR','status':'APPROVED','authority_role':'COLOR_AUTHORITY','color_authority_level':'SCENE_COLOR_CARD','media_kind':'IMAGE','video_usage':{'direct_input_allowed':True,'primary_visual_eligible':False}},
        {'asset_id':'SB1','asset_type':'STORYBOARD_CLEAN_PANEL','scene_id':'SC','shot_id':'SH1','status':'DRAFT','authority_role':'STORYBOARD','layout_type':'CLEAN_PANEL','storyboard_render_mode':'WHITE_LINE_STORYBOARD_ONLY','storyboard_cleanliness':clean,'media_kind':'IMAGE','video_usage':{'direct_input_allowed':True,'primary_visual_eligible':False}}
    ]}; ywrite(reg,regd)
    fp=hashlib.sha256(img.read_bytes()).hexdigest()
    jobd={'schema_version':1,'skill_version':'4.5.7','generation_job_id':'J1','media_kind':'IMAGE','target_asset_id':'SB1','target_asset_type':'STORYBOARD_CLEAN_PANEL','route':'STAGE_04_STORYBOARD','scene_id':'SC','shot_id':'SH1','video_unit_id':'VU1','attempt_no':1,'status':'CANDIDATE_CAPTURED','host_profile':'GENERIC','prompt_ref':'p.txt','prompt_fingerprint':'a'*64,'required_bindings':[],'color_binding':{'required':False,'authority_level':'SCENE_COLOR_CARD','color_asset_id':'COLOR','scene_scope':'SC:INTERIOR','binding_status':'NOT_REQUIRED','projection_mode':'VALUE_LIGHTING_LINEAGE_ONLY'},'lineage':{'parent_asset_ids':['COLOR'],'derivation_kind':'OTHER','source_generation_job_ids':[]},'result_handles':[{'candidate_id':'C1','file_path':str(img),'fingerprint':fp,'captured':True,'attempt_no':1,'eligible_for_selection':True}],'selected_candidate_id':'C1','approval_ref':None,'failure_code':None,'look_domain':'INTERIOR'}
    ywrite(job,jobd)
    cp=run([PY,'validators/storyboard_coverage_lint.py','--registry',str(reg),'--shot-state',str(shot),'--job',str(job),'--phase','qc'],expect=2)
    assert any(x['type']=='STORYBOARD_JOB_NOT_QC_READY' for x in jout(cp)['issues'])
    jobd['status']='QC_PASS_WAITING_APPROVAL'; ywrite(job,jobd)
    run([PY,'validators/storyboard_coverage_lint.py','--registry',str(reg),'--shot-state',str(shot),'--job',str(job),'--phase','qc'])

    # Approved phase cannot pass before user approval + promotion.
    run([PY,'validators/storyboard_coverage_lint.py','--registry',str(reg),'--shot-state',str(shot),'--job',str(job),'--phase','approved'],expect=2)
    aprd={'schema_version':1,'skill_version':'4.5.7','approval_id':'APR1','artifact_id':'STORYBOARD_SET:SEG','artifact_status_before':'STORYBOARD_QC_PASSED_WAITING_APPROVAL','decision':'APPROVED','approved_by':'USER','approved_at':'2026-08-21T00:00:00Z','evidence_refs':['SB1'],'approved_asset_ids':['SB1'],'approved_asset_fingerprints':{'SB1':'b'*64},'note':None}; ywrite(apr,aprd)
    jobd['status']='APPROVED_PROMOTED'; jobd['approval_ref']='APR1'; ywrite(job,jobd)
    regbad=copy.deepcopy(regd); regbad['assets'][1].update({'status':'APPROVED','generation_job_id':'J1','approval_ref':'APR1','fingerprint':fp,'fingerprint_type':'FILE_SHA256','scene_color_authority_id':'COLOR','color_authority_level':'SCENE_COLOR_CARD','color_projection_mode':'VALUE_LIGHTING_LINEAGE_ONLY'}); ywrite(reg,regbad)
    cp=run([PY,'validators/storyboard_coverage_lint.py','--registry',str(reg),'--shot-state',str(shot),'--job',str(job),'--phase','approved','--approval-record',str(apr)],expect=2)
    assert any(x['type']=='STORYBOARD_APPROVAL_FINGERPRINT_SCOPE_MISMATCH' for x in jout(cp)['issues'])
    aprd['approved_asset_fingerprints']['SB1']=fp; ywrite(apr,aprd)
    run([PY,'validators/storyboard_coverage_lint.py','--registry',str(reg),'--shot-state',str(shot),'--job',str(job),'--phase','approved','--approval-record',str(apr)])

print('HOTFIX_C_STORYBOARD_COLOR_LINEAGE_ONLY')
with tempfile.TemporaryDirectory() as td:
    td=Path(td); reg=td/'reg.yaml'; job=td/'job.yaml'
    ywrite(reg,{'schema_version':7,'skill_version':'4.5.7','assets':[{'asset_id':'COLOR','asset_type':'SCENE_COLOR_CARD','scene_id':'SC','look_domain':'INTERIOR','status':'APPROVED','authority_role':'COLOR_AUTHORITY','color_authority_level':'SCENE_COLOR_CARD','video_usage':{'direct_input_allowed':True,'primary_visual_eligible':False}}]})
    base={'schema_version':1,'skill_version':'4.5.7','generation_job_id':'J','media_kind':'IMAGE','target_asset_id':'SB','target_asset_type':'STORYBOARD_CLEAN_PANEL','route':'STAGE_04_STORYBOARD','scene_id':'SC','shot_id':'SH','attempt_no':1,'status':'PLANNED','required_bindings':[],'color_binding':{'required':False,'authority_level':'SCENE_COLOR_CARD','color_asset_id':'COLOR','scene_scope':'SC:INTERIOR','binding_status':'NOT_REQUIRED','projection_mode':'VALUE_LIGHTING_LINEAGE_ONLY'},'lineage':{'parent_asset_ids':['COLOR'],'derivation_kind':'OTHER','source_generation_job_ids':[]},'result_handles':[],'selected_candidate_id':None,'approval_ref':None,'failure_code':None,'look_domain':'INTERIOR'}
    ywrite(job,base); run([PY,'validators/generation_job_binding_lint.py','--job',str(job),'--registry',str(reg),'--json'])
    bad=copy.deepcopy(base); bad['required_bindings']=[{'asset_id':'COLOR','role':'COLOR_AUTHORITY','binding_mode':'COLOR_AUTHORITY'}]; bad['color_binding'].update({'required':True,'binding_status':'BOUND','projection_mode':'DIRECT_COLOR_REFERENCE'}); ywrite(job,bad)
    cp=run([PY,'validators/generation_job_binding_lint.py','--job',str(job),'--registry',str(reg),'--json'],expect=1)
    assert any(x['type']=='STORYBOARD_DIRECT_COLOR_REFERENCE_FORBIDDEN' for x in jout(cp)['issues'])

print('HOTFIX_D_HANDOFF_EXACT_INHERITANCE')
plan={'storyboard_handoff':{'source_storyboard_asset_ids':['SB1'],'items':[
 {'field':'CAMERA_MOTION','applicability':'REQUIRED','source_text':'摄影机缓慢右移并停在门口构图','prompt_anchor':'摄影机缓慢右移并停在门口构图'},
 {'field':'TIMING','applicability':'REQUIRED','source_text':'0到2秒保持静止，2到5秒起身','prompt_anchor':'0到2秒保持静止，2到5秒起身'},
 {'field':'CUT_NOCUT','applicability':'REQUIRED','source_text':'全镜头不切换，连续完成','prompt_anchor':'全镜头不切换，连续完成'},
 {'field':'ACTION_BEAT','applicability':'REQUIRED','source_text':'先听见，再转头，再起身','prompt_anchor':'先听见，再转头，再起身'},
 {'field':'PERFORMANCE','applicability':'REQUIRED','source_text':'先迟疑半拍再压住紧张','prompt_anchor':'先迟疑半拍再压住紧张'},
 {'field':'EYELINE','applicability':'REQUIRED','source_text':'视线从杯子转到门把','prompt_anchor':'视线从杯子转到门把'},
 {'field':'SHOT_RELATION','applicability':'NOT_APPLICABLE','reason':'单镜头无跨镜关系'},
 {'field':'LANDING','applicability':'REQUIRED','source_text':'最后停在门内侧半步','prompt_anchor':'最后停在门内侧半步'}]}}
with tempfile.TemporaryDirectory() as td:
    td=Path(td); pp=td/'plan.yaml'; good=td/'good.txt'; bad=td/'bad.txt'; ywrite(pp,plan)
    anchors='。'.join(x['prompt_anchor'] for x in plan['storyboard_handoff']['items'] if x['applicability']=='REQUIRED')
    good.write_text(anchors,encoding='utf-8'); run([PY,'validators/storyboard_to_video_prompt_handoff_lint.py','--execution-plan',str(pp),'--prompt',str(good)])
    bad.write_text('摄影机向左移动。时间轴完整。人物表演紧张。视线看向窗外。最后停在桌旁。',encoding='utf-8')
    cp=run([PY,'validators/storyboard_to_video_prompt_handoff_lint.py','--execution-plan',str(pp),'--prompt',str(bad)],expect=2)
    assert any(x['type']=='STORYBOARD_TO_VIDEO_PROMPT_HANDOFF_GAP' for x in jout(cp)['issues'])

print('HOTFIX_E_NO_MODEL_GENERATED_GRID_OR_PRIMARY_PROMOTION')
cp=run([PY,'tools/asset_route_dispatcher.py','STORYBOARD_CLEAN_SEQUENCE_BOARD','--json'],expect=2); assert jout(cp)['pass'] is False
st=(ROOT/'templates/storyboard_prompt_template.md').read_text(encoding='utf-8')
pr=(ROOT/'templates/previsualization_strategy_router.md').read_text(encoding='utf-8')
assert '到下一关键时刻' not in st
assert 'Mandatory白描Clean Storyboard Panel**禁止执行`PROMOTE_TO_VIDEO_CONDITIONING`作为Primary Visual**' in pr
assert '不得渲染综合色相' in st
assert '### 【画面 2】' not in st and '### 【剪切点】' not in st
assert 'ONE GENERATION JOB = ONE CLEAN 16:9 PANEL' in st

print(json.dumps({'pass':True,'checks':['approval_order','all_shot_real_coverage','approval_fingerprint_scope','value_lineage_only','exact_storyboard_prompt_handoff','deterministic_grid','no_storyboard_primary_promotion']},ensure_ascii=False,indent=2))
