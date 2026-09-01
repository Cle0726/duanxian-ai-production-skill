#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml
APPROVED_REGISTRY={'APPROVED','APPROVED_SUPPORT','APPROVED_ASSEMBLY','APPROVED_SCOPED_FIGURE','APPROVED_VIDEO_CONDITIONING'}
ROLE_BY_TYPE={
 'VOICE_IDENTITY':{'VOICE_IDENTITY'}, 'DIALOGUE_TAKE':{'DIALOGUE_CONTENT'}, 'TEMP_SYNC_DIALOGUE':{'TIMING','DIALOGUE_CONTENT'},
 'SFX':{'SFX'}, 'FOLEY':{'SFX'}, 'AMBIENCE':{'AMBIENCE'}, 'MUSIC':{'MUSIC'}, 'DIEGETIC_MUSIC':{'MUSIC'},
 'RHYTHM_REFERENCE':{'RHYTHM'}, 'PERFORMANCE_AUDIO_REFERENCE':{'PERFORMANCE','TIMING','RHYTHM'}, 'OTHER':{'OTHER'}
}
SCOPE_FIELD={'CHARACTER':'subject_entity_id','EPISODE':'episode_id','SEQUENCE':'sequence_id','SCENE':'scene_id','SHOT':'shot_id'}

def load(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))
def add(issues,t,**kw): d={'type':t}; d.update(kw); issues.append(d)

def lint(manifest, registry):
    issues=[]; assets={a.get('asset_id'):a for a in (registry.get('assets') or []) if a.get('asset_id')}; seen=set(); reuse={}; tokens={}
    for x in manifest.get('audio_assets') or []:
        aid=x.get('asset_id')
        if aid in seen: add(issues,'AUDIO_MANIFEST_DUPLICATE_ASSET',asset_id=aid)
        seen.add(aid); a=assets.get(aid)
        if not a: add(issues,'AUDIO_MANIFEST_ASSET_UNKNOWN',asset_id=aid); continue
        if a.get('media_kind')!='AUDIO': add(issues,'AUDIO_MANIFEST_MEDIA_KIND_FAIL',asset_id=aid,actual=a.get('media_kind'))
        typ=x.get('audio_type'); role=x.get('authority_role'); allowed=ROLE_BY_TYPE.get(typ,set())
        if allowed and role not in allowed: add(issues,'AUDIO_TYPE_AUTHORITY_ROLE_MISMATCH',asset_id=aid,audio_type=typ,authority_role=role,allowed=sorted(allowed))
        sf=SCOPE_FIELD.get(x.get('scope'))
        if sf and not x.get(sf): add(issues,'AUDIO_SCOPE_OWNER_MISSING',asset_id=aid,scope=x.get('scope'),required_field=sf)
        if x.get('status')=='APPROVED' and a.get('status') not in APPROVED_REGISTRY:
            add(issues,'AUDIO_MANIFEST_APPROVED_BUT_REGISTRY_NOT_APPROVED',asset_id=aid,status=a.get('status'))
        regtok=a.get('native_token'); mtok=x.get('native_token')
        if regtok and mtok and regtok!=mtok: add(issues,'AUDIO_NATIVE_TOKEN_MISMATCH',asset_id=aid,manifest=mtok,registry=regtok)
        ms=x.get('subject_entity_id'); rs=a.get('subject_entity_id')
        if ms and rs and ms!=rs: add(issues,'AUDIO_SUBJECT_ENTITY_MISMATCH',asset_id=aid,manifest=ms,registry=rs)
        if x.get('reference_policy')=='VIDEO_REFERENCE_ALLOWED':
            if x.get('status')!='APPROVED': add(issues,'AUDIO_VIDEO_REFERENCE_NOT_APPROVED',asset_id=aid)
            if x.get('direct_reference_eligible') is not True: add(issues,'AUDIO_VIDEO_REFERENCE_NOT_ELIGIBLE',asset_id=aid)
            if x.get('binding_status')=='READY' and not (mtok or regtok): add(issues,'AUDIO_NATIVE_TOKEN_MISSING',asset_id=aid)
            if 'VIDEO_REFERENCE' not in (x.get('intended_use') or []): add(issues,'AUDIO_VIDEO_REFERENCE_INTENDED_USE_MISSING',asset_id=aid)
            if x.get('status')=='APPROVED' and not x.get('fingerprint'): add(issues,'AUDIO_APPROVED_FINGERPRINT_MISSING',asset_id=aid)
        elif x.get('direct_reference_eligible') is True:
            add(issues,'AUDIO_DIRECT_ELIGIBILITY_POLICY_CONFLICT',asset_id=aid,reference_policy=x.get('reference_policy'))
        if typ=='VOICE_IDENTITY' and not x.get('subject_entity_id'): add(issues,'VOICE_AUDIO_SUBJECT_ENTITY_MISSING',asset_id=aid)
        rk=x.get('reuse_key')
        if rk and x.get('status')!='DEPRECATED':
            if rk in reuse: add(issues,'AUDIO_REUSE_KEY_CONFLICT',reuse_key=rk,asset_ids=[reuse[rk],aid])
            else: reuse[rk]=aid
        tok=mtok or regtok
        if tok and x.get('status')!='DEPRECATED':
            if tok in tokens and tokens[tok]!=aid: add(issues,'AUDIO_NATIVE_TOKEN_COLLISION',native_token=tok,asset_ids=[tokens[tok],aid])
            else: tokens[tok]=aid
    return {'pass':not issues,'audio_asset_count':len(seen),'issues':issues}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--manifest',required=True); ap.add_argument('--registry',required=True); a=ap.parse_args()
    out=lint(load(a.manifest),load(a.registry)); print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
