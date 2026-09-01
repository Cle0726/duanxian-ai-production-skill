#!/usr/bin/env python3
"""Hard gate for Contact-Sheet-First white-line storyboard proof.

Canonical lineage:
  one real STORYBOARD_CONTACT_SHEET image Generation Job
  -> deterministic splitter manifest
  -> N derived STORYBOARD_CLEAN_PANEL assets
  -> panel QC/entity binding
  -> one user approval covering master + derived fingerprints

Derived panels MUST NOT need fake per-panel generation jobs. Their provenance is
proved by the parent job, parent fingerprint, splitter manifest and panel SHA256.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import yaml

QC_OK={'QC_PASS_WAITING_APPROVAL','APPROVED'}
APPROVED={'APPROVED'}
CLEAN_KEYS={
    'visible_text','visible_numbers','arrows_or_motion_lines','timecode',
    'shot_or_panel_labels','cut_or_camera_labels','caption_boxes','subtitle_or_logo',
    'recognizable_face_present','recognizable_hair_present',
    'recognizable_costume_detail_present','identity_specific_feature_present'
}


def load(p):
    if not p: return None
    path=Path(p); text=path.read_text(encoding='utf-8')
    return json.loads(text) if path.suffix.lower()=='.json' else yaml.safe_load(text)


def add(issues,t,**kw):
    d={'type':t}; d.update(kw); issues.append(d)


def sha256(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(65536),b''): h.update(chunk)
    return h.hexdigest()


def selected_handle(job):
    cid=job.get('selected_candidate_id')
    if not cid: return None
    attempt=int(job.get('attempt_no') or 1)
    hs=[h for h in (job.get('result_handles') or [])
        if h.get('candidate_id')==cid
        and h.get('eligible_for_selection',True)
        and int(h.get('attempt_no') or 1)==attempt]
    return hs[0] if len(hs)==1 else None


def cleanliness(asset, issues, prefix='CONTACT_SHEET'):
    aid=asset.get('asset_id')
    cl=asset.get('storyboard_cleanliness') or {}
    dirty=sorted(k for k in CLEAN_KEYS if cl.get(k) is True)
    if dirty: add(issues,f'{prefix}_PIXEL_OR_IDENTITY_CONTAMINATION',asset_id=aid,present=dirty)


def lint(proof, registry, jobs=None, phase='qc', approval=None):
    issues=[]; jobs=jobs or []
    assets={a.get('asset_id'):a for a in (registry.get('assets') or []) if a.get('asset_id')}
    aid=proof.get('contact_sheet_asset_id'); cs=assets.get(aid)

    # Proof shape cannot claim more panels than it actually enumerates.
    order=proof.get('panel_order') or []
    expected=proof.get('panel_count')
    rows=proof.get('rows'); cols=proof.get('cols')
    if expected != len(order):
        add(issues,'CONTACT_SHEET_PANEL_COUNT_MISMATCH',declared=expected,actual=len(order))
    if isinstance(rows,int) and isinstance(cols,int) and rows*cols != expected:
        add(issues,'CONTACT_SHEET_GRID_CAPACITY_MISMATCH',rows=rows,cols=cols,panel_count=expected,capacity=rows*cols)
    indices=[x.get('panel_index') for x in order]
    if indices != list(range(1,(expected or 0)+1)):
        add(issues,'CONTACT_SHEET_PANEL_INDEX_SEQUENCE_INVALID',expected=list(range(1,(expected or 0)+1)),actual=indices)
    pids=[x.get('panel_asset_id') for x in order]
    if len(pids)!=len(set(pids)):
        add(issues,'CONTACT_SHEET_DUPLICATE_PANEL_ASSET_ID',panel_asset_ids=pids)

    # Master asset is structural proof only, never direct video input/primary.
    if not cs:
        add(issues,'CONTACT_SHEET_ASSET_MISSING',asset_id=aid)
    else:
        if cs.get('asset_type')!='STORYBOARD_CONTACT_SHEET': add(issues,'CONTACT_SHEET_ASSET_TYPE_FAIL',asset_id=aid,actual=cs.get('asset_type'))
        if cs.get('storyboard_render_mode')!='WHITE_LINE_STORYBOARD_ONLY': add(issues,'CONTACT_SHEET_NOT_WHITE_LINE',asset_id=aid)
        if cs.get('layout_type')!='CONTACT_SHEET': add(issues,'CONTACT_SHEET_LAYOUT_INVALID',asset_id=aid,actual=cs.get('layout_type'))
        cleanliness(cs,issues)
        vu=cs.get('video_usage') or {}
        if vu.get('primary_visual_eligible') is True: add(issues,'CONTACT_SHEET_PRIMARY_VISUAL_FORBIDDEN',asset_id=aid)
        if vu.get('direct_input_allowed') is not False: add(issues,'CONTACT_SHEET_DIRECT_VIDEO_REFERENCE_FORBIDDEN',asset_id=aid,actual=vu.get('direct_input_allowed'))
        if cs.get('fingerprint')!=proof.get('contact_sheet_fingerprint'): add(issues,'CONTACT_SHEET_FINGERPRINT_MISMATCH',asset_id=aid)
        if phase=='qc' and cs.get('status') not in QC_OK: add(issues,'CONTACT_SHEET_STATUS_FAIL',asset_id=aid,status=cs.get('status'))
        if phase=='approved' and cs.get('status') not in APPROVED: add(issues,'CONTACT_SHEET_NOT_APPROVED',asset_id=aid,status=cs.get('status'))

    if proof.get('splitter_tool')!='tools/storyboard_contact_sheet_splitter.py': add(issues,'CONTACT_SHEET_SPLITTER_TOOL_INVALID')

    # A persisted deterministic split manifest is mandatory proof.
    mref=proof.get('manifest_ref')
    manifest=None
    if not mref:
        add(issues,'CONTACT_SHEET_SPLIT_MANIFEST_MISSING')
    else:
        mp=Path(mref)
        if not mp.is_file():
            add(issues,'CONTACT_SHEET_SPLIT_MANIFEST_FILE_MISSING',manifest_ref=mref)
        else:
            try: manifest=load(mref)
            except Exception as e: add(issues,'CONTACT_SHEET_SPLIT_MANIFEST_PARSE_FAIL',manifest_ref=mref,error=str(e))
    manifest_panels={}
    if isinstance(manifest,dict):
        if manifest.get('splitter_tool')!='tools/storyboard_contact_sheet_splitter.py': add(issues,'CONTACT_SHEET_MANIFEST_TOOL_MISMATCH')
        if manifest.get('source_sha256')!=proof.get('contact_sheet_fingerprint'): add(issues,'CONTACT_SHEET_MANIFEST_SOURCE_FINGERPRINT_MISMATCH',expected=proof.get('contact_sheet_fingerprint'),actual=manifest.get('source_sha256'))
        if manifest.get('rows')!=rows or manifest.get('cols')!=cols: add(issues,'CONTACT_SHEET_MANIFEST_GRID_MISMATCH',expected=[rows,cols],actual=[manifest.get('rows'),manifest.get('cols')])
        mps=manifest.get('panels') or []
        if len(mps)!=expected: add(issues,'CONTACT_SHEET_MANIFEST_PANEL_COUNT_MISMATCH',expected=expected,actual=len(mps))
        manifest_panels={p.get('index'):p for p in mps if p.get('index') is not None}
        if sorted(manifest_panels)!=list(range(1,(expected or 0)+1)): add(issues,'CONTACT_SHEET_MANIFEST_INDEX_SEQUENCE_INVALID',actual=sorted(manifest_panels))

    # Every derived panel must close split metadata + lineage + file fingerprint.
    for row in order:
        idx=row.get('panel_index'); pid=row.get('panel_asset_id'); a=assets.get(pid)
        if not a:
            add(issues,'CONTACT_SHEET_SPLIT_PANEL_MISSING',asset_id=pid); continue
        if a.get('asset_type')!='STORYBOARD_CLEAN_PANEL': add(issues,'CONTACT_SHEET_SPLIT_PANEL_TYPE_FAIL',asset_id=pid,actual=a.get('asset_type'))
        if a.get('storyboard_render_mode')!='WHITE_LINE_STORYBOARD_ONLY': add(issues,'CONTACT_SHEET_SPLIT_PANEL_NOT_WHITE_LINE',asset_id=pid)
        if a.get('layout_type') not in {'CLEAN_PANEL','SINGLE_FRAME'}: add(issues,'CONTACT_SHEET_SPLIT_PANEL_LAYOUT_FAIL',asset_id=pid,actual=a.get('layout_type'))
        cleanliness(a,issues,'CONTACT_SHEET_SPLIT_PANEL')
        sp=a.get('storyboard_contact_sheet_split') or {}
        if sp.get('splitter_tool')!='tools/storyboard_contact_sheet_splitter.py': add(issues,'CONTACT_SHEET_SPLIT_METADATA_TOOL_MISMATCH',asset_id=pid)
        if sp.get('contact_sheet_asset_id')!=aid: add(issues,'CONTACT_SHEET_SPLIT_PARENT_MISMATCH',asset_id=pid)
        if sp.get('contact_sheet_fingerprint')!=proof.get('contact_sheet_fingerprint'): add(issues,'CONTACT_SHEET_SPLIT_PARENT_FINGERPRINT_MISMATCH',asset_id=pid)
        if sp.get('panel_index')!=idx: add(issues,'CONTACT_SHEET_SPLIT_INDEX_MISMATCH',asset_id=pid,expected=idx,actual=sp.get('panel_index'))
        if mref and sp.get('manifest_ref')!=mref: add(issues,'CONTACT_SHEET_SPLIT_MANIFEST_REF_MISMATCH',asset_id=pid,expected=mref,actual=sp.get('manifest_ref'))
        lin=a.get('lineage') or {}
        if lin.get('derivation_kind')!='STORYBOARD_PANELS_FROM_CONTACT_SHEET': add(issues,'CONTACT_SHEET_SPLIT_LINEAGE_KIND_INVALID',asset_id=pid,actual=lin.get('derivation_kind'))
        if aid not in (lin.get('parent_asset_ids') or []): add(issues,'CONTACT_SHEET_SPLIT_LINEAGE_PARENT_MISSING',asset_id=pid,parent_asset_id=aid)
        mp=manifest_panels.get(idx)
        if mp:
            if sp.get('row')!=mp.get('row') or sp.get('col')!=mp.get('col'): add(issues,'CONTACT_SHEET_SPLIT_CELL_MISMATCH',asset_id=pid,expected=[mp.get('row'),mp.get('col')],actual=[sp.get('row'),sp.get('col')])
            if a.get('fingerprint')!=mp.get('sha256'): add(issues,'CONTACT_SHEET_SPLIT_PANEL_FINGERPRINT_MISMATCH',asset_id=pid,expected=mp.get('sha256'),actual=a.get('fingerprint'))
            fp=mp.get('file_path')
            if not fp:
                add(issues,'CONTACT_SHEET_SPLIT_FILE_PATH_MISSING',asset_id=pid,panel_index=idx)
            else:
                fpath=Path(fp)
                if not fpath.is_file():
                    add(issues,'CONTACT_SHEET_SPLIT_FILE_MISSING',asset_id=pid,panel_index=idx,file_path=fp)
                else:
                    actual=sha256(fpath)
                    if actual!=mp.get('sha256'): add(issues,'CONTACT_SHEET_SPLIT_FILE_SHA_INVALID',asset_id=pid,expected=mp.get('sha256'),actual=actual)
                    if a.get('fingerprint')!=actual: add(issues,'CONTACT_SHEET_SPLIT_REGISTRY_FINGERPRINT_NOT_ACTUAL_FILE_SHA',asset_id=pid,expected=actual,actual=a.get('fingerprint'))
                afp=a.get('file_path')
                if not afp:
                    add(issues,'CONTACT_SHEET_SPLIT_REGISTRY_FILE_PATH_MISSING',asset_id=pid,panel_index=idx)
                else:
                    apath=Path(afp)
                    if not apath.is_file(): add(issues,'CONTACT_SHEET_SPLIT_REGISTRY_FILE_MISSING',asset_id=pid,panel_index=idx,file_path=afp)
                    if apath.resolve()!=fpath.resolve(): add(issues,'CONTACT_SHEET_SPLIT_FILE_PATH_MISMATCH',asset_id=pid,expected=fp,actual=afp)
        if phase=='approved' and a.get('status')!='APPROVED': add(issues,'CONTACT_SHEET_SPLIT_PANEL_NOT_APPROVED',asset_id=pid,status=a.get('status'))

    # Parent generation proof: exactly one real image job for the contact-sheet master.
    if jobs:
        parent_jobs=[j for j in jobs if j.get('target_asset_id')==aid]
        if len(parent_jobs)!=1:
            add(issues,'CONTACT_SHEET_PARENT_GENERATION_JOB_NOT_UNIQUE',asset_id=aid,job_count=len(parent_jobs))
        else:
            j=parent_jobs[0]
            if j.get('media_kind')!='IMAGE' or j.get('route')!='STAGE_04_STORYBOARD': add(issues,'CONTACT_SHEET_PARENT_GENERATION_JOB_SCOPE_MISMATCH',generation_job_id=j.get('generation_job_id'))
            h=selected_handle(j)
            if not h or not h.get('captured',True) or not (h.get('file_path') or h.get('tool_result_handle')): add(issues,'CONTACT_SHEET_PARENT_REAL_RESULT_MISSING',generation_job_id=j.get('generation_job_id'))
            else:
                if h.get('fingerprint')!=proof.get('contact_sheet_fingerprint'): add(issues,'CONTACT_SHEET_PARENT_RESULT_FINGERPRINT_MISMATCH',generation_job_id=j.get('generation_job_id'),expected=proof.get('contact_sheet_fingerprint'),actual=h.get('fingerprint'))
            if phase=='qc' and j.get('status') not in {'QC_PASS_WAITING_APPROVAL','APPROVED_PROMOTED'}: add(issues,'CONTACT_SHEET_PARENT_JOB_NOT_QC_READY',generation_job_id=j.get('generation_job_id'),status=j.get('status'))
            if phase=='approved' and j.get('status')!='APPROVED_PROMOTED': add(issues,'CONTACT_SHEET_PARENT_JOB_NOT_APPROVED_PROMOTED',generation_job_id=j.get('generation_job_id'),status=j.get('status'))
        # Derived panels must not invent independent image generation jobs.
        for pid in pids:
            child_jobs=[j for j in jobs if j.get('target_asset_id')==pid]
            if child_jobs: add(issues,'CONTACT_SHEET_DERIVED_PANEL_FAKE_GENERATION_JOB_FORBIDDEN',asset_id=pid,job_ids=[j.get('generation_job_id') for j in child_jobs])

    # One approval record covers the exact master + derived fingerprints.
    if phase=='approved':
        if not isinstance(approval,dict):
            add(issues,'CONTACT_SHEET_APPROVAL_RECORD_MISSING')
        else:
            if approval.get('decision')!='APPROVED': add(issues,'CONTACT_SHEET_APPROVAL_DECISION_NOT_APPROVED',decision=approval.get('decision'))
            expected_ids={aid,*pids}; approved_ids=set(approval.get('approved_asset_ids') or [])
            missing=sorted(expected_ids-approved_ids)
            if missing: add(issues,'CONTACT_SHEET_APPROVAL_SCOPE_GAP',asset_ids=missing)
            fpmap=approval.get('approved_asset_fingerprints') or {}
            for x in expected_ids:
                ax=assets.get(x)
                if ax and fpmap.get(x)!=ax.get('fingerprint'): add(issues,'CONTACT_SHEET_APPROVAL_FINGERPRINT_SCOPE_MISMATCH',asset_id=x,expected=ax.get('fingerprint'),approved=fpmap.get(x))
            apr=approval.get('approval_id')
            for x in expected_ids:
                ax=assets.get(x)
                if ax and ax.get('approval_ref') not in {None,apr}: add(issues,'CONTACT_SHEET_APPROVAL_REF_MISMATCH',asset_id=x,expected=apr,actual=ax.get('approval_ref'))

    return {'pass':not issues,'phase':phase,'declared_panel_count':expected,'actual_panel_count':len(order),'issues':issues}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--proof',required=True)
    ap.add_argument('--registry',required=True)
    ap.add_argument('--job',action='append',default=[])
    ap.add_argument('--phase',choices=['qc','approved'],default='qc')
    ap.add_argument('--approval-record')
    a=ap.parse_args()
    out=lint(load(a.proof),load(a.registry),[load(x) for x in a.job],a.phase,load(a.approval_record) if a.approval_record else None)
    print(json.dumps(out,ensure_ascii=False,indent=2))
    raise SystemExit(0 if out['pass'] else 2)

if __name__=='__main__': main()
