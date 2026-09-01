#!/usr/bin/env python3
"""Promote one approved IMAGE Generation Job candidate into an existing planned Asset Registry record."""
import argparse, hashlib, json, pathlib, yaml

def load(p):
 with open(p,encoding='utf-8') as f: return yaml.safe_load(f)
def dump(d,p): pathlib.Path(p).write_text(yaml.safe_dump(d,sort_keys=False,allow_unicode=True),encoding='utf-8')
def fail(code,**kw): print(json.dumps({'pass':False,'error':code,**kw},ensure_ascii=False,indent=2)); return 2
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--job',required=True); ap.add_argument('--registry',required=True); ap.add_argument('--output',required=True); ap.add_argument('--approved-status'); a=ap.parse_args()
 j=load(a.job); reg=load(a.registry)
 if j.get('media_kind')!='IMAGE': return fail('VIDEO_MUST_NOT_BE_PROMOTED_INTO_ASSET_REGISTRY')
 if j.get('status')!='APPROVED_PROMOTED': return fail('JOB_NOT_APPROVED_FOR_PROMOTION',status=j.get('status'))
 sel=j.get('selected_candidate_id'); approval=j.get('approval_ref')
 if not sel or not approval: return fail('PROMOTION_AUTHORITY_MISSING')
 handles=[h for h in j.get('result_handles',[]) if h.get('candidate_id')==sel and h.get('eligible_for_selection',True) and int(h.get('attempt_no') or 1)==int(j.get('attempt_no') or 1)]
 if len(handles)!=1: return fail('CURRENT_SELECTED_RESULT_HANDLE_NOT_UNIQUE',candidate_id=sel)
 h=handles[0]
 if not (h.get('file_path') or h.get('tool_result_handle')): return fail('REAL_RESULT_HANDLE_MISSING')
 target=None
 for x in reg.get('assets',[]):
  if x.get('asset_id')==j.get('target_asset_id'): target=x; break
 if target is None: return fail('PLANNED_ASSET_STUB_MISSING',target_asset_id=j.get('target_asset_id'))
 if target.get('status') in {'APPROVED','APPROVED_SUPPORT','APPROVED_ASSEMBLY','APPROVED_SCOPED_FIGURE','APPROVED_VIDEO_CONDITIONING'} and target.get('generation_job_id') not in {None,j.get('generation_job_id')}:
  return fail('TARGET_ASSET_ALREADY_APPROVED_BY_DIFFERENT_JOB')
 t=(j.get('target_asset_type') or '').upper()
 status=a.approved_status or ('APPROVED_VIDEO_CONDITIONING' if ('VIDEO_' in t and ('FRAME' in t or 'POSE' in t)) or t in {'SHOT_EXECUTION_FRAME','PRIMARY_VISUAL_CONDITIONING'} else 'APPROVED_ASSEMBLY' if 'ASSEMBLY' in t else 'APPROVED_SUPPORT' if 'SUPPORT' in t else 'APPROVED')
 target['status']=status; target['generation_job_id']=j.get('generation_job_id'); target['approval_ref']=approval; target['file_path']=h.get('file_path') or target.get('file_path'); target['candidate_record_ids']=list(dict.fromkeys((target.get('candidate_record_ids') or [])+[sel])); target['lineage']=j.get('lineage') or {'parent_asset_ids':[]}
 fp=h.get('fingerprint')
 if not fp and h.get('file_path') and pathlib.Path(h['file_path']).is_file(): fp=hashlib.sha256(pathlib.Path(h['file_path']).read_bytes()).hexdigest()
 if fp: target['fingerprint']=fp; target['fingerprint_type']='FILE_SHA256'
 cb=j.get('color_binding') or {}; cid=cb.get('color_asset_id'); target['color_authority_id']=cid
 if cb.get('authority_level')=='SCENE_COLOR_CARD': target['scene_color_authority_id']=cid
 target['color_authority_level']=cb.get('authority_level','UNKNOWN'); target['color_projection_mode']=cb.get('projection_mode') or ('DIRECT_COLOR_REFERENCE' if cb.get('required') else 'NOT_APPLICABLE')
 if j.get('scene_id') is not None: target['scene_id']=j.get('scene_id')
 if j.get('look_domain') is not None: target['look_domain']=j.get('look_domain')
 dump(reg,a.output); print(json.dumps({'pass':True,'asset_id':target.get('asset_id'),'status':status,'generation_job_id':j.get('generation_job_id'),'candidate_id':sel},ensure_ascii=False,indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
