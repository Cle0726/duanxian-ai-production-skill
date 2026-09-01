#!/usr/bin/env python3
"""Validate V4.5.1 Spatial Canon + Logic Closure architecture invariants."""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
import yaml

def load(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]); ap.add_argument('--json',action='store_true'); a=ap.parse_args(); root=a.root.resolve(); errors=[]; warnings=[]
    rr=load(root/'controller/route_registry.yaml'); wf=load(root/'controller/workflow_state_machine.yaml'); ar=load(root/'controller/authority_registry.yaml')
    for name,obj in [('route_registry',rr),('workflow',wf),('authority_registry',ar)]:
        if obj.get('skill_version') not in {'4.5.1','4.5.2','4.5.3','4.5.4','4.5.5','4.5.6','4.5.7','4.5.8','4.5.9','4.5.10','4.5.11'}: errors.append(f'{name} unsupported skill_version {obj.get("skill_version")}')
    sa=rr.get('structured_artifacts') or {}
    for key in ['SHOT_RELATION_GRAPH','VISUAL_ASSET_OBLIGATION','SPATIAL_CANON']:
        rel=sa.get(key)
        if not rel or not (root/rel).exists(): errors.append(f'missing structured artifact {key}: {rel}')
    if 'SPATIAL_CANON_RUNTIME' not in (rr.get('runtime_types') or []): errors.append('SPATIAL_CANON_RUNTIME missing from runtime_types')
    routes=rr.get('routes') or {}
    for rn in ['STAGE_03_SPATIAL_CANON_BUILD','STAGE_03_SPATIAL_CANON_QC','EPISODE_ASSET_BUILD','EPISODE_ASSET_FREEZE','STAGE_04_STORYBOARD','STAGE_04_VIDEO_CONDITIONING_BUILD','STAGE_04_VIDEO_CONDITIONING_QC','STAGE_05_VIDEO']:
        if rn not in routes: errors.append(f'missing route {rn}')
    prod=routes.get('STAGE_02C_PRODUCTION_TRANSLATION',{})
    if 'validators/shot_relation_asset_obligation_lint.py' not in (prod.get('validators') or []): errors.append('Stage 02C planning relation validator missing')
    inv=prod.get('validator_invocations') or []
    if not any(x.get('validator')=='validators/shot_relation_asset_obligation_lint.py' and x.get('phase')=='planning' for x in inv): errors.append('Stage 02C explicit planning phase invocation missing')
    for rn in ['EPISODE_ASSET_BUILD','EPISODE_ASSET_FREEZE','STAGE_04_STORYBOARD','STAGE_04_VIDEO_CONDITIONING_BUILD','STAGE_04_VIDEO_CONDITIONING_QC','STAGE_05_VIDEO']:
        si=set(routes.get(rn,{}).get('structured_inputs') or [])
        if 'SPATIAL_CANON' not in si: errors.append(f'{rn}: SPATIAL_CANON structured input missing')
    states=set((wf.get('states') or {}).keys())
    for s in ['SPATIAL_CANON_IN_PROGRESS','SPATIAL_CANON_QC_PASSED_WAITING_APPROVAL','SPATIAL_CANON_LOCKED']:
        if s not in states: errors.append(f'missing workflow state {s}')
    tids={t.get('id'):t for t in (wf.get('transitions') or [])}
    for tid in ['T10_SPATIAL_CANON_BUILD','T10B_SPATIAL_CANON_QC','T10C_SPATIAL_CANON_APPROVE','T10D_ASSET_BUILD']:
        if tid not in tids: errors.append(f'missing transition {tid}')
    if 'RELATION_PLANNING_VALIDATION_PASS' not in set(tids.get('T09_BREAKDOWN_READY',{}).get('requires') or []): errors.append('T09 missing relation planning validation pass')
    t09=set(tids.get('T09_BREAKDOWN_READY',{}).get('requires') or []); t10d=set(tids.get('T10D_ASSET_BUILD',{}).get('requires') or [])
    if 'PROVISIONAL_EPISODE_ASSET_MANIFEST_READY' not in t09: errors.append('T09 must use provisional, not final, asset manifest before Spatial Canon')
    if 'FINAL_EPISODE_ASSET_MANIFEST_READY' in t09: errors.append('T09 incorrectly finalizes asset manifest before Spatial Canon')
    if not {'FINAL_EPISODE_ASSET_MANIFEST_READY','SPATIAL_ASSET_REQUIREMENTS_RECONCILED'} <= t10d: errors.append('T10D must finalize asset manifest after Spatial Canon')
    if any(t.get('from')=='APPROVED_PREVIS_SET' and t.get('to')=='VIDEO_GENERATION_READY' for t in wf.get('transitions') or []): errors.append('direct previs->video bypass exists')
    for auth in ['world_spatial_canon','location_topology_floorplan_sightline','scene_event_node_spatial_binding']:
        if auth not in (ar.get('authorities') or {}): errors.append(f'missing authority {auth}')
    # Current active docs must not retain obsolete workflow states / optional-primary semantics.
    active=list((root/'templates').glob('*.md'))+[root/'SKILL.md',root/'README.md']
    for p in active:
        text=p.read_text(encoding='utf-8')
        if 'WAITING HD SHOT SUPPORT' in text: errors.append(f'legacy state remains: {p.relative_to(root)}')
        if 'HD_SHOT_ANCHOR_REQUIRED' in text: errors.append(f'legacy optional anchor flag remains: {p.relative_to(root)}')
    sanitizer=(root/'templates/model_facing_prompt_surface_sanitizer.md').read_text(encoding='utf-8')
    if '正文可以完全不枚举它们' in sanitizer: errors.append('old UI-only reference omission rule remains in sanitizer')
    sb=(root/'templates/storyboard_prompt_template.md').read_text(encoding='utf-8')
    for token in ['图片像素中禁止出现','tools/storyboard_grid_assembler.py','CLEAN_STORYBOARD_PANEL']:
        if token not in sb: errors.append(f'clean storyboard contract missing token: {token}')
    # No duplicate pycache in distributable source tree.
    caches=list(root.rglob('__pycache__'))+list(root.rglob('*.pyc'))
    if caches: warnings.append(f'python cache artifacts present: {len(caches)} (must be removed before package)')
    out={'errors':errors,'warnings':warnings,'route_count':len(routes),'state_count':len(states),'transition_count':len(wf.get('transitions') or [])}
    print(json.dumps(out,ensure_ascii=False,indent=2) if a.json else out); return 1 if errors else 0
if __name__=='__main__': raise SystemExit(main())
