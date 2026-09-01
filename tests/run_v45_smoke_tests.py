#!/usr/bin/env python3
from __future__ import annotations
import subprocess, sys
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
def run(*args,capture=False):
    cmd=[sys.executable,*map(str,args)]; print('$',*map(str,args)); return subprocess.run(cmd,check=True,cwd=ROOT,text=True,capture_output=capture)
def main():
    run(ROOT/'tests/run_v44_smoke_tests.py')
    run(ROOT/'validators/v45_architecture_lint.py','--root',ROOT,'--json')
    run(ROOT/'validators/state_schema_lint.py',ROOT/'state/shot_relation_graph.schema.yaml',ROOT/'tests/fixtures/shot_relation_graph.clue_reveal.valid.yaml','--json')
    run(ROOT/'validators/state_schema_lint.py',ROOT/'state/visual_asset_obligation.schema.yaml',ROOT/'tests/fixtures/visual_asset_obligation.clue_reveal.valid.yaml','--json')
    run(ROOT/'validators/state_schema_lint.py',ROOT/'runtime/video_conditioning_runtime.schema.yaml',ROOT/'tests/fixtures/video_conditioning_runtime.clue_reveal.valid.yaml','--json')
    run(ROOT/'validators/shot_relation_asset_obligation_lint.py','--graph',ROOT/'tests/fixtures/shot_relation_graph.clue_reveal.valid.yaml','--obligations',ROOT/'tests/fixtures/visual_asset_obligation.clue_reveal.valid.yaml','--phase','conditioning','--conditioning-runtime',ROOT/'tests/fixtures/video_conditioning_runtime.clue_reveal.valid.yaml')
    bad=subprocess.run([sys.executable,str(ROOT/'validators/shot_relation_asset_obligation_lint.py'),'--graph',str(ROOT/'tests/fixtures/shot_relation_graph.clue_reveal.valid.yaml'),'--obligations',str(ROOT/'tests/fixtures/visual_asset_obligation.clue_reveal.invalid_missing_relation_assets.yaml'),'--phase','freeze'],cwd=ROOT,text=True,capture_output=True)
    assert bad.returncode==2 and ('RELATION_ASSET_OBLIGATION_REF_MISSING' in bad.stdout or 'CLUE_VIEW_OR_LOCATION_PROOF_MISSING' in bad.stdout)
    for p in list((ROOT/'state').glob('*.schema.yaml'))+list((ROOT/'runtime').glob('*.schema.yaml')):
        Draft202012Validator.check_schema(yaml.safe_load(p.read_text(encoding='utf-8')))
    print('V4.5 smoke tests: PASS'); return 0
if __name__=='__main__': raise SystemExit(main())
