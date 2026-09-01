#!/usr/bin/env python3
"""Render an approved/planned SPATIAL_CANON planning diagram to deterministic SVG.

This is a planning artifact only. Text/arrows are allowed here because the SVG is
not a storyboard or video-conditioning visual reference.
"""
from __future__ import annotations
import argparse, html
from pathlib import Path
import yaml

def load(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))
def esc(x): return html.escape(str(x or ''))
def pt(x,y,w,h,m=55): return (m+x*(w-2*m), m+y*(h-2*m))
def arrow_marker():
    return '<defs><marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#222"/></marker></defs>'

def render(spatial, diagram_id, width=1200, height=800):
    ds={d.get('diagram_id'):d for d in spatial.get('planning_diagrams') or []}; d=ds.get(diagram_id)
    if not d: raise SystemExit(f'unknown diagram_id: {diagram_id}')
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',arrow_marker(),'<rect width="100%" height="100%" fill="white"/>']
    out.append(f'<text x="30" y="35" font-size="24" font-family="sans-serif" font-weight="700">{esc(diagram_id)} · {esc(d.get("diagram_type"))}</text>')
    # floor/zone geometry
    for z in d.get('zone_boxes') or []:
        x,y=pt(z['x'],z['y'],width,height); ww=z['w']*(width-110); hh=z['h']*(height-110)
        out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{ww:.1f}" height="{hh:.1f}" fill="none" stroke="#222" stroke-width="3"/>')
        out.append(f'<text x="{x+10:.1f}" y="{y+28:.1f}" font-size="20" font-family="sans-serif">{esc(z.get("label") or z["zone_id"])}</text>')
    for a in d.get('anchor_points') or []:
        x,y=pt(a['x'],a['y'],width,height); out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="#222"/>')
        out.append(f'<text x="{x+12:.1f}" y="{y-8:.1f}" font-size="16" font-family="sans-serif">{esc(a.get("label") or a["anchor_id"])}</text>')
    # topology nodes/edges
    nodes={n['node_ref']:n for n in d.get('nodes') or []}
    for e in d.get('edges') or []:
        a=nodes.get(e['from_ref']); b=nodes.get(e['to_ref']);
        if not a or not b: continue
        x1,y1=pt(a['x'],a['y'],width,height); x2,y2=pt(b['x'],b['y'],width,height)
        marker=' marker-end="url(#arrow)"' if e.get('directed') else ''
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#222" stroke-width="3"{marker}/>')
        if e.get('label'):
            out.append(f'<text x="{(x1+x2)/2:.1f}" y="{(y1+y2)/2-10:.1f}" text-anchor="middle" font-size="16" font-family="sans-serif">{esc(e["label"])}</text>')
    for n in nodes.values():
        x,y=pt(n['x'],n['y'],width,height); out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="12" fill="white" stroke="#b3261e" stroke-width="4"/>')
        out.append(f'<text x="{x+18:.1f}" y="{y+6:.1f}" font-size="18" font-family="sans-serif">{esc(n.get("label") or n["node_ref"])}</text>')
    # north arrow
    if d.get('north_angle_deg') is not None:
        out.append(f'<text x="{width-75}" y="55" font-size="22" font-family="sans-serif" font-weight="700">N ↑</text>')
    if d.get('scale_note'):
        out.append(f'<text x="30" y="{height-25}" font-size="15" font-family="sans-serif">{esc(d["scale_note"])}</text>')
    out.append('</svg>'); return '\n'.join(out)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('spatial_canon'); ap.add_argument('diagram_id'); ap.add_argument('--output',required=True); ap.add_argument('--width',type=int,default=1200); ap.add_argument('--height',type=int,default=800); a=ap.parse_args()
    Path(a.output).write_text(render(load(a.spatial_canon),a.diagram_id,a.width,a.height),encoding='utf-8'); print(a.output)
if __name__=='__main__': main()
