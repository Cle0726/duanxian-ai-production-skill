#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]

def load_path(p):
    p=Path(p); txt=p.read_text(encoding='utf-8')
    return json.loads(txt) if p.suffix.lower()=='.json' else yaml.safe_load(txt)

def canonical_fp(d):
    x=dict(d); x.pop('plan_fingerprint',None)
    return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def lint(d):
    issues=[]
    def add(t,**kw): issues.append({'type':t,**kw})
    schema=yaml.safe_load((ROOT/'state/context_load_plan.schema.yaml').read_text(encoding='utf-8'))
    for e in Draft202012Validator(schema).iter_errors(d): add('CONTEXT_LOAD_PLAN_SCHEMA_FAIL',path=list(e.path),message=e.message)
    rr=yaml.safe_load((ROOT/'controller/route_registry.yaml').read_text(encoding='utf-8'))
    policy=yaml.safe_load((ROOT/'controller/context_loading_policy.yaml').read_text(encoding='utf-8'))
    modreg=yaml.safe_load((ROOT/'controller/context_module_registry.yaml').read_text(encoding='utf-8'))
    known_packs=set((modreg.get('packs') or {}).keys())
    unknown_packs=sorted(set(d.get('active_module_packs') or [])-known_packs)
    if unknown_packs: add('CONTEXT_MODULE_PACK_UNKNOWN',packs=unknown_packs)
    rid=d.get('route_id'); route=(rr.get('routes') or {}).get(rid)
    if not route: add('CONTEXT_ROUTE_UNKNOWN',route_id=rid); return {'pass':False,'issues':issues}
    for group in ['kernel_files','creative_context_files','machine_validation_files','machine_control_plane_files']:
        for rel in d.get(group) or []:
            if not (ROOT/rel).exists(): add('CONTEXT_REFERENCED_FILE_MISSING',group=group,path=rel)
    controls=set(policy.get('machine_control_plane_files') or [])
    bad=sorted(controls & set(d.get('creative_context_files') or []))
    if bad: add('MACHINE_CONTROL_PLANE_IN_CREATIVE_CONTEXT',paths=bad)
    if d.get('runtime_state')=='FRESH' and d.get('source_fallback_loaded') is not False:
        add('FRESH_RUNTIME_FALLBACK_SOURCE_CONFLICT')
    if d.get('runtime_state')!='FRESH' and d.get('source_fallback_loaded') is not True:
        add('STALE_RUNTIME_FALLBACK_SOURCE_GAP')
    proof=d.get('runtime_freshness_proof')
    if d.get('runtime_state')=='FRESH':
        if not isinstance(proof,dict):
            add('FRESH_RUNTIME_PROOF_MISSING')
        else:
            pschema=yaml.safe_load((ROOT/'state/runtime_freshness_proof.schema.yaml').read_text(encoding='utf-8'))
            for e in Draft202012Validator(pschema).iter_errors(proof): add('FRESH_RUNTIME_PROOF_SCHEMA_FAIL',path=list(e.path),message=e.message)
            px=dict(proof); pfp=px.pop('proof_fingerprint',None)
            expected_pfp=hashlib.sha256(json.dumps(px,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
            if pfp!=expected_pfp: add('FRESH_RUNTIME_PROOF_FINGERPRINT_MISMATCH')
            if proof.get('route_id')!=rid: add('FRESH_RUNTIME_PROOF_ROUTE_MISMATCH')
            if proof.get('resolved_runtime_state')!='FRESH': add('FRESH_RUNTIME_PROOF_STATE_MISMATCH')
            expected=set(route.get('runtime') or [])
            observed={e.get('runtime_type') for e in proof.get('runtime_evidence') or [] if e.get('fresh') is True}
            if expected-observed: add('FRESH_RUNTIME_PROOF_COVERAGE_GAP',runtime_types=sorted(expected-observed))
            bad=[e.get('runtime_type') for e in proof.get('runtime_evidence') or [] if e.get('fresh') is not True]
            if bad: add('FRESH_RUNTIME_PROOF_HAS_FAILURES',runtime_types=bad)
    cond=route.get('conditional_source') or {}; matched=set(d.get('matched_conditional_domains') or [])
    creative=set(d.get('creative_context_files') or [])
    for dom,files in cond.items():
        if dom in matched:
            miss=[f for f in files or [] if f not in creative]
            if miss: add('ACTIVE_CONDITIONAL_AUTHORITY_MISSING',domain=dom,paths=miss)
        else:
            # If a file is also required by an unconditional route field, it is legitimate.
            unconditional=set((route.get('source') or [])+(route.get('execute_with') or []))
            if d.get('runtime_state')!='FRESH': unconditional |= set((route.get('source_if_missing_or_stale') or [])+(route.get('compile_runtime_from_source') or []))
            leaked=[f for f in files or [] if f in creative and f not in unconditional]
            if leaked: add('INACTIVE_CONDITIONAL_AUTHORITY_LEAK',domain=dom,paths=leaked)
    if canonical_fp(d)!=d.get('plan_fingerprint'): add('CONTEXT_LOAD_PLAN_FINGERPRINT_MISMATCH')
    return {'pass':not issues,'issues':issues,'route_id':rid,'creative_file_count':len(creative)}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('plan'); a=ap.parse_args()
    out=lint(load_path(a.plan)); print(json.dumps(out,ensure_ascii=False,indent=2)); return 0 if out['pass'] else 2
if __name__=='__main__': raise SystemExit(main())
