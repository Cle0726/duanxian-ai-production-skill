#!/usr/bin/env python3
from __future__ import annotations
import copy, subprocess, sys, tempfile
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parent.parent
PYEX=sys.executable

def ywrite(p,d): Path(p).write_text(yaml.safe_dump(d,sort_keys=False,allow_unicode=True),encoding='utf-8')
def run(cmd,expect):
    cp=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True,timeout=30)
    print('$',' '.join(map(str,cmd))); print(cp.stdout)
    if cp.returncode!=expect: raise AssertionError(f'expected {expect}, got {cp.returncode}')
    return cp.stdout

def bundle(criticality='CRITICAL',subject=True):
    master={'asset_id':'CM','asset_type':'CHARACTER_MASTER','status':'APPROVED','authority_role':'CHARACTER_IDENTITY','native_token':'@X','video_usage':{'direct_input_allowed':True,'primary_visual_eligible':False}}
    if subject: master['subject_entity_id']='CHAR_X'
    reg={'schema_version':7,'skill_version':'4.5.7','assets':[{'asset_id':'PV','asset_type':'VIDEO_SHOT_EXECUTION_FRAME','status':'APPROVED_VIDEO_CONDITIONING','authority_role':'PRIMARY_VISUAL','fingerprint':'p'*64,'layout_type':'SINGLE_FRAME','video_usage':{'direct_input_allowed':True,'primary_visual_eligible':True}},master]}
    bm={'schema_version':1,'skill_version':'4.5.7','binding_map_id':'B','sequence_id':'SEQ','status':'LOCKED','frame_projection_derived_from_camera':True,'slots':[{'slot_id':'H_X','slot_kind':'HUMAN','entity_id':'CHAR_X','entity_type':'CHARACTER','prompt_entity_label':'X','visual_owner':'CHARACTER_CANON','criticality':criticality,'direct_reference_policy':'AUTO_MINIMUM_SUFFICIENT','approved_asset_ids':['CM'],'preferred_asset_id':'CM'}],'panel_states':[{'panel_asset_id':'SB','shot_id':'SH','entity_states':[{'slot_id':'H_X','frame_region':'CENTER_MG'}]}]}
    rt={'runtime_type':'VIDEO_CONDITIONING_RUNTIME','schema_version':2,'skill_version':'4.5.7','status':'VALID','scope':{},'source_fingerprints':{},'runtime_fingerprint':'f'*64,'video_units':[{'video_unit_id':'VU','shot_ids':['SH'],'conditioning_strategy':'FIRST_FRAME','primary_assets':[{'asset_id':'PV','role':'VIDEO_SHOT_EXECUTION_FRAME','approval_status':'APPROVED_VIDEO_CONDITIONING','direct_video_eligible':True}],'required_reference_bindings':[],'reference_budget':{'policy':'MINIMUM_SUFFICIENT_REFERENCE_SET','selected_direct_reference_ids':[]},'qc_status':'PASS'}],'readiness':'PASS','invalidation_triggers':[]}
    ass={'schema_version':1,'skill_version':'4.5.7','assessment_id':'A','shot_id':'SH','video_unit_id':'VU','primary_visual_asset_id':'PV','source_primary_visual_fingerprint':'p'*64,'target_platform_profile_id':'P','platform_scale':{'evaluation_basis':'PLATFORM_PROFILE_SIMULATION','effective_width_px':960,'effective_height_px':540,'preview_path':'scaled.png','preview_manifest_ref':'scaled.json'},'characters':[],'status':'PASS'}
    return reg,bm,rt,ass

def lint(td,reg,bm,rt,ass,expect):
    for n,d in [('reg',reg),('bm',bm),('rt',rt),('ass',ass)]: ywrite(td/f'{n}.yaml',d)
    return run([PYEX,'validators/identity_readability_lint.py','--assessment',str(td/'ass.yaml'),'--binding-map',str(td/'bm.yaml'),'--runtime',str(td/'rt.yaml'),'--registry',str(td/'reg.yaml')],expect)

with tempfile.TemporaryDirectory() as x:
    td=Path(x)
    print('A SUPPORT NAMED HUMAN MAY NOT BYPASS')
    reg,bm,rt,ass=bundle('SUPPORT'); out=lint(td,reg,bm,rt,ass,2); assert 'IDENTITY_READABILITY_ASSESSMENT_MISSING' in out

    print('B DECLARED PASS NEEDS REAL SCALE/FACE/CONFIDENCE EVIDENCE')
    reg,bm,rt,ass=bundle(); ass['platform_scale'].pop('preview_manifest_ref'); ass['characters']=[{'entity_id':'CHAR_X','required_for_identity':True,'visibility_status':'VISIBLE','identity_readability_verdict':'PASS','identity_match_confidence':'LOW','evidence_ref':'VE','reason':'declared pass','direct_identity_authority_asset_id':None}]
    out=lint(td,reg,bm,rt,ass,2); assert 'IDENTITY_READABILITY_SCALE_EVIDENCE_MISSING' in out and 'IDENTITY_READABILITY_PASS_FACE_EVIDENCE_MISSING' in out and 'IDENTITY_READABILITY_PASS_CONFIDENCE_TOO_LOW' in out

    print('C SUBJECTLESS MASTER MAY NOT SUBSTITUTE IDENTITY')
    reg,bm,rt,ass=bundle(subject=False); rt['video_units'][0]['required_reference_bindings']=[{'asset_id':'CM','role':'CHARACTER_IDENTITY','native_token':'@X','binding_status':'BOUND'}]; rt['video_units'][0]['reference_budget']['selected_direct_reference_ids']=['CM']; ass['characters']=[{'entity_id':'CHAR_X','required_for_identity':True,'visibility_status':'VISIBLE','face_box_at_effective_scale_px':{'x':10,'y':10,'width':12,'height':14},'identity_readability_verdict':'FAIL','identity_match_confidence':'LOW','evidence_ref':'VE','reason':'too small','direct_identity_authority_asset_id':'CM'}]; ass['status']='BLOCKED'
    out=lint(td,reg,bm,rt,ass,2); assert 'IDENTITY_AUTHORITY_ENTITY_OR_ROLE_MISMATCH' in out

    print('D ASSESSMENT STATUS MUST MATCH COMPUTED STATE')
    reg,bm,rt,ass=bundle(); ass['characters']=[{'entity_id':'CHAR_X','required_for_identity':True,'visibility_status':'VISIBLE','face_box_at_effective_scale_px':{'x':10,'y':10,'width':40,'height':44},'identity_readability_verdict':'PASS','identity_match_confidence':'HIGH','evidence_ref':'VE','reason':'readable','direct_identity_authority_asset_id':None}]; ass['status']='BLOCKED'
    out=lint(td,reg,bm,rt,ass,2); assert 'IDENTITY_READABILITY_STATUS_MISMATCH' in out

    print('E RESOLVER CANNOT BAKE HUMAN WITHOUT READABILITY ASSESSMENT')
    reg,bm,rt,ass=bundle(); req={'primary_visual_asset_id':'PV','slot_requests':[{'slot_id':'H_X','resolution_mode':'PRIMARY_VISUAL_BAKED','reason':'claimed baked','coverage_evidence_ref':'VE','prompt_identity_anchor':'X身份保持','blocking_anchor':'X位于中景中央位置','action_anchor':'X保持站立动作'}]}
    for n,d in [('reg',reg),('bm',bm),('req',req)]: ywrite(td/f'{n}2.yaml',d)
    out=run([PYEX,'tools/entity_binding_reference_resolver.py','--binding-map',str(td/'bm2.yaml'),'--registry',str(td/'reg2.yaml'),'--request',str(td/'req2.yaml')],2); assert 'IDENTITY_READABILITY_ASSESSMENT_REQUIRED' in out

print('IDENTITY READABILITY ADVERSARIAL LOGIC TESTS PASS')
