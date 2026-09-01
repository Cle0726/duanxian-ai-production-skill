#!/usr/bin/env python3
"""Validate Generation Job ↔ Asset Registry closure and Master→Coverage→Shot Execution→Video lineage."""
import argparse, json, yaml

APPROVED_IMAGE={'APPROVED','APPROVED_SUPPORT','APPROVED_ASSEMBLY','APPROVED_SCOPED_FIGURE','APPROVED_VIDEO_CONDITIONING'}

def load(p):
    with open(p,encoding='utf-8') as f: return yaml.safe_load(f)
def jobs_from(data): return data if isinstance(data,list) else data.get('jobs',[data])

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--registry',required=True); ap.add_argument('--jobs'); ap.add_argument('--json',action='store_true'); a=ap.parse_args()
    reg=load(a.registry); assets={x.get('asset_id'):x for x in reg.get('assets',[]) if x.get('asset_id')}; issues=[]
    jobs=[]; job_by={}
    if a.jobs:
        jobs=jobs_from(load(a.jobs)); job_by={j.get('generation_job_id'):j for j in jobs if j.get('generation_job_id')}
    for x in assets.values():
        t=(x.get('asset_type') or '').upper(); lin=x.get('lineage') or {}; parents=lin.get('parent_asset_ids') or []
        if ('COVERAGE' in t or 'SHOT_EXECUTION' in t or t in {'VIDEO_FIRST_FRAME','VIDEO_TARGET_FRAME','VIDEO_LAST_FRAME','VIDEO_CONTACT_FRAME','VIDEO_KEY_POSE'}) and not parents:
            issues.append({'type':'ASSET_LINEAGE_GAP','asset_id':x.get('asset_id')})
        for pid in parents:
            if pid not in assets: issues.append({'type':'ASSET_LINEAGE_PARENT_MISSING','asset_id':x.get('asset_id'),'parent_asset_id':pid})
        if x.get('status') in APPROVED_IMAGE and x.get('media_kind')=='IMAGE' and t!='SPATIAL_PLANNING_DIAGRAM':
            jid=x.get('generation_job_id')
            if not jid: issues.append({'type':'APPROVED_GENERATED_ASSET_JOB_MISSING','asset_id':x.get('asset_id')})
            elif a.jobs:
                j=job_by.get(jid)
                if not j: issues.append({'type':'APPROVED_ASSET_JOB_RECORD_MISSING','asset_id':x.get('asset_id'),'generation_job_id':jid})
                else:
                    if j.get('media_kind')!='IMAGE' or j.get('status')!='APPROVED_PROMOTED': issues.append({'type':'APPROVED_ASSET_JOB_NOT_PROMOTED','asset_id':x.get('asset_id'),'generation_job_id':jid,'job_status':j.get('status')})
                    if j.get('target_asset_id')!=x.get('asset_id'): issues.append({'type':'APPROVED_ASSET_JOB_TARGET_MISMATCH','asset_id':x.get('asset_id'),'generation_job_id':jid,'target_asset_id':j.get('target_asset_id')})
                    sel=j.get('selected_candidate_id')
                    if sel and sel not in (x.get('candidate_record_ids') or []): issues.append({'type':'PROMOTED_CANDIDATE_NOT_RECORDED_ON_ASSET','asset_id':x.get('asset_id'),'candidate_id':sel})
    for j in jobs:
        jid=j.get('generation_job_id'); media=j.get('media_kind'); status=j.get('status'); handles=j.get('result_handles') or []
        if status in {'RESULT_AVAILABLE','CANDIDATE_CAPTURED','QC_PASS_WAITING_APPROVAL','APPROVED_PROMOTED','VIDEO_TAKE_CAPTURED'} and not handles:
            issues.append({'type':'GENERATION_RESULT_MISSING','generation_job_id':jid})
        if media=='VIDEO' and status=='APPROVED_PROMOTED': issues.append({'type':'VIDEO_JOB_ILLEGAL_ASSET_PROMOTION','generation_job_id':jid})
        if media=='IMAGE' and status=='VIDEO_TAKE_CAPTURED': issues.append({'type':'IMAGE_JOB_ILLEGAL_VIDEO_TAKE_STATE','generation_job_id':jid})
        if status=='APPROVED_PROMOTED':
            if not j.get('selected_candidate_id') or not j.get('approval_ref'): issues.append({'type':'GENERATION_PROMOTION_AUTHORITY_MISSING','generation_job_id':jid})
            x=assets.get(j.get('target_asset_id'))
            if not x or x.get('status') not in APPROVED_IMAGE or x.get('generation_job_id')!=jid:
                issues.append({'type':'GENERATION_PROMOTION_REGISTRY_NOT_CLOSED','generation_job_id':jid,'target_asset_id':j.get('target_asset_id')})
        if status=='VIDEO_TAKE_CAPTURED' and media!='VIDEO': issues.append({'type':'VIDEO_TAKE_STATE_MEDIA_MISMATCH','generation_job_id':jid})
        # Current attempt must never select a superseded retry result.
        if j.get('selected_candidate_id'):
            current=int(j.get('attempt_no') or 1); ok=[h for h in handles if h.get('candidate_id')==j.get('selected_candidate_id') and int(h.get('attempt_no') or 1)==current and h.get('eligible_for_selection',True)]
            if not ok: issues.append({'type':'SELECTED_CANDIDATE_FROM_STALE_ATTEMPT','generation_job_id':jid,'candidate_id':j.get('selected_candidate_id'),'attempt_no':current})
    out={'pass':not issues,'issues':issues}; print(json.dumps(out,ensure_ascii=False,indent=2) if a.json else out); return 1 if issues else 0
if __name__=='__main__': raise SystemExit(main())
