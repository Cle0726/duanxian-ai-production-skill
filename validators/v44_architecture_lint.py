#!/usr/bin/env python3
"""Validate V4.4 control-plane invariants and route references."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
import yaml


def load(path: Path):
    with path.open(encoding="utf-8") as f: return yaml.safe_load(f)

def iter_route_paths(route):
    keys=("source","source_if_missing_or_stale","compile_runtime_from_source","execute_with","validators")
    for k in keys:
        for p in route.get(k,[]) or []: yield p
    cond=route.get("conditional_source",{}) or {}
    for vals in cond.values():
        for p in vals or []: yield p

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[1]); ap.add_argument("--json",action="store_true")
    a=ap.parse_args(); root=a.root.resolve(); errors=[]; warnings=[]
    rr=load(root/"controller/route_registry.yaml"); wf=load(root/"controller/workflow_state_machine.yaml"); ar=load(root/"controller/authority_registry.yaml"); mm=load(root/"controller/module_manifest.yaml")
    supported_versions={"4.4.0","4.5.0","4.5.1","4.5.2","4.5.3","4.5.4","4.5.5","4.5.6","4.5.7","4.5.8","4.5.9","4.5.10","4.5.11"}
    if rr.get("skill_version") not in supported_versions: errors.append("route_registry unsupported skill_version")
    if wf.get("skill_version") not in supported_versions: errors.append("workflow unsupported skill_version")
    if ar.get("skill_version") not in supported_versions: errors.append("authority_registry unsupported skill_version")
    routes=rr.get("routes",{})
    for rname, route in routes.items():
        for rel in iter_route_paths(route):
            if not (root/rel).exists(): errors.append(f"{rname}: missing path {rel}")
        nr=route.get("next_route")
        if nr and nr not in routes: errors.append(f"{rname}: unknown next_route {nr}")
    states=set((wf.get("states") or {}).keys())
    # V4.4: Approved storyboard may never transition directly to VIDEO_GENERATION_READY.
    for t in wf.get("transitions",[]):
        if t.get("from")=="APPROVED_PREVIS_SET" and t.get("to")=="VIDEO_GENERATION_READY":
            errors.append(f"{t.get('id')}: direct APPROVED_PREVIS_SET -> VIDEO_GENERATION_READY bypasses mandatory Video Conditioning")
    for t in wf.get("transitions",[]):
        if t.get("from") and t["from"] not in states: errors.append(f"{t.get('id')}: unknown from {t['from']}")
        for s in t.get("from_any",[]) or []:
            if s not in states: errors.append(f"{t.get('id')}: unknown from_any {s}")
        if t.get("to") not in states: errors.append(f"{t.get('id')}: unknown to {t.get('to')}")
        if t.get("route") not in routes: errors.append(f"{t.get('id')}: unknown route {t.get('route')}")
    for name, item in (ar.get("authorities") or {}).items():
        owner=item.get("owner")
        if not owner or not (root/owner).exists(): errors.append(f"authority {name}: missing owner {owner}")
    manifest=[]
    for cname, block in (mm.get("classes") or {}).items():
        for mod in block.get("modules",[]) or []:
            manifest.append(mod)
    actual=[p.name for p in (root/"templates").glob("*.md")]
    if len(manifest)!=len(set(manifest)): errors.append("module_manifest contains duplicate module entries")
    missing=sorted(set(actual)-set(manifest)); extra=sorted(set(manifest)-set(actual))
    if missing: errors.append(f"module_manifest missing templates: {missing}")
    if extra: errors.append(f"module_manifest unknown templates: {extra}")
    skill=(root/"SKILL.md").read_text(encoding="utf-8")
    direct_templates=set(re.findall(r'`?(templates/[A-Za-z0-9_\-\u4e00-\u9fff]+\.md)`?', skill))
    if len(direct_templates)>20: warnings.append(f"SKILL.md direct template refs={len(direct_templates)}; target <=20")
    result={"errors":errors,"warnings":warnings,"route_count":len(routes),"state_count":len(states),"template_manifest_count":len(manifest),"skill_direct_template_refs":len(direct_templates)}
    print(json.dumps(result,ensure_ascii=False,indent=2) if a.json else result)
    return 1 if errors else 0
if __name__=="__main__": raise SystemExit(main())
