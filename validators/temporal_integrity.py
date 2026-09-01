from __future__ import annotations
import hashlib, json
from pathlib import Path
import yaml

def load(path):
    p=Path(path); text=p.read_text(encoding='utf-8')
    return json.loads(text) if p.suffix.lower()=='.json' else yaml.safe_load(text)
def canonical_without(d,key):
    x=dict(d); x.pop(key,None)
    return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def fingerprint(d,key): return hashlib.sha256(canonical_without(d,key)).hexdigest()
def sha_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
    return h.hexdigest()
def resolve_ref(owner_path, ref):
    p=Path(ref)
    if p.is_absolute(): return p
    return (Path(owner_path).resolve().parent/p).resolve()

def validate_snapshot_path(path, seen=None):
    path=Path(path).resolve(); seen=set() if seen is None else set(seen); issues=[]
    if str(path) in seen: return {'pass':False,'issues':[{'type':'TEMPORAL_SNAPSHOT_CHAIN_CYCLE','snapshot_ref':str(path)}]}
    seen.add(str(path))
    if not path.is_file(): return {'pass':False,'issues':[{'type':'CONTINUITY_SNAPSHOT_MISSING','snapshot_ref':str(path)}]}
    try: d=load(path)
    except Exception as e: return {'pass':False,'issues':[{'type':'CONTINUITY_SNAPSHOT_PARSE_FAIL','detail':str(e)}]}
    frame=d.get('ending_frame_ref'); fp=d.get('ending_frame_file_sha256')
    if not frame: issues.append({'type':'CONTINUITY_ENDING_ANCHOR_MISSING'})
    else:
        q=resolve_ref(path,frame)
        if not q.is_file(): issues.append({'type':'CONTINUITY_ENDING_ANCHOR_FILE_MISSING','ending_frame_ref':str(q)})
        elif not fp or sha_file(q)!=fp: issues.append({'type':'CONTINUITY_ENDING_ANCHOR_HASH_MISMATCH'})
    if not d.get('source_video_fingerprint'): issues.append({'type':'CONTINUITY_SOURCE_VIDEO_FINGERPRINT_MISSING'})
    mode=d.get('provenance_mode')
    if mode not in {'LOCAL_DECODED_VIDEO','PLATFORM_EXTRACTED_VERIFIED'}: issues.append({'type':'CONTINUITY_PROVENANCE_INVALID','provenance_mode':mode})
    if mode=='PLATFORM_EXTRACTED_VERIFIED' and not d.get('extraction_proof_ref'): issues.append({'type':'CONTINUITY_PLATFORM_EXTRACTION_PROOF_MISSING'})
    try: depth=int(d.get('pixel_lineage_depth'))
    except Exception: depth=-1
    prev=d.get('previous_continuity_snapshot_ref'); prevfp=d.get('previous_continuity_snapshot_fingerprint')
    if prev:
        pp=resolve_ref(path,prev)
        r=validate_snapshot_path(pp,seen)
        issues.extend(r['issues'])
        if r.get('snapshot'):
            pd=r['snapshot']; actual=pd.get('snapshot_fingerprint')
            if not prevfp or prevfp!=actual: issues.append({'type':'TEMPORAL_PREVIOUS_SNAPSHOT_FINGERPRINT_MISMATCH'})
            try: expected=int(pd.get('pixel_lineage_depth'))+1
            except Exception: expected=-1
            if depth!=expected: issues.append({'type':'TEMPORAL_PIXEL_LINEAGE_DERIVATION_FAIL','expected':expected,'actual':depth})
        if d.get('lineage_evidence_mode')!='RECURSIVE_SNAPSHOT': issues.append({'type':'TEMPORAL_LINEAGE_EVIDENCE_MODE_INVALID'})
    else:
        if depth!=1: issues.append({'type':'TEMPORAL_PIXEL_LINEAGE_ROOT_INVALID','expected':1,'actual':depth})
        if d.get('lineage_evidence_mode')!='ROOT_GENERATED_VIDEO': issues.append({'type':'TEMPORAL_LINEAGE_EVIDENCE_MODE_INVALID'})
        if prevfp: issues.append({'type':'TEMPORAL_PREVIOUS_SNAPSHOT_REF_MISSING'})
    debt=d.get('degradation_debt') or {}
    for k in ['sharpness_debt','chroma_gamma_drift_debt','noise_debt','identity_debt']:
        try: v=float(debt.get(k)); ok=0<=v<=1
        except Exception: ok=False
        if not ok: issues.append({'type':'TEMPORAL_DEGRADATION_DEBT_INVALID','field':k})
    if debt.get('generation_depth')!=depth: issues.append({'type':'TEMPORAL_DEGRADATION_DEPTH_MISMATCH','expected':depth,'actual':debt.get('generation_depth')})
    actual=fingerprint(d,'snapshot_fingerprint')
    if d.get('snapshot_fingerprint')!=actual: issues.append({'type':'CONTINUITY_SNAPSHOT_FINGERPRINT_INVALID','expected':actual,'actual':d.get('snapshot_fingerprint')})
    return {'pass':not issues,'issues':issues,'snapshot':d,'path':str(path),'fingerprint':actual}
