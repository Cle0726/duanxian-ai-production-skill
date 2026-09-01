#!/usr/bin/env python3
"""Deterministic Generation Job lifecycle, retry isolation and result capture."""
import argparse, json, pathlib, yaml

ALLOWED={
 'PLANNED':{'READY','BLOCKED','CANCELLED'},
 'READY':{'RUNNING','BLOCKED','CANCELLED'},
 'RUNNING':{'RESULT_AVAILABLE','RETRY_REQUIRED','BLOCKED'},
 'RESULT_AVAILABLE':{'CANDIDATE_CAPTURED','RETRY_REQUIRED'},
 'CANDIDATE_CAPTURED':{'QC_PASS_WAITING_APPROVAL','VIDEO_TAKE_CAPTURED','RETRY_REQUIRED'},
 'QC_PASS_WAITING_APPROVAL':{'APPROVED_PROMOTED','RETRY_REQUIRED'},
 'VIDEO_TAKE_CAPTURED':{'RETRY_REQUIRED'},
 'RETRY_REQUIRED':{'READY','BLOCKED','CANCELLED'},
 'BLOCKED':{'READY','CANCELLED'},
 'APPROVED_PROMOTED':set(),'CANCELLED':set(),
}

def load(path):
 p=pathlib.Path(path); text=p.read_text(encoding='utf-8'); return json.loads(text) if p.suffix.lower()=='.json' else yaml.safe_load(text)
def dump(data,path):
 p=pathlib.Path(path); p.write_text((json.dumps(data,ensure_ascii=False,indent=2)+'\n') if p.suffix.lower()=='.json' else yaml.safe_dump(data,sort_keys=False,allow_unicode=True),encoding='utf-8')
def fail(msg): print(json.dumps({'pass':False,'error':msg},ensure_ascii=False)); return 2

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('job'); ap.add_argument('--to'); ap.add_argument('--candidate-id'); ap.add_argument('--tool-result-handle'); ap.add_argument('--file-path'); ap.add_argument('--fingerprint'); ap.add_argument('--select-candidate'); ap.add_argument('--approval-ref'); ap.add_argument('--write'); ap.add_argument('--json',action='store_true'); a=ap.parse_args()
 j=load(a.job); old=j['status']; media=j.get('media_kind'); attempt=int(j.get('attempt_no') or 1)
 if a.to:
  if a.to not in ALLOWED.get(old,set()): return fail(f'ILLEGAL_JOB_TRANSITION:{old}->{a.to}')
  if media=='VIDEO' and a.to=='READY':
   for key in ('video_unit_id','prompt_ref','prompt_fingerprint','execution_plan_ref','execution_plan_fingerprint','prompt_artifact_ref'):
    if not j.get(key): return fail(f'VIDEO_READY_REQUIRES_{key.upper()}')
  if a.to=='QC_PASS_WAITING_APPROVAL' and media!='IMAGE': return fail('VIDEO_JOB_CANNOT_ENTER_IMAGE_APPROVAL_LIFECYCLE')
  if a.to=='APPROVED_PROMOTED' and media!='IMAGE': return fail('VIDEO_JOB_CANNOT_PROMOTE_TO_ASSET')
  if a.to=='VIDEO_TAKE_CAPTURED' and media!='VIDEO': return fail('IMAGE_JOB_CANNOT_ENTER_VIDEO_TAKE_CAPTURED')
  if a.to=='RETRY_REQUIRED':
   j['selected_candidate_id']=None; j['approval_ref']=None
   for h in j.get('result_handles',[]) or []: h['eligible_for_selection']=False
  if old=='RETRY_REQUIRED' and a.to=='READY':
   j['attempt_no']=attempt+1; attempt+=1; j['selected_candidate_id']=None; j['approval_ref']=None
  j['status']=a.to
 if a.candidate_id:
  if j['status'] not in {'RESULT_AVAILABLE','CANDIDATE_CAPTURED'}: return fail('CANDIDATE_CAPTURE_REQUIRES_RESULT_AVAILABLE')
  if not (a.tool_result_handle or a.file_path): return fail('CANDIDATE_CAPTURE_REQUIRES_REAL_RESULT_HANDLE')
  j.setdefault('result_handles',[]).append({'candidate_id':a.candidate_id,'tool_result_handle':a.tool_result_handle,'file_path':a.file_path,'fingerprint':a.fingerprint,'captured':True,'attempt_no':int(j.get('attempt_no') or 1),'eligible_for_selection':True})
  j['status']='CANDIDATE_CAPTURED'
 if a.select_candidate:
  ids={x.get('candidate_id') for x in j.get('result_handles',[]) if x.get('eligible_for_selection',True) and int(x.get('attempt_no') or 1)==int(j.get('attempt_no') or 1)}
  if a.select_candidate not in ids: return fail('SELECTED_CANDIDATE_NOT_FOUND_IN_CURRENT_ATTEMPT')
  j['selected_candidate_id']=a.select_candidate
 if a.approval_ref:
  if media!='IMAGE': return fail('VIDEO_APPROVAL_BELONGS_TO_VIDEO_QC_NOT_GENERATION_JOB')
  j['approval_ref']=a.approval_ref
 if a.to=='APPROVED_PROMOTED' and (not j.get('selected_candidate_id') or not j.get('approval_ref')): return fail('PROMOTION_REQUIRES_SELECTED_CANDIDATE_AND_APPROVAL')
 if a.to=='VIDEO_TAKE_CAPTURED' and not j.get('result_handles'): return fail('VIDEO_TAKE_CAPTURE_REQUIRES_RESULT')
 if a.write: dump(j,a.write)
 out={'pass':True,'generation_job_id':j.get('generation_job_id'),'media_kind':media,'status':j['status'],'attempt_no':j.get('attempt_no',1),'result_count':len(j.get('result_handles',[]))}
 print(json.dumps(out,ensure_ascii=False,indent=2) if a.json else yaml.safe_dump(j,sort_keys=False,allow_unicode=True)); return 0
if __name__=='__main__': raise SystemExit(main())
