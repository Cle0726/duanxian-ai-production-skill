#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, tempfile, sys, yaml
ROOT=Path(__file__).resolve().parents[1]
VAL=ROOT/'validators/video_execution_plan_lint.py'

def run(data):
    with tempfile.NamedTemporaryFile('w',encoding='utf-8',suffix='.json',delete=False) as f:
        json.dump(data,f,ensure_ascii=False); path=f.name
    cp=subprocess.run([sys.executable,str(VAL),path],capture_output=True,text=True)
    return cp.returncode, json.loads(cp.stdout)

base={
 'status':'FROZEN_FOR_COMPILE','video_execution_plan_pass':True,'duration_sec':8,'scene_bound':True,
 'reference_integrity':{'primary_visual':'SHOT_01','scene_color_authority':'COLOR_SC01','conflict_count':0,'conflicts':[]},
 'spatial_blocking':{'conflict_count':0,'conflicts':[],'subjects':[{'id':'A','critical':True,'start':'MID_LEFT','end':'MID_CENTER','moves':True,'path_proven':True}]},
 'body_prop_occupancy':{'conflict_count':0,'conflicts':[],'subjects':[{'id':'A','critical':True,'human':True,'occupancy_clear':True}]},
 'timing':{'fits':True},'conflicts':[],
 'windows':[
  {'id':'W1','start':0,'end':4,'primary_action':'A停步并看向门口','performance_required':True,'trigger':'门外声响','perception':'先听见','micro_expression':'眼神先停住、眉心轻收','response':'身体半转确认','dominant_camera_moves':1,'camera':{'landing':'中近景保持A'}},
  {'id':'W2','start':4,'end':8,'primary_action':'A迈向门口后停住','performance_required':False,'dominant_camera_moves':1,'camera':{'landing':'中景门口落点'}}
 ],
 'ending_state':{'landing':'A停在门内侧，右手离门把半掌距离'},
 'storyboard_handoff':{'source_storyboard_asset_ids':['SB-SH1'],'items':[{'field':'CAMERA_MOTION','applicability':'REQUIRED','source_text':'单一缓慢侧移','prompt_anchor':'单一缓慢侧移'},{'field':'TIMING','applicability':'REQUIRED','source_text':'0–2s门外声响触发','prompt_anchor':'0–2s门外声响触发'},{'field':'CUT_NOCUT','applicability':'REQUIRED','source_text':'全镜头NO CUT，连续完成','prompt_anchor':'全镜头NO CUT，连续完成'},{'field':'ACTION_BEAT','applicability':'REQUIRED','source_text':'先听见、再确认、再准备、再移动、最后停稳','prompt_anchor':'先听见、再确认、再准备、再移动、最后停稳'},{'field':'PERFORMANCE','applicability':'REQUIRED','source_text':'眼睑轻收、眉心轻紧','prompt_anchor':'眼睑轻收、眉心轻紧'},{'field':'EYELINE','applicability':'REQUIRED','source_text':'视线转移到门口','prompt_anchor':'被门外声响牵引到门口'},{'field':'SHOT_RELATION','applicability':'NOT_APPLICABLE','reason':'单镜头内无跨镜关系'},{'field':'LANDING','applicability':'REQUIRED','source_text':'人物停在门内侧','prompt_anchor':'人物停在门内侧'}]},
 'assembly_order':'CHRONOLOGICAL_CAUSAL'
}
rc,out=run(base); assert rc==0 and out['pass'],out
bad=json.loads(json.dumps(base)); bad['windows'][0]['dominant_camera_moves']=3; bad['windows'][0]['camera_previs_proven']=False
rc,out=run(bad); assert rc!=0 and any(x['type']=='EXECUTION_CAMERA_COMPETITION_CONFLICT' for x in out['issues']),out
bad=json.loads(json.dumps(base)); bad['spatial_blocking']['subjects'][0]['path_proven']=False
rc,out=run(bad); assert rc!=0 and any(x['type']=='EXECUTION_MOTION_CORRIDOR_UNPROVEN' for x in out['issues']),out
bad=json.loads(json.dumps(base)); bad['timing']['fits']=False
rc,out=run(bad); assert rc!=0 and any(x['type']=='EXECUTION_TIMING_BUDGET_OVERFLOW' for x in out['issues']),out
bad=json.loads(json.dumps(base)); bad['windows'][0].pop('micro_expression')
rc,out=run(bad); assert rc!=0 and any(x['type']=='EXECUTION_MICRO_EXPRESSION_GAP' for x in out['issues']),out

long=json.loads(json.dumps(base)); long['duration_sec']=16; long['windows'][1]['end']=16
rc,out=run(long); assert rc!=0 and any(x['type']=='LONG_VIDEO_QUOTA_CONFIRMATION_REQUIRED' for x in out['issues']),out
long['long_video_quota_confirmation']={'threshold_sec':15,'question_asked':True,'user_response':'HAS_QUOTA','confirmed_by':'USER','confirmation_ref':'USER-Q-16'}
rc,out=run(long); assert rc==0 and out['pass'],out

route=yaml.safe_load((ROOT/'controller/route_registry.yaml').read_text(encoding='utf-8'))['routes']['STAGE_05_VIDEO']
assert 'templates/video_execution_plan.md' in route['compile_runtime_from_source']
assert 'validators/video_execution_plan_lint.py' in route['validators']
assert 'VIDEO_EXECUTION_PLAN_PASS' in route['produces_fields']
wf=yaml.safe_load((ROOT/'controller/workflow_state_machine.yaml').read_text(encoding='utf-8'))
t23=[x for x in wf['transitions'] if x['id']=='T23B_VIDEO_READY'][0]
assert 'VIDEO_EXECUTION_PLAN_PASS' in t23['requires']
assert 'LONG_VIDEO_QUOTA_CONFIRMATION_PASS' in t23['requires']
pt=(ROOT/'templates/video_prompt_template.md').read_text(encoding='utf-8')
assert 'Integrated Timeline Assembly' in pt and '20个彼此割裂的栏目' in pt
pc=(ROOT/'templates/prompt_compiler.md').read_text(encoding='utf-8')
assert 'SOLVE FIRST → WRITE SECOND' in pc
assert '视觉Reference已经承担的身份/空间/综合色/风格/构图不再长篇文字复述' not in pc
print('V4.5.7 EXECUTION PLAN TESTS: PASS')
