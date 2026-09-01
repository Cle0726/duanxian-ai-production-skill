#!/usr/bin/env python3
from pathlib import Path
import subprocess, sys, json, yaml
ROOT=Path(__file__).resolve().parents[1]
PY=sys.executable

def run(cmd, expect=0):
    p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
    if p.returncode!=expect:
        raise AssertionError(f"cmd={cmd}\nreturn={p.returncode}\nstdout={p.stdout}\nstderr={p.stderr}")
    return p

run([PY,'validators/state_schema_lint.py','state/editorial_plan.schema.yaml','tests/fixtures/editorial_plan.valid.yaml','--json'])
run([PY,'validators/editorial_plan_lint.py','--plan','tests/fixtures/editorial_plan.valid.yaml'])
p=run([PY,'validators/editorial_plan_lint.py','--plan','tests/fixtures/editorial_plan.invalid.yaml'],expect=2)
out=json.loads(p.stdout)
assert any(x['type']=='EDITORIAL_PLAN_NOT_LOCKED' for x in out['findings'])
assert any(x['type']=='EDITORIAL_EDIT_POINT_GAP' for x in out['findings'])
assert any(x['type']=='VIEWPOINT_STAGNATION_RISK' for x in out['findings'])

route=yaml.safe_load((ROOT/'controller/route_registry.yaml').read_text(encoding='utf-8'))
auth=yaml.safe_load((ROOT/'controller/authority_registry.yaml').read_text(encoding='utf-8'))
assert auth['authorities']['editorial_grammar']['owner']=='templates/editorial_grammar_engine.md'
assert 'EDITORIAL_PLAN' in route['routes']['STAGE_02B_DIRECTOR_ARCHITECTURE']['produces_structured_artifacts']
assert 'EDITORIAL_PLAN' in route['routes']['STAGE_04_STORYBOARD']['structured_inputs']
assert 'EDITORIAL_PLAN' in route['routes']['STAGE_05_VIDEO']['structured_inputs']
assert 'EDITORIAL_PLAN' in route['routes']['STAGE_06_POST']['structured_inputs']
assert route['structured_artifacts']['EDITORIAL_PLAN']=='state/editorial_plan.schema.yaml'
print('EDITORIAL UPGRADE TESTS PASS')
