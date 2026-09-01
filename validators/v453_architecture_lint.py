#!/usr/bin/env python3
"""Validate V4.5.3 Visual Evidence Handoff / Text-only Continuation architecture."""
from __future__ import annotations
import argparse,json
from pathlib import Path
import yaml

def load(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]); ap.add_argument('--json',action='store_true'); a=ap.parse_args(); root=a.root.resolve(); errors=[]
    rr=load(root/'controller/route_registry.yaml'); wf=load(root/'controller/workflow_state_machine.yaml'); ar=load(root/'controller/authority_registry.yaml')
    for name,obj in [('route_registry',rr),('workflow',wf),('authority_registry',ar)]:
        if obj.get('skill_version') not in {'4.5.3','4.5.4','4.5.5','4.5.6','4.5.7','4.5.8','4.5.9','4.5.10','4.5.11'}: errors.append(f'{name} unsupported skill_version {obj.get("skill_version")}')
    if 'VISUAL_EVIDENCE_RUNTIME' not in (rr.get('runtime_types') or []): errors.append('runtime type VISUAL_EVIDENCE_RUNTIME missing')
    if 'VISUAL_EVIDENCE' not in (rr.get('structured_artifacts') or {}): errors.append('structured artifact VISUAL_EVIDENCE missing')
    if 'VISUAL_EVIDENCE_CAPTURE' not in (rr.get('routes') or {}): errors.append('VISUAL_EVIDENCE_CAPTURE route missing')
    auth=ar.get('authorities') or {}
    for k in ['visual_evidence_observation','text_only_visual_handoff','reference_visual_evidence_gate']:
        if k not in auth: errors.append(f'missing authority {k}')
    for rel in ['state/visual_evidence.schema.yaml','runtime/visual_evidence_runtime.schema.yaml','templates/visual_evidence_handoff.md','validators/visual_evidence_lint.py']:
        if not (root/rel).exists(): errors.append(f'missing {rel}')
    reg=load(root/'state/asset_registry.schema.yaml'); aprops=reg['properties']['assets']['items']['properties']
    for f in ['visual_evidence_ref','visual_evidence_status','visual_evidence_source_fingerprint','visual_fact_codes','visual_issue_codes']:
        if f not in aprops: errors.append(f'asset registry missing {f}')
    ep=load(root/'state/episode_state.schema.yaml')['properties']
    for f in ['controller_capability','visual_review_queue','visual_evidence_ref']:
        if f not in ep: errors.append(f'episode state missing {f}')
    ref=load(root/'runtime/reference_runtime.schema.yaml')['properties']
    for f in ['controller_mode','required_visual_facts','forbidden_visual_facts','visual_evidence_coverage']:
        if f not in ref: errors.append(f'reference runtime missing {f}')
    t23=next((t for t in wf.get('transitions',[]) if t.get('id')=='T23B_VIDEO_READY'),{})
    if 'REFERENCE_VISUAL_EVIDENCE_PASS' not in ((t23.get('conditional_requires') or {}).get('TEXT_ONLY_CONTINUATION') or []): errors.append('Text-only video readiness evidence condition missing')
    for rn in ['STAGE_04_STORYBOARD','STAGE_04_VIDEO_CONDITIONING_BUILD','STAGE_05_VIDEO','REVISION_IMAGE']:
        r=(rr.get('routes') or {}).get(rn,{})
        if 'VISUAL_EVIDENCE_RUNTIME' not in (r.get('runtime') or []): errors.append(f'{rn}: VISUAL_EVIDENCE_RUNTIME missing')
        inv=r.get('text_only_validator_invocations') or []
        if not any(x.get('validator')=='validators/visual_evidence_lint.py' for x in inv): errors.append(f'{rn}: text-only visual evidence gate missing')
        if inv and 'REFERENCE_RUNTIME' not in (r.get('runtime') or []): errors.append(f'{rn}: text-only evidence gate requires REFERENCE_RUNTIME')
    txt=(root/'templates/visual_evidence_handoff.md').read_text(encoding='utf-8')
    for token in ['TEXT_ONLY_CONTINUATION','禁止创建新的视觉PASS','Prompt描述、文件名、资产ID','source_fingerprint']:
        if token not in txt: errors.append(f'visual evidence policy missing token {token}')
    out={'errors':errors,'route_count':len(rr.get('routes') or {}),'state_count':len(wf.get('states') or {}),'transition_count':len(wf.get('transitions') or [])}
    print(json.dumps(out,ensure_ascii=False,indent=2) if a.json else out); return 1 if errors else 0
if __name__=='__main__': raise SystemExit(main())
