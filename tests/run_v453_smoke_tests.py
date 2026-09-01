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
    for lint in ['v44_architecture_lint.py','v45_architecture_lint.py','v451_architecture_lint.py','v452_architecture_lint.py','v453_architecture_lint.py']:
        run(ROOT/'validators'/lint,'--root',ROOT,'--json')
    for p in [ROOT/'state/visual_evidence.schema.yaml',ROOT/'runtime/visual_evidence_runtime.schema.yaml']:
        Draft202012Validator.check_schema(yaml.safe_load(p.read_text(encoding='utf-8')))
    run(ROOT/'validators/state_schema_lint.py',ROOT/'state/visual_evidence.schema.yaml',ROOT/'tests/fixtures/visual_evidence.valid.yaml','--json')
    run(ROOT/'validators/state_schema_lint.py',ROOT/'runtime/visual_evidence_runtime.schema.yaml',ROOT/'tests/fixtures/visual_evidence_runtime.valid.yaml','--json')
    run(ROOT/'validators/state_schema_lint.py',ROOT/'state/episode_state.schema.yaml',ROOT/'tests/fixtures/episode_state.text_only.valid.yaml','--json')
    run(ROOT/'validators/state_schema_lint.py',ROOT/'state/asset_registry.schema.yaml',ROOT/'tests/fixtures/asset_registry.visual_evidence.valid.yaml','--json')
    run(ROOT/'validators/state_schema_lint.py',ROOT/'runtime/reference_runtime.schema.yaml',ROOT/'tests/fixtures/reference_runtime.text_only.valid.yaml','--json')
    run(ROOT/'validators/visual_evidence_lint.py','--asset-registry',ROOT/'tests/fixtures/asset_registry.visual_evidence.valid.yaml','--evidence',ROOT/'tests/fixtures/visual_evidence.valid.yaml','--phase','capture')
    run(ROOT/'validators/visual_evidence_lint.py','--asset-registry',ROOT/'tests/fixtures/asset_registry.visual_evidence.valid.yaml','--evidence',ROOT/'tests/fixtures/visual_evidence.valid.yaml','--phase','reference','--reference-runtime',ROOT/'tests/fixtures/reference_runtime.text_only.valid.yaml')
    fail_contains([ROOT/'validators/visual_evidence_lint.py','--asset-registry',ROOT/'tests/fixtures/asset_registry.visual_evidence.valid.yaml','--evidence',ROOT/'tests/fixtures/visual_evidence.empty.yaml','--phase','reference','--reference-runtime',ROOT/'tests/fixtures/reference_runtime.text_only.missing_evidence.yaml'],'TEXT_ONLY_VISUAL_EVIDENCE_MISSING')
    fail_contains([ROOT/'validators/visual_evidence_lint.py','--asset-registry',ROOT/'tests/fixtures/asset_registry.visual_evidence.valid.yaml','--evidence',ROOT/'tests/fixtures/visual_evidence.stale.yaml','--phase','capture'],'VISUAL_EVIDENCE_STALE')
    fail_contains([ROOT/'validators/visual_evidence_lint.py','--asset-registry',ROOT/'tests/fixtures/asset_registry.visual_evidence.valid.yaml','--evidence',ROOT/'tests/fixtures/visual_evidence.conflict.yaml','--phase','reference','--reference-runtime',ROOT/'tests/fixtures/reference_runtime.text_only.valid.yaml'],'VISUAL_FACT_CONFLICT')
    print('V4.5.3 smoke tests: PASS')
if __name__=='__main__': raise SystemExit(main())
