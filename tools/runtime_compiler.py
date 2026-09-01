#!/usr/bin/env python3
"""Compile a runtime only when the produced payload validates against its own runtime schema."""
import argparse, hashlib, json, pathlib, re, yaml
from jsonschema import Draft202012Validator

def load(p):
 path=pathlib.Path(p); text=path.read_text(encoding='utf-8');
 try: return json.loads(text)
 except Exception: return yaml.safe_load(text)
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def schema_name(runtime_type): return runtime_type.lower()+'.schema.yaml'
def safe_defaults(rt):
 extras={
  'ASSET_RUNTIME':{'assets':{}},
  'SPATIAL_CANON_RUNTIME':{'locations':[],'relations':[],'event_nodes':[],'character_routes':[],'planning_diagrams':[]},
  'VISUAL_EVIDENCE_RUNTIME':{'controller_mode':'UNKNOWN','assets':[]},
  'GENERATION_RUNTIME':{'host_capability':{'resolved_profile':'UNRESOLVED','image_generation':'UNKNOWN','video_generation':'UNKNOWN','reference_transport':'UNKNOWN','reference_capability_class':'UNKNOWN','supported_reference_media':[],'role_aware_reference_assignment':False},'queue':[],'completed_job_ids':[],'blocked_job_ids':[],'active_job_id':None,'scene_color_authority_map':{},'base_color_asset_id':None},
 }
 return extras.get(rt,{})
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--runtime-type',required=True); ap.add_argument('--source',action='append',default=[]); ap.add_argument('--projection'); ap.add_argument('--schema-dir',default='runtime'); ap.add_argument('--output',required=True); ap.add_argument('--skill-version',default='4.5.11'); a=ap.parse_args()
 sp=pathlib.Path(a.schema_dir)/schema_name(a.runtime_type)
 if not sp.exists(): print(json.dumps({'pass':False,'error':'RUNTIME_SCHEMA_NOT_FOUND','schema':str(sp)},ensure_ascii=False,indent=2)); return 2
 schema=load(sp); fps={str(pathlib.Path(p)):sha(p) for p in a.source}; const=((schema.get('properties') or {}).get('schema_version') or {}).get('const',1)
 payload={'runtime_type':a.runtime_type,'schema_version':const,'skill_version':a.skill_version,'status':'VALID',**safe_defaults(a.runtime_type)}
 if 'source_fingerprints' in (schema.get('properties') or {}): payload['source_fingerprints']=fps
 if 'scope' in (schema.get('properties') or {}): payload.setdefault('scope',{})
 if a.projection:
  pr=load(a.projection) or {}
  if not isinstance(pr,dict): print(json.dumps({'pass':False,'error':'PROJECTION_MUST_BE_OBJECT'},ensure_ascii=False)); return 2
  payload.update(pr)
 payload.pop('runtime_fingerprint',None)
 payload['runtime_fingerprint']=hashlib.sha256(json.dumps(payload,sort_keys=True,ensure_ascii=False,default=str).encode()).hexdigest()
 errors=sorted(Draft202012Validator(schema).iter_errors(payload),key=lambda e:list(e.absolute_path))
 if errors:
  out={'pass':False,'error':'RUNTIME_SCHEMA_CLOSURE_FAILED','schema':str(sp),'issues':[{'path':'/'.join(map(str,e.absolute_path)) or '$','message':e.message} for e in errors[:30]]}
  print(json.dumps(out,ensure_ascii=False,indent=2)); return 2
 pathlib.Path(a.output).write_text(yaml.safe_dump(payload,sort_keys=False,allow_unicode=True),encoding='utf-8')
 print(json.dumps({'pass':True,'output':a.output,'schema':str(sp),'runtime_fingerprint':payload['runtime_fingerprint']},ensure_ascii=False,indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
