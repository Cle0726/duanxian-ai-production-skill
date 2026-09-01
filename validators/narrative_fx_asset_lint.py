#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

APPROVED={'APPROVED','APPROVED_SUPPORT'}
ALLOWED_TYPES={'NARRATIVE_FX_REFERENCE','NARRATIVE_FX_STATE_SHEET'}

def load(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))
def add(issues,t,**kw): d={'type':t}; d.update(kw); issues.append(d)

def lint(manifest, registry, phase='freeze'):
    issues=[]
    assets={a.get('asset_id'):a for a in (registry.get('assets') or []) if a.get('asset_id')}
    seen_id=set(); seen_reuse={}
    for fx in manifest.get('effects') or []:
        fid=fx.get('narrative_fx_id'); rk=fx.get('reuse_key'); mode=fx.get('authority_mode'); risk=fx.get('consistency_risk'); role=fx.get('narrative_role'); recur=fx.get('recurrence_count') or 0; status=fx.get('status'); aids=fx.get('asset_ids') or []
        if fid in seen_id: add(issues,'NARRATIVE_FX_DUPLICATE_ID',narrative_fx_id=fid)
        seen_id.add(fid)
        if rk in seen_reuse and seen_reuse[rk]!=fid: add(issues,'NARRATIVE_FX_REUSE_KEY_COLLISION',reuse_key=rk,effects=[seen_reuse[rk],fid])
        else: seen_reuse[rk]=fid
        scope=fx.get('scope'); scope_id=fx.get('scope_id'); scene_ids=fx.get('scene_ids') or []; shot_ids=fx.get('shot_ids') or []
        if not scope: add(issues,'NARRATIVE_FX_SCOPE_MISSING',narrative_fx_id=fid)
        if not scope_id: add(issues,'NARRATIVE_FX_SCOPE_ID_MISSING',narrative_fx_id=fid,scope=scope)
        if not scene_ids: add(issues,'NARRATIVE_FX_SCENE_SCOPE_MISSING',narrative_fx_id=fid,scope=scope)
        if not shot_ids: add(issues,'NARRATIVE_FX_SHOT_SCOPE_MISSING',narrative_fx_id=fid,scope=scope)
        if scope=='SHOT':
            if len(shot_ids)!=1 or scope_id not in shot_ids:
                add(issues,'NARRATIVE_FX_SHOT_SCOPE_ID_MISMATCH',narrative_fx_id=fid,scope_id=scope_id,shot_ids=shot_ids)
        elif scope=='SCENE':
            if len(scene_ids)!=1 or scope_id not in scene_ids:
                add(issues,'NARRATIVE_FX_SCENE_SCOPE_ID_MISMATCH',narrative_fx_id=fid,scope_id=scope_id,scene_ids=scene_ids)
        elif scope=='EPISODE':
            if scope_id!=manifest.get('episode_id'):
                add(issues,'NARRATIVE_FX_EPISODE_SCOPE_ID_MISMATCH',narrative_fx_id=fid,expected=manifest.get('episode_id'),actual=scope_id)
        elif scope in {'SHOT_GROUP','SEQUENCE'} and not scope_id:
            add(issues,'NARRATIVE_FX_GROUP_SCOPE_ID_MISSING',narrative_fx_id=fid,scope=scope)
        if recur < len(shot_ids):
            add(issues,'NARRATIVE_FX_RECURRENCE_COUNT_BELOW_SHOT_COVERAGE',narrative_fx_id=fid,recurrence_count=recur,shot_count=len(shot_ids),shot_ids=shot_ids)
        must_ref=(risk=='HIGH' or role in {'SIGNATURE_PHENOMENON','CONTINUITY_STATE'} or (recur>=2 and role in {'PLOT_CLUE','CAUSAL_EVENT'}))
        if mode=='TEXT_GRAMMAR_ONLY':
            if must_ref: add(issues,'NARRATIVE_FX_REFERENCE_REQUIRED',narrative_fx_id=fid,consistency_risk=risk,narrative_role=role,recurrence_count=recur)
            if aids: add(issues,'NARRATIVE_FX_TEXT_ONLY_HAS_ASSET',narrative_fx_id=fid,asset_ids=aids)
            if phase=='freeze' and status!='TEXT_ONLY_READY': add(issues,'NARRATIVE_FX_TEXT_ONLY_STATUS_INVALID',narrative_fx_id=fid,status=status)
            continue
        if mode!='NARRATIVE_FX_REFERENCE':
            add(issues,'NARRATIVE_FX_AUTHORITY_MODE_INVALID',narrative_fx_id=fid,actual=mode); continue
        if phase=='freeze':
            if status!='APPROVED': add(issues,'NARRATIVE_FX_NOT_APPROVED',narrative_fx_id=fid,status=status)
            if not aids: add(issues,'NARRATIVE_FX_ASSET_MISSING',narrative_fx_id=fid)
        required_states=set(fx.get('required_visual_states') or [])
        covered=set()
        for aid in aids:
            a=assets.get(aid)
            if not a:
                add(issues,'NARRATIVE_FX_ASSET_MISSING',narrative_fx_id=fid,asset_id=aid); continue
            if phase=='freeze' and a.get('status') not in APPROVED: add(issues,'NARRATIVE_FX_ASSET_NOT_APPROVED',narrative_fx_id=fid,asset_id=aid,status=a.get('status'))
            if a.get('asset_type') not in ALLOWED_TYPES: add(issues,'NARRATIVE_FX_ASSET_TYPE_FAIL',narrative_fx_id=fid,asset_id=aid,actual=a.get('asset_type'))
            if a.get('media_kind')!='IMAGE': add(issues,'NARRATIVE_FX_MEDIA_KIND_FAIL',narrative_fx_id=fid,asset_id=aid,actual=a.get('media_kind'))
            if a.get('authority_role')!='NARRATIVE_FX_AUTHORITY': add(issues,'NARRATIVE_FX_AUTHORITY_ROLE_FAIL',narrative_fx_id=fid,asset_id=aid,actual=a.get('authority_role'))
            if a.get('narrative_fx_id')!=fid: add(issues,'NARRATIVE_FX_ENTITY_SCOPE_MISMATCH',narrative_fx_id=fid,asset_id=aid,actual=a.get('narrative_fx_id'))
            if (a.get('video_usage') or {}).get('primary_visual_eligible') is True: add(issues,'NARRATIVE_FX_PRIMARY_VISUAL_FORBIDDEN',narrative_fx_id=fid,asset_id=aid)
            if a.get('asset_type')=='NARRATIVE_FX_STATE_SHEET' and a.get('layout_type')=='MULTI_PANEL' and (a.get('video_usage') or {}).get('direct_input_allowed') is True:
                add(issues,'NARRATIVE_FX_STATE_SHEET_DIRECT_REFERENCE_FORBIDDEN',narrative_fx_id=fid,asset_id=aid)
            for s in a.get('fx_state_ids') or []: covered.add(s)
        missing=sorted(required_states-covered)
        if required_states and missing: add(issues,'NARRATIVE_FX_STATE_COVERAGE_GAP',narrative_fx_id=fid,missing_states=missing,covered_states=sorted(covered))
    if phase=='freeze' and manifest.get('status')!='FROZEN': add(issues,'NARRATIVE_FX_MANIFEST_NOT_FROZEN',status=manifest.get('status'))
    return {'pass':not issues,'phase':phase,'effect_count':len(manifest.get('effects') or []),'issues':issues}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--manifest',required=True); ap.add_argument('--asset-registry',required=True); ap.add_argument('--phase',choices=['planning','build','freeze'],default='freeze'); a=ap.parse_args()
    out=lint(load(a.manifest),load(a.asset_registry),a.phase); print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
