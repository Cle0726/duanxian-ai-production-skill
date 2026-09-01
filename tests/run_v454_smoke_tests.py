#!/usr/bin/env python3
from __future__ import annotations
import subprocess,sys,tempfile,json
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
def run(*args):
    print('$',*map(str,args)); return subprocess.run([sys.executable,*map(str,args)],check=True,cwd=ROOT,text=True)
def fail_contains(args,needle):
    r=subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,text=True,capture_output=True)
    assert r.returncode==2,(r.returncode,r.stdout,r.stderr); assert needle in r.stdout,r.stdout

def main():
    run(ROOT/'validators/yaml_duplicate_key_lint.py',ROOT/'controller',ROOT/'state',ROOT/'runtime',ROOT/'adapters',ROOT/'tests/fixtures')
    for lint in ['v44_architecture_lint.py','v45_architecture_lint.py','v451_architecture_lint.py','v452_architecture_lint.py','v453_architecture_lint.py','v454_architecture_lint.py']:
        run(ROOT/'validators'/lint,'--root',ROOT,'--json')
    for p in list((ROOT/'state').glob('*.schema.yaml'))+list((ROOT/'runtime').glob('*.schema.yaml')):
        Draft202012Validator.check_schema(yaml.safe_load(p.read_text(encoding='utf-8')))
    for schema,fixture in [
        ('state/spatial_canon.schema.yaml','tests/fixtures/spatial_canon.required_views.valid.yaml'),
        ('state/asset_registry.schema.yaml','tests/fixtures/asset_registry.required_views.valid.yaml'),
        ('state/visual_evidence.schema.yaml','tests/fixtures/visual_evidence.required_views.valid.yaml')]:
        run(ROOT/'validators/state_schema_lint.py',ROOT/schema,ROOT/fixture,'--json')
    base=[ROOT/'validators/required_view_realization_lint.py','--spatial-canon',ROOT/'tests/fixtures/spatial_canon.required_views.valid.yaml']
    run(*base,'--asset-registry',ROOT/'tests/fixtures/asset_registry.required_views.valid.yaml','--phase','planning')
    run(*base,'--asset-registry',ROOT/'tests/fixtures/asset_registry.required_views.valid.yaml','--phase','build')
    run(*base,'--asset-registry',ROOT/'tests/fixtures/asset_registry.required_views.valid.yaml','--visual-evidence',ROOT/'tests/fixtures/visual_evidence.required_views.valid.yaml','--phase','freeze')
    fail_contains([*base,'--asset-registry',ROOT/'tests/fixtures/asset_registry.required_views.invalid_missing_forward.yaml','--phase','build'],'REQUIRED_VIEW_ASSET_MISSING')
    fail_contains([*base,'--asset-registry',ROOT/'tests/fixtures/asset_registry.required_views.valid.yaml','--visual-evidence',ROOT/'tests/fixtures/visual_evidence.required_views.invalid_wrong_forward.yaml','--phase','freeze'],'REQUIRED_VIEW_ROLE_VISUALLY_UNPROVEN')
    fail_contains([*base,'--asset-registry',ROOT/'tests/fixtures/asset_registry.required_views.invalid_starvation.yaml','--phase','build'],'COVERAGE_BUDGET_STARVES_REQUIRED_VIEW')
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)/'matrix.json'
        subprocess.run([sys.executable,str(ROOT/'tools/view_coverage_planner.py'),'--spatial-canon',str(ROOT/'tests/fixtures/spatial_canon.required_views.valid.yaml'),'--asset-registry',str(ROOT/'tests/fixtures/asset_registry.required_views.invalid_missing_forward.yaml'),'--output',str(out)],check=True,cwd=ROOT)
        obj=json.loads(out.read_text(encoding='utf-8')); assert obj['missing_count']==1; assert obj['generation_queue'][0]['view_requirement_id']=='VR_WAGON_FORWARD'
    print('V4.5.4 smoke tests: PASS')
if __name__=='__main__': raise SystemExit(main())
