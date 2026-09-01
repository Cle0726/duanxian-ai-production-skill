#!/usr/bin/env python3
"""Hard-gate mandatory white-line storyboard coverage against formal Shot State.

Supports two legitimate provenance modes:
1) SINGLE_PANEL_JOB: one real Stage04 image job generated the clean panel.
2) DERIVED_FROM_CONTACT_SHEET: one real contact-sheet image job generated the
   master and deterministic splitting produced the clean panel. No fake child job
   is required or allowed.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import yaml

CLEAN_TYPES={'STORYBOARD_CLEAN_PANEL'}
CLEAN_KEYS={
    'visible_text','visible_numbers','arrows_or_motion_lines','timecode',
    'shot_or_panel_labels','cut_or_camera_labels','caption_boxes','subtitle_or_logo'
}
QC_JOB_STATUSES={'QC_PASS_WAITING_APPROVAL','APPROVED_PROMOTED'}
APPROVED_ASSET_STATUSES={'APPROVED'}


def load(path):
    p=Path(path); text=p.read_text(encoding='utf-8')
    return json.loads(text) if p.suffix.lower()=='.json' else yaml.safe_load(text)


def selected_handle(job):
    cid=job.get('selected_candidate_id')
    if not cid: return None
    attempt=int(job.get('attempt_no') or 1)
    hs=[h for h in (job.get('result_handles') or [])
        if h.get('candidate_id')==cid
        and h.get('eligible_for_selection',True)
        and int(h.get('attempt_no') or 1)==attempt]
    return hs[0] if len(hs)==1 else None


def panel_contract_issues(asset, shot_id):
    issues=[]; aid=asset.get('asset_id')
    if asset.get('asset_type') not in CLEAN_TYPES:
        issues.append({'type':'MANDATORY_STORYBOARD_ASSET_WRONG_TYPE','shot_id':shot_id,'asset_id':aid,'asset_type':asset.get('asset_type')})
    if asset.get('shot_id')!=shot_id:
        issues.append({'type':'MANDATORY_STORYBOARD_SHOT_BINDING_MISMATCH','shot_id':shot_id,'asset_id':aid,'actual_shot_id':asset.get('shot_id')})
    if asset.get('layout_type') not in {'CLEAN_PANEL','SINGLE_FRAME'}:
        issues.append({'type':'STORYBOARD_PANEL_LAYOUT_NOT_CLEAN_SINGLE_FRAME','shot_id':shot_id,'asset_id':aid,'layout_type':asset.get('layout_type')})
    if asset.get('storyboard_render_mode')!='WHITE_LINE_STORYBOARD_ONLY':
        issues.append({'type':'STORYBOARD_NOT_WHITE_LINE_BASELINE','shot_id':shot_id,'asset_id':aid,'storyboard_render_mode':asset.get('storyboard_render_mode')})
    cl=asset.get('storyboard_cleanliness')
    if not isinstance(cl,dict):
        issues.append({'type':'STORYBOARD_CLEANLINESS_QC_MISSING','shot_id':shot_id,'asset_id':aid})
    else:
        missing=sorted(CLEAN_KEYS-set(cl))
        if missing: issues.append({'type':'STORYBOARD_CLEANLINESS_FIELDS_MISSING','shot_id':shot_id,'asset_id':aid,'fields':missing})
        dirty=sorted(k for k in CLEAN_KEYS if cl.get(k) is True)
        if dirty: issues.append({'type':'STORYBOARD_PIXEL_ANNOTATION_FAIL','shot_id':shot_id,'asset_id':aid,'present':dirty})
    vu=asset.get('video_usage') or {}
    if vu.get('primary_visual_eligible') is True:
        issues.append({'type':'BAIMIAO_STORYBOARD_PRIMARY_VISUAL_FORBIDDEN','shot_id':shot_id,'asset_id':aid})
    return issues


def validate_real_job(j, expected_target, shot_id, phase, issues, allow_parent_scope=False):
    if j.get('media_kind')!='IMAGE' or j.get('route')!='STAGE_04_STORYBOARD':
        issues.append({'type':'MANDATORY_STORYBOARD_GENERATION_JOB_SCOPE_MISMATCH','shot_id':shot_id,'asset_id':expected_target,'generation_job_id':j.get('generation_job_id')})
    if not allow_parent_scope and j.get('shot_id')!=shot_id:
        issues.append({'type':'MANDATORY_STORYBOARD_GENERATION_JOB_SHOT_SCOPE_MISMATCH','shot_id':shot_id,'asset_id':expected_target,'generation_job_id':j.get('generation_job_id'),'actual_shot_id':j.get('shot_id')})
    h=selected_handle(j)
    if not h or not h.get('captured',True) or not (h.get('file_path') or h.get('tool_result_handle')):
        issues.append({'type':'MANDATORY_STORYBOARD_REAL_RESULT_MISSING','shot_id':shot_id,'asset_id':expected_target,'generation_job_id':j.get('generation_job_id')})
        return None
    if h.get('file_path') and not h.get('tool_result_handle'):
        fp=Path(h.get('file_path'))
        if not fp.is_file(): issues.append({'type':'MANDATORY_STORYBOARD_LOCAL_RESULT_FILE_MISSING','shot_id':shot_id,'asset_id':expected_target,'generation_job_id':j.get('generation_job_id'),'file_path':h.get('file_path')})
    if not h.get('fingerprint'):
        issues.append({'type':'MANDATORY_STORYBOARD_RESULT_FINGERPRINT_MISSING','shot_id':shot_id,'asset_id':expected_target,'generation_job_id':j.get('generation_job_id')})
    elif h.get('file_path') and Path(h.get('file_path')).is_file():
        actual=hashlib.sha256(Path(h.get('file_path')).read_bytes()).hexdigest()
        if actual!=h.get('fingerprint'):
            issues.append({'type':'MANDATORY_STORYBOARD_RESULT_FINGERPRINT_INVALID','shot_id':shot_id,'asset_id':expected_target,'generation_job_id':j.get('generation_job_id'),'expected':actual,'actual':h.get('fingerprint')})
    if phase=='qc' and j.get('status') not in QC_JOB_STATUSES:
        issues.append({'type':'STORYBOARD_JOB_NOT_QC_READY','shot_id':shot_id,'asset_id':expected_target,'generation_job_id':j.get('generation_job_id'),'status':j.get('status')})
    if phase=='approved' and j.get('status')!='APPROVED_PROMOTED':
        issues.append({'type':'STORYBOARD_JOB_NOT_APPROVED_PROMOTED','shot_id':shot_id,'asset_id':expected_target,'generation_job_id':j.get('generation_job_id'),'status':j.get('status')})
    return h


def lint(registry, shot_states, jobs, phase='qc', approval=None, contact_sheet_proof=None):
    issues=[]
    assets={a.get('asset_id'):a for a in (registry.get('assets') or []) if a.get('asset_id')}
    job_by_target={}
    for j in jobs:
        tid=j.get('target_asset_id')
        if tid: job_by_target.setdefault(tid,[]).append(j)
    proof_panel_map={}
    proof_parent=None
    if isinstance(contact_sheet_proof,dict):
        proof_parent=contact_sheet_proof.get('contact_sheet_asset_id')
        proof_panel_map={p.get('panel_asset_id'):p for p in (contact_sheet_proof.get('panel_order') or []) if p.get('panel_asset_id')}

    if not shot_states:
        issues.append({'type':'STORYBOARD_EXPECTED_SHOTS_MISSING'})
        return {'pass':False,'phase':phase,'expected_shot_count':0,'covered_shot_count':0,'issues':issues}

    seen=set(); coverage={}; all_required=[]; provenance={}
    for st in shot_states:
        sid=st.get('shot_id')
        if not sid:
            issues.append({'type':'SHOT_STATE_SHOT_ID_MISSING'}); continue
        if sid in seen:
            issues.append({'type':'DUPLICATE_FORMAL_SHOT_STATE','shot_id':sid}); continue
        seen.add(sid)
        sb=st.get('storyboard') or {}
        if sb.get('mandatory_coverage_planned') is not True:
            issues.append({'type':'SHOT_MANDATORY_STORYBOARD_NOT_PLANNED','shot_id':sid})
        planned=list(dict.fromkeys(sb.get('mandatory_panel_asset_ids') or []))
        if not planned:
            issues.append({'type':'SHOT_STORYBOARD_PANEL_PLAN_IDS_MISSING','shot_id':sid}); coverage[sid]=[]; continue
        req=sb.get('required_panel_count')
        if req is None: req=len(planned)
        try: req=int(req)
        except Exception: req=0
        if req < 1: issues.append({'type':'SHOT_STORYBOARD_REQUIRED_PANEL_COUNT_INVALID','shot_id':sid,'required_panel_count':sb.get('required_panel_count')})
        if req != len(planned): issues.append({'type':'SHOT_STORYBOARD_PANEL_PLAN_COUNT_MISMATCH','shot_id':sid,'required_panel_count':req,'planned_panel_count':len(planned)})
        coverage[sid]=planned; all_required.extend(planned)
        for aid in planned:
            ax=assets.get(aid)
            if not ax:
                issues.append({'type':'MANDATORY_STORYBOARD_PANEL_MISSING_FROM_REGISTRY','shot_id':sid,'asset_id':aid}); continue
            issues.extend(panel_contract_issues(ax,sid))
            direct_jobs=job_by_target.get(aid,[])
            split=ax.get('storyboard_contact_sheet_split') or {}
            lin=ax.get('lineage') or {}
            derived=(lin.get('derivation_kind')=='STORYBOARD_PANELS_FROM_CONTACT_SHEET' or bool(split.get('contact_sheet_asset_id')))

            if derived:
                provenance[aid]='DERIVED_FROM_CONTACT_SHEET'
                if direct_jobs:
                    issues.append({'type':'CONTACT_SHEET_DERIVED_PANEL_FAKE_GENERATION_JOB_FORBIDDEN','shot_id':sid,'asset_id':aid,'job_ids':[j.get('generation_job_id') for j in direct_jobs]})
                parent=split.get('contact_sheet_asset_id')
                if not parent: issues.append({'type':'CONTACT_SHEET_DERIVED_PANEL_PARENT_MISSING','shot_id':sid,'asset_id':aid}); continue
                if proof_parent and parent!=proof_parent: issues.append({'type':'CONTACT_SHEET_DERIVED_PANEL_PROOF_PARENT_MISMATCH','shot_id':sid,'asset_id':aid,'expected':proof_parent,'actual':parent})
                if contact_sheet_proof is not None and aid not in proof_panel_map: issues.append({'type':'CONTACT_SHEET_DERIVED_PANEL_NOT_IN_PROOF','shot_id':sid,'asset_id':aid})
                pjobs=job_by_target.get(parent,[])
                if len(pjobs)!=1:
                    issues.append({'type':'CONTACT_SHEET_PARENT_GENERATION_JOB_NOT_UNIQUE','shot_id':sid,'asset_id':aid,'parent_asset_id':parent,'job_count':len(pjobs)}); continue
                ph=validate_real_job(pjobs[0],parent,sid,phase,issues,allow_parent_scope=True)
                passet=assets.get(parent)
                if not passet: issues.append({'type':'CONTACT_SHEET_PARENT_ASSET_MISSING','shot_id':sid,'asset_id':aid,'parent_asset_id':parent})
                else:
                    if passet.get('asset_type')!='STORYBOARD_CONTACT_SHEET': issues.append({'type':'CONTACT_SHEET_PARENT_ASSET_TYPE_FAIL','shot_id':sid,'asset_id':aid,'parent_asset_id':parent,'actual':passet.get('asset_type')})
                    if ph and passet.get('fingerprint')!=ph.get('fingerprint'): issues.append({'type':'CONTACT_SHEET_PARENT_ASSET_JOB_FINGERPRINT_MISMATCH','shot_id':sid,'asset_id':aid,'parent_asset_id':parent})
                if phase=='approved' and ax.get('status') not in APPROVED_ASSET_STATUSES:
                    issues.append({'type':'MANDATORY_STORYBOARD_ASSET_NOT_APPROVED','shot_id':sid,'asset_id':aid,'status':ax.get('status')})
            else:
                provenance[aid]='SINGLE_PANEL_JOB'
                if len(direct_jobs)!=1:
                    issues.append({'type':'MANDATORY_STORYBOARD_GENERATION_JOB_NOT_UNIQUE','shot_id':sid,'asset_id':aid,'job_count':len(direct_jobs)}); continue
                j=direct_jobs[0]
                h=validate_real_job(j,aid,sid,phase,issues)
                if phase=='approved':
                    if ax.get('status') not in APPROVED_ASSET_STATUSES: issues.append({'type':'MANDATORY_STORYBOARD_ASSET_NOT_APPROVED','shot_id':sid,'asset_id':aid,'status':ax.get('status')})
                    if ax.get('generation_job_id')!=j.get('generation_job_id'): issues.append({'type':'STORYBOARD_ASSET_JOB_LINEAGE_MISMATCH','shot_id':sid,'asset_id':aid,'asset_generation_job_id':ax.get('generation_job_id'),'job_id':j.get('generation_job_id')})
                    if h and ax.get('fingerprint')!=h.get('fingerprint'): issues.append({'type':'STORYBOARD_APPROVED_FINGERPRINT_MISMATCH','shot_id':sid,'asset_id':aid,'asset_fingerprint':ax.get('fingerprint'),'selected_fingerprint':h.get('fingerprint')})

    if phase=='approved':
        if not isinstance(approval,dict):
            issues.append({'type':'STORYBOARD_APPROVAL_RECORD_MISSING'})
        else:
            apr_id=approval.get('approval_id')
            if approval.get('decision')!='APPROVED': issues.append({'type':'STORYBOARD_APPROVAL_DECISION_NOT_APPROVED','decision':approval.get('decision')})
            approved_ids=set(approval.get('approved_asset_ids') or [])
            fpmap=approval.get('approved_asset_fingerprints') or {}
            expected_ids=set(all_required)
            if proof_parent: expected_ids.add(proof_parent)
            missing=sorted(expected_ids-approved_ids)
            if missing: issues.append({'type':'STORYBOARD_APPROVAL_SCOPE_GAP','asset_ids':missing})
            for aid in expected_ids:
                ax=assets.get(aid)
                if not ax: continue
                if ax.get('fingerprint') and fpmap.get(aid)!=ax.get('fingerprint'):
                    issues.append({'type':'STORYBOARD_APPROVAL_FINGERPRINT_SCOPE_MISMATCH','asset_id':aid,'expected':ax.get('fingerprint'),'approved':fpmap.get(aid)})
                if ax.get('approval_ref') not in {None,apr_id}:
                    issues.append({'type':'STORYBOARD_APPROVAL_REF_MISMATCH','asset_id':aid,'approval_id':apr_id,'asset_approval_ref':ax.get('approval_ref')})
                if provenance.get(aid)=='SINGLE_PANEL_JOB':
                    js=job_by_target.get(aid,[])
                    if len(js)==1 and js[0].get('approval_ref')!=apr_id:
                        issues.append({'type':'STORYBOARD_APPROVAL_REF_MISMATCH','asset_id':aid,'approval_id':apr_id,'job_approval_ref':js[0].get('approval_ref')})
            if proof_parent:
                pjs=job_by_target.get(proof_parent,[])
                if len(pjs)==1 and pjs[0].get('approval_ref') not in {None,apr_id}:
                    issues.append({'type':'STORYBOARD_APPROVAL_REF_MISMATCH','asset_id':proof_parent,'approval_id':apr_id,'job_approval_ref':pjs[0].get('approval_ref')})

    covered=sum(1 for sid,ids in coverage.items() if ids)
    return {'pass':not issues,'phase':phase,'expected_shot_count':len(seen),'covered_shot_count':covered,'mandatory_panel_count':len(all_required),'provenance':provenance,'issues':issues}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--registry',required=True)
    ap.add_argument('--shot-state',action='append',default=[])
    ap.add_argument('--job',action='append',default=[])
    ap.add_argument('--phase',choices=['qc','approved'],default='qc')
    ap.add_argument('--approval-record')
    ap.add_argument('--contact-sheet-proof')
    a=ap.parse_args()
    out=lint(load(a.registry),[load(x) for x in a.shot_state],[load(x) for x in a.job],a.phase,load(a.approval_record) if a.approval_record else None,load(a.contact_sheet_proof) if a.contact_sheet_proof else None)
    print(json.dumps(out,ensure_ascii=False,indent=2))
    raise SystemExit(0 if out['pass'] else 2)

if __name__=='__main__': main()
