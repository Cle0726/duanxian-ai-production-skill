#!/usr/bin/env python3
import argparse,json,pathlib,yaml

def load(p):
    t=pathlib.Path(p).read_text(encoding='utf-8')
    return json.loads(t) if pathlib.Path(p).suffix.lower()=='.json' else yaml.safe_load(t)

def lint(plan,job,prompt):
    issues=[]; ri=plan.get('reference_integrity') or {}
    policy=ri.get('direct_binding_policy')
    allowed={'FULL_AUTHORITY_DIRECT_BINDING','FIELD_AUTHORITY_PROVIDER_ROUTED_BINDING'}
    if policy not in allowed: issues.append({'type':'DIRECT_BINDING_POLICY_MISSING_OR_INVALID','policy':policy})
    handoff=(plan.get('entity_binding_handoff') or {}).get('bindings') or []
    mandatory=set(ri.get('mandatory_direct_reference_ids') or []); humans=[]; envs=[]
    for b in handoff:
        et=str(b.get('entity_type') or '').upper(); sid=b.get('slot_id')
        if et in {'CHARACTER','HUMAN','MINOR_HUMAN','FUNCTIONAL_MINOR_HUMAN'} or str(sid).startswith('H_'):
            humans.append(b)
            if b.get('resolution_mode')!='DIRECT_REFERENCE': issues.append({'type':'VISIBLE_HUMAN_MASTER_NOT_DIRECT','slot_id':sid})
        if et=='ENVIRONMENT' or str(sid).startswith('E_'):
            envs.append(b)
            if b.get('resolution_mode')!='DIRECT_REFERENCE': issues.append({'type':'EMPTY_ENVIRONMENT_MASTER_NOT_DIRECT','slot_id':sid})
        if b.get('resolution_mode')=='DIRECT_REFERENCE':
            if not b.get('resolved_asset_id') or not b.get('native_token'): issues.append({'type':'MANDATORY_DIRECT_BINDING_INCOMPLETE','slot_id':sid})
            else: mandatory.add(b['resolved_asset_id'])
    jb=job.get('required_bindings') or []; roles={str(x.get('role') or '').upper() for x in jb}; aids={x.get('asset_id') for x in jb}
    required_roles=[('EMPTY_ENVIRONMENT_MASTER','EMPTY_ENVIRONMENT_DIRECT_BINDING_MISSING'),('CURRENT_SHOT_STORYBOARD_TEMPORAL_CONTROL','STORYBOARD_DIRECT_BINDING_MISSING')]
    if policy=='FULL_AUTHORITY_DIRECT_BINDING': required_roles.insert(0,('PRIMARY_VISUAL','PRIMARY_VISUAL_DIRECT_BINDING_MISSING'))
    for role,code in required_roles:
        if role not in roles: issues.append({'type':code})
    if policy=='FIELD_AUTHORITY_PROVIDER_ROUTED_BINDING':
        route=ri.get('primary_visual_route')
        if route=='OMIT_REDUNDANT_BAKED_COMPOSITE' and 'PRIMARY_VISUAL' in roles:
            issues.append({'type':'REDUNDANT_COMPOSITE_REFERENCE_COMPETITION'})
        if route not in {'OMIT_REDUNDANT_BAKED_COMPOSITE','DIRECT_UNIQUE_FIELD_OWNER','CONTINUITY_ENTRY'}:
            issues.append({'type':'PRIMARY_VISUAL_PROVIDER_ROUTE_MISSING','route':route})
        if route=='DIRECT_UNIQUE_FIELD_OWNER' and not ri.get('primary_unique_fields'):
            issues.append({'type':'PRIMARY_VISUAL_UNIQUE_FIELD_UNPROVEN'})
        if route=='OMIT_REDUNDANT_BAKED_COMPOSITE' and not ri.get('storyboard_prompt_closure'):
            issues.append({'type':'REDUNDANT_PRIMARY_OMISSION_CLOSURE_MISSING'})
    for b in humans:
        if b.get('resolved_asset_id') not in aids: issues.append({'type':'VISIBLE_HUMAN_MASTER_JOB_BINDING_MISSING','slot_id':b.get('slot_id'),'asset_id':b.get('resolved_asset_id')})
    for b in envs:
        if b.get('resolved_asset_id') not in aids: issues.append({'type':'EMPTY_ENVIRONMENT_MASTER_JOB_BINDING_MISSING','slot_id':b.get('slot_id'),'asset_id':b.get('resolved_asset_id')})
    for x in jb:
        tok=x.get('native_token')
        if tok and prompt.count(tok)!=1: issues.append({'type':'MANDATORY_NATIVE_TOKEN_COUNT_FAIL','token':tok,'count':prompt.count(tok)})
    missing=sorted(x for x in mandatory if x not in aids)
    if missing: issues.append({'type':'MANDATORY_DIRECT_REFERENCE_ID_MISSING','asset_ids':missing})
    return {'pass':not issues,'policy':policy,'human_count':len(humans),'environment_count':len(envs),'job_direct_count':len(jb),'issues':issues}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--plan',required=True); ap.add_argument('--job',required=True); ap.add_argument('--prompt',required=True); a=ap.parse_args()
    out=lint(load(a.plan),load(a.job),pathlib.Path(a.prompt).read_text(encoding='utf-8'))
    print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
