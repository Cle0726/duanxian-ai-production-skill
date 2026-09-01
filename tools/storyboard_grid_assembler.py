#!/usr/bin/env python3
"""Assemble already-clean storyboard panels into a plain deterministic grid.

No text, numbering, arrows, timestamps, CUT labels, captions, or decorative frame
chrome are added. An optional manifest records input order and SHA-256 hashes so
GENERATION_ENVELOPE can prove that a multishot grid uses exactly the approved
CUT panels in exactly CUT order.
"""
from __future__ import annotations
import argparse, hashlib, json, math
from pathlib import Path
from PIL import Image


def sha256_path(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('panels',nargs='+')
    ap.add_argument('--output',required=True)
    ap.add_argument('--columns',type=int,default=0)
    ap.add_argument('--gap',type=int,default=12)
    ap.add_argument('--background',default='white')
    ap.add_argument('--manifest-output')
    a=ap.parse_args()
    panel_paths=[Path(p) for p in a.panels]
    for p in panel_paths:
        if not p.is_file(): raise SystemExit(f'panel not found: {p}')
    imgs=[Image.open(p).convert('RGB') for p in panel_paths]
    if not imgs: raise SystemExit('no panels')
    w=max(i.width for i in imgs); h=max(i.height for i in imgs)
    cols=a.columns or math.ceil(math.sqrt(len(imgs))); rows=math.ceil(len(imgs)/cols)
    if cols < 1: raise SystemExit('columns must be >=1')
    canvas=Image.new('RGB',(cols*w+(cols-1)*a.gap,rows*h+(rows-1)*a.gap),a.background)
    for idx,img in enumerate(imgs):
        if img.size!=(w,h):
            copy=Image.new('RGB',(w,h),a.background)
            x=(w-img.width)//2; y=(h-img.height)//2
            copy.paste(img,(x,y)); img=copy
        r,c=divmod(idx,cols)
        canvas.paste(img,(c*(w+a.gap),r*(h+a.gap)))
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); canvas.save(out)
    manifest={
        'schema_version':1,
        'assembler_tool':'tools/storyboard_grid_assembler.py',
        'panel_count':len(panel_paths),
        'columns':cols,
        'rows':rows,
        'gap':a.gap,
        'output_path':str(out),
        'output_sha256':sha256_path(out),
        'source_panels_ordered':[
            {'path':str(p),'sha256':sha256_path(p)} for p in panel_paths
        ],
    }
    if a.manifest_output:
        mp=Path(a.manifest_output); mp.parent.mkdir(parents=True,exist_ok=True)
        mp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(manifest,ensure_ascii=False))

if __name__=='__main__': main()
