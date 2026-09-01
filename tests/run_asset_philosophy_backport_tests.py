#!/usr/bin/env python3
from __future__ import annotations
import copy, json, subprocess, sys, tempfile
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]; PY=sys.executable

def ywrite(p,d): Path(p).write_text(yaml.safe_dump(d,sort_keys=False,allow_unicode=True),encoding='utf-8')
def run(cmd,expect=0):
    cp=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
    print('$',' '.join(map(str,cmd))); print(cp.stdout)
    if cp.stderr: print(cp.stderr)
    if cp.returncode!=expect: raise AssertionError(f'expected {expect}, got {cp.returncode}')
    return cp

perf={
 'schema_version':1,'skill_version':'4.5.7','episode_id':'EP1','status':'FROZEN','requirements':[
  {'requirement_id':'PERF_A_SH1','entity_id':'CHAR_A','actor_class':'CHARACTER_CANON','readability':'READABLE','scene_ids':['SC1'],'shot_ids':['SH1'],'requirement_type':'EXPRESSION_SUPPORT','trigger_codes':['MICRO_EXPRESSION_CRITICAL'],'reason':'subtle recognition beat must read','fulfill_by':'STAGE_03_FREEZE','interaction_entity_ids':[],'support_asset_ids':['PERF_A_EXPR'],'status':'APPROVED'},
  {'requirement_id':'PERF_B_SH1','entity_id':'CHAR_B','actor_class':'MINOR_HUMAN','readability':'READABLE','scene_ids':['SC1'],'shot_ids':['SH1'],'requirement_type':'PERFORMANCE_SUPPORT_PACK','trigger_codes':['EXPRESSION_IS_STORY_PAYLOAD','CONTACT_RELATION'],'reason':'reaction plus contact pose','fulfill_by':'STAGE_03_FREEZE','interaction_entity_ids':['CHAR_A'],'support_asset_ids':['PERF_B_EXPR','PERF_B_CONTACT'],'status':'APPROVED'},
  {'requirement_id':'PERF_C_SH2','entity_id':'CHAR_C','actor_class':'MINOR_HUMAN','readability':'SILHOUETTE_READABLE','scene_ids':['SC1'],'shot_ids':['SH2'],'requirement_type':'NONE','trigger_codes':[],'reason':'ordinary background walk is adequately controlled','fulfill_by':'STAGE_03_FREEZE','interaction_entity_ids':[],'support_asset_ids':[],'status':'NOT_REQUIRED'}
 ]
}
fx={
 'schema_version':1,'skill_version':'4.5.7','episode_id':'EP1','status':'FROZEN','effects':[
  {'narrative_fx_id':'NFX_SILENCE','display_name':'全城失声视觉异常','scope':'SEQUENCE','scope_id':'SEQ1','scene_ids':['SC1'],'shot_ids':['SH1','SH2'],'reuse_key':'NFX:SILENCE:v1','authority_mode':'NARRATIVE_FX_REFERENCE','consistency_risk':'HIGH','narrative_role':'SIGNATURE_PHENOMENON','recurrence_count':2,'required_visual_states':['START','PEAK'],'asset_ids':['NFX_SILENCE_SHEET'],'status':'APPROVED'},
  {'narrative_fx_id':'NFX_DUST','display_name':'普通灰尘','scope':'SHOT','scope_id':'SH2','scene_ids':['SC1'],'shot_ids':['SH2'],'reuse_key':'NFX:DUST:SH2','authority_mode':'TEXT_GRAMMAR_ONLY','consistency_risk':'LOW','narrative_role':'ATMOSPHERIC','recurrence_count':1,'required_visual_states':[],'asset_ids':[],'status':'TEXT_ONLY_READY'}
 ]
}
registry={
 'schema_version':7,'skill_version':'4.5.7','assets':[
  {'asset_id':'PERF_A_EXPR','asset_type':'PERFORMANCE_EXPRESSION_SUPPORT','subject_entity_id':'CHAR_A','performance_requirement_id':'PERF_A_SH1','performance_support_kind':'EXPRESSION','authority_role':'PERFORMANCE_SUPPORT_AUTHORITY','status':'APPROVED_SUPPORT','layout_type':'SINGLE_FRAME','media_kind':'IMAGE','transient_content_policy':'SHOT_SPECIFIC','video_usage':{'direct_input_allowed':True,'primary_visual_eligible':False}},
  {'asset_id':'PERF_B_EXPR','asset_type':'PERFORMANCE_EXPRESSION_SUPPORT','subject_entity_id':'CHAR_B','performance_requirement_id':'PERF_B_SH1','performance_support_kind':'EXPRESSION','authority_role':'PERFORMANCE_SUPPORT_AUTHORITY','status':'APPROVED_SUPPORT','layout_type':'SINGLE_FRAME','media_kind':'IMAGE','transient_content_policy':'SHOT_SPECIFIC','video_usage':{'direct_input_allowed':True,'primary_visual_eligible':False}},
  {'asset_id':'PERF_B_CONTACT','asset_type':'PERFORMANCE_CONTACT_POSE_SUPPORT','subject_entity_id':'CHAR_B','performance_requirement_id':'PERF_B_SH1','performance_support_kind':'CONTACT_POSE','performance_interaction_entity_ids':['CHAR_A'],'authority_role':'PERFORMANCE_SUPPORT_AUTHORITY','status':'APPROVED_SUPPORT','layout_type':'SINGLE_FRAME','media_kind':'IMAGE','transient_content_policy':'SHOT_SPECIFIC','video_usage':{'direct_input_allowed':True,'primary_visual_eligible':False}},
  {'asset_id':'NFX_SILENCE_SHEET','asset_type':'NARRATIVE_FX_STATE_SHEET','subject_entity_id':None,'narrative_fx_id':'NFX_SILENCE','fx_state_ids':['START','PEAK'],'authority_role':'NARRATIVE_FX_AUTHORITY','status':'APPROVED_SUPPORT','layout_type':'MULTI_PANEL','media_kind':'IMAGE','transient_content_policy':'STATE_VARIANT','video_usage':{'direct_input_allowed':False,'primary_visual_eligible':False}}
 ]
}
base={'schema_version':1,'skill_version':'4.5.7','episode_id':'EP1','environments':[],'minor_humans':[],'actor_authority_index':[],'crowd_archetype_set_refs':[],'status':'FROZEN','manifest_fingerprint':None}
obligations={'schema_version':3,'skill_version':'4.5.7','episode_id':'EP1','status':'COMPLETE','obligations':[
 {'obligation_id':'OB_PERF_A','trigger_type':'SHOT','shot_ids':['SH1'],'obligation_type':'PERFORMANCE_EXPRESSION_SUPPORT','fulfill_by':'STAGE_03_FREEZE','reason':'critical expression','subject_entity_id':'CHAR_A','performance_requirement_id':'PERF_A_SH1','fulfillment_asset_ids':['PERF_A_EXPR'],'status':'FULFILLED','waiver_policy':'NON_WAIVABLE','proof_status':'PASS'},
 {'obligation_id':'OB_NFX','trigger_type':'SHOT','shot_ids':['SH1','SH2'],'obligation_type':'NARRATIVE_FX_REFERENCE','fulfill_by':'STAGE_03_FREEZE','reason':'signature narrative effect','narrative_fx_id':'NFX_SILENCE','fulfillment_asset_ids':['NFX_SILENCE_SHEET'],'status':'FULFILLED','waiver_policy':'NON_WAIVABLE','proof_status':'PASS'}
]}

print('SECTION_0_ROUTES')
for at,expected in [
 ('PERFORMANCE_EXPRESSION_SUPPORT','PERFORMANCE_SUPPORT_ASSET'),('PERFORMANCE_ACTION_POSE_SUPPORT','PERFORMANCE_SUPPORT_ASSET'),('PERFORMANCE_CONTACT_POSE_SUPPORT','PERFORMANCE_SUPPORT_ASSET'),('NARRATIVE_FX_REFERENCE','NARRATIVE_FX_ASSET'),('NARRATIVE_FX_STATE_SHEET','NARRATIVE_FX_ASSET')]:
    cp=run([PY,'tools/asset_route_dispatcher.py',at,'--json']); assert json.loads(cp.stdout)['route']==expected

with tempfile.TemporaryDirectory() as td:
    td=Path(td); pp=td/'perf.yaml'; fp=td/'fx.yaml'; rp=td/'registry.yaml'; bp=td/'base.yaml'; op=td/'ob.yaml'
    for p,d in [(pp,perf),(fp,fx),(rp,registry),(bp,base),(op,obligations)]: ywrite(p,d)
    print('SECTION_1_SCHEMAS')
    for schema,data in [('state/performance_asset_requirement_set.schema.yaml',pp),('state/narrative_fx_asset_manifest.schema.yaml',fp),('state/asset_registry.schema.yaml',rp),('state/base_visual_authority_manifest.schema.yaml',bp),('state/visual_asset_obligation.schema.yaml',op)]:
        run([PY,'validators/state_schema_lint.py',schema,str(data),'--json'])
    print('SECTION_2_VALID_PERFORMANCE')
    run([PY,'validators/performance_asset_requirement_lint.py','--requirements',str(pp),'--asset-registry',str(rp),'--phase','freeze'])
    print('SECTION_3_VALID_NARRATIVE_FX')
    run([PY,'validators/narrative_fx_asset_lint.py','--manifest',str(fp),'--asset-registry',str(rp),'--phase','freeze'])
    print('SECTION_4_COMPLETENESS')
    run([PY,'validators/asset_library_completeness_lint.py','--base-visual-manifest',str(bp),'--performance-requirements',str(pp),'--narrative-fx-manifest',str(fp),'--obligations',str(op),'--asset-registry',str(rp),'--phase','freeze'])

    print('SECTION_5_MISSING_PERFORMANCE_SUPPORT_FAILS')
    bad=copy.deepcopy(perf); bad['requirements'][0]['support_asset_ids']=[]; badp=td/'perf_missing.yaml'; ywrite(badp,bad)
    run([PY,'validators/performance_asset_requirement_lint.py','--requirements',str(badp),'--asset-registry',str(rp),'--phase','freeze'],expect=2)

    print('SECTION_6_ENTITY_MISMATCH_FAILS')
    badr=copy.deepcopy(registry); badr['assets'][0]['subject_entity_id']='CHAR_WRONG'; badrp=td/'registry_bad_entity.yaml'; ywrite(badrp,badr)
    run([PY,'validators/performance_asset_requirement_lint.py','--requirements',str(pp),'--asset-registry',str(badrp),'--phase','freeze'],expect=2)

    print('SECTION_7_MULTIPANEL_DIRECT_PERFORMANCE_FAILS')
    badr=copy.deepcopy(registry); badr['assets'][0]['layout_type']='MULTI_PANEL'; badr['assets'][0]['video_usage']['direct_input_allowed']=True; badrp=td/'registry_bad_panel.yaml'; ywrite(badrp,badr)
    run([PY,'validators/performance_asset_requirement_lint.py','--requirements',str(pp),'--asset-registry',str(badrp),'--phase','freeze'],expect=2)

    print('SECTION_8_HIGH_RISK_TEXT_ONLY_FX_FAILS')
    badfx=copy.deepcopy(fx); e=badfx['effects'][0]; e['authority_mode']='TEXT_GRAMMAR_ONLY'; e['asset_ids']=[]; e['status']='TEXT_ONLY_READY'; badfp=td/'fx_text_only_bad.yaml'; ywrite(badfp,badfx)
    run([PY,'validators/narrative_fx_asset_lint.py','--manifest',str(badfp),'--asset-registry',str(rp),'--phase','freeze'],expect=2)

    print('SECTION_9_FX_STATE_COVERAGE_GAP_FAILS')
    badr=copy.deepcopy(registry); badr['assets'][-1]['fx_state_ids']=['START']; badrp=td/'registry_fx_gap.yaml'; ywrite(badrp,badr)
    run([PY,'validators/narrative_fx_asset_lint.py','--manifest',str(fp),'--asset-registry',str(badrp),'--phase','freeze'],expect=2)

    print('SECTION_10_STATE_SHEET_DIRECT_REFERENCE_FAILS')
    badr=copy.deepcopy(registry); badr['assets'][-1]['video_usage']['direct_input_allowed']=True; badrp=td/'registry_fx_direct.yaml'; ywrite(badrp,badr)
    run([PY,'validators/narrative_fx_asset_lint.py','--manifest',str(fp),'--asset-registry',str(badrp),'--phase','freeze'],expect=2)

    print('SECTION_10A_PERFORMANCE_REQUIREMENT_BACKREF_REQUIRED')
    badr=copy.deepcopy(registry); badr['assets'][0]['performance_requirement_id']=None; badrp=td/'registry_perf_missing_backref.yaml'; ywrite(badrp,badr)
    run([PY,'validators/performance_asset_requirement_lint.py','--requirements',str(pp),'--asset-registry',str(badrp),'--phase','freeze'],expect=2)

    print('SECTION_10B_CONTACT_POSE_WRONG_INTERACTION_FAILS')
    badr=copy.deepcopy(registry); badr['assets'][2]['performance_interaction_entity_ids']=['CHAR_WRONG']; badrp=td/'registry_bad_contact_entity.yaml'; ywrite(badrp,badr)
    run([PY,'validators/performance_asset_requirement_lint.py','--requirements',str(pp),'--asset-registry',str(badrp),'--phase','freeze'],expect=2)

    print('SECTION_10C_FX_SCOPE_ID_FAILS')
    badfx=copy.deepcopy(fx); badfx['effects'][1]['scope_id']='SH_WRONG'; badfp=td/'fx_bad_scope_id.yaml'; ywrite(badfp,badfx)
    run([PY,'validators/narrative_fx_asset_lint.py','--manifest',str(badfp),'--asset-registry',str(rp),'--phase','freeze'],expect=2)

    print('SECTION_10D_FX_RECURRENCE_BELOW_SHOT_COVERAGE_FAILS')
    badfx=copy.deepcopy(fx); badfx['effects'][0]['recurrence_count']=1; badfp=td/'fx_bad_recurrence.yaml'; ywrite(badfp,badfx)
    run([PY,'validators/narrative_fx_asset_lint.py','--manifest',str(badfp),'--asset-registry',str(rp),'--phase','freeze'],expect=2)

    print('SECTION_11_COMPLETENESS_OPEN_OBLIGATION_FAILS')
    badob=copy.deepcopy(obligations); badob['obligations'][0]['status']='IN_PROGRESS'; badob['obligations'][0]['proof_status']='NOT_RUN'; badop=td/'ob_open.yaml'; ywrite(badop,badob)
    run([PY,'validators/asset_library_completeness_lint.py','--base-visual-manifest',str(bp),'--performance-requirements',str(pp),'--narrative-fx-manifest',str(fp),'--obligations',str(badop),'--asset-registry',str(rp),'--phase','freeze'],expect=2)

print('ASSET PHILOSOPHY BACKPORT TESTS PASSED')
