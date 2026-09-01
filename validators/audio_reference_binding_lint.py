#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml
AUDIO_MODES={'AUDIO_AUTHORITY','VOICE_AUTHORITY','RHYTHM_AUTHORITY','AMBIENCE_AUTHORITY','MUSIC_AUTHORITY','SFX_AUTHORITY'}
APPROVED_REGISTRY={'APPROVED','APPROVED_SUPPORT','APPROVED_ASSEMBLY','APPROVED_SCOPED_FIGURE','APPROVED_VIDEO_CONDITIONING'}

def load(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))
def add(issues,t,**kw): d={'type':t}; d.update(kw); issues.append(d)

def scope_matches(x, job):
    scope=x.get('scope')
    checks={'EPISODE':('episode_id','episode_id'),'SEQUENCE':('sequence_id','sequence_id'),'SCENE':('scene_id','scene_id'),'SHOT':('shot_id','shot_id')}
    if scope in checks:
        xf,jf=checks[scope]; xv=x.get(xf); jv=job.get(jf)
        if xv and jv and xv!=jv: return False, xf, xv, jv
    return True,None,None,None

def lint(job, registry, manifest):
    issues=[]; assets={a.get('asset_id'):a for a in (registry.get('assets') or []) if a.get('asset_id')}; aud={x.get('asset_id'):x for x in (manifest.get('audio_assets') or []) if x.get('asset_id')}
    if job.get('media_kind')=='VIDEO' and manifest.get('status') not in {'READY','APPROVED'}:
        add(issues,'AUDIO_MANIFEST_NOT_READY_FOR_VIDEO',status=manifest.get('status'))
    for b in job.get('required_bindings') or []:
        aid=b.get('asset_id'); a=assets.get(aid); mode=b.get('binding_mode'); role=b.get('role'); audio_declared=(mode in AUDIO_MODES or role in AUDIO_MODES)
        if not a:
            add(issues,'GENERATION_REQUIRED_BINDING_ASSET_UNKNOWN',asset_id=aid)
            continue
        mk=a.get('media_kind')
        if mk=='VIDEO': add(issues,'REFERENCE_VIDEO_FORBIDDEN',asset_id=aid,reason='FORBIDDEN_QUOTA_COST')
        if audio_declared and mk!='AUDIO':
            add(issues,'AUDIO_REFERENCE_ASSET_KIND_MISMATCH',asset_id=aid,media_kind=mk,binding_mode=mode,role=role)
            continue
        if mk=='AUDIO':
            if not audio_declared:
                add(issues,'AUDIO_REFERENCE_ROLE_UNDECLARED',asset_id=aid,binding_mode=mode,role=role)
            x=aud.get(aid)
            if not x: add(issues,'AUDIO_REFERENCE_NOT_IN_MANIFEST',asset_id=aid); continue
            if x.get('status')!='APPROVED' or x.get('reference_policy')!='VIDEO_REFERENCE_ALLOWED' or x.get('direct_reference_eligible') is not True:
                add(issues,'AUDIO_REFERENCE_NOT_READY',asset_id=aid,status=x.get('status'),reference_policy=x.get('reference_policy'))
            if x.get('binding_status')!='READY': add(issues,'AUDIO_REFERENCE_NATIVE_BINDING_NOT_READY',asset_id=aid,binding_status=x.get('binding_status'))
            if a.get('status') not in APPROVED_REGISTRY: add(issues,'AUDIO_REFERENCE_REGISTRY_NOT_APPROVED',asset_id=aid,status=a.get('status'))
            if not (a.get('video_usage') or {}).get('direct_input_allowed', False): add(issues,'AUDIO_REFERENCE_REGISTRY_DIRECT_INPUT_FORBIDDEN',asset_id=aid)
            mtok=x.get('native_token'); rtok=a.get('native_token'); tok=mtok or rtok
            if mtok and rtok and mtok!=rtok: add(issues,'AUDIO_NATIVE_TOKEN_MISMATCH',asset_id=aid,manifest=mtok,registry=rtok)
            if not tok: add(issues,'AUDIO_REFERENCE_NATIVE_TOKEN_MISSING',asset_id=aid)
            if not b.get('native_token'): add(issues,'AUDIO_REFERENCE_JOB_TOKEN_MISSING',asset_id=aid,expected=tok)
            elif tok and b.get('native_token')!=tok: add(issues,'AUDIO_REFERENCE_JOB_TOKEN_MISMATCH',asset_id=aid,expected=tok,actual=b.get('native_token'))
            ms=x.get('subject_entity_id'); rs=a.get('subject_entity_id')
            if ms and rs and ms!=rs: add(issues,'AUDIO_SUBJECT_ENTITY_MISMATCH',asset_id=aid,manifest=ms,registry=rs)
            ok,field,expected,actual=scope_matches(x,job)
            if not ok: add(issues,'AUDIO_REFERENCE_SCOPE_MISMATCH',asset_id=aid,field=field,expected=expected,actual=actual)
    return {'pass':not issues,'issues':issues}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--job',required=True); ap.add_argument('--registry',required=True); ap.add_argument('--manifest',required=True); a=ap.parse_args()
    out=lint(load(a.job),load(a.registry),load(a.manifest)); print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
