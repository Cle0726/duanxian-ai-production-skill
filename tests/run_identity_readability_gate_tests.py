#!/usr/bin/env python3
from __future__ import annotations
import copy, json, subprocess, sys, tempfile, hashlib
from pathlib import Path
import yaml
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parent.parent
PYEX=sys.executable

def run(cmd, expect=0):
    cp=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
    print('$',' '.join(map(str,cmd)))
    if cp.stdout: print(cp.stdout)
    if cp.stderr: print(cp.stderr)
    if cp.returncode!=expect:
        raise AssertionError(f'expected {expect}, got {cp.returncode}: {cmd}')
    return cp

def ywrite(p,d): Path(p).write_text(yaml.safe_dump(d,sort_keys=False,allow_unicode=True),encoding='utf-8')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def registry(primary='PV_SH07'):
    return {'schema_version':7,'skill_version':'4.5.7','assets':[
      {'asset_id':'PV_SH07','asset_type':'VIDEO_SHOT_EXECUTION_FRAME','status':'APPROVED_VIDEO_CONDITIONING','authority_role':'PRIMARY_VISUAL','fingerprint':'p'*64,'layout_type':'SINGLE_FRAME','video_usage':{'direct_input_allowed':True,'primary_visual_eligible':True}},
      {'asset_id':'PV_SH07_REGEN','asset_type':'VIDEO_SHOT_EXECUTION_FRAME','status':'APPROVED_VIDEO_CONDITIONING','authority_role':'PRIMARY_VISUAL','fingerprint':'r'*64,'layout_type':'SINGLE_FRAME','video_usage':{'direct_input_allowed':True,'primary_visual_eligible':True}},
      {'asset_id':'CHAR_A_MASTER','asset_type':'CHARACTER_MASTER','status':'APPROVED','authority_role':'CHARACTER_IDENTITY','subject_entity_id':'CHAR_A','native_token':'@角色A','video_usage':{'direct_input_allowed':True,'primary_visual_eligible':False}},
      {'asset_id':'CHAR_B_MASTER','asset_type':'CHARACTER_MASTER','status':'APPROVED','authority_role':'CHARACTER_IDENTITY','subject_entity_id':'CHAR_B','native_token':'@角色B','video_usage':{'direct_input_allowed':True,'primary_visual_eligible':False}},
      {'asset_id':'FMH_C_MASTER','asset_type':'FUNCTIONAL_MINOR_HUMAN_ASSET','status':'APPROVED_SCOPED_FIGURE','authority_role':'SCOPED_CHARACTER_APPEARANCE','subject_entity_id':'FMH_C','native_token':'@配角C','video_usage':{'direct_input_allowed':True,'primary_visual_eligible':False}},
      {'asset_id':'ENV_STAGE','asset_type':'ENVIRONMENT_CLEAN_CANON','status':'APPROVED','authority_role':'ENVIRONMENT_CANON','native_token':'@空舞台','video_usage':{'direct_input_allowed':True,'primary_visual_eligible':False}},
      {'asset_id':'SB_SH07','asset_type':'STORYBOARD_CLEAN_PANEL','status':'APPROVED','authority_role':'STORYBOARD','native_token':'@白描SH07','video_usage':{'direct_input_allowed':True,'primary_visual_eligible':False}},
    ]}

def binding_map():
    return {'schema_version':1,'skill_version':'4.5.7','binding_map_id':'BMAP_SH07','episode_id':'EP1','scene_id':'SC1','sequence_id':'SEQ1','status':'LOCKED','frame_projection_derived_from_camera':True,
      'slots':[
        {'slot_id':'H_A','slot_kind':'HUMAN','entity_id':'CHAR_A','entity_type':'CHARACTER','prompt_entity_label':'角色A','visual_owner':'CHARACTER_CANON','criticality':'CRITICAL','direct_reference_policy':'AUTO_MINIMUM_SUFFICIENT','approved_asset_ids':['CHAR_A_MASTER'],'preferred_asset_id':'CHAR_A_MASTER'},
        {'slot_id':'H_B','slot_kind':'HUMAN','entity_id':'CHAR_B','entity_type':'CHARACTER','prompt_entity_label':'角色B','visual_owner':'CHARACTER_CANON','criticality':'CRITICAL','direct_reference_policy':'AUTO_MINIMUM_SUFFICIENT','approved_asset_ids':['CHAR_B_MASTER'],'preferred_asset_id':'CHAR_B_MASTER'},
        {'slot_id':'H_C','slot_kind':'HUMAN','entity_id':'FMH_C','entity_type':'MINOR_HUMAN','prompt_entity_label':'配角C','visual_owner':'MINOR_HUMAN_CANON_VIEW_SET','criticality':'CRITICAL','direct_reference_policy':'AUTO_MINIMUM_SUFFICIENT','approved_asset_ids':['FMH_C_MASTER'],'preferred_asset_id':'FMH_C_MASTER'},
      ],
      'panel_states':[{'panel_asset_id':'SB_SH07','shot_id':'SH07','entity_states':[{'slot_id':'H_A','frame_region':'LEFT_MG'},{'slot_id':'H_B','frame_region':'CENTER_MG'},{'slot_id':'H_C','frame_region':'RIGHT_MG'}]}]
    }

def runtime(primary='PV_SH07', direct=()):
    b=[]
    role={'CHAR_B_MASTER':'CHARACTER_IDENTITY','FMH_C_MASTER':'SCOPED_CHARACTER_APPEARANCE','CHAR_A_MASTER':'CHARACTER_IDENTITY','ENV_STAGE':'ENVIRONMENT_CANON','SB_SH07':'STORYBOARD_CONTROL'}
    for aid in direct:
        b.append({'asset_id':aid,'role':role[aid],'native_token':'@x','binding_status':'BOUND'})
    return {'runtime_type':'VIDEO_CONDITIONING_RUNTIME','schema_version':2,'skill_version':'4.5.7','status':'VALID','scope':{},'source_fingerprints':{},'runtime_fingerprint':'f'*64,
      'video_units':[{'video_unit_id':'VU_SH07','shot_ids':['SH07'],'conditioning_strategy':'FIRST_FRAME','primary_assets':[{'asset_id':primary,'role':'VIDEO_SHOT_EXECUTION_FRAME','approval_status':'APPROVED_VIDEO_CONDITIONING','direct_video_eligible':True}], 'required_reference_bindings':b,'reference_budget':{'policy':'MINIMUM_SUFFICIENT_REFERENCE_SET','selected_direct_reference_ids':list(direct)},'qc_status':'PASS'}], 'readiness':'PASS','invalidation_triggers':[]}

def assessment(basis='PLATFORM_ACTUAL_SCALE', primary='PV_SH07', direct_b='CHAR_B_MASTER', direct_c='FMH_C_MASTER', all_pass=False):
    return {'schema_version':1,'skill_version':'4.5.7','assessment_id':'IRA_SH07','shot_id':'SH07','video_unit_id':'VU_SH07','primary_visual_asset_id':primary,'source_primary_visual_fingerprint':('r'*64 if primary.endswith('REGEN') else 'p'*64),'target_platform_profile_id':'TARGET_PLATFORM_TEST',
      'platform_scale':{'evaluation_basis':basis,'source_width_px':4096,'source_height_px':2304,'effective_width_px':960,'effective_height_px':540,'scale_factor':0.234375,'original_file_size_bytes':19922944,'preview_path':'scaled.png','preview_manifest_ref':'scaled.json'},
      'characters':[
        {'entity_id':'CHAR_A','required_for_identity':True,'visibility_status':'VISIBLE','face_box_at_effective_scale_px':{'x':100,'y':180,'width':42,'height':48},'identity_readability_verdict':'PASS','identity_match_confidence':'HIGH','evidence_ref':'VE_A','reason':'platform-scale face remains identifiable','direct_identity_authority_asset_id':None},
        {'entity_id':'CHAR_B','required_for_identity':True,'visibility_status':'VISIBLE','face_box_at_effective_scale_px':{'x':430,'y':190,'width':18,'height':21},'identity_readability_verdict':('PASS' if all_pass else 'FAIL'),'identity_match_confidence':('HIGH' if all_pass else 'LOW'),'evidence_ref':'VE_B','reason':('readable after regenerated tighter framing' if all_pass else 'face too small after platform scaling'),'direct_identity_authority_asset_id':(None if all_pass else direct_b)},
        {'entity_id':'FMH_C','required_for_identity':True,'visibility_status':'VISIBLE','face_box_at_effective_scale_px':{'x':760,'y':195,'width':15,'height':18},'identity_readability_verdict':('PASS' if all_pass else 'FAIL'),'identity_match_confidence':('HIGH' if all_pass else 'LOW'),'evidence_ref':'VE_C','reason':('readable after regenerated tighter framing' if all_pass else 'face too small after platform scaling'),'direct_identity_authority_asset_id':(None if all_pass else direct_c)},
      ],'status':('PASS' if all_pass else 'NEEDS_DIRECT_IDENTITY_SUPPORT')}

with tempfile.TemporaryDirectory() as td:
    td=Path(td)
    # deterministic platform-scale preview
    src=td/'source.png'; Image.new('RGB',(1600,900),'white').save(src)
    prev=td/'scaled.png'; mani=td/'scaled.json'
    run([PYEX,'tools/platform_scaled_readability_preview.py',str(src),'--effective-width','960','--effective-height','540','--basis','PLATFORM_PROFILE_SIMULATION','--profile-id','TEST','--output',str(prev),'--manifest-output',str(mani)])
    assert Image.open(prev).size==(960,540)

    reg=td/'registry.yaml'; bm=td/'binding.yaml'; rt=td/'runtime.yaml'; ass=td/'assessment.yaml'
    ywrite(reg,registry()); ywrite(bm,binding_map())

    print('SECTION 1: schema')
    ywrite(ass,assessment())
    run([PYEX,'validators/state_schema_lint.py','state/identity_readability_assessment.schema.yaml',str(ass),'--json'])

    print('SECTION 2: file size/original resolution cannot pass')
    ywrite(rt,runtime(direct=('CHAR_B_MASTER','FMH_C_MASTER')))
    ywrite(ass,assessment(basis='FILE_SIZE_ONLY'))
    cp=run([PYEX,'validators/identity_readability_lint.py','--assessment',str(ass),'--binding-map',str(bm),'--runtime',str(rt),'--registry',str(reg)],2)
    assert 'IDENTITY_READABILITY_EVIDENCE_BASIS_FAIL' in cp.stdout

    print('SECTION 3: unreadable and no direct identity support must fail')
    ywrite(rt,runtime(direct=()))
    ywrite(ass,assessment(direct_b=None,direct_c=None))
    cp=run([PYEX,'validators/identity_readability_lint.py','--assessment',str(ass),'--binding-map',str(bm),'--runtime',str(rt),'--registry',str(reg)],2)
    assert cp.stdout.count('IDENTITY_READABILITY_FAIL')>=2

    print('SECTION 4: unreadable primary + direct character masters can pass')
    ywrite(rt,runtime(direct=('CHAR_B_MASTER','FMH_C_MASTER')))
    ywrite(ass,assessment())
    cp=run([PYEX,'validators/identity_readability_lint.py','--assessment',str(ass),'--binding-map',str(bm),'--runtime',str(rt),'--registry',str(reg)],0)
    assert 'PRIMARY_PLUS_DIRECT_IDENTITY' in cp.stdout

    print('SECTION 5: storyboard/environment cannot substitute identity')
    bad=assessment(direct_b='ENV_STAGE',direct_c='SB_SH07'); ywrite(ass,bad)
    ywrite(rt,runtime(direct=('ENV_STAGE','SB_SH07')))
    cp=run([PYEX,'validators/identity_readability_lint.py','--assessment',str(ass),'--binding-map',str(bm),'--runtime',str(rt),'--registry',str(reg)],2)
    assert 'IDENTITY_AUTHORITY_ENTITY_OR_ROLE_MISMATCH' in cp.stdout

    print('SECTION 6: regenerated readable primary can become sole identity authority')
    ywrite(rt,runtime(primary='PV_SH07_REGEN',direct=()))
    ywrite(ass,assessment(primary='PV_SH07_REGEN',all_pass=True))
    cp=run([PYEX,'validators/identity_readability_lint.py','--assessment',str(ass),'--binding-map',str(bm),'--runtime',str(rt),'--registry',str(reg)],0)
    assert 'PRIMARY_VISUAL_SUFFICIENT' in cp.stdout

    print('SECTION 7: entity resolver may not claim PRIMARY_VISUAL_BAKED on unreadable humans')
    ywrite(rt,runtime(direct=()))
    ywrite(ass,assessment(direct_b=None,direct_c=None))
    req_baked={'primary_visual_asset_id':'PV_SH07','slot_requests':[
      {'slot_id':'H_A','resolution_mode':'PRIMARY_VISUAL_BAKED','reason':'A readable','coverage_evidence_ref':'VE_A','prompt_identity_anchor':'角色A保持身份','blocking_anchor':'角色A站在左侧中景','action_anchor':'角色A保持站立'},
      {'slot_id':'H_B','resolution_mode':'PRIMARY_VISUAL_BAKED','reason':'attempt baked','coverage_evidence_ref':'VE_B','prompt_identity_anchor':'角色B保持身份','blocking_anchor':'角色B站在中央中景','action_anchor':'角色B保持站立'},
      {'slot_id':'H_C','resolution_mode':'PRIMARY_VISUAL_BAKED','reason':'attempt baked','coverage_evidence_ref':'VE_C','prompt_identity_anchor':'配角C保持身份','blocking_anchor':'配角C站在右侧中景','action_anchor':'配角C保持站立'}]}
    rq=td/'request.yaml'; ywrite(rq,req_baked)
    cp=run([PYEX,'tools/entity_binding_reference_resolver.py','--binding-map',str(bm),'--registry',str(reg),'--request',str(rq),'--identity-readability',str(ass)],2)
    assert 'IDENTITY_READABILITY_FAIL' in cp.stdout

    print('SECTION 8: resolver passes when failed identities become direct references')
    req_direct=copy.deepcopy(req_baked)
    req_direct['slot_requests'][1].update({'resolution_mode':'DIRECT_REFERENCE','asset_id':'CHAR_B_MASTER','reason':'platform-scale identity unreadable; direct master required'})
    req_direct['slot_requests'][2].update({'resolution_mode':'DIRECT_REFERENCE','asset_id':'FMH_C_MASTER','reason':'platform-scale identity unreadable; direct master required'})
    ywrite(rq,req_direct)
    run([PYEX,'tools/entity_binding_reference_resolver.py','--binding-map',str(bm),'--registry',str(reg),'--request',str(rq),'--identity-readability',str(ass),'--direct-budget','4'],0)

print('IDENTITY READABILITY HARD GATE TESTS PASS')
