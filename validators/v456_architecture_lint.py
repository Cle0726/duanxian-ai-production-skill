#!/usr/bin/env python3
"""V4.5.6 Logic Integrity architecture audit.

Checks producer/consumer closure for Reality gates, exact failure-code routing,
contract lifecycle hooks, vehicle planning support and Stage 04/05 Reality rechecks.
"""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
import yaml

ROOT_DEFAULT=Path(__file__).resolve().parents[1]

def load(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))

def emitted_codes(path):
    txt=Path(path).read_text(encoding='utf-8')
    codes=set(re.findall(r"(?:'type'\s*:\s*|add\(issues,\s*)['\"]([A-Z][A-Z0-9_]+)['\"]",txt))
    # Dynamic category failures emitted by everyday_realism_lint.
    if Path(path).name=='everyday_realism_lint.py':
        codes.update({c+'_FAIL' for c in ['ENVIRONMENT_FUNCTIONAL_REALISM','ARCHITECTURAL_REALISM','VEHICLE_REALISM','HUMAN_ERGONOMICS','OBJECT_AFFORDANCE','SOCIAL_SPATIAL_PLAUSIBILITY','MUNDANE_PHYSICS','MUNDANE_CONTINUITY']})
    return codes

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',type=Path,default=ROOT_DEFAULT); ap.add_argument('--json',action='store_true')
    a=ap.parse_args(); root=a.root.resolve(); errors=[]
    rr=load(root/'controller/route_registry.yaml'); wf=load(root/'controller/workflow_state_machine.yaml'); ar=load(root/'controller/authority_registry.yaml'); mm=load(root/'controller/module_manifest.yaml'); fr=load(root/'controller/failure_router.yaml')
    for name,obj in [('route_registry',rr),('workflow',wf),('authority_registry',ar),('module_manifest',mm),('failure_router',fr)]:
        if obj.get('skill_version') not in {'4.5.6','4.5.7','4.5.8','4.5.9','4.5.10','4.5.11'}: errors.append(f'{name}: unsupported skill_version {obj.get("skill_version")}')
    for rel in ['validators/everyday_realism_lint.py','validators/video_realism_qc_lint.py','docs/V4.5.6_MIGRATION.md']:
        if not (root/rel).exists(): errors.append(f'missing {rel}')

    # Vehicle diagram false-fail fix + access paths.
    sp=load(root/'state/spatial_canon.schema.yaml'); locp=sp['properties']['locations']['items']['properties']
    if 'access_paths' not in locp: errors.append('SPATIAL_CANON missing locations[].access_paths')
    txt=(root/'validators/spatial_canon_lint.py').read_text(encoding='utf-8')
    if "'VEHICLE':{'VEHICLE_LAYOUT'}" not in txt: errors.append('spatial_canon_lint does not accept VEHICLE_LAYOUT for reusable VEHICLE')

    # Contract lifecycle / basis and asset coverage fields.
    rc=load(root/'state/realism_contract.schema.yaml'); cp=rc['properties']['contracts']['items']['properties']
    if 'QC_PASS_WAITING_APPROVAL' not in cp['status']['enum']: errors.append('REALISM_CONTRACT status lifecycle missing QC_PASS_WAITING_APPROVAL')
    if 'reality_basis' not in cp: errors.append('REALISM_CONTRACT missing reality_basis')
    reg=load(root/'state/asset_registry.schema.yaml'); apx=reg['properties']['assets']['items']['properties']
    for f in ['realism_applicability','realism_applicability_reason','realism_contract_ids','realism_exception_ids']:
        if f not in apx: errors.append(f'ASSET_REGISTRY missing {f}')
    ve=load(root/'state/visual_evidence.schema.yaml'); rp=ve['properties']['records']['items']['properties']['observed']['properties']['realism']['properties']
    envp=rp['environment']['properties']
    for f in ['front_direction_code','driver_forward_visibility','entry_anchor_ids','passenger_count','access_path_ids']:
        if f not in envp: errors.append(f'VISUAL_EVIDENCE realism.environment missing {f}')
    if 'continuity' not in rp: errors.append('VISUAL_EVIDENCE realism missing continuity')

    routes=rr.get('routes') or {}
    stage_specs={
      'STAGE_03_SPATIAL_CANON_QC':('planning','REALISM_CONTRACT_QC_PASS'),
      'EPISODE_ASSET_BUILD':('build','EVERYDAY_REALISM_PRECHECK_PASS'),
      'EPISODE_ASSET_FREEZE':('freeze','EVERYDAY_REALISM_PLAUSIBILITY_PASS'),
      'STAGE_04_STORYBOARD':('storyboard','STORYBOARD_EVERYDAY_REALISM_PASS'),
      'STAGE_04_VIDEO_CONDITIONING_QC':('conditioning','VIDEO_CONDITIONING_EVERYDAY_REALISM_PASS'),
      'STAGE_05_VIDEO':('pre_video','EVERYDAY_REALISM_PRE_VIDEO_PASS'),
    }
    for rn,(phase,field) in stage_specs.items():
        r=routes.get(rn,{})
        if 'validators/everyday_realism_lint.py' not in (r.get('validators') or []): errors.append(f'{rn}: everyday_realism_lint missing')
        inv=[i for i in r.get('validator_invocations') or [] if isinstance(i,dict) and i.get('validator')=='validators/everyday_realism_lint.py' and i.get('phase')==phase]
        if not inv: errors.append(f'{rn}: everyday_realism_lint phase={phase} invocation missing')
        if field not in set(r.get('produces_fields') or []): errors.append(f'{rn}: producer field missing {field}')
    vq=routes.get('STAGE_05_VIDEO_QC',{})
    if 'validators/video_realism_qc_lint.py' not in (vq.get('validators') or []): errors.append('STAGE_05_VIDEO_QC missing video_realism_qc_lint')
    if 'VIDEO_EVERYDAY_REALISM_QC_PASS' not in set(vq.get('produces_fields') or []): errors.append('STAGE_05_VIDEO_QC missing VIDEO_EVERYDAY_REALISM_QC_PASS producer')
    if not any(isinstance(i,dict) and i.get('validator')=='validators/video_realism_qc_lint.py' for i in vq.get('validator_invocations') or []): errors.append('STAGE_05_VIDEO_QC missing video realism validator invocation')

    # New Reality-gate producer/consumer closure.
    producers={}
    for rn,r in routes.items():
        for field in r.get('produces_fields') or []: producers.setdefault(field,set()).add(rn)
    realism_gates=set()
    for t in wf.get('transitions') or []:
        for field in t.get('requires') or []:
            if 'REALISM' in field or field.startswith('REALISM_CONTRACT_'): realism_gates.add(field)
    externally_satisfied={'REALISM_CONTRACT_LOCKED'}  # produced by Spatial QC route after user approval, still must be declared.
    for field in sorted(realism_gates):
        if field not in producers:
            errors.append(f'dead Reality gate with no route producer: {field}')
    if 'REALISM_CONTRACT_AVAILABLE' not in set(routes.get('STAGE_03_SPATIAL_CANON_BUILD',{}).get('produces_fields') or []): errors.append('Spatial Canon Build must produce REALISM_CONTRACT_AVAILABLE')
    if 'REALISM_CONTRACT_LOCKED' not in set(routes.get('STAGE_03_SPATIAL_CANON_QC',{}).get('produces_fields') or []): errors.append('Spatial Canon QC/approval must produce REALISM_CONTRACT_LOCKED')

    # Exact hard failure-code closure: direct route or alias -> canonical route.
    f_routes=fr.get('routes') or {}; aliases=fr.get('code_aliases') or {}
    for rel in ['validators/required_view_realization_lint.py','validators/spatial_canon_lint.py','validators/everyday_realism_lint.py','validators/video_realism_qc_lint.py']:
        for code in sorted(emitted_codes(root/rel)):
            if code in f_routes: continue
            target=aliases.get(code)
            if not target: errors.append(f'unrouted emitted failure code {code} from {rel}')
            elif target not in f_routes: errors.append(f'failure alias {code}->{target} points to missing route')

    # Schema hooks for actual video evidence.
    vr=load(root/'runtime/video_runtime.schema.yaml'); qr=load(root/'runtime/qc_runtime.schema.yaml')
    if 'video_take_fingerprint' not in vr.get('properties',{}): errors.append('VIDEO_RUNTIME missing video_take_fingerprint')
    if 'video_realism_evidence' not in qr.get('properties',{}): errors.append('QC_RUNTIME missing video_realism_evidence')

    # Text authority must say that fine-grained evidence overrides summary and exceptions need real scope.
    checks={
      'SKILL.md':['V4.5.6 Logic Integrity Hard Boundary','Fine-grained Evidence > Summary','Exception ID不是权限'],
      'templates/everyday_realism_plausibility_gate.md':['V4.5.6｜Logic Integrity Closure','Reality Coverage by default','Scoped Exception不可借用','Reality Basis / Provenance'],
      'docs/V4.5.6_MIGRATION.md':['adversarial','realism_applicability','fine-grained']
    }
    for rel,toks in checks.items():
        text=(root/rel).read_text(encoding='utf-8').lower()
        for tok in toks:
            if tok.lower() not in text: errors.append(f'{rel} missing token {tok}')

    out={'errors':errors,'route_count':len(routes),'state_count':len(wf.get('states') or {}),'transition_count':len(wf.get('transitions') or []),'realism_gate_count':len(realism_gates)}
    print(json.dumps(out,ensure_ascii=False,indent=2) if a.json else out)
    return 1 if errors else 0
if __name__=='__main__': raise SystemExit(main())
