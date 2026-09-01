#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from PIL import Image

def sha256(p: Path) -> str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser(description='Create a deterministic platform-effective preview for identity readability QC.')
    ap.add_argument('image')
    ap.add_argument('--effective-width', type=int, required=True)
    ap.add_argument('--effective-height', type=int, required=True)
    ap.add_argument('--basis', choices=['PLATFORM_ACTUAL_SCALE','PLATFORM_PROFILE_SIMULATION'], required=True)
    ap.add_argument('--profile-id', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--manifest-output', required=True)
    a=ap.parse_args()
    src=Path(a.image); out=Path(a.output); out.parent.mkdir(parents=True, exist_ok=True)
    im=Image.open(src).convert('RGB')
    sw,sh=im.size
    # Fit inside the platform-effective canvas while preserving aspect ratio; no sharpening/upscale tricks.
    scale=min(a.effective_width/sw, a.effective_height/sh)
    nw=max(1,round(sw*scale)); nh=max(1,round(sh*scale))
    resized=im.resize((nw,nh), Image.Resampling.LANCZOS)
    canvas=Image.new('RGB',(a.effective_width,a.effective_height),'black')
    ox=(a.effective_width-nw)//2; oy=(a.effective_height-nh)//2
    canvas.paste(resized,(ox,oy)); canvas.save(out)
    manifest={
      'tool':'tools/platform_scaled_readability_preview.py',
      'source_path':str(src),'source_sha256':sha256(src),'source_width_px':sw,'source_height_px':sh,
      'profile_id':a.profile_id,'evaluation_basis':a.basis,
      'effective_width_px':a.effective_width,'effective_height_px':a.effective_height,
      'content_width_px':nw,'content_height_px':nh,'scale_factor':scale,
      'output_path':str(out),'output_sha256':sha256(out)
    }
    Path(a.manifest_output).write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(manifest,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
