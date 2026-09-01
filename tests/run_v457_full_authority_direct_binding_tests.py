#!/usr/bin/env python3
from pathlib import Path
import importlib.util,json
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('lint',ROOT/'validators/full_authority_direct_binding_lint.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
plan={'reference_integrity':{'direct_binding_policy':'FULL_AUTHORITY_DIRECT_BINDING','mandatory_direct_reference_ids':['PV','ENV','KA','NO','CE','SB']},'entity_binding_handoff':{'bindings':[
 {'slot_id':'E_STAGE','entity_type':'ENVIRONMENT','resolution_mode':'DIRECT_REFERENCE','resolved_asset_id':'ENV','native_token':'@图2'},
 {'slot_id':'H_K','entity_type':'CHARACTER','resolution_mode':'DIRECT_REFERENCE','resolved_asset_id':'KA','native_token':'@图3'},
 {'slot_id':'H_N','entity_type':'CHARACTER','resolution_mode':'DIRECT_REFERENCE','resolved_asset_id':'NO','native_token':'@图4'},
 {'slot_id':'H_C','entity_type':'CHARACTER','resolution_mode':'DIRECT_REFERENCE','resolved_asset_id':'CE','native_token':'@图5'}]}}
job={'required_bindings':[
 {'asset_id':'PV','role':'PRIMARY_VISUAL','native_token':'@图1'}, {'asset_id':'ENV','role':'EMPTY_ENVIRONMENT_MASTER','native_token':'@图2'},
 {'asset_id':'KA','role':'CHARACTER_MASTER','native_token':'@图3'}, {'asset_id':'NO','role':'CHARACTER_MASTER','native_token':'@图4'}, {'asset_id':'CE','role':'CHARACTER_MASTER','native_token':'@图5'},
 {'asset_id':'SB','role':'CURRENT_SHOT_STORYBOARD_TEMPORAL_CONTROL','native_token':'@图6'}]}
prompt='@图1 @图2 @图3 @图4 @图5 @图6'
out=m.lint(plan,job,prompt); assert out['pass'],out
bad=json.loads(json.dumps(plan)); bad['entity_binding_handoff']['bindings'][1]['resolution_mode']='PRIMARY_VISUAL_BAKED'; out=m.lint(bad,job,prompt); assert not out['pass'] and any(x['type']=='VISIBLE_HUMAN_MASTER_NOT_DIRECT' for x in out['issues'])
skill=(ROOT/'SKILL.md').read_text(encoding='utf-8'); resolver=(ROOT/'templates/reference_resolver.md').read_text(encoding='utf-8')
assert 'FIELD_AUTHORITY_PROVIDER_ROUTED_BINDING' in skill and 'FIELD_AUTHORITY_PROVIDER_ROUTED_BINDING' in resolver
omni=json.loads(json.dumps(plan)); omni['reference_integrity'].update({'direct_binding_policy':'FIELD_AUTHORITY_PROVIDER_ROUTED_BINDING','primary_visual_route':'OMIT_REDUNDANT_BAKED_COMPOSITE','storyboard_prompt_closure':True}); omni['reference_integrity']['mandatory_direct_reference_ids']=['ENV','KA','NO','CE','SB']
ojob={'required_bindings':[x for x in job['required_bindings'] if x['role']!='PRIMARY_VISUAL']}; oprompt='@图2 @图3 @图4 @图5 @图6'
out=m.lint(omni,ojob,oprompt); assert out['pass'],out
badjob=json.loads(json.dumps(ojob)); badjob['required_bindings'].append({'asset_id':'PV','role':'PRIMARY_VISUAL','native_token':'@图1'}); out=m.lint(omni,badjob,'@图1 '+oprompt); assert not out['pass'] and any(x['type']=='REDUNDANT_COMPOSITE_REFERENCE_COMPETITION' for x in out['issues'])
print('V4.5.10 provider-routed field authority tests: PASS')
