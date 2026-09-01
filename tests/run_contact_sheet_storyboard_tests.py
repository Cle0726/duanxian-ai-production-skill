#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, sys, tempfile, hashlib
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parent.parent
PY=sys.executable
FIX=ROOT/'tests'/'fixtures'/'v457_contact_sheet'

def sha256(p):
    h=hashlib.sha256();
    with open(p,'rb') as f:
        h.update(f.read())
    return h.hexdigest()

def run(cmd, expect=0):
    cp=subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    print(cp.stdout)
    if cp.stderr: print(cp.stderr)
    if cp.returncode!=expect:
        raise AssertionError(f'{cmd} expected {expect} got {cp.returncode}')
    return cp

def ywrite(p,d): Path(p).write_text(yaml.safe_dump(d, sort_keys=False, allow_unicode=True), encoding='utf-8')

def clean_flags():
    return {'visible_text':False,'visible_numbers':False,'arrows_or_motion_lines':False,'timecode':False,'shot_or_panel_labels':False,'cut_or_camera_labels':False,'caption_boxes':False,'subtitle_or_logo':False,'recognizable_face_present':False,'recognizable_hair_present':False,'recognizable_costume_detail_present':False,'identity_specific_feature_present':False}

with tempfile.TemporaryDirectory() as td:
    outdir=Path(td)/'panels'; manifest=Path(td)/'manifest.json'
    run([PY,'tools/storyboard_contact_sheet_splitter.py',str(FIX/'contact_sheet.png'),'--rows','2','--cols','2','--output-dir',str(outdir),'--manifest-output',str(manifest),'--prefix','cs'])
    data=json.loads(manifest.read_text(encoding='utf-8'))
    assert len(data['panels'])==4
    registry={'assets':[
        {'asset_id':'CS-01','asset_type':'STORYBOARD_CONTACT_SHEET','status':'APPROVED','layout_type':'CONTACT_SHEET','storyboard_render_mode':'WHITE_LINE_STORYBOARD_ONLY','storyboard_cleanliness':clean_flags(),'file_path':str(FIX/'contact_sheet.png'),'fingerprint':sha256(FIX/'contact_sheet.png'),'video_usage':{'direct_input_allowed':False,'primary_visual_eligible':False}},
    ]}
    panel_order=[]
    for i,panel in enumerate(data['panels'], start=1):
        aid=f'SB-{i:02d}'
        registry['assets'].append({'asset_id':aid,'asset_type':'STORYBOARD_CLEAN_PANEL','status':'APPROVED','layout_type':'CLEAN_PANEL','storyboard_render_mode':'WHITE_LINE_STORYBOARD_ONLY','storyboard_cleanliness':clean_flags(),'file_path':panel['file_path'],'fingerprint':panel['sha256'],'shot_id':f'SH{i}','video_usage':{'direct_input_allowed':True,'primary_visual_eligible':False},'storyboard_contact_sheet_split':{'splitter_tool':'tools/storyboard_contact_sheet_splitter.py','contact_sheet_asset_id':'CS-01','contact_sheet_fingerprint':sha256(FIX/'contact_sheet.png'),'panel_index':i,'row':panel['row'],'col':panel['col'],'manifest_ref':str(manifest)},'lineage':{'parent_asset_ids':['CS-01'],'derivation_kind':'STORYBOARD_PANELS_FROM_CONTACT_SHEET','source_generation_job_ids':[]}})
        panel_order.append({'panel_index':i,'panel_asset_id':aid,'shot_id':f'SH{i}','panel_role':'BASELINE'})
    reg=Path(td)/'registry.yaml'; ywrite(reg, registry)
    proof={'schema_version':1,'skill_version':'4.5.7','storyboard_contact_sheet_proof_id':'CSP-01','episode_id':'EP1','sequence_id':'SEQ1','scene_id':'SC1','grid_mode':'SHOT_GRID','panel_count':4,'rows':2,'cols':2,'contact_sheet_asset_id':'CS-01','contact_sheet_fingerprint':sha256(FIX/'contact_sheet.png'),'splitter_tool':'tools/storyboard_contact_sheet_splitter.py','manifest_ref':str(manifest),'shot_order':['SH1','SH2','SH3','SH4'],'panel_order':panel_order,'status':'APPROVED'}
    pf=Path(td)/'proof.yaml'; ywrite(pf, proof)
    run([PY,'validators/state_schema_lint.py','state/storyboard_contact_sheet_proof.schema.yaml',str(pf),'--json'])
    run([PY,'validators/storyboard_contact_sheet_lint.py','--proof',str(pf),'--registry',str(reg)])

    # Adversarial: manifest panel file_path is mandatory proof, not optional metadata.
    bad_manifest_missing_path=Path(td)/'manifest_missing_path.json'
    bad_data=json.loads(manifest.read_text(encoding='utf-8'))
    bad_data['panels'][0].pop('file_path',None)
    bad_manifest_missing_path.write_text(json.dumps(bad_data,ensure_ascii=False,indent=2),encoding='utf-8')
    bad_reg_data=yaml.safe_load(reg.read_text(encoding='utf-8'))
    for x in bad_reg_data['assets']:
        sp=x.get('storyboard_contact_sheet_split') or {}
        if sp: sp['manifest_ref']=str(bad_manifest_missing_path)
    bad_reg=Path(td)/'registry_missing_path.yaml'; ywrite(bad_reg,bad_reg_data)
    bad_proof=dict(proof); bad_proof['manifest_ref']=str(bad_manifest_missing_path)
    bad_pf=Path(td)/'proof_missing_path.yaml'; ywrite(bad_pf,bad_proof)
    cp=run([PY,'validators/storyboard_contact_sheet_lint.py','--proof',str(bad_pf),'--registry',str(bad_reg)],expect=2)
    assert 'CONTACT_SHEET_SPLIT_FILE_PATH_MISSING' in cp.stdout

    # Adversarial: fake/nonexistent derived file cannot pass by carrying a plausible stored SHA.
    bad_manifest_missing_file=Path(td)/'manifest_missing_file.json'
    bad_data=json.loads(manifest.read_text(encoding='utf-8'))
    missing_file=str(Path(td)/'panels'/'does_not_exist.png')
    bad_data['panels'][0]['file_path']=missing_file
    bad_manifest_missing_file.write_text(json.dumps(bad_data,ensure_ascii=False,indent=2),encoding='utf-8')
    bad_reg_data=yaml.safe_load(reg.read_text(encoding='utf-8'))
    for x in bad_reg_data['assets']:
        sp=x.get('storyboard_contact_sheet_split') or {}
        if sp:
            sp['manifest_ref']=str(bad_manifest_missing_file)
            if sp.get('panel_index')==1: x['file_path']=missing_file
    bad_reg=Path(td)/'registry_missing_file.yaml'; ywrite(bad_reg,bad_reg_data)
    bad_proof=dict(proof); bad_proof['manifest_ref']=str(bad_manifest_missing_file)
    bad_pf=Path(td)/'proof_missing_file.yaml'; ywrite(bad_pf,bad_proof)
    cp=run([PY,'validators/storyboard_contact_sheet_lint.py','--proof',str(bad_pf),'--registry',str(bad_reg)],expect=2)
    assert 'CONTACT_SHEET_SPLIT_FILE_MISSING' in cp.stdout and 'CONTACT_SHEET_SPLIT_REGISTRY_FILE_MISSING' in cp.stdout

    # Adversarial: registry path cannot point somewhere else even if the stored fingerprint matches.
    other=Path(td)/'other.png'; other.write_bytes(Path(data['panels'][1]['file_path']).read_bytes())
    bad_reg_data=yaml.safe_load(reg.read_text(encoding='utf-8'))
    for x in bad_reg_data['assets']:
        sp=x.get('storyboard_contact_sheet_split') or {}
        if sp.get('panel_index')==1: x['file_path']=str(other)
    bad_reg=Path(td)/'registry_wrong_file.yaml'; ywrite(bad_reg,bad_reg_data)
    cp=run([PY,'validators/storyboard_contact_sheet_lint.py','--proof',str(pf),'--registry',str(bad_reg)],expect=2)
    assert 'CONTACT_SHEET_SPLIT_FILE_PATH_MISMATCH' in cp.stdout

    # old sequence board path still works with split panels
    board=Path(td)/'board.png'; mani2=Path(td)/'board_manifest.json'
    run([PY,'tools/storyboard_grid_assembler.py',*(str(Path(x['file_path'])) for x in data['panels']),'--output',str(board),'--manifest-output',str(mani2)])
print('CONTACT SHEET STORYBOARD TESTS PASSED')
