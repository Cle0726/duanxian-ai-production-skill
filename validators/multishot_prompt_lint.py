#!/usr/bin/env python3
"""Ensure final video prompt respects GENERATION_ENVELOPE cut count and mode."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
import yaml

MULTI={'SEQUENTIAL_MULTISHOT','TIMED_MULTISHOT','FREESTYLE_BROLL'}

def load(p):
    text=Path(p).read_text(encoding='utf-8')
    return json.loads(text) if Path(p).suffix.lower()=='.json' else yaml.safe_load(text)

def lint(text,envelope):
    issues=[]; mode=envelope.get('format_mode'); cuts=envelope.get('cut_contracts') or []
    # CUT labels must be explicit in multishot prompts. Accept CUT 1 / CUT1 / CUT_1.
    labels=[int(x) for x in re.findall(r'(?im)\bCUT[ _-]?(\d+)\b',text)]
    unique=[]
    for x in labels:
        if x not in unique: unique.append(x)
    if mode=='ONER':
        if any(x>1 for x in unique): issues.append({'type':'ONER_PROMPT_CONTAINS_EXTRA_CUT','cuts':unique})
        if not re.search(r'(?i)NO\s*CUT|无切镜|不切镜|一镜到底',text):
            issues.append({'type':'ONER_PROMPT_NO_CUT_LOCK_MISSING'})
    elif mode in MULTI:
        expected=list(range(1,len(cuts)+1))
        if unique!=expected:
            issues.append({'type':'MULTISHOT_PROMPT_CUT_COUNT_OR_ORDER_MISMATCH','expected':expected,'actual':unique})
        if not re.search(r'(?i)FORMAT\s*MODE|多镜头|MULTISHOT|SEQUENCE\s+OF\s+(?:SPECIFIED\s+)?CUTS',text):
            issues.append({'type':'MULTISHOT_PROMPT_FORMAT_MODE_SURFACE_MISSING','format_mode':mode})
        # Explicitly lock no extra cuts. Chinese/English accepted.
        if not re.search(r'(?i)只(?:能|允许).*切|不得.*新增.*(?:CUT|切镜)|cuts?\s+only\s+at|exact\s+cut\s+count|仅在.*切',text):
            issues.append({'type':'MULTISHOT_PROMPT_CUT_BOUNDARY_LOCK_MISSING'})
        if mode=='TIMED_MULTISHOT':
            for c in sorted(cuts,key=lambda x:x.get('order',9999)):
                s=c.get('start_sec'); e=c.get('end_sec')
                if s is None or e is None: continue
                pats=[
                    rf'{re.escape(str(s))}\s*[–\-~至]\s*{re.escape(str(e))}\s*s',
                    rf'{float(s):g}\s*[–\-~至]\s*{float(e):g}\s*s',
                ]
                if not any(re.search(p,text,re.I) for p in pats):
                    issues.append({'type':'TIMED_MULTISHOT_PROMPT_WINDOW_MISSING','cut_id':c.get('cut_id'),'start':s,'end':e})
    else:
        issues.append({'type':'MULTISHOT_PROMPT_UNKNOWN_FORMAT_MODE','format_mode':mode})
    return {'pass':not issues,'format_mode':mode,'detected_cuts':unique,'issues':issues}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--prompt',required=True); ap.add_argument('--envelope',required=True); a=ap.parse_args()
    out=lint(Path(a.prompt).read_text(encoding='utf-8'),load(a.envelope)); print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['pass'] else 2)
if __name__=='__main__': main()
