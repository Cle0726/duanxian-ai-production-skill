#!/usr/bin/env python3
"""Validate Visual Evidence persistence and Text-only reference safety (V4.5.3)."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

def load(path):
    return yaml.safe_load(Path(path).read_text(encoding='utf-8'))

def index_registry(registry):
    return {a.get('asset_id'): a for a in (registry or {}).get('assets', []) if a.get('asset_id')}

def index_evidence(evidence):
    out={}; dup=[]
    for r in (evidence or {}).get('records', []):
        aid=r.get('asset_id')
        if not aid: continue
        if aid in out: dup.append(aid)
        out[aid]=r
    return out, dup

def current_record(asset, rec):
    if not rec or rec.get('evidence_status')!='CURRENT':
        return False
    af=asset.get('fingerprint')
    ef=rec.get('source_fingerprint')
    return bool(af and ef and af==ef)

def lint(registry, evidence, phase='capture', reference_runtime=None, vision_mode=None):
    issues=[]; warnings=[]
    assets=index_registry(registry); records,dup=index_evidence(evidence)
    for aid in dup:
        issues.append({'type':'VISUAL_EVIDENCE_DUPLICATE_ASSET_RECORD','asset_id':aid})

    # Validate evidence-to-file provenance.
    for aid,rec in records.items():
        asset=assets.get(aid)
        if not asset:
            issues.append({'type':'VISUAL_EVIDENCE_ASSET_NOT_IN_REGISTRY','asset_id':aid}); continue
        if rec.get('evidence_status')=='CURRENT' and not current_record(asset,rec):
            issues.append({'type':'VISUAL_EVIDENCE_STALE','asset_id':aid,'asset_fingerprint':asset.get('fingerprint'),'evidence_fingerprint':rec.get('source_fingerprint')})
        if rec.get('evidence_status')=='CURRENT':
            insp=(rec.get('inspector') or {}).get('mode')
            if insp not in {'MULTIMODAL_MODEL','HUMAN','MIXED'}:
                issues.append({'type':'VISUAL_EVIDENCE_INSPECTOR_INVALID','asset_id':aid})
            obs=rec.get('observed') or {}
            if 'summary' not in obs or 'fact_codes' not in obs or 'issue_codes' not in obs:
                issues.append({'type':'VISUAL_EVIDENCE_OBSERVATION_INCOMPLETE','asset_id':aid})

    if phase=='reference':
        rr=reference_runtime or {}
        mode=vision_mode or rr.get('controller_mode') or 'UNKNOWN'
        bindings=rr.get('bindings') or []
        required=set(rr.get('required_visual_facts') or [])
        forbidden=set(rr.get('forbidden_visual_facts') or [])
        covered=set(); observed_conflicts=set()
        for b in bindings:
            aid=b.get('asset_id')
            if not aid: continue
            asset=assets.get(aid)
            if not asset:
                issues.append({'type':'REFERENCE_ASSET_NOT_IN_REGISTRY','asset_id':aid}); continue
            # DATA/AUDIO can be routed without image evidence. Deterministic planning diagrams are not final visual evidence.
            needs_visual=(asset.get('media_kind')=='IMAGE')
            rec=records.get(aid)
            is_current=current_record(asset,rec) if rec else False
            if mode=='TEXT_ONLY_CONTINUATION' and needs_visual and not is_current:
                issues.append({'type':'TEXT_ONLY_VISUAL_EVIDENCE_MISSING' if not rec else 'TEXT_ONLY_VISUAL_EVIDENCE_STALE','asset_id':aid})
                continue
            if is_current:
                obs=rec.get('observed') or {}; role=rec.get('role_assessment') or {}
                facts=set(obs.get('fact_codes') or []); bad=set(obs.get('issue_codes') or [])
                covered |= facts; observed_conflicts |= (facts|bad)
                requested_role=b.get('visual_evidence_role') or b.get('authority_role')
                unsafe=set(role.get('unsafe_roles') or [])
                if requested_role and requested_role in unsafe:
                    issues.append({'type':'VISUAL_ROLE_EVIDENCE_CONFLICT','asset_id':aid,'role':requested_role})
                if b.get('primary_visual') and role.get('primary_visual_eligible') is False and requested_role!='PRIMARY_VISUAL':
                    issues.append({'type':'VISUAL_ROLE_EVIDENCE_CONFLICT','asset_id':aid,'role':'PRIMARY_VISUAL'})
                if b.get('direct_video_eligible') and role.get('direct_video_eligible') is False:
                    issues.append({'type':'VISUAL_ROLE_EVIDENCE_CONFLICT','asset_id':aid,'role':'DIRECT_VIDEO'})
        missing=sorted(required-covered)
        if mode=='TEXT_ONLY_CONTINUATION' and missing:
            issues.append({'type':'VISUAL_FACT_COVERAGE_GAP','missing_fact_codes':missing})
        conflicts=sorted(forbidden & observed_conflicts)
        if conflicts:
            issues.append({'type':'VISUAL_FACT_CONFLICT','conflict_codes':conflicts})
        if mode!='TEXT_ONLY_CONTINUATION':
            missing_evidence=[b.get('asset_id') for b in bindings if b.get('asset_id') in assets and assets[b.get('asset_id')].get('media_kind')=='IMAGE' and not current_record(assets[b.get('asset_id')],records.get(b.get('asset_id')))]
            if missing_evidence:
                warnings.append({'type':'VISUAL_EVIDENCE_PERSISTENCE_RECOMMENDED','asset_ids':sorted(set(missing_evidence))})
    return {'pass':not issues,'phase':phase,'issues':issues,'warnings':warnings}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--asset-registry',required=True)
    ap.add_argument('--evidence',required=True)
    ap.add_argument('--phase',choices=['capture','reference'],default='capture')
    ap.add_argument('--reference-runtime')
    ap.add_argument('--vision-mode',choices=['MULTIMODAL_ACTIVE','TEXT_ONLY_CONTINUATION','UNKNOWN'])
    a=ap.parse_args()
    out=lint(load(a.asset_registry),load(a.evidence),a.phase,load(a.reference_runtime) if a.reference_runtime else None,a.vision_mode)
    print(json.dumps(out,ensure_ascii=False,indent=2))
    raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
