#!/usr/bin/env python3
"""V4.5.11-M1 hybrid architecture audit."""
import argparse,json,re
from pathlib import Path
import yaml

def load(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]); ap.add_argument('--json',action='store_true'); a=ap.parse_args(); root=a.root.resolve(); errors=[]; warnings=[]
    rr=load(root/'controller/route_registry.yaml'); wf=load(root/'controller/workflow_state_machine.yaml'); ar=load(root/'controller/authority_registry.yaml'); mm=load(root/'controller/module_manifest.yaml')
    for name,obj in [('route_registry',rr),('workflow',wf),('authority_registry',ar),('module_manifest',mm)]:
        if obj.get('skill_version')!='4.5.11': errors.append(f'{name}: skill_version must be 4.5.11')
    required_files=['state/generation_job.schema.yaml','runtime/generation_runtime.schema.yaml','templates/generation_execution_spine.md','templates/scene_color_card_auto_derivation.md','adapters/generation/host_profiles.yaml','tools/asset_route_dispatcher.py','tools/scene_color_router.py','tools/generation_job_manager.py','tools/controller_engine.py','tools/runtime_compiler.py','tools/generation_runtime_manager.py','tools/asset_promoter.py','validators/generation_chain_lint.py','validators/scene_color_binding_lint.py','validators/generation_job_binding_lint.py','state/video_execution_plan.schema.yaml','state/video_prompt_artifact.schema.yaml','controller/gate_producer_registry.yaml','tools/video_execution_plan_freezer.py','tools/video_prompt_artifact.py','tools/video_runtime_manager.py','tools/ending_frame_capture.py','tools/video_unit_advance.py','validators/video_execution_plan_fingerprint_lint.py','validators/video_generation_job_prompt_lint.py','validators/gate_producer_lint.py','tools/runtime_freshness_resolver.py','state/runtime_freshness_proof.schema.yaml','validators/video_experience_execution_qc_lint.py','tools/runtime_capsule_sealer.py']
    for rel in required_files:
        if not (root/rel).exists(): errors.append(f'missing {rel}')
    routes=rr.get('routes',{})
    for rn in ['GENERATION_JOB_DISPATCH','GENERATION_JOB_EXECUTOR','SCENE_COLOR_CARD_DERIVATION']:
        if rn not in routes: errors.append(f'missing route {rn}')
    build=routes.get('EPISODE_ASSET_BUILD',{}); subs=set(build.get('callable_subroutes') or [])
    for rn in ['CHARACTER_MASTER','ENVIRONMENT_MASTER_COVERAGE','PROP_MASTER_COVERAGE','TRANSFORMATION_FIRST_DESIGN','TRANSFORMATION_REPEAT','PRODUCTION_SUPPORT_REFERENCE','SHOT_ASSEMBLY_ASSET','SCENE_COLOR_CARD_DERIVATION']:
        if rn not in subs: errors.append(f'EPISODE_ASSET_BUILD cannot dispatch {rn}')
    # Reachability counts normal workflow + callable subroutes; revision/evidence routes may be failure-only.
    reachable={t.get('route') for t in wf.get('transitions',[]) if t.get('route')}
    frontier=list(reachable)
    while frontier:
        cur=frontier.pop()
        for sub in routes.get(cur,{}).get('callable_subroutes',[]) or []:
            if sub not in reachable: reachable.add(sub); frontier.append(sub)
    generation_routes=['CHARACTER_MASTER','ENVIRONMENT_MASTER_COVERAGE','PROP_MASTER_COVERAGE','SHOT_ASSEMBLY_ASSET','TRANSFORMATION_FIRST_DESIGN','TRANSFORMATION_REPEAT','SCENE_COLOR_CARD_DERIVATION']
    for rn in generation_routes:
        if rn not in reachable: errors.append(f'unreachable generation route {rn}')
    fr=load(root/'controller/failure_router.yaml')
    failure_reachable={v.get('route') for v in (fr.get('routes') or {}).values() if isinstance(v,dict) and v.get('route')}
    active_routes={rn for rn,r in routes.items() if not r.get('compatibility_only')}
    orphan=sorted(active_routes-reachable-failure_reachable)
    if orphan: errors.append(f'active routes have no normal/callable/failure path: {orphan}')
    # Transition producer closure for new V4.5.7 gates.
    producers={}
    for rn,r in routes.items():
        for fld in r.get('produces_fields') or []: producers.setdefault(fld,set()).add(rn)
    new_gates={'GENERATION_QUEUE_DRAINED','ASSET_LINEAGE_COMPLETE','SCENE_COLOR_AUTHORITY_COVERAGE_COMPLETE','SHOT_EXECUTION_GENERATION_JOBS_COMPLETE','VIDEO_CONDITIONING_COLOR_BINDING_PASS','VIDEO_COLOR_AUTHORITY_BOUND'}
    required={f for t in wf.get('transitions',[]) for f in (t.get('requires') or [])}
    for g in sorted(new_gates & required):
        if g not in producers: errors.append(f'new gate has no producer: {g}')

    # Workflow initial-state and hot-state domain closure.
    initial_by_mode=wf.get('initial_state_by_mode') or {}
    expected_modes=set((wf.get('modes') or {}).keys())
    if set(initial_by_mode)!=expected_modes: errors.append(f'workflow initial_state_by_mode must cover exactly modes {sorted(expected_modes)}; got {sorted(initial_by_mode)}')
    for mode,st in initial_by_mode.items():
        if st not in (wf.get('states') or {}): errors.append(f'workflow initial state unknown: {mode}:{st}')
    eps=load(root/'state/episode_state.schema.yaml')
    state_enum=set((((eps.get('properties') or {}).get('workflow_state') or {}).get('enum') or []))
    workflow_states=set((wf.get('states') or {}).keys())
    if state_enum!=workflow_states: errors.append(f'episode_state workflow_state enum mismatch missing={sorted(workflow_states-state_enum)} extra={sorted(state_enum-workflow_states)}')

    # REALISM_CONTRACT has one explicit structured owner; plausibility consumes it rather than redefining it.
    rc=ar.get('authorities',{}).get('realism_contract') or {}
    if rc.get('owner')!='templates/everyday_realism_plausibility_gate.md': errors.append('realism_contract owner missing or invalid')
    if rc.get('structured_schema')!='state/realism_contract.schema.yaml': errors.append('realism_contract structured schema not registered')
    if rc.get('deterministic_validator')!='validators/everyday_realism_lint.py': errors.append('realism_contract deterministic validator not registered')
    realism_schema_owners=[k for k,v in (ar.get('authorities') or {}).items() if isinstance(v,dict) and v.get('structured_schema')=='state/realism_contract.schema.yaml']
    if realism_schema_owners!=['realism_contract']: errors.append(f'realism_contract structured owner must be unique; got {realism_schema_owners}')
    plaus=ar.get('authorities',{}).get('everyday_realism_plausibility') or {}
    if plaus.get('consumes_authority')!='realism_contract': errors.append('everyday_realism_plausibility must consume realism_contract authority')

    # Execution closure: every active image generation route gets preflight/result/promotion; Stage 05 video gets dispatch/result capture but never image promotion.
    for rn in ['CHARACTER_MASTER','ENVIRONMENT_MASTER_COVERAGE','PROP_MASTER_COVERAGE','SCENE_COLOR_CARD_DERIVATION','PRODUCTION_SUPPORT_REFERENCE','SHOT_ASSEMBLY_ASSET','TRANSFORMATION_FIRST_DESIGN','TRANSFORMATION_REPEAT','STAGE_04_STORYBOARD','STAGE_04_VIDEO_CONDITIONING_BUILD','REVISION_IMAGE']:
        r=routes.get(rn,{})
        if 'validators/generation_job_binding_lint.py' not in (r.get('validators') or []): errors.append(f'{rn} missing generation preflight')
        if not r.get('result_capture_tool'): errors.append(f'{rn} missing result capture')
        if not r.get('asset_promotion_tool'): errors.append(f'{rn} missing image asset promotion')
    v=routes.get('STAGE_05_VIDEO',{})
    if not {'GENERATION_JOB_DISPATCH','GENERATION_JOB_EXECUTOR'}.issubset(set(v.get('callable_subroutes') or [])): errors.append('STAGE_05_VIDEO generation subroutes incomplete')
    if not v.get('result_capture_tool'): errors.append('STAGE_05_VIDEO result capture missing')
    if v.get('asset_promotion_tool'): errors.append('STAGE_05_VIDEO must not use image asset promotion')
    if not routes.get('PRODUCTION_SUPPORT_REFERENCE',{}).get('execute_with'): errors.append('PRODUCTION_SUPPORT_REFERENCE has no execution surface')

    # V4.5.11-M1 anti-shortcut closure: FRESH must be proof-derived and actual Video Take must pass experience/creature execution QC.
    planner=(root/'tools/context_load_planner.py').read_text(encoding='utf-8')
    if "choices=['AUTO','MISSING','STALE','INCOMPLETE']" not in planner: errors.append('Context Planner may still allow caller-declared FRESH')
    if 'FRESH_RUNTIME_REQUIRES_VERIFIED_PROOF' not in planner: errors.append('Context Planner missing verified freshness proof gate')
    vq=routes.get('STAGE_05_VIDEO_QC',{})
    exp_validator='validators/video_experience_execution_qc_lint.py'
    if exp_validator not in (vq.get('validators') or []): errors.append('STAGE_05_VIDEO_QC missing actual-take experience validator')
    for fld in ['VIDEO_EXPERIENCE_EXECUTION_QC_PASS','VIDEO_CREATURE_PERFORMANCE_QC_PASS']:
        if fld not in set(vq.get('produces_fields') or []): errors.append(f'STAGE_05_VIDEO_QC missing {fld} producer')
    t25=next((x for x in wf.get('transitions',[]) if x.get('id')=='T25_VIDEO_QC'),{})
    for fld in ['VIDEO_EXPERIENCE_EXECUTION_QC_PASS','VIDEO_CREATURE_PERFORMANCE_QC_PASS']:
        if fld not in set(t25.get('requires') or []): errors.append(f'T25 missing actual-take hard gate {fld}')

    # Full Stage 04/05 gate-producer closure.
    gpr=load(root/'controller/gate_producer_registry.yaml'); gate_producers=gpr.get('producers') or {}; states=wf.get('states') or {}
    for tr in wf.get('transitions',[]):
        srcs=tr.get('from_any') or ([tr.get('from')] if tr.get('from') else [])
        relevant=False
        for stname in srcs+[tr.get('to')]:
            stage=str((states.get(stname) or {}).get('stage',''))
            if stage.startswith('04') or stage=='05': relevant=True
        if not relevant: continue
        req=list(tr.get('requires') or [])
        for xs in (tr.get('conditional_requires') or {}).values(): req.extend(xs or [])
        for fld in req:
            if fld not in gate_producers: errors.append(f'Stage04/05 gate has no explicit producer: {tr.get("id")}:{fld}')
    # Storyboard must be a real image generation route, not a prompt-only route.
    sb=routes.get('STAGE_04_STORYBOARD',{})
    if not {'GENERATION_JOB_DISPATCH','GENERATION_JOB_EXECUTOR'}.issubset(set(sb.get('callable_subroutes') or [])): errors.append('STAGE_04_STORYBOARD generation subroutes incomplete')
    if not sb.get('result_capture_tool') or not sb.get('asset_promotion_tool'): errors.append('STAGE_04_STORYBOARD real generation/promotion closure missing')
    # Video must bind a frozen plan and persisted prompt artifact before generation.
    for fld in ['VIDEO_EXECUTION_PLAN_FINGERPRINT_CURRENT','FINAL_VIDEO_PROMPT_VALID','VIDEO_GENERATION_JOB_PROMPT_BOUND']:
        tr=next((x for x in wf.get('transitions',[]) if x.get('id')=='T23B_VIDEO_READY'),{})
        if fld not in (tr.get('requires') or []): errors.append(f'T23B missing {fld}')
    # Approved video must pass ending-frame continuity before Post, with a next-unit loop.
    post=next((x for x in wf.get('transitions',[]) if x.get('id')=='T28_POST'),{})
    if post.get('from')!='ENDING_FRAME_APPROVED': errors.append('POST may bypass ending-frame continuity')
    if not {'REQUIRED_SEGMENTS_APPROVED','NO_REMAINING_VIDEO_UNITS'}.issubset(set(post.get('requires') or [])): errors.append('POST completion gates incomplete')
    adv=next((x for x in wf.get('transitions',[]) if x.get('id')=='T27B_ADVANCE_VIDEO_UNIT'),{})
    if adv.get('to')!='STORYBOARD_IN_PROGRESS' or adv.get('route')!='ADVANCE_VIDEO_UNIT': errors.append('next Video Unit loop missing')

    # Legacy production names may remain only in compatibility/migration docs, never active templates.
    legacy_terms=['HD_SHOT_ANCHOR','HD_SHOT_SUPPORT_ANCHOR','HD_SHOT_ANCHOR_PLAN','EVENT_NODE_VIEW','RECIPROCAL_COVERAGE_VIEW','PREDICTIVE_COVERAGE_VIEW','SCENE_CLUE_VIEW','LOCATION_VISIBILITY_VIEW','LOCATION_IDENTITY_VIEW','DERIVED_COVERAGE_VIEW']
    for tp in (root/'templates').glob('*.md'):
        text=tp.read_text(encoding='utf-8')
        for term in legacy_terms:
            if term in text: errors.append(f'active legacy term {term} remains in {tp.relative_to(root)}')

    # Readable scoped/minor-human Base Appearance Authority must never regress to Assembly/Previs ownership.
    forbidden_scoped_appearance_patterns={
      r'SHOT_ASSEMBLY_ASSET.*SCOPED_CHARACTER_APPEARANCE_AUTHORITY':'Assembly claims scoped appearance authority',
      r'FMH_NURSE_A\s+or\s+ASM_HOSPITAL_DELIVERY':'coverage map allows Assembly as scoped appearance substitute',
      r'FMH\s*/\s*Assembly\s*/\s*Approved Previs Human Anchor':'FMH/Assembly/Previs are treated as interchangeable visual owners',
      r'Assembly[^\n]{0,80}只有授权`SCOPED_CAST`例外':'Assembly identity/appearance exception remains for scoped cast',
      r'Identity/Human Appearance\s*→\s*[^；\n]*(?:Shot Assembly|Previs Human Anchor)':'Assembly/Previs listed as human appearance owner',
      r'(?:Assembly|PREVIS_HUMAN_ANCHOR|Previs Human Anchor)[^\n]{0,100}唯一Appearance Owner':'ambiguous unique-only appearance-owner ban leaves shared ownership open',
      r'Assembly/Previs[^\n]{0,80}唯一人物Appearance Authority':'ambiguous unique-only appearance-authority ban leaves shared ownership open',
    }
    for tp in (root/'templates').glob('*.md'):
        text=tp.read_text(encoding='utf-8')
        for pat,why in forbidden_scoped_appearance_patterns.items():
            if re.search(pat,text,re.I): errors.append(f'forbidden scoped appearance ownership regression in {tp.relative_to(root)}: {why}')

    # Module manifest closure
    manifest=[mod for b in (mm.get('classes') or {}).values() for mod in (b.get('modules') or [])]
    actual=[p.name for p in (root/'templates').glob('*.md')]
    if set(actual)!=set(manifest):
        errors.append(f'module_manifest mismatch missing={sorted(set(actual)-set(manifest))} extra={sorted(set(manifest)-set(actual))}')
    # Text invariants
    checks={
      'templates/generation_execution_spine.md':['Generation Job','Candidate Capture','Shot Execution Frame','Color Authority'],
      'templates/scene_color_card_auto_derivation.md':['自动触发','SCENE_COLOR_FROM_BASE','LINEAGE_ONLY','@对应场景色卡'],
      'templates/video_conditioning_asset_architecture.md':['Master Lineage + Scene Color Continuity','Scene Color'],
      'templates/color_script_derivation_engine.md':['Scene Color','自动派生'],
    }
    for rel,toks in checks.items():
        text=(root/rel).read_text(encoding='utf-8')
        for tok in toks:
            if tok.lower() not in text.lower(): errors.append(f'{rel} missing token {tok}')
    out={'errors':errors,'warnings':warnings,'route_count':len(routes),'reachable_route_count':len(reachable),'failure_reachable_route_count':len(failure_reachable),'new_gate_count':len(new_gates)}
    print(json.dumps(out,ensure_ascii=False,indent=2) if a.json else out); return 1 if errors else 0
if __name__=='__main__': raise SystemExit(main())
