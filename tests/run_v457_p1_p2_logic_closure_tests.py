#!/usr/bin/env python3
from __future__ import annotations
import copy, importlib.util, yaml
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def loadmod(name, rel):
    spec=importlib.util.spec_from_file_location(name, ROOT/rel)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

perfmod=loadmod('perf','validators/performance_asset_requirement_lint.py')
fxmod=loadmod('fx','validators/narrative_fx_asset_lint.py')
compmod=loadmod('comp','validators/asset_library_completeness_lint.py')

def issue_types(out): return {x['type'] for x in out['issues']}

reqset={'schema_version':1,'skill_version':'4.5.7','episode_id':'EP1','status':'FROZEN','requirements':[
 {'requirement_id':'PERF1','entity_id':'NURSE_A','actor_class':'MINOR_HUMAN','readability':'READABLE','scene_ids':['SC1'],'shot_ids':['SH1'],'requirement_type':'CONTACT_POSE_SUPPORT','trigger_codes':['CONTACT_RELATION'],'reason':'support patient','fulfill_by':'STAGE_03_FREEZE','interaction_entity_ids':['PATIENT_A'],'support_asset_ids':['PERF1_CONTACT'],'status':'APPROVED'}]}
registry={'schema_version':7,'skill_version':'4.5.7','assets':[
 {'asset_id':'PERF1_CONTACT','asset_type':'PERFORMANCE_CONTACT_POSE_SUPPORT','subject_entity_id':'NURSE_A','performance_requirement_id':'PERF1','performance_support_kind':'CONTACT_POSE','performance_interaction_entity_ids':['PATIENT_A'],'authority_role':'PERFORMANCE_SUPPORT_AUTHORITY','status':'APPROVED_SUPPORT','layout_type':'SINGLE_FRAME','media_kind':'IMAGE','video_usage':{'direct_input_allowed':True,'primary_visual_eligible':False}}]}
assert perfmod.lint(reqset,registry,'freeze')['pass']
bad=copy.deepcopy(registry); bad['assets'][0]['performance_requirement_id']=None
assert 'PERFORMANCE_REQUIREMENT_ASSET_REF_MISMATCH' in issue_types(perfmod.lint(reqset,bad,'freeze'))
bad=copy.deepcopy(registry); bad['assets'][0]['performance_interaction_entity_ids']=['PATIENT_WRONG']
out=perfmod.lint(reqset,bad,'freeze'); types=issue_types(out)
assert {'PERFORMANCE_CONTACT_SUPPORT_WRONG_INTERACTION_ENTITY','PERFORMANCE_CONTACT_SUPPORT_INTERACTION_COVERAGE_GAP'} <= types

fx={'schema_version':1,'skill_version':'4.5.7','episode_id':'EP1','status':'FROZEN','effects':[
 {'narrative_fx_id':'FX1','display_name':'signature pulse','scope':'SEQUENCE','scope_id':'SEQ1','scene_ids':['SC1'],'shot_ids':['SH1','SH2'],'reuse_key':'FX:1','authority_mode':'NARRATIVE_FX_REFERENCE','consistency_risk':'HIGH','narrative_role':'SIGNATURE_PHENOMENON','recurrence_count':2,'required_visual_states':['START','PEAK'],'asset_ids':['FX1_ASSET'],'status':'APPROVED'}]}
fxreg={'assets':[{'asset_id':'FX1_ASSET','asset_type':'NARRATIVE_FX_STATE_SHEET','narrative_fx_id':'FX1','fx_state_ids':['START','PEAK'],'authority_role':'NARRATIVE_FX_AUTHORITY','status':'APPROVED_SUPPORT','layout_type':'MULTI_PANEL','media_kind':'IMAGE','video_usage':{'direct_input_allowed':False,'primary_visual_eligible':False}}]}
assert fxmod.lint(fx,fxreg,'freeze')['pass']
bad=copy.deepcopy(fx); bad['effects'][0].update({'scope':'SHOT','scope_id':'SH_WRONG'})
assert 'NARRATIVE_FX_SHOT_SCOPE_ID_MISMATCH' in issue_types(fxmod.lint(bad,fxreg,'freeze'))
bad=copy.deepcopy(fx); bad['effects'][0]['recurrence_count']=1
assert 'NARRATIVE_FX_RECURRENCE_COUNT_BELOW_SHOT_COVERAGE' in issue_types(fxmod.lint(bad,fxreg,'freeze'))

base={'status':'FROZEN'}; perf={'status':'FROZEN','requirements':[]}; fxempty={'status':'FROZEN','effects':[]}; regempty={'assets':[]}
obs={'skill_version':'4.5.7','obligations':[{'obligation_id':'OLD','obligation_type':'SCENE_CLUE_VIEW','fulfill_by':'STAGE_03_FREEZE','status':'FULFILLED','proof_status':'PASS','waiver_policy':'NON_WAIVABLE','fulfillment_asset_ids':[]}]}
out=compmod.lint(base,perf,fxempty,obs,regempty,'freeze')
assert 'LEGACY_COVERAGE_OBLIGATION_REQUIRES_MIGRATION' in issue_types(out)

wf=yaml.safe_load((ROOT/'controller/workflow_state_machine.yaml').read_text(encoding='utf-8'))
eps=yaml.safe_load((ROOT/'state/episode_state.schema.yaml').read_text(encoding='utf-8'))
assert wf['initial_state_by_mode']=={'PRODUCTION':'SOURCE_NARRATIVE_PENDING','DEMO':'SOURCE_NARRATIVE_PENDING','MIGRATION':'MIGRATION_REQUIRED'}
assert set(eps['properties']['workflow_state']['enum'])==set(wf['states'])
ar=yaml.safe_load((ROOT/'controller/authority_registry.yaml').read_text(encoding='utf-8'))
owners=[k for k,v in ar['authorities'].items() if isinstance(v,dict) and v.get('structured_schema')=='state/realism_contract.schema.yaml']
assert owners==['realism_contract']
assert ar['authorities']['realism_contract']['deterministic_validator']=='validators/everyday_realism_lint.py'
assert ar['authorities']['everyday_realism_plausibility']['consumes_authority']=='realism_contract'

print('V4.5.7 P1/P2 LOGIC CLOSURE TESTS PASSED')
