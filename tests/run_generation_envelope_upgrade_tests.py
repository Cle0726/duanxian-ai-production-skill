#!/usr/bin/env python3
from pathlib import Path
import copy, hashlib, json, subprocess, sys, tempfile, yaml
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
PY=sys.executable

def run(cmd,expect=0):
    p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
    if p.returncode!=expect:
        raise AssertionError(f"cmd={cmd}\nexpected={expect} got={p.returncode}\nstdout={p.stdout}\nstderr={p.stderr}")
    return p

def ywrite(p,d): Path(p).write_text(yaml.safe_dump(d,sort_keys=False,allow_unicode=True),encoding='utf-8')

def clean_flags():
    return {k:False for k in ['visible_text','visible_numbers','arrows_or_motion_lines','timecode','shot_or_panel_labels','cut_or_camera_labels','caption_boxes','subtitle_or_logo']}

def panel_asset(aid,sid,path):
    return {'asset_id':aid,'asset_type':'STORYBOARD_CLEAN_PANEL','scene_id':'SC1','shot_id':sid,'status':'APPROVED','authority_role':'STORYBOARD','layout_type':'CLEAN_PANEL','storyboard_render_mode':'WHITE_LINE_STORYBOARD_ONLY','storyboard_cleanliness':clean_flags(),'file_path':str(path),'fingerprint':hashlib.sha256(Path(path).read_bytes()).hexdigest(),'video_usage':{'direct_input_allowed':False,'primary_visual_eligible':False}}

def cut(idx,sid,pid,start,end,view,cam,info):
    return {'cut_id':f'C{idx}','order':idx,'shot_id':sid,'narrative_function':info,'viewpoint_role':view,'camera_character':cam,'core_lens_intent':'natural human relation' if idx==1 else 'detail evidence','provider_fov_anchor_deg':47 if idx==1 else 18,'camera_start':f'{sid} start composition','camera_path':'locked with only minimal framing correction','camera_end':f'{sid} end composition','action_beat':f'{sid} primary action','performance_beat':f'{sid} performance response','information_revealed':info,'cut_in_trigger':'START_OF_ENVELOPE' if idx==1 else 'previous gaze lands','cut_out_trigger':'gaze lands on object' if idx==1 else 'END_OF_ENVELOPE','continuity_handoff':'screen direction and eyeline preserved','start_sec':start,'end_sec':end,'storyboard_panel_asset_id':pid,'primary_visual_asset_ids':[f'PV-{sid}'],'positive_locks':['identity remains stable']}

print('SECTION_1_SCHEMA_AND_CONTROL_PLANE')
run([PY,'validators/state_schema_lint.py','state/generation_envelope.schema.yaml','tests/fixtures/generation_envelope.oner.valid.yaml','--json'])
route=yaml.safe_load((ROOT/'controller/route_registry.yaml').read_text(encoding='utf-8'))
auth=yaml.safe_load((ROOT/'controller/authority_registry.yaml').read_text(encoding='utf-8'))
workflow=yaml.safe_load((ROOT/'controller/workflow_state_machine.yaml').read_text(encoding='utf-8'))
assert route['structured_artifacts']['GENERATION_ENVELOPE']=='state/generation_envelope.schema.yaml'
assert auth['authorities']['generation_envelope']['owner']=='templates/generation_envelope_engine.md'
assert 'GENERATION_ENVELOPE' in route['routes']['STAGE_05_VIDEO']['structured_inputs']
assert 'tools/storyboard_grid_assembler.py' in route['routes']['STAGE_04_VIDEO_CONDITIONING_BUILD']['deterministic_tools']
t21=next(t for t in workflow['transitions'] if t['id']=='T21_CONDITIONING_BUILD')
t23=next(t for t in workflow['transitions'] if t['id']=='T23B_VIDEO_READY')
assert 'MULTISHOT_STORYBOARD_GRID_GATE_PASS' in t21['requires']
assert 'MULTISHOT_STORYBOARD_GRID_GATE_PASS' in t23['requires']

print('SECTION_2_DETERMINISTIC_GRID_AND_VALID_MULTISHOT')
with tempfile.TemporaryDirectory() as td:
    td=Path(td)
    p1,p2=td/'p1.png',td/'p2.png'
    for p,offset in [(p1,20),(p2,70)]:
        im=Image.new('RGB',(320,180),'white'); dr=ImageDraw.Draw(im); dr.rectangle((offset,40,offset+80,150),outline='black',width=4); im.save(p)
    board,manifest=td/'board.png',td/'board.manifest.json'
    cp=run([PY,'tools/storyboard_grid_assembler.py',str(p1),str(p2),'--output',str(board),'--manifest-output',str(manifest)])
    m=json.loads(cp.stdout); assert m['panel_count']==2 and m['source_panels_ordered'][0]['path']==str(p1) and m['source_panels_ordered'][1]['path']==str(p2)
    bfp=hashlib.sha256(board.read_bytes()).hexdigest(); assert bfp==m['output_sha256']
    reg={'schema_version':7,'skill_version':'4.5.7','assets':[panel_asset('SB-SH1','SH1',p1),panel_asset('SB-SH2','SH2',p2),{
        'asset_id':'SB-GRID-E1','asset_type':'STORYBOARD_CLEAN_SEQUENCE_BOARD','scene_id':'SC1','status':'APPROVED','authority_role':'STORYBOARD_SEQUENCE','layout_type':'MULTI_PANEL','storyboard_render_mode':'WHITE_LINE_STORYBOARD_ONLY','storyboard_cleanliness':clean_flags(),'file_path':str(board),'fingerprint':bfp,'video_usage':{'direct_input_allowed':True,'primary_visual_eligible':False},'storyboard_grid_assembly':{'assembler_tool':'tools/storyboard_grid_assembler.py','source_panel_asset_ids_ordered':['SB-SH1','SB-SH2'],'manifest_ref':str(manifest),'output_sha256':bfp},'lineage':{'parent_asset_ids':['SB-SH1','SB-SH2'],'derivation_kind':'STORYBOARD_GRID_FROM_CLEAN_PANELS','source_generation_job_ids':[]}
    }]}
    editorial={'schema_version':1,'skill_version':'4.5.7','episode_id':'EP1','scene_id':'SC1','sequence_id':'SEQ1','editing_mode':'IN_MODEL_MULTISHOT','status':'LOCKED','shot_order':['SH1','SH2'],'shots':[{'shot_id':'SH1','viewpoint_role':'CHARACTER_ALIGNED','entry_function':'establish attention','exit_function':'gaze lands'},{'shot_id':'SH2','viewpoint_role':'DETAIL_EVIDENCE','entry_function':'show object','exit_function':'land evidence'}],'edits':[{'edit_id':'E1','from_shot_id':'SH1','to_shot_id':'SH2','edit_function':'GAZE_REVEAL','cut_trigger':'GAZE_TRIGGER','cut_timing':'ON_GAZE_LANDING','transition_type':'HARD_CUT','continuity_strategy':['EYELINE_MATCH'],'information_delta':'object revealed','audience_effect':'knowledge increases','audio_bridge':'NONE','status':'LOCKED'}]}
    env={'schema_version':1,'skill_version':'4.5.7','generation_envelope_id':'ENV1','episode_id':'EP1','sequence_id':'SEQ1','scene_id':'SC1','source_editorial_plan_ref':'editorial.yaml','source_editorial_fingerprint':'e'*64,'target_generation_profile':'SEEDANCE_CONTROLLED_MULTISHOT','format_mode':'TIMED_MULTISHOT','status':'READY_FOR_COMPILE','total_duration_sec':6.0,'shot_ids':['SH1','SH2'],'cut_contracts':[cut(1,'SH1','SB-SH1',0.0,3.0,'CHARACTER_ALIGNED','STABLE_RELATIONAL','character notices clue'),cut(2,'SH2','SB-SH2',3.0,6.0,'DETAIL_EVIDENCE','DETAIL_INSPECTION','clue becomes readable')],'storyboard_grid':{'required':True,'panel_asset_ids':['SB-SH1','SB-SH2'],'sequence_board_asset_id':'SB-GRID-E1','sequence_board_fingerprint':bfp,'qc_status':'PASS','assembly_tool':'tools/storyboard_grid_assembler.py','manifest_ref':str(manifest)},'fallback_strategy':'SPLIT_TO_SINGLE_SHOT_ENVELOPES','generation_envelope_fingerprint':'f'*64}
    rp,ep,edp=td/'registry.yaml',td/'envelope.yaml',td/'editorial.yaml'; ywrite(rp,reg); ywrite(ep,env); ywrite(edp,editorial)
    proof={'schema_version':1,'skill_version':'4.5.7','storyboard_sequence_proof_id':'SBP-SEQ1','episode_id':'EP1','sequence_id':'SEQ1','scene_id':'SC1','source_editorial_plan_ref':str(edp),'source_editorial_fingerprint':'e'*64,'shot_order':['SH1','SH2'],'panel_order':[{'shot_id':'SH1','panel_asset_id':'SB-SH1','panel_role':'BASELINE'},{'shot_id':'SH2','panel_asset_id':'SB-SH2','panel_role':'BASELINE'}],'sequence_board_asset_id':'SB-GRID-E1','sequence_board_fingerprint':bfp,'assembly_tool':'tools/storyboard_grid_assembler.py','manifest_ref':str(manifest),'status':'APPROVED','storyboard_sequence_proof_fingerprint':'9'*64}
    spp=td/'sequence_proof.yaml'; ywrite(spp,proof)
    run([PY,'validators/state_schema_lint.py','state/storyboard_sequence_proof.schema.yaml',str(spp),'--json'])
    run([PY,'validators/storyboard_sequence_grid_lint.py','--editorial-plan',str(edp),'--registry',str(rp),'--proof',str(spp),'--phase','qc'])
    run([PY,'validators/storyboard_sequence_grid_lint.py','--editorial-plan',str(edp),'--registry',str(rp),'--proof',str(spp),'--phase','approved'])
    missing=json.loads(run([PY,'validators/storyboard_sequence_grid_lint.py','--editorial-plan',str(edp),'--registry',str(rp),'--phase','qc'],expect=2).stdout)
    assert any(x['type']=='MULTISHOT_SEQUENCE_STORYBOARD_GRID_MISSING' for x in missing['issues'])
    run([PY,'validators/state_schema_lint.py','state/generation_envelope.schema.yaml',str(ep),'--json'])
    out=json.loads(run([PY,'validators/generation_envelope_lint.py','--envelope',str(ep),'--registry',str(rp),'--editorial-plan',str(edp)]).stdout)
    assert out['pass'] and out['multishot'] and out['cut_count']==2

    # Board order cannot be swapped.
    bad=copy.deepcopy(env); bad['storyboard_grid']['panel_asset_ids']=['SB-SH2','SB-SH1']; badp=td/'bad.yaml'; ywrite(badp,bad)
    out=json.loads(run([PY,'validators/generation_envelope_lint.py','--envelope',str(badp),'--registry',str(rp),'--editorial-plan',str(edp)],expect=2).stdout)
    assert any(x['type']=='MULTISHOT_STORYBOARD_GRID_ORDER_MISMATCH' for x in out['issues'])

    # Multishot cannot silently omit the board.
    bad2=copy.deepcopy(env); bad2['storyboard_grid']['sequence_board_asset_id']=None; bad2['storyboard_grid']['sequence_board_fingerprint']=None; bad2['storyboard_grid']['qc_status']='NOT_READY'; bad2p=td/'bad2.yaml'; ywrite(bad2p,bad2)
    out=json.loads(run([PY,'validators/generation_envelope_lint.py','--envelope',str(bad2p),'--registry',str(rp),'--editorial-plan',str(edp)],expect=2).stdout)
    assert any(x['type']=='MULTISHOT_STORYBOARD_GRID_MISSING' for x in out['issues'])

    # Prompt must contain exactly the planned cuts and explicit boundary lock.
    prompt=td/'prompt.txt'; prompt.write_text('FORMAT MODE = TIMED MULTISHOT；Exact CUT count = 2；cuts only at specified boundaries.\nCUT 1 0–3s：人物看向线索。\nHARD CUT。\nCUT 2 3–6s：线索特写。不得新增CUT。',encoding='utf-8')
    run([PY,'validators/multishot_prompt_lint.py','--prompt',str(prompt),'--envelope',str(ep)])
    prompt.write_text('人物连续看向线索，摄影机慢慢推近。',encoding='utf-8')
    run([PY,'validators/multishot_prompt_lint.py','--prompt',str(prompt),'--envelope',str(ep)],expect=2)

print('SECTION_3_ONER_DOES_NOT_REQUIRE_EXTRA_GRID')
with tempfile.TemporaryDirectory() as td:
    td=Path(td); p=td/'p.png'; Image.new('RGB',(160,90),'white').save(p)
    reg={'schema_version':7,'skill_version':'4.5.7','assets':[panel_asset('SB-SH1','SH1',p)]}; rp=td/'r.yaml'; ywrite(rp,reg)
    env=yaml.safe_load((ROOT/'tests/fixtures/generation_envelope.oner.valid.yaml').read_text(encoding='utf-8')); ep=td/'e.yaml'; ywrite(ep,env)
    run([PY,'validators/generation_envelope_lint.py','--envelope',str(ep),'--registry',str(rp)])
    single_editorial={'schema_version':1,'skill_version':'4.5.7','episode_id':'EP1','scene_id':'SC1','sequence_id':'SEQ-SINGLE','editing_mode':'ASSEMBLY_FIRST','status':'LOCKED','shot_order':['SH1'],'shots':[{'shot_id':'SH1','viewpoint_role':'CHARACTER_ALIGNED','entry_function':'enter','exit_function':'land'}],'edits':[]}
    sep=td/'single_editorial.yaml'; ywrite(sep,single_editorial)
    out=json.loads(run([PY,'validators/storyboard_sequence_grid_lint.py','--editorial-plan',str(sep),'--registry',str(rp),'--phase','qc']).stdout); assert out['required'] is False
    prompt=td/'p.txt'; prompt.write_text('FORMAT MODE = ONER；全镜头NO CUT，一镜到底；人物完成单一动作。',encoding='utf-8')
    run([PY,'validators/multishot_prompt_lint.py','--prompt',str(prompt),'--envelope',str(ep)])

print('SECTION_4_GATE_PRODUCER_AND_FAILURE_ROUTING')
run([PY,'validators/gate_producer_lint.py','--workflow','controller/workflow_state_machine.yaml','--registry','controller/gate_producer_registry.yaml'])
fr=yaml.safe_load((ROOT/'controller/failure_router.yaml').read_text(encoding='utf-8'))
assert fr['code_aliases']['MULTISHOT_STORYBOARD_GRID_MISSING']=='MULTISHOT_STORYBOARD_GRID_FAIL'
assert fr['routes']['MULTISHOT_PROVIDER_CAPABILITY_FAIL']['action'].startswith('DOWNGRADE_TO_SPLIT_SINGLE_SHOT')

print('GENERATION ENVELOPE UPGRADE TESTS PASS')
