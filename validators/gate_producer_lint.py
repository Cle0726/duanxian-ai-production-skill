#!/usr/bin/env python3
"""Ensure every Stage 04/05 transition requirement has an explicit producer."""
import argparse, json, pathlib, yaml

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--workflow',default='controller/workflow_state_machine.yaml'); ap.add_argument('--registry',default='controller/gate_producer_registry.yaml'); a=ap.parse_args()
    wf=yaml.safe_load(open(a.workflow,encoding='utf-8')); gr=yaml.safe_load(open(a.registry,encoding='utf-8')); producers=gr.get('producers') or {}; states=wf.get('states') or {}; issues=[]
    for t in wf.get('transitions',[]):
        srcs=t.get('from_any') or ([t.get('from')] if t.get('from') else []); relevant=False
        for s in srcs+[t.get('to')]:
            stage=str((states.get(s) or {}).get('stage',''))
            if stage.startswith('04') or stage=='05': relevant=True
        if not relevant: continue
        req=list(t.get('requires') or [])
        for xs in (t.get('conditional_requires') or {}).values(): req.extend(xs or [])
        for field in req:
            if field not in producers: issues.append({'type':'TRANSITION_GATE_PRODUCER_MISSING','transition':t.get('id'),'field':field})
    out={'pass':not issues,'issues':issues}; print(json.dumps(out,ensure_ascii=False,indent=2)); return 0 if not issues else 2
if __name__=='__main__': raise SystemExit(main())
