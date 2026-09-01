#!/usr/bin/env python3
import argparse, json, re, sys
from pathlib import Path
from temporal_scope import overlap, numeric_interval

try:
    from prompt_constraint_lint import lint as base_lint
except Exception:
    base_lint = None


def norm(v):
    return str(v or '').strip().upper()


def ambiguous(v):
    s = norm(v)
    return bool(re.search(r'\bOR\b|/OR/|(?:^|\s)或(?:\s|$)|或者|二选一|\bMAYBE\b|\bALTERNATIVELY\b', s, re.I))


def key(c):
    # Frame scope is semantic, not decoration: WORLD and FRAME_VISIBLE are different claims.
    return (norm(c.get('domain')), norm(c.get('subject')), norm(c.get('predicate')), norm(c.get('target')), norm(c.get('frame_scope')))


def same_value_polarity(a, b):
    return key(a) == key(b) and norm(a.get('value')) == norm(b.get('value')) and norm(a.get('polarity','POSITIVE')) == norm(b.get('polarity','POSITIVE'))


def claim_within_resolved(r, c):
    if not same_value_polarity(r, c):
        return False
    ri, ci = numeric_interval(r), numeric_interval(c)
    if ri and ci:
        return ci[0] >= ri[0] - 1e-6 and ci[1] <= ri[1] + 1e-6
    rt, ct = norm(r.get('time_scope')), norm(c.get('time_scope'))
    if rt or ct:
        return rt == ct
    return True


def resolved_covered(r, claims):
    matching=[c for c in claims if same_value_polarity(r,c) and claim_within_resolved(r,c)]
    ri=numeric_interval(r)
    if not ri:
        return bool(matching)
    spans=[]
    for c in matching:
        ci=numeric_interval(c)
        if ci: spans.append(ci)
    if not spans:
        return False
    spans.sort()
    cursor=ri[0]
    for a,b in spans:
        if b < cursor-1e-6: continue
        if a > cursor+1e-6: return False
        cursor=max(cursor,b)
        if cursor >= ri[1]-1e-6: return True
    return cursor >= ri[1]-1e-6


def same_claim(a, b):
    # Exact semantic match with no temporal expansion. Used for authorization, not just overlap.
    return claim_within_resolved(a, b)


def lint(data):
    resolved = data.get('resolved_constraints', [])
    claims = data.get('prompt_claims', [])
    issues = []

    for c in claims:
        if ambiguous(c.get('value')):
            issues.append({'type':'PROMPT_AMBIGUOUS_EXCLUSIVE_VALUE','id':c.get('id'),'value':c.get('value')})
        owner = norm(c.get('owner','PROMPT_COMPILER'))
        if owner and owner != 'PROMPT_COMPILER':
            issues.append({'type':'PROMPT_MULTI_OWNER_REINTRODUCED','id':c.get('id'),'owner':c.get('owner')})

        field_candidates = [r for r in resolved if key(r) == key(c)]
        if not field_candidates:
            issues.append({'type':'PROMPT_NEW_CONSTRAINT','id':c.get('id'),'claim':key(c),'value':c.get('value')})
        elif not any(same_value_polarity(r, c) for r in field_candidates):
            issues.append({'type':'PROMPT_STATE_CONTRADICTION','id':c.get('id'),'resolved_values':[r.get('value') for r in field_candidates],'prompt_value':c.get('value')})
        elif not any(claim_within_resolved(r, c) for r in field_candidates):
            issues.append({'type':'PROMPT_STATE_CONTRADICTION','id':c.get('id'),'reason':'PROMPT_TEMPORAL_SCOPE_EXPANSION','resolved_scopes':[(r.get('start'),r.get('end'),r.get('time_scope')) for r in field_candidates],'prompt_scope':(c.get('start'),c.get('end'),c.get('time_scope'))})

    for r in resolved:
        sr = norm(r.get('surface_requirement'))
        required = r.get('required', True)
        if sr == 'MODEL_TEXT' and required:
            if not resolved_covered(r, claims):
                issues.append({'type':'PROMPT_MISSING_REQUIRED_MODEL_TEXT','id':r.get('id'),'claim':key(r),'value':r.get('value'),'reason':'FULL_REQUIRED_SCOPE_NOT_COVERED'})

    # Duplicate semantic keys with different owners/values are reintroduced conflicts.
    for i,a in enumerate(claims):
        for b in claims[i+1:]:
            if key(a)==key(b) and overlap(a,b):
                if norm(a.get('value')) != norm(b.get('value')) or norm(a.get('polarity','POSITIVE')) != norm(b.get('polarity','POSITIVE')):
                    issues.append({'type':'PROMPT_MULTI_OWNER_REINTRODUCED','a':a.get('id'),'b':b.get('id'),'reason':'SAME_FIELD_MULTIPLE_FINAL_VALUES'})

    # Reuse pre-compile mechanical conflict classes against the final semantic claims.
    if base_lint:
        base = base_lint({'constraints': claims, 'references': data.get('references', [])})
        for c in base.get('conflicts', []):
            issues.append({'type':'PROMPT_STATE_CONTRADICTION','source_conflict':c})

    counts = {
        'NEW_CONSTRAINT_IN_PROMPT': sum(1 for x in issues if x['type']=='PROMPT_NEW_CONSTRAINT'),
        'MISSING_REQUIRED_MODEL_TEXT': sum(1 for x in issues if x['type']=='PROMPT_MISSING_REQUIRED_MODEL_TEXT'),
        'STATE_CONTRADICTION': sum(1 for x in issues if x['type']=='PROMPT_STATE_CONTRADICTION'),
        'AMBIGUOUS_EXCLUSIVE_VALUE': sum(1 for x in issues if x['type']=='PROMPT_AMBIGUOUS_EXCLUSIVE_VALUE'),
        'MULTI_OWNER_REINTRODUCED': sum(1 for x in issues if x['type']=='PROMPT_MULTI_OWNER_REINTRODUCED'),
    }
    return {'status':'PASS' if not issues else 'BLOCKED', 'counts':counts, 'issues':issues}


def main():
    ap = argparse.ArgumentParser(description='Post-compile semantic-claim closure lint')
    ap.add_argument('json_file', nargs='?', help='JSON file; stdin if omitted')
    args = ap.parse_args()
    if args.json_file:
        data = json.loads(Path(args.json_file).read_text(encoding='utf-8'))
    else:
        data = json.load(sys.stdin)
    result = lint(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result['status']=='PASS' else 2)

if __name__ == '__main__':
    main()
