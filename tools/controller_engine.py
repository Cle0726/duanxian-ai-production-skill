#!/usr/bin/env python3
"""Resolve the next route deterministically from workflow state plus Generation Runtime."""
import argparse, json, yaml

def load(p):
    with open(p,encoding='utf-8') as f: return yaml.safe_load(f)

def approved_color(assets, aid, scene_id=None, look=None, global_only=False):
    x=assets.get(aid)
    if not x or x.get('status')!='APPROVED': return False
    if global_only: return x.get('asset_type') in {'GLOBAL_COLOR_CARD','BASE_COLOR_CARD'}
    if x.get('asset_type') not in {'SCENE_COLOR_CARD','SCENE_COLOR_EXTENSION_CARD'}: return False
    if scene_id and x.get('scene_id')!=scene_id: return False
    if look and look not in {'UNKNOWN','NONE'} and x.get('look_domain') not in {look,None,'UNKNOWN'}: return False
    return True

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--state',required=True); ap.add_argument('--workflow',default='controller/workflow_state_machine.yaml'); ap.add_argument('--generation-runtime'); ap.add_argument('--registry'); ap.add_argument('--json',action='store_true'); a=ap.parse_args()
    state=load(a.state); wf=load(a.workflow); current=state['workflow_state']
    states=wf.get('states') or {}; mode=state.get('mode'); initial_by_mode=wf.get('initial_state_by_mode') or {}
    if current not in states:
        out={'next_action':'BLOCKED','failure_code':'WORKFLOW_STATE_UNKNOWN','workflow_state':current,'valid_states':sorted(states)}; print(json.dumps(out,ensure_ascii=False,indent=2)); return 2
    if mode not in initial_by_mode:
        out={'next_action':'BLOCKED','failure_code':'WORKFLOW_MODE_INITIAL_STATE_UNDEFINED','mode':mode}; print(json.dumps(out,ensure_ascii=False,indent=2)); return 2
    generation_states={'EPISODE_ASSET_BUILD','STORYBOARD_IN_PROGRESS','VIDEO_CONDITIONING_IN_PROGRESS','VIDEO_GENERATION_READY'}
    if a.generation_runtime and current in generation_states:
        gr=load(a.generation_runtime); registry=load(a.registry) if a.registry else None; assets={x.get('asset_id'):x for x in (registry or {}).get('assets',[]) if x.get('asset_id')}
        scene_id=state.get('current_scene_id'); look=state.get('current_look_domain') or 'UNKNOWN'
        # Scene-bound build/conditioning/video cannot decide color lineage without the registry.
        if scene_id:
            if not registry:
                out={'next_action':'BLOCKED','route':'GENERATION_JOB_DISPATCH','failure_code':'ASSET_REGISTRY_REQUIRED_FOR_COLOR_AUTHORITY'}; print(json.dumps(out,ensure_ascii=False,indent=2)); return 2
            base=gr.get('base_color_asset_id')
            if not base or not approved_color(assets,base,global_only=True):
                out={'next_action':'BLOCKED','route':'SCENE_COLOR_CARD_DERIVATION','failure_code':'BASE_COLOR_AUTHORITY_INVALID','base_color_asset_id':base}; print(json.dumps(out,ensure_ascii=False,indent=2)); return 2
            scope_key=f'{scene_id}:{look}'; cmap=gr.get('scene_color_authority_map') or {}; cid=cmap.get(scope_key)
            if not cid or not approved_color(assets,cid,scene_id,look):
                matches=[x for x in assets.values() if approved_color(assets,x.get('asset_id'),scene_id,look)]
                if len(matches)==1:
                    out={'next_action':'SYNC_EXISTING_SCENE_COLOR_AUTHORITY','route':'SCENE_COLOR_CARD_DERIVATION','scene_id':scene_id,'look_domain':look,'scene_color_asset_id':matches[0].get('asset_id'),'base_color_asset_id':base}; print(json.dumps(out,ensure_ascii=False,indent=2)); return 0
                if len(matches)>1:
                    out={'next_action':'BLOCKED','route':'SCENE_COLOR_CARD_DERIVATION','failure_code':'AMBIGUOUS_APPROVED_SCENE_COLOR_AUTHORITY','scene_id':scene_id,'look_domain':look,'asset_ids':[x.get('asset_id') for x in matches]}; print(json.dumps(out,ensure_ascii=False,indent=2)); return 2
                out={'next_action':'DERIVE_SCENE_COLOR_AUTHORITY','route':'SCENE_COLOR_CARD_DERIVATION','scene_id':scene_id,'look_domain':look,'base_color_asset_id':base,'invalid_existing_color_asset_id':cid}; print(json.dumps(out,ensure_ascii=False,indent=2)); return 0
        if gr.get('active_job_id'):
            out={'next_action':'EXECUTE_GENERATION_JOB','active_job_id':gr['active_job_id'],'route':'GENERATION_JOB_EXECUTOR'}; print(json.dumps(out,ensure_ascii=False,indent=2)); return 0
        if gr.get('queue'):
            out={'next_action':'DISPATCH_NEXT_GENERATION_JOB','active_job_id':gr['queue'][0],'route':'GENERATION_JOB_DISPATCH'}; print(json.dumps(out,ensure_ascii=False,indent=2)); return 0
    matches=[]
    for t in wf.get('transitions',[]):
        if t.get('from')==current or current in t.get('from_any',[]): matches.append(t)
    out={'workflow_state':current,'candidate_transitions':[{'id':t.get('id'),'to':t.get('to'),'route':t.get('route'),'requires':t.get('requires',[])} for t in matches]}
    print(json.dumps(out,ensure_ascii=False,indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
