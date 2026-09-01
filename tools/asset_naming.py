#!/usr/bin/env python3
"""Deterministic default names for 《断弦之歌》 production artifacts."""
from __future__ import annotations
import argparse, re

SAFE = re.compile(r"[^A-Za-z0-9_-]+")

def clean(s: str) -> str:
    return SAFE.sub("-", s.strip()).strip("-") or "UNK"

def build(kind: str, episode: str, scene: str | None, segment: str | None, shot: str | None, version: int, take: int | None) -> str:
    ep, sc, seg, sh = map(clean, [episode, scene or "NA", segment or "NA", shot or "NA"])
    v = f"v{version:03d}"
    if kind == "storyboard": return f"DSG_{ep}_{sc}_{seg}_SB_{v}.png"
    if kind == "video": return f"DSG_{ep}_{sc}_{seg}_VID_TAKE{(take or 1):02d}.mp4"
    if kind == "ending": return f"DSG_{ep}_{sc}_{seg}_END_{v}.png"
    if kind == "anchor": return f"ANCHOR_{ep}_{sc}_{sh}_HD_{v}.png"
    if kind == "assembly": return f"ASM_{ep}_{sc}_{sh}_{v}.png"
    if kind == "support": return f"SUP_{ep}_{sh}_{v}.png"
    raise ValueError(f"unsupported kind: {kind}")

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("kind", choices=["storyboard","video","ending","anchor","assembly","support"])
    ap.add_argument("--episode", required=True)
    ap.add_argument("--scene")
    ap.add_argument("--segment")
    ap.add_argument("--shot")
    ap.add_argument("--version", type=int, default=1)
    ap.add_argument("--take", type=int)
    a=ap.parse_args()
    print(build(a.kind,a.episode,a.scene,a.segment,a.shot,a.version,a.take))
    return 0
if __name__ == "__main__": raise SystemExit(main())
