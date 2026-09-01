#!/usr/bin/env python3
from __future__ import annotations
import copy, subprocess, sys, tempfile
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

spatial={
 'schema_version':2,'skill_version':'4.5.7','episode_id':'EP1',
 'locations':[{'location_entity_id':'SHOP_01','reuse_tier':'C','location_kind':'INTERIOR','status':'LOCKED','zones':['COUNTER'],'anchors':[]}],
 'relations':[],
 'event_nodes':[{'event_node_id':'EV1','scene_id':'SC1','location_entity_id':'SHOP_01','description':'一次性商店场景','actor_ids':['CHAR_MAIN','FMH_CLERK']}],
 'character_routes':[],'planning_diagrams':[],'status':'LOCKED'
}
manifest={
 'schema_version':1,'skill_version':'4.5.7','episode_id':'EP1','status':'FROZEN',
 'environments':[{'requirement_id':'BVA_ENV_SHOP','location_entity_id':'SHOP_01','scene_ids':['SC1'],'reuse_tier':'C','reuse_key':'ENV:SHOP_01:v1','obligation_id':'OB_ENV_SHOP','empty_master_asset_id':'ENV_SHOP_MASTER','visual_anchor_set_ref':None,'status':'APPROVED'}],
 'minor_humans':[{'requirement_id':'BVA_FMH_CLERK','entity_id':'FMH_CLERK','display_name':'一次性店员','scene_ids':['SC1'],'shot_ids':['SH1'],'readability':'READABLE','reuse_key':'FMH:CLERK:v1','visual_owner':'FMH_ASSET','obligation_id':'OB_FMH_CLERK','human_master_asset_id':'FMH_CLERK_MASTER','canon_view_set_ref':None,'promotion_state':'SCOPED','status':'APPROVED'}],
 'actor_authority_index':[
  {'entity_id':'CHAR_MAIN','actor_class':'CHARACTER_CANON','readability':'READABLE','authority_kind':'CHARACTER_AUTHORITY','authority_asset_id':'CHAR_MAIN_MASTER','minor_human_requirement_id':None,'crowd_archetype_set_ref':None},
  {'entity_id':'FMH_CLERK','actor_class':'MINOR_HUMAN','readability':'READABLE','authority_kind':'FMH_ASSET','authority_asset_id':'FMH_CLERK_MASTER','minor_human_requirement_id':'BVA_FMH_CLERK','crowd_archetype_set_ref':None}
 ],
 'crowd_archetype_set_refs':[]
}
obligations={
 'schema_version':3,'skill_version':'4.5.7','episode_id':'EP1','status':'COMPLETE','obligations':[
  {'obligation_id':'OB_ENV_SHOP','trigger_type':'SHOT','shot_ids':['SH1'],'obligation_type':'EMPTY_ENVIRONMENT_MASTER','fulfill_by':'STAGE_03_FREEZE','reason':'formal location needs clean empty visual authority','authority_fields':['ENVIRONMENT_APPEARANCE'],'required_visual_fact':'empty shop master','location_entity_id':'SHOP_01','fulfillment_asset_ids':['ENV_SHOP_MASTER'],'status':'FULFILLED','waiver_policy':'NON_WAIVABLE','proof_status':'PASS'},
  {'obligation_id':'OB_FMH_CLERK','trigger_type':'SHOT','shot_ids':['SH1'],'obligation_type':'FUNCTIONAL_MINOR_HUMAN_MASTER','fulfill_by':'STAGE_03_FREEZE','reason':'readable one-shot clerk needs style-consistent human master','authority_fields':['HUMAN_APPEARANCE'],'required_visual_fact':'clerk look','fulfillment_asset_ids':['FMH_CLERK_MASTER'],'status':'FULFILLED','waiver_policy':'NON_WAIVABLE','proof_status':'PASS'}
 ]
}
registry={
 'schema_version':7,'skill_version':'4.5.7','assets':[
  {'asset_id':'ENV_SHOP_MASTER','asset_type':'ENVIRONMENT_CLEAN_CANON','scope':'SC1','reuse_key':'ENV:SHOP_01:v1','asset_family_id':'ENVBASE_SHOP_01','subject_entity_id':None,'authority_role':'ENVIRONMENT_CANON','status':'APPROVED','layout_type':'SINGLE_FRAME','transient_content_policy':'CLEAN_CANON','population_policy':'EMPTY_ENVIRONMENT_ONLY','readable_human_count':0,'location_entity_id':'SHOP_01','obligation_ids':['OB_ENV_SHOP'],'video_usage':{'direct_input_allowed':True,'primary_visual_eligible':False}},
  {'asset_id':'FMH_CLERK_MASTER','asset_type':'FUNCTIONAL_MINOR_HUMAN_ASSET','scope':'SC1','reuse_key':'FMH:CLERK:v1','asset_family_id':'FMHBASE_CLERK','subject_entity_id':'FMH_CLERK','authority_role':'SCOPED_HUMAN_APPEARANCE','status':'APPROVED_SCOPED_FIGURE','layout_type':'SINGLE_FRAME','transient_content_policy':'CLEAN_CANON','population_policy':'NOT_APPLICABLE','readable_human_count':1,'obligation_ids':['OB_FMH_CLERK'],'video_usage':{'direct_input_allowed':True,'primary_visual_eligible':False}}
 ]
}

print('SECTION_0_DIRECT_GENERATION_ROUTING')
for at,expected in [('EMPTY_ENVIRONMENT_MASTER','ENVIRONMENT_MASTER_COVERAGE'),('FUNCTIONAL_MINOR_HUMAN_ASSET','FUNCTIONAL_MINOR_HUMAN_MASTER'),('MINOR_HUMAN_MASTER','FUNCTIONAL_MINOR_HUMAN_MASTER')]:
    cp=run([PY,'tools/asset_route_dispatcher.py',at,'--json'])
    import json as _json
    assert _json.loads(cp.stdout)['route']==expected

with tempfile.TemporaryDirectory() as td:
    td=Path(td); sp=td/'spatial.yaml'; ma=td/'manifest.yaml'; ob=td/'obligations.yaml'; rg=td/'registry.yaml'
    ywrite(sp,spatial); ywrite(ma,manifest); ywrite(ob,obligations); ywrite(rg,registry)
    print('SECTION_1_SCHEMA')
    run([PY,'validators/state_schema_lint.py','state/base_visual_authority_manifest.schema.yaml',str(ma),'--json'])
    run([PY,'validators/state_schema_lint.py','state/visual_asset_obligation.schema.yaml',str(ob),'--json'])
    run([PY,'validators/state_schema_lint.py','state/asset_registry.schema.yaml',str(rg),'--json'])
    print('SECTION_2_VALID_TIER_C_ENV_AND_ONE_SHOT_MINOR')
    run([PY,'validators/base_visual_authority_lint.py','--manifest',str(ma),'--spatial-canon',str(sp),'--obligations',str(ob),'--asset-registry',str(rg),'--phase','freeze'])
    print('SECTION_3_EMPTY_ENV_WITH_HUMAN_MUST_FAIL')
    bad=copy.deepcopy(registry); bad['assets'][0]['readable_human_count']=1; bad['assets'][0]['population_policy']='POPULATED_CANON'; badp=td/'bad_env.yaml'; ywrite(badp,bad)
    run([PY,'validators/base_visual_authority_lint.py','--manifest',str(ma),'--spatial-canon',str(sp),'--obligations',str(ob),'--asset-registry',str(badp),'--phase','freeze'],expect=2)
    print('SECTION_4_READABLE_MINOR_CANNOT_USE_PREVIS_OR_ASSEMBLY')
    badm=copy.deepcopy(manifest); badm['minor_humans'][0]['visual_owner']='TEXT_ONLY'; badm['minor_humans'][0]['human_master_asset_id']=None; badmp=td/'bad_manifest.yaml'; ywrite(badmp,badm)
    run([PY,'validators/base_visual_authority_lint.py','--manifest',str(badmp),'--spatial-canon',str(sp),'--obligations',str(ob),'--asset-registry',str(rg),'--phase','freeze'],expect=2)
    print('SECTION_5_DUPLICATE_ENTITY_REQUIREMENT_MUST_FAIL')
    dup=copy.deepcopy(manifest); dup['minor_humans'].append(copy.deepcopy(dup['minor_humans'][0])); dup['minor_humans'][-1]['requirement_id']='BVA_FMH_CLERK_2'; dupp=td/'dup.yaml'; ywrite(dupp,dup)
    run([PY,'validators/base_visual_authority_lint.py','--manifest',str(dupp),'--spatial-canon',str(sp),'--obligations',str(ob),'--asset-registry',str(rg),'--phase','freeze'],expect=2)
    print('SECTION_6_EVENT_ACTOR_CLASSIFICATION_MUST_NOT_LEAK')
    leak=copy.deepcopy(manifest); leak['actor_authority_index']=[x for x in leak['actor_authority_index'] if x['entity_id']!='FMH_CLERK']; leakp=td/'actor_leak.yaml'; ywrite(leakp,leak)
    run([PY,'validators/base_visual_authority_lint.py','--manifest',str(leakp),'--spatial-canon',str(sp),'--obligations',str(ob),'--asset-registry',str(rg),'--phase','freeze'],expect=2)
print('BASE VISUAL AUTHORITY TESTS PASSED')
