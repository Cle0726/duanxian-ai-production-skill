#!/usr/bin/env python3
from __future__ import annotations
import subprocess,sys
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
    run(ROOT/'validators/v44_architecture_lint.py','--root',ROOT,'--json')
    run(ROOT/'validators/v45_architecture_lint.py','--root',ROOT,'--json')
    run(ROOT/'validators/v452_architecture_lint.py','--root',ROOT,'--json')
    for p in list((ROOT/'state').glob('*.schema.yaml'))+list((ROOT/'runtime').glob('*.schema.yaml')):
        Draft202012Validator.check_schema(yaml.safe_load(p.read_text(encoding='utf-8')))
    run(ROOT/'validators/state_schema_lint.py',ROOT/'state/spatial_canon.schema.yaml',ROOT/'tests/fixtures/spatial_canon.virtual_set.valid.yaml','--json')
    run(ROOT/'validators/state_schema_lint.py',ROOT/'runtime/spatial_canon_runtime.schema.yaml',ROOT/'tests/fixtures/spatial_canon_runtime.v452.valid.yaml','--json')
    run(ROOT/'validators/state_schema_lint.py',ROOT/'state/asset_registry.schema.yaml',ROOT/'tests/fixtures/asset_registry.virtual_set.valid.yaml','--json')
    run(ROOT/'validators/spatial_canon_lint.py','--spatial-canon',ROOT/'tests/fixtures/spatial_canon.virtual_set.valid.yaml')
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)/'topology.svg'
        subprocess.run([sys.executable,str(ROOT/'tools/spatial_diagram_renderer.py'),str(ROOT/'tests/fixtures/spatial_canon.virtual_set.valid.yaml'),'D_TOPO','--output',str(out)],check=True,cwd=ROOT)
        svg=out.read_text(encoding='utf-8'); assert '<svg' in svg and 'A 起点' in svg and '110m / 下坡' in svg
    fail_contains([ROOT/'validators/spatial_canon_lint.py','--spatial-canon',ROOT/'tests/fixtures/spatial_canon.virtual_set.invalid_route.yaml'],'CHARACTER_ROUTE_UNKNOWN_ANCHOR')
    run(ROOT/'validators/virtual_set_asset_lint.py','--spatial-canon',ROOT/'tests/fixtures/spatial_canon.virtual_set.valid.yaml','--asset-registry',ROOT/'tests/fixtures/asset_registry.virtual_set.valid.yaml','--phase','freeze')
    fail_contains([ROOT/'validators/virtual_set_asset_lint.py','--spatial-canon',ROOT/'tests/fixtures/spatial_canon.virtual_set.valid.yaml','--asset-registry',ROOT/'tests/fixtures/asset_registry.virtual_set.invalid_parentage.yaml','--phase','build'],'COVERAGE_VISUAL_PARENT_MISSING')
    fail_contains([ROOT/'validators/virtual_set_asset_lint.py','--spatial-canon',ROOT/'tests/fixtures/spatial_canon.virtual_set.valid.yaml','--asset-registry',ROOT/'tests/fixtures/asset_registry.virtual_set.invalid_justification.yaml','--phase','build'],'ASSET_WHY_REQUIRED_MISSING')
    print('V4.5.2 smoke tests: PASS')
if __name__=='__main__': raise SystemExit(main())
