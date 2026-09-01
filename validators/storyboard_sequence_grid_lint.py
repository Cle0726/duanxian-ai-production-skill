#!/usr/bin/env python3
"""Hard gate: every sequence with 2+ formal shots must have a clean white-line grid."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

CLEAN_KEYS={'visible_text','visible_numbers','arrows_or_motion_lines','timecode','shot_or_panel_labels','cut_or_camera_labels','caption_boxes','subtitle_or_logo'}
QC_OK={'DRAFT','QC_PASS_WAITING_APPROVAL','APPROVED','APPROVED_SUPPORT','APPROVED_ASSEMBLY'}
APPROVED={'APPROVED','APPROVED_SUPPORT','APPROVED_ASSEMBLY'}

def load(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))
def add(issues,t,**kw): d={'type':t}; d.update(kw); issues.append(d)

def clean(asset,issues):
    aid=asset.get('asset_id')
    if asset.get('storyboard_render_mode')!='WHITE_LINE_STORYBOARD_ONLY': add(issues,'SEQUENCE_STORYBOARD_NOT_WHITE_LINE',asset_id=aid)
    cl=asset.get('storyboard_cleanliness')
    if not isinstance(cl,dict): add(issues,'SEQUENCE_STORYBOARD_CLEANLINESS_QC_MISSING',asset_id=aid)
    else:
        dirty=sorted(k for k in CLEAN_KEYS if cl.get(k) is True)
        if dirty: add(issues,'SEQUENCE_STORYBOARD_PIXEL_ANNOTATION_FAIL',asset_id=aid,present=dirty)
    if (asset.get('video_usage') or {}).get('primary_visual_eligible') is True: add(issues,'SEQUENCE_STORYBOARD_PRIMARY_VISUAL_FORBIDDEN',asset_id=aid)

def lint(editorial,registry,proof=None,phase='qc'):
    issues=[]; shot_order=editorial.get('shot_order') or []
    if len(shot_order)<=1:
        return {'pass':True,'required':False,'phase':phase,'shot_count':len(shot_order),'issues':[]}
    if not proof:
        add(issues,'MULTISHOT_SEQUENCE_STORYBOARD_GRID_MISSING',reason='proof_missing')
        return {'pass':False,'required':True,'phase':phase,'shot_count':len(shot_order),'issues':issues}
    if proof.get('sequence_id')!=editorial.get('sequence_id'): add(issues,'SEQUENCE_STORYBOARD_PROOF_SEQUENCE_MISMATCH')
    if proof.get('shot_order')!=shot_order: add(issues,'SEQUENCE_STORYBOARD_SHOT_ORDER_MISMATCH',expected=shot_order,actual=proof.get('shot_order'))
    panel_order=proof.get('panel_order') or []
    covered=[]
    for x in panel_order:
        sid=x.get('shot_id')
        if sid not in shot_order: add(issues,'SEQUENCE_STORYBOARD_UNKNOWN_SHOT',shot_id=sid)
        elif sid not in covered: covered.append(sid)
    missing=[s for s in shot_order if s not in covered]
    if missing: add(issues,'SEQUENCE_STORYBOARD_SHOT_COVERAGE_GAP',shot_ids=missing)
    # First appearance of each shot must follow formal shot order. Extra panels may follow within their shot block.
    if covered!=shot_order: add(issues,'SEQUENCE_STORYBOARD_PANEL_SHOT_ORDER_MISMATCH',expected=shot_order,actual=covered)
    assets={a.get('asset_id'):a for a in (registry.get('assets') or []) if a.get('asset_id')}
    panel_ids=[]
    for x in panel_order:
        sid=x.get('shot_id'); pid=x.get('panel_asset_id'); panel_ids.append(pid)
        a=assets.get(pid)
        if not a: add(issues,'SEQUENCE_STORYBOARD_PANEL_MISSING',shot_id=sid,asset_id=pid); continue
        if a.get('asset_type')!='STORYBOARD_CLEAN_PANEL': add(issues,'SEQUENCE_STORYBOARD_PANEL_TYPE_FAIL',asset_id=pid,actual=a.get('asset_type'))
        if a.get('shot_id')!=sid: add(issues,'SEQUENCE_STORYBOARD_PANEL_SHOT_MISMATCH',asset_id=pid,expected=sid,actual=a.get('shot_id'))
        clean(a,issues)
        allowed=APPROVED if phase=='approved' else QC_OK
        if a.get('status') not in allowed: add(issues,'SEQUENCE_STORYBOARD_PANEL_STATUS_FAIL',asset_id=pid,status=a.get('status'),phase=phase)
    bid=proof.get('sequence_board_asset_id'); board=assets.get(bid)
    if not board: add(issues,'MULTISHOT_SEQUENCE_STORYBOARD_GRID_MISSING',asset_id=bid)
    else:
        if board.get('asset_type')!='STORYBOARD_CLEAN_SEQUENCE_BOARD': add(issues,'SEQUENCE_STORYBOARD_GRID_TYPE_FAIL',asset_id=bid,actual=board.get('asset_type'))
        if board.get('layout_type')!='MULTI_PANEL': add(issues,'SEQUENCE_STORYBOARD_GRID_LAYOUT_FAIL',asset_id=bid,actual=board.get('layout_type'))
        clean(board,issues)
        allowed=APPROVED if phase=='approved' else QC_OK
        if board.get('status') not in allowed: add(issues,'SEQUENCE_STORYBOARD_GRID_STATUS_FAIL',asset_id=bid,status=board.get('status'),phase=phase)
        if board.get('fingerprint')!=proof.get('sequence_board_fingerprint'): add(issues,'SEQUENCE_STORYBOARD_GRID_FINGERPRINT_MISMATCH',asset_id=bid)
        ga=board.get('storyboard_grid_assembly') or {}
        if ga.get('assembler_tool')!='tools/storyboard_grid_assembler.py' or proof.get('assembly_tool')!='tools/storyboard_grid_assembler.py': add(issues,'SEQUENCE_STORYBOARD_GRID_ASSEMBLER_MISMATCH',asset_id=bid)
        if ga.get('source_panel_asset_ids_ordered')!=panel_ids: add(issues,'SEQUENCE_STORYBOARD_GRID_PANEL_ORDER_MISMATCH',expected=panel_ids,actual=ga.get('source_panel_asset_ids_ordered') or [])
    if phase=='approved' and proof.get('status')!='APPROVED': add(issues,'SEQUENCE_STORYBOARD_PROOF_NOT_APPROVED',status=proof.get('status'))
    if phase=='qc' and proof.get('status') not in {'QC_PASS_WAITING_APPROVAL','APPROVED'}: add(issues,'SEQUENCE_STORYBOARD_PROOF_NOT_QC_READY',status=proof.get('status'))
    return {'pass':not issues,'required':True,'phase':phase,'shot_count':len(shot_order),'panel_count':len(panel_order),'issues':issues}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--editorial-plan',required=True); ap.add_argument('--registry',required=True); ap.add_argument('--proof'); ap.add_argument('--phase',choices=['qc','approved'],default='qc'); a=ap.parse_args()
    out=lint(load(a.editorial_plan),load(a.registry),load(a.proof) if a.proof else None,a.phase); print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
