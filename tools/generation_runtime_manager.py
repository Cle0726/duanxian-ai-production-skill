#!/usr/bin/env python3
"""Deterministically maintain GENERATION_RUNTIME queue/active/completed/color map."""
import argparse, json, pathlib, yaml

def load(p):
 with open(p,encoding='utf-8') as f: return yaml.safe_load(f)
def dump(d,p): pathlib.Path(p).write_text(yaml.safe_dump(d,sort_keys=False,allow_unicode=True),encoding='utf-8')
def fail(code,**kw): print(json.dumps({'pass':False,'error':code,**kw},ensure_ascii=False,indent=2)); return 2

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--runtime',required=True); ap.add_argument('--job'); ap.add_argument('--action',required=True,choices=['ENQUEUE','ACTIVATE','COMPLETE','BLOCK','REGISTER_COLOR']); ap.add_argument('--registry'); ap.add_argument('--asset-id'); ap.add_argument('--scene-id'); ap.add_argument('--look-domain'); ap.add_argument('--output',required=True); a=ap.parse_args()
 rt=load(a.runtime); q=rt.setdefault('queue',[]); done=rt.setdefault('completed_job_ids',[]); blocked=rt.setdefault('blocked_job_ids',[])
 if rt.get('runtime_type')!='GENERATION_RUNTIME': return fail('NOT_GENERATION_RUNTIME')
 if a.action=='REGISTER_COLOR':
  if not (a.registry and a.asset_id and a.scene_id and a.look_domain): return fail('REGISTER_COLOR_REQUIRES_REGISTRY_ASSET_SCENE_LOOK')
  reg=load(a.registry); ax=next((x for x in reg.get('assets',[]) if x.get('asset_id')==a.asset_id),None)
  if not ax or ax.get('status')!='APPROVED' or ax.get('asset_type') not in {'SCENE_COLOR_CARD','SCENE_COLOR_EXTENSION_CARD'} or ax.get('scene_id')!=a.scene_id or ax.get('look_domain') not in {a.look_domain,None,'UNKNOWN'}:
   return fail('SCENE_COLOR_AUTHORITY_INVALID_FOR_RUNTIME_SYNC',asset_id=a.asset_id)
  rt.setdefault('scene_color_authority_map',{})[f'{a.scene_id}:{a.look_domain}']=a.asset_id
  dump(rt,a.output); print(json.dumps({'pass':True,'action':a.action,'scene_color_authority_map':rt.get('scene_color_authority_map')},ensure_ascii=False,indent=2)); return 0
 if not a.job: return fail('JOB_REQUIRED_FOR_ACTION',action=a.action)
 j=load(a.job); jid=j.get('generation_job_id')
 if a.action=='ENQUEUE':
  if jid not in q and jid not in done: q.append(jid)
 elif a.action=='ACTIVATE':
  if jid not in q: return fail('JOB_NOT_QUEUED',generation_job_id=jid)
  if rt.get('active_job_id') not in {None,jid}: return fail('ANOTHER_JOB_ALREADY_ACTIVE',active_job_id=rt.get('active_job_id'))
  rt['active_job_id']=jid
 elif a.action=='BLOCK':
  if jid not in blocked: blocked.append(jid)
  if rt.get('active_job_id')==jid: rt['active_job_id']=None
 elif a.action=='COMPLETE':
  expected='APPROVED_PROMOTED' if j.get('media_kind')=='IMAGE' else 'VIDEO_TAKE_CAPTURED'
  if j.get('status')!=expected: return fail('JOB_NOT_AT_COMPLETION_STATE',expected=expected,actual=j.get('status'))
  if j.get('media_kind')=='IMAGE':
   if not a.registry: return fail('REGISTRY_REQUIRED_TO_COMPLETE_IMAGE_JOB')
   reg=load(a.registry); ax=next((x for x in reg.get('assets',[]) if x.get('asset_id')==j.get('target_asset_id')),None)
   if not ax or ax.get('generation_job_id')!=jid or ax.get('status') not in {'APPROVED','APPROVED_SUPPORT','APPROVED_ASSEMBLY','APPROVED_SCOPED_FIGURE','APPROVED_VIDEO_CONDITIONING'}:
    return fail('IMAGE_JOB_REGISTRY_PROMOTION_NOT_CLOSED',target_asset_id=j.get('target_asset_id'))
   if (j.get('target_asset_type') or '').upper() in {'SCENE_COLOR_CARD','SCENE_COLOR_EXTENSION_CARD'}:
    if not j.get('scene_id'): return fail('SCENE_COLOR_JOB_SCOPE_MISSING')
    key=f"{j.get('scene_id')}:{j.get('look_domain') or 'UNKNOWN'}"; rt.setdefault('scene_color_authority_map',{})[key]=j.get('target_asset_id')
   if (j.get('target_asset_type') or '').upper() in {'GLOBAL_COLOR_CARD','BASE_COLOR_CARD'}: rt['base_color_asset_id']=j.get('target_asset_id')
  while jid in q: q.remove(jid)
  while jid in blocked: blocked.remove(jid)
  if jid not in done: done.append(jid)
  if rt.get('active_job_id')==jid: rt['active_job_id']=None
 dump(rt,a.output); print(json.dumps({'pass':True,'action':a.action,'generation_job_id':jid,'active_job_id':rt.get('active_job_id'),'queue':rt.get('queue'),'completed_job_ids':rt.get('completed_job_ids'),'scene_color_authority_map':rt.get('scene_color_authority_map',{})},ensure_ascii=False,indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
