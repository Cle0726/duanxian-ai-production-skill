#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, tempfile, sys, yaml, hashlib
ROOT=Path(__file__).resolve().parents[1]; PY=sys.executable

def run(args,expect=0):
    cp=subprocess.run(args,cwd=ROOT,capture_output=True,text=True)
    if cp.returncode!=expect:
        print('$',' '.join(map(str,args))); print(cp.stdout); print(cp.stderr,file=sys.stderr); raise SystemExit(f'expected {expect}, got {cp.returncode}')
    return cp

def ywrite(p,d): Path(p).write_text(yaml.safe_dump(d,sort_keys=False,allow_unicode=True),encoding='utf-8')
def yload(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))

def prompt_text():
    head='''@SH017镜头执行图 @酒吧场景色卡\n镜头目标：让观众确认人物听见门外声响后决定靠近门口，同时保持不安但克制的表演。\n全镜头NO CUT，连续完成。\n起始状态：t=0，人物站在中景左侧，身体微侧，右手自然垂落，左手靠近衣摆。\n人物外观/服装：保持已批准人物身份、发型和当前湿润外套，衣料重量与雨水状态连续。\n场景空间：前景吧台边缘，中景人物，后景门口；入口、出口与Anchor保持既定几何。\n道具状态：杯子留在吧台，人物没有持杯，Holder关系不得变化。\n构图：人物位于左侧三分区，门口留出视觉压力空间。\n景别：中近景起步，结束保持中景。\n摄影机：机位略低于眼平，单一缓慢侧移，Focus从人物眼神保持到门口方向，最后Landing稳定。\n时间轴：0–2s门外声响触发；2–5s人物感知、迟疑、视线转移；5–8s迈步靠近并停稳。\n逐段动作：动作先有准备与重心变化，再迈步，减速后停稳，不瞬移。\n表演：Trigger后先停顿，眼睑轻收、眉心轻紧，下颌有短暂紧张，Processing Delay后才行动。\n视线：先固定前方，再被门外声响牵引到门口，Landing保持门把附近。\n肢体占用：右手空闲、左手不持物，左右脚按步态交替承重。\n物理反馈：外套与发梢在身体转向后有轻微惯性余摆，鞋底落地与重心转移一致。\n环境动态：雨声持续，门缝微光稳定，远处灯光只有轻微环境闪动。\n光影综合色：遵守对应场景综合色，冷环境光与室内暖边缘光保持主体分离，主光方向不漂移。\n声音：门外声响先于人物反应，脚步Foley与落脚同步，环境雨声维持。\n对白/呼吸：无对白；迟疑阶段出现一次有剧情原因的浅呼吸，停稳后恢复自然。\n结尾状态：人物停在门内侧，右手距离门把半掌，身体朝门口，摄影机Landing在稳定中景。\n必要限制：禁止人物身份漂移、手脚瞬移、无因换手、空间左右翻转和镜头突然切换。\n'''
    filler='人物的动作顺序必须保持因果连续：先听见、再确认、再准备、再移动、最后停稳；每一步都保留自然的处理延迟和身体重量感。摄影机只服务这一条表演主线，不额外加入环绕、升降或无动机快速推拉。场景空间、门口Anchor、吧台遮挡和人物落点必须保持一致，衣料、头发、雨水与脚步反馈都跟随真实动作发生。'
    s=head
    while len(''.join(s.split()))<2700: s+=filler
    return s

print('SECTION_A_GATE_PRODUCERS')
run([PY,'validators/gate_producer_lint.py','--workflow','controller/workflow_state_machine.yaml','--registry','controller/gate_producer_registry.yaml'])

print('SECTION_B_STORYBOARD_GENERATION_SPINE')
cp=run([PY,'tools/asset_route_dispatcher.py','STORYBOARD_CLEAN_PANEL','--json']); assert json.loads(cp.stdout)['route']=='STAGE_04_STORYBOARD'
route=yload(ROOT/'controller/route_registry.yaml')['routes']['STAGE_04_STORYBOARD']
assert 'GENERATION_JOB_DISPATCH' in route['callable_subroutes'] and 'GENERATION_JOB_EXECUTOR' in route['callable_subroutes']
assert 'STORYBOARD_GENERATION_JOBS_QC_READY' in route['produces_fields']
assert 'MANDATORY_STORYBOARD_APPROVED_COVERAGE_PASS' in route['produces_fields']
with tempfile.TemporaryDirectory() as td:
    td=Path(td); reg=td/'registry.yaml'; job=td/'job.yaml'; shot=td/'shot.yaml'; apr=td/'approval.yaml'; img=td/'panel.png'; img.write_bytes(b'not-a-real-image-but-a-real-result-handle')
    ywrite(reg,{'schema_version':7,'skill_version':'4.5.7','assets':[
      {'asset_id':'COLOR-SC1','asset_type':'SCENE_COLOR_CARD','scene_id':'SC1','look_domain':'INTERIOR','status':'APPROVED','authority_role':'COLOR_AUTHORITY','video_usage':{'direct_input_allowed':True,'primary_visual_eligible':False}},
      {'asset_id':'SB-SH1','asset_type':'STORYBOARD_CLEAN_PANEL','scene_id':'SC1','shot_id':'SH1','status':'DRAFT','authority_role':'STORYBOARD','layout_type':'CLEAN_PANEL','storyboard_render_mode':'WHITE_LINE_STORYBOARD_ONLY','storyboard_cleanliness':{'visible_text':False,'visible_numbers':False,'arrows_or_motion_lines':False,'timecode':False,'shot_or_panel_labels':False,'cut_or_camera_labels':False,'caption_boxes':False,'subtitle_or_logo':False},'video_usage':{'direct_input_allowed':False,'primary_visual_eligible':False}}
    ]})
    ywrite(shot,{'schema_version':3,'skill_version':'4.5.7','episode_id':'EP1','scene_id':'SC1','segment_id':'SEG1','shot_id':'SH1','entry_mode':'SCENE_OPENING','storyboard':{'mandatory_coverage_planned':True,'required_panel_count':1,'mandatory_panel_asset_ids':['SB-SH1'],'status':'IN_PROGRESS'}})
    ywrite(job,{'schema_version':1,'skill_version':'4.5.7','generation_job_id':'JOB-SB1','media_kind':'IMAGE','target_asset_id':'SB-SH1','target_asset_type':'STORYBOARD_CLEAN_PANEL','route':'STAGE_04_STORYBOARD','scene_id':'SC1','shot_id':'SH1','video_unit_id':'VU1','attempt_no':1,'status':'PLANNED','host_profile':'NAMED_ASSET_PLATFORM','prompt_ref':'storyboard_prompt.txt','prompt_fingerprint':'a'*64,'required_bindings':[],'color_binding':{'required':False,'authority_level':'SCENE_COLOR_CARD','color_asset_id':'COLOR-SC1','scene_scope':'SC1:INTERIOR','binding_status':'NOT_REQUIRED','projection_mode':'VALUE_LIGHTING_LINEAGE_ONLY'},'lineage':{'parent_asset_ids':['COLOR-SC1'],'derivation_kind':'OTHER','source_generation_job_ids':[]},'result_handles':[],'selected_candidate_id':None,'approval_ref':None,'failure_code':None,'look_domain':'INTERIOR'})
    run([PY,'validators/generation_job_binding_lint.py','--job',str(job),'--registry',str(reg),'--named-mention-mode','--json'])
    def step(*args): run([PY,'tools/generation_job_manager.py',str(job),*args,'--write',str(job),'--json'])
    fp=hashlib.sha256(img.read_bytes()).hexdigest()
    step('--to','READY'); step('--to','RUNNING'); step('--to','RESULT_AVAILABLE'); step('--candidate-id','SB-C1','--file-path',str(img),'--fingerprint',fp); step('--select-candidate','SB-C1'); step('--to','QC_PASS_WAITING_APPROVAL')
    run([PY,'validators/storyboard_coverage_lint.py','--registry',str(reg),'--shot-state',str(shot),'--job',str(job),'--phase','qc'])
    run([PY,'validators/storyboard_coverage_lint.py','--registry',str(reg),'--shot-state',str(shot),'--job',str(job),'--phase','approved'],expect=2)
    ywrite(apr,{'schema_version':1,'skill_version':'4.5.7','approval_id':'APR-SB1','artifact_id':'STORYBOARD_SET:SEG1','artifact_status_before':'STORYBOARD_QC_PASSED_WAITING_APPROVAL','decision':'APPROVED','approved_by':'USER','approved_at':'2026-08-21T00:00:00Z','evidence_refs':['SB-SH1'],'approved_asset_ids':['SB-SH1'],'approved_asset_fingerprints':{'SB-SH1':fp},'note':None})
    step('--approval-ref','APR-SB1'); step('--to','APPROVED_PROMOTED')
    out=td/'reg2.yaml'; run([PY,'tools/asset_promoter.py','--job',str(job),'--registry',str(reg),'--output',str(out)])
    run([PY,'validators/clean_storyboard_contract_lint.py','--registry',str(out)])
    run([PY,'validators/storyboard_coverage_lint.py','--registry',str(out),'--shot-state',str(shot),'--job',str(job),'--phase','approved','--approval-record',str(apr)])
    assert next(x for x in yload(out)['assets'] if x['asset_id']=='SB-SH1')['status']=='APPROVED'

print('SECTION_C_PLAN_FINGERPRINT_AND_STALE')
base={'status':'FROZEN_FOR_COMPILE','video_execution_plan_pass':True,'duration_sec':8,'scene_bound':True,'reference_integrity':{'primary_visual':'SHOT1','scene_color_authority':'COLOR1','conflict_count':0,'conflicts':[]},'spatial_blocking':{'conflict_count':0,'conflicts':[],'subjects':[{'id':'A','critical':True,'start':'L','end':'C','moves':True,'path_proven':True}]},'body_prop_occupancy':{'conflict_count':0,'conflicts':[],'subjects':[{'id':'A','critical':True,'human':True,'occupancy_clear':True}]},'timing':{'fits':True},'conflicts':[],'windows':[{'id':'W1','start':0,'end':4,'primary_action':'A看门','performance_required':True,'trigger':'声响','perception':'听见','micro_expression':'眼神停住','response':'半转','dominant_camera_moves':1,'camera':{'landing':'中近景'}},{'id':'W2','start':4,'end':8,'primary_action':'A靠近','performance_required':False,'dominant_camera_moves':1,'camera':{'landing':'中景'}}],'ending_state':{'landing':'A停在门内'},'storyboard_handoff':{'source_storyboard_asset_ids':['SB-SH1'],'items':[{'field':'CAMERA_MOTION','applicability':'REQUIRED','source_text':'单一缓慢侧移','prompt_anchor':'单一缓慢侧移'},{'field':'TIMING','applicability':'REQUIRED','source_text':'0–2s门外声响触发','prompt_anchor':'0–2s门外声响触发'},{'field':'CUT_NOCUT','applicability':'REQUIRED','source_text':'全镜头NO CUT，连续完成','prompt_anchor':'全镜头NO CUT，连续完成'},{'field':'ACTION_BEAT','applicability':'REQUIRED','source_text':'先听见、再确认、再准备、再移动、最后停稳','prompt_anchor':'先听见、再确认、再准备、再移动、最后停稳'},{'field':'PERFORMANCE','applicability':'REQUIRED','source_text':'眼睑轻收、眉心轻紧','prompt_anchor':'眼睑轻收、眉心轻紧'},{'field':'EYELINE','applicability':'REQUIRED','source_text':'视线转移到门口','prompt_anchor':'被门外声响牵引到门口'},{'field':'SHOT_RELATION','applicability':'NOT_APPLICABLE','reason':'单镜头内无跨镜关系'},{'field':'LANDING','applicability':'REQUIRED','source_text':'人物停在门内侧','prompt_anchor':'人物停在门内侧'}]},'assembly_order':'CHRONOLOGICAL_CAUSAL'}
with tempfile.TemporaryDirectory() as td:
    td=Path(td); raw=td/'raw.json'; frozen=td/'plan.yaml'; cur=td/'current.yaml'; raw.write_text(json.dumps(base,ensure_ascii=False),encoding='utf-8')
    run([PY,'tools/video_execution_plan_freezer.py','--plan',str(raw),'--output',str(frozen),'--execution-plan-id','PLAN1','--video-unit-id','VU1','--shot-id','SH1','--scene-id','SC1','--director-fp','D1','--storyboard-fp','S1','--shot-execution-fp','X1','--scene-color-fp','C1','--world-state-fp','W1'])
    run([PY,'validators/state_schema_lint.py','state/video_execution_plan.schema.yaml',str(frozen),'--json'])
    ywrite(cur,{'director':'D1','storyboard':'S1','shot_execution':'X1','scene_color':'C1','world_state':'W1'}); run([PY,'validators/video_execution_plan_fingerprint_lint.py','--plan',str(frozen),'--current',str(cur)])
    ywrite(cur,{'director':'D1','storyboard':'S2','shot_execution':'X1','scene_color':'C1','world_state':'W1'}); run([PY,'validators/video_execution_plan_fingerprint_lint.py','--plan',str(frozen),'--current',str(cur)],expect=2)

    print('SECTION_D_PROMPT_ARTIFACT_VIDEO_JOB_HARD_BIND')
    prompt=td/'master.txt'; prompt.write_text(prompt_text(),encoding='utf-8'); pa=td/'prompt_artifact.yaml'
    voice_plan=td/'voice_plan.yaml'; voice_handoff=td/'voice_handoff.yaml'
    ywrite(voice_plan,{'schema_version':1,'skill_version':'4.5.7','voice_direction_plan_id':'VDP-NONE','episode_id':'EP1','sequence_id':'SEQ1','scene_id':'SC1','source_performance_ref':None,'source_screenplay_ref':None,'dialogue_required':False,'coverage':{'declared_dialogue_line_ids':[],'important_line_ids':[],'excluded_lines':[]},'lines':[],'status':'NOT_REQUIRED','plan_fingerprint':None})
    run([PY,'tools/voice_direction_prompt_compiler.py','--plan',str(voice_plan),'--video-unit-id','VU1','--shot-id','SH1','--output',str(voice_handoff),'--handoff-id','VPH-NONE'])
    run([PY,'tools/video_prompt_artifact.py','--prompt',str(prompt),'--execution-plan',str(frozen),'--output',str(pa),'--prompt-id','PROMPT1','--video-unit-id','VU1','--shot-id','SH1','--segment-type','NON_COMBAT','--voice-plan',str(voice_plan),'--voice-handoff',str(voice_handoff)])
    run([PY,'validators/state_schema_lint.py','state/video_prompt_artifact.schema.yaml',str(pa),'--json'])
    pad=yload(pa); ep=yload(frozen)
    bad=td/'bad_video_job.yaml'; ywrite(bad,{'schema_version':1,'skill_version':'4.5.7','generation_job_id':'JOB-V1','media_kind':'VIDEO','target_asset_id':'TAKE1','target_asset_type':'VIDEO_TAKE','route':'STAGE_05_VIDEO','scene_id':'SC1','shot_id':'SH1','video_unit_id':'VU1','attempt_no':1,'status':'PLANNED','required_bindings':[],'color_binding':{'required':True,'authority_level':'SCENE_COLOR_CARD','color_asset_id':'COLOR1','scene_scope':'SC1:INTERIOR','binding_status':'BOUND'},'lineage':{'parent_asset_ids':['SHOT1'],'derivation_kind':'VIDEO_FROM_SHOT_EXECUTION','source_generation_job_ids':[]}})
    run([PY,'validators/state_schema_lint.py','state/generation_job.schema.yaml',str(bad),'--json'],expect=1)
    run([PY,'tools/generation_job_manager.py',str(bad),'--to','READY','--write',str(bad),'--json'],expect=2)
    good=td/'good_video_job.yaml'; data=yload(bad); data.update({'prompt_ref':pad['prompt_ref'],'prompt_fingerprint':pad['prompt_fingerprint'],'prompt_artifact_ref':str(pa.resolve()),'execution_plan_ref':str(frozen.resolve()),'execution_plan_fingerprint':ep['execution_plan_fingerprint'],'result_handles':[],'selected_candidate_id':None,'approval_ref':None,'failure_code':None}); ywrite(good,data)
    run([PY,'validators/state_schema_lint.py','state/generation_job.schema.yaml',str(good),'--json'])
    run([PY,'validators/video_generation_job_prompt_lint.py','--job',str(good),'--prompt-artifact',str(pa),'--execution-plan',str(frozen)])
    run([PY,'tools/generation_job_manager.py',str(good),'--to','READY','--write',str(good),'--json'])

print('SECTION_E_ENDING_FRAME_NEXT_UNIT_LOOP')
with tempfile.TemporaryDirectory() as td:
    td=Path(td); frame=td/'ending.png'; frame.write_bytes(b'real-ending-frame-bytes'); snap=td/'snap.yaml'; exitst=td/'exit.yaml'; ywrite(exitst,{'actor_state':{'A':{'position':'door_inside'}},'screen_direction_state':{'A':'RIGHT'}})
    run([PY,'tools/ending_frame_capture.py','--ending-frame-path',str(frame),'--source-video-fingerprint','1'*64,'--extraction-proof-ref','TEST_PLATFORM_EXTRACT_PROOF','--output-frame',str(td/'captured.png'),'--snapshot-output',str(snap),'--episode-id','EP1','--video-ref','VID1','--snapshot-id','SNAP1','--scene-id','SC1','--segment-id','VU1','--shot-id','SH1','--exit-state',str(exitst)])
    run([PY,'validators/state_schema_lint.py','state/continuity_snapshot.schema.yaml',str(snap),'--json'])
    st=td/'state.yaml'; out=td/'state2.yaml'; ywrite(st,{'schema_version':1,'skill_version':'4.5.7','episode_id':'EP1','mode':'PRODUCTION','workflow_state':'ENDING_FRAME_APPROVED','current_segment_id':'VU1','video_units':{'ordered_ids':['VU1','VU2'],'completed_ids':[],'current_video_unit_id':'VU1','next_video_unit_id':'VU2','all_units_complete':False}})
    run([PY,'tools/video_unit_advance.py','--state',str(st),'--snapshot',str(snap),'--output',str(out)])
    sd=yload(out); assert sd['workflow_state']=='ENDING_FRAME_APPROVED' and sd['current_segment_id']=='VU2' and sd['video_units']['next_video_unit_available'] is True and sd['previous_approved_ending_frame']['fingerprint']
    wf=yload(ROOT/'controller/workflow_state_machine.yaml'); tnext=next(x for x in wf['transitions'] if x['id']=='T27B_ADVANCE_VIDEO_UNIT'); assert tnext['to']=='STORYBOARD_IN_PROGRESS'; tpost=next(x for x in wf['transitions'] if x['id']=='T28_POST'); assert tpost['from']=='ENDING_FRAME_APPROVED' and 'NO_REMAINING_VIDEO_UNITS' in tpost['requires']

print(json.dumps({'pass':True,'checks':['gate_producers','storyboard_real_generation','execution_plan_fingerprint_stale','video_prompt_artifact_hard_bind','ending_frame_next_unit_loop']},ensure_ascii=False,indent=2))
