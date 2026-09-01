#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from runtime_freshness_resolver import resolve as resolve_runtime_freshness, parse_bindings, parse_scope


def load(rel):
    with (ROOT/rel).open(encoding='utf-8') as f: return yaml.safe_load(f)

def uniq(seq):
    out=[]; seen=set()
    for x in seq or []:
        if x and x not in seen:
            seen.add(x); out.append(x)
    return out

def expand_caps(raw, policy):
    aliases=policy.get('capability_aliases') or {}
    out=[]
    for cap in raw:
        k=str(cap).strip()
        if not k: continue
        out.append(k)
        out.extend(aliases.get(k,[]))
    return uniq(out)

def expand_module_dependencies(caps):
    reg=load('controller/context_module_registry.yaml')
    packs=reg.get('packs') or {}
    capset=set(caps); active=set(); expansions=[]
    changed=True
    while changed:
        changed=False
        for pid,item in packs.items():
            triggers=set(item.get('trigger_domains') or [])
            if not (triggers & capset):
                continue
            if pid not in active:
                active.add(pid); changed=True
            for dep in item.get('depends_on') or []:
                ditem=packs.get(dep) or {}
                if dep not in active:
                    active.add(dep); changed=True
                for domain in ditem.get('trigger_domains') or []:
                    if domain not in capset:
                        capset.add(domain); expansions.append(f'{pid}->{dep}:{domain}'); changed=True
    return uniq(list(caps)+sorted(capset-set(caps))), sorted(active), uniq(expansions)

def canonical_fp(d):
    x=dict(d); x.pop('plan_fingerprint',None)
    b=json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
    return hashlib.sha256(b).hexdigest()

def build(route_id, runtime_state, capabilities, freshness_proof=None, allow_compatibility=False):
    rr=load('controller/route_registry.yaml'); policy=load('controller/context_loading_policy.yaml')
    routes=rr.get('routes') or {}
    if route_id not in routes:
        raise ValueError(f'UNKNOWN_ROUTE:{route_id}')
    route=routes[route_id]
    if route.get('compatibility_only') and not allow_compatibility:
        raise ValueError(f'COMPATIBILITY_ROUTE_REQUIRES_MIGRATION_MODE:{route_id}')
    if runtime_state not in (policy.get('runtime_states') or []):
        raise ValueError(f'UNKNOWN_RUNTIME_STATE:{runtime_state}')
    if runtime_state=='FRESH':
        if not isinstance(freshness_proof,dict) or freshness_proof.get('resolved_runtime_state')!='FRESH':
            raise ValueError('FRESH_RUNTIME_REQUIRES_VERIFIED_PROOF')
        if freshness_proof.get('route_id')!=route_id:
            raise ValueError('FRESH_RUNTIME_PROOF_ROUTE_MISMATCH')
        bad=[e.get('runtime_type') for e in freshness_proof.get('runtime_evidence') or [] if e.get('fresh') is not True]
        if bad:
            raise ValueError('FRESH_RUNTIME_PROOF_HAS_FAILED_RUNTIME:'+','.join(str(x) for x in bad))

    caps=expand_caps(capabilities,policy)
    caps, active_packs, dependency_expansions=expand_module_dependencies(caps)
    # Enforce Stage/Route forbidden context before any source is loaded.
    forbidden=route.get('forbidden_context') or []
    f_alias=policy.get('forbidden_capability_aliases') or {}
    conflicts=[]
    low={c.lower() for c in caps}
    for f in forbidden:
        if any(a.lower() in low for a in f_alias.get(f,[])):
            conflicts.append(f)
    if conflicts:
        raise ValueError('FORBIDDEN_CONTEXT_CAPABILITY:'+','.join(conflicts))

    creative=[]
    creative += route.get('source') or []
    fallback = runtime_state != 'FRESH'
    if fallback:
        creative += route.get('source_if_missing_or_stale') or []
        creative += route.get('compile_runtime_from_source') or []
    creative += route.get('execute_with') or []

    cond=route.get('conditional_source') or {}
    matched=[]
    capset=set(caps)
    for domain,files in cond.items():
        if domain in capset:
            matched.append(domain); creative += files or []
    creative=uniq(creative)

    # Control-plane and validator/schema files stay machine-side by default.
    machine=[]
    machine += route.get('validators') or []
    for item in route.get('validator_invocations') or []:
        if isinstance(item,dict) and item.get('validator'): machine.append(item['validator'])
    for item in route.get('text_only_validator_invocations') or []:
        if isinstance(item,dict) and item.get('validator'): machine.append(item['validator'])
    artmap=rr.get('structured_artifacts') or {}
    for a in route.get('structured_inputs') or []:
        if a in artmap: machine.append(artmap[a])
    for a in (route.get('produces_structured_artifacts') or []) + (route.get('additional_structured_artifacts') or []):
        if a in artmap: machine.append(artmap[a])
    machine += route.get('additional_output_schemas') or []
    if route.get('generation_job_contract'): machine.append(route['generation_job_contract'])
    machine=uniq(machine)

    all_domains=sorted(set(cond) | set((route.get('conditional_structured_inputs') or {}).keys()))
    excluded=[x for x in all_domains if x not in matched]
    soft=int((policy.get('recommended_limits') or {}).get('creative_source_file_count_soft',16))
    structured_inputs=uniq(route.get('structured_inputs') or [])
    for domain,items in (route.get('conditional_structured_inputs') or {}).items():
        if domain in capset:
            structured_inputs=uniq(structured_inputs+(items or []))
            matched.append(domain)
    # Include schemas for conditional structured inputs after they are resolved.
    for a in structured_inputs:
        if a in artmap: machine.append(artmap[a])
    machine=uniq(machine)

    out={
      'schema_version':1,'skill_version':'4.5.11',
      'context_load_plan_id':f'CLP-{route_id}-{runtime_state}',
      'route_id':route_id,'runtime_state':runtime_state,
      'runtime_freshness_proof':freshness_proof,
      'active_capabilities':caps,'active_module_packs':active_packs,'dependency_expansions':dependency_expansions,'matched_conditional_domains':sorted(set(matched)),
      'kernel_files':policy.get('kernel_files') or ['SKILL.md'],
      'runtime_types':uniq(route.get('runtime') or []),
      'structured_inputs':structured_inputs,
      'creative_context_files':creative,
      'machine_validation_files':machine,
      'machine_control_plane_files':policy.get('machine_control_plane_files') or [],
      'excluded_conditional_domains':excluded,
      'forbidden_context':forbidden,
      'source_fallback_loaded':fallback,
      'soft_file_count_exceeded':len(creative)>soft,
      'notes':[]
    }
    if out['soft_file_count_exceeded']:
        out['notes'].append('SOFT_CONTEXT_REVIEW_ONLY: refine route/capabilities or use verified fresh runtime; never drop required authority for token budget.')
    if runtime_state=='FRESH': out['notes'].append('VERIFIED_FAST_PATH: fallback source skipped only because runtime freshness proof passed.')
    else: out['notes'].append('SAFE_FALLBACK: runtime freshness was not proven; required fallback source remains loaded.')
    out['plan_fingerprint']=canonical_fp(out)
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--route',required=True)
    ap.add_argument('--runtime-state',choices=['AUTO','MISSING','STALE','INCOMPLETE'],default='AUTO',help='AUTO verifies real runtime evidence. FRESH cannot be caller-declared.')
    ap.add_argument('--runtime',action='append',default=[],help='TYPE=/path/to/runtime.yaml; used by AUTO freshness proof')
    ap.add_argument('--scope',action='append',default=[],help='scope key=value; required to prove FRESH')
    ap.add_argument('--source-root',action='append',default=[])
    ap.add_argument('--migration-compat-mode',action='store_true')
    ap.add_argument('--capability',action='append',default=[])
    ap.add_argument('--out')
    a=ap.parse_args()
    try:
        proof=None
        if a.runtime_state=='AUTO':
            bindings=parse_bindings(a.runtime)
            scope=parse_scope(a.scope)
            roots=[Path(x).expanduser().resolve() for x in a.source_root]
            proof=resolve_runtime_freshness(a.route,bindings,scope,roots,allow_compatibility=a.migration_compat_mode)
            runtime_state=proof['resolved_runtime_state']
        else:
            runtime_state=a.runtime_state
        out=build(a.route,runtime_state,a.capability,proof,allow_compatibility=a.migration_compat_mode)
    except ValueError as e:
        print(json.dumps({'pass':False,'failure_code':str(e)},ensure_ascii=False,indent=2)); return 2
    text=json.dumps(out,ensure_ascii=False,indent=2)
    if a.out: Path(a.out).write_text(text+'\n',encoding='utf-8')
    print(text); return 0
if __name__=='__main__': raise SystemExit(main())
