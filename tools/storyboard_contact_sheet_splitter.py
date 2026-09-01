#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from PIL import Image

def sha256(p: Path) -> str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(65536), b''): h.update(chunk)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser(description='Deterministically split storyboard contact sheet into panel images.')
    ap.add_argument('image')
    ap.add_argument('--rows', type=int, required=True)
    ap.add_argument('--cols', type=int, required=True)
    ap.add_argument('--output-dir', required=True)
    ap.add_argument('--prefix', default='panel')
    ap.add_argument('--manifest-output', required=True)
    ap.add_argument('--gap', type=int, default=0, help='uniform inter-cell gap pixels')
    a=ap.parse_args()
    src=Path(a.image); outdir=Path(a.output_dir); outdir.mkdir(parents=True, exist_ok=True)
    im=Image.open(src).convert('RGB'); w,h=im.size
    cell_w=(w - (a.cols-1)*a.gap)//a.cols; cell_h=(h - (a.rows-1)*a.gap)//a.rows
    manifest={'splitter_tool':'tools/storyboard_contact_sheet_splitter.py','source_image':str(src),'source_sha256':sha256(src),'rows':a.rows,'cols':a.cols,'gap':a.gap,'panels':[]}
    idx=1
    for r in range(a.rows):
        for c in range(a.cols):
            left=c*(cell_w+a.gap); upper=r*(cell_h+a.gap); right=left+cell_w; lower=upper+cell_h
            panel=im.crop((left,upper,right,lower))
            name=f"{a.prefix}_{idx:02d}.png"; path=outdir/name; panel.save(path)
            manifest['panels'].append({'index':idx,'row':r+1,'col':c+1,'file_path':str(path),'sha256':sha256(path)})
            idx+=1
    Path(a.manifest_output).write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'ok':True,'panel_count':len(manifest['panels']),'manifest':str(Path(a.manifest_output))}, ensure_ascii=False))

if __name__=='__main__': main()
