#!/usr/bin/env python3
"""Validate shot-to-generation envelopes and the mandatory white-line grid gate.

Core rule: any non-ONER or multi-cut/multi-shot envelope MUST have an approved
STORYBOARD_CLEAN_SEQUENCE_BOARD deterministically assembled from the approved
clean panels in exactly CUT order before Stage 05 video generation.
"""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import yaml

APPROVED_ASSET_STATUSES={
    'APPROVED','APPROVED_SUPPORT','APPROVED_ASSEMBLY','APPROVED_SCOPED_FIGURE','APPROVED_VIDEO_CONDITIONING'
}
CLEAN_KEYS={
    'visible_text','visible_numbers','arrows_or_motion_lines','timecode',
    'shot_or_panel_labels','cut_or_camera_labels','caption_boxes','subtitle_or_logo'
}
MULTI_MODES={'SEQUENTIAL_MULTISHOT','TIMED_MULTISHOT','FREESTYLE_BROLL'}


def load(p):
    return yaml.safe_load(Path(p).read_text(encoding='utf-8'))


def issue(issues, typ, **kw):
    d={'type':typ}; d.update(kw); issues.append(d)


def is_clean_storyboard(asset, expected_type=None):
    issues=[]
    aid=asset.get('asset_id')
    if expected_type and asset.get('asset_type')!=expected_type:
        issue(issues,'MULTISHOT_STORYBOARD_ASSET_TYPE_MISMATCH',asset_id=aid,expected=expected_type,actual=asset.get('asset_type'))
    if asset.get('storyboard_render_mode')!='WHITE_LINE_STORYBOARD_ONLY':
        issue(issues,'MULTISHOT_STORYBOARD_NOT_WHITE_LINE',asset_id=aid,actual=asset.get('storyboard_render_mode'))
    cl=asset.get('storyboard_cleanliness')
    if not isinstance(cl,dict):
        issue(issues,'MULTISHOT_STORYBOARD_CLEANLINESS_QC_MISSING',asset_id=aid)
    else:
        dirty=sorted(k for k in CLEAN_KEYS if cl.get(k) is True)
        if dirty:
            issue(issues,'MULTISHOT_STORYBOARD_PIXEL_ANNOTATION_FAIL',asset_id=aid,present=dirty)
    vu=asset.get('video_usage') or {}
    if vu.get('primary_visual_eligible') is True:
        issue(issues,'MULTISHOT_STORYBOARD_PRIMARY_VISUAL_FORBIDDEN',asset_id=aid)
    return issues


def lint(envelope, registry=None, editorial=None, execution_plan=None, job=None):
    issues=[]; warnings=[]
    mode=envelope.get('format_mode')
    shot_ids=envelope.get('shot_ids') or []
    cuts=envelope.get('cut_contracts') or []
    grid=envelope.get('storyboard_grid') or {}
    multi=(mode!='ONER' or len(shot_ids)>1 or len(cuts)>1)

    if mode=='ONER' and (len(shot_ids)!=1 or len(cuts)!=1):
        issue(issues,'GENERATION_ENVELOPE_FORMAT_CONFLICT',format_mode=mode,shot_count=len(shot_ids),cut_count=len(cuts))
    if mode in MULTI_MODES and (len(shot_ids)<2 or len(cuts)<2):
        issue(issues,'GENERATION_ENVELOPE_FORMAT_CONFLICT',format_mode=mode,shot_count=len(shot_ids),cut_count=len(cuts))
    if len(set(shot_ids))!=len(shot_ids):
        issue(issues,'GENERATION_ENVELOPE_SHOT_SET_CONFLICT',reason='duplicate_shot_ids')

    orders=[]; cut_ids=[]; cut_shots=[]; panel_ids=[]
    for c in cuts:
        cid=c.get('cut_id'); order=c.get('order'); sid=c.get('shot_id'); panel=c.get('storyboard_panel_asset_id')
        if not cid or order is None or not sid:
            issue(issues,'CUT_CONTRACT_GAP',cut_id=cid,shot_id=sid)
        if cid in cut_ids:
            issue(issues,'CUT_ORDER_CONFLICT',reason='duplicate_cut_id',cut_id=cid)
        cut_ids.append(cid); orders.append(order); cut_shots.append(sid); panel_ids.append(panel)
        for req in ('narrative_function','viewpoint_role','camera_character','camera_start','camera_path','camera_end','action_beat','performance_beat','cut_in_trigger','cut_out_trigger','continuity_handoff','storyboard_panel_asset_id'):
            if c.get(req) in (None,''):
                issue(issues,'CUT_CONTRACT_GAP',cut_id=cid,field=req)
    if orders and sorted(orders)!=list(range(1,len(cuts)+1)):
        issue(issues,'CUT_ORDER_CONFLICT',orders=orders,expected=list(range(1,len(cuts)+1)))
    ordered_cuts=sorted(cuts,key=lambda x:x.get('order',10**9))
    ordered_shots=[c.get('shot_id') for c in ordered_cuts]
    ordered_panels=[c.get('storyboard_panel_asset_id') for c in ordered_cuts]
    if ordered_shots and ordered_shots!=shot_ids:
        issue(issues,'GENERATION_ENVELOPE_SHOT_SET_CONFLICT',reason='shot_ids_not_cut_order',shot_ids=shot_ids,cut_order=ordered_shots)

    if editorial:
        e_shots=set(editorial.get('shot_order') or [])
        unknown=[s for s in shot_ids if s not in e_shots]
        if unknown: issue(issues,'GENERATION_ENVELOPE_EDITORIAL_SHOT_UNKNOWN',shot_ids=unknown)
        if mode!='ONER' and editorial.get('editing_mode')=='ASSEMBLY_FIRST':
            issue(issues,'MULTISHOT_NOT_AUTHORIZED_BY_EDITORIAL_PLAN',editing_mode=editorial.get('editing_mode'))

    if multi:
        if grid.get('required') is not True:
            issue(issues,'MULTISHOT_STORYBOARD_GRID_MISSING',reason='grid_not_required')
        if grid.get('qc_status')!='PASS':
            issue(issues,'MULTISHOT_STORYBOARD_GRID_QC_FAIL',qc_status=grid.get('qc_status'))
        board_id=grid.get('sequence_board_asset_id')
        board_fp=grid.get('sequence_board_fingerprint')
        if not board_id or not board_fp:
            issue(issues,'MULTISHOT_STORYBOARD_GRID_MISSING',reason='board_id_or_fingerprint_missing')
        if grid.get('assembly_tool')!='tools/storyboard_grid_assembler.py':
            issue(issues,'MULTISHOT_STORYBOARD_GRID_ASSEMBLER_MISMATCH',actual=grid.get('assembly_tool'))
        if grid.get('panel_asset_ids')!=ordered_panels:
            issue(issues,'MULTISHOT_STORYBOARD_GRID_ORDER_MISMATCH',grid_panels=grid.get('panel_asset_ids') or [],cut_panels=ordered_panels)
    else:
        if grid.get('required') is not False or grid.get('qc_status')!='NOT_REQUIRED':
            issue(issues,'ONER_STORYBOARD_GRID_POLICY_CONFLICT',required=grid.get('required'),qc_status=grid.get('qc_status'))

    assets={}
    if registry:
        assets={a.get('asset_id'):a for a in (registry.get('assets') or []) if a.get('asset_id')}
        for c in ordered_cuts:
            sid=c.get('shot_id'); pid=c.get('storyboard_panel_asset_id'); panel=assets.get(pid)
            if not panel:
                issue(issues,'MULTISHOT_STORYBOARD_PANEL_GAP' if multi else 'STORYBOARD_PANEL_GAP',cut_id=c.get('cut_id'),shot_id=sid,asset_id=pid)
                continue
            issues.extend(is_clean_storyboard(panel,'STORYBOARD_CLEAN_PANEL'))
            if panel.get('shot_id')!=sid:
                issue(issues,'MULTISHOT_STORYBOARD_PANEL_SHOT_MISMATCH',cut_id=c.get('cut_id'),shot_id=sid,asset_id=pid,asset_shot_id=panel.get('shot_id'))
            if panel.get('status') not in APPROVED_ASSET_STATUSES:
                issue(issues,'MULTISHOT_STORYBOARD_PANEL_NOT_APPROVED' if multi else 'STORYBOARD_PANEL_NOT_APPROVED',asset_id=pid,status=panel.get('status'))
        if multi:
            bid=grid.get('sequence_board_asset_id'); board=assets.get(bid)
            if not board:
                issue(issues,'MULTISHOT_STORYBOARD_GRID_MISSING',asset_id=bid)
            else:
                issues.extend(is_clean_storyboard(board,'STORYBOARD_CLEAN_SEQUENCE_BOARD'))
                if board.get('layout_type')!='MULTI_PANEL':
                    issue(issues,'MULTISHOT_STORYBOARD_GRID_LAYOUT_FAIL',asset_id=bid,layout_type=board.get('layout_type'))
                if board.get('status') not in APPROVED_ASSET_STATUSES:
                    issue(issues,'MULTISHOT_STORYBOARD_GRID_NOT_APPROVED',asset_id=bid,status=board.get('status'))
                if board.get('fingerprint')!=grid.get('sequence_board_fingerprint'):
                    issue(issues,'MULTISHOT_STORYBOARD_GRID_FINGERPRINT_MISMATCH',asset_id=bid,asset_fingerprint=board.get('fingerprint'),envelope_fingerprint=grid.get('sequence_board_fingerprint'))
                ga=board.get('storyboard_grid_assembly') or {}
                if ga.get('assembler_tool')!='tools/storyboard_grid_assembler.py':
                    issue(issues,'MULTISHOT_STORYBOARD_GRID_ASSEMBLER_MISMATCH',asset_id=bid,actual=ga.get('assembler_tool'))
                if ga.get('source_panel_asset_ids_ordered')!=ordered_panels:
                    issue(issues,'MULTISHOT_STORYBOARD_GRID_ORDER_MISMATCH',asset_id=bid,board_panels=ga.get('source_panel_asset_ids_ordered') or [],cut_panels=ordered_panels)

    if mode=='TIMED_MULTISHOT':
        total=envelope.get('total_duration_sec')
        prev=0.0
        for c in ordered_cuts:
            s=c.get('start_sec'); e=c.get('end_sec')
            if s is None or e is None or not isinstance(s,(int,float)) or not isinstance(e,(int,float)):
                issue(issues,'MULTISHOT_TIMING_BUDGET_FAIL',cut_id=c.get('cut_id'),reason='timing_missing')
                continue
            if e<=s: issue(issues,'MULTISHOT_TIMING_BUDGET_FAIL',cut_id=c.get('cut_id'),reason='end_not_after_start',start=s,end=e)
            if abs(float(s)-prev)>0.05: issue(issues,'MULTISHOT_TIMING_BUDGET_FAIL',cut_id=c.get('cut_id'),reason='gap_or_overlap',expected_start=prev,actual_start=s)
            prev=float(e)
        if not isinstance(total,(int,float)) or abs(prev-float(total or 0))>0.05:
            issue(issues,'MULTISHOT_TIMING_BUDGET_FAIL',reason='total_not_closed',last_end=prev,total_duration_sec=total)

    # A multishot should change more than crop size; warn when consecutive camera character + viewpoint repeat with no information delta.
    for a,b in zip(ordered_cuts,ordered_cuts[1:]):
        same_view=a.get('viewpoint_role')==b.get('viewpoint_role')
        same_char=a.get('camera_character')==b.get('camera_character')
        no_info=not b.get('information_revealed') or b.get('information_revealed')==a.get('information_revealed')
        if same_view and same_char and no_info:
            warnings.append({'type':'PSEUDO_MULTISHOT_STAGNATION_RISK','from_cut':a.get('cut_id'),'to_cut':b.get('cut_id')})

    if execution_plan:
        if execution_plan.get('generation_envelope_id')!=envelope.get('generation_envelope_id'):
            issue(issues,'VIDEO_EXECUTION_PLAN_ENVELOPE_MISMATCH',plan=envelope.get('generation_envelope_id'),actual=execution_plan.get('generation_envelope_id'))
        if execution_plan.get('format_mode')!=mode:
            issue(issues,'VIDEO_EXECUTION_PLAN_FORMAT_MISMATCH',expected=mode,actual=execution_plan.get('format_mode'))
        ep=execution_plan.get('source_fingerprints') or {}
        ef=envelope.get('generation_envelope_fingerprint')
        if ef and ep.get('generation_envelope')!=ef:
            issue(issues,'VIDEO_EXECUTION_PLAN_ENVELOPE_FINGERPRINT_MISMATCH',expected=ef,actual=ep.get('generation_envelope'))
        hand=execution_plan.get('storyboard_handoff') or {}
        if multi and hand.get('generation_envelope_storyboard_grid_asset_id')!=grid.get('sequence_board_asset_id'):
            issue(issues,'VIDEO_EXECUTION_PLAN_STORYBOARD_GRID_MISMATCH',expected=grid.get('sequence_board_asset_id'),actual=hand.get('generation_envelope_storyboard_grid_asset_id'))

    if job:
        if job.get('media_kind')!='VIDEO': issue(issues,'GENERATION_ENVELOPE_JOB_MEDIA_KIND_MISMATCH',actual=job.get('media_kind'))
        if job.get('generation_envelope_id')!=envelope.get('generation_envelope_id'):
            issue(issues,'VIDEO_JOB_ENVELOPE_MISMATCH',expected=envelope.get('generation_envelope_id'),actual=job.get('generation_envelope_id'))
        if job.get('format_mode')!=mode:
            issue(issues,'VIDEO_JOB_FORMAT_MISMATCH',expected=mode,actual=job.get('format_mode'))

    return {
        'pass':not issues,
        'generation_envelope_id':envelope.get('generation_envelope_id'),
        'format_mode':mode,
        'multishot':multi,
        'shot_count':len(shot_ids),
        'cut_count':len(cuts),
        'issues':issues,
        'warnings':warnings,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--envelope',required=True)
    ap.add_argument('--registry')
    ap.add_argument('--editorial-plan')
    ap.add_argument('--execution-plan')
    ap.add_argument('--job')
    a=ap.parse_args()
    out=lint(load(a.envelope), load(a.registry) if a.registry else None, load(a.editorial_plan) if a.editorial_plan else None, load(a.execution_plan) if a.execution_plan else None, load(a.job) if a.job else None)
    print(json.dumps(out,ensure_ascii=False,indent=2))
    raise SystemExit(0 if out['pass'] else 2)

if __name__=='__main__': main()
