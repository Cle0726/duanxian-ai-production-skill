#!/usr/bin/env python3
"""Resolve route runtime freshness from real runtime capsules; never trust a caller-declared FRESH state."""
from __future__ import annotations
import argparse, hashlib, json, os
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CURRENT_SKILL_VERSION = '4.5.11'
VALID_STATUSES = {'VALID', 'CURRENT'}
STALE_STATUSES = {'STALE', 'INVALID', 'REBUILD_REQUIRED'}


def load_path(p: Path):
    text = p.read_text(encoding='utf-8')
    try:
        return json.loads(text)
    except Exception:
        return yaml.safe_load(text)


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def canonical_runtime_fp(d: dict) -> str:
    x = dict(d)
    x.pop('runtime_fingerprint', None)
    return hashlib.sha256(json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':'), default=str).encode('utf-8')).hexdigest()


def schema_path(runtime_type: str) -> Path:
    return ROOT / 'runtime' / (runtime_type.lower() + '.schema.yaml')


def parse_bindings(items):
    out = {}
    for item in items or []:
        if '=' not in item:
            raise ValueError(f'RUNTIME_BINDING_FORMAT:{item}')
        k, v = item.split('=', 1)
        k, v = k.strip(), v.strip()
        if not k or not v:
            raise ValueError(f'RUNTIME_BINDING_FORMAT:{item}')
        out[k] = Path(v).expanduser()
    return out


def parse_scope(items):
    out = {}
    for item in items or []:
        if '=' not in item:
            raise ValueError(f'SCOPE_FORMAT:{item}')
        k, v = item.split('=', 1)
        k, v = k.strip(), v.strip()
        if not k or not v:
            raise ValueError(f'SCOPE_FORMAT:{item}')
        out[k] = v
    return out


def resolve_source_path(key: str, runtime_path: Path, roots: list[Path]):
    p = Path(key).expanduser()
    if p.is_absolute() and p.exists():
        return p.resolve()
    candidates = [Path.cwd() / p, ROOT / p, runtime_path.parent / p]
    candidates.extend(r / p for r in roots)
    for c in candidates:
        try:
            if c.exists() and c.is_file():
                return c.resolve()
        except OSError:
            pass
    return None


def hard_conflict_codes(d: dict):
    codes = []
    # Only fields with explicit "open" semantics are treated as blockers here.
    for key in ('open_failures', 'realism_open_failures', 'open_p0_failures', 'open_p1_failures', 'critical_conflicts'):
        v = d.get(key)
        if isinstance(v, list) and v:
            codes.append(key)
    if isinstance(d.get('readiness'), dict):
        for k, v in d['readiness'].items():
            if str(k).upper().startswith(('P0', 'P1', 'HARD_')) and str(v).upper() in {'FAIL', 'BLOCKED', 'OPEN'}:
                codes.append(f'readiness.{k}')
    return codes


def verify_one(runtime_type: str, path: Path, expected_scope: dict, roots: list[Path], verify_sources: bool = True):
    issues = []
    evidence = {'runtime_type': runtime_type, 'path': str(path.resolve()) if path.exists() else str(path), 'checks': {}}
    if not path.exists():
        issues.append('RUNTIME_FILE_MISSING')
        evidence['issues'] = issues
        return evidence
    try:
        d = load_path(path)
    except Exception as e:
        issues.append(f'RUNTIME_READ_FAIL:{type(e).__name__}')
        evidence['issues'] = issues
        return evidence
    if not isinstance(d, dict):
        issues.append('RUNTIME_NOT_OBJECT')
        evidence['issues'] = issues
        return evidence

    sp = schema_path(runtime_type)
    if not sp.exists():
        issues.append('RUNTIME_SCHEMA_MISSING')
    else:
        schema = load_path(sp)
        schema_errors = sorted(Draft202012Validator(schema).iter_errors(d), key=lambda e: list(e.absolute_path))
        if schema_errors:
            issues.append('RUNTIME_SCHEMA_INVALID')
            evidence['schema_issues'] = [{'path': '/'.join(map(str, e.absolute_path)) or '$', 'message': e.message} for e in schema_errors[:12]]
    evidence['checks']['runtime_type'] = d.get('runtime_type') == runtime_type
    if d.get('runtime_type') != runtime_type:
        issues.append('RUNTIME_TYPE_MISMATCH')

    evidence['checks']['skill_version'] = d.get('skill_version') == CURRENT_SKILL_VERSION
    if d.get('skill_version') != CURRENT_SKILL_VERSION:
        issues.append('RUNTIME_SKILL_VERSION_STALE')

    status = str(d.get('status') or '').upper()
    evidence['status'] = status
    evidence['checks']['status'] = status in VALID_STATUSES
    if status in STALE_STATUSES:
        issues.append('RUNTIME_STATUS_STALE')
    elif status not in VALID_STATUSES:
        issues.append('RUNTIME_STATUS_NOT_FRESH')

    schema = load_path(sp) if sp.exists() else {}
    schema_has_scope = 'scope' in (schema.get('properties') or {})
    scope = d.get('scope')
    matched_scope = {}
    if not schema_has_scope:
        scope_ok = True
    else:
        scope_ok = isinstance(scope, dict) and bool(scope) and bool(expected_scope)
        if scope_ok:
            overlap = set(scope) & set(expected_scope)
            if not overlap:
                scope_ok = bool(scope.get('global') is True)
            else:
                for k in sorted(overlap):
                    matched_scope[k] = {'runtime': str(scope.get(k)), 'expected': str(expected_scope.get(k))}
                    if str(scope.get(k)) != str(expected_scope.get(k)):
                        scope_ok = False
            # If the runtime declares an expected key, it must match; broader runtimes may omit narrower keys.
    evidence['checks']['scope_coverage'] = scope_ok
    evidence['matched_scope'] = matched_scope
    if schema_has_scope:
        if not expected_scope:
            issues.append('EXPECTED_SCOPE_MISSING')
        elif not isinstance(scope, dict) or not scope:
            issues.append('RUNTIME_SCOPE_EMPTY')
        elif not scope_ok:
            issues.append('RUNTIME_SCOPE_MISMATCH')

    fp = d.get('runtime_fingerprint')
    fp_ok = isinstance(fp, str) and len(fp) == 64 and fp == canonical_runtime_fp(d)
    evidence['checks']['runtime_fingerprint'] = fp_ok
    if not fp_ok:
        issues.append('RUNTIME_FINGERPRINT_INVALID')

    schema_has_sources = 'source_fingerprints' in (schema.get('properties') or {})
    sf = d.get('source_fingerprints') if schema_has_sources else None
    source_checks = []
    source_ok = True
    if schema_has_sources and verify_sources:
        if not isinstance(sf, dict) or not sf:
            source_ok = False
            issues.append('RUNTIME_SOURCE_FINGERPRINTS_EMPTY')
        else:
            for key, expected in sf.items():
                rp = resolve_source_path(str(key), path, roots)
                row = {'source': str(key), 'expected': str(expected), 'resolved_path': str(rp) if rp else None}
                if rp is None:
                    row['match'] = False
                    source_ok = False
                else:
                    actual = sha256_file(rp)
                    row['actual'] = actual
                    row['match'] = actual == str(expected)
                    if not row['match']:
                        source_ok = False
                source_checks.append(row)
            if not source_ok:
                issues.append('RUNTIME_SOURCE_FINGERPRINT_MISMATCH_OR_UNRESOLVED')
    evidence['checks']['source_fingerprints'] = source_ok
    evidence['source_checks'] = source_checks

    blockers = hard_conflict_codes(d)
    evidence['checks']['no_open_hard_conflict'] = not blockers
    if blockers:
        issues.append('RUNTIME_OPEN_HARD_CONFLICT')
        evidence['hard_conflict_fields'] = blockers

    evidence['issues'] = issues
    evidence['fresh'] = not issues
    return evidence


def resolve(route_id: str, runtime_bindings: dict[str, Path], expected_scope: dict, roots: list[Path], allow_compatibility: bool = False):
    rr = load_path(ROOT / 'controller/route_registry.yaml')
    route = (rr.get('routes') or {}).get(route_id)
    if not route:
        raise ValueError(f'UNKNOWN_ROUTE:{route_id}')
    if route.get('compatibility_only') and not allow_compatibility:
        raise ValueError(f'COMPATIBILITY_ROUTE_REQUIRES_MIGRATION_MODE:{route_id}')
    required = list(dict.fromkeys(route.get('runtime') or []))
    evidence = []
    missing = []
    for rt in required:
        p = runtime_bindings.get(rt)
        if p is None:
            missing.append(rt)
            evidence.append({'runtime_type': rt, 'fresh': False, 'issues': ['RUNTIME_BINDING_MISSING']})
        else:
            evidence.append(verify_one(rt, p, expected_scope, roots))
    if missing:
        state = 'MISSING'
    elif any('RUNTIME_STATUS_STALE' in (e.get('issues') or []) or 'RUNTIME_SKILL_VERSION_STALE' in (e.get('issues') or []) or 'RUNTIME_SOURCE_FINGERPRINT_MISMATCH_OR_UNRESOLVED' in (e.get('issues') or []) for e in evidence):
        state = 'STALE'
    elif any(not e.get('fresh') for e in evidence):
        state = 'INCOMPLETE'
    else:
        state = 'FRESH'
    proof = {
        'schema_version': 1,
        'skill_version': CURRENT_SKILL_VERSION,
        'route_id': route_id,
        'resolved_runtime_state': state,
        'expected_runtime_types': required,
        'expected_scope': expected_scope,
        'runtime_evidence': evidence,
    }
    x = dict(proof)
    proof['proof_fingerprint'] = hashlib.sha256(json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()
    return proof


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--route', required=True)
    ap.add_argument('--runtime', action='append', default=[], help='TYPE=/path/to/runtime.yaml')
    ap.add_argument('--scope', action='append', default=[], help='scope key=value; at least one anchor is required for FRESH')
    ap.add_argument('--source-root', action='append', default=[])
    ap.add_argument('--migration-compat-mode', action='store_true')
    ap.add_argument('--out')
    a = ap.parse_args()
    try:
        bindings = parse_bindings(a.runtime)
        scope = parse_scope(a.scope)
        roots = [Path(x).expanduser().resolve() for x in a.source_root]
        out = resolve(a.route, bindings, scope, roots, allow_compatibility=a.migration_compat_mode)
    except ValueError as e:
        print(json.dumps({'pass': False, 'failure_code': str(e)}, ensure_ascii=False, indent=2))
        return 2
    text = json.dumps(out, ensure_ascii=False, indent=2)
    if a.out:
        Path(a.out).write_text(text + '\n', encoding='utf-8')
    print(text)
    return 0 if out['resolved_runtime_state'] == 'FRESH' else 3


if __name__ == '__main__':
    raise SystemExit(main())
