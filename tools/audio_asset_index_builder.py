#!/usr/bin/env python3
from __future__ import annotations
import argparse, yaml, json, hashlib
from pathlib import Path

def infer_type(asset_type):
    t=(asset_type or '').upper()
    if 'VOICE' in t: return 'VOICE_IDENTITY'
    if 'TEMP' in t and 'DIALOGUE' in t: return 'TEMP_SYNC_DIALOGUE'
    if 'DIALOGUE' in t: return 'DIALOGUE_TAKE'
    if 'AMBI' in t: return 'AMBIENCE'
    if 'FOLEY' in t: return 'FOLEY'
    if 'SFX' in t: return 'SFX'
    if 'RHYTHM' in t: return 'RHYTHM_REFERENCE'
    if 'PERFORMANCE' in t: return 'PERFORMANCE_AUDIO_REFERENCE'
    if 'DIEGETIC' in t and ('MUSIC' in t or 'BGM' in t): return 'DIEGETIC_MUSIC'
    if 'MUSIC' in t or 'BGM' in t: return 'MUSIC'
    return 'OTHER'

def canon_fp(doc):
    clone=dict(doc); clone['manifest_fingerprint']=None
    text=yaml.safe_dump(clone,sort_keys=True,allow_unicode=True).encode('utf-8')
    return hashlib.sha256(text).hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--registry',required=True); ap.add_argument('--output',required=True); ap.add_argument('--episode-id'); a=ap.parse_args()
    reg=yaml.safe_load(Path(a.registry).read_text(encoding='utf-8')); out=[]
    rolemap={'VOICE_IDENTITY':'VOICE_IDENTITY','DIALOGUE_TAKE':'DIALOGUE_CONTENT','TEMP_SYNC_DIALOGUE':'TIMING','AMBIENCE':'AMBIENCE','FOLEY':'SFX','SFX':'SFX','MUSIC':'MUSIC','DIEGETIC_MUSIC':'MUSIC','RHYTHM_REFERENCE':'RHYTHM','PERFORMANCE_AUDIO_REFERENCE':'PERFORMANCE','OTHER':'OTHER'}
    for x in reg.get('assets') or []:
        if x.get('media_kind')!='AUDIO': continue
        typ=infer_type(x.get('asset_type')); approved=str(x.get('status','')).startswith('APPROVED'); token=x.get('native_token')
        if x.get('shot_id'): scope='SHOT'
        elif x.get('scene_id'): scope='SCENE'
        elif typ=='VOICE_IDENTITY' and x.get('subject_entity_id'): scope='CHARACTER'
        elif a.episode_id: scope='EPISODE'
        else: scope='GLOBAL'
        video_eligible=(typ!='OTHER' and approved)
        policy='VIDEO_REFERENCE_ALLOWED' if video_eligible else 'STAGE06_ONLY'
        intended=['STAGE06_EDIT'] + (['VIDEO_REFERENCE'] if video_eligible else []) + (['VOICE_CANON'] if typ=='VOICE_IDENTITY' else [])
        out.append({'asset_id':x.get('asset_id'),'asset_display_name':x.get('asset_display_name'),'native_token':token,'audio_type':typ,'authority_role':rolemap[typ],'scope':scope,'subject_entity_id':x.get('subject_entity_id'),'episode_id':a.episode_id,'sequence_id':x.get('sequence_id'),'scene_id':x.get('scene_id'),'shot_id':x.get('shot_id'),'reuse_key':x.get('reuse_key'),'version':x.get('version'),'fingerprint':x.get('fingerprint'),'status':'APPROVED' if approved else 'DRAFT','reference_policy':policy,'binding_status':'READY' if token else ('PENDING_NATIVE_BINDING' if video_eligible else 'NOT_REQUIRED'),'direct_reference_eligible':video_eligible,'intended_use':intended})
    doc={'schema_version':1,'skill_version':'4.5.11','audio_asset_manifest_id':'AUDIO-MANIFEST-'+(a.episode_id or 'GLOBAL'),'episode_id':a.episode_id,'status':'READY','manifest_fingerprint':None,'audio_assets':out}
    doc['manifest_fingerprint']=canon_fp(doc)
    Path(a.output).write_text(yaml.safe_dump(doc,sort_keys=False,allow_unicode=True),encoding='utf-8'); print(json.dumps({'ok':True,'count':len(out),'output':a.output,'manifest_fingerprint':doc['manifest_fingerprint']},ensure_ascii=False))
if __name__=='__main__': main()
